"""Normalise every source_urls cell to exactly one SRC-####|<canonical url> pair."""
import csv
import glob
import os
import re

PAIR = re.compile(r"SRC-(\d{4})\|(\S+?)(?=;SRC-\d{4}\||$)")

src = {}
for r in csv.DictReader(open("09_sources/sources.csv", encoding="utf-8")):
    src[r["source_id"]] = r["url"].rstrip("/")

changed = 0
multi = 0
for path in sorted(glob.glob("**/*.csv", recursive=True)):
    if path.startswith("_staging") or path.endswith("sources.csv"):
        continue
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    if not rows:
        continue
    fields = list(rows[0].keys())
    touched = False
    for r in rows:
        for f in fields:
            if "url" not in f:
                continue
            cell = r[f]
            if not cell or "SRC-" not in cell:
                continue
            pairs = PAIR.findall(cell)
            if not pairs:
                continue
            if len(pairs) > 1:
                multi += 1
                touched = True
            sid, url = pairs[0]
            canon = src.get(f"SRC-{sid}")
            if canon is None:
                continue
            new = f"SRC-{sid}|{canon}"
            if cell != new:
                r[f] = new
                changed += 1
                touched = True
    if touched:
        with open(path, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print("rewrote", path)
print("cells fixed:", changed, "cells that had multiple pairs:", multi)
