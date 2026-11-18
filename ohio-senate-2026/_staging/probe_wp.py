import json
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
sites = [
    "https://ohiocapitaljournal.com",
    "https://www.statenews.org",
    "https://signalohio.org",
    "https://www.thehill.com",
    "https://www.cleveland.com",
]
for s in sites:
    u = s + "/wp-json/wp/v2/posts?" + urllib.parse.urlencode(
        {"search": "Husted Brown Senate", "per_page": 5, "_fields": "id,date,link,title"})
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            b = r.read()
        data = json.loads(b)
        print("OK", s, len(data))
        for d in data[:5]:
            print("   ", d.get("date"), d.get("link"))
            t = d.get("title")
            if isinstance(t, dict):
                print("      ", t.get("rendered", "")[:90])
    except Exception as e:
        print("ERR", s, type(e).__name__, str(e)[:100])
