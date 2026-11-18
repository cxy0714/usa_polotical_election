import csv
import re

rows = list(csv.DictReader(open("_staging/discovery/ocj_hits.csv", encoding="utf-8")))
KEY = re.compile(r"(Sherrod Brown|Jon Husted|Husted|U\.S\. Senate race|US Senate race|"
                 r"Senate candidates|Ohio US Senate|Ohio U\.S\. Senate|Senate seat)", re.I)
NOT = re.compile(r"(Missouri|Alaska|majority leader|filibuster|reconciliation|"
                 r"vote-a-rama|NPR|PBS|budget resolution|debt limit|SAVE Act|"
                 r"war powers|child marriage)", re.I)
seen = set()
out = []
for r in rows:
    if not re.search(r"20(25|26) ", r["pubDate"]):
        continue
    if not KEY.search(r["title"]) or NOT.search(r["title"]):
        continue
    if r["link"] in seen:
        continue
    seen.add(r["link"])
    out.append(r)
out.sort(key=lambda r: r["pubDate"][5:16])
for i, r in enumerate(out, 1):
    print("{:2d} {} {}".format(i, r["pubDate"][5:17], r["title"][:115]))
print(len(out))
