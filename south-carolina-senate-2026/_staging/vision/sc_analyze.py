#!/usr/bin/env python3
"""Frame, face and audio analysis for the downloaded corpus.

Everything produced here is measurable from the files themselves: scene-change positions, face
counts and boxes, loudness and silence, caption-derived word counts. Nothing is interpreted 鈥?the interpretation lives in the Markdown analyses, so this stage stays reproducible.

Outputs
  10_video_frames/keyframes.csv            one row per extracted keyframe
  10_video_frames/video_face_summary.csv   one row per video
  10_video_frames/keyframes/<slug>/*.jpg
  11_speech_audio/audio_metrics.csv        one row per video
  11_speech_audio/transcripts/<slug>.{vtt,txt}

Captions are YouTube's own (auto-generated where human captions are absent); their presence and
quality are recorded rather than assumed, because a machine transcript is not a transcript of
record.

Run: python _staging/vision/sc_analyze.py [--only SLUG] [--limit N]
"""
import csv
import json
import os
import re
import subprocess
import sys
import wave

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KF = os.path.join(ROOT, "10_video_frames")
AUD = os.path.join(ROOT, "11_speech_audio")
RAW = os.path.join(HERE, "raw")
CONF = os.path.join(HERE, "videos.json")

KF_HEADER = ["frame_id", "video_id", "slug", "candidate_source", "kind", "timestamp_s", "timecode",
             "scene_score", "file", "width", "height", "faces_detected", "largest_face_area_pct",
             "face_boxes", "caption", "notes"]
FACE_HEADER = ["video_id", "slug", "candidate_source", "kind", "frames_extracted",
               "frames_with_face", "max_faces", "mean_largest_face_pct", "duration_s", "notes"]
AUD_HEADER = ["video_id", "slug", "candidate_source", "kind", "duration_s", "mean_rms_dbfs",
              "silence_ratio", "loudest_second", "transcript_source", "transcript_words",
              "words_per_min", "transcript_file", "notes"]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def detect_faces(img, detector):
    """YuNet (OpenCV Zoo) face detection 鈥?this OpenCV build ships no Haar cascades."""
    h, w = img.shape[:2]
    detector.setInputSize((w, h))
    _, faces = detector.detect(img)
    if faces is None:
        return []
    boxes = []
    for f in faces:
        x, y, bw, bh = f[0], f[1], f[2], f[3]
        conf = float(f[-1])
        if conf < 0.6:
            continue
        boxes.append((int(x), int(y), int(bw), int(bh)))
    return boxes


def extract_keyframes(entry, cascade, limit_frames=22):
    slug = entry["slug"]
    path = os.path.join(RAW, entry["file"])
    outdir = os.path.join(KF, "keyframes", slug)
    os.makedirs(outdir, exist_ok=True)
    pattern = re.compile(r"pts_time:([0-9.]+)")
    cmd = ["ffmpeg", "-hide_banner", "-i", path,
           "-vf", f"select='gt(scene,0.30)',showinfo,scale=960:-2",
           "-vsync", "vfr", "-frames:v", str(limit_frames), "-q:v", "3",
           os.path.join(outdir, "%03d.jpg")]
    r = run(cmd)
    times = [float(x) for x in pattern.findall(r.stderr)]
    files = sorted(f for f in os.listdir(outdir) if f.endswith(".jpg"))
    rows = []
    for i, fname in enumerate(files):
        ts = times[i] if i < len(times) else None
        img = cv2.imread(os.path.join(outdir, fname))
        if img is None:
            continue
        h, w = img.shape[:2]
        boxes = detect_faces(img, cascade)
        largest = 0.0
        box_str = "unknown"
        if len(boxes):
            areas = [(bw * bh) / float(w * h) * 100.0 for (bx, by, bw, bh) in boxes]
            largest = float(np.max(areas))
            box_str = ";".join(f"{bx},{by},{bw},{bh}" for (bx, by, bw, bh) in boxes[:6])
        rows.append({
            "frame_id": f"{slug}-KF-{i + 1:03d}",
            "video_id": entry["video_id"],
            "slug": slug,
            "candidate_source": entry["candidate_source"],
            "kind": entry["kind"],
            "timestamp_s": f"{ts:.1f}" if ts is not None else "unknown",
            "timecode": timecode(ts) if ts is not None else "unknown",
            "scene_score": "unknown",
            "file": f"keyframes/{slug}/{fname}",
            "width": w, "height": h,
            "faces_detected": len(boxes),
            "largest_face_area_pct": f"{largest:.1f}" if len(boxes) else "0.0",
            "face_boxes": box_str,
            "caption": "unknown",
            "notes": "scene-change frame (threshold 0.30); no vision-model captioning in this pass",
        })
    return rows


def timecode(ts):
    if ts is None:
        return "unknown"
    m, s = divmod(ts, 60)
    h, m = divmod(int(m), 60)
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def audio_metrics(entry):
    slug = entry["slug"]
    path = os.path.join(RAW, entry["file"])
    wav = os.path.join(AUD, "audio_cache", f"{slug}.wav")
    os.makedirs(os.path.dirname(wav), exist_ok=True)
    if not os.path.exists(wav):
        r = run(["ffmpeg", "-hide_banner", "-y", "-i", path, "-ac", "1", "-ar", "16000",
                 "-vn", wav])
        if not os.path.exists(wav):
            return None, (r.stderr or "")[-200:]
    with wave.open(wav, "rb") as w:
        frames = w.getnframes()
        rate = w.getframerate()
        raw = w.readframes(frames)
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    dur = frames / float(rate)
    win = rate  # one-second windows
    n = len(samples) // win
    if n == 0:
        return None, "audio shorter than one second"
    rms = np.array([np.sqrt(np.mean(samples[i * win:(i + 1) * win] ** 2)) for i in range(n)])
    db = 20 * np.log10(np.maximum(rms, 1e-6))
    silence = float(np.mean(db < -45.0))
    loudest = int(np.argmax(db))
    return {
        "duration_s": f"{dur:.1f}",
        "mean_rms_dbfs": f"{float(np.mean(db)):.1f}",
        "silence_ratio": f"{silence:.3f}",
        "loudest_second": f"{loudest}",
    }, None


