#!/usr/bin/env python3
"""Render the South Carolina case site with the Texas case's design system.

The two sites are meant to read as one archive, so this builder does not invent a look: it copies
`texas-senate-2026/site`'s stylesheet verbatim and emits the same components (sticky header with the
twelve-nav, language-mode buttons, hero with bilingual columns and tags, stat grid, card grid,
`.table-wrap` tables, prose rules). Only the content is South Carolina's.

Output (overwrites the previous SC build):
  site/index.html                     overview
  site/{events,candidates,speeches,visual,video,audio,media,context,compare,sources}/index.html
  site/data/<dataset>.html            one page per CSV
  site/docs/<slug>.html               one page per Markdown document
  site/about.html                     method
  site/assets/{style.css,app.js}

Run: python _staging/_lead_site_txstyle.py
"""
import csv
import html
import json
import os
import re
import shutil
import sys

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
SITE = os.path.join(ROOT, "site")
TX_CSS = os.path.join(REPO, "_tools", "_tx_style.css")

CASE_NO = "案例研究 002"
CASE_EN = "South Carolina Senate 2026"
CASE_ZH = "2026 南卡罗来纳州联邦参议员选举"

# nav: (dir or page, zh label, en label, section id used to assign datasets/docs)
NAV = [
    ("index.html", "首页", "Home", "home"),
    ("events/", "事件", "Events", "events"),
    ("candidates/", "候选人", "Candidates", "candidates"),
    ("speeches/", "演讲", "Speeches", "speeches"),
    ("visual/", "影像", "Images", "visual"),
    ("video/", "视频帧", "Frames", "video"),
    ("audio/", "音频", "Audio", "audio"),
    ("media/", "媒体与资金", "Media & money", "media"),
    ("context/", "选举背景", "Context", "context"),
    ("compare/", "对比分析", "Comparison", "compare"),
    ("sources/", "来源与缺口", "Sources", "sources"),
    ("about.html", "关于档案", "About", "about"),
]

# path, section, en title, zh title, description
DATASETS = [
    ("01_candidates/policy_positions.csv", "candidates", "Policy positions", "政策立场",
     "51 rows. Andrews has no legislative record, so her record columns are unknown throughout."),
    ("01_candidates/andrews/career_timeline.csv", "candidates", "Career timeline: Andrews", "生涯年表：安德鲁斯",
     "20 dated milestones."),
    ("01_candidates/graham/career_timeline.csv", "candidates", "Career timeline: Graham", "生涯年表：格雷厄姆",
     "24 dated milestones."),
    ("02_campaign_events/campaign_events.csv", "events", "Campaign events", "竞选活动",
     "32 documented events in 17 categories, with the vacancy columns Texas does not need."),
    ("03_speeches/speech_archive.csv", "speeches", "Speech archive", "演讲档案",
     "24 speeches and speech-like appearances."),
    ("03_speeches/speech_video_index.csv", "speeches", "Speech video index", "演讲视频索引",
     "22 rows mapping speeches to recorded video."),
    ("04_visual_archive/image_archive.csv", "visual", "Image archive", "图片档案",
     "52 photographs with licence, resolution and description."),
    ("10_video_frames/video_sources.csv", "video", "Video corpus", "视频语料",
     "27 videos with local filenames, byte sizes and duration."),
    ("10_video_frames/keyframes.csv", "video", "Keyframes", "关键帧",
     "300 scene-change frames with face counts and bounding boxes."),
    ("10_video_frames/keyframes_identity.csv", "video", "Keyframe identities", "关键帧身份识别",
     "Per-frame SFace match against archive photographs: Andrews, Graham, unidentified, or no face."),
    ("10_video_frames/video_face_summary.csv", "video", "Per-video face summary", "逐视频人脸汇总",
     "Frames extracted, frames with faces, largest face share."),
    ("11_speech_audio/audio_metrics.csv", "audio", "Audio metrics", "音频指标",
     "Mean level, silence ratio, caption word count and speaking rate per video."),
    ("05_campaign_media/media_coverage.csv", "media", "Media coverage", "媒体报道",
     "55 coverage rows with outlet, author, title and framing."),
    ("05_campaign_media/advertisements.csv", "media", "Advertisements", "广告",
     "3 rows; two are independent-expenditure transfers rather than ad creative."),
    ("05_campaign_media/social_media.csv", "media", "Social media", "社交媒体",
     "3 documented posts, two of them second-hand."),
    ("06_campaign_finance/campaign_finance.csv", "media", "Campaign finance", "竞选财务",
     "5 FEC snapshots for the two principals; never summed with outside spending."),
    ("06_campaign_finance/other_candidates_finance.csv", "media", "Other candidates' finance",
     "其他候选人财务", "15 rows for the other filed candidates."),
    ("07_electoral_context/election_results.csv", "context", "Election results", "选举结果",
     "26 rows: primaries, the runoff and the general."),
    ("07_electoral_context/county_results.csv", "context", "County results", "县级结果",
     "46 counties that sum exactly to the statewide total."),
    ("07_electoral_context/polling.csv", "context", "General-election polling", "大选民调",
     "20 rows including forecasters."),
    ("07_electoral_context/primary_polling.csv", "context", "Primary polling", "初选民调",
     "6 rows."),
    ("09_sources/exit_poll_2026.csv", "context", "Exit poll", "出口民调",
     "45 subgroups across 15 groups."),
    ("09_sources/sources.csv", "sources", "Sources", "来源",
     "370 sources with tier, type and a computed used_by citation map."),
]

