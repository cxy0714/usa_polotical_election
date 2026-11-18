#!/usr/bin/env python3
"""Sanity-check the generated site for one case.

Usage: python _tools/case_site_check.py <case-slug>

Checks:
  * index.html exists and contains the race name and both candidate names
  * every data/<csv>.html page's <tr> count matches the CSV's row count (+1 header)
  * no literal "None", "nan", "{", "}" leaks in rendered pages
  * every local href/src resolves inside the case site or the case folder
"""
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rows(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.reader(f))


def main(argv):
    case = argv[1]
    d = os.path.join(ROOT, case)
    site = os.path.join(d, "site")
    problems = []
    with open(os.path.join(d, "_staging", "case_meta.json"), encoding="utf-8") as f:
        import json
        meta = json.load(f)
    home = open(os.path.join(site, "index.html"), encoding="utf-8").read()
    for needle in [meta["race_name"]] + [c["name"] for c in meta["candidates"]]:
        if needle not in home:
            problems.append(f"index.html missing {needle}")

    for base, _, files in os.walk(site):
        for name in files:
            if not name.endswith(".html"):
                continue
            p = os.path.join(base, name)
            text = open(p, encoding="utf-8").read()
            stripped = re.sub(r"<code>.*?</code>", "", text, flags=re.S)
            rel_page = os.path.relpath(p, site).replace(os.sep, "/")
            leak = re.search(r"\bnan\b|\{[a-z_]+\}", stripped)
            if rel_page.startswith("data/") and re.search(r">\s*None\s*<", stripped):
                leak = leak or True
            if leak:
                problems.append(f"{os.path.relpath(p, site)}: leaked template/None value")
            for href in re.findall(r'(?:href|src)="([^"#]+)"', text):
                if href.startswith(("http", "mailto", "data:")):
                    continue
                target = os.path.normpath(os.path.join(base, href))
                if not os.path.exists(target):
                    problems.append(f"{os.path.relpath(p, site)}: broken {href}")

    data_dir = os.path.join(site, "data")
    used = set()
    for base, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if x not in ("site", "_staging", "mirrors")]
        for name in sorted(files):
            if not name.endswith(".csv") or name == "sources.csv":
                continue
            base_name = name[:-4]
            page_name = base_name
            if page_name in used:
                page_name = os.path.basename(base) + "_" + base_name
            used.add(page_name)
            page = os.path.join(data_dir, page_name + ".html")
            if not os.path.exists(page):
                problems.append(f"missing data page for {name} (expected {page_name}.html)")
                continue
            csv_rows = max(0, len(rows(os.path.join(base, name))) - 1)
            tr = open(page, encoding="utf-8").read().count("<tr>")
            if tr != csv_rows + 1:
                problems.append(f"{name}: page has {tr} rows, CSV has {csv_rows} (+header)")

    print(f"{case}: {len(problems)} problems")
    for p in problems[:25]:
        print("  ", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
