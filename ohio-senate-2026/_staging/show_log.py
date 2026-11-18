import csv
import os

rows = list(csv.DictReader(open("_staging/fetch_log.csv", encoding="utf-8")))
ok = [r for r in rows if r["http_status"].startswith("2")]
print("total logged", len(rows), "2xx", len(ok))
for r in ok:
    stem = os.path.splitext(os.path.basename(r["saved_file"]))[0]
    print(f"{r['http_status']} {int(r['bytes']):>8} {stem[:62]:62s} {r['url'][:110]}")