# path, section, en title, zh title
DOCS = [
    ("08_comparative_analysis/candidate_comparison.md", "compare", "Candidate comparison", "候选人对比"),
    ("02_campaign_events/event_coverage_gaps.md", "sources", "Event coverage gaps", "活动覆盖缺口"),
    ("09_sources/data_dictionary_bilingual.md", "sources", "Data dictionary", "数据字典"),
    ("research_gaps.md", "sources", "Research gaps", "研究缺口"),
    ("_research_conventions.md", "sources", "Research conventions", "研究规范"),
    ("07_electoral_context/election_context.md", "context", "Electoral context", "选举语境"),
    ("07_electoral_context/results_notes.md", "context", "Results and reconciliation", "结果与对账"),
    ("03_speeches/communication_analysis_andrews.md", "speeches", "Communication analysis: Andrews",
     "传播分析：安德鲁斯"),
    ("03_speeches/communication_analysis_graham.md", "speeches", "Communication analysis: Graham",
     "传播分析：格雷厄姆"),
    ("01_candidates/andrews/biography.md", "candidates", "Biography: Andrews", "传记：安德鲁斯"),
    ("01_candidates/andrews/political_positions.md", "candidates", "Positions: Andrews", "立场：安德鲁斯"),
    ("01_candidates/graham/biography.md", "candidates", "Biography: Graham", "传记：格雷厄姆"),
    ("01_candidates/graham/political_positions.md", "candidates", "Positions: Graham", "立场：格雷厄姆"),
    ("02_campaign_events/andrews_timeline.md", "events", "Timeline: Andrews", "时间线：安德鲁斯"),
    ("02_campaign_events/graham_timeline.md", "events", "Timeline: Graham", "时间线：格雷厄姆"),
]

SECTION_TITLES = {
    "events": ("Campaign events and timelines", "竞选活动与时间线"),
    "candidates": ("The two candidates", "两位候选人"),
    "speeches": ("Speeches and communication", "演讲与传播"),
    "visual": ("Visual archive", "视觉档案"),
    "video": ("Video frames", "视频帧"),
    "audio": ("Audio measurements", "音频测量"),
    "media": ("Media coverage and money", "媒体报道与资金"),
    "context": ("Electoral context", "选举语境"),
    "compare": ("Comparative analysis", "对比分析"),
    "sources": ("Sources, dictionaries and gaps", "来源、字典与缺口"),
}

