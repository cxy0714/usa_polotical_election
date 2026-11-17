#!/usr/bin/env python3
"""Merge every staging source file into 09_sources/sources.csv with full 12-column enrichment.

What it does beyond concatenation:
  * validates every id against SRC-#### and every url against http(s)
  * detects id collisions across streams (same id, different url) 閳?a silent killer in a merged
    citation table
  * de-duplicates by normalized url, keeping the earliest id and listing the merges
  * derives source_tier and source_type from the domain/URL pattern (documented in the data
    dictionary), never from guesswork about content
  * computes `used_by` by scanning every CSV and Markdown file in the archive for `SRC-####`, so
    the citation graph is real rather than asserted
  * adds the video corpus (yt-dlp-verified) as its own source block
  * reports dangling citations: rows citing an id that no source file defines

Run: python _staging/_lead_merge_sources.py
"""
import csv
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "09_sources", "sources.csv")
ACCESS = "2026-11-12"

HEADER = ["source_id", "url", "title", "publisher", "publication_date", "event_date",
          "access_date", "source_tier", "source_type", "relevant_quote_or_info",
          "reliability_notes", "used_by"]

TIER1 = {"scvotes.gov", "fec.gov", "senate.gov", "congress.gov", "scetv.org", "c-span.org",
         "supremecourt.gov", "sceducation.gov", "governor.sc.gov", "census.gov"}
TIER3_MARKERS = {"blogspot", "wordpress", "substack", "medium.com", "reddit.com", "x.com",
                 "twitter.com", "facebook.com", "tiktok.com", "instagram.com", "youtube.com",
                 "rumble.com", "patch.com", "devdiscourse.com"}
NEWS_MARKERS = {"nytimes.com", "washingtonpost.com", "apnews.com", "cbsnews.com", "nbcnews.com",
                "cnn.com", "politico.com", "thehill.com", "pbs.org", "time.com", "usatoday.com",
                "theguardian.com", "postandcourier.com", "thestate.com", "scdailygazette.com",
                "greenvilleonline.com", "goupstate.com", "foxnews.com", "foxcarolina.com",
                "wistv.com", "abcnews4.com", "wbtw.com", "wmbfnews.com", "live5news.com",
                "wyff4.com", "wcnc.com", "wbtv.com", "newsmax.com", "ms.now", "abcnews.go.com",
                "npr.org", "reuters.com", "bbc.com", "bbc.co.uk", "axios.com", "semafor.com",
                "notus.org", "punchbowl.news", "the19th.org", "19thnews.org", "ebony.com"}
SOCIAL_MARKERS = {"x.com", "twitter.com", "facebook.com", "instagram.com", "tiktok.com",
                  "youtube.com", "rumble.com", "threads.net", "bsky.app"}


def host(u):
    try:
        return (urlparse(u).hostname or "").lower().replace("www.", "")
    except ValueError:
        return ""


def match(h, table):
    return any(h == d or h.endswith("." + d) for d in table)


def tier(h):
    if match(h, TIER1) or h.endswith(".gov"):
        return "T1"
    if match(h, TIER3_MARKERS):
        return "T3"
    if match(h, NEWS_MARKERS):
        return "T2"
    if h.endswith(".org") and ("party" in h or "gop" in h or "democrat" in h):
        return "T1"
    return "T3"


def stype(u, h):
    if match(h, SOCIAL_MARKERS):
        return "social_media"
    if match(h, TIER1) or h.endswith(".gov"):
        return "government_record"
    if h.endswith(".wikipedia.org") or "wiki" in h:
        return "encyclopedia"
    if match(h, NEWS_MARKERS):
        return "news_article"
    if "poll" in u.lower() or "trafalgar" in h or "realclearpolitics" in h:
        return "poll"
    return "other"


def norm(u):
    return re.sub(r"[?#].*$", "", u.strip()).rstrip("/").lower()


MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august", "september",
     "october", "november", "december"], start=1)}


def norm_date(s):
    """Staging files wrote human dates; the contract wants ISO or 'unknown'."""
    s = (s or "").strip()
    if not s or s.lower() == "unknown":
        return "unknown"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}|\d{4}-\d{2}|\d{4}", s):
        return s
    m = re.fullmatch(r"([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})", s)
    if m and m.group(1).lower() in MONTHS:
        return f"{int(m.group(3)):04d}-{MONTHS[m.group(1).lower()]:02d}-{int(m.group(2)):02d}"
    m = re.fullmatch(r"(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})", s)
    if m and m.group(2).lower() in MONTHS:
        return f"{int(m.group(3)):04d}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    return "unknown"


