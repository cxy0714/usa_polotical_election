"""Download the two official candidate portraits used as SFace reference faces.

Both files are public-domain U.S. Senate / federal portraits served by Wikimedia
Commons (conventions §1.7 allows downloading public-domain government portraits;
news photographs are link-only and are NOT fetched here). The Commons API is asked
for a 600 px thumbnail URL, and the thumbnail is written to `refs/`.

Naming matters: recognize_faces.py labels references by the *lowercase prefix of the
file name* (`andrews_*.jpg` -> ANDREWS, `graham_*.jpg` -> GRAHAM), so the two files are
stored as `andrews_<n>.jpg` / `graham_<n>.jpg`.

    python south-carolina-senate-2026/_staging/vision/fetch_refs.py
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REFS = Path(__file__).resolve().parent / "refs"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) sc-senate-2026-research/1.0"

API = ("https://commons.wikimedia.org/w/api.php?action=query&titles="
       "File:Annie_Andrews_in_November_2026.jpg|"
       "File:Official_portrait_of_Darline_Graham,_member_of_the_United_States_Senate_"
       "from_South_Carolina_(2026).jpg"
       "&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=600&format=json")

PREFIX = {
    "Annie_Andrews_in_November_2026.jpg": "andrews",
    "Official_portrait_of_Darline_Graham,_member_of_the_United_States_Senate_from_South_Carolina_(2026).jpg": "graham",
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def main():
    REFS.mkdir(parents=True, exist_ok=True)
    raw = get(API)
    data = json.loads(raw.decode("utf-8"))
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        print("API returned no pages:", raw[:400])
        return 1
    got = 0
    for pid, page in pages.items():
        title = page.get("title", "")
        key = title[len("File:"):] if title.startswith("File:") else title
        if "missing" in page:
            print("MISSING on Commons:", key)
            continue
        ii = (page.get("imageinfo") or [{}])[0]
        thumb = ii.get("thumburl") or ii.get("url")
        if not thumb:
            print("no imageinfo URL for", key)
            continue
        pre = PREFIX.get(key)
        if pre is None:
            pre = "andrews" if "andrews" in key.lower() else "graham" if "graham" in key.lower() else "ref"
        out = REFS / f"{pre}_01.jpg"
        blob = get(thumb)
        out.write_bytes(blob)
        meta = (ii.get("extmetadata") or {})
        lic = (meta.get("LicenseShortName") or {}).get("value", "unknown")
        art = (meta.get("Artist") or {}).get("value", "unknown")
        print(f"wrote {out.name} {len(blob)} bytes  license={lic}  artist={art}")
        (REFS / f"{pre}_01.source.txt").write_text(
            f"title={title}\nthumb_url={thumb}\noriginal_url={ii.get('url','')}\n"
            f"license={lic}\nartist={art}\naccess_date=2026-11-12\n", encoding="utf-8")
        got += 1
    print("reference portraits:", got)
    return 0 if got else 1


if __name__ == "__main__":
    sys.exit(main())
