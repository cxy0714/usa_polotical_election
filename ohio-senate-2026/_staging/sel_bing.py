import csv
import re
import urllib.parse

rows = list(csv.DictReader(open("_staging/discovery/bing_news.csv", encoding="utf-8")))
TITLE_OK = re.compile(r"(Brown|Husted|Ohio Senate|U\.S\. Senate|Senate race|Senate seat)", re.I)
TITLE_NO = re.compile(r"(Texas|Georgia|Michigan|Iowa|Alaska|Maine|North Carolina|"
                      r"House|governor|Ramaswamy|Acton|crypto|market report|"
                      r"libertarian|Ninth Congressional)", re.I)
out = []
seen = set()
for r in rows:
    host = urllib.parse.urlsplit(r["url"]).netloc.lower().replace("www.", "")
    if host == "msn.com":
        continue
    if not re.search(r"20(25|26)", r["pubDate"]):
        continue
    if not TITLE_OK.search(r["title"]) or TITLE_NO.search(r["title"]):
        continue
    if r["url"] in seen:
        continue
    seen.add(r["url"])
    out.append((host, r))
print(len(out))
for i, (host, r) in enumerate(out, 1):
    print(f"{i:2d} {r['pubDate'][5:22]} {host[:26]:26s} {r['title'][:90]}")
    print(f"     {r['url'][:150]}")
