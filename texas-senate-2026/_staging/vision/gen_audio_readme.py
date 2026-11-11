#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Aggregate the speech delivery measurements and regenerate 11_speech_audio/README.md.

Reads delivery_metrics.csv / speech_segments.csv / transcripts and writes:
    summary_by_candidate.json     medians per candidate over speech-type videos
    fig_delivery_comparison.png   four delivery measures, candidate vs candidate
    fig_pacing.png                words-per-minute vs pause rate per speech
    README.md                     bilingual documentation (EN + ZH)

Only speech-type videos enter the candidate comparison; news packages are excluded
because their audio is reporter narration, not the candidate speaking.

    python texas-senate-2026/_staging/vision/gen_audio_readme.py
"""
import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "11_speech_audio"
VISION = ROOT / "_staging" / "vision"

SPEECH_KINDS = {"rally_speech", "victory_speech", "concession_speech", "convention_speech",
                "town_hall", "interview", "final_rally", "tour_launch"}
PAIR_KINDS = {"rally_speech", "victory_speech", "concession_speech", "convention_speech",
              "town_hall", "interview"}


def rows(p):
    with open(p, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def num(r, k):
    try:
        v = float(r[k])
        return v if np.isfinite(v) else np.nan
    except (KeyError, TypeError, ValueError):
        return np.nan


def med(rs, k):
    a = [num(r, k) for r in rs]
    a = [x for x in a if np.isfinite(x)]
    return (float(np.median(a)), len(a)) if a else (np.nan, 0)


def main():
    m = rows(DEST / "delivery_metrics.csv")
    seg = rows(DEST / "speech_segments.csv")
    trans = sorted((DEST / "transcripts").glob("*.txt"))
    audio = sorted((DEST / "audio").glob("*.m4a"))
    plots = sorted((DEST / "plots").glob("*.png"))

    # one row per slug (re-runs append)
    by_slug = {}
    for r in m:
        by_slug[r["slug"]] = r
    m = list(by_slug.values())

    speech = [r for r in m if r["kind"] in SPEECH_KINDS]
    tal = [r for r in speech if r["candidate"] == "TALARICO" and r["kind"] in PAIR_KINDS]
    pax = [r for r in speech if r["candidate"] == "PAXTON" and r["kind"] in PAIR_KINDS]

    metrics = [
        ("speech_ratio", "speaking share of audio / 说话占比", 2),
        ("pauses_per_min", "pauses ≥0.25 s per minute / 每分钟停顿", 1),
        ("wpm", "words per minute / 语速", 0),
        ("f0_median_hz", "median F0, Hz / 基频中位数", 1),
        ("f0_range_semitones", "F0 range, semitones / 音域", 1),
        ("speech_db_std", "loudness SD, dB / 音量动态", 1),
        ("pause_mean_s", "mean pause, s / 平均停顿", 2),
    ]
    summary = {"n_videos_analysed": len(m), "n_speech_type": len(speech),
               "speech_audio_hours": round(sum(num(r, "video_duration_s") for r in speech) / 3600, 2),
               "n_transcripts": len(trans), "n_audio_copies": len(audio), "n_plots": len(plots),
               "candidates": {}}
    for name, rs in (("TALARICO", tal), ("PAXTON", pax)):
        d = {"n": len(rs), "metric_median": {}}
        for k, _lab, nd in metrics:
            v, n = med(rs, k)
            d["metric_median"][k] = None if not np.isfinite(v) else round(v, nd)
            d["metric_median"][k + "_n"] = n
        for k in ("pron_i", "pron_we", "pron_you", "pron_they", "mentions_texas", "words"):
            v, n = med(rs, k)
            d["metric_median"][k] = None if not np.isfinite(v) else round(v, 0)
        summary["candidates"][name] = d
    (DEST / "summary_by_candidate.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    # ------------------------------------------------------------------ figures
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 4, figsize=(12, 3.4))
        keys = [("speech_ratio", "speech share"), ("pauses_per_min", "pauses / min"),
                ("wpm", "words / min"), ("f0_median_hz", "F0 median (Hz)")]
        for ax, (k, lab) in zip(axes, keys):
            vals, errs, ns = [], [], []
            for rs in (tal, pax):
                a = [num(r, k) for r in rs]
                a = [x for x in a if np.isfinite(x)]
                vals.append(np.median(a) if a else 0)
                errs.append(np.std(a) if a else 0)
                ns.append(len(a))
            ax.bar(["Talarico", "Paxton"], vals, yerr=errs, capsize=4,
                   color=["#3b6ea5", "#b4492f"])
            ax.set_title(lab, fontsize=9)
            for i, (v, n) in enumerate(zip(vals, ns)):
                ax.text(i, v, f"n={n}", ha="center", va="bottom", fontsize=7)
        fig.suptitle("Delivery measures, speech-type videos only (median ± SD)", fontsize=10)
        fig.tight_layout(rect=(0, 0, 1, 0.93))
        fig.savefig(DEST / "fig_delivery_comparison.png", dpi=120)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(6.4, 4.2))
        for rs, lab, col in ((tal, "Talarico", "#3b6ea5"), (pax, "Paxton", "#b4492f")):
            xs = [num(r, "pauses_per_min") for r in rs]
            ys = [num(r, "wpm") for r in rs]
            ss = [max(20, min(240, num(r, "video_duration_s") / 30)) for r in rs]
            sel = [(x, y, s) for x, y, s in zip(xs, ys, ss) if np.isfinite(x) and np.isfinite(y)]
            if sel:
                ax.scatter([s[0] for s in sel], [s[1] for s in sel], s=[s[2] for s in sel],
                           alpha=0.7, color=col, label=lab)
        ax.set_xlabel("pauses per minute")
        ax.set_ylabel("words per minute")
        ax.set_title("Pacing: speech rate vs pause rate (bubble = video length)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(DEST / "fig_pacing.png", dpi=120)
        plt.close(fig)
    except Exception as e:  # noqa: BLE001
        print("figure step skipped:", e)

    # ------------------------------------------------------------------ README
    A, L = (lambda s: L.append(s)), []
    L = []
    A = L.append
    A("# 11_speech_audio — 演讲音频与交付分析")
    A("")
    A("**English** — Audio was pulled from every downloaded video and measured, because the")
    A("archive's own gap register said delivery, tone and pacing were `unknown`. For")
    A("speech-type videos the audio track is also kept as a 64 kbps mono copy, and word-level")
    A("captions are captured as timed transcripts. Nothing here interprets *why* a candidate")
    A("sounds the way he does; it records what can be measured and marks the rest.")
    A("")
    A("**中文** — 本目录从每段已下载视频中抽出音轨并做测量。档案此前的缺口登记写明：交付方式、")
    A("语气与节奏均为 `unknown`。演讲类视频另存 64 kbps 单声道音频副本，并把字幕整理成带时间码的")
    A("逐字稿。这里不解释「为什么听起来是这样」，只记录可测的量，其余标注为不可测。")
    A("")
    A("---")
    A("")
    A("## 1. Coverage / 覆盖范围")
    A("")
    A("| | |")
    A("|---|---|")
    A("| Videos analysed | **%d** |" % summary["n_videos_analysed"])
    A("| Speech-type videos | **%d** (%s h of audio) |"
      % (summary["n_speech_type"], summary["speech_audio_hours"]))
    A("| Audio copies kept (`audio/*.m4a`, 64 kbps mono) | **%d** |" % summary["n_audio_copies"])
    A("| Timed transcripts (`transcripts/`) | **%d** |" % summary["n_transcripts"])
    A("| Delivery plots (`plots/`) | **%d** |" % summary["n_plots"])
    A("| Segments (60 s windows) | **%d** |" % len(seg))
    A("")
    A("Kinds treated as \"speech\": rally_speech, victory_speech, concession_speech,")
    A("convention_speech, town_hall, interview, final_rally, tour_launch. News packages are")
    A("measured but excluded from the candidate comparison, because their audio is mostly")
    A("reporter narration.")
    A("")
    A("## 2. Method / 方法")
    A("")
    A("1. **Decode** — `ffmpeg` → 16 kHz mono PCM; the working WAV is deleted after measurement,")
    A("   the kept copy is AAC 64 kbps mono.")
    A("2. **Speech/silence** — 25 ms frames, 10 ms hop, RMS in dBFS. The noise floor is the 10th")
    A("   percentile; the speech threshold is `max(noise+9 dB, min(p95−6 dB, −32 dB))`, then")
    A("   150 ms gaps are closed and runs under 120 ms dropped.")
    A("3. **Pauses** — silence runs ≥ 0.25 s *inside* the first–last speech span, reported as")
    A("   count, mean and maximum length, and per minute of speech.")
    A("4. **Loudness** — mean, SD and p10/p90 of dBFS over speech frames (dynamics, not LUFS).")
    A("5. **F0** — normalised autocorrelation, 40 ms window / 20 ms hop, 55–400 Hz; the first lag")
    A("   within 85 % of the frame maximum is taken as the period (this avoids the usual")
    A("   octave-up error from a strong second harmonic), then median-filtered over 5 frames.")
    A("   **Indicative only** on rally audio that contains music, applause and PA.")
    A("6. **Spectral centroid** — mean over speech frames (a rough brightness/timbre proxy).")
    A("7. **Speech rate** — words from the English captions yt-dlp saved (auto or manual).")
    A("   `wpm` divides by the caption span; `articulation_wpm` divides by measured speech time.")
    A("8. **Rhetoric counters** — pronoun classes, \"Texas\" mentions, vocabulary richness,")
    A("   mean sentence length and the 12 most frequent content words, all from the caption text.")
    A("")
    A("Scripts: `../_staging/vision/analyze_speech.py` (measure) and")
    A("`../_staging/vision/gen_audio_readme.py` (this file + figures).")
    A("")
    A("## 3. Deliverables / 交付物")
    A("")
    A("| File | Content |")
    A("|---|---|")
    A("| `delivery_metrics.csv` | one row per video: speech/silence, pauses, loudness, F0, centroid, caption-derived rate and rhetoric counters |")
    A("| `speech_segments.csv` | 60 s windows per video: speech ratio, loudness, F0, words, wpm — the pacing arc |")
    A("| `transcripts/<slug>.txt` | caption text (English, verbatim as published) |")
    A("| `transcripts/<slug>.cues.csv` | timed cues: start, end, text |")
    A("| `audio/<slug>.m4a` | 64 kbps mono audio copy for speech-type videos |")
    A("| `plots/<slug>.png` | waveform envelope + VAD + F0 track + caption density |")
    A("| `summary_by_candidate.json` | medians per candidate and coverage counts |")
    A("| `fig_delivery_comparison.png` | four delivery measures, candidate vs candidate |")
    A("| `fig_pacing.png` | words-per-minute vs pause rate per speech |")
    A("")
    A("## 4. Measured delivery / 测量结果")
    A("")
    A("Medians over speech-type videos. n is the number of videos contributing a value.")
    A("")
    A("| Measure | Talarico | Paxton |")
    A("|---|---|---|")
    for k, lab, nd in metrics:
        t = summary["candidates"]["TALARICO"]["metric_median"]
        p = summary["candidates"]["PAXTON"]["metric_median"]
        A("| %s | %s (n=%s) | %s (n=%s) |" % (
            lab,
            "—" if t.get(k) is None else f"{t[k]:.{nd}f}", t.get(k + "_n", 0),
            "—" if p.get(k) is None else f"{p[k]:.{nd}f}", p.get(k + "_n", 0)))
    A("")
    A("Rhetoric counters (median per speech, caption-derived):")
    A("")
    A("| Counter | Talarico | Paxton |")
    A("|---|---|---|")
    for k, lab in (("words", "words per speech"), ("pron_i", "first person I"),
                   ("pron_we", "we / our / us"), ("pron_you", "you / your"),
                   ("pron_they", "they / them / their"), ("mentions_texas", "\"Texas\"")):
        t = summary["candidates"]["TALARICO"]["metric_median"].get(k)
        p = summary["candidates"]["PAXTON"]["metric_median"].get(k)
        A("| %s | %s | %s |" % (lab, "—" if t is None else int(t), "—" if p is None else int(p)))
    A("")
    A("## 5. What can and cannot be claimed / 可以说与不可以说")
    A("")
    A("- **Can**: speech share, pause counts, loudness dynamics, caption-based speaking rate,")
    A("  and *indicative* pitch ranges, each per video and per 60 s segment.")
    A("- **Cannot**: infer emotion, sincerity, confidence or \"tone\" from these numbers; infer")
    A("  audience reaction from loudness (applause contaminates the VAD); compare venues as if")
    A("  microphone and PA were equal — they are not. Rally audio is a *mix*, not a studio feed.")
    A("- **Do not average across kinds.** A 20 s news soundbite and a 20 min rally speech are not")
    A("  the same measurement; the comparison table already restricts to speech-type videos.")
    A("")
    A("## 6. Reproduction / 复现")
    A("")
    A("```powershell")
    A("python texas-senate-2026/_staging/vision/download_all.py        # video + captions")
    A("python texas-senate-2026/_staging/vision/analyze_speech.py      # decode + measure")
    A("python texas-senate-2026/_staging/vision/gen_audio_readme.py    # this file + figures")
    A("```")
    A("")
    A("## 7. Limits and rights / 局限与版权")
    A("")
    A("1. **Caption coverage is partial.** Where no English captions exist, `words`, `wpm` and the")
    A("   rhetoric counters are empty — the delivery measures are still valid.")
    A("2. **Auto captions are not transcripts.** They drop punctuation and mishear names; counts")
    A("   are approximate (±few %) and sentence statistics are rough.")
    A("3. **F0 on mixed audio** can lock onto music or crowd noise. `voiced_ratio` and the wide")
    A("   p10–p90 spread show how much of each file is genuinely trackable.")
    A("4. **Loudness is dBFS, not LUFS**, and no microphone calibration exists — never compare")
    A("   absolute levels across venues.")
    A("5. **Rights**: audio is cut from YouTube uploads owned by the campaigns and stations.")
    A("   Internal analysis only; not licensed for republication or for re-upload.")
    A("")
    (DEST / "README.md").write_text("\n".join(L), encoding="utf-8")
    print("wrote summary, figures and README;",
          summary["n_videos_analysed"], "videos,", summary["n_speech_type"], "speech-type")


if __name__ == "__main__":
    main()
