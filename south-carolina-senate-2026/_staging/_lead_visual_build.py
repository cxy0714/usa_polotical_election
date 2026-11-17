#!/usr/bin/env python3
"""Build the visual archive from Wikimedia Commons metadata.

Why this exists: the visual stream needs (a) licence-clean local copies and (b) a per-row record
of what is actually documented about each image. Commons gives both via two API calls, and the
copyright rule (conventions §1.7) means only PD/CC files may be copied — rights-reserved news
photographs enter as link-only rows.

Outputs
  04_visual_archive/andrews/campaign/*   downloaded PD/CC files
  04_visual_archive/graham/campaign/*
  04_visual_archive/image_archive.csv    one row per image (header per conventions §4)
  04_visual_archive/_commons_raw.json    the raw API payload, for auditability
  _staging/_lead_visual_sources.csv      the SRC rows for the files used here

Run: python _staging/_lead_visual_build.py
"""
import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEST = os.path.join(ROOT, "04_visual_archive")
UA = {"User-Agent": "SC-Senate-Archive/1.0 (academic research; python-urllib)"}

HEADER = ["image_id", "candidate_id", "image_date", "event_id", "event_category", "source_name",
          "source_url", "original_image_url", "photographer", "copyright_status", "license",
          "local_filename", "image_resolution", "framing", "camera_angle", "image_quality",
          "face_visibility", "body_visibility", "clothing_notes", "notes", "verification_status"]

SEED_FILES = {
    "ANDREWS": [
        "File:Annie Andrews in November 2026.jpg",
        "File:Annie Andrews Fort Mill 2026 (cropped 3).png",
        "File:Annie Andrews 2022 (cropped).jpg",
    ],
    "GRAHAM": [
        "File:Official portrait of Darline Graham, member of the United States Senate from "
        "South Carolina (2026).jpg",
        "File:Senator Chuck Grassley Swears In Darline Graham As Senator Of South Carolina.jpg",
        "File:Darline Graham Nordone butter cow.jpg",
        "File:Departure — October 21, 2026 (P20261021DT-0457).jpg",
    ],
}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def api(params):
    q = urllib.parse.urlencode(params, safe="|")
    return json.loads(get(f"https://commons.wikimedia.org/w/api.php?{q}").decode("utf-8"))


def search(term, limit=50):
    d = api({"action": "query", "list": "search", "srsearch": term, "srnamespace": "6",
             "srlimit": str(limit), "format": "json", "formatversion": "2"})
    return [(h["title"], h.get("snippet", "")) for h in d.get("query", {}).get("search", [])]


def category(name, limit=200):
    d = api({"action": "query", "list": "categorymembers", "cmtitle": f"Category:{name}",
             "cmlimit": str(limit), "format": "json", "formatversion": "2"})
    return [m["title"] for m in d.get("query", {}).get("categorymembers", [])
            if m["title"].startswith("File:")]


def imageinfo(titles, width=900):
    out = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        d = api({"action": "query", "titles": "|".join(chunk), "prop": "imageinfo",
                 "iiprop": "url|size|extmetadata|mime", "iiurlwidth": str(width),
                 "format": "json", "formatversion": "2"})
        for p in d.get("query", {}).get("pages", []):
            if "imageinfo" in p:
                out[p["title"]] = p["imageinfo"][0]
    return out


def meta(ii, key):
    v = ii.get("extmetadata", {}).get(key, {}).get("value", "")
    v = re.sub(r"<[^>]+>", "", str(v)).strip()
    return v or "unknown"


def is_free(lic):
    l = lic.lower()
    return any(k in l for k in ("cc0", "cc by", "public domain", "pd-", "no restrictions"))


def slugify(title, cand):
    base = title[5:] if title.startswith("File:") else title
    base = re.sub(r"\.(jpg|jpeg|png|webp)$", "", base, flags=re.I)
    base = re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_").lower()
    folder = "andrews" if cand == "ANDREWS" else "graham"
    return os.path.join(folder, "campaign", base[:80] + ext_of(title))


def ext_of(title):
    m = re.search(r"(\.(?:jpg|jpeg|png|webp))$", title, re.I)
    return m.group(1).lower() if m else ".jpg"


