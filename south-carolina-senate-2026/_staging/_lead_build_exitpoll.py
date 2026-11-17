#!/usr/bin/env python3
"""Turn the mirrored CNN exit-poll table into a clean CSV.

Input : _staging/mirrors/tables/59_1.csv
Output: 09_sources/exit_poll_2026.csv

The source table uses single-cell rows as group headings ("Ideology", "Party", …). This script
carries those headings down onto the following subgroup rows, so the output is tidy without
losing the grouping.

Run: python _staging/_lead_build_exitpoll.py
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "mirrors", "tables", "59_1.csv")
DST = os.path.join(ROOT, "09_sources", "exit_poll_2026.csv")

GROUPS = {"Ideology", "Party", "Donald Trump job approval", "2024 presidential vote", "Gender",
          "Income", "Race/ethnicity", "White born-again or evangelical Christian?", "Race by gender",
          "Age", "Area type", "Education", "Education by race",
          "Education by gender and race", "Voters of color", "Educational attainment"}


def fix(s):
    s = s.replace("\ufffd", "-").replace("\u2013", "-").replace("\u2014", "-")
    return s.strip()


def main():
    rows = list(csv.reader(open(SRC, encoding="utf-8")))
    out = []
    group = "unknown"
    for r in rows[1:]:
        if not r or not any(c.strip() for c in r):
            continue
        cells = [fix(c) for c in r]
        if len([c for c in cells if c]) == 1:
            if cells[0] in GROUPS:
                group = cells[0]
            continue
        if len(cells) < 4:
            cells += [""] * (4 - len(cells))
        subgroup, a, g, share = cells[0], cells[1], cells[2], cells[3]
        if subgroup in ("Demographic subgroup",) or not subgroup:
            continue
        out.append([group, subgroup, a or "unknown", g or "unknown", share or "unknown"])

    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with open(DST, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["subgroup_group", "subgroup", "andrews_pct", "graham_pct",
                    "pct_of_total_vote"])
        w.writerows(out)
    print(f"{DST}: {len(out)} subgroups, {len({r[0] for r in out})} groups")
    for r in out[:4]:
        print("  ", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
