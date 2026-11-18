#!/usr/bin/env python3
"""Extract candidate reference URLs from the local Wikipedia mirror."""
import re, collections, sys, json

p = r"C:\Users\12257\Documents\usa_polotical_election\los-angeles-mayor-2026\_staging\mirrors\wiki_la_mayor.wikitext"
t = open(p, encoding="utf-8").read()
urls = re.findall(r"https?://[^\s\|\]\}<>\"]+", t)
seen = []
s = set()
for u in urls:
    u = u.rstrip(".,;)")
    if u in s:
        continue
    s.add(u)
    seen.append(u)
dom = collections.Counter(re.sub(r"^https?://", "", u).split("/")[0] for u in seen)
print("unique:", len(seen))
for k, v in dom.most_common():
    print(f"{v:4d} {k}")
json.dump(seen, open(r"C:\Users\12257\Documents\usa_polotical_election\los-angeles-mayor-2026\_staging\wiki_urls.json", "w"), indent=0)
