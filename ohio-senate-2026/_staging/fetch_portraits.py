#!/usr/bin/env python3
"""Fetch Wikimedia Commons portrait metadata + 800px thumbnails.

Only PD/CC0/CC BY / CC BY-SA files are downloaded. Each download and each API
call is appended to _staging/fetch_log.csv. Thumbnails are kept well under 2 MB.
"""
import csv
import datetime
import json
import os
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(BASE, "_staging", "fetch_log.csv")
FIELDS = ["url", "http_status", "bytes", "fetched_at", "saved_file", "note"]

FILES = [
    ("brown", "File:Sherrod Brown 117th Congress (1) (cropped).jpg", "brown_portrait_2021.jpg"),
    ("husted", "File:Sen. Jon Husted official portrait, 119th Congress (cropped 2).jpg",
     "husted_portrait_2025.jpg"),
    ("husted", "File:Jon Husted sworn in by JD Vance (2025).jpg", "husted_sworn_in_2025.jpg"),
    ("brown", "File:Sherrod Brown official photo 2009.jpg", "brown_portrait_2009.jpg"),
    ("husted", "File:Jon Husted (2025) (cropped).jpg", "husted_2025_cropped.jpg"),
]


def log(rows, url, status, size, saved, note=""):
    rows.append({
        "url": url, "http_status": str(status), "bytes": str(size),
        "fetched_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "saved_file": saved, "note": note,
    })


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def main():
    rows = []
    if os.path.exists(LOG):
        with open(LOG, encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
    meta_out = {}
    for cand, title, fname in FILES:
        api = ("https://commons.wikimedia.org/w/api.php?action=query&titles="
               + urllib.parse.quote(title)
               + "&prop=imageinfo&iiprop=url%7Csize%7Cextmetadata&iiurlwidth=800&format=json")
        try:
            st, body = get(api)
        except Exception as e:
            print("API ERR", title, type(e).__name__, str(e)[:80])
            log(rows, api, 0, 0, "unknown", "api failure")
            continue
        with open(os.path.join(BASE, "_staging", "mirrors",
                               f"commons_{fname}.json"), "wb") as f:
            f.write(body)
        log(rows, api, st, len(body), f"_staging/mirrors/commons_{fname}.json", "commons imageinfo")
        d = json.loads(body)
        page = list(d["query"]["pages"].values())[0]
        if "imageinfo" not in page:
            print("no imageinfo", title)
            continue
        ii = page["imageinfo"][0]
        em = ii.get("extmetadata", {})
        lic = (em.get("LicenseShortName", {}).get("value") or "").strip()
        thumb = ii.get("thumburl") or ii["url"]
        meta_out[fname] = {
            "title": page["title"],
            "license": lic,
            "artist": (em.get("Artist", {}).get("value") or "").strip(),
            "credit": (em.get("Credit", {}).get("value") or "").strip(),
            "date": (em.get("DateTimeOriginal", {}).get("value") or "").strip(),
            "description": (em.get("ImageDescription", {}).get("value") or "").strip(),
            "file_page": ii.get("descriptionurl", ""),
            "original_url": ii["url"],
            "thumb_url": thumb,
            "width": ii.get("width"),
            "height": ii.get("height"),
            "thumb_width": ii.get("thumbwidth"),
        }
        allowed = lic.lower()
        if not any(k in allowed for k in ("public domain", "pd", "cc0", "cc by", "cc-by")):
            print("SKIP licence not allowed:", lic, title)
            continue
        try:
            st, body = get(thumb)
        except Exception as e:
            print("DL ERR", title, type(e).__name__, str(e)[:80])
            log(rows, thumb, 0, 0, "unknown", "download failure")
            continue
        dst = os.path.join(BASE, "04_visual_archive", cand, fname)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as f:
            f.write(body)
        rel = f"04_visual_archive/{cand}/{fname}"
        log(rows, thumb, st, len(body), rel, f"commons thumbnail of {title}")
        print(f"{st} {len(body):>8} {rel}  [{lic}]")
    with open(os.path.join(BASE, "_staging", "commons_meta.json"), "w",
              encoding="utf-8") as f:
        json.dump(meta_out, f, ensure_ascii=False, indent=2)
    with open(LOG, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print("logged", len(rows))


if __name__ == "__main__":
    main()
