import collections
import re

t = open("_staging/mirrors/wiki_ohio.wikitext", encoding="utf-8").read()
urls = re.findall(r"https?://[^\s\|\[\]\}\<>\"]+", t)
seen = []
for u in urls:
    u = u.rstrip(".,;)")
    if u not in seen:
        seen.append(u)
print(len(urls), len(seen))
dom = collections.Counter(re.sub(r"^https?://", "", u).split("/")[0] for u in seen)
for d, c in dom.most_common(80):
    print(c, d)
with open("_staging/wikitext_urls.txt", "w", encoding="utf-8") as f:
    for u in seen:
        f.write(u + "\n")
