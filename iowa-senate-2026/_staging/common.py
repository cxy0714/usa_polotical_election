# -*- coding: utf-8 -*-
"""Shared helpers: source keys, CSV writing, paths."""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(HERE)
with open(os.path.join(HERE, "srckey.json"), encoding="utf-8") as f:
    KEY = json.load(f)
URL = {}
for r in csv.DictReader(open(os.path.join(CASE, "09_sources", "sources.csv"), encoding="utf-8")):
    URL[r["source_id"]] = r["url"]


def S(*keys):
    """Return the single SRC-id|url pair required by the contract (first key wins)."""
    sid = KEY[keys[0]]
    return "%s|%s" % (sid, URL[sid])


def S1(k):
    return S(k)


def write(rel, header, rows):
    path = os.path.join(CASE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            assert len(r) == len(header), (rel, len(r), len(header), r[:2])
            for c in r:
                assert str(c).strip() != "", (rel, r[:2])
            w.writerow(r)
    print("wrote %-52s %3d rows" % (rel, len(rows)))