HEAD_LINES = {
    "events": ("Every documented appearance, plus the two timelines and an explicit account of what could not be found.",
               "每一项有记录的活动，加上两份时间线与一份关于缺失内容的明确说明。"),
    "candidates": ("Biographies, positions and career chronologies for Annie Andrews and Darline Graham.",
                   "安妮·安德鲁斯与达琳·格雷厄姆的传记、立场与生涯年表。"),
    "speeches": ("24 speeches, 22 video mappings, and two communication analyses built on caption transcripts.",
                 "24 篇演讲、22 条视频映射，以及两篇基于字幕文本的传播分析。"),
    "visual": ("52 photographs from the campaign and the vacancy period, with licence and resolution.",
               "52 张来自竞选期与空缺期的照片，含授权与分辨率。"),
    "video": ("27 videos, 300 keyframes and per-video face detection counts.",
              "27 个视频、300 个关键帧与逐视频人脸检出统计。"),
    "audio": ("Speech rate, silence ratio and caption coverage measured from the audio track of each video.",
              "从每个视频的音轨测得的语速、静音比与字幕覆盖。"),
    "media": ("55 coverage rows, 3 advertisement rows, 3 social posts and 20 finance rows across four FEC snapshots.",
              "55 条报道、3 条广告、3 条社交帖子，以及四个 FEC 时点上的 20 行财务数据。"),
    "context": ("Results, 46 counties, 26 polling rows and a 45-row exit poll.",
                "结果、46 个县、26 行民调与 45 行出口民调。"),
    "compare": ("What the two campaigns did differently, without a verdict on which worked.",
                "两场竞选做法上的差异，不对孰优孰劣下判断。"),
    "sources": ("370 sources with a computed citation graph, the column dictionary, and the gaps.",
                "370 条来源及其计算得出的引用图、列字典，以及缺口清单。"),
}


def esc(v):
    return html.escape(str(v), quote=False)


def md_body(path):
    text = open(path, encoding="utf-8").read()
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        text = text[m.end():]
    return meta, markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])


def slug_for(relpath, seen, sep="_"):
    if relpath == "README.md":
        return "overview"
    stem = os.path.basename(relpath)[:-3]
    slug = stem
    if slug in seen:
        slug = f"{os.path.basename(os.path.dirname(relpath))}{sep}{stem}"
    seen.add(slug)
    return slug


def data_slug(relpath, seen):
    stem = os.path.basename(relpath)[:-4]
    slug = stem
    if slug in seen:
        slug = f"{os.path.basename(os.path.dirname(relpath))}_{stem}"
    seen.add(slug)
    return slug


def shell(title, body, depth, active="", toc=None, wide=False):
    up = "../" * depth
    nav_items = []
    for target, zh, en, sid in NAV:
        href = up + (target if target.endswith(".html") else target + "index.html")
        cls = " on" if sid == active else ""
        nav_items.append(f'<a class="{cls.strip()}" href="{href}">{zh}'
                         f'<span style="opacity:.6;font-size:.78em"> {en}</span></a>')
    toc_html = ""
    if toc:
        items = "".join(f'<a class="h{t}" href="#{a}">{esc(t)}</a>' for t, a in toc)
        toc_html = f'<aside class="toc"><h4>本页 / On this page</h4>{items}</aside>'
    # The Texas stylesheet lays out 250px + 1fr; a page with no TOC must not sit in the 250px column.
    body_cls = "wide" if (wide or not toc) else ""
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} — {CASE_NO} · 双语档案</title>
<link rel="stylesheet" href="{up}assets/style.css">
<link rel="stylesheet" href="{up}assets/overrides.css">
</head><body class="{body_cls}">
<header class="top"><div class="top-in">
  <div class="brand">{CASE_NO} · 双语档案<small>{esc(CASE_EN)} / {CASE_ZH}</small></div>
  <nav class="main">{''.join(nav_items)}</nav>
  <div class="modes" role="group" aria-label="语言模式">
    <button data-mode="both" class="on">双语</button><button data-mode="en">EN</button><button data-mode="zh">中文</button>
  </div>
</div></header>
<div class="layout">
  {toc_html}
  <main>
{body}
  </main>
</div>
<footer><div class="in">
  <p>Compiled 2026-11-12. Every CSV row carries <code>SRC-####|https://...</code>; <code>unknown</code> is a value, not a gap.</p>
  <p>2026-11-12 编制。每个 CSV 行均带 <code>SRC-####|https://...</code>；<code>unknown</code> 是取值，不是缺失。</p>
