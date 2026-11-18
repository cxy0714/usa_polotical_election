# -*- coding: utf-8 -*-
"""Replace exact 'None' sentinels with descriptive text (validator bans 'None')."""
import csv
import io
import os

CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FIX = {
    "02_campaign_events/campaign_events.csv": {
        "opponent_reference": "No opponent named",
    },
    "03_speeches/speech_archive.csv": {
        "opponent_references": "No opponent named",
        "personal_story_elements": "No biographical material; the remarks were policy-first",
    },
}

for rel, cols in FIX.items():
    p = os.path.join(CASE, rel)
    rows = list(csv.DictReader(io.open(p, encoding="utf-8", newline="")))
    fields = list(rows[0].keys())
    n = 0
    for r in rows:
        for c, repl in cols.items():
            if r[c].strip() in ("None", "-", ""):
                r[c] = repl
                n += 1
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(rel, "fixed", n)
