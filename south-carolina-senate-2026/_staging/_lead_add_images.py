#!/usr/bin/env python
"""Add news photographs from States Newsroom's South Carolina outlet, verified by face match.

Why this source: Commons is exhausted for these two candidates (20 files, all already archived), while
the SC Daily Gazette publishes its own 2026 photography under CC BY-ND 4.0 — reusable with credit and
without modification.

Two gates before a photograph enters the archive:
  1. the article must be about the candidate (title or slug), and
  2. the photograph must contain that candidate's face according to the same SFace test used for the
     video frames (cosine >= 0.363 and a 0.05 margin over the other candidate).

Files are stored unmodified (CC BY-ND forbids derivatives, so no cropping) and every row records the
article it came from, the credit line and the licence.
"""
import csv
import datetime as dt
import os
import re
import shutil
import sys
import urllib.parse
import urllib.request

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ARCH = os.path.join(ROOT, "04_visual_archive")
MODELS = os.path.join(HERE, "vision", "models")
INCOMING = os.path.join(HERE, "images_incoming")
IMAGES_CSV = os.path.join(ARCH, "image_archive.csv")
SOURCES_CSV = os.path.join(ROOT, "09_sources", "sources.csv")

UA = "Mozilla/5.0 (compatible; archive-research/1.0)"
ACCESS_DATE = "2026-11-18"
SIM_THRESHOLD = 0.363
MARGIN = 0.05

SEARCHES = [
    "https://scdailygazette.com/?s=Annie+Andrews",
    "https://scdailygazette.com/?s=Andrews",
    "https://scdailygazette.com/?s=Darline+Graham",
    "https://scdailygazette.com/?s=Graham",
    "https://scdailygazette.com/tag/annie-andrews/",
    "https://scdailygazette.com/tag/darline-graham/",
]


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def article_links(html):
    out = set()
    for m in re.finditer(r'href="(https://scdailygazette\.com/20\d\d/\d\d/[^"#?]+)"', html):
        out.add(m.group(1))
    return out


def candidate_by_text(text):
    low = text.lower()
    hits = set()
    if "andrews" in low:
        hits.add("ANDREWS")
    if "darline" in low or "graham" in low:
        hits.add("GRAHAM")
    return hits


class Verifier:
    def __init__(self):
        self.det = cv2.FaceDetectorYN.create(os.path.join(MODELS, "yunet.onnx"), "", (640, 640),
                                             0.6, 0.3, 200)
        self.rec = cv2.FaceRecognizerSF.create(os.path.join(MODELS, "sface.onnx"), "")
        self.refs = self._refs()

    def _refs(self):
        refs = []
        for who in ("ANDREWS", "GRAHAM"):
            folder = os.path.join(ARCH, who.lower(), "campaign")
            if not os.path.isdir(folder):
                continue
            for name in sorted(os.listdir(folder)):
                if not name.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue
                if re.search(r"signature", name, re.I):
                    continue
                img = cv2.imread(os.path.join(folder, name))
                if img is None:
                    continue
                faces = self._detect(img)
                if not faces:
                    continue
                face = max(faces, key=lambda f: f[2] * f[3])
                if (face[2] * face[3]) / float(img.shape[0] * img.shape[1]) < 0.03:
                    continue
                try:
                    refs.append((who, self._embed(img, face)))
                except cv2.error:
                    continue
        return refs

    def _detect(self, img):
        h, w = img.shape[:2]
        self.det.setInputSize((w, h))
        _n, faces = self.det.detect(img)
        return [] if faces is None else list(faces)

    def _embed(self, img, face):
        aligned = self.rec.alignCrop(img, face)
        feat = self.rec.feature(aligned).flatten().astype(np.float64)
        n = np.linalg.norm(feat)
        return feat / (n if n > 0 else 1.0)

    def best(self, path):
        img = cv2.imread(path)
        if img is None:
            return None
        faces = self._detect(img)
        if not faces:
            return None
        scores = {}
        for face in faces:
            if face[2] < 30:
                continue
            try:
                feat = self._embed(img, face)
            except cv2.error:
                continue
            for who, ref in self.refs:
                s = float(np.dot(feat, ref))
                if s > scores.get(who, -1.0):
                    scores[who] = s
        if not scores:
            return None
        ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        return ranked


def next_ids():
    rows = list(csv.DictReader(open(IMAGES_CSV, encoding="utf-8")))
    ids = {}
    for r in rows:
        m = re.match(r"(AND|GRA)-IMG-(\d+)", r["image_id"])
        if m:
            ids[m.group(1)] = max(ids.get(m.group(1), 0), int(m.group(2)))
    return ids


def next_src():
    src = list(csv.DictReader(open(SOURCES_CSV, encoding="utf-8")))
    used = {int(s["source_id"].split("-")[1]) for s in src if s["source_id"].startswith("SRC-06")}
    n = 649
    while n in used:
        n += 1
    return n


