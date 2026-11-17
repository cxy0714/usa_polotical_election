#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Search YouTube for South Carolina 2026 Senate race video, then enrich with metadata.

Two passes because the two things are cheap in different ways:

  1. `yt-dlp --flat-playlist ytsearch12:QUERY` — ~2.5 s per query, returns
     id / title / duration / channel. No upload date.
  2. per-candidate metadata pass — ~3.5 s per video, 8 threads — pulls
     upload_date, real duration, channel, view_count.

The upload-date window (2025-01-01 .. 2026-11-12) is applied *here*, because
`--flat-playlist` cannot supply it and a pre-2025 upload cannot be about this race
(Andrews launched in 2025; the vacancy opened 2026-07-11).

Output: _staging/vision/discovery/candidates.json  (+ search_log.json)
    python south-carolina-senate-2026/_staging/vision/discover_videos.py
    python .../discover_videos.py --refresh-metadata   # reuse the search, re-probe dates
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

VISION = Path(__file__).resolve().parent
DISC = VISION / "discovery"
CAND = DISC / "candidates.json"
LOG = DISC / "search_log.json"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")

DATE_MIN, DATE_MAX = "20250101", "20261112"
PER_QUERY = 12

QUERIES = [
    "Annie Andrews South Carolina Senate",
    "Darline Graham Senate South Carolina",
    "Annie Andrews Senate launch Unafraid",
    "South Carolina Senate debate 2026 Andrews Graham Whitener",
    "South Carolina Republican Senate runoff debate Graham Norman",
    "Darline Graham sworn in senator",
    "Trump rally Myrtle Beach Darline Graham",
    "Darline Graham Clemson rally October 2026",
    "Annie Andrews victory speech South Carolina Senate",
    "Darline Graham concession South Carolina Senate",
    "South Carolina Senate race results November 2026",
    "Annie Andrews concession OR victory night",
    "Darline Graham special primary election night",
    "Annie Andrews primary night June 2026",
    "South Carolina Senate debate October 2026",
    # added after the first pass: the vacancy, the runoff result and the two campaigns
    "Lindsey Graham sister Darline appointed Senate",
    "Darline Graham appointed senator South Carolina July 2026",
    "South Carolina Senate special primary August 2026 results",
    "South Carolina Senate runoff results Graham Norman August 2026",
    "Annie Andrews Charleston Senate campaign",
    "Darline Graham campaign rally South Carolina",
    "South Carolina Senate debate Graham Andrews SCETV",
    "Kasie Whitener South Carolina Senate Libertarian",
    "Annie Andrews senator elect interview",
    "Darline Graham senator interview South Carolina",
    "South Carolina Senate election night 2026 results Andrews Graham",
]

# forced inclusions: real ids verified in this session (see G_gaps.md §1)
KNOWN_IDS = ["PyxGkBSpS8g", "y2q_WK7EYf4", "cXE2Ik6YxMg", "J8wMNLaSNW4",
             "jjw3a1ZO6j4", "8AKQvDrng_0", "X-5IhdI5biM", "DN__FMK9Wjw"]

OFF_RACE = re.compile(
    r"\b(texas|florida|north carolina|georgia senate|ohio|pennsylvania|arizona|"
    r"michigan|wisconsin|nevada|new hampshire|maine|governor|mayor|city council|"
    r"school board|house race|congressional district|2028|state house)\b")


def run(args, timeout=180):
    try:
        r = subprocess.run(args, capture_output=True, timeout=timeout, env=ENV)
    except subprocess.TimeoutExpired:
        return None
    out = r.stdout.decode("utf-8", "replace")
    return out


def search(q):
    out = run(["python", "-m", "yt_dlp", "--no-warnings", "--flat-playlist",
               "--print", "%(id)s|%(title)s|%(duration)s|%(channel)s",
               f"ytsearch{PER_QUERY}:{q}"])
    hits = []
    for line in (out or "").splitlines():
        parts = line.split("|")
        if len(parts) < 4 or not re.fullmatch(r"[A-Za-z0-9_-]{11}", parts[0]):
            continue
        try:
            dur = float(parts[2]) if parts[2] not in ("NA", "None", "") else 0.0
        except ValueError:
            dur = 0.0
        hits.append({"video_id": parts[0], "title": parts[1], "duration": dur,
                     "channel": parts[3]})
    return hits


