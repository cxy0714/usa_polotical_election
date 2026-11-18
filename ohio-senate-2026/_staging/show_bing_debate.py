import csv
import re

rows = list(csv.DictReader(open("_staging/discovery/bing_news.csv", encoding="utf-8")))
KEY = re.compile(r"(debate|forum|joint|appearance|cancel)", re.I)
for r in rows:
    if KEY.search(r["query"]) or KEY.search(r["title"]):
        print(f"{r['pubDate'][:22]:22s} {r['title'][:100]}")
        print(f"{'':22s} {r['url'][:150]}")
