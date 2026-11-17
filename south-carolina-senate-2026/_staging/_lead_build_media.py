#!/usr/bin/env python3
"""Build the media-coverage register and the (thin, honest) ads/social tables.

The coverage register is an *index*, not a set of read articles: each row is a URL the race
article cited, with its publisher and tier resolved from the domain, and with every content
column explicitly `unknown` because the body was not retrieved in this pass. Recording that
plainly is more useful than inventing framing labels.

Run: python _staging/_lead_build_media.py
"""
import csv
import os
import re
import sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MIR = os.path.join(HERE, "mirrors")
OUT = os.path.join(ROOT, "05_campaign_media")

COV_HEADER = ["coverage_id", "candidate_id", "event_id", "publication_date", "outlet", "author",
              "title", "url", "source_tier", "coverage_type", "key_framing", "notable_quotes",
              "framing_of_candidate", "mentions_opponent", "reliability_notes"]
AD_HEADER = ["ad_id", "candidate_id", "sponsor", "sponsor_type", "release_date", "title",
             "platform", "length_seconds", "issue_or_message", "main_visual_elements",
             "narration_soundtrack", "candidate_appearance", "main_claims", "video_url",
             "transcript_url", "fact_check", "media_coverage", "source_urls", "verification_status",
             "notes"]
SOC_HEADER = ["post_id", "candidate_id", "platform", "account_handle", "post_date", "post_type",
              "content_summary", "media_included", "engagement_notes", "url", "verification_status",
              "notes"]

PUBLISHER = {
    "nytimes.com": "The New York Times", "washingtonpost.com": "The Washington Post",
    "apnews.com": "Associated Press", "cbsnews.com": "CBS News", "nbcnews.com": "NBC News",
    "cnn.com": "CNN", "politico.com": "Politico", "thehill.com": "The Hill", "pbs.org": "PBS NewsHour",
    "time.com": "Time", "usatoday.com": "USA Today", "theguardian.com": "The Guardian",
    "postandcourier.com": "The Post and Courier", "thestate.com": "The State",
    "scdailygazette.com": "South Carolina Daily Gazette", "greenvilleonline.com": "The Greenville News",
    "goupstate.com": "Spartanburg Herald-Journal", "fitsnews.com": "FITSNews",
    "wistv.com": "WIS-TV", "abcnews4.com": "WCIV ABC News 4", "wbtw.com": "WBTW News13",
    "wmbfnews.com": "WMBF News", "foxcarolina.com": "FOX Carolina", "live5news.com": "Live 5 WCSC",
    "wyff4.com": "WYFF4", "ebony.com": "EBONY", "theminorityeye.com": "The MinorityEye",
    "motherjones.com": "Mother Jones", "washingtonexaminer.com": "Washington Examiner",
    "washingtontimes.com": "The Washington Times", "washingtonreporter.news": "Washington Reporter",
    "devdiscourse.com": "Devdiscourse", "justthenews.com": "Just the News",
    "decisiondeskhq.com": "Decision Desk HQ", "cookpolitical.com": "Cook Political Report",
    "emilyslist.org": "EMILYs List", "314action.org": "314 Action", "scetv.org": "South Carolina ETV",
    "wrhi.com": "WRHI", "katv.com": "ABC7 KATV", "punchbowl.news": "Punchbowl News",
    "ms.now": "MS NOW", "natesilver.net": "Silver Bulletin", "fiftyplusone.news": "FiftyPlusOne",
    "insideelections.com": "Inside Elections", "centerforpolitics.org": "Sabato's Crystal Ball",
    "realclearpolling.com": "RealClearPolitics", "foxnews.com": "Fox News",
    "theeconomist.com": "The Economist", "economist.com": "The Economist",
}
TIER1 = {"scvotes.gov", "fec.gov", "senate.gov", "scetv.org", "c-span.org"}
TIER2 = set(PUBLISHER) - {"emilyslist.org", "314action.org", "punchbowl.news", "justthenews.com",
                          "washingtonreporter.news", "devdiscourse.com"}
ANALYSIS_SECTIONS = {"52", "59", "60", "53"}


def host(u):
    try:
        return (urlparse(u).hostname or "").lower().replace("www.", "")
    except ValueError:
        return ""


def publisher_for(h):
    for d, p in PUBLISHER.items():
        if h == d or h.endswith("." + d):
            return p
    return h or "unknown"


def tier_for(h):
    if any(h == d or h.endswith("." + d) for d in TIER1):
        return "T1"
    if any(h == d or h.endswith("." + d) for d in TIER2):
        return "T2"
    return "T3"


def subject(url, section):
    u = url.lower()
    a = "andrews" in u or "annie" in u
    g = "graham" in u or "darline" in u
    if a and not g:
        return "ANDREWS"
    if g and not a:
        return "GRAHAM"
    return None


