#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix two catalogue errors before any visual/audio processing.

  1. **Candidate attribution** — discovery slugs were built from search-result
     titles, so a Talarico campaign video called "…SHUTS DOWN Ken Paxton…" became
     `BOTH_*`. Ownership comes from the channel, so official campaign uploads are
     re-attributed and their slug prefix rewritten.
  2. **Kind attribution** — the archive's central claim is that no debate took
     place, so a clip titled "Talarico CHALLENGES Paxton to 3 Debates" is recorded
     as `debate_challenge`, never `debate`.

Slugs otherwise stay as downloaded (venues in slug names are cosmetic); only the
prefix changes. Renames are two-phase (old → temp → new) so they cannot collide.
Legacy entries (the original 29) are untouched.

    python texas-senate-2026/_staging/vision/normalize_config.py --dry-run
    python texas-senate-2026/_staging/vision/normalize_config.py
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

VISION = Path(__file__).resolve().parent
RAW = VISION / "raw"
CONFIG = VISION / "videos.json"
ROOT = VISION.parents[0].parent

OFFICIAL_TAL = re.compile(r"^james talarico", re.I)
OFFICIAL_PAX = re.compile(r"^ken paxton", re.I)
CHALLENGE = re.compile(r"challeng|urges|call(s)? for|demand|agree(d)? to|refus|invit", re.I)
DEBATE = re.compile(r"\bdebate(s)?\b", re.I)
CAND_TOKEN = {"TALARICO": "TAL", "PAXTON": "PAX", "BOTH": "BOTH", "OTHER": "OTH"}


def legacy_ids():
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "show",
                              "HEAD:texas-senate-2026/_staging/vision/videos.json"],
                             capture_output=True, text=True, encoding="utf-8")
        if out.returncode == 0:
            return {v["video_id"] for v in json.loads(out.stdout)}
    except Exception:
        pass
    return set()


def load_info(slug, vid):
    p = RAW / ("%s_%s.info.json" % (slug, vid))
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    legacy = legacy_ids()
    entries = []
    changes = []

    for v in cfg:
        e = dict(v)
        e["_old"] = v["slug"]
        e["_legacy"] = v["video_id"] in legacy
        if not e["_legacy"]:
            info = load_info(v["slug"], v["video_id"])
            channel = (v.get("channel") or info.get("channel") or "").strip()
            title = info.get("title") or v.get("title") or ""

            # candidate: official channel always wins; otherwise keep the selection
            # label, which was already derived from title mentions.
            cand = v["candidate_source"]
            if OFFICIAL_TAL.search(channel):
                cand = "TALARICO"
            elif OFFICIAL_PAX.search(channel):
                cand = "PAXTON"

            kind = v["kind"]
            if kind == "debate" and DEBATE.search(title) and CHALLENGE.search(
                    title + " " + (info.get("description") or "")):
                kind = "debate_challenge"

            if cand != v["candidate_source"]:
                parts = e["_old"].split("_", 1)
                new_slug = "%s_%s" % (CAND_TOKEN[cand], parts[1])
                changes.append((e, new_slug))
            e["candidate_source"] = cand
            e["kind"] = kind
            e["title"] = title or v["title"]
            e["channel"] = channel or v["channel"]
        entries.append(e)

    # keep target slugs unique against everything that is not itself being renamed
    taken = {e["_old"] for e in entries}
    for e, target in changes:
        taken.discard(e["_old"])
    final_map = {}
    for e, target in changes:
        m = re.match(r"^(.*?)(\d+)$", target)
        stem, n = (m.group(1), int(m.group(2)) + 1) if m else (target, 2)
        slug = target
        while slug in taken:
            slug = "%s%d" % (stem, n)
            n += 1
        taken.add(slug)
        final_map[e["video_id"]] = slug
        e["slug"] = slug

    print("entries: %d | legacy: %d | candidate/kind changes: %d"
          % (len(entries), len(legacy), len(changes)))
    for e, _t in changes[:50]:
        print("  %-34s -> %-30s %s" % (e["_old"], e["slug"],
                                       "%s/%s" % (e["candidate_source"], e["kind"])))
    if args.dry_run:
        return 0

    # two-phase rename: <old>_<id>.* -> __tmp_<id>.* -> <new>_<id>.*
    for e, _t in changes:
        vid, old = e["video_id"], e["_old"]
        for p in RAW.glob("%s_%s.*" % (old, vid)):
            suffix = p.name.replace("%s_%s." % (old, vid), "", 1)
            p.rename(RAW / ("__tmp_%s.%s" % (vid, suffix)))
        e["file"] = "%s_%s.mp4" % (e["slug"], vid)
    for e, _t in changes:
        vid = e["video_id"]
        for p in RAW.glob("__tmp_%s.*" % vid):
            suffix = p.name.replace("__tmp_%s." % vid, "", 1)
            p.rename(RAW / ("%s_%s.%s" % (e["slug"], vid, suffix)))

    out = []
    for e in entries:
        if not (RAW / e["file"]).exists() and not list(RAW.glob("%s_*.mp4" % e["slug"])):
            continue
        out.append({k: e[k] for k in ("slug", "file", "video_id", "candidate_source", "kind",
                                      "title", "channel", "upload_date", "duration")})
    CONFIG.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print("config rewritten: %d entries" % len(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
