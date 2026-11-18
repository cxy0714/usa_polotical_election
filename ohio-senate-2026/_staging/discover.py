#!/usr/bin/env python3
"""Discovery via Google News RSS. Writes _staging/discovery/<slug>.csv per query
and a merged _staging/discovery/all_hits.csv. Real network requests only."""
import csv
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
OUT = "_staging/discovery"
QUERIES = [
    "Sherrod Brown Jon Husted debate",
    "Ohio Senate debate Husted Brown October",
    "Brown Husted Senate forum Cleveland",
    "Sherrod Brown campaign rally Ohio 2026",
    "Jon Husted campaign rally Ohio Senate",
    "Sherrod Brown county fair Ohio",
    "Husted county fair Ohio Senate campaign",
    "Sherrod Brown victory speech Ohio Senate",
    "Jon Husted concession speech Ohio Senate",
    "Jon Husted sworn in Senate January 2025",
    "DeWine appoints Husted Senate",
    "Sherrod Brown launches Senate campaign 2026",
    "Husted launches Senate campaign 2026",
    "Ohio Senate race data centers Brown Husted",
    "UAW endorses Sherrod Brown Senate",
    "Sherrod Brown tariffs trade Ohio Senate",
    "Husted Brown abortion Ohio Senate",
    "Ohio Senate race ads Brown Husted",
    "Sherrod Brown East Palestine rail safety",
    "Ohio Senate special election results Brown",
    "Husted Brown debate city club",
    "Ohio Senate debate Cincinnati Columbus",
    "Brown Husted endorsements Ohio Senate",
    "Ohio Senate race polls Brown Husted",
    "Sherrod Brown FEC fundraising Senate 2026",
    "Husted FEC fundraising Senate 2026",
]
os.makedirs(OUT, exist_ok=True)


def slugify(q):
    return re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")


all_rows = []
for q in QUERIES:
    url = ("https://news.google.com/rss/search?q=" + urllib.parse.quote(q)
           + "&hl=en-US&gl=US&ceid=US:en")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
    except Exception as e:
        print("ERR", q, type(e).__name__, str(e)[:80])
        continue
    fn = os.path.join(OUT, slugify(q) + ".xml")
    with open(fn, "wb") as f:
        f.write(body)
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        print("PARSE ERR", q, e)
        continue
    items = root.findall("./channel/item")
    rows = []
    for it in items:
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        pub = (it.findtext("pubDate") or "").strip()
        src = it.find("source")
        sname = (src.text or "").strip() if src is not None else ""
        rows.append({"query": q, "title": title, "link": link, "pubDate": pub,
                     "source": sname})
    all_rows.extend(rows)
    print(f"{len(rows):3d} {q}")

with open(os.path.join(OUT, "all_hits.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["query", "title", "link", "pubDate", "source"],
                       lineterminator="\n")
    w.writeheader()
    w.writerows(all_rows)
print("total", len(all_rows))
