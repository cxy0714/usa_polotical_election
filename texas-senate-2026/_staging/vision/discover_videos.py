#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Discover candidate videos for the Texas Senate 2026 archive via YouTube search.

Runs ~30 targeted yt-dlp searches (flat playlists, metadata only), merges the
results, drops videos that are already configured, scores relevance from the
title/channel, and writes:

    _staging/vision/discovery/candidates.json   merged, scored, de-duplicated
    _staging/vision/discovery/candidates.csv    human-readable review table

Nothing is downloaded here. Review the CSV, then run download_all.py.

    python texas-senate-2026/_staging/vision/discover_videos.py --per-query 40
"""
import argparse
import concurrent.futures as cf
import csv
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# yt-dlp writes to a pipe in the console code page on Windows unless this is set.
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")

VISION = Path(__file__).resolve().parent
OUT = VISION / "discovery"
CONFIG = VISION / "videos.json"

# (query, tag) — tag groups the query so coverage can be audited later.
QUERIES = [
    ("James Talarico Texas Senate", "talarico"),
    ("James Talarico rally", "talarico"),
    ("James Talarico speech", "talarico"),
    ("James Talarico full speech", "talarico"),
    ("James Talarico town hall", "talarico"),
    ("James Talarico interview", "talarico"),
    ("James Talarico victory speech", "talarico"),
    ("James Talarico campaign launch", "talarico"),
    ("James Talarico bus tour", "talarico"),
    ("James Talarico border", "talarico"),
    ("James Talarico Houston", "talarico"),
    ("James Talarico Dallas", "talarico"),
    ("James Talarico Austin", "talarico"),
    ("James Talarico San Antonio", "talarico"),
    ("James Talarico El Paso", "talarico"),
    ("James Talarico Lubbock", "talarico"),
    ("James Talarico ad", "talarico"),
    ("Ken Paxton Texas Senate", "paxton"),
    ("Ken Paxton rally", "paxton"),
    ("Ken Paxton full speech", "paxton"),
    ("Ken Paxton speech Texas", "paxton"),
    ("Ken Paxton debate", "paxton"),
    ("Ken Paxton concession speech", "paxton"),
    ("Ken Paxton bus tour", "paxton"),
    ("Ken Paxton campaign", "paxton"),
    ("Ken Paxton Trump endorsement", "paxton"),
    ("Ken Paxton Cornyn primary", "paxton"),
    ("Ken Paxton ad", "paxton"),
    ("Ken Paxton impeachment", "paxton"),
    ("Texas Senate race 2026 Talarico Paxton", "race"),
    ("Texas Senate debate 2026", "race"),
    ("Texas Senate election results 2026", "race"),
    ("Talarico Paxton poll", "race"),
    ("Texas Senate race Talarico leads", "race"),
    ("Texas midterm election 2026 Senate", "race"),
]

NAME_RE = re.compile(r"talarico|paxton", re.I)
TAL_RE = re.compile(r"talarico", re.I)
PAX_RE = re.compile(r"paxton", re.I)
SENATE_RE = re.compile(r"senate|texas|campaign|rally|speech|election|midterm|vote|concession|victory", re.I)
# Other people named Paxton (actor Bill Paxton, Paxton, IL, etc.) — cheap guard.
NOISE_RE = re.compile(r"bill paxton|paxton,? il|paxton illinois|paxton,? fl|paxton,? ca|paxton,? ut", re.I)

KIND_RULES = [
    ("concession_speech", r"conced|concession"),
    ("victory_speech", r"victory (speech|party|rally)|wins|win the|projected|declares? victory|election night"),
    ("convention_speech", r"convention|rnc|nomination"),
    ("town_hall", r"town hall|townhall|jubilee"),
    ("debate", r"debate"),
    ("interview", r"interview|colbert|ms now|meet the press|sunday|briefing|podcast|one-on-one"),
    ("ad", r"\bad\b|attack ad|tv ad|commercial|spot"),
    ("tour_launch", r"kick(s|ed)? off|launch|announc|bus tour|tour"),
    ("final_rally", r"final (rally|push)|last rally|eve of"),
    ("news_package", r"news|package|report|update|results|projection|watch party|poll|react|voters|explain"),
    ("rally_speech", r"rally|speech|remarks|speaks|address|delivers|unveils|slams|exposes|shuts down|response|vision|plan for|accepts"),
]
MIN_DUR, MAX_DUR = 20, 10800
OFFICIAL = re.compile(r"james talarico|ken paxton for senate|paxton for senate", re.I)


def run_search(query, n):
    cmd = ["python", "-m", "yt_dlp", "--flat-playlist", "--no-warnings",
           "--print", "%(id)s|%(title)s|%(channel)s|%(duration)s|%(view_count)s",
           f"ytsearch{n}:{query}"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=180, env=ENV)
    except subprocess.TimeoutExpired:
        print("  timeout:", query, flush=True)
        return []
    rows = []
    for line in r.stdout.splitlines():
        parts = line.split("|")
        if len(parts) < 4 or len(parts[0]) < 6:
            continue
        vid, title, channel = parts[0].strip(), parts[1].strip(), parts[2].strip()
        try:
            dur = float(parts[3]) if parts[3] not in ("NA", "None", "") else 0.0
        except ValueError:
            dur = 0.0
        try:
            views = int(parts[4]) if len(parts) > 4 and parts[4].isdigit() else 0
        except ValueError:
            views = 0
        rows.append({"video_id": vid, "title": title, "channel": channel,
                     "duration": dur, "views": views})
    return rows


def classify(title, channel=""):
    t = title.lower()
    for kind, pat in KIND_RULES:
        if re.search(pat, t):
            return kind
    if OFFICIAL.search(channel) and len(title) > 20:
        return "rally_speech"   # official channel long-form clip of the candidate speaking
    return "other"


def score(c):
    """Relevance score: name + race keywords + official/news channel + popularity."""
    s = 0.0
    title = c["title"]
    if TAL_RE.search(title):
        s += 3
    if PAX_RE.search(title):
        s += 3
    if SENATE_RE.search(title):
        s += 2
    if re.search(r"full (speech|video)|live|watch", title, re.I):
        s += 1
    ch = c["channel"].lower()
    if "talarico" in ch or "paxton" in ch:
        s += 4                      # official campaign channel
    elif re.search(r"cnn|abc|nbc|cbs|fox|pbs|ap |associated press|reuters|news|npr|usa today", ch):
        s += 2
    s += min(2.0, c["views"] / 100_000)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-query", type=int, default=40)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    known = {v["video_id"] for v in json.loads(CONFIG.read_text(encoding="utf-8"))}
    print(f"{len(QUERIES)} queries x {args.per_query} results, {len(known)} already configured")

    found = {}
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_search, q, args.per_query): (q, tag) for q, tag in QUERIES}
        for fut in cf.as_completed(futs):
            q, tag = futs[fut]
            rows = fut.result()
            new = 0
            for c in rows:
                vid = c["video_id"]
                if vid in found:
                    found[vid]["queries"].add(tag)
                    continue
                c["queries"] = {tag}
                found[vid] = c
                new += 1
            print(f"  {q!r}: {len(rows)} results, {new} new ids", flush=True)

    kept, dropped = [], {"known": 0, "noise": 0, "irrelevant": 0, "duration": 0}
    for c in found.values():
        if c["video_id"] in known:
            dropped["known"] += 1
            continue
        blob = f'{c["title"]} {c["channel"]}'
        if NOISE_RE.search(blob):
            dropped["noise"] += 1
            continue
        has_tal, has_pax = bool(TAL_RE.search(blob)), bool(PAX_RE.search(blob))
        if not (has_tal or (has_pax and SENATE_RE.search(blob))):
            dropped["irrelevant"] += 1
            continue
        if not (MIN_DUR <= c["duration"] <= MAX_DUR):
            dropped["duration"] += 1
            continue
        c["queries"] = sorted(c["queries"])
        c["kind_guess"] = classify(c["title"], c["channel"])
        c["score"] = round(score(c), 2)
        kept.append(c)

    kept.sort(key=lambda c: (-c["score"], -c["views"]))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "candidates.json").write_text(json.dumps(kept, indent=2, ensure_ascii=False), encoding="utf-8")

    with open(OUT / "candidates.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rank", "video_id", "score", "duration_s", "views", "kind_guess", "channel", "title", "queries"])
        for i, c in enumerate(kept, 1):
            w.writerow([i, c["video_id"], c["score"], int(c["duration"]), c["views"],
                        c["kind_guess"], c["channel"], c["title"], ",".join(c["queries"])])

    print(f"\ncandidates kept: {len(kept)}  | dropped: {dropped}")
    from collections import Counter
    print("kinds:", dict(Counter(c["kind_guess"] for c in kept).most_common()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
