#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Download the expanded video set: legacy config + discovered selection.

Two phases, because YouTube rate-limits caption requests hard:

  1. video+audio (N parallel, 480p for long uploads / 720p for short clips)
  2. captions (sequential, backoff) — a caption failure never invalidates a video

Sidecar files in _staging/vision/raw/:

    <slug>_<id>.mp4          merged video+audio
    <slug>_<id>.info.json    yt-dlp metadata (title, channel, upload_date, ...)
    <slug>_<id>.<lang>.vtt   auto/manual English captions when available

Regenerates _staging/vision/videos.json (legacy order first, then new by score)
and download_report.csv. Re-running resumes: present mp4s are skipped.

    python texas-senate-2026/_staging/vision/download_all.py --jobs 7
"""
import argparse
import concurrent.futures as cf
import csv
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

VISION = Path(__file__).resolve().parent
RAW = VISION / "raw"
CONFIG = VISION / "videos.json"
CAND = VISION / "discovery" / "selected.json"
REPORT = VISION / "download_report.csv"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
ID_RE = re.compile(r"_([A-Za-z0-9_-]{11})\.mp4$")

CITY_PATTERNS = [
    ("san_antonio", r"san antonio"), ("el_paso", r"el paso"), ("fort_worth", r"fort worth"),
    ("college_station", r"college station"), ("clear_lake", r"clear lake"),
    ("round_rock", r"round rock"), ("san_marcos", r"san marcos"),
]
CITIES = [
    "houston", "dallas", "austin", "lubbock", "tyler", "waco", "plano", "conroe",
    "allen", "cypress", "brownsville", "laredo", "mcallen", "corpus", "midland",
    "odessa", "rockwall", "denton", "arlington", "beaumont", "amarillo", "abilene",
    "killeen", "wylie", "frisco", "mckinney", "irving", "garland", "pearland",
    "sugarland", "texarkana", "longview", "temple", "bryan", "elpaso",
]
CHANNEL_ABBR = [
    (r"james talarico", "jtc"), (r"ken paxton", "kpc"),
    (r"associated press", "ap"), (r"usa today", "usat"), (r"pbs newshour", "pbs"),
    (r"good morning america", "gma"), (r"fox 4", "fox4"), (r"fox 26", "fox26"),
    (r"fox news", "foxn"), (r"khou", "khou"), (r"kvue", "kvue"), (r"kxan", "kxan"),
    (r"kens", "kens"), (r"kxxv", "kxxv"), (r"ketk", "ketk"), (r"cbs19", "cbs19"),
    (r"cbs texas", "cbstx"), (r"nbc dfw", "nbcdfw"), (r"nbc", "nbc"), (r"cbs", "cbs"),
    (r"abc13", "abc13"), (r"abc", "abc"), (r"cnn", "cnn"), (r"msnbc", "msnbc"),
    (r"the hill", "hill"), (r"wfaa", "wfaa"), (r"spectrum", "spectrum"),
    (r"telemundo", "telemundo"), (r"univision", "univision"), (r"dallas morning", "dmnews"),
    (r"fox news clips", "foxn"), (r"cbs mornings", "cbsm"), (r"cbs evening", "cbse"),
]
KIND_TOKEN = {
    "concession_speech": "concession", "victory_speech": "victory",
    "convention_speech": "convention", "town_hall": "townhall",
    "debate": "debate", "interview": "interview", "ad": "ad",
    "tour_launch": "tour", "final_rally": "final", "news_package": "news",
    "rally_speech": "rally",
}


def make_slug(title, channel, kind, existing):
    blob = f"{title} {channel}".lower()
    if "talarico" in blob and "paxton" in blob:
        cand = "BOTH"
    elif "talarico" in blob:
        cand = "TAL"
    elif "paxton" in blob:
        cand = "PAX"
    else:
        cand = "OTH"
    venue = "tx"
    for name, pat in CITY_PATTERNS:
        if re.search(pat, blob):
            venue = name
            break
    else:
        for c in CITIES:
            if re.search(r"\b" + re.escape(c) + r"\b", blob):
                venue = c
                break
    chan = "web"
    for pat, ab in CHANNEL_ABBR:
        if re.search(pat, channel.lower()):
            chan = ab
            break
    ktok = KIND_TOKEN.get(kind, "clip")
    base = f"{cand}_{venue}_{ktok}_{chan}"
    slug, n = base, 2
    while slug in existing:
        slug, n = f"{base}{n}", n + 1
    return slug


def pick_format(duration):
    return ("bv*[height<=480]+ba/b[height<=480]" if duration > 1200
            else "bv*[height<=720]+ba/b[height<=720]")


def download(v):
    out_tmpl = str(RAW / f"{v['slug']}_%(id)s.%(ext)s")
    cmd = ["python", "-m", "yt_dlp", "--no-warnings", "--no-playlist",
           "-f", pick_format(v.get("duration") or 0), "--merge-output-format", "mp4",
           "--write-info-json",
           "--retries", "3", "--fragment-retries", "5", "--socket-timeout", "20",
           "-o", out_tmpl,
           f"https://www.youtube.com/watch?v={v['video_id']}"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=2400, env=ENV)
    except subprocess.TimeoutExpired:
        return v["slug"], "timeout", 0, ""
    hits = list(RAW.glob(f"{v['slug']}_*.mp4"))
    size = hits[0].stat().st_size if hits else 0
    if size == 0:
        tail = (r.stderr or "").strip().splitlines()[-2:]
        return v["slug"], "failed", 0, " | ".join(tail)
    return v["slug"], "ok", size, ""


def fetch_subs(v):
    cmd = ["python", "-m", "yt_dlp", "--no-warnings", "--skip-download",
           "--write-auto-subs", "--write-subs", "--sub-langs", "en,en-US,en-orig",
           "--sub-format", "vtt", "--retries", "2", "--socket-timeout", "20",
           "-o", str(RAW / f"{v['slug']}_%(id)s.%(ext)s"),
           f"https://www.youtube.com/watch?v={v['video_id']}"]
    for attempt in range(3):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=180, env=ENV)
        except subprocess.TimeoutExpired:
            return False
        if list(RAW.glob(f"{v['slug']}_{v['video_id']}*.vtt")):
            return True
        if "429" in (r.stderr or ""):
            time.sleep(3 * (attempt + 1))
            continue
        return False
    return False


def raw_index():
    """video_id -> mp4 file name already on disk."""
    idx = {}
    for p in RAW.glob("*.mp4"):
        m = ID_RE.search(p.name)
        if m:
            idx[m.group(1)] = p.name
    return idx


def read_info(slug, vid):
    p = RAW / f"{slug}_{vid}.info.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def enrich(entry, info):
    if info:
        entry["title"] = info.get("title") or entry["title"]
        entry["channel"] = info.get("channel") or entry["channel"]
        entry["upload_date"] = info.get("upload_date") or entry.get("upload_date", "")
        if info.get("duration"):
            entry["duration"] = int(info["duration"])
    return entry


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--budget-gb", type=float, default=20.0)
    ap.add_argument("--no-subs", action="store_true")
    args = ap.parse_args()

    legacy = json.loads(CONFIG.read_text(encoding="utf-8"))
    cands = json.loads(CAND.read_text(encoding="utf-8")) if CAND.exists() else []
    idx = raw_index()
    RAW.mkdir(parents=True, exist_ok=True)
    known_ids = {v["video_id"] for v in legacy}

    used_slugs = {v["slug"] for v in legacy}
    new_entries, todo = [], []
    for c in cands:
        vid = c["video_id"]
        if vid in known_ids:
            continue
        if args.limit and len(new_entries) + len(todo) >= args.limit:
            break
        slug = make_slug(c["title"], c["channel"], c["kind_guess"], used_slugs)
        used_slugs.add(slug)
        entry = {
            "slug": slug,
            "file": idx.get(vid) or f"{slug}_{vid}.mp4",
            "video_id": vid,
            "candidate_source": ("BOTH" if slug.startswith("BOTH") else
                                 "TALARICO" if slug.startswith("TAL") else
                                 "PAXTON" if slug.startswith("PAX") else "OTHER"),
            "kind": c["kind_guess"],
            "title": c["title"], "channel": c["channel"],
            "duration": int(c["duration"]),
            "upload_date": "",
        }
        if vid in idx:
            new_entries.append(enrich(entry, read_info(slug, vid)))
        else:
            todo.append(entry)

    legacy_todo = [dict(v, file=idx.get(v["video_id"]) or v["file"], origin="legacy")
                   for v in legacy if v["video_id"] not in idx]
    todo = legacy_todo + todo
    print(f"to download: {len(todo)} ({len(legacy_todo)} legacy, {len(todo) - len(legacy_todo)} new)"
          f" | already on disk: {len(idx)}", flush=True)

    results, failed = [], []
    total_bytes = sum(p.stat().st_size for p in RAW.glob("*.mp4"))
    if todo:
        with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
            futs = {ex.submit(download, v): v for v in todo}
            for i, fut in enumerate(cf.as_completed(futs), 1):
                v = futs[fut]
                try:
                    slug, status, size, err = fut.result()
                except Exception as e:  # noqa: BLE001
                    slug, status, size, err = v["slug"], "error", 0, str(e)
                print(f"[{i}/{len(todo)}] {status:8s} {slug:34s} {size/1e6:7.1f} MB  {err}", flush=True)
                results.append({"slug": slug, "status": status, "bytes": size, "error": err})
                if status != "ok":
                    failed.append(v)
                    continue
                total_bytes += size
                v["file"] = idx.get(v["video_id"]) or v["file"]
                hits = list(RAW.glob(f"{v['slug']}_*.mp4"))
                if hits:
                    v["file"] = hits[0].name
                enrich(v, read_info(v["slug"], v["video_id"]))
                if v.get("origin") != "legacy" and v not in new_entries:
                    new_entries.append({k: v[k] for k in ("slug", "file", "video_id",
                                                          "candidate_source", "kind", "title",
                                                          "channel", "upload_date", "duration")})
                if total_bytes > args.budget_gb * 1e9:
                    print("budget reached; cancelling queued downloads", flush=True)
                    for f2 in futs:
                        f2.cancel()

    # stable config: legacy order preserved, then new entries by discovery score order
    cfg = []
    for v in legacy:
        hits = list(RAW.glob(f"{v['slug']}_*.mp4"))
        entry = {k: v[k] for k in ("slug", "file", "video_id", "candidate_source", "kind",
                                   "title", "channel", "upload_date", "duration")}
        if hits:
            entry["file"] = hits[0].name
        cfg.append(entry)
    have = {c["video_id"] for c in cfg}
    rank = {c["video_id"]: c.get("rank", 9999) for c in cands}
    for e in sorted(new_entries, key=lambda e: rank.get(e["video_id"], 9999)):
        if e["video_id"] not in have:
            cfg.append(e)
            have.add(e["video_id"])
    CONFIG.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")

    with open(REPORT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["slug", "status", "bytes", "error"])
        w.writeheader()
        w.writerows(results)

    print(f"config entries: {len(cfg)} | ok: {sum(1 for r in results if r['status']=='ok')}"
          f" | failed: {len(failed)} | corpus: {total_bytes/1e9:.1f} GB")
    if failed:
        print("failed:", ", ".join(v["slug"] for v in failed))

    if not args.no_subs:
        missing = [v for v in cfg if (RAW / v["file"]).exists()
                   and not list(RAW.glob(f"{v['slug']}_{v['video_id']}*.vtt"))]
        print(f"captions: {len(missing)} videos without a .vtt — fetching sequentially", flush=True)
        ok = 0
        for i, v in enumerate(missing, 1):
            got = fetch_subs(v)
            ok += int(got)
            print(f"  [{i}/{len(missing)}] {v['slug']:34s} {'vtt' if got else 'none'}", flush=True)
            time.sleep(1.2)
        print(f"captions fetched: {ok}/{len(missing)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
