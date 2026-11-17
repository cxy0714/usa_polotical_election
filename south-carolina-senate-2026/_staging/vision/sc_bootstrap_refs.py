#!/usr/bin/env python
"""Bootstrap extra reference faces from the highest-confidence identifications.

The Graham reference set is composed of studio portraits, so podium frames of her score lower than
Andrews's event photographs do. One documented bootstrap round fixes that: take the frames the
first pass already matched to a candidate with high cosine, crop that face, and add it as a second
reference source. The added files are crops of frames the archive already holds, so nothing new is
being asserted — but the loop is recorded here and in the identity CSV's notes because a
self-referential reference set must be disclosed.

Output: `_staging/vision/refs_extra/{ANDREWS,GRAHAM}/*.jpg`

Run: python _staging/vision/sc_bootstrap_refs.py [--min-sim 0.55] [--per-candidate 6]
"""
import argparse
import csv
import os
import sys

import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MODELS = os.path.join(HERE, "models")
OUT = os.path.join(HERE, "refs_extra")
KF = os.path.join(ROOT, "10_video_frames", "keyframes.csv")
IDN = os.path.join(ROOT, "10_video_frames", "keyframes_identity.csv")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-sim", type=float, default=0.55)
    ap.add_argument("--per-candidate", type=int, default=6)
    args = ap.parse_args()

    det = cv2.FaceDetectorYN.create(os.path.join(MODELS, "yunet.onnx"), "", (640, 640), 0.6, 0.3, 200)
    kf = {r["frame_id"]: r for r in csv.DictReader(open(KF, encoding="utf-8"))}
    rows = [r for r in csv.DictReader(open(IDN, encoding="utf-8"))
            if r["identity"] in ("ANDREWS", "GRAHAM") and r["identity_sim"] not in ("", "unknown")]
    rows.sort(key=lambda r: -float(r["identity_sim"]))

    taken = {"ANDREWS": 0, "GRAHAM": 0}
    seen_video = {"ANDREWS": set(), "GRAHAM": set()}
    kept = 0
    for r in rows:
        who = r["identity"]
        if taken[who] >= args.per_candidate:
            continue
        if float(r["identity_sim"]) < args.min_sim:
            continue
        slug = kf[r["frame_id"]]["slug"]
        # Only harvest from videos whose subject is that one candidate, and only when the
        # recogniser agrees with the video's own subject. This is what keeps a misread face in a
        # mixed video from becoming a permanent reference (a first, looser round poisoned the
        # reference set exactly that way).
        video_candidate = "ANDREWS" if slug.startswith("AND") else (
            "GRAHAM" if slug.startswith("GRA") else None)
        if video_candidate != who:
            continue
        if slug in seen_video[who]:          # one crop per video keeps the variety
            continue
        img = cv2.imread(os.path.join(ROOT, "10_video_frames", kf[r["frame_id"]]["file"]))
        if img is None:
            continue
        scale = 2.0 if img.shape[1] < 1600 else 1.0
        if scale != 1.0:
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        h, w = img.shape[:2]
        det.setInputSize((w, h))
        _n, faces = det.detect(img)
        if faces is None or len(faces) == 0:
            continue
        face = max(faces, key=lambda f: f[2] * f[3])
        x, y, fw, fh = [int(v) for v in face[:4]]
        pad = int(0.35 * max(fw, fh))
        x0, y0 = max(0, x - pad), max(0, y - pad)
        x1, y1 = min(w, x + fw + pad), min(h, y + fh + pad)
        crop = img[y0:y1, x0:x1]
        if crop.size == 0:
            continue
        folder = os.path.join(OUT, who)
        os.makedirs(folder, exist_ok=True)
        name = f"{r['frame_id']}_sim{float(r['identity_sim']):.2f}.jpg"
        cv2.imwrite(os.path.join(folder, name), crop, [cv2.IMWRITE_JPEG_QUALITY, 95])
        seen_video[who].add(slug)
        taken[who] += 1
        kept += 1
        print(f"  {who}: {name} (from {slug})")
    print(f"kept {kept} crops -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