</div></footer>
<script src="{up}assets/app.js"></script>
</body></html>
"""


def hero(title_en, title_zh, pairs, tags):
    cols = "".join(f'<div class="col {cls}"><p>{p}</p></div>' for cls, p in pairs)
    taghtml = "".join(f'<span class="tag">{esc(t)}</span>' for t in tags)
    return f"""<div class="hero">
  <h1 style="font-size:2rem">{esc(title_en)}<span class="zh" style="font-size:1rem">{esc(title_zh)}</span></h1>
  <div class="pair">{cols}</div>
  <p style="margin-top:.5rem">{taghtml}</p>
</div>"""


def stat_grid(items):
    return '<div class="stats">' + "".join(
        f'<div class="stat"><b>{esc(n)}</b><span>{esc(label)}</span></div>' for n, label in items) + "</div>"


def card_grid(cards):
    return '<div class="cards">' + "".join(
        f'<a class="card" href="{href}"><span class="n">{esc(n)}</span><h3>{esc(t_en)}'
        f'<span class="zh" style="display:block;font-size:.85em">{esc(t_zh)}</span></h3>'
        f'<p>{esc(desc)}</p></a>'
        for href, n, t_en, t_zh, desc in cards) + "</div>"


def image_rows():
    path = os.path.join(ROOT, "04_visual_archive", "image_archive.csv")
    return list(csv.DictReader(open(path, encoding="utf-8"))) if os.path.exists(path) else []


def gallery_items():
    """Map each image_archive row to the file actually on disk (files carry an image_id prefix)."""
    path = os.path.join(ROOT, "04_visual_archive", "image_archive.csv")
    out = []
    if not os.path.exists(path):
        return out
    for r in csv.DictReader(open(path, encoding="utf-8")):
        folder = os.path.join(ROOT, "04_visual_archive", os.path.dirname(r["local_filename"]))
        stem = os.path.splitext(os.path.basename(r["local_filename"]))[0]
        hit = None
        if os.path.isdir(folder):
            files = sorted(os.listdir(folder))
            for f in files:
                if f.startswith(r["image_id"] + "_") or os.path.splitext(f)[0] == stem:
                    hit = os.path.join(folder, f)
                    break
        if hit:
            out.append((r, hit))
    return out


def gallery_html(items, page_dir, limit=None):
    figs = []
    for r, path in (items[:limit] if limit else items):
        src = os.path.relpath(path, page_dir).replace(os.sep, "/")
        cap = (f'{esc(r["candidate_id"])} · {esc(r["image_date"])} · {esc(r["event_category"])} · '
               f'{esc(r["image_resolution"])}')
        note = esc(r.get("notes", "")[:190])
        figs.append(f'<figure><a href="{src}"><img loading="lazy" src="{src}" alt="{esc(r["image_id"])}"></a>'
                    f'<figcaption><b>{cap}</b><br>{note}</figcaption></figure>')
    return '<div class="gal">' + "".join(figs) + "</div>"


def frame_rows():
    path = os.path.join(ROOT, "10_video_frames", "keyframes.csv")
    if not os.path.exists(path):
        return {}
    by_video = {}
    for r in csv.DictReader(open(path, encoding="utf-8")):
        by_video.setdefault(r["slug"], []).append(r)
    for slug in by_video:
        by_video[slug].sort(key=lambda r: r["file"])
    return by_video


def identity_map():
    path = os.path.join(ROOT, "10_video_frames", "keyframes_identity.csv")
    if not os.path.exists(path):
        return {}
    return {r["frame_id"]: r for r in csv.DictReader(open(path, encoding="utf-8"))}


IDENT_LABEL = {"ANDREWS": "安德鲁斯 / Andrews", "GRAHAM": "格雷厄姆 / Graham"}


def identity_badge(frame, ident):
    row = ident.get(frame["frame_id"])
    if not row:
        return ""
    who = row.get("identity", "unknown")
    sim = row.get("identity_sim", "unknown")
    if who in IDENT_LABEL:
        return f'<b class="idtag id-{who.lower()}">{IDENT_LABEL[who]} · {esc(sim)}</b>'
    if who == "noface":
        return '<span class="idtag">无人脸 / no face</span>'
    return '<span class="idtag">未识别 / unidentified</span>'


def candidate_frames(frames, ident, limit=4):
    """Preview strip: the candidate's own frames first; strangers only if no candidate was found."""
    hits = [f for f in frames if ident.get(f["frame_id"], {}).get("identity") in IDENT_LABEL]
    return hits[:limit] if hits else frames[:limit]


