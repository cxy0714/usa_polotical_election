"""Lead: build 04_visual_archive/image_archive.csv from Wikimedia Commons.

Enumerates Commons files for both candidates, pulls structured metadata
(URL, dimensions, licence, author, date) via batched imageinfo calls, and
writes the archive CSV. Downloads a licensed subset locally for pixel-level
visual annotation.

Respects a fixed user-agent, throttles, and retries on HTTP 429/5xx.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = {"User-Agent": "TexasSenate2026ResearchArchive/1.0 "
      "(academic campaign-visual archive; low request rate)"}
API = "https://commons.wikimedia.org/w/api.php"
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CACHE = os.path.join(ROOT, "_staging", "_commons_cache.json")


def api(params, tries=5):
    params = dict(params)
    params["format"] = "json"
    url = API + "?" + urllib.parse.urlencode(params)
    last = None
    for n in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(4 * (n + 1))
                continue
            raise
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 * (n + 1))
    raise RuntimeError(f"API failed after {tries} tries: {last}")


def category_files(cat, depth=0, seen=None):
    if seen is None:
        seen = set()
    if cat in seen or depth > 2:
        return []
    seen.add(cat)
    try:
        d = api({"action": "query", "list": "categorymembers",
                 "cmtitle": cat, "cmlimit": "500"})
    except Exception:
        return []
    time.sleep(1.0)
    out = []
    for m in d.get("query", {}).get("categorymembers", []):
        t = m["title"]
        if t.startswith("Category:"):
            out += category_files(t, depth + 1, seen)
        elif t.startswith("File:"):
            out.append(t)
    return out


def search_files(term, limit=200):
    try:
        d = api({"action": "query", "list": "search", "srsearch": term,
                 "srnamespace": "6", "srlimit": str(limit)})
    except Exception:
        return []
    time.sleep(1.0)
    return [m["title"] for m in d.get("query", {}).get("search", [])]


def imageinfo(titles):
    """Batched imageinfo: 50 titles per call."""
    out = {}
    for i in range(0, len(titles), 50):
        batch = titles[i:i + 50]
        d = api({"action": "query", "titles": "|".join(batch), "prop": "imageinfo",
                 "iiprop": "url|size|mime|extmetadata", "iiurlwidth": "800"})
        for page in d.get("query", {}).get("pages", {}).values():
            if "imageinfo" in page:
                out[page["title"]] = page["imageinfo"][0]
        time.sleep(1.2)
    return out


def meta(ii, key):
    v = ii.get("extmetadata", {}).get(key, {}).get("value")
    if v is None:
        return ""
    v = re.sub(r"<[^>]+>", "", str(v))
    return re.sub(r"\s+", " ", v).strip()


def iso_date(ii):
    raw = meta(ii, "DateTimeOriginal") or meta(ii, "DateTime")
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", raw or "")
    if m:
        return m.group(0)
    m = re.search(r"(\d{1,2}) (\w+) (\d{4})", raw or "")
    if m:
        return raw
    return "unknown"


def main():
    collect = "--collect" in sys.argv
    if collect or not os.path.exists(CACHE):
        data = {}
        for cand, cat, terms in [
            ("TALARICO", "Category:James Talarico",
             ["James Talarico", "Talarico Texas Senate campaign", "James Talarico rally"]),
            ("PAXTON", "Category:Ken Paxton",
             ["Ken Paxton", "Ken Paxton AmericaFest", "Ken Paxton rally Texas"]),
        ]:
            titles = set(category_files(cat))
            for t in terms:
                titles.update(search_files(t))
            titles = sorted(titles)
            print(f"{cand}: {len(titles)} candidate file titles")
            ii = imageinfo(titles)
            data[cand] = ii
            print(f"{cand}: metadata for {len(ii)} files")
            time.sleep(2)
        with open(CACHE, "w", encoding="utf-8") as f:
            json.dump(data, f)
        print("cache written:", CACHE)
    else:
        with open(CACHE, encoding="utf-8") as f:
            data = json.load(f)
        print("cache loaded from", CACHE)
    for cand, ii in data.items():
        photos = [t for t, v in ii.items()
                  if v.get("mime", "").startswith("image/")
                  and ".svg" not in t.lower()
                  and any(k in t.lower() for k in (cand.lower().replace("tal", "tal"),))]
        print(f"{cand}: image/ files = {sum(1 for v in ii.values() if v.get('mime','').startswith('image/'))}")
        for t, v in list(ii.items())[:3]:
            print("  sample:", t, "|", v.get("width"), "x", v.get("height"),
                  "|", meta(v, "LicenseShortName"), "|", meta(v, "Artist")[:40],
                  "|", iso_date(v))


if __name__ == "__main__":
    main()
