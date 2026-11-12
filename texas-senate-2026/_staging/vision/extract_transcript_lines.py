#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Turn caption cue files into readable, translatable lines.

The captions yt-dlp saves are cue fragments (often 1–4 words). For reading and for
1:1 bilingual alignment we merge consecutive cues into lines: a line closes when it
has ~28 words, when the next cue starts >1.2 s later, or when it ends a sentence
after at least 12 words.

Input : 11_speech_audio/transcripts/<slug>.cues.csv   (start_s,end_s,text)
Output: 11_speech_audio/transcripts/<slug>.lines.csv  (idx,start_s,end_s,words,text)

    python texas-senate-2026/_staging/vision/extract_transcript_lines.py
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TR = ROOT / "11_speech_audio" / "transcripts"

MAX_WORDS = 28
MIN_SENT_WORDS = 12
GAP_S = 1.2
SENT_END = (".", "?", "!", "…", '."', '?"', '!"')


def flush(buf, out, idx):
    if not buf:
        return idx
    text = " ".join(e[2].strip() for e in buf if e[2] and e[2].strip())
    text = " ".join(text.split())
    if not text:
        return idx
    out.append({"idx": idx, "start_s": "%.2f" % buf[0][0], "end_s": "%.2f" % buf[-1][1],
                "words": len(text.split()), "text": text})
    return idx + 1


def merge(cues):
    out, buf, idx = [], [], 0
    for start, end, text in cues:
        if not text:
            continue
        if buf and start - buf[-1][1] > GAP_S:
            idx = flush(buf, out, idx)
            buf = []
        buf.append((start, end, text))
        n = sum(len(t.split()) for _s, _e, t in buf)
        last = text.strip()
        if n >= MAX_WORDS or (n >= MIN_SENT_WORDS and last.endswith(SENT_END)):
            idx = flush(buf, out, idx)
            buf = []
    flush(buf, out, idx)
    return out


def read_cues(p):
    rows = []
    with open(p, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            try:
                rows.append((float(r["start_s"]), float(r["end_s"]), (r["text"] or "").strip()))
            except (KeyError, ValueError, TypeError):
                continue
    return rows


def main():
    cues = sorted(TR.glob("*.cues.csv"))
    if not cues:
        print("no cue files")
        return 1
    total_lines = total_words = 0
    for p in cues:
        slug = p.name[: -len(".cues.csv")]
        lines = merge(read_cues(p))
        if not lines:
            continue
        out = TR / (slug + ".lines.csv")
        with open(out, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["idx", "start_s", "end_s", "words", "text"])
            w.writeheader()
            w.writerows(lines)
        total_lines += len(lines)
        total_words += sum(x["words"] for x in lines)
    print(f"transcripts: {len(cues)} | lines: {total_lines} | words: {total_words}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
