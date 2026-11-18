import csv
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
QUERIES = [
    "Ohio Senate candidates debate rising costs ahead of midterms",
    "Brown Husted debate moderators Ohio",
    "Ohio Senate race debate scheduled October 2026",
    "Husted Brown face off debate",
]
seen = set()
out = []
for q in QUERIES:
    u = "https://www.bing.com/news/search?q=" + urllib.parse.quote(q) + "&format=RSS"
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        root = ET.fromstring(body)
    except Exception as e:
        print("ERR", q, type(e).__name__, str(e)[:70])
        continue
    for it in root.findall("./channel/item"):
        link = (it.findtext("link") or "").strip()
        qs = urllib.parse.parse_qs(urllib.parse.urlsplit(link).query)
        real = urllib.parse.unquote(qs["url"][0]) if "url" in qs else ""
        if not real or real in seen:
            continue
        seen.add(real)
        out.append(((it.findtext("pubDate") or "").strip(),
                    (it.findtext("title") or "").strip(), real))
for pub, title, url in out:
    print(pub[:22], "|", title[:95])
    print("   ", url[:150])
with open("_staging/urls_debate.txt", "w", encoding="utf-8") as f:
    for i, (pub, title, url) in enumerate(out, 1):
        f.write(f"deb{i:02d},{url}\n")
print(len(out))
