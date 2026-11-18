import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
tests = [
    "https://news.google.com/rss/search?q=Brown+Husted+Senate+debate+Ohio&hl=en-US&gl=US&ceid=US:en",
    "https://ohiocapitaljournal.com/?s=Husted+Brown+debate",
    "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=2026%20Ohio%20Senate%20debate&format=json",
    "https://duckduckgo.com/html/?q=Brown+Husted+Ohio+Senate+debate+2026",
    "https://www.bing.com/search?q=Brown+Husted+Ohio+Senate+debate+2026",
]
for u in tests:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            b = r.read()
            print(r.status, len(b), u)
            print("   head:", b[:200].decode("utf-8", "replace").replace("\n", " "))
    except Exception as e:
        print("ERR", type(e).__name__, str(e)[:100], u)
