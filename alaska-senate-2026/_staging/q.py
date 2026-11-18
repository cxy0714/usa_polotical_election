"""Grep the extracted mirror corpus with context. Usage: python _staging/q.py "regex" [context_chars]"""
import os, re, sys, glob

CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT = os.path.join(CASE, "_staging", "mirrors", "text")
pat = re.compile(sys.argv[1], re.I)
ctx = int(sys.argv[2]) if len(sys.argv) > 2 else 160
hits = 0
for p in sorted(glob.glob(os.path.join(TEXT, "*.txt"))):
    t = open(p, encoding="utf-8", errors="ignore").read()
    t = re.sub(r"\s+", " ", t)
    for m in pat.finditer(t):
        a, b = max(0, m.start() - ctx), min(len(t), m.end() + ctx)
        print("### %s" % os.path.basename(p)[:78])
        print("..." + t[a:b].strip() + "...")
        hits += 1
        if hits > 120:
            sys.exit(0)
