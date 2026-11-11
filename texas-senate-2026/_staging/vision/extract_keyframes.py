#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Shot-level frame extraction: scene cuts, keyframes and per-video visual metrics.

This is the *coverage* layer that complements the identity layer (extract_faces.py):
where that script asks "who is on screen", this one asks "how is the video cut and
staged" — shot lengths, brightness/colour, motion, face presence, keyframe stills.

For each video:
  * decode a 160x90 RGB proxy at 2 fps through ffmpeg (fast: no full-res decode),
  * detect cuts on the proxy (adaptive threshold over frame-to-frame difference),
  * pick <= 8 representative keyframes spread over the longest scenes,
  * decode those few frames at full resolution and measure brightness, contrast,
    sharpness, colourfulness, saturation, mean RGB and YuNet face coverage,
  * write the still at <= 720 px wide plus a row in shot_index.csv.

Outputs (10_video_frames/):
    keyframes/<slug>/kf_###_t####.#.jpg     local working copies (Git-excluded)
    shot_index.csv                            one row per scene/keyframe
    video_visual_metrics.csv                  one row per video
    sheet_shots_1..N.jpg                      committed contact sheets

    python texas-senate-2026/_staging/vision/extract_keyframes.py --jobs 3
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
VISION = ROOT / "_staging" / "vision"
RAW = VISION / "raw"
CONFIG = VISION / "videos.json"
MODELS = VISION / "models"
DEST = ROOT / "10_video_frames"
KF = DEST / "keyframes"

PROXY_W, PROXY_H = 160, 90
PROXY_FPS = 2.0
MAX_KEYFRAMES = 8
MAX_WIDTH = 720
MIN_GAP_S = 1.5


def ffmpeg_proxy(mp4):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(mp4), "-an", "-sn",
           "-vf", f"fps={PROXY_FPS},scale={PROXY_W}:{PROXY_H}:flags=area",
           "-pix_fmt", "rgb24", "-f", "rawvideo", "pipe:1"]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10 ** 7)


def colorfulness(rgb):
    r, g, b = rgb[..., 0].astype(np.float32), rgb[..., 1].astype(np.float32), rgb[..., 2].astype(np.float32)
    rg, yb = r - g, 0.5 * (r + g) - b
    return float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))


def proxy_pass(mp4):
    """Return per-sample arrays: t, brightness, contrast, saturation, colourfulness, motion."""
    size = PROXY_W * PROXY_H * 3
    p = ffmpeg_proxy(mp4)
    bright, contr, sat, colf, motion = [], [], [], [], []
    prev = None
    n = 0
    while True:
        buf = p.stdout.read(size)
        if not buf or len(buf) < size:
            break
        arr = np.frombuffer(buf, dtype=np.uint8).reshape(PROXY_H, PROXY_W, 3)
        g = arr.mean(axis=2)
        bright.append(float(g.mean()))
        contr.append(float(g.std()))
        mx = arr.max(axis=2).astype(np.int16)
        mn = arr.min(axis=2).astype(np.int16)
        sat.append(float((mx - mn).mean()))
        colf.append(colorfulness(arr))
        motion.append(0.0 if prev is None else float(np.abs(g - prev).mean()) / 255.0)
        prev = g
        n += 1
    p.stdout.close()
    p.wait()
    if n == 0:
        return None
    t = np.arange(n) / PROXY_FPS
    return dict(t=t, brightness=np.array(bright), contrast=np.array(contr),
                saturation=np.array(sat), colorfulness=np.array(colf),
                motion=np.array(motion), n=n)


def detect_cuts(pr):
    m = pr["motion"]
    med = float(np.median(m))
    mad = float(np.median(np.abs(m - med))) + 1e-6
    thr = float(np.clip(med + 6 * mad, 0.055, 0.22))
    cuts = []
    last = -10.0
    for i in range(1, len(m)):
        if m[i] > thr and pr["t"][i] - last >= MIN_GAP_S:
            cuts.append(float(pr["t"][i]))
            last = float(pr["t"][i])
    return cuts, thr


def shot_scale(frac):
    if frac >= 0.22:
        return "close-up"
    if frac >= 0.12:
        return "medium-close"
    if frac >= 0.06:
        return "medium"
    return "wide"


def read_frame_at(cap, t, fps):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps)))
    ok, frame = cap.read()
    return frame if ok else None


