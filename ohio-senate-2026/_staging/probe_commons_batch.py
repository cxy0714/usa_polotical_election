import json
import urllib.parse
import urllib.request

TITLES = [
    "File:Sherrod Brown 113th Congress.jpg",
    "File:Sherrod Brown in 2018.jpg",
    "File:Sherrod Brown official Senate photo portrait, 2007.jpg",
    "File:DNC 2016 - Sherrod Brown (cropped).jpeg",
    "File:Sherrod Brown and Kamala Harris - Warriors win - 2017 01.jpg",
    "File:Sherrod brown-interview (183054174).jpg",
    "File:Sherrod Brown for Ohio 2026 logo-blue-yellow.png",
    "File:LtGov-Jon-Husted.jpg",
    "File:Kelly Loeffler and Jon Husted (2025).jpg",
    "File:Jon Husted 2016-05-12 (cropped).jpg",
    "File:Husted speaking (31790509004).jpg",
    "File:Senator Jon Husted announcing 8,500 new jobs created in Ohio.jpg",
    "File:Family of Senator Jon Husted, 2025.jpg",
    "File:VOTE FOR JON HUSTED!!!.webm",
]
url = ("https://commons.wikimedia.org/w/api.php?action=query&titles="
       + urllib.parse.quote("|".join(TITLES))
       + "&prop=imageinfo&iiprop=url%7Csize%7Cextmetadata%7Cmime&format=json")
req = urllib.request.Request(url, headers={"User-Agent": "case-archive-research/1.0"})
with urllib.request.urlopen(req, timeout=60) as r:
    raw = r.read()
open("_staging/mirrors/commons_batch.json", "wb").write(raw)
d = json.loads(raw.decode("utf-8"))
out = []
for pg in d["query"]["pages"].values():
    ii = (pg.get("imageinfo") or [{}])[0]
    em = ii.get("extmetadata", {})
    rec = {
        "title": pg.get("title"),
        "url": ii.get("url", "").split("?")[0],
        "mime": ii.get("mime"),
        "size": ii.get("size"),
        "width": ii.get("width"),
        "height": ii.get("height"),
        "date": (em.get("DateTimeOriginal", {}) or {}).get("value", ""),
        "artist": (em.get("Artist", {}) or {}).get("value", ""),
        "credit": (em.get("Credit", {}) or {}).get("value", ""),
        "license": (em.get("LicenseShortName", {}) or {}).get("value", ""),
        "desc": (em.get("ImageDescription", {}) or {}).get("value", ""),
    }
    out.append(rec)
json.dump(out, open("_staging/commons_batch_summary.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
for r in out:
    print(r["title"])
    print("   ", r["mime"], r["size"], r["width"], r["height"], "|", r["license"], "|", r["date"][:40])
    print("   artist:", r["artist"][:120])
    print("   desc:", r["desc"][:160])
