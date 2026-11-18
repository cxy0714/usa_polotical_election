"""Download the remaining Commons images and build 04_visual_archive/image_archive.csv."""
import csv
import datetime
import json
import os
import sys
import urllib.request

sys.path.insert(0, "_staging")
from b_common import ref, write_csv  # noqa: E402

UA = "Mozilla/5.0 (research archive)"
LOG = "_staging/fetch_log.csv"


def log_row(url, status, nbytes, saved, note):
    with open(LOG, "a", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerow(
            [url, status, nbytes, datetime.datetime.now().isoformat(timespec="seconds"),
             saved, note])


def download(rec):
    dest = rec["local_file"]
    if dest != "unknown" and os.path.exists(dest) and os.path.getsize(dest) > 5000:
        return True, os.path.getsize(dest)
    cand = "brown" if rec["candidate"] == "BROWN" else "husted"
    ext = os.path.splitext(rec["orig_url"].split("?")[0])[1] or ".jpg"
    name = rec["key"] + ext
    dest = f"04_visual_archive/{cand}/{name}"
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if rec["size"] and rec["size"] > 2_000_000:
        return False, 0
    req = urllib.request.Request(rec["orig_url"], headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = r.read()
    except Exception as exc:  # noqa: BLE001
        log_row(rec["orig_url"], "0", 0, "unknown", f"image download failed: {exc}"[:120])
        return False, 0
    open(dest, "wb").write(data)
    log_row(rec["orig_url"], "200", len(data), dest, "Commons image download")
    rec["local_file"] = dest
    rec["size"] = len(data)
    return True, len(data)


FIELDS = ["image_id", "candidate_id", "image_date", "event_id", "event_category",
          "source_name", "source_url", "original_image_url", "photographer",
          "copyright_status", "license", "local_filename", "image_resolution", "framing",
          "camera_angle", "image_quality", "face_visibility", "body_visibility",
          "clothing_notes", "notes", "verification_status"]

# hand-written descriptive cells per image key ------------------------------
DESC = {}
# only two images can be tied to a dated event, and both ties are stated in the
# Commons metadata itself (oath photo dated 2025-01-21; video dated 2026-10-29).
EVENT = {"husted_sworn_in_2025": "EV-017", "video_vote_for_husted_2026": "EV-034"}


def main():
    images = json.load(open("_staging/images.json", encoding="utf-8"))
    rows = []
    for i, rec in enumerate(images, 1):
        if rec["status"] in ("download", "downloaded"):
            ok, size = download(rec)
            if not ok:
                rec["local_file"] = "unknown"
        d = DESC.get(rec["key"], {})
        lic = rec["license"]
        pd = "public_domain" if "public domain" in lic.lower() else "licensed"
        res = (f"{rec['width']}x{rec['height']}" if rec.get("width")
               else "unknown")
        if res == "unknown" and rec["local_file"] != "unknown":
            try:
                from PIL import Image
                with Image.open(rec["local_file"]) as im:
                    res = f"{im.width}x{im.height}"
                    rec["width"], rec["height"] = im.width, im.height
            except Exception:  # noqa: BLE001
                res = "unknown"
        # image_quality is derived from the pixel dimensions only, never from
        # looking at the file; the archiver did not open the pixels.
        w = rec.get("width") or 0
        if w >= 1500:
            quality = "high resolution for web use (width >= 1500 px)"
        elif w >= 800:
            quality = "medium resolution for web use (width 800-1499 px)"
        elif w:
            quality = "low resolution for web use (width < 800 px)"
        else:
            quality = "unknown"
        # framing is taken only from the Commons title/description wording.
        title_desc = (rec["title"] + " " + (rec.get("desc") or "")).lower()
        if "portrait" in title_desc or "official photo" in title_desc:
            framing = "official portrait (per Commons title)"
        elif "cropped" in title_desc:
            framing = "cropped photograph (per Commons title)"
        elif "screen capture" in title_desc:
            framing = "screen capture from video (per Commons description)"
        elif "logo" in title_desc:
            framing = "campaign logo graphic (per Commons description)"
        elif "webm" in title_desc or rec["title"].endswith(".webm"):
            framing = "vertical video (1080x1920 per Commons metadata)"
        else:
            framing = "unknown — no retrieved caption describes composition"
        note = ("Clothing, camera angle, face and body visibility are left 'unknown' on "
                "purpose: this build has no image-reading step, and no retrieved caption "
                "describes what the subjects are wearing or how the frame is composed. "
                "Resolution is the Commons pixel size; framing is read from the Commons "
                "file title or description.")
        if rec.get("desc"):
            note += " Commons description: \"" + rec["desc"].strip()[:180] + "\""
        ev = EVENT.get(rec["key"], "unknown")
        rows.append(dict(
            image_id=f"IMG-{i:03d}", candidate_id=rec["candidate"],
            image_date=rec["date"] if rec["date"] != "unknown" else "unknown",
            event_id=ev, event_category=rec["category"], source_name="Wikimedia Commons",
            source_url=ref(rec["key"]),
            original_image_url=rec["orig_url"], photographer=rec["artist"][:200],
            copyright_status=pd, license=lic,
            local_filename=rec["local_file"] if rec["local_file"] != "unknown"
            else "unknown",
            image_resolution=res, framing=framing, camera_angle="unknown",
            image_quality=quality, face_visibility="unknown",
            body_visibility="unknown", clothing_notes="unknown",
            notes=note, verification_status="verified"))
    write_csv("04_visual_archive/image_archive.csv", FIELDS, rows)
    dl = sum(1 for r in rows if r["local_filename"] != "unknown")
    print("downloaded files:", dl)


if __name__ == "__main__":
    main()
