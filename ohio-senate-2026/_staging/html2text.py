#!/usr/bin/env python3
"""Convert mirrored HTML/XML to plain text for grepping and quoting.

Writes _staging/text/<mirror-stem>.txt. Skips PDFs/binary. Idempotent.
"""
import glob
import html
import os
import re
import sys

MIR = "_staging/mirrors"
OUT = "_staging/text"
os.makedirs(OUT, exist_ok=True)

SCRIPT = re.compile(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>")
COMMENT = re.compile(r"(?s)<!--.*?-->")
TAG = re.compile(r"(?s)<[^>]+>")
BLOCK = re.compile(r"(?i)</?(p|div|br|li|tr|h[1-6]|section|article|td|th|blockquote)[^>]*>")


def to_text(raw):
    s = SCRIPT.sub(" ", raw)
    s = COMMENT.sub(" ", s)
    s = BLOCK.sub("\n", s)
    s = TAG.sub(" ", s)
    s = html.unescape(s)
    s = s.replace("\xa0", " ")
    lines = []
    for ln in s.split("\n"):
        ln = re.sub(r"[ \t\r\f\v]+", " ", ln).strip()
        if ln:
            lines.append(ln)
    return "\n".join(lines)


def main():
    files = sorted(glob.glob(os.path.join(MIR, "*.html"))) + \
        sorted(glob.glob(os.path.join(MIR, "*.xml"))) + \
        sorted(glob.glob(os.path.join(MIR, "*.json")))
    n = 0
    for f in files:
        stem = os.path.splitext(os.path.basename(f))[0]
        dst = os.path.join(OUT, stem + ".txt")
        try:
            raw = open(f, "rb").read().decode("utf-8", "replace")
        except Exception as e:
            print("skip", f, e)
            continue
        txt = to_text(raw) if f.endswith((".html", ".xml")) else raw
        with open(dst, "w", encoding="utf-8", newline="\n") as g:
            g.write(txt)
        n += 1
    print("wrote", n, "text files to", OUT)


if __name__ == "__main__":
    main()
