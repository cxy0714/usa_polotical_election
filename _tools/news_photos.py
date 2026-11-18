#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Harvest credited news photographs from the archived article HTML.

For each case, scan `_staging/mirrors/*.html`, pull `<figure>` blocks whose
`<figcaption>` (or image alt text) names a candidate, and append a link-only row to
`04_visual_archive/image_archive.csv`. Nothing is downloaded: national and regional
news photography is almost always all-rights-reserved, so the archive records the
article URL, the caption and the credit line and explicitly stores no local file.

    python _tools/news_photos.py <case> [<case> ...] [--dry-run]

Rows are deduplicated by (article URL, caption). The original image URL is recorded
when the page exposes an absolute one; otherwise it is `unknown` with the reason.
"""
import argparse
import csv
import html
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]

HEADER = ["image_id", "candidate_id", "image_date", "event_id", "event_category", "source_name",
          "source_url", "original_image_url", "photographer", "copyright_status", "license",
          "local_filename", "image_resolution", "framing", "camera_angle", "image_quality",
          "face_visibility", "body_visibility", "clothing_notes", "notes", "verification_status"]

FIG_RE = re.compile(r"<figure\b[^>]*>(.*?)</figure>", re.S | re.I)
IMG_RE = re.compile(r"<img\b[^>]*>", re.S | re.I)
CAP_RE = re.compile(r"<figcaption\b[^>]*>(.*?)</figcaption>", re.S | re.I)
SRC_RE = re.compile(r"""\bsrc\s*=\s*["']([^"']+)["']""", re.I)
ALT_RE = re.compile(r"""\balt\s*=\s*["']([^"']*)["']""", re.I)
CREDIT_RE = re.compile(r"(photo|photograph|image|credit)\s*(by|:)?\s*([A-Z][^.|]{2,60})", re.I)
TAG_RE = re.compile(r"<[^>]+>")

CATEGORY = [
    ("debate", r"\bdebate\b"),
    ("rally", r"\brally|rallies\b"),
    ("town_hall", r"town hall"),
    ("interview", r"interview|one-on-one"),
    ("victory", r"victory|wins|winning|elected|projected"),
    ("concession", r"concede|concession"),
    ("primary", r"primary|nominee|nomination"),
    ("fundraiser", r"fundrais|donor"),
    ("advertising", r"ad\b|advert"),
    ("senate_floor", r"senate floor|hearing|committee"),
]

OUTLETS = {
    "apnews.com": "AP", "cbsnews.com": "CBS News", "cnn.com": "CNN", "nytimes.com": "The New York Times",
    "washingtonpost.com": "The Washington Post", "politico.com": "Politico", "axios.com": "Axios",
    "nbcnews.com": "NBC News", "abcnews.go.com": "ABC News", "reuters.com": "Reuters",
    "theguardian.com": "The Guardian", "usatoday.com": "USA Today", "npr.org": "NPR",
    "ajc.com": "The Atlanta Journal-Constitution", "detroitnews.com": "The Detroit News",
    "freep.com": "Detroit Free Press", "bridgemi.com": "Bridge Michigan", "mlive.com": "MLive",
    "adn.com": "Anchorage Daily News", "alaskabeacon.com": "Alaska Beacon", "alaskapublic.org": "Alaska Public Media",
    "desmoinesregister.com": "Des Moines Register", "iowacapitaldispatch.com": "Iowa Capital Dispatch",
    "kcrg.com": "KCRG", "cleveland.com": "cleveland.com", "dispatch.com": "The Columbus Dispatch",
    "cincinnati.com": "The Cincinnati Enquirer", "ideastream.org": "Ideastream", "wosu.org": "WOSU",
    "latimes.com": "Los Angeles Times", "dailynews.com": "Los Angeles Daily News",
    "calmatters.org": "CalMatters", "laist.com": "LAist", "kcrw.com": "KCRW",
    "sos.ohio.gov": "Ohio Secretary of State", "ohiosos.gov": "Ohio Secretary of State",
}


def clean(s):
    s = html.unescape(TAG_RE.sub(" ", s))
    return re.sub(r"\s+", " ", s).strip()


def outlet(url):
    host = urlparse(url).netloc.lower().replace("www.", "")
    for k, v in OUTLETS.items():
        if host.endswith(k):
            return v
    return host or "unknown"


def article_date(url):
    m = re.search(r"/(20\d\d)/(\d\d)/(\d\d)/", url)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.search(r"/(20\d\d)-(\d\d)-(\d\d)", url)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return "unknown"


def category_of(text):
    low = text.lower()
    for name, pat in CATEGORY:
        if re.search(pat, low):
            return name
    return "unknown"


def load_fetch_log(case):
    p = ROOT / case / "_staging" / "fetch_log.csv"
    out = []
    if not p.exists():
        return out
    with open(p, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if (r.get("http_status") or "") != "200":
                continue
            saved = (r.get("saved_file") or "").replace("\\", "/").lstrip("./")
            # fetch_log paths vary by case: case-relative, root-relative or _staging-relative.
            for cand in (ROOT / saved, ROOT / case / saved, ROOT / case / "_staging" / saved):
                if cand.exists():
                    out.append((r["url"], cand))
                    break
    return out


def harvest(case, dry=False):
    meta = json.load(open(ROOT / case / "_staging" / "case_meta.json", encoding="utf-8"))
    cands = meta.get("candidates") or []
    names = {c["id"]: [c["name"], c["name"].split()[-1]] for c in cands}
    arch = ROOT / case / "04_visual_archive"
    csv_path = arch / "image_archive.csv"
    if not csv_path.exists():
        print("no image_archive.csv in", case)
        return 0
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    existing = {(r["source_url"], clean(r["notes"]).split("|")[0][:80]) for r in rows}
    counters = {}
    prefixes = {}
    for r in rows:
        m = re.match(r"([A-Z]+)-IMG-(\d+)", r["image_id"])
        if not m:
            continue
        pref = m.group(1)
        counters[pref] = max(counters.get(pref, 0), int(m.group(2)))
        prefixes.setdefault(r["candidate_id"], {}).setdefault(pref, 0)
        prefixes[r["candidate_id"]][pref] += 1

    def prefix_for(cid):
        best = prefixes.get(cid) or {}
        if best:
            return max(best.items(), key=lambda kv: kv[1])[0]
        return cid[:3]

    added = []

    def consider(url, caption, alt, src):
        caption = clean(caption)
        if not (25 <= len(caption) <= 320):
            return
        if not re.search(r"\b(speaks?|speaking|talks?|talking|addresses?|addressing|rally|rallies|"
                         r"debate|campaign\w*|greets?|attends?|holds?|holding|stands?|walks?|"
                         r"gestures?|smiles?|listens?|during|on stage|at the podium|photo|"
                         r"left|right|appears|arrives?)\b", caption, re.I):
            return
        if re.search(r"review of records|according to|said in a statement|records showed", caption, re.I):
            return
        if re.search(r"\b(logo|map|chart|graph|screenshot|screen shot|illustration|icon|ballot)\b", caption, re.I):
            return
        low = (caption + " " + alt).lower()
        hit, hit_pos = None, 10 ** 6
        for cid, toks in names.items():
            for t in toks:
                pos = low.find(t.lower())
                if pos >= 0 and pos < hit_pos:
                    hit, hit_pos = cid, pos
        if not hit:
            return
        key = (url, caption[:80])
        if key in existing:
            return
        existing.add(key)
        photo_url = "unknown"
        if src and not src.startswith("data:"):
            photo_url = urljoin(url, src)
        credit = "unknown"
        cm = CREDIT_RE.search(caption)
        if cm:
            credit = clean(cm.group(0))
        pref = prefix_for(hit)
        counters[pref] = counters.get(pref, 0) + 1
        added.append({
            "image_id": f"{pref}-IMG-{counters[pref]:04d}",
            "candidate_id": hit,
            "image_date": article_date(url),
            "event_id": "unknown",
            "event_category": category_of(caption),
            "source_name": outlet(url),
            "source_url": url,
            "original_image_url": photo_url if photo_url != "unknown" else
                                  "unknown (page exposes caption/credit only; no stable file URL)",
            "photographer": credit,
            "copyright_status": "all_rights_reserved_link_only",
            "license": "all rights reserved - link and credit only",
            "local_filename": "unknown",
            "image_resolution": "unknown",
            "framing": "unknown",
            "camera_angle": "unknown",
            "image_quality": "unknown",
            "face_visibility": "unknown",
            "body_visibility": "unknown",
            "clothing_notes": "unknown",
            "notes": caption + " | Recorded from the outlet's caption/credit line; the image itself was NOT copied or read.",
            "verification_status": "partially verified",
        })

    for url, path in load_fetch_log(case):
        host = urlparse(url).netloc.lower()
        if re.search(r"wikipedia|wikimedia|archive\.org|fandom|facebook|twitter|x\.com|youtube", host):
            continue
        if not path.exists() or path.suffix.lower() not in (".html", ".htm"):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for block in FIG_RE.findall(text):
            imgs = IMG_RE.findall(block)
            caps = CAP_RE.findall(block)
            cap = clean(caps[0]) if caps else ""
            alt, src = "", ""
            if imgs:
                am = ALT_RE.search(imgs[0])
                sm = SRC_RE.search(imgs[0])
                alt = am.group(1) if am else ""
                src = sm.group(1) if sm else ""
            else:
                sm = SRC_RE.search(block)
                src = sm.group(1) if sm else ""
            consider(url, cap or alt, alt, src)
        # Fallback: some outlets ship no <figure>, but put a full caption in alt text.
        for tag in IMG_RE.findall(text):
            am = ALT_RE.search(tag)
            sm = SRC_RE.search(tag)
            if not am or not sm:
                continue
            alt = am.group(1)
            if alt.startswith("http"):
                continue
            consider(url, alt, alt, sm.group(1))
    print(f"{case}: +{len(added)} news-photo rows (from {sum(1 for _ in load_fetch_log(case))} archived pages)")
    for r in added[:6]:
        print(f"   {r['image_id']} {r['image_date']} {r['source_name']}: {r['notes'][:100]}")
    if dry or not added:
        return len(added)
    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, lineterminator="\n")
        for r in added:
            w.writerow(r)
    return len(added)


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("cases", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    for c in a.cases:
        harvest(c, a.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
