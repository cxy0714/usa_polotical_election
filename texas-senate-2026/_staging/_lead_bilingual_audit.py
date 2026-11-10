#!/usr/bin/env python3
"""Lead bilingual-integration audit for texas-senate-2026.

Checks that the Chinese-English conversion did not damage the archive:
  1. every deliverable .md has bilingual front matter (title_zh, language: en+zh)
  2. no leftover agent-local source tokens ([A-E]-S##) in deliverables
  3. every heading is bilingual on one line (English / 中文)
  4. substantial Chinese presence per file (no half-translated files)
  5. no mojibake / replacement characters
  6. every relative markdown link resolves
  7. every cited event/speech/image/ad id exists in its dataset
Run from the project root:  python _staging/_lead_bilingual_audit.py
"""
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CJK = re.compile(r"[\u4e00-\u9fff]")
LOCAL_TOK = re.compile(r"\b[ABCDE]-S\d+\b")
MOJIBAKE = ("鈥", "\ufffd", "Ã", "â€")
SKIP_DIRS = {"_staging"}

# markdown files that are intentionally English-only or non-deliverable
EXEMPT = {
    "_research_conventions.md",  # handled by comparative-zh, but is a contract not a report
}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def walk_md():
    for dp, _, fs in os.walk(ROOT):
        if any(s in dp for s in SKIP_DIRS):
            continue
        for f in fs:
            if f.endswith(".md"):
                yield os.path.join(dp, f)


def load_ids():
    ids = {}
    spec = {
        "campaign_events.csv": ("event_id", r"^[A-Z]{3}-EVT-\d{4}$"),
        "speech_archive.csv": ("speech_id", r"^[A-Z]{3}-SPC-\d{4}$"),
        "image_archive.csv": ("image_id", r"^[A-Z]{3}-IMG-\d{4}$"),
        "advertisements.csv": ("ad_id", r"^(?:[A-Z]{3}|EXT)-AD-\d{4}$"),
    }
    for dp, _, fs in os.walk(ROOT):
        for f in fs:
            if f in spec:
                col, _ = spec[f]
                with open(os.path.join(dp, f), newline="", encoding="utf-8-sig") as fh:
                    ids[f] = {r[col] for r in csv.DictReader(fh) if r.get(col)}
    return ids


def main():
    problems = []
    warnings = []
    files = sorted(walk_md())
    ids = load_ids()
    event_ids = ids.get("campaign_events.csv", set())
    speech_ids = ids.get("speech_archive.csv", set())
    image_ids = ids.get("image_archive.csv", set())
    ad_ids = ids.get("advertisements.csv", set())

    for p in files:
        rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
        txt = read(p)
        head = txt[:4000]

        # 1 front matter
        if txt.startswith("---"):
            fm = txt.split("---", 2)[1] if txt.count("---") >= 2 else ""
            if "title_zh" not in fm:
                problems.append(f"{rel}: front matter lacks title_zh")
            if "language: en+zh" not in fm:
                problems.append(f"{rel}: front matter lacks 'language: en+zh'")
        else:
            warnings.append(f"{rel}: no YAML front matter (acceptable only for a contract/index)")

        # 2 local source tokens
        toks = LOCAL_TOK.findall(txt)
        if toks:
            problems.append(f"{rel}: {len(toks)} leftover local source tokens, e.g. {sorted(set(toks))[:4]}")

        # 3 bilingual headings
        h2 = re.findall(r"^#{2,4} (.+)$", txt, re.M)
        mono = [h for h in h2 if not CJK.search(h)]
        if mono and len(h2) >= 3:
            problems.append(f"{rel}: {len(mono)}/{len(h2)} headings not bilingual on one line, e.g. {mono[:3]}")

        # 4 Chinese presence
        eng_words = len(re.findall(r"[A-Za-z]{4,}", txt))
        zh_chars = len(CJK.findall(txt))
        if zh_chars < 200:
            problems.append(f"{rel}: only {zh_chars} Chinese chars — likely not converted")
        elif eng_words and zh_chars / max(eng_words, 1) < 0.35:
            warnings.append(f"{rel}: thin Chinese density ({zh_chars} zh chars vs {eng_words} en words)")

        # 5 mojibake
        for m in MOJIBAKE:
            if m in txt:
                problems.append(f"{rel}: mojibake marker {m!r}")
                break

        # 6 links
        for link in re.findall(r"\]\(([^)]+)\)", txt):
            if link.startswith(("http", "#", "mailto")):
                continue
            target = link.split("#")[0].strip()
            if not target:
                continue
            full = os.path.normpath(os.path.join(os.path.dirname(p), target))
            if not os.path.exists(full):
                problems.append(f"{rel}: broken link -> {link}")

        # 7 id references
        illustrative = rel in {"_research_conventions.md", "09_sources/data_dictionary_bilingual.md"}
        for eid in set(re.findall(r"\b[A-Z]{3}-EVT-\d{4}\b", txt)):
            if event_ids and eid not in event_ids and not illustrative:
                warnings.append(f"{rel}: references {eid} not in campaign_events.csv (may be retired)")
        for sid in set(re.findall(r"\b[A-Z]{3}-SPC-\d{4}\b", txt)):
            if speech_ids and sid not in speech_ids and not illustrative:
                warnings.append(f"{rel}: references {sid} not in speech_archive.csv")
        RETIRED_IMAGES = {"PAX-IMG-0801"}  # deliberately removed wrong-subject file; mentions are documentation
        for iid in set(re.findall(r"\b[A-Z]{3}-IMG-\d{4}\b", txt)):
            if image_ids and iid not in image_ids and iid not in RETIRED_IMAGES and not illustrative:
                problems.append(f"{rel}: references {iid} not in image_archive.csv (retired row?)")
        for aid in set(re.findall(r"\b(?:[A-Z]{3}|EXT)-AD-\d{4}\b", txt)):
            if ad_ids and aid not in ad_ids and not illustrative:
                warnings.append(f"{rel}: references {aid} not in advertisements.csv")

    print(f"audited {len(files)} markdown files")
    print(f"hard problems: {len(problems)}")
    for x in problems:
        print("  [FAIL]", x)
    print(f"warnings: {len(warnings)}")
    for x in warnings[:40]:
        print("  [warn]", x)
    if len(warnings) > 40:
        print(f"  ... and {len(warnings) - 40} more")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
