"""Fill sources.csv used_by mechanically by scanning every CSV/MD for SRC ids."""
import csv
import glob
import os
import re

CASE = "."
SRC_RE = re.compile(r"SRC-\d{4}")

files = []
for pat in ("*.csv", "*.md", "**/*.csv", "**/*.md"):
    for p in glob.glob(os.path.join(CASE, pat), recursive=True):
        rel = os.path.relpath(p, CASE).replace("\\", "/")
        if rel.startswith("_staging/") or rel == "09_sources/sources.csv":
            continue
        if rel not in files:
            files.append(rel)

cited = {}
for rel in files:
    try:
        text = open(os.path.join(CASE, rel), encoding="utf-8").read()
    except UnicodeDecodeError:
        continue
    for sid in set(SRC_RE.findall(text)):
        cited.setdefault(sid, []).append(rel)

rows = list(csv.DictReader(open("09_sources/sources.csv", encoding="utf-8")))
fields = list(rows[0].keys())
for r in rows:
    used = sorted(cited.get(r["source_id"], []))
    if used:
        r["used_by"] = "; ".join(used)
    else:
        r["used_by"] = "catalogued only — no dataset or document cites this source yet"
with open("09_sources/sources.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)

n_used = sum(1 for r in rows if not r["used_by"].startswith("catalogued only"))
print(f"{len(rows)} sources; {n_used} cited by at least one file; "
      f"{len(rows) - n_used} catalogued only")