def main():
    os.makedirs(os.path.join(DEST, "andrews", "campaign"), exist_ok=True)
    os.makedirs(os.path.join(DEST, "graham", "campaign"), exist_ok=True)

    found = {"ANDREWS": set(), "GRAHAM": set()}
    for cand, seeds in SEED_FILES.items():
        found[cand].update(seeds)
    for term, cand in [("Annie Andrews pediatrician", "ANDREWS"), ("Annie Andrews senator", "ANDREWS"),
                       ("Darline Graham senator", "GRAHAM"), ("Darline Graham", "GRAHAM")]:
        for t, _ in search(term):
            if t.lower().endswith((".pdf", ".svg", ".djvu", ".tif", ".webm", ".ogg")):
                continue
            if cand == "ANDREWS" and "andrews" in t.lower():
                found[cand].add(t)
            if cand == "GRAHAM" and "graham" in t.lower():
                found[cand].add(t)
    for cat, cand in [("Annie Andrews", "ANDREWS"), ("Darline Graham", "GRAHAM")]:
        for t in category(cat):
            found[cand].add(t)

    for cand in found:
        print(f"{cand}: {len(found[cand])} candidate files")

    all_titles = sorted({t for s in found.values() for t in s})
    info = imageinfo(all_titles)
    print(f"imageinfo resolved for {len(info)} of {len(all_titles)} titles")

    rows = []
    counter = {"ANDREWS": 0, "GRAHAM": 0}
    for cand in ("ANDREWS", "GRAHAM"):
        for title in sorted(found[cand]):
            ii = info.get(title)
            if not ii:
                continue
            lic = meta(ii, "LicenseShortName")
            artist = meta(ii, "Artist")
            dt = meta(ii, "DateTimeOriginal")
            date = "unknown"
            m = re.search(r"(\d{4})-(\d{2})-(\d{2})", dt)
            if m:
                date = m.group(0)
            else:
                m = re.search(r"(\d{4})", dt)
                if m:
                    date = m.group(1)
            free = is_free(lic)
            counter[cand] += 1
            iid = f"{'AND' if cand == 'ANDREWS' else 'GRA'}-IMG-{counter[cand]:04d}"
            local = "unknown"
            if free:
                rel = slugify(title, cand)
                path = os.path.join(DEST, rel)
                if os.path.exists(path) and os.path.getsize(path) > 1000:
                    local = rel.replace("\\", "/")
                else:
                    for attempt in range(3):
                        try:
                            data = get(ii.get("thumburl") or ii["url"])
                            with open(path, "wb") as f:
                                f.write(data)
                            local = rel.replace("\\", "/")
                            break
                        except Exception as e:                    # noqa: BLE001
                            print(f"  download attempt {attempt + 1} failed {title}: {e}")
                            time.sleep(3 * (attempt + 1))
                time.sleep(0.7)
            rows.append({
                "image_id": iid,
                "candidate_id": cand,
                "image_date": date,
                "event_id": "unknown",
                "event_category": "unknown",
                "source_name": "Wikimedia Commons",
                "source_url": f"SRC-0600|https://commons.wikimedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
                "original_image_url": ii.get("url", "unknown"),
                "photographer": artist,
                "copyright_status": "licensed" if free else "all_rights_reserved_link_only",
                "license": lic,
                "local_filename": local,
                "image_resolution": f"{ii.get('width', 'unknown')}x{ii.get('height', 'unknown')}",
                "framing": "unknown",
                "camera_angle": "unknown",
                "image_quality": "unknown",
                "face_visibility": "unknown",
                "body_visibility": "unknown",
                "clothing_notes": "unknown",
                "notes": f"Commons file title: {title}; description: {meta(ii, 'ImageDescription')[:180]}",
                "verification_status": "partially verified",
            })

    rows.sort(key=lambda r: r["image_id"])
    with open(os.path.join(DEST, "image_archive.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    with open(os.path.join(DEST, "_commons_raw.json"), "w", encoding="utf-8") as f:
        json.dump({t: info.get(t) for t in all_titles}, f, ensure_ascii=False, indent=1)

    local_n = sum(1 for r in rows if r["local_filename"] != "unknown")
    print(f"image_archive.csv: {len(rows)} rows; {local_n} local copies, {len(rows) - local_n} link-only")
    for cand in ("ANDREWS", "GRAHAM"):
        n = sum(1 for r in rows if r["candidate_id"] == cand)
        print(f"  {cand}: {n} rows")

    # SRC rows for the Commons files actually cited
    src_rows = {}
    for r in rows:
        key = r["source_url"].split("|", 1)[1]
        src_rows[key] = r["notes"]
    with open(os.path.join(HERE, "_lead_visual_sources.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["source_id", "url", "title", "publisher", "publication_date", "event_date",
                    "access_date", "source_tier", "source_type", "relevant_quote_or_info",
                    "reliability_notes", "used_by"])
        w.writerow(["SRC-0600", "https://commons.wikimedia.org/wiki/Category:Annie_Andrews",
                    "Commons category: Annie Andrews", "Wikimedia Commons", "unknown", "unknown",
                    "2026-11-12", "T3", "photo",
                    "licence and photographer metadata for every downloaded portrait",
                    "Commons metadata is contributor-maintained; licences were read from "
                    "extmetadata, not independently verified", "Lead (visual)"])
        for i, (u, note) in enumerate(sorted(src_rows.items()), start=601):
            w.writerow([f"SRC-{i:04d}", u, "Commons file", "Wikimedia Commons", "unknown",
                        "unknown", "2026-11-12", "T3", "photo", note[:200],
                        "file description page; licence read from Commons extmetadata", "Lead (visual)"])
    print(f"_lead_visual_sources.csv: {len(src_rows) + 1} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
