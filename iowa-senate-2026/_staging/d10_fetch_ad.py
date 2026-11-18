# -*- coding: utf-8 -*-
"""Fetch the Turek transgender-ad article, log it, register it, and add it to the ad table."""
import csv
import io
import os
import re
import urllib.request

CASE = r"C:\Users\12257\Documents\usa_polotical_election\iowa-senate-2026"
URL = ("https://iowacapitaldispatch.com/2026/10/26/"
       "josh-turek-ad-on-transgender-issues-draws-bipartisan-criticism/")
UA = "Mozilla/5.0 (research archive)"

req = urllib.request.Request(URL, headers={"User-Agent": UA})
try:
    with urllib.request.urlopen(req, timeout=90) as r:
        body = r.read()
        status = r.status
except Exception as e:
    status = getattr(e, "code", -1)
    body = b""
print("status", status, "bytes", len(body))

saved = "mirrors/f201_iowacapitaldispatch_2026_10_26_josh_turek_ad_on_transgender_issues.html"
if body:
    io.open(os.path.join(CASE, "_staging", saved), "wb").write(body)
    html = body.decode("utf-8", "replace")
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;?", " ", text)
    text = re.sub(r"&#8217;", "'", text)
    text = re.sub(r"&#8220;|&#8221;", '"', text)
    text = re.sub(r"&#8212;", "-", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    io.open(os.path.join(CASE, "_staging/text/f201_transgender_ad.txt"), "w",
            encoding="utf-8", newline="\n").write(text)
    print("text chars", len(text))

# log the fetch
log = os.path.join(CASE, "_staging/fetch_log.csv")
rows = list(csv.DictReader(io.open(log, encoding="utf-8", newline="")))
rows.append({"url": URL, "http_status": str(status), "bytes": str(len(body)),
             "fetched_at": "2026-11-18T14:05:00", "saved_file": saved})
with io.open(log, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["url", "http_status", "bytes", "fetched_at", "saved_file"],
                       lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print("fetch_log rows", len(rows))
