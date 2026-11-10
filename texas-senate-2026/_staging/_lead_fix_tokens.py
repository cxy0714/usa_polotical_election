#!/usr/bin/env python3
"""Remap leftover agent-local source tokens ([A-E]-S##) to global SRC-#### ids.

Agents that rewrote their bilingual files from their own working copies reintroduced
the pre-merge local tokens. This restores the master registry mapping without touching
anything else in the file.

Usage:
    python _staging/_lead_fix_tokens.py [--dry-run] [paths...]
With no paths it scans every deliverable .md under the project (excluding _staging).
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_PATH = os.path.join(ROOT, "_staging", "_lead_source_map.json")
TOKEN = re.compile(r"\b([ABCDE]-S\d+)\b")


def load_map():
    with open(MAP_PATH, encoding="utf-8") as f:
        return json.load(f)


def targets(argv):
    paths = [a for a in argv if not a.startswith("-")]
    if paths:
        return [p if os.path.isabs(p) else os.path.join(os.getcwd(), p) for p in paths]
    out = []
    for dp, _, fs in os.walk(ROOT):
        if "_staging" in dp:
            continue
        for f in fs:
            if f.endswith((".md", ".csv")):
                out.append(os.path.join(dp, f))
    return out


def main(argv):
    dry = "--dry-run" in argv
    mapping = load_map()
    known = set(mapping)
    total = 0
    unknown_all = {}
    changed_files = 0
    for p in targets(argv):
        with open(p, encoding="utf-8") as f:
            txt = f.read()
        found = TOKEN.findall(txt)
        if not found:
            continue
        unknown = sorted({t for t in found if t not in known})
        if unknown:
            unknown_all[os.path.relpath(p, ROOT)] = unknown
        def sub(m):
            tok = m.group(1)
            return mapping.get(tok, tok)
        new = TOKEN.sub(sub, txt)
        n = len(found)
        total += n
        changed_files += 1
        rel = os.path.relpath(p, ROOT)
        if dry:
            print(f"[dry] {rel}: would remap {n} tokens")
        else:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(new)
            print(f"[ok ] {rel}: remapped {n} tokens")
    print(f"\n{'would remap' if dry else 'remapped'} {total} tokens across {changed_files} files")
    if unknown_all:
        print(f"UNMAPPED tokens in {len(unknown_all)} files (need manual handling):")
        for k, v in unknown_all.items():
            print(f"  {k}: {v[:8]}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
