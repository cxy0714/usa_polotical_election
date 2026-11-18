# -*- coding: utf-8 -*-
"""Download the licensed portraits from Wikimedia Commons (Special:FilePath thumbnails)."""
import io
import json
import os
import urllib.parse
import urllib.request

CASE = r"C:\Users\12257\Documents\usa_polotical_election\iowa-senate-2026"
OUT = os.path.join(CASE, "04_visual_archive")
os.makedirs(OUT, exist_ok=True)

FILES = [
    ("Congresswoman Ashley Hinson Official portrait.jpg", "hinson_2024_official_portrait.jpg", 1100),
    ("Ashley Hinson 119th Congress.jpg", "hinson_119th_congress.jpg", 410),
    ("Democratic senators-elect meet with Chuck Schumer in November 2026.jpg",
     "senators_elect_schumer_2026_11_09.jpg", 1600),
    ("Ashley Hinson has my Complete and Total Endorsement to be the next Senator from Iowa.jpg",
     "trump_endorsement_graphic_2026_09_18.jpg", 1280),
]

UA = "Mozilla/5.0 (research archive)"
for name, local, w in FILES:
    url = ("https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(name)
           + "?width=%d" % w)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = r.read()
            status = r.status
            final = r.geturl()
    except Exception as e:
        print("ERR", name, e)
        continue
    p = os.path.join(OUT, local)
    with open(p, "wb") as f:
        f.write(data)
    print("%-58s %s %8d -> %s (%s)" % (name[:58], status, len(data), local, final[:70]))
