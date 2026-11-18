import urllib.error
import urllib.request

UA = "Mozilla/5.0 (research archive)"
CANDIDATES = [
    "https://publicfiles.ohiosos.gov/election-results/past-elections/2026/"
    "Primary+Special%20Election%20-%20May%205,%202026/group1/"
    "summary-level-official-results-2026-primary---democratic.xlsx",
    "https://publicfiles.ohiosos.gov/election-results/past-elections/2026/"
    "General%20Election%20-%20November%203,%202026/group1/"
    "summary-level-official-results-2026-general.xlsx",
    "https://publicfiles.ohiosos.gov/election-results/past-elections/2026/"
    "General%20Election%20-%20November%203,%202026/group1/"
    "summary-level-official-results-2026-general---us-senate.xlsx",
]
for u in CANDIDATES:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45) as r:
            data = r.read()
        name = "_staging/mirrors/probe_" + u.rsplit("/", 1)[-1]
        open(name, "wb").write(data)
        print("OK", r.status, len(data), name)
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, u.rsplit("/", 1)[-1][:60])
    except Exception as e:  # noqa: BLE001
        print("ERR", type(e).__name__, str(e)[:80], u.rsplit("/", 1)[-1][:50])
