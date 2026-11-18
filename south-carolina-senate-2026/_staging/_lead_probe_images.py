#!/usr/bin/env python
"""Probe non-Commons pages for candidate photographs (read-only).

Commons is effectively exhausted for these two: 88 files, of which the relevant ones are the 48 rows
already in the archive. This probe asks the places that actually published 2026 photographs:
official Senate sites, the campaign site, Congress.gov, and States Newsroom outlets like the SC Daily
Gazette, which release their own photography under CC BY-ND.

Prints, per page: HTTP status, the licence statement found on the page, and the image URLs that look
like photographs of a person (large, in the article body or an og:image tag).
"""
import json
import re
import sys
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; archive-research/1.0)"

PAGES = {
    "graham.senate.gov": "https://www.graham.senate.gov/",
    "graham.senate.gov/about": "https://www.graham.senate.gov/about",
    "senate.gov SC delegation": "https://www.senate.gov/states/SC/senators.htm",
    "congress.gov search": "https://www.congress.gov/search?q=%7B%22search%22%3A%22Darline+Graham%22%7D",
    "enwiki Annie Andrews": "https://en.wikipedia.org/wiki/Annie_Andrews",
    "enwiki Darline Graham": "https://en.wikipedia.org/wiki/Darline_Graham",
    "annieandrews.com": "https://www.annieandrews.com/",
    "annieandrews.com press": "https://www.annieandrews.com/press",
    "scdailygazette search graham": "https://scdailygazette.com/?s=Darline+Graham",
    "scdailygazette search andrews": "https://scdailygazette.com/?s=Annie+Andrews",
    "scdailygazette about": "https://scdailygazette.com/about/",
}

LICENCE_HINTS = re.compile(
    r"(CC BY[- ]?(?:ND|NC|SA)?[- ]?\d\.\d|Creative Commons[^<]{0,60}|public domain|"
    r"all rights reserved|States Newsroom)", re.I)


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "text/html,application/xhtml+xml"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace"), r.geturl()
    except Exception as e:
        return getattr(e, "code", "ERR"), "", url


def images(html, base):
    out = []
    for m in re.finditer(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', html, re.I):
        out.append(("og", m.group(1)))
    for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', html, re.I):
        tag = m.group(0)
        src = m.group(1)
        w = re.search(r'width=["\'](\d+)', tag)
        out.append((f"img{w.group(1) if w else '?'}", src))
    clean = []
    for kind, src in out:
        src = urllib.parse.urljoin(base, src)
        if re.search(r"\.(jpe?g|png|webp)(\?|$)", src, re.I) and "logo" not in src.lower() \
                and "icon" not in src.lower():
            clean.append((kind, src))
    seen, uniq = set(), []
    for kind, src in clean:
        if src not in seen:
            seen.add(src)
            uniq.append((kind, src))
    return uniq


def main():
    report = {}
    for label, url in PAGES.items():
        status, html, final = fetch(url)
        lic = sorted({m.group(1).strip() for m in LICENCE_HINTS.finditer(html)})[:5] if html else []
        found = images(html, final)[:12] if html else []
        report[label] = {"url": url, "status": status, "final": final,
                         "licence_hits": lic, "images": found}
        print(f"\n== {label} [{status}] {final[:90]}")
        if lic:
            print("   licence hints:", "; ".join(lic)[:200])
        for kind, src in found:
            print(f"   {kind:7s} {src[:130]}")
    json.dump(report, open("_staging/images_probe.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("\nwrote _staging/images_probe.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
