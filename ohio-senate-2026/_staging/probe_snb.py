import re
import urllib.request

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
pages = [
    "https://www.statenews.org/tags/election-2026",
    "https://www.statenews.org/government-politics",
    "https://www.statenews.org/elections",
]
for u in pages:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            html = r.read().decode("utf-8", "replace")
        print("OK", r.status, len(html), u)
        links = re.findall(r'href="(/[^"]*20\d\d[^"]*)"', html)
        seen = []
        for l in links:
            if l not in seen:
                seen.append(l)
        print("  dated links", len(seen))
        for l in seen[:25]:
            print("    ", l[:140])
    except Exception as e:
        print("ERR", u, type(e).__name__, str(e)[:100])
