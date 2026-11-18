import json
import urllib.parse
import urllib.request

TITLES = [
    "File:Sherrod Brown on his support for the nomination of Lisa Cook as Federal Reserve "
    "Governor.ogg",
    "File:VOTE FOR JON HUSTED!!!.webm",
]
url = ("https://commons.wikimedia.org/w/api.php?action=query&titles="
       + urllib.parse.quote("|".join(TITLES))
       + "&prop=imageinfo&iiprop=url%7Csize%7Cextmetadata%7Cmime&format=json")
req = urllib.request.Request(url, headers={"User-Agent": "case-archive-research/1.0"})
with urllib.request.urlopen(req, timeout=60) as r:
    raw = r.read()
open("_staging/mirrors/commons_av.json", "wb").write(raw)
d = json.loads(raw.decode("utf-8"))
for pg in d["query"]["pages"].values():
    ii = (pg.get("imageinfo") or [{}])[0]
    em = ii.get("extmetadata", {})
    print(pg.get("title"))
    print("  url:", (ii.get("url") or "").split("?")[0])
    print("  mime:", ii.get("mime"), "size:", ii.get("size"))
    print("  dur:", ii.get("duration"), "w/h:", ii.get("width"), ii.get("height"))
    print("  date:", (em.get("DateTimeOriginal", {}) or {}).get("value", "")[:30])
    print("  lic:", (em.get("LicenseShortName", {}) or {}).get("value", ""))
    print("  desc:", (em.get("ImageDescription", {}) or {}).get("value", "")[:200])
