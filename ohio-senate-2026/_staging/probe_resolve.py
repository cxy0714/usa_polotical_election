import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
g = ("https://news.google.com/rss/articles/CBMijAFBVV95cUxOVnZVdHg1S1V4Mzlja0tzcWdrU1RRV1VEUy0yTnluNS1Oc1lxUVVTVVpYRlBIaW9n"
     "RkNaV1JDU1dJRHhNVnUzd3QxajVBQmRUZmVfby1Pb25qVHc0aVhKUU52NFU5bmNYd0w5OUJ0ZmN4NW1CNG8")
try:
    req = urllib.request.Request(g, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        b = r.read()
        print("google status", r.status, len(b), r.geturl()[:200])
        print(b[:600].decode("utf-8", "replace"))
except Exception as e:
    print("google ERR", type(e).__name__, str(e)[:150])

b2 = urllib.request.Request("https://www.bing.com/search?q=%22Husted%22+%22Brown%22+Ohio+Senate+debate+October+2026",
                            headers={"User-Agent": UA})
with urllib.request.urlopen(b2, timeout=30) as r:
    html = r.read().decode("utf-8", "replace")
print("bing len", len(html))
hrefs = re.findall(r'href="(https?://[^"]+)"', html)
seen = []
for h in hrefs:
    if "bing.com" in h or "microsoft" in h or "msn.com" in h:
        continue
    if h not in seen:
        seen.append(h)
print(len(seen))
for h in seen[:40]:
    print(h[:150])