def build_coverage():
    rows = list(csv.DictReader(open(os.path.join(MIR, "refs_urls.csv"), encoding="utf-8")))
    seen = set()
    buckets = {"ANDREWS": [], "GRAHAM": []}
    for r in rows:
        u = r["url"].strip()
        h = host(u)
        if not h or "wikipedia.org" in h or "wikimedia" in h:
            continue
        cand = subject(u, r["section_index"])
        if not cand:
            continue
        key = re.sub(r"[?#].*$", "", u).lower()
        if key in seen:
            continue
        seen.add(key)
        sec = r["section_index"]
        buckets[cand].append({
            "candidate_id": cand,
            "event_id": "unknown",
            "publication_date": "unknown",
            "outlet": publisher_for(h),
            "author": "unknown",
            "title": "unknown",
            "url": u,
            "source_tier": tier_for(h),
            "coverage_type": "analysis" if sec in ANALYSIS_SECTIONS else "news_report",
            "key_framing": "unknown",
            "notable_quotes": "unknown",
            "framing_of_candidate": "unknown",
            "mentions_opponent": "unknown",
            "reliability_notes": f"cited by the race article in section {sec}; URL and publisher "
                                 f"resolved from the domain, article body not retrieved in this pass",
            "_sec": int(sec) if sec.isdigit() else 999,
        })
    # balance the register instead of letting the Graham-heavy GOP sections fill the quota first
    out = []
    per_cap = 24
    for cand in ("ANDREWS", "GRAHAM"):
        bucket = sorted(buckets[cand], key=lambda x: ({"T1": 0, "T2": 1}.get(x["source_tier"], 2),
                                                      x["_sec"]))
        chosen = bucket[:per_cap]
        for row in chosen:
            row.pop("_sec", None)
            row["coverage_id"] = f"COV-{len(out) + 1:04d}"
            out.append(row)
        print(f"  {cand}: {len(bucket)} candidate-specific links available, {len(chosen)} kept")
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "media_coverage.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COV_HEADER, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    print(f"media_coverage.csv: {len(out)} rows {dict(Counter(r['candidate_id'] for r in out))}")


def build_ads():
    """Only what a source actually states: sponsor, date, reported spend, 口径. No creative."""
    rows = [
        ["EXT-AD-0001", "GRAHAM", "MAGA Inc.", "outside_pac", "2026-08", "unknown", "unknown",
         "unknown", "unknown", "unknown", "unknown", "unknown",
         "reported $827,000 in support of Darline Graham in August 2026", "unknown", "unknown",
         "unknown", "SRC-2111|https://www.cbsnews.com/news/south-carolina-2026-senate-annie-andrews-darline-graham/",
         "partially verified",
         "an independent-expenditure transfer figure reported by CBS, not an ad flight; creative "
         "and placement are unknown"],
        ["EXT-AD-0002", "GRAHAM", "Senate Leadership Fund", "outside_pac", "2026-10", "unknown",
         "unknown", "unknown", "unknown", "unknown", "unknown", "unknown",
         "reported $5,000,000 investment in the race in October 2026", "unknown", "unknown",
         "unknown", "SRC-2111|https://www.cbsnews.com/news/south-carolina-2026-senate-annie-andrews-darline-graham/",
         "partially verified",
         "reported by CBS as an October investment; no individual ad is documented here"],
    ]
    with open(os.path.join(OUT, "advertisements.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        w.writerow(AD_HEADER)
        w.writerows(rows)
    print(f"advertisements.csv: {len(rows)} rows (outside-money transfers only)")


def build_social():
    rows = [
        ["AND-SOC-0001", "ANDREWS", "YouTube", "Annie Andrews", "2025-05-29", "video",
         "launch video 'Unafraid' published to the campaign channel", "yes", "unknown",
         "https://www.youtube.com/watch?v=J8wMNLaSNW4", "partially verified",
         "view count recorded at discovery time; not a social-media engagement metric"],
        ["GRA-SOC-0001", "GRAHAM", "YouTube", "Darline Graham", "2026-08-12", "video",
         "primary-night speech posted by the campaign", "yes", "unknown",
         "https://www.youtube.com/watch?v=pDsefMH15mU", "partially verified", "unknown"],
        ["GRA-SOC-0002", "GRAHAM", "X", "unknown", "2026-08", "post",
         "Trafalgar Group's runoff tracking poll was released as a tweet by Robert Cahaly "
         "(post 2092072107240837128), reported as 48-48", "no", "unknown",
         "SRC-2108|https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_South_Carolina",
         "unverified",
         "the post itself was not retrievable; the number is documented through the poll table"],
    ]
    with open(os.path.join(OUT, "social_media.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        w.writerow(SOC_HEADER)
        w.writerows(rows)
    print(f"social_media.csv: {len(rows)} rows")


def main():
    os.makedirs(OUT, exist_ok=True)
    build_coverage()
    build_ads()
    build_social()
    return 0


if __name__ == "__main__":
    sys.exit(main())
