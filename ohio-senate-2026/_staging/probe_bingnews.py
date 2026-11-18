import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
qs = ["Brown Husted Ohio Senate debate", "Ohio Senate special election debate 2026"]
for q in qs:
    u = "https://www.bing.com/news/search?q=" + urllib.parse.quote(q) + "&format=RSS"
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            b = r.read()
        print("OK", r.status, len(b), q)
        root = ET.fromstring(b)
        items = root.findall("./channel/item")
        print(" items", len(items))
        for it in items[:10]:
            print("   ", (it.findtext("pubDate") or "")[:25], "|", (it.findtext("title") or "")[:80])
            print("      ", (it.findtext("link") or "")[:130])
    except Exception as e:
        print("ERR", type(e).__name__, str(e)[:90], q)
