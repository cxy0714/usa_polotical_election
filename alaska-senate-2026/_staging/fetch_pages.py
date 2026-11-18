"""Fetch a curated URL list, save mirrors, append _staging/fetch_log.csv.

Usage: python _staging/fetch_pages.py _staging/fetchlist.json
Log columns (contract 1.10): url,http_status,bytes,fetched_at,saved_file
TLS: some .gov hosts present a chain that fails verification in this environment; on
CERTIFICATE_VERIFY_FAILED the request is retried once with verification off and that
fact is recorded in _staging/tls_fallback.json.
"""
import urllib.request, urllib.error, ssl, sys, json, os, re, csv, hashlib
import concurrent.futures
from datetime import datetime, timezone, timedelta

CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIR = os.path.join(CASE, "_staging", "mirrors", "pages")
LOG = os.path.join(CASE, "_staging", "fetch_log.csv")
TLSF = os.path.join(CASE, "_staging", "tls_fallback.json")
UA = "Mozilla/5.0 (research archive; +https://example.org/research)"
TZ = timezone(timedelta(hours=8))
ctx_ok = ssl.create_default_context()
ctx_no = ssl._create_unverified_context()
os.makedirs(MIR, exist_ok=True)


def slug(u):
    p = re.sub(r"^https?://", "", u)
    p = re.sub(r"[^A-Za-z0-9]+", "_", p).strip("_")
    h = hashlib.sha1(u.encode()).hexdigest()[:6]
    return p[:90] + "_" + h


def ext_for(ct, u):
    if "pdf" in ct or u.lower().endswith(".pdf"):
        return ".pdf"
    if "json" in ct:
        return ".json"
    return ".html"


def get(u):
    req = urllib.request.Request(u, headers={"User-Agent": UA, "Accept": "*/*",
                                             "Accept-Language": "en-US,en;q=0.9"})
    try:
        r = urllib.request.urlopen(req, timeout=45, context=ctx_ok)
        return r.status, r.read(), r.headers.get("content-type", ""), ""
    except urllib.error.HTTPError as e:
        return e.code, b"", "HTTPError", ""
    except urllib.error.URLError as e:
        reason = getattr(e, "reason", None)
        if isinstance(reason, ssl.SSLError) or "CERTIFICATE" in str(reason):
            try:
                r = urllib.request.urlopen(req, timeout=45, context=ctx_no)
                return r.status, r.read(), r.headers.get("content-type", ""), "unverified_tls"
            except urllib.error.HTTPError as e2:
                return e2.code, b"", "HTTPError", "unverified_tls"
            except Exception as e2:
                return "ERR", b"", type(e2).__name__, "unverified_tls"
        return "ERR", b"", type(e).__name__, ""
    except Exception as e:
        return "ERR", b"", type(e).__name__, ""


def work(u):
    st, data, ct, tls = get(u)
    now = datetime.now(TZ).isoformat(timespec="seconds")
    saved = "not_saved"
    if isinstance(st, int) and 200 <= st < 300 and data:
        fn = slug(u) + ext_for(ct, u)
        with open(os.path.join(MIR, fn), "wb") as f:
            f.write(data)
        saved = "_staging/mirrors/pages/" + fn
    return [u, st, len(data) if data else 0, now, saved, ct[:60], tls]


def main(listfile):
    urls = json.load(open(listfile, encoding="utf-8"))
    head = not os.path.exists(LOG)
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for row in ex.map(work, urls):
            rows.append(row)
            print(row[1], row[2], row[0])
    with open(LOG, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        if head:
            w.writerow(["url", "http_status", "bytes", "fetched_at", "saved_file"])
        for u, st, n, now, saved, ct, tls in rows:
            w.writerow([u, st, n, now, saved])
    tls_rows = {u: t for u, st, n, now, saved, ct, t in rows if t}
    if tls_rows:
        old = json.load(open(TLSF, encoding="utf-8")) if os.path.exists(TLSF) else {}
        old.update(tls_rows)
        with open(TLSF, "w", encoding="utf-8") as f:
            json.dump(old, f, indent=1)
    ok = sum(1 for r in rows if r[1] == 200)
    print("\nOK %d/%d -> %s" % (ok, len(rows), LOG))


if __name__ == "__main__":
    main(sys.argv[1])
