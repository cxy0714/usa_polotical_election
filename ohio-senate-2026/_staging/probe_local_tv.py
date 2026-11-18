import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
tests = [
    "https://www.wdtn.com/feed/?s=Senate+debate",
    "https://www.wdtn.com/?s=Senate+debate",
    "https://www.wtol.com/feed/?s=Husted+Brown",
    "https://www.10tv.com/feed/?s=Husted",
]
for u in tests:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            b = r.read()
            ct = r.headers.get("Content-Type", "")
        print("OK", r.status, len(b), ct[:40], u)
        if b[:5] == b"<?xml":
            root = ET.fromstring(b)
            items = root.findall("./channel/item")
            print("  items", len(items))
            for it in items[:8]:
                print("   ", (it.findtext("title") or "")[:80])
                print("      ", (it.findtext("link") or "")[:130])
        else:
            import re
            html = b.decode("utf-8", "replace")
            links = re.findall(r'href="(https?://[^"]*(?:senate|husted|brown)[^"]*)"', html, re.I)
            seen = []
            for l in links:
                if l not in seen:
                    seen.append(l)
            print("  links", len(seen))
            for l in seen[:10]:
                print("   ", l[:140])
    except Exception as e:
        print("ERR", type(e).__name__, str(e)[:70], u)
