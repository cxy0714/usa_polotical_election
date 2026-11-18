#!/usr/bin/env python3
"""Fetch a list of URLs, save mirrors, append to _staging/fetch_log.csv.

Usage: python _staging/fetch_urls.py urls.json
urls.json = [{"url": "...", "tag": "latimes_001"}, ...]
"""
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
MIRRORS = os.path.join(BASE, "mirrors")
LOG = os.path.join(BASE, "fetch_log.csv")
UA = "Mozilla/5.0 (research archive)"

os.makedirs(MIRRORS, exist_ok=True)


def safe(tag, url):
    ext = ".html"
    low = url.lower()
    if "youtube.com" in low or "youtu.be" in low:
        ext = ".html"
    if "action=raw" in low:
        ext = ".wikitext"
    if low.endswith(".pdf"):
        ext = ".pdf"
    return re.sub(r"[^A-Za-z0-9_.-]", "_", tag)[:80] + ext


def fetch(url, tag):
    out = os.path.join(MIRRORS, safe(tag, url))
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    status, body = "ERR", b""
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            status = r.status
            body = r.read()
    except urllib.error.HTTPError as e:
        status = e.code
        try:
            body = e.read()
        except Exception:
            body = b""
    except Exception as e:  # noqa: BLE001
        status = type(e).__name__
        body = b""
    if body:
        with open(out, "wb") as f:
            f.write(body)
    else:
        out = "unknown"
    rec = {
        "url": url,
        "http_status": str(status),
        "bytes": str(len(body)),
        "fetched_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "saved_file": os.path.relpath(out, os.path.dirname(BASE)).replace("\\", "/") if out != "unknown" else "unknown",
    }
    return rec


def main(argv):
    items = json.load(open(argv[1], encoding="utf-8"))
    new = not os.path.exists(LOG)
    rows = []
    with open(LOG, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        if new:
            w.writerow(["url", "http_status", "bytes", "fetched_at", "saved_file"])
        for it in items:
            rec = fetch(it["url"], it.get("tag", "x"))
            w.writerow([rec["url"], rec["http_status"], rec["bytes"], rec["fetched_at"], rec["saved_file"]])
            f.flush()
            rows.append(rec)
            print(rec["http_status"], rec["bytes"], rec["url"][:110])
            time.sleep(0.4)
    print(f"done {len(rows)}")


if __name__ == "__main__":
    main(sys.argv)