def process(v, dur):
    mp4 = RAW / v["file"]
    if not mp4.exists():
        return [], None, "missing"
    pr = proxy_pass(mp4)
    if pr is None:
        return [], None, "no proxy"
    dur = float(dur or pr["n"] / PROXY_FPS)

    cuts, thr = detect_cuts(pr)
    bounds = [0.0] + [c for c in cuts if 0.5 < c < dur - 0.5] + [round(dur, 2)]
    scenes = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        if b - a < 0.3:
            continue
        scenes.append((a, b))

    # pick up to MAX_KEYFRAMES scenes: longest first, then restore time order
    order = sorted(range(len(scenes)), key=lambda i: -(scenes[i][1] - scenes[i][0]))
    chosen_idx = sorted(order[:MAX_KEYFRAMES])
    cap = cv2.VideoCapture(str(mp4))
    if not cap.isOpened():
        return [], None, "cannot open"
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

    try:
        det = cv2.FaceDetectorYN.create(str(MODELS / "yunet.onnx"), "", (640, 640), 0.5, 0.3, 100)
    except cv2.error:
        det = None

    outdir = KF / v["slug"]
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob("*.jpg"):
        old.unlink()

    rows = []
    for j, si in enumerate(chosen_idx):
        a, b = scenes[si]
        kt = a + 0.35 * (b - a)
        frame = read_frame_at(cap, kt, fps)
        if frame is None:
            frame = read_frame_at(cap, max(0.0, kt - 0.5), fps)
        if frame is None:
            continue
        h, w = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sharp = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        bright = float(gray.mean())
        contr = float(gray.std())
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        sat = float(hsv[..., 1].mean())
        rgb_mean = [int(x) for x in cv2.mean(frame)[::-1][:3]]

        faces, face_frac, face_w = [], 0.0, 0
        if det is not None:
            det.setInputSize((w, h))
            _r, found = det.detect(frame)
            if found is not None and len(found):
                big = max(found, key=lambda f: f[2] * f[3])
                face_w = int(big[2])
                face_frac = face_w / float(w)
                faces = list(found)

        small = frame
        if w > MAX_WIDTH:
            nh = int(round(h * MAX_WIDTH / w))
            small = cv2.resize(frame, (MAX_WIDTH, nh), interpolation=cv2.INTER_AREA)
        tag = f"{v['slug']}_kf{j:02d}_t{kt:07.1f}"
        path = outdir / f"{tag}.jpg"
        cv2.imwrite(str(path), small, [cv2.IMWRITE_JPEG_QUALITY, 80])

        rows.append(dict(
            keyframe_id=tag, slug=v["slug"], video_id=v["video_id"],
            candidate_source=v["candidate_source"], kind=v["kind"],
            channel=v["channel"], upload_date=v.get("upload_date", ""),
            scene_idx=si, scene_count=len(scenes),
            t_start_s=round(a, 1), t_end_s=round(b, 1), scene_len_s=round(b - a, 1),
            keyframe_t_s=round(kt, 1),
            brightness=round(bright, 1), contrast=round(contr, 1),
            sharpness=round(sharp, 1), saturation=round(sat, 1),
            colorfulness=round(colorfulness(frame), 1),
            mean_rgb=f"{rgb_mean[0]},{rgb_mean[1]},{rgb_mean[2]}",
            face_count=len(faces), largest_face_w_px=face_w,
            face_width_frac=round(face_frac, 3),
            shot_scale=shot_scale(face_frac),
            frame_path=str(path.relative_to(ROOT)),
        ))
    cap.release()

    m = pr["motion"]
    vm = dict(
        slug=v["slug"], video_id=v["video_id"], candidate_source=v["candidate_source"],
        kind=v["kind"], channel=v["channel"], upload_date=v.get("upload_date", ""),
        duration_s=round(dur, 1),
        sampled_frames=int(pr["n"]),
        scene_count=len(scenes),
        cuts_per_min=round(max(0, len(scenes) - 1) / (dur / 60), 2) if dur > 60 else "",
        mean_scene_len_s=round(dur / max(1, len(scenes)), 1),
        cut_threshold=round(thr, 3),
        brightness_mean=round(float(pr["brightness"].mean()), 1),
        contrast_mean=round(float(pr["contrast"].mean()), 1),
        saturation_mean=round(float(pr["saturation"].mean()), 1),
        colorfulness_mean=round(float(pr["colorfulness"].mean()), 1),
        motion_mean=round(float(m.mean()), 4),
        static_ratio=round(float((m < 0.01).mean()), 3),
        keyframes=len(rows),
        face_presence_ratio=round(sum(1 for r in rows if r["face_count"]) / max(1, len(rows)), 2),
    )
    return rows, vm, f"{len(scenes)} scenes, {len(rows)} keyframes"


