#!/usr/bin/env python
"""Re-check the news photographs with a stricter face gate, and drop the ones that fail.

The first harvest accepted a photograph of Lindsey Graham standing beside Tim Scott as if it were
Annie Andrews, at cosine 0.367 — barely over the 0.363 floor used for video frames, where the frame
context already implies who is on screen. A news photograph carries no such context, so the bar here
is raised to 0.55, and every row already appended is re-checked against it.
"""
import csv
import os
import re
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ARCH = os.path.join(ROOT, "04_visual_archive")
MODELS = os.path.join(HERE, "vision", "models")
IMAGES = os.path.join(ARCH, "image_archive.csv")
SOURCES = os.path.join(ROOT, "09_sources", "sources.csv")

STRICT = 0.55
MARGIN = 0.05


def refs(rec, det):
    out = []
    for who in ("ANDREWS", "GRAHAM"):
        folder = os.path.join(ARCH, who.lower(), "campaign")
        for name in sorted(os.listdir(folder)):
            if not name.lower().endswith((".jpg", ".jpeg", ".png")) or "signature" in name.lower():
                continue
            img = cv2.imread(os.path.join(folder, name))
            if img is None:
                continue
            det.setInputSize((img.shape[1], img.shape[0]))
            _n, faces = det.detect(img)
            if faces is None or len(faces) == 0:
                continue
            face = max(faces, key=lambda f: f[2] * f[3])
            if (face[2] * face[3]) / float(img.shape[0] * img.shape[1]) < 0.03:
                continue
            try:
                f = rec.feature(rec.alignCrop(img, face)).flatten().astype(np.float64)
            except cv2.error:
                continue
            out.append((who, f / np.linalg.norm(f)))
    return out


def score(path, rec, det, R):
    img = cv2.imread(path)
    if img is None:
        return None
    det.setInputSize((img.shape[1], img.shape[0]))
    _n, faces = det.detect(img)
    if faces is None:
        return None
    best = {}
    for face in faces:
        if face[2] < 30:
            continue
        try:
            f = rec.feature(rec.alignCrop(img, face)).flatten().astype(np.float64)
        except cv2.error:
            continue
        f = f / np.linalg.norm(f)
        for who, r in R:
            s = float(np.dot(f, r))
            best[who] = max(best.get(who, -1.0), s)
    if not best:
        return None
    return sorted(best.items(), key=lambda kv: kv[1], reverse=True)


def main():
    det = cv2.FaceDetectorYN.create(os.path.join(MODELS, "yunet.onnx"), "", (640, 640), 0.6, 0.3, 200)
    rec = cv2.FaceRecognizerSF.create(os.path.join(MODELS, "sface.onnx"), "")
    R = refs(rec, det)

    rows = list(csv.DictReader(open(IMAGES, encoding="utf-8")))
    fields = list(rows[0].keys())
    keep, drop = [], []
    for r in rows:
        if r["source_name"] != "SC Daily Gazette (States Newsroom)":
            keep.append(r)
            continue
        path = os.path.join(ARCH, r["local_filename"])
        ranked = score(path, rec, det, R) if os.path.exists(path) else None
        if not ranked:
            drop.append((r, "re-check: no face found"))
            continue
        top, sim = ranked[0]
        second = ranked[1][1] if len(ranked) > 1 else -1.0
        if top != r["candidate_id"] or sim < STRICT or (sim - second) < MARGIN:
            drop.append((r, f"re-check: {top} {sim:.3f} vs {second:.3f}, row says {r['candidate_id']}"))
            continue
        r["notes"] = r["notes"] + f"; re-checked at strict gate {sim:.3f}"
        keep.append(r)
        print(f"  keep {r['image_id']} {r['candidate_id']:7s} {sim:.3f}")

    for r, why in drop:
        print(f"  drop {r['image_id']} {r['candidate_id']:7s} — {why}")
        path = os.path.join(ARCH, r["local_filename"])
        if os.path.exists(path):
            os.remove(path)
        src_id = r["source_url"].split("|")[0]
        still_used = any(s["source_url"].startswith(src_id + "|") for s in keep)
        if not still_used:
            src_rows = list(csv.DictReader(open(SOURCES, encoding="utf-8")))
            src_fields = list(src_rows[0].keys())
            src_rows = [s for s in src_rows if s["source_id"] != src_id]
            with open(SOURCES, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=src_fields, lineterminator="\n")
                w.writeheader()
                w.writerows(src_rows)

    with open(IMAGES, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(keep)
    print(f"\nkept {len(keep)} rows ({len(keep) - (len(rows) - len([r for r in rows if r['source_name'] != 'SC Daily Gazette (States Newsroom)']))} from the news source), dropped {len(drop)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
