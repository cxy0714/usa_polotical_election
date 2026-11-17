#!/usr/bin/env python3
"""Select and download the video corpus for Case Study 002.

Discovery already happened (`_staging/vision/discovery/candidates.json`, 144 candidates from
yt-dlp searches). This script classifies, selects, downloads and writes the config the
frame/audio stages consume.

Outputs
  _staging/vision/raw/<slug>_<id>.mp4
  _staging/vision/videos.json            list of {slug,file,video_id,candidate_source,kind,title,channel,upload_date,duration}
  10_video_frames/video_sources.csv      one row per downloaded video

Rules
  - debates are the only hour-long items and are fetched at 480p to stay inside the disk budget
  - everything else is capped at 720p
  - a slug is PREFIX_kind_<id>; PREFIX is AND / GRA / JNT / CTX
  - nothing is invented: kind and candidate_source come from title/channel keywords, and every
    video keeps its real id, channel, upload date and duration

Run: python _staging/vision/sc_download.py [--limit 26] [--dry-run]
"""
import csv
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RAW = os.path.join(HERE, "raw")
CONF = os.path.join(HERE, "videos.json")
DISC = os.path.join(HERE, "discovery", "candidates.json")
SRC_CSV = os.path.join(ROOT, "10_video_frames", "video_sources.csv")

KNOWN = {
    "PyxGkBSpS8g": ("JNT", "debate"),
    "y2q_WK7EYf4": ("JNT", "debate"),
    "cXE2Ik6YxMg": ("JNT", "debate"),
    "J8wMNLaSNW4": ("ANDREWS", "launch"),
    "jjw3a1ZO6j4": ("ANDREWS", "victory_speech"),
    "8AKQvDrng_0": ("ANDREWS", "news"),
    "X-5IhdI5biM": ("ANDREWS", "news"),
    "DN__FMK9Wjw": ("ANDREWS", "news"),
    "rG8w9atWV2c": ("ANDREWS", "ad"),
}

# Curated ids that the search sweep did not return; metadata verified directly with yt-dlp
# (`--print "%(title)s | %(duration)s | %(upload_date)s"`) on 2026-11-12.
ANCHORS = {
    "cXE2Ik6YxMg": {"title": "U.S. Senate Debate | Election 2026", "channel": "South Carolina ETV",
                    "duration": 3549, "upload_date": "20261011"},
}

CURATED = os.path.join(HERE, "sc_curated.csv")

DEBATE_HINTS = ("debate", "forum")
LAUNCH_HINTS = ("launch", "announcement", "announces")
VICTORY_HINTS = ("victory", "winner", "wins", "concession", "speech")
RALLY_HINTS = ("rally", "clemson", "myrtle", "trump")
AD_HINTS = ("ad ", "advert", "spot", "commercial")
NEWS_HINTS = ("nbc", "cbs", "abc", "cnn", "fox", "news", "report", "wjbf", "wis", "wciv",
              "live 5", "wbtw", "wmbf", "ap ", "reuters", "guardian", "politico")


def classify(entry):
    vid = entry["video_id"]
    if vid in KNOWN:
        return KNOWN[vid]
    blob = (entry.get("title") or "").lower() + " " + (entry.get("channel") or "").lower()
    kind = "news"
    if any(h in blob for h in DEBATE_HINTS):
        kind = "debate"
    elif any(h in blob for h in RALLY_HINTS):
        kind = "rally"
    elif any(h in blob for h in LAUNCH_HINTS):
        kind = "launch"
    elif any(h in blob for h in VICTORY_HINTS):
        kind = "speech"
    elif any(h in blob for h in AD_HINTS):
        kind = "ad"
    if "andrews" in blob and "graham" not in blob:
        cand = "ANDREWS"
    elif "graham" in blob and "andrews" not in blob:
        cand = "GRAHAM"
    elif "andrews" in blob and "graham" in blob:
        cand = "JNT"
    else:
        cand = "CTX"
    if kind == "debate":
        cand = "JNT"
    return cand, kind


def score(entry, cand, kind):
    s = 0
    ch = (entry.get("channel") or "").lower()
    if kind in ("debate", "launch", "victory_speech", "speech"):
        s += 60
    if "official campaign" in ch or ch in ("annie andrews", "darline graham"):
        s += 30
    if kind == "rally":
        s += 25
    if kind == "ad":
        s += 20
    if kind == "news":
        s += 10
    dur = entry.get("duration") or 0
    if 60 <= dur <= 1200:
        s += 10
    s += min((entry.get("view_count") or 0) / 50000.0, 8)
    return s


def slugify(cand, kind, vid):
    return f"{'AND' if cand == 'ANDREWS' else 'GRA' if cand == 'GRAHAM' else 'JNT' if cand == 'JNT' else 'CTX'}_{kind}_{vid}"


