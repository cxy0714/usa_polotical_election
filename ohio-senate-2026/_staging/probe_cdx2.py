import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"


def cdx(prefix, frm="20250101", to="20261118", limit=400):
    p = {
        "url": prefix,
        "matchType": "prefix",
        "output": "json",
        "from": frm,
        "to": to,
        "limit": str(limit),
        "collapse": "urlkey",
        "fl": "original,timestamp",
    }
    u = "http://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(u, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        b = r.read()
    data = json.loads(b)
    return data[1:] if data else []


PREFIXES = [
    "cleveland.com/news/2026/",
    "cleveland.com/open/2026/",
    "cleveland.com/open/2025/",
    "dispatch.com/story/news/politics/2026/",
    "dispatch.com/story/opinion/2026/",
    "politico.com/news/2026/",
    "politico.com/news/2025/",
]
PAT = re.compile(r"(senate|husted|brown|ohio)", re.I)
for p in PREFIXES:
    try:
        rows = cdx(p)
    except Exception as e:
        print("ERR", p, type(e).__name__, str(e)[:90])
        continue
    hits = [r for r in rows if PAT.search(r[0])]
    print(f"{p}: {len(rows)} rows, {len(hits)} matched")
    for r in hits[:25]:
        print("   ", r[1], r[0][:150])
