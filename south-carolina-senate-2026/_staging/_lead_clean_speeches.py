#!/usr/bin/env python3
"""Normalise the recovered speech CSVs: strip stray wrapping quotes, check vocabularies.

The stream that produced these files quoted every value, so cells arrived as `"ANDREWS"` rather
than `ANDREWS`, which would fail the validator's controlled-vocabulary check. This pass strips a
single wrapping quote pair per cell and reports the resulting value sets so the Lead can see
whether the controlled vocabularies are actually respected.

Run: python _staging/_lead_clean_speeches.py
"""
import csv
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FILES = [os.path.join(ROOT, "03_speeches", "speech_archive.csv"),
         os.path.join(ROOT, "03_speeches", "speech_video_index.csv")]

Q = chr(34)

# Only controlled-vocabulary fields get their stray quotes stripped. Quote-bearing prose lives in
# columns such as `major_quotes`, where a leading quote is part of the quotation itself.
VOCAB_FIELDS = {"candidate_id", "verification_status", "completeness", "transcript_available",
                "source_tier", "source_type", "event_status", "campaign_phase", "state_region",
                "opponent_reference", "sponsor_type", "coverage_type", "copyright_status",
                "vacancy_context", "winner", "mentions_opponent", "position_changed", "issue"}


def unwrap(v):
    return v.strip()


def clean_vocab(v):
    return v.strip().strip(Q).strip()


def main():
    for path in FILES:
        if not os.path.exists(path):
            print(f"missing {path}")
            continue
        rows = list(csv.reader(open(path, encoding="utf-8-sig")))
        header = rows[0]
        idx0 = {name: i for i, name in enumerate(header)}
        body = []
        for r in rows[1:]:
            if not r:
                continue
            cells = [unwrap(c) for c in r]
            for name, i in idx0.items():
                if name in VOCAB_FIELDS and i < len(cells):
                    cells[i] = clean_vocab(cells[i])
            body.append(cells)
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
            w.writerow(header)
            w.writerows(body)
        wide = {len(r) for r in body}
        print(f"{os.path.basename(path)}: {len(body)} rows, widths {wide}")
        idx = {name: i for i, name in enumerate(header)}
        for field in ("candidate_id", "verification_status", "completeness",
                      "transcript_available"):
            if field in idx:
                c = Counter(r[idx[field]] for r in body)
                print(f"  {field}: {dict(c)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