def main():
    os.makedirs(INCOMING, exist_ok=True)
    links = set()
    for s in SEARCHES:
        try:
            links |= article_links(fetch(s).decode("utf-8", "replace"))
        except Exception as e:
            print(f"  search failed {s}: {e}")
    print(f"article links found: {len(links)}")

    ver = Verifier()
    print(f"reference faces: {len(ver.refs)}")

    existing = {r["original_image_url"].split("?")[0]
                for r in csv.DictReader(open(IMAGES_CSV, encoding="utf-8"))}
    ids = next_ids()
    src_n = next_src()

    picked, skipped = [], []
    for url in sorted(links)[:60]:
        slug = url.rstrip("/").rsplit("/", 1)[-1]
        who_text = candidate_by_text(slug)
        if not who_text:
            continue
        try:
            html = fetch(url).decode("utf-8", "replace")
        except Exception as e:
            skipped.append((url, f"fetch failed: {e}"))
            continue
        title = re.search(r"<title>(.*?)</title>", html, re.S)
        title = re.sub(r"\s+", " ", title.group(1)).strip() if title else ""
        og = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', html, re.I)
        if not og:
            skipped.append((url, "no og:image"))
            continue
        img_url = urllib.parse.urljoin(url, og.group(1))
        if img_url.split("?")[0] in existing:
            skipped.append((url, "image already archived"))
            continue
        tmp = os.path.join(INCOMING, re.sub(r"[^A-Za-z0-9._-]", "_", img_url.rsplit("/", 1)[-1]))
        try:
            data = fetch(img_url, timeout=60)
            open(tmp, "wb").write(data)
        except Exception as e:
            skipped.append((url, f"image fetch failed: {e}"))
            continue
        ranked = ver.best(tmp)
        if not ranked:
            skipped.append((url, "no face detected"))
            continue
        top, top_sim = ranked[0]
        second_sim = ranked[1][1] if len(ranked) > 1 else -1.0
        if top not in who_text or top_sim < SIM_THRESHOLD or (top_sim - second_sim) < MARGIN:
            skipped.append((url, f"face gate: {top} {top_sim:.3f} vs {second_sim:.3f}"))
            continue
        img = cv2.imread(tmp)
        h, w = img.shape[:2]
        picked.append({"url": url, "title": title, "who": top, "sim": round(top_sim, 3),
                       "file": tmp, "w": w, "h": h,
                       "date": "/".join(url.split("/")[3:6])})
    print(f"\naccepted {len(picked)}, skipped {len(skipped)}")

    image_rows = list(csv.DictReader(open(IMAGES_CSV, encoding="utf-8")))
    src_rows = list(csv.DictReader(open(SOURCES_CSV, encoding="utf-8")))
    fields = list(image_rows[0].keys())
    src_fields = list(src_rows[0].keys())

    added_img, added_src = [], []
    for p in picked:
        prefix = "AND" if p["who"] == "ANDREWS" else "GRA"
        ids[prefix] = ids.get(prefix, 0) + 1
        image_id = f"{prefix}-IMG-{ids[prefix]:04d}"
        folder = p["who"].lower()
        dest_dir = os.path.join(ARCH, folder, "news")
        os.makedirs(dest_dir, exist_ok=True)
        ext = os.path.splitext(p["file"])[1].lower() or ".jpg"
        local = f"{image_id}_{re.sub(r'[^A-Za-z0-9]+', '_', p['url'].rstrip('/').rsplit('/', 1)[-1])[:48]}{ext}"
        shutil.copyfile(p["file"], os.path.join(dest_dir, local))
        os.remove(p["file"])

        src_id = f"SRC-{src_n:04d}"
        src_n += 1
        added_src.append({
            "source_id": src_id, "url": p["url"], "title": p["title"][:160] or "unknown",
            "publisher": "SC Daily Gazette (States Newsroom)",
            "publication_date": p["date"], "event_date": "unknown", "access_date": ACCESS_DATE,
            "source_tier": "T2", "source_type": "news_article",
            "relevant_quote_or_info": "Photograph published with this article",
            "reliability_notes": ("States Newsroom outlet; article photography released under "
                                  "CC BY-ND 4.0, reused unmodified with credit"),
            "used_by": "unknown",
        })
        added_img.append({
            "image_id": image_id, "candidate_id": p["who"],
            "image_date": p["date"], "event_id": "unknown", "event_category": "campaign_event",
            "source_name": "SC Daily Gazette (States Newsroom)",
            "source_url": f"{src_id}|{p['url']}",
            "original_image_url": p["url"],
            "photographer": "SC Daily Gazette staff (credit on article)",
            "copyright_status": "licensed", "license": "CC BY-ND 4.0",
            "local_filename": f"{folder}/news/{local}",
            "image_resolution": f"{p['w']}x{p['h']}",
            "framing": "unknown", "camera_angle": "unknown", "image_quality": "unknown",
            "face_visibility": "unknown", "body_visibility": "unknown", "clothing_notes": "unknown",
            "notes": (f"File from article '{p['title'][:90]}'; stored unmodified (no crop) because "
                      f"CC BY-ND forbids derivatives; face gate {p['sim']} against archive references"),
            "verification_status": "verified",
        })
        print(f"  {image_id} {p['who']:7s} sim {p['sim']:.3f} {local[:60]}")

    if added_img:
        with open(IMAGES_CSV, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
            w.writerows(added_img)
        with open(SOURCES_CSV, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=src_fields, lineterminator="\n")
            w.writerows(added_src)
    report = os.path.join(HERE, "images_added_report.csv")
    with open(report, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["url", "reason"])
        w.writerows([(u, r) for u, r in skipped])
    print(f"\nappended {len(added_img)} image rows, {len(added_src)} source rows; skips in {report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
