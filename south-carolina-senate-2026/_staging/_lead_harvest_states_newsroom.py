#!/usr/bin/env python
"""Harvest candidate photographs from SC Daily Gazette articles (States Newsroom, CC BY-ND 4.0).

States Newsroom outlets publish their own photography under CC BY-ND 4.0: reuse is allowed with
attribution, derivatives are not, so files are stored unmodified and every row records the credit line
that appears under the photograph.

Writes a staging CSV for review; nothing is merged into `04_visual_archive/` by this script.
"""
import csv
import os
import re
import sys
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; archive-research/1.0)"
SEARCH = {
    "ANDREWS": ["https://scdailygazette.com/?s=Annie+Andrews"],
    "GRAHAM": ["https://scdailygazette.com/?s=Darline+Graham", "https://scdailygazette.com/?s=Graham"],
}
OUT = "_staging/images_states_newsroom.csv"
HOST_OK = re.compile(r"^https://scdailygazette\.com/", re.I)


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def article_links(html):
    links = set()
    for m in re.finditer(r'href="(https://scdailygazette\.com/20\d\d/\d\d/[^"#?]+)"', html):
        links.add(m.group(1))
    return sorted(links)


def pick_image(html, base):
    og = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if og:
        return urllib.parse.urljoin(base, og.group(1))
    for m in re.finditer(r'<img[^>]+src=["\']([^"\']*wp-content/uploads/20\d\d/\d\d/[^"\']+\.(?:jpe?g|png))', html, re.I):
        return urllib.parse.urljoin(base, m.group(1))
    return ""


def caption_near(html, img_url):
    tail = img_url.rsplit("/", 1)[-1].split("?")[0]
    idx = html.find(tail)
    if idx < 0:
        return ""
    window = html[idx:idx + 1200]
    cap = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", window, re.S | re.I)
    if cap:
        txt = re.sub(r"<[^>]+>", " ", cap.group(1))
        return re.sub(r"\s+", " ", txt).strip()[:300]
    return ""


def licence(html):
    hits = sorted({m.group(0).strip() for m in re.finditer(
        r"CC BY[- ]?ND[- ]?\d\.\d|Creative Commons[^<\"]{0,40}|all rights reserved", html, re.I)})
    return "; ".join(hits)[:160]


def main():
    rows = []
    for cand, searches in SEARCH.items():
        links = set()
        for s in searches:
            try:
                links.update(article_links(fetch(s)))
            except Exception as e:
                print(f"  search failed {s}: {e}")
        keep = [u for u in sorted(links)
                if (cand == "ANDREWS" and "andrews" in u.lower())
                or (cand == "GRAHAM" and ("graham" in u.lower()))]
        print(f"{cand}: {len(links)} article links, {len(keep)} matching the candidate")
        for url in keep[:14]:
            try:
                html = fetch(url)
            except Exception as e:
                print(f"   skip {url}: {e}")
                continue
            img = pick_image(html, url)
            if not img or not HOST_OK.match(img):
                continue
            title = re.search(r"<title>(.*?)</title>", html, re.S)
            rows.append({
                "candidate_id": cand,
                "article_url": url,
                "article_title": re.sub(r"\s+", " ", title.group(1)).strip()[:160] if title else "",
                "image_url": img,
                "caption": caption_near(html, img),
                "licence_found": licence(html),
            })
            print(f"   {cand} {url.rsplit('/', 1)[-1][:60]:60s} -> {img.rsplit('/', 1)[-1][:50]}")
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else
                           ["candidate_id", "article_url", "article_title", "image_url", "caption",
                            "licence_found"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {OUT}: {len(rows)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
