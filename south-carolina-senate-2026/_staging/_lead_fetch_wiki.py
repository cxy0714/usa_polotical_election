#!/usr/bin/env python3
"""Mirror the Wikipedia sources for Case Study 002 into small local files.

Why: conversation-level fetching of a 177 KB article is expensive and fragile. This
script pulls every section separately over urllib (with a User-Agent, which is what the
Wikimedia API requires), stores the raw wikitext, and writes three kinds of small local
artifact that downstream streams can read cheaply:

  _staging/mirrors/sections/NN.wikitext   raw wikitext, one file per section
  _staging/mirrors/sections/NN.txt        markup-stripped prose, one file per section
  _staging/mirrors/refs_urls.csv          every URL cited in the article, with its section
  _staging/mirrors/pages/<Name>.txt       stripped text of the three candidate articles

Run: python _staging/_lead_fetch_wiki.py [--force]
"""
import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MIR = os.path.join(ROOT, "_staging", "mirrors")
SEC_DIR = os.path.join(MIR, "sections")
PAGE_DIR = os.path.join(MIR, "pages")
UA = {"User-Agent": "SC-Senate-Archive/1.0 (academic research; python-urllib)"}

RACE = "2026_United_States_Senate_election_in_South_Carolina"
PAGES = ["Annie_Andrews", "Darline_Graham", "Lindsey_Graham"]


def get(url, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:                                    # noqa: BLE001
            last = e
            time.sleep(1.5 * (i + 1))
    raise last


def section_index(page):
    url = ("https://en.wikipedia.org/w/api.php?action=parse&prop=sections&format=json"
           f"&formatversion=2&page={urllib.parse.quote(page)}")
    data = json.loads(get(url))
    return data.get("parse", {}).get("sections", [])


def strip_wiki(t):
    """Reduce wikitext to readable prose. Deliberately lossy — the raw file is the source."""
    t = re.sub(r"<ref[^>/]*/>", "", t)
    t = re.sub(r"<ref[^>]*>.*?</ref>", "", t, flags=re.S)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    # tables -> keep only cell text, one row per line
    def tbl(m):
        body = m.group(0)
        rows = re.split(r"\n\|-", body)
        out = []
        for row in rows:
            cells = [c.strip() for c in re.split(r"\n[!|]", row)]
            cells = [re.sub(r"^\s*[!|]\s*", "", c) for c in cells]
            cells = [c for c in cells if c and not c.startswith("}")]
            if cells:
                out.append(" | ".join(cells))
        return "\n".join(out)
    t = re.sub(r"\{\|.*?\n\|\}", tbl, t, flags=re.S)
    t = re.sub(r"\{\{[Ee]lection box.*?\}\}", "", t, flags=re.S)
    t = re.sub(r"\{\{(?:efn|cite|sfn|refn)[^}]*\}\}", "", t)
    t = re.sub(r"\{\{[^{}]*\}\}", "", t)
    t = re.sub(r"\{\{[^{}]*\}\}", "", t)
    t = re.sub(r"\[\[File:[^\]]*\]\]", "", t, flags=re.I)
    t = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", t)
    t = re.sub(r"\[https?://\S+\s+([^\]]+)\]", r"\1", t)
    t = re.sub(r"\[https?://\S+\]", "", t)
    t = re.sub(r"'{2,}", "", t)
    t = re.sub(r"^=+\s*(.*?)\s*=+\s*$", r"\1", t, flags=re.M)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def main():
    force = "--force" in sys.argv
    os.makedirs(SEC_DIR, exist_ok=True)
    os.makedirs(PAGE_DIR, exist_ok=True)

    secs = section_index(RACE)
    print(f"{len(secs)} sections indexed")
    urls = []
    for s in secs:
        n = s["index"]
        raw_p = os.path.join(SEC_DIR, f"{int(n):02d}.wikitext")
        txt_p = os.path.join(SEC_DIR, f"{int(n):02d}.txt")
        if os.path.exists(raw_p) and not force:
            raw = open(raw_p, encoding="utf-8").read()
        else:
            url = f"https://en.wikipedia.org/w/index.php?title={RACE}&action=raw&section={n}"
            raw = get(url)
            with open(raw_p, "w", encoding="utf-8", newline="\n") as f:
                f.write(raw)
            time.sleep(0.4)
        if force or not os.path.exists(txt_p):
            with open(txt_p, "w", encoding="utf-8", newline="\n") as f:
                f.write(f"# [{s['number']}] {s['line']}\n\n" + strip_wiki(raw))
        for m in re.finditer(r"https?://[^\s\|\]}<>\"]+", raw):
            urls.append((n, s["line"], m.group(0).rstrip(".,;)")))
        print(f"  {int(n):02d} {s['line'][:60]:60s} {len(raw):>7d} bytes")

    with open(os.path.join(MIR, "refs_urls.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["section_index", "section_title", "url"])
        seen = set()
        for n, title, u in urls:
            if (u, n) in seen:
                continue
            seen.add((u, n))
            w.writerow([n, title, u])
    print(f"refs_urls.csv: {len(seen)} rows")

    for page in PAGES:
        raw_p = os.path.join(PAGE_DIR, f"{page}.wikitext")
        txt_p = os.path.join(PAGE_DIR, f"{page}.txt")
        if force or not os.path.exists(raw_p):
            url = f"https://en.wikipedia.org/w/index.php?title={page}&action=raw"
            raw = get(url)
            with open(raw_p, "w", encoding="utf-8", newline="\n") as f:
                f.write(raw)
            time.sleep(0.4)
        raw = open(raw_p, encoding="utf-8").read()
        with open(txt_p, "w", encoding="utf-8", newline="\n") as f:
            f.write(strip_wiki(raw))
        print(f"  page {page}: {len(raw)} bytes")

    print("done")


if __name__ == "__main__":
    main()
