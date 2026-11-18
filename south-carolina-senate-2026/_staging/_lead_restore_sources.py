#!/usr/bin/env python
"""Restore the source rows for the news photographs into a staging file the merge can see.

`_lead_merge_sources.py` rebuilds `09_sources/sources.csv` from every `_staging/*sources*.csv`, so rows
appended straight to the deliverable are wiped on the next merge. The canonical place for them is a
staging CSV, which is what this script writes — one row per article that supplied a photograph.
"""
import csv
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMAGES = os.path.join(ROOT, "04_visual_archive", "image_archive.csv")
SOURCES = os.path.join(ROOT, "09_sources", "sources.csv")
OUT = os.path.join(HERE, "_lead_sources_images.csv")
UA = "Mozilla/5.0 (compatible; archive-research/1.0)"
ACCESS = "2026-11-18"

HEADER = ["source_id", "url", "title", "publisher", "publication_date", "event_date",
          "access_date", "source_tier", "source_type", "relevant_quote_or_info",
          "reliability_notes", "used_by"]


def title_of(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip()[:160]
    except Exception as e:
        print(f"  title fetch failed {url[:70]}: {e}")
    return "unknown"


def main():
    have = {s["source_id"] for s in csv.DictReader(open(SOURCES, encoding="utf-8"))}
    existing_extra = []
    if os.path.exists(OUT):
        existing_extra = list(csv.DictReader(open(OUT, encoding="utf-8")))
    known = {r["source_id"] for r in existing_extra}

    rows = []
    for r in csv.DictReader(open(IMAGES, encoding="utf-8")):
        sid, _, url = r["source_url"].partition("|")
        if not sid or not url or sid in have or sid in known:
            continue
        date = "/".join(url.split("/")[3:6]) if "/20" in url else "unknown"
        rows.append({
            "source_id": sid, "url": url, "title": title_of(url),
            "publisher": "SC Daily Gazette (States Newsroom)", "publication_date": date,
            "event_date": "unknown", "access_date": ACCESS, "source_tier": "T2",
            "source_type": "news_article", "relevant_quote_or_info": "Photograph published with this article",
            "reliability_notes": ("States Newsroom outlet; article photography CC BY-ND 4.0; "
                                  "reused unmodified with credit"),
            "used_by": r["image_id"],
        })
        print(f"  restored {sid} {url.rsplit('/', 1)[-1][:60]}")

    if rows:
        with open(OUT, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=HEADER, lineterminator="\n")
            w.writeheader()
            w.writerows(existing_extra + rows)
    print(f"wrote {OUT}: {len(existing_extra) + len(rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
