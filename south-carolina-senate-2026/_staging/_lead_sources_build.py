#!/usr/bin/env python3
"""Build the Lead-owned source registry from the mirrored Wikipedia citation list.

Input : _staging/mirrors/refs_urls.csv  (section_index, section_title, url)
Output: _staging/_lead_sources.csv      (SRC-1900 … SRC-2999)
        _staging/_lead_url_index.json   (normalised url -> source_id)

This is deliberately mechanical: publisher and tier are derived from the domain by rule,
title stays `unknown` unless it is later hand-filled, and every row records the Wikipedia
section that cited it so a reviewer can go straight back. Nothing is invented — a URL only
enters the registry because the article cited it.
"""
import csv
import json
import os
import re
import sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
MIR = os.path.join(HERE, "mirrors")

TIER1 = {"scvotes.gov", "fec.gov", "senate.gov", "congress.gov", "govinfo.gov", "whitehouse.gov",
         "sc.gov", "house.gov", "census.gov", "supremecourt.gov"}
TIER2 = {"nytimes.com", "washingtonpost.com", "wsj.com", "apnews.com", "reuters.com",
         "cbsnews.com", "nbcnews.com", "cnn.com", "abcnews.go.com", "politico.com", "thehill.com",
         "pbs.org", "npr.org", "time.com", "usatoday.com", "theguardian.com", "bbc.com",
         "bloomberg.com", "axios.com", "motherjones.com", "propublica.org", "rollcall.com",
         "postandcourier.com", "thestate.com", "scdailygazette.com", "greenvilleonline.com",
         "goupstate.com", "fitsnews.com", "wistv.com", "abcnews4.com", "wbtw.com", "wmbfnews.com",
         "foxcarolina.com", "live5news.com", "wyff4.com", "katv.com", "wrhi.com", "wcsc.com",
         "washingtonexaminer.com", "washingtontimes.com", "decisiondeskhq.com", "cookpolitical.com",
         "sabato", "insideelections.com", "emilyslist.org", "314action.org", "sbaprolife.org",
         "punchbowl.news", "justthenews.com", "washingtonreporter.news", "devdiscourse.com",
         "theminorityeye.com", "ebony.com", "c-span.org", "youtube.com", "commons.wikimedia.org",
         "wikipedia.org"}

PUBLISHER = {
    "nytimes.com": "The New York Times", "washingtonpost.com": "The Washington Post",
    "wsj.com": "The Wall Street Journal", "apnews.com": "Associated Press",
    "reuters.com": "Reuters", "cbsnews.com": "CBS News", "nbcnews.com": "NBC News",
    "cnn.com": "CNN", "abcnews.go.com": "ABC News", "politico.com": "Politico",
    "thehill.com": "The Hill", "pbs.org": "PBS NewsHour", "npr.org": "NPR", "time.com": "Time",
    "usatoday.com": "USA Today", "theguardian.com": "The Guardian", "bbc.com": "BBC",
    "bloomberg.com": "Bloomberg", "axios.com": "Axios", "motherjones.com": "Mother Jones",
    "propublica.org": "ProPublica", "rollcall.com": "Roll Call",
    "postandcourier.com": "The Post and Courier", "thestate.com": "The State",
    "scdailygazette.com": "South Carolina Daily Gazette", "greenvilleonline.com": "The Greenville News",
    "goupstate.com": "Spartanburg Herald-Journal", "fitsnews.com": "FITSNews", "wistv.com": "WIS-TV",
    "abcnews4.com": "WCIV ABC News 4", "wbtw.com": "WBTW News13", "wmbfnews.com": "WMBF News",
    "foxcarolina.com": "FOX Carolina", "live5news.com": "Live 5 WCSC", "wyff4.com": "WYFF4",
    "katv.com": "ABC7 KATV", "wrhi.com": "WRHI", "washingtonexaminer.com": "Washington Examiner",
    "washingtontimes.com": "The Washington Times", "decisiondeskhq.com": "Decision Desk HQ",
    "emilyslist.org": "EMILYs List", "314action.org": "314 Action", "sbaprolife.org":
    "Susan B. Anthony Pro-Life America", "punchbowl.news": "Punchbowl News",
    "justthenews.com": "Just the News", "washingtonreporter.news": "Washington Reporter",
    "devdiscourse.com": "Devdiscourse", "theminorityeye.com": "The MinorityEye", "ebony.com": "EBONY",
    "c-span.org": "C-SPAN", "youtube.com": "YouTube", "scvotes.gov": "South Carolina Election Commission",
    "fec.gov": "Federal Election Commission", "senate.gov": "U.S. Senate", "congress.gov": "Congress.gov",
    "commons.wikimedia.org": "Wikimedia Commons", "wikipedia.org": "Wikipedia",
    "drannieandrews.com": "Annie Andrews for Senate", "darlinegraham.com": "Darline Graham for Senate",
}

