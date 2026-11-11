#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Identity pass over extracted face crops (OpenCV SFace, cosine metric).

- References: licensed candidate photographs already in 04_visual_archive/.
- Queries   : face crops produced by extract_faces.py.
- Output    : _staging/vision/out/identity.csv  + curated contact sheets

No appearance judgement is made. Labels are nearest-neighbour votes over
reference photos and are reported with their similarity scores.
"""
import argparse
import concurrent.futures as cf
import csv
import glob
import sys
from collections import Counter, defaultdict
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
VISION = ROOT / "_staging" / "vision"
MODELS = VISION / "models"
OUT = VISION / "out"
ARCH = ROOT / "04_visual_archive"

REF_DIRS = {
    "TALARICO": str(ARCH / "talarico" / "campaign"),
    "PAXTON": str(ARCH / "paxton" / "campaign"),
}
DET_CONF = 0.7
SIM_THRESHOLD = 0.40      # SFace cosine, conservative
MARGIN = 0.05             # top class must beat the other class by this much


def load_models():
    det = cv2.FaceDetectorYN.create(str(MODELS / "yunet.onnx"), "", (640, 640), 0.6, 0.3, 200)
    rec = cv2.FaceRecognizerSF.create(str(MODELS / "sface.onnx"), "")
    return det, rec


def biggest_face(det, img):
    h, w = img.shape[:2]
    det.setInputSize((w, h))
    _r, faces = det.detect(img)
    if faces is None or len(faces) == 0:
        return None
    best = max(faces, key=lambda f: f[2] * f[3])
    return best


def embed(rec, img, face):
    aligned = rec.alignCrop(img, face)
    feat = rec.feature(aligned).flatten().astype(np.float64)
    n = np.linalg.norm(feat)
    return feat / (n if n > 0 else 1.0)


def build_references(det, rec, quiet=False):
    refs = []
    for label, d in REF_DIRS.items():
        files = sorted(glob.glob(d + "/*.jpg") + glob.glob(d + "/*.jpeg") + glob.glob(d + "/*.png"))
        if not quiet:
            print(f"{label}: {len(files)} reference files")
        for f in files:
            img = cv2.imread(f)
            if img is None:
                continue
            face = biggest_face(det, img)
            if face is None:
                continue
            if face[2] < 40:
                continue
            try:
                feat = embed(rec, img, face)
            except cv2.error:
                continue
            refs.append((label, feat, Path(f).name))
    if not quiet:
        print("reference embeddings:", len(refs))
    import itertools
    same, cross = [], []
    for (l1, f1, _), (l2, f2, _) in itertools.combinations(refs, 2):
        s = float(np.dot(f1, f2))
        (same if l1 == l2 else cross).append(s)
    if not quiet:
        print(f"ref-sanity: same-class mean={np.mean(same):.3f}  cross-class mean={np.mean(cross):.3f}")
    return refs


def classify(feat, refs):
    """Class-balanced nearest-neighbour: best cosine per class, then margin."""
    best = {}
    for lab, f, _name in refs:
        s = float(np.dot(feat, f))
        if lab not in best or s > best[lab]:
            best[lab] = s
    ranked = sorted(best.items(), key=lambda kv: kv[1], reverse=True)
    top_lab, top_sim = ranked[0]
    second_lab, second_sim = ranked[1] if len(ranked) > 1 else ("", -1.0)
    return top_lab, top_sim, second_lab, second_sim


def label_img(img, text, scale=0.45):
    cv2.putText(img, text, (5, img.shape[0] - 7), cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(img, text, (5, img.shape[0] - 7), cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), 1, cv2.LINE_AA)
    return img


def sheet(items, cols, cell, title, out_path):
    if not items:
        print("no items for", out_path.name)
        return
    rows = (len(items) + cols - 1) // cols
    pad, head = 8, 46
    W = cols * cell + (cols + 1) * pad
    H = rows * (cell + 24) + (rows + 1) * pad + head
    canvas = np.full((H, W, 3), 22, dtype=np.uint8)
    cv2.putText(canvas, title, (pad, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (245, 245, 245), 2, cv2.LINE_AA)
    for i, (img, cap) in enumerate(items):
        r, c = divmod(i, cols)
        y0 = head + pad + r * (cell + 24)
        x0 = pad + c * (cell + pad)
        canvas[y0:y0 + cell, x0:x0 + cell] = cv2.resize(img, (cell, cell))
        cv2.putText(canvas, cap, (x0 + 2, y0 + cell + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (195, 195, 195), 1, cv2.LINE_AA)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 88])
    print("wrote", out_path.relative_to(ROOT))


def ts_of(fid):
    try:
        return float(fid.rsplit("_t", 1)[1].split("_")[0])
    except Exception:  # noqa: BLE001
        return 0.0


_DET = _REC = _REFS = None


def _init():
    global _DET, _REC, _REFS
    _DET, _REC = load_models()
    _REFS = build_references(_DET, _REC, quiet=True)


def _work(job):
    path, fid, slug = job
    img = cv2.imread(path)
    if img is None:
        return None
    face = biggest_face(_DET, img)
    if face is None:
        return dict(frame_id=fid, slug=slug, label="noface", sim=0.0,
                    best_other="", best_other_sim=0.0)
    try:
        feat = embed(_REC, img, face)
    except cv2.error:
        return None
    top_lab, top_sim, sec_lab, sec_sim = classify(feat, _REFS)
    ok = top_sim >= SIM_THRESHOLD and (top_sim - sec_sim) >= MARGIN
    return dict(frame_id=fid, slug=slug, label=top_lab if ok else "unknown",
                sim=round(float(top_sim), 4), best_other=sec_lab,
                best_other_sim=round(float(sec_sim), 4))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--per-video", type=int, default=120,
                    help="max crops per video, evenly spread in time (0 = all)")
    ap.add_argument("--only", default="")
    args = ap.parse_args()

    manifest_ids = {r["frame_id"] for r in csv.DictReader(open(OUT / "manifest.csv", encoding="utf-8"))}
    only = {s for s in args.only.split(",") if s.strip()}
    by_slug = defaultdict(list)
    for crop in sorted(glob.glob(str(OUT / "*" / "faces" / "*.jpg"))):
        p = Path(crop)
        if p.stem not in manifest_ids:
            continue
        slug = p.parents[1].name
        if only and slug not in only:
            continue
        by_slug[slug].append((crop, p.stem, slug))

    jobs = []
    for slug, items in by_slug.items():
        items.sort(key=lambda j: ts_of(j[1]))
        n = len(items)
        keep = n if not args.per_video else min(n, args.per_video)
        stride = max(1, n // keep) if keep else 1
        jobs.extend(items[::stride][:keep])
        if args.per_video and n > keep and len(items[::stride][:keep]) < keep:
            jobs.extend(items[-1:])
    print(f"crops: {sum(len(v) for v in by_slug.values())} | sampled: {len(jobs)} "
          f"| videos: {len(by_slug)} | jobs: {args.jobs}", flush=True)

    rows = []
    with cf.ProcessPoolExecutor(max_workers=args.jobs, initializer=_init) as ex:
        for i, res in enumerate(ex.map(_work, jobs, chunksize=16), 1):
            if res is not None:
                rows.append(res)
            if i % 2000 == 0:
                print(f"  {i}/{len(jobs)}", flush=True)

    with open(OUT / "identity.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["frame_id", "slug", "label", "sim",
                                          "best_other", "best_other_sim"])
        w.writeheader(); w.writerows(rows)
    counts = Counter(r["label"] for r in rows)
    print("identity counts:", dict(counts))

    # curated sheets: per candidate, best-scoring, time-spread
    for cand in ("TALARICO", "PAXTON"):
        sel = [r for r in rows if r["label"] == cand]
        sel.sort(key=lambda r: (-r["sim"], r["slug"]))
        seen = defaultdict(int); items = []
        for r in sel:
            img = cv2.imread(str(OUT / r["slug"] / "faces" / (r["frame_id"] + ".jpg")))
            if img is None:
                continue
            t = ts_of(r["frame_id"])
            key = (r["slug"], int(t // 10))
            if seen[key] >= 2:
                continue
            seen[key] += 1
            items.append((label_img(img, f"{r['sim']:.2f} t={t:.1f}s"), r["frame_id"]))
            if len(items) >= 35:
                break
        sheet(items, 5, 200, f"IDENTIFIED {cand}  (SFace cosine vs archive refs)", OUT / f"sheet_{cand.lower()}.jpg")

    # two-candidate comparison sheet: best BOTH-source video by identified count
    both_counts = Counter(r["slug"] for r in rows
                          if r["label"] in ("TALARICO", "PAXTON") and r["slug"].startswith("BOTH"))
    if both_counts:
        slug = both_counts.most_common(1)[0][0]
        items = []
        for r in rows:
            if r["slug"] != slug or r["label"] not in ("TALARICO", "PAXTON"):
                continue
            img = cv2.imread(str(OUT / r["slug"] / "faces" / (r["frame_id"] + ".jpg")))
            if img is None:
                continue
            t = ts_of(r["frame_id"])
            items.append((label_img(img, f"{r['label'][:3]} {r['sim']:.2f} t={t:.0f}s"), r["frame_id"]))
        items = items[:40]
        sheet(items, 5, 200, f"BOTH CANDIDATES — {slug}", OUT / "sheet_both.jpg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
