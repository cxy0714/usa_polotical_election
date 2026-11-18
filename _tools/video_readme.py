#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write 10_video_frames/README.md from the generated CSVs (bilingual).

    python _tools/video_readme.py <case> [...]

Keeps the prose tied to the files: counts, per-video coverage, identity distribution
and the method's limits. No interpretation of appearance.
"""
import csv
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build(case):
    d = ROOT / case / "10_video_frames"
    vids = rows(d / "video_sources.csv")
    kfs = rows(d / "keyframes.csv")
    ident = rows(d / "keyframes_identity.csv")
    fsum = {r["slug"]: r for r in rows(d / "video_face_summary.csv")}
    if not vids:
        print(case, "no video data")
        return
    imap = {r["frame_id"]: r for r in ident}
    per_video = {}
    for k in kfs:
        per_video.setdefault(k["slug"], []).append(k)
    dist = Counter(imap[k["frame_id"]]["identity"] for k in kfs if k["frame_id"] in imap)
    total_dur = sum(float(v["duration_s"]) for v in vids if v["duration_s"].replace(".", "").isdigit())

    lines = []
    lines.append("---")
    lines.append('title: "Video keyframes and face identification"')
    lines.append('title_zh: "视频关键帧与人脸识别"')
    lines.append("compiled_by: Lead Research Agent")
    lines.append("last_updated: 2026-11-18")
    lines.append("status: complete")
    lines.append("---")
    lines.append("")
    lines.append("# Video keyframes and face identification / 视频关键帧与人脸识别")
    lines.append("")
    lines.append(f"{len(vids)} source videos, {len(kfs)} extracted keyframes and {len(ident)} identity "
                 f"rows. The corpus is a convenience sample of publicly available YouTube uploads — "
                 f"debates, rallies, interviews, victory and concession speeches — not a controlled "
                 f"sample of the campaign's video output.")
    lines.append("")
    lines.append(f"共 {len(vids)} 个来源视频、{len(kfs)} 张关键帧、{len(ident)} 条身份判定。语料是公开 YouTube "
                 f"视频的便利样本——辩论、集会、采访、胜选与承认败选演讲——不是竞选视频产出的受控样本。")
    lines.append("")
    lines.append("## Corpus / 语料")
    lines.append("")
    lines.append("| slug | kind | side | duration (s) | frames | frames with face | attributed |")
    lines.append("|---|---|---|---:|---:|---:|---:|")
    for v in vids:
        s = fsum.get(v["slug"], {})
        fr = per_video.get(v["slug"], [])
        att = sum(1 for k in fr if imap.get(k["frame_id"], {}).get("identity", "unknown") != "unknown")
        lines.append(f"| `{v['slug']}` | {v['kind']} | {v['candidate_source']} | {v['duration_s']} | "
                     f"{s.get('frames_extracted','unknown')} | {s.get('frames_with_face','unknown')} | {att} |")
    lines.append("")
    lines.append("Identity distribution / 身份分布: " +
                 ", ".join(f"{k} {n}" for k, n in dist.most_common()))
    lines.append("")
    lines.append("## Method / 方法")
    lines.append("")
    lines.append("- Frames: ffmpeg scene-change selection (`scene > 0.30`, at most 20 per video, 960 px wide). "
                 "When a static-camera video yields fewer than six cuts, twelve evenly spaced frames are "
                 "sampled instead and the row notes this.")
    lines.append("- Detection: OpenCV YuNet (`yunet.onnx`), confidence 0.6, on frames upscaled 2× when "
                 "narrower than 1600 px.")
    lines.append("- Identification: OpenCV SFace (`sface.onnx`), cosine similarity against faces detected in "
                 "the case's licensed portraits; a frame is attributed only when the best match clears "
                 "0.363 and beats the runner-up identity by 0.05. Everything else is `unknown`.")
    lines.append("- Long videos (over 20 minutes) were downloaded as their first 15 minutes only; the "
                 "`duration_s` column records the local excerpt, not the full upload.")
    lines.append("")
    lines.append("## Limits / 限制")
    lines.append("")
    lines.append("- The recogniser distinguishes only the two nominees in this case. A moderator, surrogate "
                 "or crowd member can be assigned to whichever nominee is the closer of the two; the "
                 "margin rule reduces but does not eliminate this.")
    lines.append("- No captions, transcripts or audio measures are produced in this pass.")
    lines.append("- Source videos are not committed (size and platform terms); `video_sources.csv` carries "
                 "the URL and the local file name.")
    lines.append("- The archive does not describe clothing, grooming or body language from these frames. "
                 "`clothing_notes` in the image archive stays `unknown` unless a text source states it.")
    lines.append("")
    lines.append("## Reproduce / 复现")
    lines.append("")
    lines.append("```")
    lines.append(f"python _tools/video_pipeline.py meta     {case}")
    lines.append(f"python _tools/video_pipeline.py download {case}")
    lines.append(f"python _tools/video_pipeline.py frames   {case}")
    lines.append(f"python _tools/video_pipeline.py faces    {case}")
    lines.append("```")
    lines.append("")
    (d / "README.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(case, "wrote", d / "README.md", f"({len(vids)} videos, {len(kfs)} frames)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for c in sys.argv[1:]:
        build(c)
