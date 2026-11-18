import json
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"


def head(u):
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45) as r:
            b = r.read()
            print(r.status, len(b), u[:120])
            txt = b.decode("utf-8", "replace")
            print("   ", txt[:120].replace("\n", " "))
    except Exception as e:
        print("ERR", type(e).__name__, str(e)[:80], u[:120])


head("https://web.archive.org/web/20260115102850/https://www.dispatch.com/story/news/politics/2026/01/13/ohio-senator-jon-husted-warns-not-to-interfere-with-ice-operations/88157304007/")
head("https://www.cleveland.com/open/2026/01/jon-husted-challenges-commerce-department-on-frozen-jobs-funds-for-ohio-capitol-letter.html")
head("https://web.archive.org/web/2025/https://www.politico.com/news/2025/01/17/ohio-senate-seat-dewine-husted-ramaswamy-00198974")
