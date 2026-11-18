import csv
import glob
import json
import os
import re

MIR = "_staging/mirrors"
rows = list(csv.DictReader(open("_staging/fetch_log.csv", encoding="utf-8")))
out = {}
for r in rows:
    if not r["http_status"].startswith("2"):
        continue
    saved = r["saved_file"].replace("/", os.sep)
    path = os.path.join(os.path.dirname(os.path.abspath(".")), saved) if not saved.startswith("_staging") else saved
    if not os.path.exists(path):
        path = saved
    stem = os.path.splitext(os.path.basename(saved))[0]
    title = ""
    pubdate = ""
    if path.endswith((".html", ".htm")):
        raw = open(path, "rb").read().decode("utf-8", "replace")
        m = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw)
        if m:
            title = re.sub(r"\s+", " ", m.group(1)).strip()
        for pat in (r'"datePublished"\s*:\s*"([^"]+)"',
                    r'property="article:published_time" content="([^"]+)"',
                    r'name="date" content="([^"]+)"',
                    r'"pubDate"\s*:\s*"([^"]+)"'):
            m2 = re.search(pat, raw)
            if m2:
                pubdate = m2.group(1)
                break
        m3 = re.search(r'name="author"\s+content="([^"]+)"', raw)
        if m3:
            out.setdefault("_authors", {})[stem] = m3.group(1)
    out[stem] = {"url": r["url"], "title": title, "pubdate": pubdate}
json.dump(out, open("_staging/titles.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out))
for k, v in list(out.items())[:5]:
    if k == "_authors":
        continue
    print(k, "|", v["title"][:90], "|", v["pubdate"][:25])
