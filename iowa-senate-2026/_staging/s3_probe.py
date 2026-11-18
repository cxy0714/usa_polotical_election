# -*- coding: utf-8 -*-
"""Probe candidate county-results endpoints + fetch Wikipedia bios + Commons metadata."""
import io
import json
import os
import re
import ssl
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MIR = os.path.join(HERE, "mirrors")
UA = "Mozilla/5.0 (research archive)"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            return r.getcode(), r.read(6_000_000)
    except Exception as e:
        code = getattr(e, "code", -1)
        try:
            body = e.read(200_000)
        except Exception:
            body = b""
        return code, body


PROBES = [
    "https://www.cnn.com/election/2026/results/iowa/senate",
    "https://www.nbcnews.com/politics/2026-elections/iowa-senate-results",
    "https://www.270towin.com/2026-election-results-live/iowa/",
    "https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_Iowa",
    "https://en.wikipedia.org/wiki/Josh_Turek",
    "https://en.wikipedia.org/wiki/Ashley_Hinson",
]

for i, u in enumerate(PROBES, start=1):
    code, body = get(u)
    fn = "probe_%02d.html" % i
    with open(os.path.join(MIR, fn), "wb") as f:
        f.write(body)
    txt = body.decode("utf-8", "replace")
    title = re.search(r"<title[^>]*>(.*?)</title>", txt, re.S | re.I)
    print(code, len(body), fn, (title.group(1).strip()[:90] if title else ""))
    print("   url:", u)

# Commons metadata for the two portraits used in the article infobox
FILES = ["File:Joshua Turek (croppedb).jpg",
         "File:Congresswoman Ashley Hinson Official portrait (cropped).jpg",
         "File:Ashley Hinson official portrait.jpg",
         "File:Josh Turek.jpg"]
API = "https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url|size|extmetadata&titles="
for f in FILES:
    code, body = get(API + urllib.parse.quote(f))
    print("COMMONS", code, f, len(body))
    with open(os.path.join(MIR, "commons_" + re.sub(r"[^A-Za-z0-9]+", "_", f)[:60] + ".json"), "wb") as fh:
        fh.write(body)
    try:
        d = json.loads(body.decode("utf-8"))
        pages = d["query"]["pages"]
        for pid, p in pages.items():
            if "imageinfo" in p:
                ii = p["imageinfo"][0]
                em = ii.get("extmetadata", {})
                print("   ", ii["width"], "x", ii["height"], ii["url"][:120])
                for k in ("LicenseShortName", "Artist", "Credit", "ImageDescription"):
                    v = em.get(k, {}).get("value", "")
                    v = re.sub(r"<[^>]+>", "", v)
                    print("    ", k, "=", v[:160])
            else:
                print("    missing:", pid)
    except Exception as e:
        print("   parse error", e)