# url fragments that are not usable as a citation for this archive
SKIP = ("doi.org", "jstor.org", "archive.org/wayback", "web.archive.org", "books.google",
        "linkedin.com", "facebook.com", "instagram.com", "tiktok.com", "x.com/", "twitter.com/",
        "ballotpedia.org/Sample", "ourcampaigns.com/Race")


def host(u):
    try:
        h = urlparse(u).hostname or ""
    except ValueError:
        return ""
    return h.lower().replace("www.", "")


def tier_for(h):
    for d in TIER1:
        if h == d or h.endswith("." + d):
            return "T1"
    for d in TIER2:
        if h == d or h.endswith("." + d):
            return "T2"
    return "T3"


def type_for(h, u):
    if h.endswith("scvotes.gov") or h.endswith("fec.gov") or h.endswith("senate.gov"):
        return "official_government"
    if h.endswith("commons.wikimedia.org") or re.search(r"\.(jpg|jpeg|png|svg|webp)$", u, re.I):
        return "photo"
    if "youtube.com" in h or "c-span.org" in h:
        return "news_video"
    if h.endswith("emilyslist.org") or h.endswith("314action.org") or h.endswith("sbaprolife.org"):
        return "press_release"
    if h.endswith("wikipedia.org"):
        return "other"
    return "news_article"


def publisher_for(h):
    for d, p in PUBLISHER.items():
        if h == d or h.endswith("." + d):
            return p
    return h or "unknown"


def norm(u):
    u = u.strip()
    u = re.sub(r"[?#].*$", "", u)
    u = re.sub(r"^https?://(www\.)?", "", u, flags=re.I)
    return u.rstrip("/").lower()


def main():
    src = os.path.join(MIR, "refs_urls.csv")
    rows = list(csv.DictReader(open(src, encoding="utf-8")))
    seen = {}
    out = []
    n = 1900
    for r in rows:
        u = r["url"].strip()
        if not u.startswith("http"):
            continue
        if any(s in u for s in SKIP):
            continue
        k = norm(u)
        if k in seen:
            continue
        h = host(u)
        if not h:
            continue
        sid = f"SRC-{n:04d}"
        n += 1
        seen[k] = sid
        out.append({
            "source_id": sid,
            "url": u,
            "title": "unknown",
            "publisher": publisher_for(h),
            "publication_date": "unknown",
            "event_date": "unknown",
            "access_date": "2026-11-12",
            "source_tier": tier_for(h),
            "source_type": type_for(h, u),
            "relevant_quote_or_info": f"cited by Wikipedia section {r['section_index']} ({r['section_title']})",
            "reliability_notes": f"harvested from the Wikipedia {{cite}} list, section {r['section_index']}; title not captured",
            "used_by": "Lead",
        })

    if n > 2999:
        print(f"WARNING: source ids exceeded the reserved block (last {n - 1})")

    dst = os.path.join(HERE, "_lead_sources.csv")
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["source_id", "url", "title", "publisher",
                                          "publication_date", "event_date", "access_date",
                                          "source_tier", "source_type", "relevant_quote_or_info",
                                          "reliability_notes", "used_by"], lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    with open(os.path.join(HERE, "_lead_url_index.json"), "w", encoding="utf-8") as f:
        json.dump(seen, f, indent=1, ensure_ascii=False)

    tiers = {}
    for r in out:
        tiers[r["source_tier"]] = tiers.get(r["source_tier"], 0) + 1
    print(f"{dst}: {len(out)} sources, tiers {dict(sorted(tiers.items()))}, ids SRC-1900..SRC-{n-1:04d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