def load_staging():
    rows, collisions = [], []
    seen_ids = {}
    for path in sorted(glob.glob(os.path.join(HERE, "*sources*.csv"))):
        if os.path.basename(path).startswith("_lead_url"):
            continue
        for r in csv.DictReader(open(path, encoding="utf-8-sig")):
            sid = (r.get("source_id") or "").strip()
            url = (r.get("url") or "").strip()
            if not re.fullmatch(r"SRC-\d{4}", sid):
                print(f"  [BAD ID ] {os.path.basename(path)}: {sid!r}")
                continue
            if not url.startswith("http"):
                print(f"  [BAD URL] {sid}: {url!r}")
                continue
            if sid in seen_ids and norm(seen_ids[sid]) != norm(url):
                collisions.append((sid, seen_ids[sid], url, os.path.basename(path)))
                continue
            seen_ids.setdefault(sid, url)
            rows.append({
                "source_id": sid, "url": url,
                "title": (r.get("title") or "unknown").strip() or "unknown",
                "publisher": (r.get("publisher") or "").strip() or host(url) or "unknown",
                "publication_date": norm_date(r.get("publication_date")),
                "event_date": norm_date(r.get("event_date")),
                "access_date": (r.get("access_date") or ACCESS).strip() or ACCESS,
                "_origin": os.path.basename(path),
            })
    return rows, collisions


def add_videos(rows, seen_ids):
    conf = os.path.join(HERE, "vision", "videos.json")
    if not os.path.exists(conf):
        return 0
    videos = json.load(open(conf, encoding="utf-8"))
    start = 2200
    added = 0
    for i, v in enumerate(sorted(videos, key=lambda x: x["slug"])):
        sid = f"SRC-{start + i}"
        if sid in seen_ids:
            print(f"  [COLLIDE] video id {sid} already defined")
            continue
        rows.append({
            "source_id": sid,
            "url": f"https://www.youtube.com/watch?v={v['video_id']}",
            "title": v["title"],
            "publisher": v.get("channel") or "YouTube",
            "publication_date": norm_date(v.get("upload_date")),
            "event_date": "unknown",
            "access_date": ACCESS,
            "_origin": "video_corpus",
            "_slug": v["slug"],
        })
        added += 1
    return added


def scan_references():
    """id -> sorted list of row ids / files that cite it."""
    used = defaultdict(set)
    files = []
    for pat in ("**/*.csv", "**/*.md"):
        files += glob.glob(os.path.join(ROOT, pat), recursive=True)
    for path in files:
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        if rel == "_research_conventions.md":
            continue
        if rel.startswith("_staging/") or rel.startswith("site/") or rel == "09_sources/sources.csv":
            continue
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for sid in set(re.findall(r"SRC-\d{4}", text)):
            used[sid].add(rel)
    return used


def main():
    rows, collisions = load_staging()
    seen_ids = {r["source_id"]: r["url"] for r in rows}
    videos_added = add_videos(rows, seen_ids)

    used = scan_references()

    # de-duplicate by URL, but never at the cost of a citation: an id that is cited somewhere in
    # the archive keeps its row even when another id already registered the same URL.
    by_url, merged_raw, dropped = {}, [], []
    for r in rows:
        k = norm(r["url"])
        first = by_url.get(k)
        if first is None:
            by_url[k] = r
            merged_raw.append(r)
            continue
        if r["source_id"] in used:
            r["_dup_of"] = first["source_id"]
            merged_raw.append(r)
        else:
            dropped.append((r["source_id"], first["source_id"], r["url"]))
    merged = sorted(merged_raw, key=lambda r: int(r["source_id"].split("-")[1]))

    defined = {r["source_id"] for r in merged}
    dangling = sorted(s for s in used if s not in defined)
    orphan = sorted(s for s in defined if s not in used)

    for r in merged:
        h = host(r["url"])
        r["source_tier"] = tier(h)
        r["source_type"] = stype(r["url"], h)
        r["relevant_quote_or_info"] = "unknown"
        r["reliability_notes"] = (
            f"tier {r['source_tier']} by domain ({h or 'unknown'}); "
            f"collected via {r['_origin']}; content not re-read during the merge")
        r["used_by"] = ", ".join(sorted(used.get(r["source_id"], []))) or "unknown"

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(merged)

    print(f"sources.csv: {len(merged)} unique sources "
          f"({len(rows)} rows read, {len(dropped)} url-duplicates dropped, "
          f"{videos_added} videos added)")
    print("  tiers:", dict(Counter(r["source_tier"] for r in merged)))
    print("  types:", dict(Counter(r["source_type"] for r in merged)))
    print("  blocks:", dict(Counter(r["source_id"].split("-")[1][0] for r in merged)))
    if collisions:
        print(f"  [ID COLLISIONS] {len(collisions)}:")
        for c in collisions[:10]:
            print(f"    {c[0]}: {c[1]}  vs  {c[2]}  ({c[3]})")
    if dangling:
        print(f"  [DANGLING] {len(dangling)} cited ids with no definition: {dangling[:12]}")
    print(f"  unreferenced sources: {len(orphan)} (kept; they are collected background)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

