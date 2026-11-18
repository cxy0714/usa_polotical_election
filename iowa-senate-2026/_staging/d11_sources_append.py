# -*- coding: utf-8 -*-
"""Append three sources (candidate Wikipedia entries + the transgender-ad report) and extend srckey."""
import csv
import io
import json
import os

CASE = r"C:\Users\12257\Documents\usa_polotical_election\iowa-senate-2026"
SRC = os.path.join(CASE, "09_sources/sources.csv")

NEW = [
    ["SRC-0109", "https://en.wikipedia.org/wiki/Josh_Turek", "Josh Turek", "Wikipedia", "unknown", "unknown",
     "2026-11-18", "T3", "encyclopedia",
     "Turek was first elected to the Iowa House in 2022, becoming the Iowa Legislature's first permanently disabled lawmaker.",
     "Encyclopedia entry used for biography and career chronology only; fetched and archived under _staging/mirrors (HTTP 200).",
     "01_candidates/turek/biography.md; 01_candidates/turek/career_timeline.csv"],
    ["SRC-0110", "https://en.wikipedia.org/wiki/Ashley_Hinson", "Ashley Hinson", "Wikipedia", "unknown",
     "unknown", "2026-11-18", "T3", "encyclopedia",
     "In July 2020, The New York Times reported several instances of Hinson's campaign website plagiarizing portions of articles from media outlets.",
     "Encyclopedia entry used for biography and career chronology only; fetched and archived under _staging/mirrors (HTTP 200).",
     "01_candidates/hinson/biography.md; 01_candidates/hinson/career_timeline.csv"],
    ["SRC-0111",
     "https://iowacapitaldispatch.com/2026/10/26/josh-turek-ad-on-transgender-issues-draws-bipartisan-criticism/",
     "Josh Turek ad on transgender issues draws bipartisan criticism", "Iowa Capital Dispatch", "2026-10-26",
     "2026-10-26", "2026-11-18", "T2", "news_article",
     "Turek released an ad Sunday titled \"Stop the Nonsense\" about issues related to transgender Iowans; other ads that week covered diesel prices and health-care costs.",
     "Full text retrieved and archived under _staging/mirrors (HTTP 200); byline Robin Opsahl.",
     "05_campaign_media/advertisements.csv"],
]

rows = list(csv.reader(io.open(SRC, encoding="utf-8", newline="")))
header, body = rows[0], rows[1:]
ids = {r[0] for r in body}
for r in NEW:
    if r[0] in ids:
        print("already present", r[0])
        continue
    body.append(r)
with io.open(SRC, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(header)
    w.writerows(body)
print("sources now", len(body))

kp = os.path.join(CASE, "_staging/srckey.json")
km = json.load(io.open(kp, encoding="utf-8"))
km["wiki_turek"] = "SRC-0109"
km["wiki_hinson"] = "SRC-0110"
km["f201"] = "SRC-0111"
json.dump(km, io.open(kp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("srckey", len(km))
