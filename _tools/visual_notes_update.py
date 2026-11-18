#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append a dated 'news photographs' section to each case's visual archive notes.

Counts come from image_archive.csv; the prose states the licence position (link and
credit only, no local copy) and the limits of caption-derived rows.

    python _tools/visual_notes_update.py <case> [...]
"""
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARK = "## News photograph harvest (2026-11-18)"


def rows(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for case in argv:
        arch = ROOT / case / "04_visual_archive"
        imgs = rows(arch / "image_archive.csv")
        news = [r for r in imgs if r["copyright_status"] == "all_rights_reserved_link_only"]
        local = [r for r in imgs if r["local_filename"] not in ("", "unknown", "n/a")]
        by_cand = Counter(r["candidate_id"] for r in news)
        by_outlet = Counter(r["source_name"] for r in news).most_common(6)
        text = (arch / "visual_archive_notes.md")
        body = text.read_text(encoding="utf-8") if text.exists() else ""
        if MARK in body:
            print(case, "section already present")
            continue
        add = []
        add.append("")
        add.append(MARK)
        add.append("")
        add.append(f"On 2026-11-18 the archive added **{len(news)} credited news-photograph rows** harvested "
                   f"from the article HTML already stored for fact-checking. {len(local)} rows in this file "
                   f"have a local licensed copy; the news rows do not — the photograph is all rights reserved, "
                   f"so only the article URL, caption and credit line are recorded.")
        add.append("")
        add.append(f"按候选人 / by candidate: " + ", ".join(f"{k} {v}" for k, v in by_cand.most_common()))
        add.append("")
        add.append("Top outlets / 主要来源: " + ", ".join(f"{k} ({v})" for k, v in by_outlet))
        add.append("")
        add.append("Every row is `verification_status = partially verified`: the caption was read in the "
                   "archived page, but **the image itself was neither downloaded nor viewed**. A caption that "
                   "names both nominees may describe either of them; rows record the candidate named first "
                   "in the caption and do not assert who is pictured.")
        add.append("")
        add.append("每一行都是 `partially verified`：说明文字确实在读到的存档页面中出现，但**图片本身既未下载也未查看**。"
                   "同时提到两位候选人的说明文字可能描述其中任何一位；记录取说明中最先出现的候选人，并不断言画面中是谁。")
        add.append("")
        add.append("Rows whose caption names no candidate are not harvested; gallery pages, logos, maps and "
                   "charts are excluded. See `_tools/news_photos.py` for the exact filters.")
        add.append("")
        body = body.rstrip() + "\n" + "\n".join(add)
        text.write_text(body, encoding="utf-8", newline="\n")
        print(case, f"appended ({len(news)} news rows)")


if __name__ == "__main__":
    main(sys.argv[1:])
