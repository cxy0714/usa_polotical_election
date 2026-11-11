#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Frame sampling + YuNet face detection over the configured video set.

Decoder: ffmpeg pipes sampled frames (RGB24) at a fixed rate — OpenCV's own
VideoCapture decodes at real-time speed on this machine (measured ~30 fps), which
would make a 40-hour corpus take 40 hours; ffmpeg decodes the same files at ~17×
real time. Frames arrive on a uniform grid (0.5 s for clips ≤2 min, else 1.0 s).

Config : _staging/vision/videos.json
Inputs : raw videos in _staging/vision/raw/
Outputs: _staging/vision/out/<slug>/{faces/, .done}
         _staging/vision/out/manifest.csv

Work is split per video across processes, so a 100+ video corpus finishes in
minutes instead of hours. Already-processed videos are skipped (`.done` marker).

    python texas-senate-2026/_staging/vision/extract_faces.py --jobs 6
    python texas-senate-2026/_staging/vision/extract_faces.py --only TAL_victory_cnn --redo
"""
import argparse
import concurrent.futures as cf
import csv
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "_staging" / "vision" / "raw"
MODELS = ROOT / "_staging" / "vision" / "models"
OUT = ROOT / "_staging" / "vision" / "out"
CONFIG = ROOT / "_staging" / "vision" / "videos.json"

CONF_MIN = 0.55
MIN_FACE_PX = 64
SHARP_MIN = 25.0
SHORT_STEP = 0.5
LONG_STEP = 1.0
FACES_PER_FRAME = 2
DETECT_WIDTH = 640      # YuNet at 1280 px costs ~100 ms/frame; 640 px ~57 ms and still
                        # finds the same faces. Boxes are scaled back before cropping.


def load_detector():
    model = MODELS / "yunet.onnx"
    if model.exists() and hasattr(cv2, "FaceDetectorYN"):
        return ("yunet", cv2.FaceDetectorYN.create(str(model), "", (640, 640), CONF_MIN, 0.3, 500))
    return ("haar", cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml"))


def detect(kind, det, frame):
    h, w = frame.shape[:2]
    faces = []
    if kind == "yunet":
        det.setInputSize((w, h))
        _r, found = det.detect(frame)
        if found is not None:
            for row in found:
                x, y, bw, bh = int(row[0]), int(row[1]), int(row[2]), int(row[3])
                if bw >= MIN_FACE_PX and bh >= MIN_FACE_PX:
                    faces.append((max(0, x), max(0, y), bw, bh, float(row[-1])))
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for (x, y, bw, bh) in det.detectMultiScale(gray, 1.1, 5, minSize=(MIN_FACE_PX, MIN_FACE_PX)):
            faces.append((int(x), int(y), int(bw), int(bh), 1.0))
    faces.sort(key=lambda f: f[2] * f[3], reverse=True)
    return faces


def square_crop(frame, x, y, w, h, margin=0.45):
    cx, cy = x + w / 2.0, y + h / 2.0
    side = max(w, h) * (1.0 + margin * 2)
    x1, y1 = int(max(0, cx - side / 2)), int(max(0, cy - side / 2))
    x2, y2 = int(min(frame.shape[1], cx + side / 2)), int(min(frame.shape[0], cy + side / 2))
    crop = frame[y1:y2, x1:x2]
    if crop.size == 0:
        return None
    return cv2.resize(crop, (256, 256), interpolation=cv2.INTER_CUBIC)


def probe(mp4):
    cap = cv2.VideoCapture(str(mp4))
    if not cap.isOpened():
        return None
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return fps, frames, w, h


def process(v):
    path = RAW / v["file"]
    if not path.exists():
        return v["slug"], 0, "missing"
    info = probe(path)
    if not info or not info[2]:
        return v["slug"], 0, "cannot open"
    fps, nframes, w, h = info
    dur = nframes / fps if nframes else float(v.get("duration") or 0)
    step_s = SHORT_STEP if dur <= 120 else LONG_STEP
    sample_fps = 1.0 / step_s

    outdir = OUT / v["slug"]
    (outdir / "faces").mkdir(parents=True, exist_ok=True)
    for old in (outdir / "faces").glob("*.jpg"):
        old.unlink()

    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path), "-an", "-sn",
           "-vf", "fps=%g" % sample_fps, "-pix_fmt", "rgb24", "-f", "rawvideo", "pipe:1"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10 ** 7)
    frame_bytes = w * h * 3
    kind, det = load_detector()

    idx, kept, sampled = 0, 0, 0
    rows = []
    try:
        while True:
            buf = proc.stdout.read(frame_bytes)
            if not buf or len(buf) < frame_bytes:
                break
            rgb = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 3)
            frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            t = idx / sample_fps
            idx += 1
            sampled += 1
            faces = detect(kind, det, frame)
            if faces:
                for (x, y, fw, fh, conf) in faces[:FACES_PER_FRAME]:
                    crop = square_crop(frame, x, y, fw, fh)
                    if crop is None:
                        continue
                    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                    sharp = float(cv2.Laplacian(gray, cv2.CV_64F).var())
                    if sharp < SHARP_MIN:
                        continue
                    kept += 1
                    tag = f"{v['slug']}_t{t:07.2f}_f{kept:04d}"
                    cv2.imwrite(str(outdir / "faces" / f"{tag}.jpg"), crop,
                                [cv2.IMWRITE_JPEG_QUALITY, 88])
                    rows.append({
                        "frame_id": tag, "slug": v["slug"], "candidate_source": v["candidate_source"],
                        "video_id": v["video_id"], "video_kind": v["kind"],
                        "source_video": v["file"], "timestamp_s": round(t, 2),
                        "face_w_px": fw, "face_h_px": fh, "confidence": round(conf, 3),
                        "sharpness": round(sharp, 1), "brightness": round(float(gray.mean()), 1),
                    })
    finally:
        proc.stdout.close()
        proc.wait()

    (outdir / ".done").write_text(str(kept), encoding="utf-8")
    return v["slug"], rows, f"dur={dur:.1f}s step={step_s}s sampled={sampled} faces={kept}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default="", help="comma-separated slugs")
    ap.add_argument("--redo", action="store_true", help="re-process even if .done exists")
    args = ap.parse_args()

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    only = {s for s in args.only.split(",") if s.strip()}
    todo = [v for v in cfg if (not only or v["slug"] in only)]
    if not args.redo:
        todo = [v for v in todo if not (OUT / v["slug"] / ".done").exists()]
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"videos: {len(todo)} | jobs: {args.jobs}", flush=True)

    all_rows = []
    with cf.ProcessPoolExecutor(max_workers=args.jobs) as ex:
        futs = {ex.submit(process, v): v for v in todo}
        for i, fut in enumerate(cf.as_completed(futs), 1):
            v = futs[fut]
            try:
                slug, rows, msg = fut.result()
            except Exception as e:  # noqa: BLE001
                print(f"[{i}/{len(todo)}] FAIL {v['slug']}: {e}", flush=True)
                continue
            if isinstance(rows, list):
                all_rows += rows
            print(f"[{i}/{len(todo)}] {slug:34s} {msg}", flush=True)

    # merge with rows from previously processed videos that were skipped
    have = {r["frame_id"] for r in all_rows}
    mp = OUT / "manifest.csv"
    if mp.exists():
        for r in csv.DictReader(open(mp, encoding="utf-8")):
            if r["frame_id"] not in have:
                all_rows.append(r)
    all_rows.sort(key=lambda r: (r["slug"], float(r["timestamp_s"])))
    if all_rows:
        with open(mp, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
            w.writeheader()
            w.writerows(all_rows)
    print("manifest rows:", len(all_rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
