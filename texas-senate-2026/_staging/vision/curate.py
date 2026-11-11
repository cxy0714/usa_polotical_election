#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Curate identified frames with scene/outfit de-duplication.

Reads _staging/vision/out/{manifest.csv,identity.csv} and _staging/vision/videos.json,
re-extracts candidate frames, then keeps one representative per "same scene + same
outfit" cluster (perceptual hash + torso-colour signature) and writes
texas-senate-2026/10_video_frames/.

Rights note: frames are research references cut from news / official campaign videos.
They are NOT licensed for republication.
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
VISION = ROOT / "_staging" / "vision"
RAW = VISION / "raw"
OUTV = VISION / "out"
DEST = ROOT / "10_video_frames"

MIN_SIM = 0.62
MIN_SHARP = 40.0
MIN_FACE = 80
MAX_PICKS_PER_VIDEO = 6
MAX_PICKS_PER_CAND = 110
MIN_GAP = 1.5

PHASH_HAMMING = 12        # same video: <= this = near-identical framing
PHASH_CROSS = 6           # across videos: only near-identical image counts as duplicate
OUTFIT_RGB_DIST = 40.0    # torso-region colour distance (0-441 scale)
MAX_PER_VIDEO_OUTFIT = 3  # keep at most 3 frames per (video, outfit colour) cluster


def load_videos():
    cfg = json.loads((VISION / "videos.json").read_text(encoding="utf-8"))
    return {v["slug"]: v for v in cfg}


def phash(img):
    """64-bit DCT perceptual hash of the frame."""
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.resize(g, (32, 32), interpolation=cv2.INTER_AREA).astype(np.float32)
    d = cv2.dct(g)[:8, :8]
    bits = d > np.median(d)
    val = 0
    for b in bits.flatten():
        val = (val << 1) | int(bool(b))
    return val


def hamming(a, b):
    return int(a ^ b).bit_count()


def shot_scale(face_w, frame_w):
    r = face_w / float(frame_w)
    if r >= 0.22:
        return "close-up"
    if r >= 0.12:
        return "medium-close"
    if r >= 0.06:
        return "medium"
    return "wide"


def torso_color(frame, bbox):
    x, y, w, h = bbox
    x1 = int(max(0, x - 0.3 * w)); x2 = int(min(frame.shape[1], x + 1.3 * w))
    y1 = int(min(frame.shape[0], y + 1.15 * h)); y2 = int(min(frame.shape[0], y + 2.6 * h))
    if y2 <= y1:
        return (0, 0, 0)
    reg = frame[y1:y2, x1:x2]
    if reg.size == 0:
        return (0, 0, 0)
    b, g, r = [int(v) for v in cv2.mean(reg)[:3]]
    return (r, g, b)


def rgb_dist(a, b):
    return float(np.sqrt(sum((int(x) - int(y)) ** 2 for x, y in zip(a, b))))


