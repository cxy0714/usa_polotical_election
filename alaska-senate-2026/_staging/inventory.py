"""Inventory of retrieved mirrors: url, title, published date -> for source-id assignment."""
import csv, os, json
CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log = {}
for r in csv.DictReader(open(os.path.join(CASE, "_staging", "fetch_log.csv"), encoding="utf-8")):
    log[r["saved_file"].replace("\\", "/").split("/")[-1]] = r
rows = []
for m in csv.DictReader(open(os.path.join(CASE, "_staging", "mirror_manifest.csv"), encoding="utf-8")):
    f = m["file"]
    lr = log.get(f)
    if not lr or lr["http_status"] != "200":
        continue
    rows.append((lr["url"], m["title"][:90], m["published"][:10], m["chars"]))
rows.sort(key=lambda r: r[0])
for r in rows:
    print("%-10s %s\n           %s" % (r[2], r[0], r[1]))
print(len(rows))
