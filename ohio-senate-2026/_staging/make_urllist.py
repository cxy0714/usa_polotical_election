import csv
import os
import re

t = open("_staging/mirrors/wiki_ohio.wikitext", encoding="utf-8").read()
urls = re.findall(r"https?://[^\s\|\[\]\}\<>\"]+", t)
seen = []
for u in urls:
    u = u.rstrip(".,;)")
    if u not in seen:
        seen.append(u)

out = []
for i, u in enumerate(seen, start=1):
    host = re.sub(r"^https?://", "", u).split("/")[0]
    slug = re.sub(r"[^A-Za-z0-9]+", "_", u.split("://", 1)[1])[:70].strip("_")
    out.append(f"ref{i:03d}_{slug},{u}")
with open("_staging/urls_refs.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print(len(out))