def sheet(items, cols, cell, title, out_path):
    if not items:
        return
    rows = (len(items) + cols - 1) // cols
    pad, head = 8, 44
    W = cols * cell + (cols + 1) * pad
    H = rows * (cell + 26) + (rows + 1) * pad + head
    canvas = np.full((H, W, 3), 20, np.uint8)
    cv2.putText(canvas, title, (pad, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (240, 240, 240), 2, cv2.LINE_AA)
    for i, (img, cap_) in enumerate(items):
        r, c = divmod(i, cols)
        y0, x0 = head + pad + r * (cell + 26), pad + c * (cell + pad)
        ih, iw = img.shape[:2]
        s = min(cell / iw, cell / ih)
        th, tw = max(1, int(ih * s)), max(1, int(iw * s))
        canvas[y0:y0 + th, x0:x0 + tw] = cv2.resize(img, (tw, th))
        cv2.putText(canvas, cap_[:46], (x0 + 2, y0 + cell + 17), cv2.FONT_HERSHEY_SIMPLEX,
                    0.36, (200, 200, 200), 1, cv2.LINE_AA)
    cv2.imwrite(str(out_path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 88])
    print("wrote", out_path.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--only", default="")
    ap.add_argument("--max-videos", type=int, default=0)
    args = ap.parse_args()

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    if args.only:
        only = {s.strip() for s in args.only.split(",") if s.strip()}
        cfg = [v for v in cfg if v["slug"] in only]
    if args.max_videos:
        cfg = cfg[:args.max_videos]
    KF.mkdir(parents=True, exist_ok=True)
    print(f"{len(cfg)} videos, {args.jobs} workers", flush=True)

    all_rows, vms = [], []
    with cf.ProcessPoolExecutor(max_workers=args.jobs) as ex:
        futs = {ex.submit(process, v, v.get("duration")): v for v in cfg}
        for i, fut in enumerate(cf.as_completed(futs), 1):
            v = futs[fut]
            try:
                rows, vm, msg = fut.result()
            except Exception as e:  # noqa: BLE001
                print(f"[{i}/{len(cfg)}] FAIL {v['slug']}: {e}", flush=True)
                continue
            all_rows += rows
            if vm:
                vms.append(vm)
            print(f"[{i}/{len(cfg)}] {v['slug']:34s} {msg}", flush=True)

    all_rows.sort(key=lambda r: (r["slug"], r["keyframe_t_s"]))
    if not all_rows:
        print("no keyframes produced")
        return 1
    with open(DEST / "shot_index.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        w.writeheader()
        w.writerows(all_rows)
    vms.sort(key=lambda r: r["slug"])
    with open(DEST / "video_visual_metrics.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(vms[0].keys()))
        w.writeheader()
        w.writerows(vms)
    print(f"keyframes: {len(all_rows)} across {len(vms)} videos")

    # global contact sheets: up to 2 keyframes per video, 36 per sheet
    pick = []
    by_slug = {}
    for r in all_rows:
        by_slug.setdefault(r["slug"], []).append(r)
    for slug in sorted(by_slug):
        rs = by_slug[slug]
        take = [rs[0]] + ([rs[len(rs) // 2]] if len(rs) > 2 else [])
        pick += take
    per_sheet, cols, cell = 36, 6, 250
    for k in range(0, len(pick), per_sheet):
        items = []
        for r in pick[k:k + per_sheet]:
            img = cv2.imread(str(ROOT / r["frame_path"]))
            if img is None:
                continue
            items.append((img, f"{r['slug']} t={r['keyframe_t_s']:.0f}s {r['shot_scale']}"))
        sheet(items, cols, cell, f"Shot keyframes {k // per_sheet + 1} — staging / framing (no identity claim)",
              DEST / f"sheet_shots_{k // per_sheet + 1}.jpg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
