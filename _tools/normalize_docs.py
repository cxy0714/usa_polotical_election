#!/usr/bin/env python3
"""Normalise batch-2 Markdown documents before the site build.

  * add the YAML front matter required by the case contract when it is missing
  * rewrite internal collection keys (`SRC f080`, `f080`) to public `SRC-####` ids when a
    case provides a key map (`_staging/srckey.json` or `_staging/source_key.json`)

Usage: python _tools/normalize_docs.py [case ...]
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH2 = ["michigan-senate-2026", "alaska-senate-2026", "iowa-senate-2026",
          "ohio-senate-2026", "georgia-senate-2026", "los-angeles-mayor-2026"]

FRONT = """---
title: "{title}"
title_zh: "{title}"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: "See research_gaps.md for what is thin in this case."
---
"""


def keymap(case_dir):
    for name in ("srckey.json", "source_key.json", "source_map.json"):
        p = os.path.join(case_dir, "_staging", name)
        if os.path.exists(p):
            try:
                return json.load(open(p, encoding="utf-8"))
            except Exception:
                return {}
    return {}


def main(argv):
    cases = argv[1:] or BATCH2
    for case in cases:
        d = os.path.join(ROOT, case)
        if not os.path.isdir(d):
            continue
        km = keymap(d)
        added, fixed = 0, 0
        for base, dirs, files in os.walk(d):
            dirs[:] = [x for x in dirs if x not in ("site", "_staging", "mirrors")]
            for name in files:
                if not name.endswith(".md"):
                    continue
                p = os.path.join(base, name)
                text = open(p, encoding="utf-8-sig").read()
                orig = text
                if km:
                    def sub(m):
                        nonlocal fixed
                        key = m.group(2)
                        sid = km.get(key)
                        if not sid:
                            return m.group(0)
                        fixed += 1
                        return f"SRC-{sid.split('-')[1]}" if m.group(1).upper().startswith("SRC") else sid
                    text = re.sub(r"(SRC\s*)?\b(f\d{3})\b", sub, text)
                if not text.startswith("---"):
                    title = name[:-3]
                    m = re.search(r"^#\s+(.+)$", text, re.M)
                    if m:
                        title = m.group(1).strip()
                    text = FRONT.format(title=title.replace('"', "'")) + "\n" + text
                    added += 1
                if text != orig:
                    with open(p, "w", encoding="utf-8", newline="\n") as f:
                        f.write(text)
        print(f"{case}: front matter added {added}, source keys rewritten {fixed} (map entries {len(km)})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
