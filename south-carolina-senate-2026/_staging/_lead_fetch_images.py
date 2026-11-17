#!/usr/bin/env python3
"""Fetch the image files the archive cites but never downloaded.

Seven `image_archive.csv` rows point at Wikimedia Commons uploads and carry `local_filename = unknown`
because no file was saved. A gallery cannot show what is not on disk, so this fills those seven,
writes the resulting relative path back into `local_filename`, and leaves everything else alone.

Run: python _staging/_lead_fetch_images.py  [--dry-run]
"""
import csv
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CSV_PATH = os.path.join(ROOT, "04_visual_archive", "image_archive.csv")
UA = "Mozilla/5.0"


def target_dir(candidate_id):
    who = "andrews" if candidate_id == "ANDREWS" else "graham"
    return os.path.join(ROOT, "04_visual_archive", who, "campaign")


def have_file(row):
    folder = os.path.join(ROOT, "04_visual_archive", os.path.dirname(row["local_filename"]))
    stem = os.path.splitext(os.path.basename(row["local_filename"]))[0]
    if not os.path.isdir(folder):
        return False
    for f in os.listdir(folder):
        if f.startswith(row["image_id"] + "_") or os.path.splitext(f)[0] == stem:
            return True
    return False


def main(argv):
    dry = "--dry-run" in argv
    rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
    fields = list(rows[0].keys())
    fetched = 0
    for row in rows:
        if have_file(row):
            continue
        url = row.get("original_image_url", "")
        if not url.startswith("http"):
            print(f"  {row['image_id']}: no original_image_url, skipped")
            continue
        name = os.path.basename(urllib.parse.unquote(url.split("?")[0]))
        if not name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            name += ".jpg"
        folder = target_dir(row["candidate_id"])
        local_name = f"{row['image_id']}_{name}"
        dest = os.path.join(folder, local_name)
        rel = os.path.relpath(dest, os.path.join(ROOT, "04_visual_archive")).replace(os.sep, "/")
        if dry:
            print(f"  would fetch {row['image_id']} -> {rel}")
            continue
        os.makedirs(folder, exist_ok=True)
        data = None
        for attempt in range(4):
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = resp.read()
                break
            except Exception as exc:  # noqa: BLE001
                wait = 6 * (attempt + 1)
                print(f"  {row['image_id']}: {type(exc).__name__}, retry in {wait}s")
                time.sleep(wait)
        if data is None:
            print(f"  {row['image_id']}: FAILED after retries")
            continue
        if len(data) < 2000:
            print(f"  {row['image_id']}: suspiciously small ({len(data)} bytes), skipped")
            continue
        with open(dest, "wb") as f:
            f.write(data)
        row["local_filename"] = rel
        fetched += 1
        print(f"  {row['image_id']}: {len(data) // 1024} KB -> {rel}")
        time.sleep(2.5)

    if dry or not fetched:
        print(f"fetched {fetched}")
        return 0
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"fetched {fetched}; image_archive.csv updated")
    return 0


if __name__ == "__main__":
    import urllib.parse  # noqa: F401  (used above via urllib.parse)
    sys.exit(main(sys.argv[1:]))
