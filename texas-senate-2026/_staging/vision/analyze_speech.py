#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extract speech audio and measure delivery for every downloaded video.

For each video in videos.json this script

  1. decodes the audio track to 16 kHz mono PCM (ffmpeg),
  2. runs an energy VAD and measures silence/pause structure, loudness dynamics,
     spectral centroid and an autocorrelation F0 track,
  3. parses the English captions yt-dlp saved (auto or manual) to get word counts,
     words-per-minute and a timed transcript,
  4. writes per-60 s segments so pacing over a speech can be read, and
  5. keeps a 64 kbps mono AAC copy of the audio for speech-type videos.

Deliverables go to texas-senate-2026/11_speech_audio/:
    delivery_metrics.csv, speech_segments.csv, transcript_index.csv,
    transcripts/<slug>.txt|.cues.csv, plots/<slug>.png, audio/<slug>.m4a

Rights: audio is cut from YouTube uploads owned by the campaigns / stations.
Internal analysis only; not licensed for republication.

    python texas-senate-2026/_staging/vision/analyze_speech.py --only speech
    python texas-senate-2026/_staging/vision/analyze_speech.py --only all --skip-plots
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
VISION = ROOT / "_staging" / "vision"
RAW = VISION / "raw"
CONFIG = VISION / "videos.json"
DEST = ROOT / "11_speech_audio"
CACHE = VISION / "audio_cache"

SR = 16000
FRAME_MS, HOP_MS = 25, 10
PITCH_WIN_MS, PITCH_HOP_MS = 40, 20
SPEECH_KINDS = {"rally_speech", "victory_speech", "concession_speech", "convention_speech",
                "town_hall", "debate", "interview", "final_rally", "tour_launch"}
STOP = set("""a an the and or but if then than that this these those of to in on at for with from by
as is are was were be been being it its it's i i'm i've you you're we we're they they're he she his her
them our your my me us do does did not no so up out about into over after before what who which when where
why how all any some more most other such only also just very can could would should will shall may might
have has had there here their theirs one two three get got go going been am """.split())


# ---------------------------------------------------------------- audio utils
def ffmpeg_wav(mp4, wav_path):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(mp4),
           "-vn", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(wav_path)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or not wav_path.exists() or wav_path.stat().st_size < 1000:
        return False
    return True


