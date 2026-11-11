#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Select the download set from discovery/candidates.json under explicit quotas.

The archive does not need 600 clips; it needs coverage of *distinct events* across
both candidates, without letting one outlet or one rally monopolise the corpus.
Selection is therefore quota-driven and auditable:

  * hard filters   — duration window, noise channels, >2 h streams only if official
  * channel cap    — at most --per-channel videos from one channel
  * kind floors    — every speech/news kind gets at least N slots when available
  * duration budget— the selected corpus must stay under --hours of footage
  * dedupe         — near-identical titles from the same channel collapse to one

Writes discovery/selected.json + discovery/selection_report.csv.
"""
import argparse
import csv
import difflib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

VISION = Path(__file__).resolve().parent
DISC = VISION / "discovery"

# Minimum slots per kind, filled before pure score ranking.
FLOORS = {
    "victory_speech": 8, "concession_speech": 6, "convention_speech": 4,
    "town_hall": 6, "debate": 6, "interview": 6, "ad": 5,
    "rally_speech": 40, "tour_launch": 6, "final_rally": 4, "news_package": 25,
}
OFFICIAL = re.compile(r"james talarico|ken paxton", re.I)


def norm_title(t):
    t = re.sub(r"[^a-z0-9 ]+", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=20.0)
    ap.add_argument("--per-channel", type=int, default=9)
    ap.add_argument("--max-per-video", type=int, default=7200)
    args = ap.parse_args()

    cands = json.loads((DISC / "candidates.json").read_text(encoding="utf-8"))
    kept, reasons = [], Counter()
    seen_titles = defaultdict(list)

    for c in cands:
        d = int(c["duration"])
        official = bool(OFFICIAL.search(c["channel"]))
        if d < 25:
            reasons["too_short"] += 1
            continue
        if d > args.max_per_video and not official:
            reasons["too_long"] += 1
            continue
        nt = norm_title(c["title"])
        dup = any(difflib.SequenceMatcher(None, nt, prev).ratio() > 0.88
                  for prev in seen_titles[c["channel"]])
        if dup:
            reasons["near_duplicate_title"] += 1
            continue
        seen_titles[c["channel"]].append(nt)
        kept.append(c)

    # quotas: floors first (score order), then score order under budget
    by_kind = defaultdict(list)
    for c in kept:
        by_kind[c["kind_guess"]].append(c)
    for lst in by_kind.values():
        lst.sort(key=lambda c: (-c["score"], -c["views"]))

    chosen, chosen_ids = [], set()
    chan_count = Counter()

    def add(c, why):
        if c["video_id"] in chosen_ids:
            return False
        if chan_count[c["channel"]] >= args.per_channel:
            return False
        chosen.append(dict(c, select_reason=why))
        chosen_ids.add(c["video_id"])
        chan_count[c["channel"]] += 1
        return True

    for kind, floor in FLOORS.items():
        for c in by_kind.get(kind, []):
            if sum(1 for x in chosen if x["kind_guess"] == kind) >= floor:
                break
            add(c, f"floor:{kind}")

    for c in sorted(kept, key=lambda c: (-c["score"], -c["views"])):
        add(c, "score")

    # trim to the duration budget; keep floors untouched, drop the lowest-scored extras
    budget = args.hours * 3600
    total = sum(int(c["duration"]) for c in chosen)
    if total > budget:
        extras = [c for c in chosen if not c["select_reason"].startswith("floor:")]
        extras.sort(key=lambda c: (c["score"], c["views"]))
        dropped = set()
        for c in extras:
            if total <= budget:
                break
            dropped.add(c["video_id"])
            total -= int(c["duration"])
        chosen = [c for c in chosen if c["video_id"] not in dropped]
        reasons["budget_trimmed"] = len(dropped)

    chosen.sort(key=lambda c: (-c["score"], -c["views"]))
    for i, c in enumerate(chosen, 1):
        c["rank"] = i

    (DISC / "selected.json").write_text(json.dumps(chosen, indent=2, ensure_ascii=False), encoding="utf-8")
    with open(DISC / "selection_report.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rank", "video_id", "score", "duration_s", "kind", "channel", "title", "reason"])
        for c in chosen:
            w.writerow([c["rank"], c["video_id"], c["score"], int(c["duration"]),
                        c["kind_guess"], c["channel"], c["title"], c["select_reason"]])

    hours = sum(int(c["duration"]) for c in chosen) / 3600
    print(f"selected {len(chosen)} videos, {hours:.1f} h of footage"
          f"  | dropped: {dict(reasons)}")
    print("kinds:", dict(Counter(c["kind_guess"] for c in chosen).most_common()))
    print("channels:", len({c["channel"] for c in chosen}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
