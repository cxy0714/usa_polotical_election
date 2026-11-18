import base64
import csv
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def get(u, timeout=30):
    req = urllib.request.Request(u, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read(), r.geturl()


rows = list(csv.DictReader(open("_staging/discovery/all_hits.csv", encoding="utf-8")))
gl = rows[0]["link"]
print("GLEN", len(gl))
try:
    s, b, final = get(gl)
    print("google", s, len(b), final[:160])
    txt = b.decode("utf-8", "replace")
    m = re.findall(r'https?://[^"\'<>\\ ]{20,}', txt)
    print("candidate urls in body:", len(m))
    for x in m[:8]:
        print("  ", x[:140])
except Exception as e:
    print("google ERR", type(e).__name__, str(e)[:120])

q = "%22Husted%22+%22Brown%22+Ohio+Senate+debate+October+2026"
s, b, final = get("https://www.bing.com/search?q=" + q)
html = b.decode("utf-8", "replace")
print("bing", s, len(html))
params = re.findall(r"[?&]u=a1([A-Za-z0-9_\-=%]+)", html)
print("u params", len(params))
out = []
for p in params:
    p = urllib.parse.unquote(p)
    pad = p + "=" * (-len(p) % 4)
    try:
        dec = base64.urlsafe_b64decode(pad).decode("utf-8", "replace")
    except Exception:
        continue
    if dec.startswith("http") and dec not in out:
        out.append(dec)
print("decoded", len(out))
for d in out[:30]:
    print("  ", d[:150])