def video_rows():
    path = os.path.join(ROOT, "10_video_frames", "video_sources.csv")
    return list(csv.DictReader(open(path, encoding="utf-8"))) if os.path.exists(path) else []


def shots_html(frames, page_dir, ident, limit=4):
    cells = []
    for r in frames[:limit]:
        src = os.path.relpath(os.path.join(ROOT, "10_video_frames", r["file"]), page_dir).replace(os.sep, "/")
        cells.append(f'<a href="{src}"><img loading="lazy" src="{src}" alt="{esc(r["frame_id"])}"></a>'
                     f'<span>{esc(r["timecode"])} {identity_badge(r, ident)}</span>')
    return '<div class="shots">' + "".join(cells) + "</div>"


def table_page(relpath, depth, filter_id):
    rows = list(csv.reader(open(os.path.join(ROOT, relpath), encoding="utf-8-sig")))
    header, body = rows[0], [r for r in rows[1:] if r]
    out = [f'<div class="search"><input data-filter="{filter_id}" '
           f'placeholder="过滤行：输入县名、日期、候选人、SRC 编号…… / Filter rows"></div>',
           f'<div class="table-wrap"><table id="{filter_id}"><thead><tr>']
    out += [f"<th>{esc(h)}</th>" for h in header]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>" + "".join(
            f'<td{" class=\"nolink\"" if (i < len(r) and r[i].strip() == "unknown") else ""}>'
            f"{esc(r[i] if i < len(r) else '')}</td>" for i in range(len(header))) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def build():
    if not os.path.exists(TX_CSS):
        print("missing Texas stylesheet; run the extractor first")
        return 1
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
    shutil.copyfile(TX_CSS, os.path.join(SITE, "assets", "style.css"))
    open(os.path.join(SITE, "assets", "app.js"), "w", encoding="utf-8", newline="\n").write(JS)
    open(os.path.join(SITE, "assets", "overrides.css"), "w", encoding="utf-8", newline="\n").write(OVERRIDES)
    print("assets: style.css (from Texas), app.js")

    seen_doc, seen_data = set(), set()
    doc_pages = {p: f"docs/{slug_for(p, seen_doc)}.html" for p, *_ in DOCS}
    data_pages = {p: f"data/{data_slug(p, seen_data)}.html" for p, *_ in DATASETS}

    # --- data pages
    os.makedirs(os.path.join(SITE, "data"), exist_ok=True)
    for relpath, section, en, zh, desc in DATASETS:
        src = os.path.join(ROOT, relpath)
        if not os.path.exists(src):
            continue
        n = max(0, sum(1 for _ in open(src, encoding="utf-8-sig")) - 1)
        fid = "tbl-" + re.sub(r"[^a-z0-9]+", "-", os.path.basename(relpath).lower())
        body = hero(en, zh, [("en", desc), ("zh", f"{zh}：{desc}")],
                    [f"{n} rows", relpath, "CSV"])
        body += table_page(relpath, 1, fid)
        out = os.path.join(SITE, data_pages[relpath].replace("/", os.sep))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8", newline="\n").write(
            shell(f"{en} / {zh}", body, 1, section, wide=True))
    print(f"data pages: {len(data_pages)}")

    # --- doc pages
    os.makedirs(os.path.join(SITE, "docs"), exist_ok=True)
    for relpath, section, en, zh in DOCS:
        src = os.path.join(ROOT, relpath)
        if not os.path.exists(src):
            print(f"  missing {relpath}")
            continue
        meta, body = md_body(src)
        wrapped = (f'<div class="crumb"><a href="../index.html">首页</a> / {esc(en)}</div>'
                   f'<div class="meta">{esc(relpath)} · {esc(meta.get("last_updated", "unknown"))}</div>'
                   f'{body}')
        out = os.path.join(SITE, doc_pages[relpath].replace("/", os.sep))
        open(out, "w", encoding="utf-8", newline="\n").write(
            shell(f"{en} / {zh}", wrapped, 1, section))
    print(f"doc pages: {len(doc_pages)}")

    # --- section hubs
    for target, zh, en, sid in NAV:
        if not target.endswith("/"):
            continue
        sec = target.strip("/")
        t_en, t_zh = SECTION_TITLES[sec]
        lede_en, lede_zh = HEAD_LINES.get(sec, ("", ""))
        ds = [d for d in DATASETS if d[1] == sec]
        dc = [d for d in DOCS if d[1] == sec]
        cards = []
        for relpath, _, den, dzh, desc in ds:
            n = max(0, sum(1 for _ in open(os.path.join(ROOT, relpath), encoding="utf-8-sig")) - 1)
            cards.append(("../" + data_pages[relpath], f"{n}", den, dzh, desc))
        for relpath, _, den, dzh in dc:
            cards.append(("../" + doc_pages[relpath], "MD", den, dzh, "Bilingual document."))
        body = hero(t_en, t_zh, [("en", lede_en), ("zh", lede_zh)],
                    [f"{len(ds)} datasets", f"{len(dc)} documents"])
        if cards:
            body += '<h2>Contents</h2>' + card_grid(cards)
        else:
            body += ('<p class="warn">这一部分尚在编写中 / This section is still being written.</p>')
        page_dir = os.path.join(SITE, sec)
        if sec == "visual":
            items = gallery_items()
            body += (f'<h2>照片 / Photographs</h2><p class="meta">{len(items)} files on disk, '
                     f'shown at full size when clicked.</p>' + gallery_html(items, page_dir))
            shown = {r["image_id"] for r, _ in items}
            absent = [r for r in image_rows() if r["image_id"] not in shown]
            if absent:
                rows_html = "".join(
                    f'<li>{esc(r["image_id"])} · {esc(r["candidate_id"])} · {esc(r["image_date"])} — '
                    f'<a href="{esc(r["original_image_url"])}">Commons 原始文件 / original file</a></li>'
                    for r in absent)
                body += (f'<h2>未下载 / Not fetched</h2>'
                         f'<p class="meta">These rows are documented but Wikimedia rate-limited the download '
                         f'(HTTP 429). The links go straight to the file.</p>'
                         f'<ul>{rows_html}</ul>')
        if sec == "video":
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
                cand = candidate_frames(frames, ident, limit=len(frames))
                link = f'<a href="{esc(v["slug"])}.html">候选人帧 {len(cand)} / 全部 {len(frames)} 帧</a>'
                if cand:
                    strip = shots_html(cand[:4], page_dir, ident)
                else:
                    strip = '<p class="meta">没有识别出候选人的画面 / no candidate frame attributed</p>'
                blocks.append(f'<h3>{esc(v["title"])}</h3>'
                              f'<p class="meta">{esc(v["candidate_source"])} · {esc(v["kind"])} · '
                              f'{esc(v["duration_s"])}s · {esc(v["upload_date"])} · {link}</p>'
                              f'<p class="meta">{summary}</p>'
                              + strip)
            body += ('<h2>逐视频帧 / Frames by video</h2><p class="meta">First four detected keyframes per '
                     'video; every frame page carries face counts and timecodes.</p>' + "".join(blocks))
        out = os.path.join(page_dir, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8", newline="\n").write(shell(f"{t_en} / {t_zh}", body, 1, sid))
    print("section hubs: 10")

    # --- per-video frame pages
    by_video = frame_rows()
    vdir = os.path.join(SITE, "video")
    made = 0
    for v in video_rows():
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
                + gallery)
        open(os.path.join(vdir, f'{v["slug"]}.html'), "w", encoding="utf-8", newline="\n").write(
            shell(f'{v["title"]}', body, 1, "video"))
        made += 1
    print(f"video frame pages: {made}")

    # --- overview
    totals = sum(max(0, sum(1 for _ in open(os.path.join(ROOT, p), encoding="utf-8-sig")) - 1)
                 for p, *_ in DATASETS if os.path.exists(os.path.join(ROOT, p)))
    src_rows = max(0, sum(1 for _ in open(os.path.join(ROOT, "09_sources/sources.csv"),
                                          encoding="utf-8-sig")) - 1)
    facts = [
        ("Result / 结果", "Andrews 1,044,001 (51.14%) to Graham 952,191 (46.64%); 2,041,487 votes cast.",
         "安德鲁斯 1,044,001 票（51.14%），格雷厄姆 952,191 票（46.64%）；总投票 2,041,487。"),
        ("First since 1998 / 1998 年以来首次", "The first Democrat elected to this Senate seat since 1998.",
         "该参议院席位自 1998 年以来选出的第一位民主党人。"),
        ("A vacancy, not a normal cycle / 不是常规周期，而是空缺",
         "Lindsey Graham died 2026-07-11; Darline Graham was appointed 07-13, sworn in 07-14, won a "
         "ten-candidate special primary and a runoff, then lost the general.",
         "林赛·格雷厄姆于 2026-07-11 去世；达琳·格雷厄姆 07-13 受任命、07-14 宣誓，赢下十人特别初选与决选，随后输掉大选。"),
        ("Money / 资金",
         "As of 2026-10-14: Andrews $24,216,841 raised, Graham $1,917,646 — 12.6:1. Outside money "
         "favoured Graham: SLF $5M, MAGA Inc. $827,000.",
         "截至 2026-10-14：安德鲁斯筹得 24,216,841 美元，格雷厄姆 1,917,646 美元——12.6:1。外部资金偏向格雷厄姆：SLF 500 万美元、MAGA Inc. 82.7 万美元。"),
        ("Debates / 辩论", "Graham took part in four televised debates; Andrews in one.",
         "格雷厄姆参加四场电视辩论；安德鲁斯一场。"),
    ]
    fact_html = "".join(
        f'<div class="blk mix"><h3>{esc(h)}</h3><div class="pair">'
        f'<div class="col en"><p>{esc(en)}</p></div><div class="col zh"><p>{esc(zh)}</p></div></div></div>'
        for h, en, zh in facts)
    cards = []
    for target, zh, en, sid in NAV[1:-1]:
        sec = target.strip("/")
        n_ds = len([d for d in DATASETS if d[1] == sec])
        n_dc = len([d for d in DOCS if d[1] == sec])
        cards.append((target + "index.html", f"{n_ds + n_dc}", en, zh, HEAD_LINES.get(sec, ("", ""))[0]))
    body = hero(
        "South Carolina Senate 2026",
        "2026 南卡罗来纳州联邦参议员选举",
        [("en", "Andrews versus Darline Graham: a senator dies mid-cycle, his sister is appointed, and the "
                "state elects its first Democratic senator since 1998."),
         ("zh", "安德鲁斯对达琳·格雷厄姆：一位在任参议员在周期中途去世，其妹受任命，该州选出 1998 年以来首位民主党参议员。")],
        [f"{totals:,} CSV rows", f"{src_rows} sources", "32 events", "27 videos", "300 keyframes", "EN + 中文"])
    body += stat_grid([(f"{totals:,}", "CSV 行数 / rows"), (f"{src_rows}", "来源 / sources"),
                       ("32", "活动 / events"), ("27", "视频 / videos"), ("300", "关键帧 / frames"),
                       ("46", "县 / counties")])
    body += '<h2>核心事实 / Key facts</h2>' + fact_html
    body += '<h2>档案分区 / Sections</h2>' + card_grid(cards)
    body += ('<div class="search"><input id="q" placeholder="站内检索：输入人名、县名、关键词……">'
             '<div id="results"></div></div>')
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8", newline="\n").write(
        shell("总览 / Overview", body, 0, "home", wide=True))
    print("index.html")

    # --- about
    about = """<div class="crumb"><a href="index.html">首页</a> / 关于档案</div>
<h1>这套档案是怎么做的<span class="zh">How this archive was built</span></h1>
<h2>采集 / Collection</h2>
<p>The Wikipedia race article supplied the skeleton: 63 sections and 534 cited URLs were mirrored to disk, parsed into
county, polling and finance tables, then cross-checked against CBS's results reporting and the FEC tables quoted in the
sources. Video came from yt-dlp searches plus a curated list of 27 uploads, downloaded at 720p (480p for the two
hour-long debates).</p>
<p>维基百科的选举条目提供了骨架：63 个章节与 534 条引用 URL 被镜像到本地，解析出县级、民调与财务表，再与 CBS 的
结果报道以及来源中引用的 FEC 表格交叉核对。视频来自 yt-dlp 搜索与手工筛选的 27 条上传，720p 下载（两场一小时的辩论为 480p）。</p>
<h2>校验 / Verification</h2>
<p><code>_staging/_lead_validate.py</code> enforces header conformance, field counts, no blank cells, controlled
vocabularies, ISO dates, and an <code>SRC-####</code> token plus URL in every row. The archive passes with zero hard
failures.</p>
<p><code>_staging/_lead_validate.py</code> 强制表头一致、字段数、无空单元格、受控词表、ISO 日期，以及每行都带
<code>SRC-####</code> 与 URL。档案目前以零硬失败通过。</p>
<h2>等级规则 / Tier rules</h2>
<p><code>T1</code> official records (.gov domains, SCETV debate video); <code>T2</code> established news organisations;
<code>T3</code> everything else, including Wikipedia, advocacy sites and social posts. Tier is assigned from the domain
mechanically: it describes the venue, not the accuracy of a claim.</p>
<p><code>T1</code> 官方记录（.gov 域、SCETV 辩论视频）；<code>T2</code> 既有新闻机构；<code>T3</code> 其余，包括
维基百科、倡议组织网站与社交帖子。等级按域名机械判定：它描述发表场所，而非某条主张的准确性。</p>
<h2>与德州案例的关系 / Relation to the Texas case</h2>
<p>Both cases use the same components and the same stylesheet, so a reader moving between them does not have to learn a
second interface. The data models differ where the races differ: South Carolina adds <code>actor_note</code> and
<code>vacancy_context</code> because a death and an appointment sit inside its event sequence.</p>
<p>两个案例使用同一套组件与同一份样式表，读者在两个案例之间切换时不必重新适应界面。数据模型随选举不同而不同：南卡增加了
<code>actor_note</code> 与 <code>vacancy_context</code>，因为其事件序列中包含一次死亡与一次任命。</p>
"""
    open(os.path.join(SITE, "about.html"), "w", encoding="utf-8", newline="\n").write(
        shell("关于档案 / About", about, 0, "about"))
    print("about.html")
    return 0


