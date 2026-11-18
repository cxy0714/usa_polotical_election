import csv
from pathlib import Path

for case in ("michigan-senate-2026", "iowa-senate-2026"):
    p = Path(case) / "_staging" / "fetch_log.csv"
    rows = list(csv.DictReader(open(p, encoding="utf-8-sig")))
    ok = 0
    for r in rows[:5]:
        saved = (r.get("saved_file") or "").replace("\\", "/").lstrip("./")
        fp = Path(case) / saved
        print(case, r.get("http_status"), saved, fp.exists())
    print(case, "rows", len(rows))
