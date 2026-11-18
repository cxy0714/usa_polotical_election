#!/usr/bin/env python3
"""Discovery through Bing News RSS; decodes the publisher URL from the
`url=` query parameter of each bing apiclick link. Real requests only.
Writes _staging/discovery/bing_news.csv and per-query XML mirrors."""
import csv
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
OUT = "_staging/discovery/bing"
os.makedirs(OUT, exist_ok=True)

QUERIES = [
    "Sherrod Brown Jon Husted debate Ohio",
    "Ohio Senate candidates debate October 2026",
    "Brown Husted forum Cleveland City Club",
    "Husted Brown joint appearance",
    "Sherrod Brown rally Ohio 2026",
    "Jon Husted rally Ohio 2026",
    "Trump rally Husted Ohio October 2026",
    "Brown county fair Ohio Senate",
    "Husted county fair Ohio",
    "Sherrod Brown victory speech Ohio Senate 2026",
    "Jon Husted concession Ohio Senate 2026",
    "Jon Husted sworn in Senate 2025",
    "DeWine appoints Husted Senate January 2025",
    "Sherrod Brown launches Senate campaign August 2025",
    "Husted launches Senate campaign April 2025",
    "Ohio Senate race data centers Brown Husted",
    "Sherrod Brown tariffs Ohio Senate campaign",
    "UAW endorses Sherrod Brown",
    "Sherrod Brown abortion Ohio 2026",
    "East Palestine Sherrod Brown rail safety",
    "Ohio Senate special election results 2026 Brown Husted",
    "Brown Husted ads Ohio Senate 2026",
    "Husted Brown poll Ohio Senate October 2026",
    "Ohio Senate race fundraising Brown Husted 2026",
    "Sherrod Brown watch party election night 2026",
    "Husted election night Ohio Senate 2026",
    "Brown Husted NAACP Urban League Ohio",
    "Sherrod Brown endorsement Ohio Senate 2026",
    "Ohio Senate debate canceled Brown Husted",
    "Sherrod Brown swearing in January 2027",
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
        print("ERR", q, type(e).__name__, str(e)[:80])
        continue
    slug = re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:60]
    with open(os.path.join(OUT, slug + ".xml"), "wb") as f:
        f.write(body)
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        print("PARSE", q, e)
        continue
    n = 0
    for it in root.findall("./channel/item"):
        link = (it.findtext("link") or "").strip()
        title = (it.findtext("title") or "").strip()
        pub = (it.findtext("pubDate") or "").strip()
        real = ""
        qs = urllib.parse.parse_qs(urllib.parse.urlsplit(link).query)
        if "url" in qs:
            real = urllib.parse.unquote(qs["url"][0])
        if not real or real in seen:
            continue
        seen.add(real)
        rows.append({"query": q, "title": title, "pubDate": pub, "url": real})
        n += 1
    print(f"{n:3d} new / {len(root.findall('./channel/item')):3d}  <- {q}")

with open("_staging/discovery/bing_news.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["query", "title", "pubDate", "url"],
                       lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print("total", len(rows))
