# -*- coding: utf-8 -*-
"""Keyword sweep over extracted text; prints compact hit snippets."""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TXT = os.path.join(HERE, "text")
KEYS = sys.argv[1:] or ["State Fair", "steak fry", "victory", "concession", "watch party",
                        "ethanol", "E15", "farm bill", "Medicaid", "SNAP", "abortion", "six-week",
                        "wheelchair", "disability", "ADA", "county party", "central committee"]

files = sorted(glob.glob(os.path.join(TXT, "*.txt")))
for k in KEYS:
    print("######", k)
    n = 0
    for f in files:
        t = open(f, encoding="utf-8", errors="replace").read()
        low = t.lower()
        i = low.find(k.lower())
        if i < 0:
            continue
        if "probe_01" in f or "probe_02" in f:
            continue
        n += 1
        if n > 8:
            break
        snip = re.sub(r"\s+", " ", t[max(0, i - 160):i + 260])
        print("  %-46s %s" % (os.path.basename(f)[:46], snip[:400]))
    if n == 0:
        print("  (no hits)")
