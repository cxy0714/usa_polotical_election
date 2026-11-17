#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Turn the discovery pool into a download plan that respects the corpus budget.

Three decisions, all recorded in `discovery/selected.json` so the plan is auditable:

  1. **Who is in the video** — `candidate_source` ANDREWS / GRAHAM / JNT / OTHER,
     read off the title+channel. A debate is `JNT` by construction: both nominees are
     on the same stage, which is exactly why the debates are the highest-value items.
  2. **What kind of event** — `kind_guess`, keyword rules, same vocabulary as
     analyze_speech.py's SPEECH_KINDS plus news_package / ad.
  3. **How much of it to download** — one `yt-dlp -J --skip-download` probe per video
     returns every format with its byte size; the planner then drops from 720p to 480p
     to 360p until the estimated corpus fits `--budget-gb`.

Hard caps from the brief: ≤ 90 videos, ≤ 720p, ≤ 2 GB of video on disk.

    python south-carolina-senate-2026/_staging/vision/select_videos.py --budget-gb 2.0
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys
from pathlib import Path

VISION = Path(__file__).resolve().parent
DISC = VISION / "discovery"
CAND = DISC / "candidates.json"
SEL = DISC / "selected.json"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")

TIERS = (720, 480, 360)          # descending; never above 720 per the brief
DEBATE_CAP = 6
SPEECH_CAP = 46
NEWS_CAP = 44
MAX_VIDEOS = 90

# priority buckets: lower number is downloaded first and gets the better format
PRIO = {"debate": 0, "victory_speech": 1, "concession_speech": 1, "swearing_in": 1,
        "tour_launch": 2, "rally_speech": 2, "interview": 3, "town_hall": 3,
        "ad": 5, "news_package": 4, "other": 6}

KIND_RULES = [
    ("debate", r"\bdebate\b"),
    ("concession_speech", r"concession|concedes"),
    ("victory_speech", r"victory (speech|address)|winner speech|full speech|"
                       r"declares? victory|acceptance speech"),
    ("swearing_in", r"sworn in|swearing[- ]in|sworn-in|takes? the oath"),
    ("tour_launch", r"launch video|launch speech|announcement video|unafraid|"
                    r"campaign launch|kicks off"),
    ("rally_speech", r"\brally\b|\bclemson\b|\bmyrtle beach\b|\btrump\b"),
    ("town_hall", r"town hall"),
    ("interview", r"interview|sits down|one[- ]on[- ]one|q&a|talks to"),
    ("ad", r"campaign ad|\battack ad\b|\btv ad\b"),
]

SPEECHY = {"debate", "victory_speech", "concession_speech", "swearing_in", "tour_launch",
           "rally_speech", "town_hall", "interview"}


def classify(title, channel):
    blob = (title + " " + channel).lower()
    for kind, pat in KIND_RULES:
        if re.search(pat, blob):
            return kind
    return "news_package"


def who(title, channel):
    blob = (title + " " + channel).lower()
    a = "andrews" in blob or "annie andrews" in blob
    g = "graham" in blob or "darline" in blob
    if a and g:
        return "JNT"
    if a:
        return "ANDREWS"
    if g:
        return "GRAHAM"
    if "whitener" in blob or "hackett" in blob:
        return "OTHER"
    return "OTHER"


def probe(vid):
    """format inventory + authoritative metadata, one request."""
    try:
        r = subprocess.run(
            ["python", "-m", "yt_dlp", "--no-warnings", "--skip-download", "-J",
             f"https://www.youtube.com/watch?v={vid}"],
            capture_output=True, timeout=120, env=ENV)
    except subprocess.TimeoutExpired:
        return None
    if r.returncode != 0:
        return None
    try:
        info = json.loads(r.stdout.decode("utf-8", "replace"))
    except json.JSONDecodeError:
        return None
    fmts = []
    for f in info.get("formats") or []:
        fsize = f.get("filesize") or f.get("filesize_approx") or 0
        fmts.append({"height": f.get("height") or 0, "vcodec": f.get("vcodec") or "none",
                     "acodec": f.get("acodec") or "none", "ext": f.get("ext") or "",
                     "size": int(fsize)})
    return {"video_id": vid, "title": info.get("title") or "",
            "channel": info.get("channel") or "",
            "upload_date": info.get("upload_date") or "",
            "duration": float(info.get("duration") or 0),
            "view_count": int(info.get("view_count") or 0),
            "formats": fmts}


