import re, os, json, collections

case = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
wt = open(os.path.join(case, "_staging", "mirrors", "wiki_alaska.wikitext"), encoding="utf-8").read()

urls = []
for m in re.finditer(r"https?://[^\s\|\[\]\{\}<>\"']+", wt):
    u = m.group(0).rstrip(".,;:)")
    urls.append(u)

# dedupe preserving order
seen, uniq = set(), []
for u in urls:
    if u not in seen:
        seen.add(u); uniq.append(u)

dom = collections.Counter(re.sub(r"^https?://([^/]+).*", r"\1", u).lower() for u in uniq)
print("unique urls:", len(uniq))
for d, c in dom.most_common():
    print(f"{c:3d}  {d}")

json.dump(uniq, open(os.path.join(case, "_staging", "ref_urls.json"), "w", encoding="utf-8"), indent=1)
