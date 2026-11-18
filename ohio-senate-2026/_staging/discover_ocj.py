#!/usr/bin/env python3
"""Discover Ohio Capital Journal articles through the WordPress RSS search feed.

Real requests only. Writes _staging/discovery/ocj_hits.csv
"""
import csv
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
OUT = "_staging/discovery"
FEED = "https://ohiocapitaljournal.com/feed/?s="
QUERIES = [
    "Sherrod Brown", "Jon Husted", "Senate debate", "debate", "rally", "county fair",
    "UAW", "tariff", "trade", "abortion", "East Palestine", "rail", "data center",
    "immigration", "gun", "energy", "CHIPS", "manufacturing", "minimum wage",
    "endorsement", "fundraising", "FEC", "primary results", "victory", "concession",
    "sworn in", "swearing-in", "appointment", "special election", "poll", "ads",
    "campaign launch", "City Club", "Steelworkers", "AFL-CIO", "voters", "election results",
    "Redpath", "third party", "Levinson", "Obama", "Trump Ohio rally",
]
os.makedirs(OUT, exist_ok=True)
rows = []
seen = set()
for q in QUERIES:
    url = FEED + urllib.parse.quote(q)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
    except Exception as e:
        print("ERR", q, type(e).__name__, str(e)[:80])
        continue
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        print("PARSE", q, e)
        continue
    items = root.findall("./channel/item")
    n = 0
    for it in items:
        link = (it.findtext("link") or "").strip()
        if not link or link in seen:
            continue
        seen.add(link)
        rows.append({
            "query": q,
            "pubDate": (it.findtext("pubDate") or "").strip(),
            "title": (it.findtext("title") or "").strip(),
            "link": link,
        })
        n += 1
    print(f"{n:4d} new / {len(items):4d} items  <- {q}")

with open(os.path.join(OUT, "ocj_hits.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["query", "pubDate", "title", "link"],
                       lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print("total", len(rows))
