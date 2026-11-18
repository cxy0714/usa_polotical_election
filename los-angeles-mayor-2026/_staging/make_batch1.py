import json, re, os

p = r"C:\Users\12257\Documents\usa_polotical_election\los-angeles-mayor-2026\_staging\wiki_urls.json"
urls = json.load(open(p))

SKIP = (
    "facebook.com", "instagram.com", "tmz.com", "usmagazine.com", "drive.google.com",
    "cairaction.org", "complex.com", "ewrestlingnews.com", "komonews.com",
    "yahoo.com/entertainment", "yahoo.com/news", "yahoo.com/entertainment/celebrity",
    "abc3340.com", "closethegapca.org", "bizpacreview.com", "wwbl.com",
    "signalscv.com", "reviewjournal.com", "washingtontimes.com", "rockstar",
)

out = []
seen = set()
for u in urls:
    if any(s in u for s in SKIP):
        continue
    if u in seen:
        continue
    seen.add(u)
    tag = re.sub(r"^https?://(www\.)?", "", u)
    tag = re.sub(r"[^A-Za-z0-9]+", "_", tag)[:70].strip("_")
    out.append({"url": u, "tag": tag})

json.dump(out, open(r"C:\Users\12257\Documents\usa_polotical_election\los-angeles-mayor-2026\_staging\batch1.json", "w"), indent=1)
print(len(out))
