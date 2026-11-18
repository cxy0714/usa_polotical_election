#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append a dated 'video and news-photo layer' section to each case README.

    python _tools/readme_update.py <case> [...]
"""
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARK = "## Video and news-photo layer (2026-11-18)"


def rows(p):
    if not p.exists():
        return []
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for case in argv:
        p = ROOT / case / "README.md"
        body = p.read_text(encoding="utf-8") if p.exists() else ""
        if MARK in body:
            print(case, "already updated")
            continue
        imgs = rows(ROOT / case / "04_visual_archive" / "image_archive.csv")
        news = [r for r in imgs if r["copyright_status"] == "all_rights_reserved_link_only"]
        vids = rows(ROOT / case / "10_video_frames" / "video_sources.csv")
        kfs = rows(ROOT / case / "10_video_frames" / "keyframes.csv")
        ids = rows(ROOT / case / "10_video_frames" / "keyframes_identity.csv")
        dist = Counter(r["identity"] for r in ids)
        attributed = sum(n for k, n in dist.items() if k != "unknown")
        add = [
            "",
            MARK,
            "",
            f"- **News photographs:** {len(news)} credited caption rows added to "
            f"`04_visual_archive/image_archive.csv` from the archived article HTML. All are "
            f"`all_rights_reserved_link_only`: article URL, caption and credit are stored, the "
            f"image is not.",
            f"- **Video corpus:** {len(vids)} uploaded videos, {len(kfs)} keyframes, "
            f"{attributed}/{len(ids)} frames attributed by SFace against the licensed portraits. "
            f"Details, method and limits: [`10_video_frames/README.md`](10_video_frames/README.md).",
            f"- **Identity distribution:** " + (", ".join(f"{k} {n}" for k, n in dist.most_common())
                                                 or "none"),
            "- **Still no clothing evidence:** no keyframe was read by a vision model and no harvested "
            "caption names clothing, so `clothing_notes` remains `unknown` throughout.",
            "",
            f"- **新闻照片：** 从存档文章 HTML 新增 {len(news)} 条带署名的图注记录至 "
            f"`04_visual_archive/image_archive.csv`。全部为 `all_rights_reserved_link_only`：保存文章 URL、"
            f"图注与署名，不保存图片。",
            f"- **视频语料：** {len(vids)} 段上传视频、{len(kfs)} 张关键帧，SFace 对照授权肖像后归属 "
            f"{attributed}/{len(ids)} 帧。方法、限制与逐视频明细见 "
            f"[`10_video_frames/README.md`](10_video_frames/README.md)。",
            "- **仍无着装证据：** 没有关键帧被视觉模型读取，已采集图注也没有描述着装，`clothing_notes` 全部保持 `unknown`。",
            "",
        ]
        p.write_text(body.rstrip() + "\n" + "\n".join(add), encoding="utf-8", newline="\n")
        print(case, f"updated ({len(news)} news, {len(vids)} videos)")


if __name__ == "__main__":
    main(sys.argv[1:])
