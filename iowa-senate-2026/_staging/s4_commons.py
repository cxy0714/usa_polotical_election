# -*- coding: utf-8 -*-
"""Search Commons for candidate images; dump licence metadata for each hit."""
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


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
        return r.getcode(), r.read(8_000_000)


def strip(v):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", v or "")).strip()


API = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search"
       "&gsrnamespace=6&gsrlimit=60&prop=imageinfo&iiprop=url|size|extmetadata&gsrsearch=")

out = {}
for q in ("Josh Turek", "Joshua Turek", "Ashley Hinson"):
    code, body = get(API + urllib.parse.quote(q))
    d = json.loads(body.decode("utf-8"))
    pages = d.get("query", {}).get("pages", {})
    print("=== QUERY", q, "hits", len(pages))
    for pid, p in pages.items():
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        rec = dict(
            title=p.get("title"),
            w=ii.get("width"), h=ii.get("height"),
            url=ii.get("url"),
            desc=strip(em.get("ImageDescription", {}).get("value")),
            lic=strip(em.get("LicenseShortName", {}).get("value")),
            licurl=strip(em.get("LicenseUrl", {}).get("value")),
            artist=strip(em.get("Artist", {}).get("value")),
            credit=strip(em.get("Credit", {}).get("value")),
            date=strip(em.get("DateTimeOriginal", {}).get("value")),
            page="https://commons.wikimedia.org/wiki/" + urllib.parse.quote(p.get("title", "").replace(" ", "_")),
        )
        out[rec["title"]] = rec
        if rec["w"]:
            print("  %-6s %sx%s %-22s %s" % ("", rec["w"], rec["h"], rec["lic"][:22], rec["title"][:80]))

with open(os.path.join(MIR, "commons_search_all.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("total files:", len(out))
