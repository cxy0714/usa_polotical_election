#!/usr/bin/env python3
"""Make every delivered CSV satisfy the citation and vocabulary contract.

Streams that produced files independently used slightly different conventions: bare URLs in the
`url` column instead of `SRC-####|url`, `mentions_opponent` values like `Y: Lindsey Graham`, and
ids left with a stray wrapping quote. All three are mechanical, so they are repaired here rather
than by editing rows by hand — and anything that cannot be repaired from the source table is
reported instead of guessed.

Run: python _staging/_lead_fix_citations.py
"""
import csv
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC_CSV = os.path.join(ROOT, "09_sources", "sources.csv")

URL_COLS = {"url", "source_urls", "source_url", "video_url", "speech_url", "transcript_url",
            "media_coverage", "photo_urls", "image_url", "source", "poll_url"}
ID_COLS = {"speech_id", "event_id", "coverage_id", "ad_id", "post_id", "image_id", "finance_id",
           "poll_id", "video_id", "frame_id", "source_id", "pos_id", "tl_id", "row_id"}
VOCAB_CELLS = {"mentions_opponent", "opponent_reference"}
SRC_RE = re.compile(r"SRC-\d{4}")
URL_RE = re.compile(r"https?://\S+")


def norm(u):
    return re.sub(r"[?#].*$", "", u.strip()).rstrip("/").lower()


def load_map():
    m = {}
    for r in csv.DictReader(open(SRC_CSV, encoding="utf-8")):
        k = norm(r["url"])
        sid = r["source_id"]
        if k not in m or int(sid.split("-")[1]) < int(m[k].split("-")[1]):
            m[k] = sid
    return m


def fix_url_cell(cell, m, missing):
    if "SRC-" in cell:
        return cell
    urls = URL_RE.findall(cell)
    if not urls:
        return cell
    parts = []
    for u in urls:
        sid = m.get(norm(u))
        if sid is None:
            missing.append(u)
            parts.append(u)
        else:
            parts.append(f"{sid}|{u}")
    return ";".join(parts)


def fix_vocab(cell):
    c = cell.strip()
    low = c.lower()
    if low.startswith("y"):
        return "yes"
    if low.startswith("n"):
        return "no"
    if "unknown" in low or not c:
        return "unknown"
    return c


def strip_quotes(cell):
    return cell.strip().strip('"').strip()


def main():
    m = load_map()
    missing, changed = [], 0
    for path in sorted(glob.glob(os.path.join(ROOT, "**", "*.csv"), recursive=True)):
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        if rel.startswith("_staging/") or rel == "09_sources/sources.csv":
            continue
        rows = list(csv.reader(open(path, encoding="utf-8-sig")))
        if not rows:
            continue
        header, body = rows[0], rows[1:]
        idx = {n: i for i, n in enumerate(header)}
        touched = 0
        for row in body:
            if len(row) != len(header):
                continue
            for name, i in idx.items():
                val = row[i]
                if name in URL_COLS:
                    new = fix_url_cell(val, m, missing)
                elif name in VOCAB_CELLS:
                    new = fix_vocab(val)
                elif name in ID_COLS:
                    new = strip_quotes(val)
                else:
                    new = val
                if new != val:
                    row[i] = new
                    touched += 1
        if touched:
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
                w.writerow(header)
                w.writerows(body)
            print(f"{rel}: {touched} cells repaired")
            changed += touched

    if missing:
        uniq = sorted(set(missing))
        print(f"\nURLs with no source row ({len(uniq)}):")
        for u in uniq[:15]:
            print("  ", u)
    print(f"\ntotal cells repaired: {changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
