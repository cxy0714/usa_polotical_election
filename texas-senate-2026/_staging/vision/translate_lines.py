#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Machine-translate transcript lines into Chinese, for reading only.

Every transcript line (see extract_transcript_lines.py) is translated and stored next
to it as <slug>.zh.csv (idx,text_zh), one row per English line so a bilingual table
can align them 1:1.

How it talks to the service
  * lines are batched into one request, joined by newlines; the endpoint returns one
    segment per line, so alignment is 1:1 without parsing markers,
  * requests are sequential with a fixed delay (a burst of parallel requests got the
    first run rate-limited within minutes),
  * `client=dict-chrome-ex` is used because the `gtx` client was blocked by IP.

This is a READING AID, not a translation for publication:
  - the source is automatic YouTube caption text, already rough (names are misheard),
  - machine output adds its own errors, especially on names, scripture and Texas idiom,
  - the English line stays authoritative; never quote the Chinese as a candidate's words.

    python texas-senate-2026/_staging/vision/translate_lines.py --delay 0.6
    python texas-senate-2026/_staging/vision/translate_lines.py --slugs TAL_lubbock_full
"""
import argparse
import csv
import json
import sys
import time
import urllib.parse
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
TR = ROOT / "11_speech_audio" / "transcripts"
META = TR / "_translation_meta.json"
BASE = "https://translate.googleapis.com/translate_a/single"
HEADERS = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120 Safari/537.36")}
MAX_CHARS = 1600          # keep each request well under the endpoint limit
BACKOFF = (20, 40, 75, 120)


def translate_batch(lines, delay, log):
    """Translate a list of lines, one output line per input line. Returns list or None."""
    text = "\n".join(lines)
    for attempt, wait in enumerate(BACKOFF + (None,)):
        try:
            url = BASE + "?" + urllib.parse.urlencode(
                {"client": "dict-chrome-ex", "sl": "en", "tl": "zh-CN", "dt": "t", "q": text})
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                data = r.json()
                out = "".join(seg[0] for seg in data[0] if seg and seg[0])
                parts = [p.strip() for p in out.split("\n")]
                parts = [p for p in parts if p != ""] if len(parts) > len(lines) else parts
                if len(parts) == len(lines):
                    time.sleep(delay)
                    return parts
                log(f"    segment mismatch ({len(parts)} vs {len(lines)}), retrying line-by-line")
                singles = []
                for ln in lines:
                    got = translate_batch([ln], delay, log) if len(ln) <= MAX_CHARS else None
                    singles.append(got[0] if got else "")
                return singles
            if r.status_code in (429, 500, 502, 503) and wait is not None:
                log(f"    HTTP {r.status_code}, waiting {wait}s")
                time.sleep(wait)
                continue
            log(f"    HTTP {r.status_code}, giving up on this batch")
            return None
        except (requests.RequestException, ValueError, TypeError) as exc:
            log(f"    {type(exc).__name__}, retrying")
            if wait is None:
                return None
            time.sleep(wait)
    return None


def read_lines(p):
    with open(p, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def write_zh(p, pairs):
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["idx", "text_zh"])
        for idx, text in pairs:
            w.writerow([idx, text])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slugs", default="")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--delay", type=float, default=0.6)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    def log(msg):
        print(msg, flush=True)

    only = {s.strip() for s in args.slugs.split(",") if s.strip()}
    files = sorted(TR.glob("*.lines.csv"))
    if only:
        files = [p for p in files if p.name[: -len(".lines.csv")] in only]
    if args.limit:
        files = files[: args.limit]

    meta = {}
    if META.exists():
        try:
            meta = json.loads(META.read_text(encoding="utf-8"))
        except ValueError:
            meta = {}

    written = skipped = 0
    for p in files:
        slug = p.name[: -len(".lines.csv")]
        out = TR / (slug + ".zh.csv")
        lines = read_lines(p)
        existing = {}
        if out.exists() and not args.force:
            for row in read_lines(out):
                if (row.get("text_zh") or "").strip():
                    existing[int(row["idx"])] = row["text_zh"]
            if len(existing) >= len(lines):
                skipped += 1
                continue

        todo = [(int(r["idx"]), r["text"]) for r in lines if int(r["idx"]) not in existing]
        log(f"{slug}: {len(lines)} lines, {len(todo)} to translate")

        # batch by character budget
        batches, cur, cur_chars = [], [], 0
        for idx, text in todo:
            if cur and cur_chars + len(text) > MAX_CHARS:
                batches.append(cur)
                cur, cur_chars = [], 0
            cur.append((idx, text))
            cur_chars += len(text) + 1
        if cur:
            batches.append(cur)

        results = dict(existing)
        for bi, batch in enumerate(batches, 1):
            got = translate_batch([t for _i, t in batch], args.delay, log)
            if got is None:
                log(f"  batch {bi}/{len(batches)} failed, leaving those lines blank")
                continue
            for (idx, _text), zh in zip(batch, got):
                results[idx] = zh
            if bi % 10 == 0:
                log(f"  {slug} batch {bi}/{len(batches)}")

        write_zh(out, [(i, results.get(i, "")) for i in sorted(results)])
        meta[slug] = {"engine": "google-translate (client=dict-chrome-ex)",
                      "method": "machine translation, newline-aligned batches",
                      "source": "YouTube captions (auto or manual)", "date": "2026-11-12",
                      "lines": len(lines),
                      "translated": sum(1 for v in results.values() if v.strip())}
        written += 1

    for p in sorted(TR.glob("*.zh.csv")):
        slug = p.name[: -len(".zh.csv")]
        if slug not in meta:
            rows = read_lines(p)
            lines_f = TR / (slug + ".lines.csv")
            meta[slug] = {"engine": "google-translate (client=gtx)",
                          "method": "machine translation, line by line",
                          "source": "YouTube captions (auto or manual)", "date": "2026-11-12",
                          "lines": len(read_lines(lines_f)) if lines_f.exists() else len(rows),
                          "translated": sum(1 for r in rows if (r.get("text_zh") or "").strip())}
    meta["_note"] = ("Machine translation of automatic caption text. Reading aid only; "
                     "the English line is authoritative and the Chinese must not be quoted "
                     "as a candidate's words.")
    META.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"done: {written} written, {skipped} already complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