def plan_format(prof, tier):
    """Estimated bytes for `<tier>p` using the same selector download_all.py uses.

    `bv*` means "best video stream", i.e. the *highest bitrate at the highest allowed
    height*, not the smallest file — so the estimate must take the max, not the min.
    """
    vids = [f for f in prof["formats"]
            if f["vcodec"] != "none" and 0 < f["height"] <= tier and f["size"]]
    if not vids:
        return 0
    avc = [f for f in vids if f["vcodec"].startswith("avc1")]
    pool = avc or vids
    best_h = max(f["height"] for f in pool)
    v = max(f["size"] for f in pool if f["height"] == best_h)
    auds = [f for f in prof["formats"]
            if f["vcodec"] == "none" and f["acodec"] != "none" and f["size"]]
    m4a = [f for f in auds if f["ext"] == "m4a"]
    a = max(f["size"] for f in (m4a or auds)) if auds else 0
    return v + a


def fmt_string(tier):
    return (f"bv*[height<={tier}][vcodec^=avc1]+ba[ext=m4a]/"
            f"bv*[height<={tier}]+ba/b[height<={tier}]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget-gb", type=float, default=2.0)
    ap.add_argument("--max-videos", type=int, default=MAX_VIDEOS)
    ap.add_argument("--threads", type=int, default=6)
    args = ap.parse_args()

    cands = json.loads(CAND.read_text(encoding="utf-8"))
    print("pool:", len(cands))

    # bucket by kind, then cap, keeping the search-order rank for stability
    for i, c in enumerate(cands):
        c["rank"] = i
        c["kind_guess"] = classify(c.get("title", ""), c.get("channel", ""))
        c["candidate_source"] = who(c.get("title", ""), c.get("channel", ""))
    cands.sort(key=lambda c: (PRIO.get(c["kind_guess"], 6), -c.get("view_count", 0), c["rank"]))

    picked, n_deb, n_sp, n_news = [], 0, 0, 0
    for c in cands:
        k = c["kind_guess"]
        if k == "debate":
            if n_deb >= DEBATE_CAP:
                continue
            n_deb += 1
        elif k in SPEECHY:
            if n_sp >= SPEECH_CAP:
                continue
            n_sp += 1
        else:
            if n_news >= NEWS_CAP:
                continue
            n_news += 1
        picked.append(c)
        if len(picked) >= args.max_videos:
            break
    print(f"after quotas: {len(picked)} (debate {n_deb}, speech {n_sp}, news/ad {n_news})")

    print(f"probing formats for {len(picked)} videos, {args.threads} threads", flush=True)
    profs = {}
    with cf.ThreadPoolExecutor(max_workers=args.threads) as ex:
        futs = {ex.submit(probe, c["video_id"]): c for c in picked}
        for n, fut in enumerate(cf.as_completed(futs), 1):
            c = futs[fut]
            try:
                p = fut.result()
            except Exception:  # noqa: BLE001
                p = None
            if p:
                profs[c["video_id"]] = p
            if n % 20 == 0:
                print(f"  {n}/{len(picked)}", flush=True)
    print("probed:", len(profs))

    # greedy budget fill in priority order; each video gets the best tier that fits
    budget = args.budget_gb * 1e9
    total, kept, skipped = 0, [], []
    for c in picked:
        p = profs.get(c["video_id"])
        if not p or p["duration"] < 20:
            skipped.append((c["video_id"], "no probe / too short"))
            continue
        c.update({k: p[k] for k in ("duration", "upload_date", "channel", "title", "view_count")})
        chosen = None
        for tier in TIERS:
            est = plan_format(p, tier)
            if not est:
                # no byte size in the format list: fall back to a bitrate constant
                est = int(p["duration"] * {720: 1.9e5, 480: 8.0e4, 360: 5.0e4}[tier])
            if total + est <= budget:
                chosen = (tier, est)
                break
        if not chosen:
            skipped.append((c["video_id"], "budget"))
            continue
        tier, est = chosen
        total += est
        c["height_cap"] = tier
        c["format"] = fmt_string(tier)
        c["est_bytes"] = est
        kept.append(c)

    kept.sort(key=lambda c: (PRIO.get(c["kind_guess"], 6), c["rank"]))
    SEL.write_text(json.dumps(kept, ensure_ascii=False, indent=1), encoding="utf-8")
    from collections import Counter
    print(f"selected {len(kept)} videos | estimated {total/1e9:.2f} GB "
          f"(budget {args.budget_gb:.1f} GB)")
    print("kinds:", dict(Counter(c["kind_guess"] for c in kept)))
    print("sources:", dict(Counter(c["candidate_source"] for c in kept)))
    print("tiers:", dict(Counter(c["height_cap"] for c in kept)))
    if skipped:
        print(f"skipped {len(skipped)}:", ", ".join(v for v, _r in skipped[:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
