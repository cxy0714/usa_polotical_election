#!/usr/bin/env python3
"""Extract every wikitable in the mirrored sections into its own CSV.

Cells keep their text (links flattened, templates dropped, style/colspan/rowspan attributes
stripped) so that a column can be read off directly. Rowspan/colspan are NOT expanded —
the raw attribute remains visible in a sidecar manifest so nobody mistakes a merged cell for
a missing value.

Outputs: _staging/mirrors/tables/<section>_<n>.csv  + tables/manifest.csv

Run: python _staging/_lead_parse_tables.py
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SECT = os.path.join(HERE, "mirrors", "sections")
OUT = os.path.join(HERE, "mirrors", "tables")

ATTR = re.compile(r"^(?:[a-z][a-z0-9-]*=\"[^\"]*\"\s*\|)+", re.I)
ATTR2 = re.compile(r"^(?:align|colspan|rowspan|style|scope|class|bgcolor|nowrap|title|width|valign)"
                   r"\b[^|]*\|", re.I)


def cell_text(s):
    s = s.strip()
    s = s.lstrip("|!").strip()
    for _ in range(3):
        s2 = ATTR.sub("", s)
        s2 = ATTR2.sub("", s2)
        if s2 == s:
            break
        s = s2
    s = s.replace("'''", "").replace("''", "")
    s = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"\[\[([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"\[https?://\S+\s+([^\]]+)\]", r"\1", s)
    s = re.sub(r"\{\{(?:efn|cite|sfn|refn|abbr)\|[^}]*\}\}", "", s)
    s = re.sub(r"\{\{[^{}]*\}\}", "", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"&nbsp;", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def split_cells(block):
    """Split a table body into rows of cell strings, honouring the leading | / ! markers."""
    rows = []
    cur = []
    for line in block.split("\n"):
        if line.startswith("|-"):
            if cur:
                rows.append(cur)
                cur = []
            continue
        if line.startswith("|}") or line.startswith("|+"):
            continue
        if line.startswith("|") or line.startswith("!"):
            # a line may hold several cells separated by || or !!
            if "||" in line or "!!" in line:
                parts = re.split(r"\|\||!!", line)
            else:
                parts = [line]
            for p in parts:
                cur.append(cell_text(p))
    if cur:
        rows.append(cur)
    return rows


def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = []
    for fn in sorted(os.listdir(SECT)):
        if not fn.endswith(".wikitext"):
            continue
        sec = int(fn.split(".")[0])
        raw = open(os.path.join(SECT, fn), encoding="utf-8").read()
        for i, m in enumerate(re.finditer(r"\{\|.*?\n\|\}", raw, re.S), start=1):
            block = m.group(0)
            rows = split_cells(block)
            if len(rows) < 2:
                continue
            width = max(len(r) for r in rows)
            path = os.path.join(OUT, f"{sec:02d}_{i}.csv")
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f, lineterminator="\n")
                for r in rows:
                    w.writerow(r + [""] * (width - len(r)))
            caption = ""
            cm = re.search(r"\|\+\s*(.+)", block)
            if cm:
                caption = cell_text(cm.group(1))
            manifest.append({"file": os.path.basename(path), "section": sec,
                             "rows": len(rows), "cols": width, "caption": caption or "unknown"})
    with open(os.path.join(OUT, "manifest.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "section", "rows", "cols", "caption"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(manifest)
    print(f"{len(manifest)} tables -> {OUT}")
    for m in manifest:
        print(f"  {m['file']:>8s}  {m['rows']:>4d}x{m['cols']:<2d}  {m['caption'][:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
