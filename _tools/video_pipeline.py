#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generic video keyframe + face-identification pipeline for the batch-2 cases.

Stages (run one at a time, all idempotent):

    python _tools/video_pipeline.py discover <case>
    python _tools/video_pipeline.py download <case> [--limit N]
    python _tools/video_pipeline.py frames   <case>
    python _tools/video_pipeline.py faces    <case>
    python _tools/video_pipeline.py report   <case>

Inputs
    <case>/_staging/vision/videos.json     curated list [{"slug","video_id","candidate_source","kind","title"}]
    <case>/04_visual_archive/image_archive.csv  licensed portraits used as SFace references

Outputs (mirroring the South Carolina case)
    <case>/10_video_frames/keyframes.csv
    <case>/10_video_frames/keyframes_identity.csv
    <case>/10_video_frames/video_face_summary.csv
    <case>/10_video_frames/video_sources.csv
    <case>/10_video_frames/keyframes/<slug>/*.jpg

Face recognition uses OpenCV YuNet + SFace with the weights from the Texas case
(`texas-senate-2026/_staging/vision/models/*.onnx`); nothing is inferred without a
similarity floor and a margin over the runner-up identity.
"""
import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "texas-senate-2026" / "_staging" / "vision" / "models"
DET_CONF = 0.6
SIM_THRESHOLD = 0.363          # OpenCV's published SFace cosine threshold
MARGIN = 0.05
MAX_FRAMES = 20
FRAME_WIDTH = 960
SCENE_THRESHOLD = 0.30

KF_HEADER = ["frame_id", "video_id", "slug", "candidate_source", "kind", "timestamp_s", "timecode",
             "scene_score", "file", "width", "height", "faces_detected", "largest_face_area_pct",
             "face_boxes", "caption", "notes"]
ID_HEADER = ["frame_id", "identity", "identity_sim", "second_identity", "second_sim", "faces",
             "candidate_faces", "identity_note"]
SUM_HEADER = ["video_id", "slug", "candidate_source", "kind", "frames_extracted", "frames_with_face",
              "max_faces", "mean_largest_face_pct", "duration_s", "notes"]
SRC_HEADER = ["video_id", "slug", "candidate_source", "kind", "title", "channel", "upload_date",
              "duration_s", "url", "local_file", "bytes"]


def read_rows(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow([r.get(h, "unknown") for h in header])


def load_cfg(case):
    p = ROOT / case / "_staging" / "vision" / "videos.json"
    if not os.path.exists(p):
        raise SystemExit(f"missing {p}")
    return json.load(open(p, encoding="utf-8"))


def yt(args):
    cmd = [sys.executable, "-m", "yt_dlp", "--no-warnings"] + args
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def timecode(ts):
    if ts is None:
        return "unknown"
    m, s = divmod(int(round(ts)), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def cmd_meta(case):
    """Fill title/channel/upload_date/duration from YouTube for the curated list."""
    d = ROOT / case / "_staging" / "vision"
    p = d / "videos.json"
    cfg = json.load(open(p, encoding="utf-8"))
    for v in cfg:
        r = yt(["--skip-download", "-J", f"https://www.youtube.com/watch?v={v['video_id']}"])
        if r.returncode != 0:
            print("  meta failed:", v["slug"])
            continue
        try:
            m = json.loads(r.stdout)
        except Exception:
            continue
        v["title"] = m.get("title") or v.get("title", "unknown")
        v["channel"] = m.get("channel") or m.get("uploader") or v.get("channel", "unknown")
        v["upload_date"] = m.get("upload_date") or v.get("upload_date", "unknown")
        v["duration_s"] = m.get("duration")
        print(f"  {v['slug']}: {v['duration_s']}s {v['upload_date']} {v['channel']}")
    json.dump(cfg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def cmd_discover(case, queries):
    out = []
    for q in queries:
        r = yt(["--skip-download", "--flat-playlist", "-J", f"ytsearch10:{q}"])
        if r.returncode != 0:
            print("  search failed:", q, r.stderr.strip()[:200])
            continue
        try:
            data = json.loads(r.stdout)
        except Exception:
            continue
        for e in data.get("entries") or []:
            dur = e.get("duration") or 0
            if dur and (dur < 45 or dur > 5400):
                continue
            out.append({"query": q, "video_id": e.get("id"), "title": e.get("title"),
                        "duration": dur, "channel": e.get("channel") or e.get("uploader")})
    seen, uniq = set(), []
    for e in out:
        if e["video_id"] and e["video_id"] not in seen:
            seen.add(e["video_id"])
            uniq.append(e)
    d = ROOT / case / "_staging" / "vision"
    d.mkdir(parents=True, exist_ok=True)
    json.dump(uniq, open(d / "discovered.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    for e in uniq:
        print(f"  {e['video_id']}  {e['duration']:>5}s  {e['title'][:90]}")
    print(f"{case}: {len(uniq)} candidates -> {d / 'discovered.json'}")


def cmd_download(case, only=None, limit=None):
    cfg = load_cfg(case)
    raw = ROOT / case / "_staging" / "vision" / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    todo = [v for v in cfg if not (raw / v["file"]).exists() and (not only or v["slug"] in only)]
    if limit:
        todo = todo[:limit]
    if not todo:
        print(f"{case}: all videos present")
        return 0
    failed = []
    for v in todo:
        print(f"-> {v['slug']} {v['video_id']}", flush=True)
        args = ["-f", "18/b[height<=480][ext=mp4]/b[height<=480]/b",
                "--merge-output-format", "mp4", "--no-playlist",
                "--retries", "3", "--fragment-retries", "3",
                "--extractor-args", "youtube:player_client=android,ios,tv,web",
                "-o", str(raw / f"{v['slug']}_%(id)s.%(ext)s")]
        dur = v.get("duration_s") or 0
        if dur and dur > 1200:
            v["excerpt"] = "full upload (360p)"
            print("   (long video: full 360p upload)")
        r = subprocess.run([sys.executable, "-m", "yt_dlp", "--no-warnings"] + args
                           + [f"https://www.youtube.com/watch?v={v['video_id']}"])
        if r.returncode != 0 or not (raw / v["file"]).exists():
            failed.append(v["slug"])
            print("   FAILED", v["slug"])
    json.dump(cfg, open(ROOT / case / "_staging" / "vision" / "videos.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"{case}: downloaded {len(todo) - len(failed)}/{len(todo)}; failed: {failed or 'none'}")
    return 1 if failed else 0


def prepare(img):
    """Upscale small frames: podium faces at 960 px are often below YuNet's comfortable size."""
    if img.shape[1] < 1600:
        return cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    return img


def detect_faces(img, det):
    h, w = img.shape[:2]
    det.setInputSize((w, h))
    _, faces = det.detect(img)
    out = []
    if faces is None:
        return out
    for f in faces:
        if float(f[-1]) < DET_CONF:
            continue
        x, y, bw, bh = [int(v) for v in f[:4]]
        out.append((x, y, bw, bh, f))
    return out


def cmd_frames(case, only=None):
    cfg = load_cfg(case)
    raw = ROOT / case / "_staging" / "vision" / "raw"
    dest = ROOT / case / "10_video_frames"
    kf = dest / "keyframes"
    rows, sumrows, srcrows = [], [], []
    pattern = re.compile(r"pts_time:([0-9.]+)")
    for v in cfg:
        if only and v["slug"] not in only:
            continue
        path = raw / v["file"]
        if not path.exists():
            print(f"  skip {v['slug']}: no file")
            continue
        outdir = kf / v["slug"]
        if outdir.exists():
            shutil.rmtree(outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        cmd = ["ffmpeg", "-hide_banner", "-i", str(path),
               "-vf", f"select='gt(scene,{SCENE_THRESHOLD})',showinfo,scale={FRAME_WIDTH}:-2",
               "-vsync", "vfr", "-frames:v", str(MAX_FRAMES), "-q:v", "3",
               str(outdir / "%03d.jpg")]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        dur = 0.0
        m = re.search(r"Duration: (\d+):(\d+):(\d+)", r.stderr or "")
        if m:
            dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        files = sorted(f for f in os.listdir(outdir) if f.endswith(".jpg"))
        sampled = False
        if len(files) < 6 and dur > 20:
            # Static-camera rallies and single-shot speeches yield almost no scene cuts.
            # Fall back to evenly spaced samples so the video still has visual coverage.
            sampled = True
            interval = max(8.0, dur / 12.0)
            for f in list(outdir.glob("*.jpg")):
                f.unlink()
            cmd = ["ffmpeg", "-hide_banner", "-i", str(path),
                   "-vf", f"fps=1/{interval:.3f},showinfo,scale={FRAME_WIDTH}:-2",
                   "-frames:v", "12", "-q:v", "3", str(outdir / "%03d.jpg")]
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
            files = sorted(f for f in os.listdir(outdir) if f.endswith(".jpg"))
        times = [float(x) for x in pattern.findall(r.stderr or "")]
        faces_per_video, largest = [], []
        for i, fname in enumerate(files):
            img = cv2.imread(str(outdir / fname))
            if img is None:
                continue
            h, w = img.shape[:2]
            boxes = detect_faces(img, DET)
            area = 0.0
            box_str = "unknown"
            if boxes:
                area = max((bw * bh) / float(w * h) * 100.0 for (_, _, bw, bh, _) in boxes)
                box_str = ";".join(f"{x},{y},{bw},{bh}" for (x, y, bw, bh, _) in boxes[:6])
            faces_per_video.append(len(boxes))
            largest.append(area)
            ts = times[i] if i < len(times) else None
            rows.append({
                "frame_id": f"{v['slug']}-KF-{i + 1:03d}",
                "video_id": v["video_id"], "slug": v["slug"],
                "candidate_source": v["candidate_source"], "kind": v["kind"],
                "timestamp_s": f"{ts:.1f}" if ts is not None else "unknown",
                "timecode": timecode(ts),
                "scene_score": f"{SCENE_THRESHOLD:.2f}",
                "file": f"keyframes/{v['slug']}/{fname}",
                "width": w, "height": h,
                "faces_detected": len(boxes),
                "largest_face_area_pct": f"{area:.1f}" if boxes else "0.0",
                "face_boxes": box_str,
                "caption": "unknown",
                "notes": ("evenly sampled frame (too few scene cuts)" if sampled
                          else "scene-change frame (threshold %.2f); no captioning pass" % SCENE_THRESHOLD),
            })
        sumrows.append({
            "video_id": v["video_id"], "slug": v["slug"],
            "candidate_source": v["candidate_source"], "kind": v["kind"],
            "frames_extracted": len(files),
            "frames_with_face": sum(1 for n in faces_per_video if n),
            "max_faces": max(faces_per_video) if faces_per_video else 0,
            "mean_largest_face_pct": f"{np.mean(largest):.1f}" if largest else "0.0",
            "duration_s": f"{dur:.0f}" if dur else "unknown",
            "notes": "YuNet detection at confidence %.1f" % DET_CONF,
        })
        srcrows.append({
            "video_id": v["video_id"], "slug": v["slug"],
            "candidate_source": v["candidate_source"], "kind": v["kind"],
            "title": v.get("title", "unknown"), "channel": v.get("channel", "unknown"),
            "upload_date": v.get("upload_date", "unknown"),
            "duration_s": f"{dur:.0f}" if dur else "unknown",
            "url": f"https://www.youtube.com/watch?v={v['video_id']}",
            "local_file": v["file"], "bytes": path.stat().st_size,
        })
        print(f"  {v['slug']}: {len(files)} frames, {sum(1 for n in faces_per_video if n)} with faces")
    write_rows(str(dest / "keyframes.csv"), KF_HEADER, rows)
    write_rows(str(dest / "video_face_summary.csv"), SUM_HEADER, sumrows)
    write_rows(str(dest / "video_sources.csv"), SRC_HEADER, srcrows)
    print(f"{case}: {len(rows)} keyframes -> {dest}")


def candidate_prefix(cand):
    return cand.lower()


def load_refs(case):
    """Licensed portraits already stored in the case, with a detected face."""
    arch = ROOT / case / "04_visual_archive"
    rows = read_rows(str(arch / "image_archive.csv"))
    refs = {}
    for r in rows:
        fn = r.get("local_filename", "unknown")
        if fn in ("unknown", "", "n/a"):
            continue
        p = ROOT / case / fn
        if not p.exists():
            p = arch / fn
        if not p.exists():
            continue
        img = cv2.imread(str(p))
        if img is None:
            continue
        boxes = detect_faces(img, DET)
        if not boxes:
            continue
        x, y, w, h, f = max(boxes, key=lambda b: b[2] * b[3])
        aligned = REC.alignCrop(img, f)
        feat = REC.feature(aligned).flatten().astype(np.float64)
        feat /= (np.linalg.norm(feat) + 1e-9)
        refs.setdefault(r["candidate_id"], []).append((feat, r.get("image_id")))
    return refs


def cmd_faces(case, only=None):
    cfg = {v["slug"]: v for v in load_cfg(case)}
    dest = ROOT / case / "10_video_frames"
    kf_rows = read_rows(str(dest / "keyframes.csv"))
    refs = load_refs(case)
    print(f"{case}: references " + ", ".join(f"{k}={len(v)}" for k, v in refs.items()))
    ids = [k for k in refs if refs[k]]
    if not ids:
        raise SystemExit("no usable reference portraits")
    refmat = {k: np.array([e for e, _ in refs[k]]) for k in ids}
    out = []
    by_slug = {}
    for r in kf_rows:
        if only and r["slug"] not in only:
            continue
        img = cv2.imread(str(dest / r["file"]))
        if img is None:
            continue
        img = prepare(img)
        boxes = detect_faces(img, DET)
        best_label, best_sim, second_label, second_sim = "unknown", 0.0, "unknown", 0.0
        cand_faces = 0
        for (x, y, w, h, f) in boxes:
            aligned = REC.alignCrop(img, f)
            feat = REC.feature(aligned).flatten().astype(np.float64)
            feat /= (np.linalg.norm(feat) + 1e-9)
            scored = sorted(((float(np.dot(feat, e)), k) for k in ids for e in refmat[k]),
                            reverse=True)
            top = scored[0]
            second = next((s for s in scored if s[1] != top[1]), (0.0, "unknown"))
            if top[0] > best_sim:
                best_sim, best_label = top[0], top[1]
                second_sim, second_label = second[0], second[1]
            if top[0] >= SIM_THRESHOLD and top[0] - second[0] >= MARGIN:
                cand_faces += 1
        if best_sim >= SIM_THRESHOLD and best_sim - second_sim >= MARGIN:
            note = "best SFace match clears threshold %.3f and margin %.2f" % (SIM_THRESHOLD, MARGIN)
        elif boxes:
            note = "face present but no candidate reference clears threshold/margin"
            best_label = "unknown"
        else:
            note = "no face detected"
            best_label = "unknown"
        out.append({
            "frame_id": r["frame_id"], "identity": best_label,
            "identity_sim": f"{best_sim:.3f}", "second_identity": second_label,
            "second_sim": f"{second_sim:.3f}", "faces": r["faces_detected"],
            "candidate_faces": cand_faces, "identity_note": note,
        })
        by_slug.setdefault(r["slug"], []).append(best_label)
    write_rows(str(dest / "keyframes_identity.csv"), ID_HEADER, out)
    print(f"{case}: {len(out)} identity rows")
    for slug, labels in by_slug.items():
        n = sum(1 for x in labels if x != "unknown")
        print(f"   {slug}: {n}/{len(labels)} frames attributed")


def cmd_report(case):
    dest = ROOT / case / "10_video_frames"
    kf = read_rows(str(dest / "keyframes.csv"))
    ident = {r["frame_id"]: r for r in read_rows(str(dest / "keyframes_identity.csv"))}
    from collections import Counter
    c = Counter(ident[f["frame_id"]]["identity"] for f in kf if f["frame_id"] in ident)
    print(f"{case}: {len(kf)} frames; identities {dict(c)}")


DET = REC = None


def main(argv):
    global DET, REC
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["discover", "meta", "download", "frames", "faces", "report"])
    ap.add_argument("case")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--query", nargs="*")
    args = ap.parse_args(argv)
    if args.stage in ("frames", "faces"):
        DET = cv2.FaceDetectorYN.create(str(MODELS / "yunet.onnx"), "", (640, 640), DET_CONF, 0.3, 200)
        REC = cv2.FaceRecognizerSF.create(str(MODELS / "sface.onnx"), "")
    if args.stage == "discover":
        cmd_discover(args.case, args.query or [])
    elif args.stage == "meta":
        cmd_meta(args.case)
    elif args.stage == "download":
        return cmd_download(args.case, args.only, args.limit)
    elif args.stage == "frames":
        cmd_frames(args.case, args.only)
    elif args.stage == "faces":
        cmd_faces(args.case, args.only)
    elif args.stage == "report":
        cmd_report(args.case)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
