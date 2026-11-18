# -*- coding: utf-8 -*-
"""Strip HTML/PDF noise from mirrors into readable text files under _staging/text/."""
import glob
import os
import re
from html import unescape

HERE = os.path.dirname(os.path.abspath(__file__))
MIR = os.path.join(HERE, "mirrors")
OUT = os.path.join(HERE, "text")
os.makedirs(OUT, exist_ok=True)

TAG = re.compile(r"<(script|style|noscript|svg)[^>]*>.*?</\1>", re.S | re.I)
ANY = re.compile(r"<[^>]+>")


def clean(raw):
    t = raw.decode("utf-8", "replace")
    t = TAG.sub(" ", t)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"<(br|/p|/div|/li|/h[1-6]|/tr)[^>]*>", "\n", t, flags=re.I)
    t = ANY.sub(" ", t)
    t = unescape(t)
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()


n = 0
for p in sorted(glob.glob(os.path.join(MIR, "*.html"))):
    base = os.path.basename(p)
    raw = open(p, "rb").read()
    txt = clean(raw)
    with open(os.path.join(OUT, base + ".txt"), "w", encoding="utf-8") as f:
        f.write(txt[:400000])
    n += 1
print("text files:", n)
