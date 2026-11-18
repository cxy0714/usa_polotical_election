#!/usr/bin/env python
"""Scout for candidate photographs outside the Commons categories already harvested.

Read-only: prints what exists and under which licence, so the next step can decide what to keep.
Sources probed: Commons search, Commons categories, the English Wikipedia articles' images, and the
official Senate / campaign pages.
"""
import json
import re
import sys
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; archive-research/1.0; +https://example.invalid)"
API = "https://commons.wikimedia.org/w/api.php"


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout).read()


def api(params):
    params = dict(params, format="json")
    url = API + "?" + urllib.parse.urlencode(params)
    return json.loads(get(url))


def search(term, limit=50):
    try:
        d = api({"action": "query", "list": "search", "srsearch": term, "srnamespace": 6,
                 "srlimit": limit})
    except Exception as e:
        print(f"  search failed for {term!r}: {e}")
        return []
    return [r["title"] for r in d.get("query", {}).get("search", [])]


def category(name, limit=200):
    try:
        d = api({"action": "query", "list": "categorymembers", "cmtitle": name,
                 "cmtype": "file", "cmlimit": limit})
    except Exception as e:
        print(f"  category failed for {name!r}: {e}")
        return []
    return [r["title"] for r in d.get("query", {}).get("categorymembers", [])]


def wiki_images(page):
    try:
        d = api({"action": "query", "titles": page, "prop": "images", "imlimit": "max"})
    except Exception as e:
        print(f"  wiki page failed {page}: {e}")
        return []
    out = []
    for p in d.get("query", {}).get("pages", {}).values():
        for im in p.get("images", []):
            t = im["title"]
            if re.search(r"\.(jpe?g|png|webp)$", t, re.I):
                out.append(t)
    return out


def info(titles):
    if not titles:
        return {}
    d = api({"action": "query", "titles": "|".join(titles[:50]), "prop": "imageinfo",
             "iiprop": "url|size|extmetadata|mime", "iiurlwidth": "1200"})
    return d.get("query", {}).get("pages", {})


def licence_of(meta):
    lic = (meta.get("LicenseShortName") or {}).get("value", "unknown")
    return re.sub(r"<[^>]+>", "", lic).strip()


def main():
    groups = {
        "CATEGORIES": ["Category:Annie Andrews", "Category:Darline Graham",
                       "Category:Annie Andrews in 2026", "Category:Darline Graham in 2026"],
        "SEARCH:andrews": ["Annie Andrews"],
        "SEARCH:graham": ["Darline Graham", "Darline Graham Nordone"],
    }
    titles = set()
    for label, terms in groups.items():
        for t in terms:
            found = category(t) if label == "CATEGORIES" else search(t)
            print(f"{label} {t!r}: {len(found)} files")
            titles.update(found)
    for page in ("Annie Andrews", "Darline Graham"):
        imgs = wiki_images(page)
        print(f"enwiki {page!r}: {len(imgs)} images")
        titles.update(imgs)

    titles = sorted(t for t in titles if t.startswith("File:"))
    print(f"\nunique candidate files: {len(titles)}")
    pages = info(titles)
    rows = []
    for p in pages.values():
        ii = p.get("imageinfo")
        if not ii:
            continue
        ii = ii[0]
        meta = ii.get("extmetadata", {})
        rows.append({
            "title": p["title"],
            "licence": licence_of(meta),
            "artist": re.sub(r"<[^>]+>", "", (meta.get("Artist") or {}).get("value", ""))[:60],
            "date": (meta.get("DateTimeOriginal") or {}).get("value", "")[:20],
            "w": ii.get("width"), "h": ii.get("height"),
            "url": ii.get("url"),
            "thumb": ii.get("thumburl"),
        })
    rows.sort(key=lambda r: (r["date"] or "", r["title"]))
    for r in rows:
        print(f"  {r['title'][:78]:78s} {r['licence'][:18]:18s} {r['w']}x{r['h']} {r['date'][:10]}")
    json.dump(rows, open("_staging/images_scout.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nwrote _staging/images_scout.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
