import json
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"


def cdx(url, frm="20250101", to="20261118", flt=None, limit=60, collapse="urlkey"):
    p = {
        "url": url,
        "matchType": "prefix",
        "output": "json",
        "from": frm,
        "to": to,
        "limit": str(limit),
        "collapse": collapse,
        "fl": "original,timestamp",
    }
    if flt:
        p["filter"] = flt
    u = "http://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(u, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        b = r.read()
    try:
        data = json.loads(b)
    except Exception:
        return []
    return data[1:] if data else []


tests = [
    ("ap ohio senate", "apnews.com/article/", "original:.*ohio.*(senate|husted|brown).*"),
    ("cleveland senate", "cleveland.com/news/", "original:.*(senate|husted|brown).*"),
    ("cleveland open", "cleveland.com/open/", "original:.*(senate|husted|brown).*"),
    ("politico ohio", "politico.com/news/", "original:.*ohio.*"),
]
for name, prefix, flt in tests:
    try:
        rows = cdx(prefix, flt=flt)
        print(f"{name}: {len(rows)}")
        for r in rows[:12]:
            print("   ", r[1], r[0][:150])
    except Exception as e:
        print("ERR", name, type(e).__name__, str(e)[:100])
