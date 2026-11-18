import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
tests = [
    ("ocj", "https://ohiocapitaljournal.com/feed/?s=Husted"),
    ("signal", "https://signalohio.org/feed/?s=Husted"),
    ("hill", "https://thehill.com/feed/?s=Ohio+Senate"),
]
for key, u in tests:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            b = r.read()
        print(f"OK {key} {r.status} {len(b)}")
        root = ET.fromstring(b)
        items = root.findall("./channel/item")
        print("  items", len(items))
        for it in items[:10]:
            print("   ", (it.findtext("pubDate") or "")[:30], "|", (it.findtext("title") or "")[:80])
            print("       ", (it.findtext("link") or "")[:140])
    except Exception as e:
        print("ERR", key, type(e).__name__, str(e)[:90])

# also: does OCJ search HTML contain article permalinks?
u = "https://ohiocapitaljournal.com/?s=Husted+Brown"
req = urllib.request.Request(u, headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=25) as r:
    html = r.read().decode("utf-8", "replace")
arts = re.findall(r'href="(https://ohiocapitaljournal\.com/20\d\d/\d\d/\d\d/[^"]+)"', html)
seen = []
for a in arts:
    if a not in seen:
        seen.append(a)
print("OCJ html article links", len(seen))
for a in seen[:10]:
    print("   ", a[:150])
