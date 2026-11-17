#!/usr/bin/env python3
"""One-off patch: the frame pages show only frames attributed to Andrews or Graham.

Everything else (moderators, audiences, unidentified faces) is dropped from the galleries; the counts
stay visible so a reader can see how many frames were set aside, and the whole identity table remains
browsable as a dataset page.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "_lead_site_txstyle.py")

OLD_VIDEO = '''    for v in video_rows():
        frames = by_video.get(v["slug"], [])
        if not frames:
            continue
        ident = identity_map()
        figs = []
        for r in frames:
            src = os.path.relpath(os.path.join(ROOT, "10_video_frames", r["file"]), vdir).replace(os.sep, "/")
            who = ident.get(r["frame_id"], {}).get("identity", "unknown")
            figs.append(f'<figure data-identity="{esc(who)}"><a href="{src}">'
                        f'<img loading="lazy" src="{src}" alt="{esc(r["frame_id"])}"></a>'
                        f'<figcaption><b>{esc(r["timecode"])}</b> {identity_badge(r, ident)} · '
                        f'faces {esc(r["faces_detected"])} · '
                        f'largest {esc(r.get("largest_face_area_pct", "unknown"))}% · {esc(r["frame_id"])}'
                        f'</figcaption></figure>')
        body = (f'<div class="crumb"><a href="../index.html">首页</a> / <a href="index.html">视频帧</a> / '
                f'{esc(v["title"])}</div>'
                f'<h1>{esc(v["title"])}<span class="zh">{esc(v["slug"])}</span></h1>'
                f'<div class="meta">{esc(v["channel"])} · {esc(v["kind"])} · {esc(v["duration_s"])}s · '
                f'upload {esc(v["upload_date"])} · {len(frames)} keyframes · '
                f'<a href="{esc(v["url"])}">原视频 / source</a></div>'
                f'<div class="warn">These frames are scene-change samples, not a shot-by-shot edit. Face counts come '
                f'from YuNet detection at 960 px width; the archive does not caption what is happening in them.</div>'
                f'<div class="facetbar" data-facet-group="frame-gallery">'
                f'<button class="on" data-facet="all">全部 / all</button>'
                f'<button data-facet="ANDREWS">安德鲁斯 / Andrews</button>'
                f'<button data-facet="GRAHAM">格雷厄姆 / Graham</button>'
                f'<button data-facet="unknown">未识别 / unidentified</button>'
                f'</div>'
                f'<div class="gal" id="frame-gallery">{"".join(figs)}</div>')'''

NEW_VIDEO = '''    for v in video_rows():
        frames = by_video.get(v["slug"], [])
        if not frames:
            continue
        ident = identity_map()
        # Only the two candidates' frames are published. The rest exist, are counted, and stay in the
        # identity table, but they are not shown: a frame of the moderator is not evidence about a
        # candidate and was the reason the galleries read as a crowd.
        cand = [r for r in frames if ident.get(r["frame_id"], {}).get("identity") in IDENT_LABEL]
        set_aside = [r for r in frames if r not in cand]
        figs = []
        for r in cand:
            src = os.path.relpath(os.path.join(ROOT, "10_video_frames", r["file"]), vdir).replace(os.sep, "/")
            who = ident.get(r["frame_id"], {}).get("identity", "unknown")
            figs.append(f'<figure data-identity="{esc(who)}"><a href="{src}">'
                        f'<img loading="lazy" src="{src}" alt="{esc(r["frame_id"])}"></a>'
                        f'<figcaption><b>{esc(r["timecode"])}</b> {identity_badge(r, ident)} · '
                        f'faces {esc(r["faces_detected"])} · '
                        f'largest {esc(r.get("largest_face_area_pct", "unknown"))}% · {esc(r["frame_id"])}'
                        f'</figcaption></figure>')
        counts = {}
        for r in cand:
            counts[ident[r["frame_id"]]["identity"]] = counts.get(ident[r["frame_id"]]["identity"], 0) + 1
        aside = (f'另有 {len(set_aside)} 帧未归属（主持人、观众或未能识别），未在此页展示；'
                 f'逐帧结果见 <a href="../data/keyframes_identity.html">keyframes_identity.csv</a>。'
                 f' / {len(set_aside)} frames set aside as unidentified or other people.')
        if cand:
            gallery = (f'<div class="facetbar" data-facet-group="frame-gallery">'
                       f'<button class="on" data-facet="all">全部候选人帧 / all candidate frames</button>'
                       f'<button data-facet="ANDREWS">安德鲁斯 / Andrews ({counts.get("ANDREWS", 0)})</button>'
                       f'<button data-facet="GRAHAM">格雷厄姆 / Graham ({counts.get("GRAHAM", 0)})</button>'
                       f'</div>'
                       f'<div class="gal" id="frame-gallery">{"".join(figs)}</div>'
                       f'<p class="meta">{aside}</p>')
        else:
            gallery = (f'<div class="warn">本视频没有识别出候选人的画面：{len(frames)} 帧均为未归属。'
                       f' / No frame in this video was attributed to a candidate.</div>'
                       f'<p class="meta">{aside}</p>')
        body = (f'<div class="crumb"><a href="../index.html">首页</a> / <a href="index.html">视频帧</a> / '
                f'{esc(v["title"])}</div>'
                f'<h1>{esc(v["title"])}<span class="zh">{esc(v["slug"])}</span></h1>'
                f'<div class="meta">{esc(v["channel"])} · {esc(v["kind"])} · {esc(v["duration_s"])}s · '
                f'upload {esc(v["upload_date"])} · 候选人帧 {len(cand)} / 全部 {len(frames)} 帧 · '
                f'<a href="{esc(v["url"])}">原视频 / source</a></div>'
                f'<div class="warn">These frames are scene-change samples, not a shot-by-shot edit. Identity comes '
                f'from an SFace comparison against archive photographs; a frame is shown only when a face cleared '
                f'the similarity and margin tests for Andrews or Graham.</div>'
                + gallery)'''

OLD_HUB = '''                link = f'<a href="{esc(v["slug"])}.html">全部 {len(frames)} 帧 / all frames</a>'
                blocks.append(f'<h3>{esc(v["title"])}</h3>'
                              f'<p class="meta">{esc(v["candidate_source"])} · {esc(v["kind"])} · '
                              f'{esc(v["duration_s"])}s · {esc(v["upload_date"])} · {link}</p>'
                              f'<p class="meta">{summary}</p>'
                              + shots_html(candidate_frames(frames, ident), page_dir, ident))'''

NEW_HUB = '''                cand = candidate_frames(frames, ident, limit=len(frames))
                link = f'<a href="{esc(v["slug"])}.html">候选人帧 {len(cand)} / 全部 {len(frames)} 帧</a>'
                if cand:
                    strip = shots_html(cand[:4], page_dir, ident)
                else:
                    strip = '<p class="meta">没有识别出候选人的画面 / no candidate frame attributed</p>'
                blocks.append(f'<h3>{esc(v["title"])}</h3>'
                              f'<p class="meta">{esc(v["candidate_source"])} · {esc(v["kind"])} · '
                              f'{esc(v["duration_s"])}s · {esc(v["upload_date"])} · {link}</p>'
                              f'<p class="meta">{summary}</p>'
                              + strip)'''


def main():
    text = open(TARGET, encoding="utf-8").read()
    n = 0
    for old, new, label in ((OLD_VIDEO, NEW_VIDEO, "per-video pages: candidate frames only"),
                            (OLD_HUB, NEW_HUB, "video hub: candidate strips, empty state")):
        if old not in text:
            print(f"  MISS  {label}")
            continue
        text = text.replace(old, new, 1)
        n += 1
        print(f"  ok    {label}")
    if not n:
        return 1
    open(TARGET, "w", encoding="utf-8", newline="\n").write(text)
    print("written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
