"""Assemble _staging/images.json (17 Commons records) from the batch metadata
plus the five images already downloaded by fetch_portraits.py."""
import json
import urllib.parse

BATCH = json.load(open("_staging/commons_batch_summary.json", encoding="utf-8"))
EXISTING = json.load(open("_staging/commons_meta.json", encoding="utf-8"))

# --- the five already-downloaded files -------------------------------------
OLD = {
    "File:Sherrod Brown 117th Congress (1) (cropped).jpg":
        ("brown_portrait_2021", "04_visual_archive/brown/brown_portrait_2021.jpg",
         "BROWN", "portrait", "2021-11-04"),
    "File:Sen. Jon Husted official portrait, 119th Congress (cropped 2).jpg":
        ("husted_portrait_2025", "04_visual_archive/husted/husted_portrait_2025.jpg",
         "HUSTED", "portrait", "2025-03-31"),
    "File:Jon Husted sworn in by JD Vance (2025).jpg":
        ("husted_sworn_in_2025", "04_visual_archive/husted/husted_sworn_in_2025.jpg",
         "HUSTED", "swearing_in", "2025-01-21"),
    "File:Sherrod Brown official photo 2009.jpg":
        ("brown_portrait_2009", "04_visual_archive/brown/brown_portrait_2009.jpg",
         "BROWN", "portrait", "2009-06-23"),
    "File:Jon Husted (2025) (cropped).jpg":
        ("husted_2025_cropped", "04_visual_archive/husted/husted_2025_cropped.jpg",
         "HUSTED", "portrait", "2025-01-28"),
}

# --- new records -----------------------------------------------------------
NEW = {
    "File:Sherrod Brown 113th Congress.jpg":
        ("img_brown_113th", "BROWN", "portrait", "download"),
    "File:Sherrod Brown in 2018.jpg":
        ("img_brown_2018", "BROWN", "portrait", "download"),
    "File:Sherrod Brown and Kamala Harris - Warriors win - 2017 01.jpg":
        ("img_brown_harris_2017", "BROWN", "public_appearance", "download"),
    "File:DNC 2016 - Sherrod Brown (cropped).jpeg":
        ("img_brown_dnc_2016", "BROWN", "public_appearance", "download"),
    "File:Sherrod brown-interview (183054174).jpg":
        ("img_brown_2004_interview", "BROWN", "public_appearance", "download"),
    "File:Sherrod Brown for Ohio 2026 logo-blue-yellow.png":
        ("img_brown_2026_logo", "BROWN", "campaign_material", "download"),
    "File:Kelly Loeffler and Jon Husted (2025).jpg":
        ("img_husted_loeffler_2025", "HUSTED", "public_appearance", "download"),
    "File:Senator Jon Husted announcing 8,500 new jobs created in Ohio.jpg":
        ("img_husted_jobs_2025", "HUSTED", "public_appearance", "download"),
    "File:Family of Senator Jon Husted, 2025.jpg":
        ("img_husted_family_2025", "HUSTED", "personal", "download"),
    "File:Jon Husted 2016-05-12 (cropped).jpg":
        ("img_husted_cityclub_2016", "HUSTED", "public_appearance", "download"),
    "File:LtGov-Jon-Husted.jpg":
        ("img_husted_ltgov_2018", "HUSTED", "portrait", "record_only"),
    "File:Husted speaking (31790509004).jpg":
        ("img_husted_speaking_2017", "HUSTED", "public_appearance", "record_only"),
    "File:VOTE FOR JON HUSTED!!!.webm":
        ("video_vote_for_husted_2026", "HUSTED", "campaign_material", "record_only"),
}

out = []
for t, (key, path, cand, cat, date) in OLD.items():
    meta = EXISTING.get(t) or {}
    orig = meta.get("url") or ("https://commons.wikimedia.org/wiki/" +
                               urllib.parse.quote(t.replace(" ", "_")))
    out.append({
        "key": key, "title": t,
        "page_url": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(t.replace(" ", "_")),
        "orig_url": orig, "candidate": cand, "category": cat, "date": date,
        "artist": meta.get("artist", "unknown"), "license": meta.get("license", "Public domain"),
        "local_file": path, "size": meta.get("size", 0),
        "width": meta.get("width", 0), "height": meta.get("height", 0),
        "desc": meta.get("desc", ""), "status": "downloaded",
    })

by_title = {r["title"]: r for r in BATCH}
for t, (key, cand, cat, mode) in NEW.items():
    r = by_title.get(t, {})
    lic = r.get("license", "unknown")
    out.append({
        "key": key, "title": t,
        "page_url": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(t.replace(" ", "_")),
        "orig_url": r.get("url", "unknown"), "candidate": cand, "category": cat,
        "date": (r.get("date") or "unknown")[:10] if r.get("date") else "unknown",
        "artist": r.get("artist", "unknown"), "license": lic,
        "local_file": "unknown", "size": r.get("size", 0),
        "width": r.get("width", 0), "height": r.get("height", 0),
        "desc": r.get("desc", ""), "status": mode,
    })

json.dump(out, open("_staging/images.json", "w", encoding="utf-8"), indent=1,
          ensure_ascii=False)
print("images:", len(out))
for r in out:
    print(f"  {r['key']:26s} {r['status']:11s} {r['size']:>9} {r['license'][:22]:22s} {r['date']}")
# url list for fetching the Commons file pages (used by fetch.py)
with open("_staging/urls_imgpages.txt", "w", encoding="utf-8") as f:
    for r in out:
        f.write(f"{r['key']},{r['page_url']}\n")