def main():
    limit = 26
    dry = "--dry-run" in sys.argv
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    entries = json.load(open(DISC, encoding="utf-8"))

    if os.path.exists(CURATED):
        # Curated mode: the clip list was chosen by hand for documentary reach, so the scorer is
        # bypassed entirely and only the ordering of the file matters.
        by_id = {}
        for e in entries:
            by_id.setdefault(e["video_id"], e)
        chosen = []
        for r in csv.DictReader(open(CURATED, encoding="utf-8")):
            vid = r["video_id"].strip()
            meta = dict(by_id.get(vid) or ANCHORS.get(vid) or {})
            if not meta:
                print(f"  MISSING metadata for curated id {vid}; skipping")
                continue
            meta["video_id"] = vid
            meta["candidate_source"] = r["candidate_source"].strip()
            meta["kind"] = r["kind"].strip()
            meta["curation_note"] = r["why"].strip()
            chosen.append(meta)
        print(f"curated mode: {len(chosen)} videos")
        per_cand = {}
        for e in chosen:
            per_cand[e["candidate_source"]] = per_cand.get(e["candidate_source"], 0) + 1
        print(f"selected {len(chosen)} videos: {per_cand}")
        for e in chosen:
            print(f"  {e['candidate_source']:8s} {e['kind']:22s} "
                  f"{float(e.get('duration') or 0):7.0f}s  {e['title'][:62]}")
        if dry:
            return 0
        return download_all(chosen)

    picked = {}
    seen_titles = set()
    for e in entries:
        vid = e["video_id"]
        if not re.fullmatch(r"[\w-]{11}", vid):
            continue
        if vid in picked:
            continue
        # the same upload often appears as "Title" and "Title (Captioned)" — keep the first
        norm_title = re.sub(r"[^a-z0-9]+", " ", (e.get("title") or "").lower())
        norm_title = re.sub(r"\b(captioned|hd|full|official|video)\b", "", norm_title).strip()
        if norm_title in seen_titles:
            continue
        seen_titles.add(norm_title)
        cand, kind = classify(e)
        picked[vid] = dict(e, candidate_source=cand, kind=kind,
                           score=score(e, cand, kind))
    ranked = sorted(picked.values(), key=lambda x: -x["score"])

    chosen = []
    # one debate is mandatory — the 08-18 runoff and the 10-11 general are the anchors
    for vid in ("PyxGkBSpS8g", "cXE2Ik6YxMg"):
        for e in ranked:
            if e["video_id"] == vid and e not in chosen:
                chosen.append(e)
    per_cand = {"ANDREWS": 0, "GRAHAM": 0, "JNT": 0, "CTX": 0}
    caps = {"ANDREWS": 9, "GRAHAM": 9, "JNT": 6, "CTX": 5}
    for e in ranked:
        if len(chosen) >= limit:
            break
        c = e["candidate_source"]
        if e in chosen or per_cand[c] >= caps[c]:
            continue
        chosen.append(e)
        per_cand[c] += 1

    print(f"selected {len(chosen)} videos: {per_cand}")
    for e in chosen:
        print(f"  {e['candidate_source']:8s} {e['kind']:14s} {e['duration'] or 0:7.0f}s  {e['title'][:70]}")

    if dry:
        return 0
    return download_all(chosen)


def download_all(chosen):
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(os.path.dirname(SRC_CSV), exist_ok=True)
    conf = []
    for e in chosen:
        slug = slugify(e["candidate_source"], e["kind"], e["video_id"])
        out = os.path.join(RAW, f"{slug}.mp4")
        if os.path.exists(out) and os.path.getsize(out) > 100_000:
            size = os.path.getsize(out)
        else:
            fmt = ("bv*[height<=480][ext=mp4]+ba[ext=m4a]/b[height<=480]/b"
                   if (e["duration"] or 0) > 1800 else
                   "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]/b")
            cmd = [sys.executable, "-m", "yt_dlp", "-f", fmt, "--merge-output-format", "mp4",
                   "--no-playlist", "--no-warnings", "--retries", "3",
                   "-o", out, f"https://www.youtube.com/watch?v={e['video_id']}"]
            print(f"downloading {slug} ...", flush=True)
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                               errors="replace")
            if r.returncode != 0 or not os.path.exists(out):
                print(f"  FAILED {slug}: {(r.stderr or '')[-300:]}")
                continue
            size = os.path.getsize(out)
        conf.append({
            "slug": slug,
            "file": os.path.basename(out),
            "video_id": e["video_id"],
            "candidate_source": e["candidate_source"],
            "kind": e["kind"],
            "title": e.get("title", "unknown"),
            "channel": e.get("channel", "unknown"),
            "upload_date": (e.get("upload_date") or "unknown")[:4] + "-" +
                            (e.get("upload_date") or "unknown")[4:6] + "-" +
                            (e.get("upload_date") or "unknown")[6:8]
                            if (e.get("upload_date") and len(e.get("upload_date")) == 8)
                            else "unknown",
            "duration": int(e.get("duration") or 0),
            "bytes": size,
        })
        print(f"  ok {slug} {size/1e6:.1f} MB")

    with open(CONF, "w", encoding="utf-8") as f:
        json.dump(conf, f, ensure_ascii=False, indent=1)

    with open(SRC_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["video_id", "slug", "candidate_source", "kind", "title", "channel",
                    "upload_date", "duration_s", "url", "local_file", "bytes"])
        for c in conf:
            w.writerow([c["video_id"], c["slug"], c["candidate_source"], c["kind"], c["title"],
                        c["channel"], c["upload_date"], c["duration"],
                        f"https://www.youtube.com/watch?v={c['video_id']}", c["file"],
                        c["bytes"]])
    total = sum(c["bytes"] for c in conf)
    print(f"downloaded {len(conf)} videos, {total/1e9:.2f} GB -> {CONF}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
