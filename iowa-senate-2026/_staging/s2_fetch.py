# -*- coding: utf-8 -*-
"""Fetch every reference URL in the local mirror; save to _staging/mirrors; log to fetch_log.csv."""
import csv
import io
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
MIR = os.path.join(HERE, "mirrors")
WIKI = os.path.join(MIR, "wiki_iowa.wikitext")
LOG = os.path.join(HERE, "fetch_log.csv")
MAN = os.path.join(HERE, "fetch_manifest.csv")
UA = "Mozilla/5.0 (research archive)"
SKIP_HOSTS = ("archive.today", "web.archive.org", "drive.google.com", "youtube.com",
              "removepaywall.com", "abacusdata.ca", "taxrelief.org", "x.com", "twitter.com",
              "en.wikipedia.org", "ballotpedia.org", "smartpolitics.lib.umn.edu")

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def load_urls():
    text = io.open(WIKI, encoding="utf-8").read()
    urls = re.findall(r"https?://[^\s\|\]\}<>\"']+", text)
    urls = [u.rstrip(".,;)") for u in urls]
    out, seen = [], set()
    for u in urls:
        host = re.sub(r"^https?://([^/]+).*", r"\1", u)
        if any(host.lower() == s or host.lower().endswith("." + s) for s in SKIP_HOSTS):
            continue
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
    return out


def slug(u, i):
    s = re.sub(r"^https?://", "", u)
    s = re.sub(r"[^A-Za-z0-9]+", "_", s)[:90].strip("_")
    return "f%03d_%s" % (i, s)


def title_of(raw):
    m = re.search(rb"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    if not m:
        return ""
    t = m.group(1).decode("utf-8", "replace")
    t = re.sub(r"\s+", " ", t).strip()
    return t[:180]


def one(args):
    i, u = args
    req = urllib.request.Request(u, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    status, body = 0, b""
    try:
        with urllib.request.urlopen(req, timeout=25, context=CTX) as r:
            status = r.getcode()
            body = r.read(4_500_000)
    except urllib.error.HTTPError as e:
        status = e.code
        try:
            body = e.read(200_000)
        except Exception:
            body = b""
    except Exception as e:
        status = -1
        body = ("ERROR: %s" % e).encode("utf-8", "replace")
    ext = ".pdf" if u.lower().endswith(".pdf") or body[:4] == b"%PDF" else ".html"
    fn = slug(u, i) + ext
    path = os.path.join(MIR, fn)
    with open(path, "wb") as f:
        f.write(body)
    return dict(url=u, http_status=status, bytes=len(body), fetched_at=time.strftime("%Y-%m-%dT%H:%M:%S"),
                saved_file="mirrors/" + fn, title=title_of(body))


def main():
    urls = load_urls()
    print("urls to fetch:", len(urls))
    rows = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        for r in ex.map(one, list(enumerate(urls, start=1))):
            rows.append(r)
            print("%4d %8d %s" % (r["http_status"], r["bytes"], r["url"][:110]), flush=True)
    rows.sort(key=lambda r: r["saved_file"])
    with open(LOG, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["url", "http_status", "bytes", "fetched_at", "saved_file"])
        for r in rows:
            w.writerow([r["url"], r["http_status"], r["bytes"], r["fetched_at"], r["saved_file"]])
    with open(MAN, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["saved_file", "url", "http_status", "bytes", "title"])
        for r in rows:
            w.writerow([r["saved_file"], r["url"], r["http_status"], r["bytes"], r["title"]])
    ok = sum(1 for r in rows if r["http_status"] == 200)
    print("done. 200s:", ok, "of", len(rows))


if __name__ == "__main__":
    main()
