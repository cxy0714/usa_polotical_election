import csv
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
QUERIES = [
    "Ohio finally gets a statewide debate",
    "Ohio statewide debate drought ends",
    "Ohio Senate debate Brown Husted refused",
    "Husted agrees to debate Brown",
    "Brown challenges Husted to debate",
    "Ohio Senate candidates debate Chillicothe",
    "Husted Brown Westerville campaign stop",
    "Brown campaign stop Westerville",
    "Trump rally Chillicothe Husted October 2026",
    "Husted Kenworth Chillicothe jobs",
    "Ohio Senate candidates county fair August 2026",
    "Brown Husted Labor Day parade Ohio 2026",
    "Sherrod Brown Toledo campaign stop 2026",
    "Sherrod Brown Youngstown Mahoning Valley campaign 2026",
    "Husted Cincinnati campaign stop 2026",
    "Husted Columbus campaign event 2026",
]
rows = []
seen = set()
for q in QUERIES:
    u = "https://www.bing.com/news/search?q=" + urllib.parse.quote(q) + "&format=RSS"
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
    except Exception as e:
        print("ERR", q, type(e).__name__, str(e)[:70])
        continue
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        continue
    for it in root.findall("./channel/item"):
        link = (it.findtext("link") or "").strip()
        title = (it.findtext("title") or "").strip()
        pub = (it.findtext("pubDate") or "").strip()
        qs = urllib.parse.parse_qs(urllib.parse.urlsplit(link).query)
        real = urllib.parse.unquote(qs["url"][0]) if "url" in qs else ""
        if not real or real in seen:
            continue
        seen.add(real)
        rows.append({"query": q, "title": title, "pubDate": pub, "url": real})
print("new", len(rows))
with open("_staging/discovery/bing_news2.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["query", "title", "pubDate", "url"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['pubDate'][5:22]:20s} {r['title'][:95]}")
    print(f"{'':20s} {r['url'][:150]}")
