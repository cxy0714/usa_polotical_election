#!/usr/bin/env python3
"""One-off patch: surface the SFace identity pass in the site's video pages.

Applied once to `_lead_site_txstyle.py`; kept in the repository because it documents exactly which
strings changed (the builder is hand-edited otherwise).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "_lead_site_txstyle.py")

EDITS = []


def sub(old, new, label):
    EDITS.append((old, new, label))


sub(
    '''    ("10_video_frames/keyframes.csv", "video", "Keyframes", "关键帧",
     "300 scene-change frames with face counts and bounding boxes."),''',
    '''    ("10_video_frames/keyframes.csv", "video", "Keyframes", "关键帧",
     "300 scene-change frames with face counts and bounding boxes."),
    ("10_video_frames/keyframes_identity.csv", "video", "Keyframe identities", "关键帧身份识别",
     "Per-frame SFace match against archive photographs: Andrews, Graham, unidentified, or no face."),''',
    "dataset row for the identity CSV")

sub(
    '''def shots_html(frames, page_dir, limit=4):
    cells = []
    for r in frames[:limit]:
        src = os.path.relpath(os.path.join(ROOT, "10_video_frames", r["file"]), page_dir).replace(os.sep, "/")
        cells.append(f'<a href="{src}"><img loading="lazy" src="{src}" alt="{esc(r["frame_id"])}"></a>'
                     f'<span>{esc(r["timecode"])} · faces {esc(r["faces_detected"])}</span>')
    return '<div class="shots">' + "".join(cells) + "</div>"''',
    '''def shots_html(frames, page_dir, ident, limit=4):
    cells = []
    for r in frames[:limit]:
        src = os.path.relpath(os.path.join(ROOT, "10_video_frames", r["file"]), page_dir).replace(os.sep, "/")
        cells.append(f'<a href="{src}"><img loading="lazy" src="{src}" alt="{esc(r["frame_id"])}"></a>'
                     f'<span>{esc(r["timecode"])} {identity_badge(r, ident)}</span>')
    return '<div class="shots">' + "".join(cells) + "</div>"''',
    "shots carry the identity badge")

sub(
    '''        if sec == "video":
            by_video = frame_rows()
            blocks = []
            for v in video_rows():
                frames = by_video.get(v["slug"], [])
                link = f'<a href="{esc(v["slug"])}.html">全部 {len(frames)} 帧 / all frames</a>'
                blocks.append(f'<h3>{esc(v["title"])}</h3>'
                              f'<p class="meta">{esc(v["candidate_source"])} · {esc(v["kind"])} · '
                              f'{esc(v["duration_s"])}s · {esc(v["upload_date"])} · {link}</p>'
                              + shots_html(frames, page_dir))''',
    '''        if sec == "video":
            by_video = frame_rows()
            ident = identity_map()
            blocks = []
            for v in video_rows():
                frames = by_video.get(v["slug"], [])
                counts = {}
                for f in frames:
                    who = ident.get(f["frame_id"], {}).get("identity", "unknown")
                    counts[who] = counts.get(who, 0) + 1
                summary = (f'安德鲁斯 {counts.get("ANDREWS", 0)} · '
                           f'格雷厄姆 {counts.get("GRAHAM", 0)} · '
                           f'未识别 {counts.get("unknown", 0) + counts.get("other", 0)} · '
                           f'无人脸 {counts.get("noface", 0)}')
                link = f'<a href="{esc(v["slug"])}.html">全部 {len(frames)} 帧 / all frames</a>'
                blocks.append(f'<h3>{esc(v["title"])}</h3>'
                              f'<p class="meta">{esc(v["candidate_source"])} · {esc(v["kind"])} · '
                              f'{esc(v["duration_s"])}s · {esc(v["upload_date"])} · {link}</p>'
                              f'<p class="meta">{summary}</p>'
                              + shots_html(candidate_frames(frames, ident), page_dir, ident))''',
    "video hub previews candidate frames and prints counts")

sub(
    '''        figs = []
        for r in frames:
            src = os.path.relpath(os.path.join(ROOT, "10_video_frames", r["file"]), vdir).replace(os.sep, "/")
            figs.append(f'<figure><a href="{src}"><img loading="lazy" src="{src}" alt="{esc(r["frame_id"])}"></a>'
                        f'<figcaption><b>{esc(r["timecode"])}</b> · faces {esc(r["faces_detected"])} · '
                        f'largest {esc(r.get("largest_face_area_pct", "unknown"))}% · {esc(r["frame_id"])}'
                        f'</figcaption></figure>')''',
    '''        ident = identity_map()
        figs = []
        for r in frames:
            src = os.path.relpath(os.path.join(ROOT, "10_video_frames", r["file"]), vdir).replace(os.sep, "/")
            who = ident.get(r["frame_id"], {}).get("identity", "unknown")
            figs.append(f'<figure data-identity="{esc(who)}"><a href="{src}">'
                        f'<img loading="lazy" src="{src}" alt="{esc(r["frame_id"])}"></a>'
                        f'<figcaption><b>{esc(r["timecode"])}</b> {identity_badge(r, ident)} · '
                        f'faces {esc(r["faces_detected"])} · '
                        f'largest {esc(r.get("largest_face_area_pct", "unknown"))}% · {esc(r["frame_id"])}'
                        f'</figcaption></figure>')''',
    "per-video figures carry data-identity and a badge")

sub(
    '''                f'<div class="gal">{"".join(figs)}</div>')''',
    '''                f'<div class="facetbar" data-facet-group="frame-gallery">'
                f'<button class="on" data-facet="all">全部 / all</button>'
                f'<button data-facet="ANDREWS">安德鲁斯 / Andrews</button>'
                f'<button data-facet="GRAHAM">格雷厄姆 / Graham</button>'
                f'<button data-facet="unknown">未识别 / unidentified</button>'
                f'</div>'
                f'<div class="gal" id="frame-gallery">{"".join(figs)}</div>')''',
    "facet bar on the frame gallery")

sub(
    '''  document.querySelectorAll('[data-filter]').forEach(function(inp){''',
    '''  document.querySelectorAll('[data-facet-group]').forEach(function(group){
    var target=document.getElementById(group.dataset.facetGroup);
    if(!target) return;
    group.querySelectorAll('button').forEach(function(b){
      b.addEventListener('click',function(){
        group.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b)});
        var want=b.dataset.facet;
        target.querySelectorAll('[data-identity]').forEach(function(el){
          el.style.display=(want==='all'||el.dataset.identity===want)?'':'none';
        });
      });
    });
  });

  document.querySelectorAll('[data-filter]').forEach(function(inp){''',
    "JS: facet buttons filter frames")

sub(
    '''.layout{max-width:1500px}''',
    '''.layout{max-width:1500px}
.idtag{display:inline-block;padding:.05rem .35rem;border-radius:4px;font-size:.72em;font-weight:600;
  background:var(--line);color:var(--fg);margin-left:.25rem;white-space:nowrap}
.idtag.id-andrews{background:#123a5f;color:#fff}
.idtag.id-graham{background:#7a1f1f;color:#fff}
.facetbar{display:flex;gap:.4rem;flex-wrap:wrap;margin:1rem 0 .6rem}
.facetbar button{border:1px solid var(--line);background:var(--card);color:var(--muted);
  padding:.3rem .7rem;border-radius:999px;font-size:.82rem;cursor:pointer}
.facetbar button.on{background:var(--accent2);border-color:var(--accent2);color:#fff}''',
    "override CSS for identity tags and facet bar")


def main():
    text = open(TARGET, encoding="utf-8").read()
    original = text
    for old, new, label in EDITS:
        if new.strip() and new.splitlines()[0] in text and label != "dataset row for the identity CSV":
            pass
        if old not in text:
            print(f"  MISS  {label}")
            continue
        text = text.replace(old, new, 1)
        print(f"  ok    {label}")
    if text == original:
        print("nothing changed")
        return 1
    open(TARGET, "w", encoding="utf-8", newline="\n").write(text)
    print("written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
