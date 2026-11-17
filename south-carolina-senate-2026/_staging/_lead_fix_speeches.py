#!/usr/bin/env python3
"""Repair the malformed speech_archive.csv left by a failed stream.

The file was written with every field wrapped in a *doubled* quote (`""value""`), which makes it
invalid RFC-4180 despite looking quoted. Because each field boundary is marked by the literal
sequence `","`, the fields can be recovered losslessly: trim the outer doubled pair, then split on
that boundary. Internal commas survive, internal doubled quotes are un-doubled.

The script only rewrites the file if every data row recovers exactly the header's field count;
otherwise it writes a `.recovered.csv` next to it and exits non-zero so nothing is destroyed.

Run: python _staging/_lead_fix_speeches.py
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TARGET = os.path.join(ROOT, "03_speeches", "speech_archive.csv")

Q = chr(34)
BOUNDARY = Q + "," + Q
DOUBLE = Q + Q


def recover(line):
    s = line.rstrip("\r\n")
    if s.startswith(DOUBLE):
        s = s[2:]
    if s.endswith(DOUBLE):
        s = s[:-2]
    parts = s.split(BOUNDARY)
    return [p.replace(DOUBLE, Q) for p in parts]


def main():
    raw = open(TARGET, encoding="utf-8").read().split("\n")
    header = [h.strip() for h in raw[0].split(",")]
    rows = []
    failures = []
    for i, line in enumerate(raw[1:], start=2):
        if not line.strip():
            continue
        parts = recover(line)
        if len(parts) != len(header):
            failures.append((i, len(parts)))
            continue
        rows.append(parts)

    print(f"header fields: {len(header)}; recovered rows: {len(rows)}; failures: {len(failures)}")
    if failures:
        print("  first failures (line, fields):", failures[:5])

    out = os.path.join(ROOT, "03_speeches", "speech_archive.recovered.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {out}")

    if failures:
        return 1

    os.replace(out, TARGET)
    with open(TARGET, newline="", encoding="utf-8") as f:
        check = list(csv.reader(f))
    widths = {len(r) for r in check}
    print(f"replaced {TARGET}: {len(check) - 1} rows, widths {widths}")
    cands = {}
    for r in check[1:]:
        cands[r[1]] = cands.get(r[1], 0) + 1
    print("by candidate:", cands)
    return 0


if __name__ == "__main__":
    sys.exit(main())