def draw(frame, bbox, text):
    x, y, w, h = bbox
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 220, 0), 2)
    ty = max(18, y - 8)
    cv2.putText(frame, text, (x, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4, cv2.LINE_AA)
    cv2.putText(frame, text, (x, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    return frame


def sheet(items, cols, cell, title, out_path, caption_h=26):
    if not items:
        return
    rows = (len(items) + cols - 1) // cols
    pad, head = 10, 52
    W = cols * cell + (cols + 1) * pad
    H = rows * (cell + caption_h) + (rows + 1) * pad + head
    canvas = np.full((H, W, 3), 20, dtype=np.uint8)
    cv2.putText(canvas, title, (pad, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (245, 245, 245), 2, cv2.LINE_AA)
    for i, (img, cap) in enumerate(items):
        r, c = divmod(i, cols)
        y0 = head + pad + r * (cell + caption_h)
        x0 = pad + c * (cell + pad)
        ih, iw = img.shape[:2]
        s = min(cell / iw, cell / ih)
        th, tw = int(ih * s), int(iw * s)
        canvas[y0:y0 + th, x0:x0 + tw] = cv2.resize(img, (tw, th))
        cv2.putText(canvas, cap, (x0 + 2, y0 + cell + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (210, 210, 210), 1, cv2.LINE_AA)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print("wrote", out_path.relative_to(ROOT))


def read_frame(video_file, t):
    cap = cv2.VideoCapture(str(RAW / video_file))
    if not cap.isOpened():
        return None
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps)))
    ok, frame = cap.read()
    cap.release()
    return frame if ok else None


def main():
    videos = load_videos()
    manifest = {r["frame_id"]: r for r in csv.DictReader(open(OUTV / "manifest.csv", encoding="utf-8"))}
    ident = {r["frame_id"]: r for r in csv.DictReader(open(OUTV / "identity.csv", encoding="utf-8"))}

    picks = []
    for fid, idr in ident.items():
        if idr["label"] not in ("TALARICO", "PAXTON"):
            continue
        m = manifest.get(fid)
        if not m:
            continue
        if float(idr["sim"]) < MIN_SIM or float(m["sharpness"]) < MIN_SHARP:
            continue
        if int(m["face_w_px"]) < MIN_FACE:
            continue
        picks.append((fid, idr, m))
    picks.sort(key=lambda p: (-float(p[1]["sim"]), -int(p[2]["face_w_px"])))

    # stage 1: per-video candidate pools (time-spread), then round-robin across videos
    # so that a dense rally cannot starve the other venues.
    pools = defaultdict(list)  # (lab, slug) -> [(fid, idr, m)]
    for fid, idr, m in picks:
        pools[(idr["label"], m["slug"])].append((fid, idr, m))
    selected = defaultdict(list)
    for (lab, slug), items in pools.items():
        items.sort(key=lambda p: -float(p[1]["sim"]))
        chosen = []
        for fid, idr, m in items:
            if len(chosen) >= MAX_PICKS_PER_VIDEO:
                break
            t = float(m["timestamp_s"])
            if any(abs(float(mm["timestamp_s"]) - t) < MIN_GAP for _f, _i, mm in chosen):
                continue
            chosen.append((fid, idr, m))
        selected[(lab, slug)] = chosen

    cand = defaultdict(list)
    slugs_by_lab = defaultdict(list)
    for (lab, slug) in selected:
        slugs_by_lab[lab].append(slug)
    for lab, slugs in slugs_by_lab.items():
        ordered = sorted(slugs, key=lambda s: (-len(selected[(lab, s)]), s))
        round_i = 0
        while len(cand[lab]) < MAX_PICKS_PER_CAND:
            added = False
            for slug in ordered:
                pool = selected[(lab, slug)]
                if round_i < len(pool):
                    cand[lab].append(pool[round_i])
                    added = True
                    if len(cand[lab]) >= MAX_PICKS_PER_CAND:
                        break
            if not added:
                break
            round_i += 1

    for sub in ("frames", "faces", "context"):
        d = DEST / sub
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob("*.jpg"):
            old.unlink()

    det = cv2.FaceDetectorYN.create(str(VISION / "models" / "yunet.onnx"), "", (640, 640), 0.5, 0.3, 200)

    # stage 2: extract candidate frames and compute signatures
    records = []
    for lab in ("TALARICO", "PAXTON"):
        for fid, idr, m in cand[lab]:
            slug = m["slug"]
            v = videos.get(slug)
            if not v:
                continue
            frame = read_frame(v["file"], float(m["timestamp_s"]))
            if frame is None:
                continue
            fw = frame.shape[1]
            det.setInputSize((fw, frame.shape[0]))
            _r, faces = det.detect(frame)
            if faces is None:
                continue
            face = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = int(face[0]), int(face[1]), int(face[2]), int(face[3])
            records.append({
                "lab": lab, "slug": slug, "video": v, "frame": frame,
                "bbox": (x, y, w, h), "sim": float(idr["sim"]),
                "sharp": float(m["sharpness"]), "bright": m["brightness"],
                "t": float(m["timestamp_s"]), "src_id": fid,
                "phash": phash(frame), "rgb": torso_color(frame, (x, y, w, h)),
                "scale": shot_scale(w, fw),
            })

    # stage 3: greedy de-duplication (same scene + same outfit)
    records.sort(key=lambda r: (-r["sim"], -r["sharp"], -r["bbox"][2]))
    kept = []
    outfit_count = defaultdict(int)
    for rec in records:
        dup = False
        for other in kept:
            if other["lab"] != rec["lab"]:
                continue
            ham = hamming(rec["phash"], other["phash"])
            col = rgb_dist(rec["rgb"], other["rgb"])
            same_video = rec["slug"] == other["slug"]
            if same_video:
                if ham <= PHASH_HAMMING or (col <= 12.0 and ham <= 20):
                    dup = True
                    break
            elif ham <= PHASH_CROSS:
                dup = True
                break
        if dup:
            continue
        outfit_key = (rec["lab"], rec["slug"], tuple(int(c // 24) for c in rec["rgb"]))
        if outfit_count[outfit_key] >= MAX_PER_VIDEO_OUTFIT:
            continue
        outfit_count[outfit_key] += 1
        kept.append(rec)

    print(f"candidates={len(records)} kept={len(kept)} "
          f"(T={sum(1 for r in kept if r['lab']=='TALARICO')}, "
          f"P={sum(1 for r in kept if r['lab']=='PAXTON')})")

    stats = dict(
        candidates=len(records), kept=len(kept),
        kept_tal=sum(1 for r in kept if r["lab"] == "TALARICO"),
        kept_pax=sum(1 for r in kept if r["lab"] == "PAXTON"),
        removed=len(records) - len(kept),
        per_video={},
    )
    for r in kept:
        stats["per_video"][r["slug"]] = stats["per_video"].get(r["slug"], 0) + 1
    (DEST / "curation_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    caps = defaultdict(list)
    rows = []
    for rec in kept:
        v, lab = rec["video"], rec["lab"]
        x, y, w, h = rec["bbox"]
        t = rec["t"]
        text = f"{lab} {rec['sim']:.2f}"
        ann = draw(rec["frame"].copy(), (x, y, w, h), text)
        base = f"{lab.lower()}_{rec['slug']}_t{t:07.1f}"
        cv2.imwrite(str(DEST / "frames" / f"{base}.jpg"), rec["frame"], [cv2.IMWRITE_JPEG_QUALITY, 92])
        cv2.imwrite(str(DEST / "frames" / f"{base}_annot.jpg"), ann, [cv2.IMWRITE_JPEG_QUALITY, 92])
        src_crop = OUTV / rec["slug"] / "faces" / (rec["src_id"] + ".jpg")
        if src_crop.exists():
            import shutil
            shutil.copy(src_crop, DEST / "faces" / f"{base}.jpg")
        rows.append(dict(
            frame_id=base, identity=lab, identity_sim=round(rec["sim"], 3),
            video_id=v["video_id"], event_kind=v["kind"], source_title=v["title"],
            channel=v["channel"], upload_date=v["upload_date"], timestamp_s=round(t, 1),
            face_w_px=w, face_h_px=h,
            shot_scale=rec["scale"],
            sharpness=rec["bright"] if False else rec["sharp"], brightness=rec["bright"],
            torso_region_rgb=f"{rec['rgb'][0]},{rec['rgb'][1]},{rec['rgb'][2]}",
            frame_path=str((DEST / "frames" / f"{base}.jpg").relative_to(ROOT)),
            annotated_path=str((DEST / "frames" / f"{base}_annot.jpg").relative_to(ROOT)),
            face_crop_path=str((DEST / "faces" / f"{base}.jpg").relative_to(ROOT)),
        ))
        caps[lab].append((ann, f"{lab[:3]} t={t:.1f}s {rec['sim']:.2f} {rec['scale']}"))

    with open(DEST / "frame_index.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["frame_id"])
        w.writeheader(); w.writerows(rows)
    print("curated frames:", len(rows))

    vid_rows = []
    for v in videos.values():
        if not (RAW / v["file"]).exists():
            continue
        vid_rows.append(dict(video_id=v["video_id"], slug=v["slug"], event_kind=v["kind"],
                             title=v["title"], channel=v["channel"], upload_date=v["upload_date"],
                             duration_s=v["duration"],
                             url=f"https://www.youtube.com/watch?v={v['video_id']}"))
    with open(DEST / "video_sources.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(vid_rows[0].keys()))
        w.writeheader(); w.writerows(vid_rows)
    print("videos:", len(vid_rows))

    for lab in ("TALARICO", "PAXTON"):
        sheet(caps.get(lab, []), 6, 250,
              f"{lab} — de-duplicated frames identified by SFace",
              DEST / f"sheet_{lab.lower()}_frames.jpg")
    duel = []
    for lab in ("TALARICO", "PAXTON"):
        duel += caps.get(lab, [])[:12]
    sheet(duel, 6, 240, "Both candidates — face-matched, de-duplicated frames",
          DEST / "sheet_duel.jpg")

    ctx = []
    for v in videos.values():
        if not (RAW / v["file"]).exists():
            continue
        cap = cv2.VideoCapture(str(RAW / v["file"]))
        if not cap.isOpened():
            continue
        fps = cap.get(cv2.CAP_PROP_FPS) or 25
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        dur = total / fps if total else float(v["duration"])
        for frac in (0.15, 0.55, 0.90):
            t = dur * frac
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps)))
            ok, frame = cap.read()
            if not ok:
                continue
            tag = f"{v['slug']}_t{t:06.1f}"
            vis = frame.copy()
            cv2.putText(vis, f"{v['slug']}  t={t:.1f}s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (0, 0, 0), 4, cv2.LINE_AA)
            cv2.putText(vis, f"{v['slug']}  t={t:.1f}s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.imwrite(str(DEST / "context" / f"{tag}.jpg"), vis, [cv2.IMWRITE_JPEG_QUALITY, 90])
            ctx.append((vis, f"{v['slug']} t={t:.1f}s"))
        cap.release()
    for k in range(0, len(ctx), 36):
        suffix = "" if k == 0 else "_%d" % (k // 36 + 1)
        sheet(ctx[k:k + 36], 6, 240, "Staging context — evenly spaced frames from every source video",
              DEST / f"sheet_context{suffix}.jpg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