OVERRIDES = """/* widen the reading column; the Texas grid is 250px + 1fr with a 1280px cap */
.layout{max-width:1500px}
.idtag{display:inline-block;padding:.05rem .35rem;border-radius:4px;font-size:.72em;font-weight:600;
  background:var(--line);color:var(--fg);margin-left:.25rem;white-space:nowrap}
.idtag.id-andrews{background:#123a5f;color:#fff}
.idtag.id-graham{background:#7a1f1f;color:#fff}
.facetbar{display:flex;gap:.4rem;flex-wrap:wrap;margin:1rem 0 .6rem}
.facetbar button{border:1px solid var(--line);background:var(--card);color:var(--muted);
  padding:.3rem .7rem;border-radius:999px;font-size:.82rem;cursor:pointer}
.facetbar button.on{background:var(--accent2);border-color:var(--accent2);color:#fff}
body.wide .layout{max-width:1500px}
@media (min-width:1560px){.layout,body.wide .layout{max-width:1640px}}
.prose img{max-width:100%;height:auto}
"""


JS = """(function(){
  var body=document.body;
  function setMode(m){
    body.classList.remove('mode-en','mode-zh');
    if(m==='en')body.classList.add('mode-en');
    if(m==='zh')body.classList.add('mode-zh');
    document.querySelectorAll('.modes button').forEach(function(b){b.classList.toggle('on',b.dataset.mode===m)});
    try{localStorage.setItem('dsh-mode',m)}catch(e){}
  }
  document.querySelectorAll('.modes button').forEach(function(b){
    b.addEventListener('click',function(){setMode(b.dataset.mode)});
  });
  var saved='both'; try{saved=localStorage.getItem('dsh-mode')||'both'}catch(e){}
  setMode(saved);

  document.querySelectorAll('[data-facet-group]').forEach(function(group){
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

  document.querySelectorAll('[data-filter]').forEach(function(inp){
    var tbl=document.getElementById(inp.dataset.filter);
    if(!tbl)return;
    inp.addEventListener('input',function(){
      var q=inp.value.toLowerCase();
      tbl.querySelectorAll('tbody tr').forEach(function(tr){
        tr.style.display=tr.textContent.toLowerCase().indexOf(q)>-1?'':'none';
      });
    });
  });
})();
"""


if __name__ == "__main__":
    sys.exit(build())
