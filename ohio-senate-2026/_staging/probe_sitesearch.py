import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
tests = [
    ("ocj", "https://ohiocapitaljournal.com/?s=Husted+Brown"),
    ("ocj2", "https://ohiocapitaljournal.com/?s=Senate+debate"),
    ("ap", "https://apnews.com/search?q=Brown%20Husted%20Ohio%20Senate"),
    ("clev", "https://www.cleveland.com/search/?q=Husted%20Brown%20Senate"),
    ("dispatch", "https://www.dispatch.com/search/?q=Husted+Brown+Senate"),
    ("signal", "https://signalohio.org/?s=Husted"),
    ("statenews", "https://www.statenews.org/search?q=Husted"),
    ("politico", "https://www.politico.com/search?q=Husted+Ohio+Senate"),
    ("nbc4i", "https://www.nbc4i.com/?s=Husted+Brown+debate"),
    ("wkyc", "https://www.wkyc.com/search?query=Husted%20Brown"),
]
for key, u in tests:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            b = r.read()
        html = b.decode("utf-8", "replace")
        host = urllib.parse.urlsplit(u).netloc.replace("www.", "")
        links = re.findall(r'href="(https?://[^"]+)"', html)
        keep = []
        for l in links:
            if host not in l:
                continue
            if any(x in l for x in ("/search", "/?s=", "/tag/", "/author/", "#", "/category/", "/page/")):
                continue
            if l not in keep:
                keep.append(l)
        print(f"OK {key} {r.status} {len(b)} links={len(keep)}")
        for l in keep[:8]:
            print("    ", l[:150])
    except Exception as e:
        print("ERR", key, type(e).__name__, str(e)[:90])