def ffmpeg_m4a(mp4, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(mp4),
           "-vn", "-ac", "1", "-ar", "32000", "-c:a", "aac", "-b:a", "64k", str(out_path)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode == 0 and out_path.exists()


def read_wav(path):
    with wave.open(str(path), "rb") as w:
        n = w.getnframes()
        data = w.readframes(n)
    a = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
    return a


def frames(y, frame, hop):
    """Yield overlapping frames as a 2-D array (n_frames, frame)."""
    if len(y) < frame:
        return np.zeros((0, frame), dtype=np.float32)
    n = 1 + (len(y) - frame) // hop
    idx = np.arange(frame)[None, :] + hop * np.arange(n)[:, None]
    return y[idx]


def rms_db(y, hop=HOP_MS * SR // 1000, frame=FRAME_MS * SR // 1000, chunk_s=60):
    out = []
    step = chunk_s * SR
    for start in range(0, len(y), step):
        seg = y[start:start + step + frame]
        fr = frames(seg, frame, hop)
        if len(fr) == 0:
            continue
        e = np.sqrt(np.mean(fr.astype(np.float32) ** 2, axis=1) + 1e-12)
        out.append(20 * np.log10(e + 1e-9))
    return np.concatenate(out) if out else np.array([])


def spectral_centroid(y, hop=HOP_MS * SR // 1000, frame=FRAME_MS * SR // 1000, chunk_s=60):
    out = []
    step = chunk_s * SR
    win = np.hanning(frame).astype(np.float32)
    freqs = np.fft.rfftfreq(frame, 1.0 / SR).astype(np.float32)
    for start in range(0, len(y), step):
        seg = y[start:start + step + frame]
        fr = frames(seg, frame, hop)
        if len(fr) == 0:
            continue
        spec = np.abs(np.fft.rfft(fr * win, axis=1)) + 1e-9
        out.append((spec * freqs).sum(axis=1) / spec.sum(axis=1))
    return np.concatenate(out) if out else np.array([])


def vad_mask(db, noise_floor, speech_thr):
    m = db > speech_thr
    return m


def close_gaps(mask, hop_s, max_gap_s):
    """Fill silence gaps shorter than max_gap_s inside speech runs."""
    if not mask.any():
        return mask
    gap = int(max_gap_s / hop_s)
    m = mask.copy()
    idx = np.where(m)[0]
    if len(idx) < 2:
        return m
    for a, b in zip(idx[:-1], idx[1:]):
        if 1 < b - a <= gap:
            m[a + 1:b] = True
    return m


def drop_short(mask, hop_s, min_run_s):
    m = mask.copy()
    run = int(min_run_s / hop_s)
    i = 0
    n = len(m)
    while i < n:
        if m[i]:
            j = i
            while j < n and m[j]:
                j += 1
            if j - i < run:
                m[i:j] = False
            i = j
        else:
            i += 1
    return m


def f0_track(y, speech_mask_for_db=None):
    """Autocorrelation F0 on 40 ms windows, 20 ms hop. Returns (t, f0, voiced)."""
    frame = PITCH_WIN_MS * SR // 1000
    hop = PITCH_HOP_MS * SR // 1000
    fr = frames(y, frame, hop)
    if len(fr) == 0:
        return np.array([]), np.array([]), np.array([])
    out = []
    fmin, fmax = 55.0, 400.0
    lag_min, lag_max = int(SR / fmax), int(SR / fmin)
    chunk = 20000
    win = np.hanning(frame).astype(np.float32)
    f0s, confs = [], []
    for s in range(0, len(fr), chunk):
        blk = fr[s:s + chunk] * win
        n = frame
        spec = np.fft.rfft(blk, 2 * n, axis=1)
        ac = np.fft.irfft(np.abs(spec) ** 2, axis=1)[:, :n]
        ac0 = ac[:, 0:1] + 1e-9
        acn = ac / ac0
        seg = acn[:, lag_min:lag_max]
        gmax = seg.max(axis=1, keepdims=True)
        # first lag whose correlation is close to the frame maximum: harmonic peaks at
        # 2T, 3T... are as strong as T, so the *smallest* strong lag is the fundamental.
        above = seg >= 0.85 * gmax
        best = np.argmax(above, axis=1)
        peak = seg[np.arange(len(seg)), best]
        f0 = SR / (best + lag_min).astype(np.float32)
        f0s.append(f0)
        confs.append(peak)
    f0 = np.concatenate(f0s)
    conf = np.concatenate(confs)
    voiced = (conf > 0.42) & (f0 > fmin) & (f0 < fmax)
    # median filter the voiced track to remove single-frame octave jumps
    f0v = f0.copy()
    f0v[~voiced] = np.nan
    if len(f0v) > 5:
        pad = np.pad(f0v, 2, mode="edge")
        med = np.array([np.nanmedian(pad[i:i + 5]) for i in range(len(f0v))])
        f0v = np.where(voiced & np.isfinite(med), med, np.nan)
    t = np.arange(len(f0)) * hop / SR
    return t, f0v, voiced


def pct(a, p):
    a = a[np.isfinite(a)]
    return float(np.percentile(a, p)) if len(a) else float("nan")


def append_csv(path, rows):
    """Append rows to a CSV, merging headers if a later run adds a column."""
    if not path.exists() or path.stat().st_size == 0:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        return
    with open(path, newline="", encoding="utf-8") as f:
        old = list(csv.DictReader(f))
    fields = list(old[0].keys()) if old else list(rows[0].keys())
    for r in rows:
        for k in r:
            if k not in fields:
                fields.append(k)
    for r in old:
        for k in fields:
            r.setdefault(k, "")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(old + rows)


# ---------------------------------------------------------------- captions
def find_vtt(slug, vid):
    hits = sorted(RAW.glob(f"{slug}_{vid}*.vtt"))
    return hits


def parse_vtt(path):
    """Return cues [(start_s, end_s, text)] from a WebVTT file, rolling dupes removed."""
    txt = path.read_text(encoding="utf-8", errors="replace")
    lines = txt.splitlines()
    cues, last_line = [], ""
    i = 0
    ts_re = re.compile(r"(\d+):(\d+):(\d+)[.,](\d+)\s*-->\s*(\d+):(\d+):(\d+)[.,](\d+)")
    while i < len(lines):
        m = ts_re.search(lines[i])
        if m:
            h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, m.groups())
            start = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000.0
            end = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000.0
            i += 1
            buf = []
            while i < len(lines) and lines[i].strip() and not ts_re.search(lines[i]):
                buf.append(lines[i].strip())
                i += 1
            text = " ".join(buf)
            text = re.sub(r"<[^>]+>", "", text)
            text = (text.replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<")
                        .replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " "))
            text = re.sub(r"\s+", " ", text).strip()
            if not text or text == last_line:
                continue
            # rolling captions repeat the previous line inside the new cue
            if last_line and text.startswith(last_line):
                text = text[len(last_line):].strip()
                if not text:
                    continue
            last_line = text
            cues.append((round(start, 2), round(end, 2), text))
        else:
            i += 1
    return cues


def words_of(text):
    return re.findall(r"[A-Za-z']+", text)


def analyse_captions(cues):
    if not cues:
        return {}
    text = " ".join(c[2] for c in cues)
    ws = words_of(text)
    span = max(c[1] for c in cues) - min(c[0] for c in cues)
    low = [w.lower() for w in ws]
    content = [w for w in low if w not in STOP and len(w) > 2]
    from collections import Counter
    top = Counter(content).most_common(12)
    sents = [s for s in re.split(r"[.!?]+", text) if len(s.strip()) > 3]
    return dict(
        transcript=text, cues=cues, words=len(ws),
        uniq_word_ratio=round(len(set(low)) / max(1, len(low)), 3),
        caption_span_s=round(span, 1),
        mean_sentence_words=round(np.mean([len(words_of(s)) for s in sents]), 1) if sents else float("nan"),
        pron_i=sum(1 for w in low if w == "i"),
        pron_we=sum(1 for w in low if w in ("we", "our", "us")),
        pron_you=sum(1 for w in low if w in ("you", "your")),
        pron_they=sum(1 for w in low if w in ("they", "them", "their")),
        mentions_texas=sum(1 for w in low if w == "texas"),
        mentions_talarico=sum(1 for w in low if w == "talarico"),
        mentions_paxton=sum(1 for w in low if w == "paxton"),
        top_words="; ".join(f"{w}:{c}" for w, c in top),
    )


# ---------------------------------------------------------------- plot
def make_plot(slug, title, t_db, db, mask, t_f0, f0, cues, out_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(4, 1, figsize=(11, 7.2), sharex=True,
                             gridspec_kw={"height_ratios": [1.2, 1.0, 1.0, 0.6]})
    hop_s_db = len(t_db) and (t_db[-1] / max(1, len(t_db) - 1)) or 0.01
    axes[0].plot(t_db, db, lw=0.35, color="#3b6ea5")
    axes[0].fill_between(t_db, -80, db, where=mask, color="#c9a227", alpha=0.28,
                         linewidth=0, label="speech (VAD)")
    axes[0].set_ylim(-80, max(0, np.nanmax(db) + 3))
    axes[0].set_ylabel("dBFS")
    axes[0].legend(loc="upper right", fontsize=7)
    axes[1].plot(t_f0, f0, lw=0.5, color="#984ea3")
    axes[1].set_ylabel("F0 (Hz)")
    axes[1].set_ylim(60, 330)
    if len(cues):
        for s, e, _ in cues:
            axes[2].axvspan(s, e, color="#4daf4a", alpha=0.25, linewidth=0)
    axes[2].set_ylabel("caption cue")
    if len(cues):
        cs = np.array([(c[0] + c[1]) / 2 for c in cues])
        wc = np.array([len(words_of(c[2])) for c in cues])
        bins = np.arange(0, max(cs[-1], 1) + 30, 30)
        idx = np.digitize(cs, bins) - 1
        dens = np.zeros(len(bins) - 1)
        for i in range(len(bins) - 1):
            sel = idx == i
            if sel.any():
                dens[i] = wc[sel].sum() / 0.5  # words per minute in the 30 s bin
        axes[3].bar((bins[:-1] + bins[1:]) / 2, dens, width=28, color="#e41a1c")
    axes[3].set_ylabel("wpm / 30s")
    axes[3].set_xlabel("seconds")
    fig.suptitle(f"{slug} — {title[:90]}", fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=110)
    plt.close(fig)


# ---------------------------------------------------------------- main
def process(v, args):
    mp4 = RAW / v["file"]
    if not mp4.exists():
        return None
    CACHE.mkdir(parents=True, exist_ok=True)
    wav = CACHE / f"{v['slug']}.wav"
    if not ffmpeg_wav(mp4, wav):
        return dict(slug=v["slug"], video_id=v["video_id"], audio="none")
    y = read_wav(wav)
    dur = len(y) / SR
    if dur < 1.0:
        wav.unlink(missing_ok=True)
        return dict(slug=v["slug"], video_id=v["video_id"], audio="too_short", duration_s=round(dur, 1))

    hop_s = HOP_MS / 1000.0
    db = rms_db(y)
    t_db = np.arange(len(db)) * hop_s
    noise = pct(db, 10)
    peak = pct(db, 95)
    thr = max(noise + 9.0, min(peak - 6.0, -32.0))
    mask = vad_mask(db, noise, thr)
    mask = close_gaps(mask, hop_s, 0.18)
    mask = drop_short(mask, hop_s, 0.12)
    if not mask.any():
        thr = noise + 5
        mask = vad_mask(db, noise, thr)
    speech_s = float(mask.sum() * hop_s)
    idx = np.where(mask)[0]
    first, last = (idx[0], idx[-1]) if len(idx) else (0, 0)

    # pause structure inside the speaking span
    pauses = []
    if len(idx):
        run_start = None
        for i in range(first, last + 1):
            if not mask[i] and run_start is None:
                run_start = i
            elif mask[i] and run_start is not None:
                pauses.append((i - run_start) * hop_s)
                run_start = None
    pauses = [p for p in pauses if p >= 0.25]

    speech_db = db[mask] if mask.any() else db
    spec = spectral_centroid(y)
    ms = mask[:min(len(mask), len(spec))]
    cent = float(np.mean(spec[:len(ms)][ms])) if len(ms) and ms.any() else float("nan")

    t_f0, f0, voiced = f0_track(y)
    f0v = f0[np.isfinite(f0)]
    # restrict pitch statistics to frames where VAD also heard speech
    if len(f0v) and mask.any():
        vi = np.clip((t_f0 / hop_s).astype(int), 0, len(mask) - 1)
        sel = np.isfinite(f0) & mask[vi]
        f0v = f0[sel]
    f0_med, f0_lo, f0_hi = pct(f0v, 50), pct(f0v, 10), pct(f0v, 90)
    semi = 12 * np.log2(f0_hi / f0_lo) if f0_lo and f0_hi and f0_lo > 0 and f0_hi > 0 else float("nan")

    caps = {}
    vt = find_vtt(v["slug"], v["video_id"])
    if vt:
        cues = parse_vtt(vt[0])
        caps = analyse_captions(cues)
        if caps:
            (args.cues_dir).mkdir(parents=True, exist_ok=True)
            with open(args.cues_dir / f"{v['slug']}.cues.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["start_s", "end_s", "text"])
                w.writerows(cues)
            (args.txt_dir / f"{v['slug']}.txt").write_text(
                f"{caps['transcript']}\n", encoding="utf-8")

    words = caps.get("words", 0)
    wpm_span = 60 * words / caps["caption_span_s"] if caps.get("caption_span_s") else float("nan")
    art_wpm = 60 * words / speech_s if speech_s > 0 and words else float("nan")

    row = dict(
        slug=v["slug"], video_id=v["video_id"], candidate=v["candidate_source"],
        kind=v["kind"], channel=v["channel"], upload_date=v.get("upload_date", ""),
        video_duration_s=round(dur, 1),
        audio="ok",
        speech_s=round(speech_s, 1),
        speech_ratio=round(speech_s / dur, 3) if dur else float("nan"),
        silence_s=round(dur - speech_s, 1),
        pause_count=len(pauses),
        pause_mean_s=round(float(np.mean(pauses)), 2) if pauses else 0.0,
        pause_max_s=round(float(np.max(pauses)), 2) if pauses else 0.0,
        pauses_per_min=round(len(pauses) / (speech_s / 60), 2) if speech_s > 30 else float("nan"),
        noise_floor_db=round(noise, 1),
        speech_db_mean=round(float(np.mean(speech_db)), 1),
        speech_db_std=round(float(np.std(speech_db)), 1),
        speech_db_p10=round(pct(speech_db, 10), 1),
        speech_db_p90=round(pct(speech_db, 90), 1),
        f0_median_hz=round(f0_med, 1) if np.isfinite(f0_med) else "",
        f0_p10_hz=round(f0_lo, 1) if np.isfinite(f0_lo) else "",
        f0_p90_hz=round(f0_hi, 1) if np.isfinite(f0_hi) else "",
        f0_range_semitones=round(float(semi), 2) if np.isfinite(semi) else "",
        voiced_ratio=round(float(np.isfinite(f0).mean()), 3),
        spectral_centroid_hz=round(cent, 0) if np.isfinite(cent) else "",
        caption_source=vt[0].name if vt else "",
        words=words,
        wpm=round(wpm_span, 0) if np.isfinite(wpm_span) else "",
        articulation_wpm=round(art_wpm, 0) if np.isfinite(art_wpm) else "",
        uniq_word_ratio=caps.get("uniq_word_ratio", ""),
        mean_sentence_words=caps.get("mean_sentence_words", ""),
        pron_i=caps.get("pron_i", ""), pron_we=caps.get("pron_we", ""),
        pron_you=caps.get("pron_you", ""), pron_they=caps.get("pron_they", ""),
        mentions_texas=caps.get("mentions_texas", ""),
        mentions_talarico=caps.get("mentions_talarico", ""),
        mentions_paxton=caps.get("mentions_paxton", ""),
        top_words=caps.get("top_words", ""),
    )

    # 60 s segments: pacing arc
    segs = []
    if len(db):
        for k in range(0, int(np.ceil(dur / 60)), 1):
            a, b = k * 60, min((k + 1) * 60, dur)
            ia, ib = int(a / hop_s), int(min(b / hop_s, len(db)))
            if ib <= ia:
                continue
            m = mask[ia:ib]
            d = db[ia:ib]
            sel = (t_f0 >= a) & (t_f0 < b) if len(t_f0) else np.zeros(0, bool)
            f0s = f0[sel] if len(t_f0) else np.array([])
            f0s = f0s[np.isfinite(f0s)]
            w_in = 0
            if caps.get("cues"):
                w_in = sum(len(words_of(c[2])) for c in caps["cues"] if a <= c[0] < b)
            segs.append(dict(slug=v["slug"], segment=k, start_s=a, end_s=round(b, 1),
                             speech_ratio=round(float(m.mean()), 3),
                             db_mean=round(float(np.mean(d)), 1),
                             f0_median_hz=round(float(np.median(f0s)), 1) if len(f0s) else "",
                             words=w_in,
                             wpm=round(w_in / ((b - a) / 60), 0) if b > a else ""))

    if v["kind"] in SPEECH_KINDS and dur >= 45:
        out = DEST / "audio" / f"{v['slug']}.m4a"
        if not out.exists():
            ffmpeg_m4a(mp4, out)
        if not args.skip_plots:
            make_plot(v["slug"], v["title"], t_db, db, mask, t_f0, f0,
                      caps.get("cues", []), DEST / "plots" / f"{v['slug']}.png")

    wav.unlink(missing_ok=True)
    return dict(row=row, segments=segs, cues=bool(caps.get("cues")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["all", "speech", "missing"], default="all",
                    help="speech = speech-type kinds only; missing = no metrics row yet")
    ap.add_argument("--skip-plots", action="store_true")
    ap.add_argument("--slugs", default="", help="comma-separated subset (debugging)")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    DEST.mkdir(parents=True, exist_ok=True)
    for sub in ("plots", "audio", "transcripts"):
        (DEST / sub).mkdir(exist_ok=True)
    args.txt_dir = DEST / "transcripts"
    args.cues_dir = DEST / "transcripts"

    metrics_path = DEST / "delivery_metrics.csv"
    done = set()
    if args.only == "missing" and metrics_path.exists():
        done = {r["slug"] for r in csv.DictReader(open(metrics_path, encoding="utf-8"))}

    todo = []
    for v in cfg:
        if not (RAW / v["file"]).exists():
            continue
        if args.only == "speech" and v["kind"] not in SPEECH_KINDS:
            continue
        if v["slug"] in done:
            continue
        todo.append(v)
    if args.slugs:
        want = {s.strip() for s in args.slugs.split(",") if s.strip()}
        todo = [v for v in todo if v["slug"] in want]
    if args.limit:
        todo = todo[:args.limit]

    print(f"{len(todo)} videos to analyse ({args.only})", flush=True)
    rows, segs = [], []
    for i, v in enumerate(todo, 1):
        try:
            r = process(v, args)
        except Exception as e:  # noqa: BLE001
            print(f"[{i}/{len(todo)}] {v['slug']:32s} ERROR {e}", flush=True)
            continue
        if not r:
            print(f"[{i}/{len(todo)}] {v['slug']:32s} missing file", flush=True)
            continue
        if "row" in r:
            rows.append(r["row"])
            segs += r["segments"]
            print(f"[{i}/{len(todo)}] {v['slug']:32s} speech={r['row']['speech_ratio']:.2f} "
                  f"f0={r['row']['f0_median_hz']} wpm={r['row']['wpm']}", flush=True)
        else:
            print(f"[{i}/{len(todo)}] {v['slug']:32s} audio={r.get('audio')}", flush=True)

    if rows:
        append_csv(metrics_path, rows)
    seg_path = DEST / "speech_segments.csv"
    if segs:
        append_csv(seg_path, segs)
    print(f"wrote {len(rows)} metric rows, {len(segs)} segments")
    return 0


if __name__ == "__main__":
    sys.exit(main())
