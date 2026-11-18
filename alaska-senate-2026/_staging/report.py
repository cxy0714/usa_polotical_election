import csv, sys, os
CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(CASE, "_staging", "mirror_manifest.csv"), encoding="utf-8")))
rows.sort(key=lambda r: -int(r["chars"]))
for r in rows:
    print("%7d %-10s %s" % (int(r["chars"]), r["published"][:10], r["title"][:95]))
