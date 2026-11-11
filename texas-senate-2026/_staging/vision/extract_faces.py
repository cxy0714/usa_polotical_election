#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Frame sampling + YuNet face detection over the configured video set.

Config : _staging/vision/videos.json
Inputs : raw videos in _staging/vision/raw/
Outputs: _staging/vision/out/<slug>/{faces,sheet_faces.jpg,sheet_frames.jpg}
         _staging/vision/out/manifest.csv
"""
import csv
import json
import sys
from pathlib import Path

import cv2

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
FACES_PER_FRAME = 3


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


def process(v, kind, det):
    path = RAW / v["file"]
    if not path.exists():
        print("missing", v["file"])
        return 0, []
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        print("cannot open", path)
        return 0, []
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    dur = total / fps if total else float(v.get("duration") or 0)
    step_s = SHORT_STEP if dur <= 120 else LONG_STEP
    step = max(1, int(round(fps * step_s)))
    outdir = OUT / v["slug"]
    (outdir / "faces").mkdir(parents=True, exist_ok=True)

    idx, kept, sampled = 0, 0, 0
    rows = []
    while True:
        if not cap.grab():
            break
        if idx % step == 0:
            ok, frame = cap.retrieve()
            if not ok:
                break
            sampled += 1
            faces = detect(kind, det, frame)
            if faces:
                t = idx / fps
                for (x, y, w, h, conf) in faces[:FACES_PER_FRAME]:
                    crop = square_crop(frame, x, y, w, h)
                    if crop is None:
                        continue
                    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                    sharp = float(cv2.Laplacian(gray, cv2.CV_64F).var())
                    if sharp < SHARP_MIN:
                        continue
                    kept += 1
                    tag = f"{v['slug']}_t{t:07.2f}_f{kept:04d}"
                    cv2.imwrite(str(outdir / "faces" / f"{tag}.jpg"), crop, [cv2.IMWRITE_JPEG_QUALITY, 88])
                    rows.append({
                        "frame_id": tag, "slug": v["slug"], "candidate_source": v["candidate_source"],
                        "video_id": v["video_id"], "video_kind": v["kind"],
                        "source_video": v["file"], "timestamp_s": round(t, 2),
                        "face_w_px": w, "face_h_px": h, "confidence": round(conf, 3),
                        "sharpness": round(sharp, 1), "brightness": round(float(gray.mean()), 1),
                    })
        idx += 1
    cap.release()
    print(f"{v['slug']}: dur={dur:.1f}s step={step_s}s sampled={sampled} faces={kept}")
    return kept, rows


def main():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    kind, det = load_detector()
    print("detector:", kind, "| videos:", len(cfg))
    all_rows = []
    for v in cfg:
        _kept, rows = process(v, kind, det)
        all_rows += rows
    with open(OUT / "manifest.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()) if all_rows else ["frame_id"])
        w.writeheader()
        w.writerows(all_rows)
    print("manifest rows:", len(all_rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())

