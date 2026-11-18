#!/usr/bin/env python3
"""Fetch URLs for the ohio-senate-2026 case archive.

Usage:  python _staging/fetch.py <urls.txt>
urls.txt: one "<key>,<url>" per line ('#' comments allowed).

For each URL: GET with explicit User-Agent, save body under
_staging/mirrors/<key>.<ext>, append one row to _staging/fetch_log.csv
(url,http_status,bytes,fetched_at,saved_file).  HTTP errors are recorded with
their status code and no saved file; nothing is ever reported as retrieved
unless it was.
"""
import csv
import datetime
import os
import sys
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
BASE = os.path.dirname(os.path.abspath(__file__))
MIRRORS = os.path.join(BASE, "mirrors")
LOG = os.path.join(BASE, "fetch_log.csv")
FIELDS = ["url", "http_status", "bytes", "fetched_at", "saved_file", "note"]


def ext_for(url, ctype):
    low = (ctype or "").lower()
    if "json" in low:
        return "json"
    if "xml" in low:
        return "xml"
    if "pdf" in low:
        return "pdf"
    if "spreadsheet" in low or "excel" in low:
        return "xlsx"
    if "html" in low:
        return "html"
    tail = url.split("?")[0].rsplit(".", 1)
    if len(tail) == 2 and len(tail[1]) <= 5:
        return tail[1].lower()
    return "bin"


def main(path):
    rows = []
    if os.path.exists(LOG):
        with open(LOG, encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
    seen = {r["url"] for r in rows}
    lines = [l.strip() for l in open(path, encoding="utf-8") if l.strip()
             and not l.strip().startswith("#")]
    for line in lines:
        key, _, url = line.partition(",")
        key, url = key.strip(), url.strip()
        if url in seen:
            print("skip (already logged)", url)
            continue
        status, size, saved, note = "0", 0, "unknown", ""
        body = b""
        ctype = ""
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=45) as resp:
                status = str(resp.status)
                body = resp.read()
                ctype = resp.headers.get("Content-Type", "")
                size = len(body)
        except urllib.error.HTTPError as e:
            status = str(e.code)
            note = (e.reason or "")[:120]
            try:
                body = e.read()
                size = len(body)
            except Exception:
                body, size = b"", 0
        except Exception as e:  # network / TLS / timeout
            status = "0"
            note = type(e).__name__ + ": " + str(e)[:120]
        if status.startswith("2") or status == "304":
            fn = os.path.join(MIRRORS, key + "." + ext_for(url, ctype))
            with open(fn, "wb") as f:
                f.write(body)
            saved = os.path.relpath(fn, os.path.dirname(BASE)).replace("\\", "/")
        rows.append({
            "url": url,
            "http_status": status,
            "bytes": str(size),
            "fetched_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            "saved_file": saved,
            "note": note,
        })
        seen.add(url)
        print(f"{status:>4} {size:>9} {url}")
    with open(LOG, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"logged {len(rows)} urls -> {LOG}")


if __name__ == "__main__":
    main(sys.argv[1])