def meta(vid):
    out = run(["python", "-m", "yt_dlp", "--no-warnings", "--skip-download",
               "--print", "%(id)s\t%(upload_date)s\t%(duration)s\t%(channel)s\t"
                          "%(view_count)s\t%(title)s",
               f"https://www.youtube.com/watch?v={vid}"], timeout=90)
    if not out:
        return None
    line = out.strip().splitlines()[0]
    p = line.split("\t")
    if len(p) < 6:
        return None
    try:
        dur = float(p[2]) if p[2] not in ("NA", "None", "") else 0.0
    except ValueError:
        dur = 0.0
    try:
        views = int(p[4])
    except (ValueError, TypeError):
        views = 0
    return {"video_id": p[0], "upload_date": p[1] if p[1] not in ("NA", "None") else "",
            "duration": dur, "channel": p[3], "view_count": views, "title": p[5]}


def is_race(title, channel=""):
    blob = (title + " " + channel).lower()
    if OFF_RACE.search(blob):
        return False
    cand = any(k in blob for k in ("andrews", "graham", "whitener", "hackett"))
    sc = ("south carolina" in blob) or re.search(r"\bsc\b", blob) is not None
    return cand or sc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh-metadata", action="store_true",
                    help="keep the existing search results, re-probe upload dates only")
    ap.add_argument("--threads", type=int, default=8)
    args = ap.parse_args()
    DISC.mkdir(parents=True, exist_ok=True)

    seen = {}
    log = []
    if args.refresh_metadata and CAND.exists():
        old = json.loads(CAND.read_text(encoding="utf-8"))
        seen = {c["video_id"]: c for c in old}
        log = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else []
        print("reusing", len(seen), "candidates")
    else:
        for i, q in enumerate(QUERIES, 1):
            t0 = time.time()
            hits = search(q)
            new = 0
            for h in hits:
                if h["video_id"] not in seen:
                    h["queries"] = [q]
                    seen[h["video_id"]] = h
                    new += 1
                else:
                    seen[h["video_id"]].setdefault("queries", []).append(q)
            log.append({"query": q, "results": len(hits), "new": new,
                        "elapsed_s": round(time.time() - t0, 1)})
            print(f"[{i}/{len(QUERIES)}] {len(hits):2d} hits ({new} new) {q}", flush=True)
        for vid in KNOWN_IDS:
            seen.setdefault(vid, {"video_id": vid, "title": "", "duration": 0.0,
                                  "channel": "", "queries": ["forced:known_id"]})
            seen[vid].setdefault("queries", []).append("forced:known_id")

    todo = [vid for vid in seen if not seen[vid].get("upload_date")]
    print(f"metadata pass: {len(todo)} videos, {args.threads} threads", flush=True)
    done = 0
    with cf.ThreadPoolExecutor(max_workers=args.threads) as ex:
        futs = {ex.submit(meta, vid): vid for vid in todo}
        for fut in cf.as_completed(futs):
            vid = futs[fut]
            try:
                m = fut.result()
            except Exception as e:  # noqa: BLE001
                m = None
                seen[vid]["meta_error"] = f"{type(e).__name__}: {e}"
            done += 1
            if m:
                seen[vid].update({k: m[k] for k in ("upload_date", "duration",
                                                    "channel", "view_count", "title")})
            if done % 25 == 0:
                print(f"  {done}/{len(todo)}", flush=True)
    have = sum(1 for c in seen.values() if c.get("upload_date"))
    print(f"metadata ok for {have}/{len(seen)}")

    keep, dropped_date, dropped_topic = [], 0, 0
    for c in seen.values():
        d = c.get("upload_date") or ""
        if not d or not (DATE_MIN <= d <= DATE_MAX):
            dropped_date += 1
            continue
        if not is_race(c.get("title", ""), c.get("channel", "")):
            dropped_topic += 1
            continue
        keep.append(c)
    keep.sort(key=lambda c: (c["upload_date"], c["video_id"]))
    CAND.write_text(json.dumps(keep, ensure_ascii=False, indent=1), encoding="utf-8")
    LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"candidates kept: {len(keep)} | dropped {dropped_date} outside the date window, "
          f"{dropped_topic} off-topic")
    return 0


if __name__ == "__main__":
    sys.exit(main())