def captions(entry):
    slug = entry["slug"]
    vtt = os.path.join(AUD, "transcripts", f"{slug}.vtt")
    os.makedirs(os.path.dirname(vtt), exist_ok=True)
    if not os.path.exists(vtt):
        r = run([sys.executable, "-m", "yt_dlp", "--skip-download", "--write-auto-subs",
                 "--write-subs", "--sub-langs", "en.*,en", "--sub-format", "vtt",
                 "-o", os.path.join(AUD, "transcripts", f"{slug}.%(ext)s"),
                 f"https://www.youtube.com/watch?v={entry['video_id']}"])
        found = [f for f in os.listdir(os.path.dirname(vtt)) if f.startswith(slug) and
                 f.endswith(".vtt")]
        if found and not os.path.exists(vtt):
            os.replace(os.path.join(os.path.dirname(vtt), found[0]), vtt)
    if not os.path.exists(vtt):
        return "none", 0, "unknown", ""
    text = parse_vtt(vtt)
    words = len(re.findall(r"[A-Za-z']+", text))
    txt = os.path.join(AUD, "transcripts", f"{slug}.txt")
    with open(txt, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    dur = entry.get("duration") or 0
    wpm = f"{words / (dur / 60.0):.0f}" if dur else "unknown"
    source = "auto_generated" if "auto" in open(vtt, encoding="utf-8",
                                                errors="replace").read(400).lower() else "human_or_unknown"
    return source, words, wpm, text


def parse_vtt(path):
    out, last = [], None
    for line in open(path, encoding="utf-8", errors="replace"):
        s = line.strip()
        if not s or s.isdigit() or "-->" in s or s.startswith("WEBVTT") or s.startswith("Kind:") \
                or s.startswith("Language:"):
            continue
        s = re.sub(r"<[^>]+>", "", s)
        s = re.sub(r"&nbsp;", " ", s)
        if s == last:
            continue
        last = s
        out.append(s)
    return " ".join(out)


def main():
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    videos = json.load(open(CONF, encoding="utf-8"))
    if only:
        videos = [v for v in videos if v["slug"] == only]
    if limit:
        videos = videos[:limit]
    os.makedirs(KF, exist_ok=True)
    os.makedirs(AUD, exist_ok=True)
    models = os.path.join(HERE, "models")
    onnx = os.path.join(models, "face_detection_yunet_2023mar.onnx")
    if not os.path.exists(onnx):
        print(f"missing face model at {onnx}; run the fetch step first")
        return 1
    detector = cv2.FaceDetectorYN.create(onnx, "", (320, 320), 0.6, 0.3, 5000)

    kf_rows, face_rows, aud_rows = [], [], []
    for entry in videos:
        print(f"[{entry['slug']}] keyframes...", flush=True)
        try:
            rows = extract_keyframes(entry, detector)
        except Exception as exc:  # noqa: BLE001
            print(f"  frame stage failed: {type(exc).__name__}: {exc}")
            rows = []
        kf_rows += rows
        with_face = [r for r in rows if int(r["faces_detected"]) > 0]
        face_rows.append({
            "video_id": entry["video_id"], "slug": entry["slug"],
            "candidate_source": entry["candidate_source"], "kind": entry["kind"],
            "frames_extracted": len(rows), "frames_with_face": len(with_face),
            "max_faces": max([int(r["faces_detected"]) for r in rows], default=0),
            "mean_largest_face_pct": f"{np.mean([float(r['largest_face_area_pct']) for r in rows]):.1f}"
            if rows else "0.0",
            "duration_s": entry.get("duration", 0),
            "notes": "Haar frontal-face cascade on scene-change frames; profiles and rear views are "
                     "not detected, so counts are a lower bound",
        })
        print(f"[{entry['slug']}] audio...", flush=True)
        metrics, err = audio_metrics(entry)
        print(f"[{entry['slug']}] captions...", flush=True)
        source, words, wpm, _ = captions(entry)
        aud_rows.append({
            "video_id": entry["video_id"], "slug": entry["slug"],
            "candidate_source": entry["candidate_source"], "kind": entry["kind"],
            "duration_s": (metrics or {}).get("duration_s", entry.get("duration", 0)),
            "mean_rms_dbfs": (metrics or {}).get("mean_rms_dbfs", "unknown"),
            "silence_ratio": (metrics or {}).get("silence_ratio", "unknown"),
            "loudest_second": (metrics or {}).get("loudest_second", "unknown"),
            "transcript_source": source, "transcript_words": words,
            "words_per_min": wpm,
            "transcript_file": f"transcripts/{entry['slug']}.txt" if source != "none" else "unknown",
            "notes": err or "unknown",
        })

    write_csv(os.path.join(KF, "keyframes.csv"), KF_HEADER, kf_rows)
    write_csv(os.path.join(KF, "video_face_summary.csv"), FACE_HEADER, face_rows)
    write_csv(os.path.join(AUD, "audio_metrics.csv"), AUD_HEADER, aud_rows)
    print(f"keyframes: {len(kf_rows)} rows; videos: {len(face_rows)}; audio: {len(aud_rows)}")
    return 0


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "unknown") for k in header})


if __name__ == "__main__":
    sys.exit(main())

