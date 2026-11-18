#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Register article URLs cited by image_archive rows that are missing from sources.csv.

The image archive records a caption's article URL for link-only rows; every such URL
must resolve to an SRC id so the citation chain is complete. New rows continue the
case's SRC sequence and say which image they support.

    python _tools/register_image_sources.py <case> [...]
"""
import csv
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
HEADER = ["source_id", "url", "title", "publisher", "publication_date", "event_date", "access_date",
          "source_tier", "source_type", "relevant_quote_or_info", "reliability_notes", "used_by"]


def rows(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def pub(url):
    host = urlparse(url).netloc.lower().replace("www.", "")
    if "commons.wikimedia.org" in host or "wikipedia.org" in host:
        return host, "T3", "encyclopedia"
    return host, "T2", "media"


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for case in argv:
        sp = ROOT / case / "09_sources" / "sources.csv"
        ip = ROOT / case / "04_visual_archive" / "image_archive.csv"
        src = rows(sp)
        imgs = rows(ip)
        known = {r["url"].split("#")[0].rstrip("/") for r in src}
        nums = [int(m.group(1)) for r in src for m in [re.match(r"SRC-(\d+)", r["source_id"])] if m]
        nxt = max(nums or [0])
        new = []
        for r in imgs:
            u = r["source_url"]
            if not u.startswith("http"):
                continue
            key = u.split("#")[0].rstrip("/")
            if key in known:
                continue
            known.add(key)
            nxt += 1
            host, tier, stype = pub(u)
            new.append({
                "source_id": f"SRC-{nxt:04d}", "url": u,
                "title": f"Image caption source ({host})",
                "publisher": host,
                "publication_date": r["image_date"] if r["image_date"] not in ("", "unknown") else "unknown",
                "event_date": "unknown", "access_date": "2026-11-18",
                "source_tier": tier, "source_type": stype,
                "relevant_quote_or_info": (r["notes"].split("|")[0].strip()[:180] or "image caption"),
                "reliability_notes": "Article page retained only for its photo caption/credit line; "
                                     "the image itself was not downloaded or read.",
                "used_by": "04_visual_archive/image_archive.csv",
            })
        if not new:
            print(case, "no missing sources")
            continue
        with open(sp, "a", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=HEADER, lineterminator="\n")
            for r in new:
                w.writerow(r)
        print(case, f"+{len(new)} sources")


if __name__ == "__main__":
    main(sys.argv[1:])
