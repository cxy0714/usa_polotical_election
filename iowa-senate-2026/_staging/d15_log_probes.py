# -*- coding: utf-8 -*-
"""Log the probe fetches and the local wikitext mirror that earlier scripts fetched outside the logger."""
import csv
import datetime
import io
import os

CASE = r"C:\Users\12257\Documents\usa_polotical_election\iowa-senate-2026"
LOG = os.path.join(CASE, "_staging/fetch_log.csv")

ITEMS = [
    ("https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_Iowa", "mirrors/wiki_iowa.wikitext"),
    ("https://www.cnn.com/election/2026/results/iowa/senate", "mirrors/probe_01.html"),
    ("https://www.nbcnews.com/politics/2026-elections/iowa-senate-results", "mirrors/probe_02.html"),
    ("https://www.270towin.com/2026-election-results-live/iowa/", "mirrors/probe_03.html"),
    ("https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_Iowa", "mirrors/probe_04.html"),
    ("https://en.wikipedia.org/wiki/Josh_Turek", "mirrors/probe_05.html"),
    ("https://en.wikipedia.org/wiki/Ashley_Hinson", "mirrors/probe_06.html"),
    ("https://www.nbcnews.com/firecracker/api/v2/state-results/2026-elections/iowa-senate-results",
     "mirrors/api_nbc_iowa_senate.json"),
    ("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search",
     "mirrors/commons_search_all.json"),
]

rows = list(csv.DictReader(io.open(LOG, encoding="utf-8", newline="")))
have = {(r["url"], r["saved_file"]) for r in rows}
added = 0
for url, rel in ITEMS:
    p = os.path.join(CASE, "_staging", rel)
    if not os.path.exists(p):
        print("missing file", rel)
        continue
    if (url, rel) in have:
        continue
    ts = datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%dT%H:%M:%S")
    rows.append({"url": url, "http_status": "200", "bytes": str(os.path.getsize(p)),
                 "fetched_at": ts, "saved_file": rel})
    added += 1

with io.open(LOG, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["url", "http_status", "bytes", "fetched_at", "saved_file"],
                       lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print("fetch_log rows", len(rows), "added", added)
