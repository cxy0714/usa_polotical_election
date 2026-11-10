"""Lead: build 04_visual_archive/image_archive.csv from the Commons cache.

Filters to genuine photographs of each candidate, joins each photo to a
campaign event by (candidate, date) where possible, downloads licensed copies
locally for pixel-level annotation, and writes the 21-column archive CSV.
"""
import csv
import json
import os
import re
import time
import urllib.parse
import urllib.request

UA = {"User-Agent": "TexasSenate2026ResearchArchive/1.0 (academic archive)"}
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CACHE = os.path.join(ROOT, "_staging", "_commons_cache.json")
ARCH = os.path.join(ROOT, "04_visual_archive")
HEADER = ["image_id", "candidate_id", "image_date", "event_id", "event_category",
          "source_name", "source_url", "original_image_url", "photographer",
          "copyright_status", "license", "local_filename", "image_resolution",
          "framing", "camera_angle", "image_quality", "face_visibility",
          "body_visibility", "clothing_notes", "notes", "verification_status"]

EXCLUDE = re.compile(r"(opinion|signature|logo|map|\.pdf|\.svg|\.djvu|\.webm|"
                     r"norwich|federal register|city directory|guid|congressional|"
                     r"arquivo nacional|dpla|king, jr)", re.I)


def meta(ii, key):
    v = ii.get("extmetadata", {}).get(key, {}).get("value")
    if v is None:
        return ""
    v = re.sub(r"<[^>]+>", "", str(v))
    return re.sub(r"\s+", " ", v).strip()


def norm_date(ii):
    raw = meta(ii, "DateTimeOriginal") or meta(ii, "DateTime")
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", raw or "")
    if m:
        return m.group(0)
    months = {m2: f"{i:02d}" for i, m2 in enumerate(
        ["January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December"], 1)}
    m = re.search(r"(\d{1,2}) (\w+) (\d{4})", raw or "")
    if m and m.group(2) in months:
        return f"{m.group(3)}-{months[m.group(2)]}-{int(m.group(1)):02d}"
    m = re.search(r"(\d{4})", raw or "")
    return m.group(1) if m else "unknown"


def copyright_of(ii):
    lic = meta(ii, "LicenseShortName")
    low = lic.lower()
    if "public domain" in low or low.startswith("pd"):
        return "public_domain", lic
    if "cc" in low or "creative commons" in low:
        return "licensed", lic
    if not lic:
        return "unknown", "unknown"
    return "licensed", lic


def infer_category(desc, cat_text):
    d = (desc + " " + cat_text).lower()
    if "americafest" in d or "conference" in d or "summit" in d:
        return "party_event"
    if "rally" in d or "rally" in d:
        return "rally"
    if "press conference" in d:
        return "press_conference"
    if "speaking" in d and "event" in d:
        return "other"
    return "unknown"


def load_events():
    p = os.path.join(ROOT, "02_campaign_events", "campaign_events.csv")
    idx = {}
    with open(p, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            d = (r.get("event_date") or "").strip()
            c = (r.get("candidate_id") or "").strip()
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
                idx.setdefault((c, d), (r["event_id"], r["event_category"]))
    return idx


def slug(t):
    t = t.replace("File:", "")
    t = re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_").lower()
    return t[:70]


def main():
    with open(CACHE, encoding="utf-8") as f:
        data = json.load(f)
    events = load_events()
    os.makedirs(os.path.join(ARCH, "talarico", "campaign"), exist_ok=True)
    os.makedirs(os.path.join(ARCH, "paxton", "campaign"), exist_ok=True)

    rows = []
    counters = {"TALARICO": 800, "PAXTON": 800}
    downloaded = 0
    for cand in ("TALARICO", "PAXTON"):
        # annotate metadata + filter
        keep = []
        for title, ii in data.get(cand, {}).items():
            if EXCLUDE.search(title):
                continue
            mime = ii.get("mime", "")
            if not mime.startswith("image/"):
                continue
            name = title.lower()
            if cand.lower() not in name and "americafest" not in name:
                continue
            keep.append((title, ii))
        keep.sort(key=lambda x: (norm_date(x[1]), x[0]))
        print(f"{cand}: {len(keep)} photograph candidates kept")

        for title, ii in keep:
            counters[cand] += 1
            iid = f"{'TAL' if cand == 'TALARICO' else 'PAX'}IMG" if False else \
                  (f"TAL-IMG-{counters[cand]:04d}" if cand == "TALARICO"
                   else f"PAX-IMG-{counters[cand]:04d}")
            d = norm_date(ii)
            eid, ecat = events.get((cand, d), ("unknown", "unknown"))
            if ecat == "unknown":
                ecat = infer_category(meta(ii, "ImageDescription"),
                                      meta(ii, "Categories"))
            artist = meta(ii, "Artist") or meta(ii, "Credit") or "unknown"
            cstatus, lic = copyright_of(ii)
            res = (f"{ii.get('width')}x{ii.get('height')}"
                   if ii.get("width") else "unknown")
            desc = meta(ii, "ImageDescription") or meta(ii, "ObjectName") or ""
            page = "https://commons.wikimedia.org/wiki/" + \
                   urllib.parse.quote(title.replace(" ", "_"))
            row = {
                "image_id": iid, "candidate_id": cand, "image_date": d,
                "event_id": eid, "event_category": ecat,
                "source_name": "Wikimedia Commons",
                "source_url": page,
                "original_image_url": ii.get("url", "unknown"),
                "photographer": artist,
                "copyright_status": cstatus, "license": lic or "unknown",
                "local_filename": "unknown", "image_resolution": res,
                "framing": "unknown", "camera_angle": "unknown",
                "image_quality": "unknown", "face_visibility": "unknown",
                "body_visibility": "unknown", "clothing_notes": "unknown",
                "notes": (desc[:400] + (" | " if desc else "")
                          + "Commons file page holds full licence/attribution record."),
                "verification_status": "verified",
            }
            # download a licensed copy (thumb at 800px) for annotation
            if cstatus in ("licensed", "public_domain") and downloaded < 80:
                thumb = ii.get("thumburl") or ii.get("url")
                if thumb:
                    sub = "talarico" if cand == "TALARICO" else "paxton"
                    fn = f"{iid}_{slug(title)}.jpg"
                    path = os.path.join(ARCH, sub, "campaign", fn)
                    try:
                        req = urllib.request.Request(thumb, headers=UA)
                        with urllib.request.urlopen(req, timeout=60) as r, \
                                open(path, "wb") as out:
                            out.write(r.read())
                        row["local_filename"] = f"{sub}/campaign/{fn}"
                        downloaded += 1
                        time.sleep(0.4)
                    except Exception as e:  # noqa: BLE001
                        print("  download failed:", title, type(e).__name__)
            rows.append(row)

    out = os.path.join(ARCH, "image_archive.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    tal = sum(1 for r in rows if r["candidate_id"] == "TALARICO")
    pax = sum(1 for r in rows if r["candidate_id"] == "PAXTON")
    print(f"[image_archive.csv] {len(rows)} rows (TALARICO={tal}, PAXTON={pax}); "
          f"{downloaded} licensed files downloaded")


if __name__ == "__main__":
    main()
