"""Retry the Commons image downloads with pacing (429 back-off)."""
import csv
import datetime
import json
import os
import time
import urllib.request

UA = "Mozilla/5.0 (research archive; contact: research@example.org)"
LOG = "_staging/fetch_log.csv"


def log_row(url, status, nbytes, saved, note):
    with open(LOG, "a", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerow(
            [url, status, nbytes, datetime.datetime.now().isoformat(timespec="seconds"),
             saved, note])


imgs = json.load(open("_staging/images.json", encoding="utf-8"))
done = 0
for rec in imgs:
    if rec["status"] != "download":
        continue
    if rec["local_file"] != "unknown" and os.path.exists(rec["local_file"]):
        continue
    if not rec["orig_url"].startswith("https://upload.wikimedia.org"):
        print("skip (no direct url):", rec["key"], rec["orig_url"][:70])
        continue
    if rec["size"] > 2_000_000:
        print("skip (too large):", rec["key"], rec["size"])
        continue
    cand = "brown" if rec["candidate"] == "BROWN" else "husted"
    ext = os.path.splitext(rec["orig_url"].split("?")[0])[1] or ".jpg"
    dest = f"04_visual_archive/{cand}/{rec['key']}{ext}"
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    ok = False
    for attempt in range(4):
        try:
            req = urllib.request.Request(rec["orig_url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            open(dest, "wb").write(data)
            log_row(rec["orig_url"], "200", len(data), dest, "Commons image download")
            rec["local_file"] = dest
            rec["size"] = len(data)
            done += 1
            ok = True
            print("ok", rec["key"], len(data))
            break
        except Exception as exc:  # noqa: BLE001
            print("retry", rec["key"], attempt, str(exc)[:80])
            time.sleep(8 * (attempt + 1))
    if not ok:
        log_row(rec["orig_url"], "429", 0, "unknown", "image download failed after retries")
    time.sleep(4)

json.dump(imgs, open("_staging/images.json", "w", encoding="utf-8"), indent=1,
          ensure_ascii=False)
print("downloaded", done)
