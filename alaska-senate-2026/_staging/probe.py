"""Probe HTTP status for a candidate list of URLs (no files saved)."""
import urllib.request, urllib.error, ssl, sys, json, concurrent.futures

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
ctx = ssl.create_default_context()

URLS = json.load(open(sys.argv[1], encoding="utf-8"))

def probe(u):
    req = urllib.request.Request(u, headers={"User-Agent": UA,
                                             "Accept": "*/*",
                                             "Accept-Language": "en-US,en;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            data = r.read()
            return u, r.status, len(data), r.headers.get("content-type", "")
    except urllib.error.HTTPError as e:
        return u, e.code, 0, "HTTPError"
    except Exception as e:
        return u, "ERR", 0, type(e).__name__

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    for u, st, n, ct in ex.map(probe, URLS):
        print(f"{st}\t{n}\t{ct[:40]}\t{u}")
