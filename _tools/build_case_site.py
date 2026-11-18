#!/usr/bin/env python3
"""Build a small static site for one batch-2 case archive.

Usage: python _tools/build_case_site.py <case-slug> [--out DIR]

Pages produced inside <case>/site/:
  index.html            hero, stats, result table, dataset cards, portrait gallery
  data/index.html       dataset index
  data/<csv>.html       one table per dataset, SRC cells rendered as links
  docs/index.html       document index
  docs/<name>.html      markdown rendered
  sources/index.html    full source table
Nothing in the case folder is modified except the new site/ tree.

Design language is shared with the two earlier cases (assets/style.css copied from
_tools/case_style.css), so the portal can drop these pages in unchanged.
"""
import csv
import html
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.dirname(os.path.abspath(__file__))

NAV = [("index.html", "总览", "Overview"), ("data/index.html", "数据", "Data"),
       ("video/index.html", "视频", "Video"), ("docs/index.html", "文档", "Docs"),
       ("sources/index.html", "来源", "Sources")]

MAIN_DATASETS = [
    ("07_electoral_context/election_results.csv", "选举结果", "Election results"),
    ("07_electoral_context/polling.csv", "民调", "Polling"),
    ("07_electoral_context/county_results.csv", "县级结果", "County results"),
    ("02_campaign_events/campaign_events.csv", "竞选活动", "Campaign events"),
    ("01_candidates/policy_positions.csv", "政策立场", "Policy positions"),
    ("03_speeches/speech_archive.csv", "演讲", "Speeches"),
    ("03_speeches/speech_video_index.csv", "视频索引", "Video index"),
    ("05_campaign_media/advertisements.csv", "广告", "Advertisements"),
    ("05_campaign_media/media_coverage.csv", "媒体报道", "Media coverage"),
    ("05_campaign_media/social_media.csv", "社交媒体", "Social media"),
    ("06_campaign_finance/campaign_finance.csv", "竞选资金", "Campaign finance"),
    ("04_visual_archive/image_archive.csv", "图像档案", "Image archive"),
]


def esc(v):
    return html.escape(str(v), quote=True)


def read_rows(path):
    if not os.path.exists(path):
        return [], []
    with open(path, encoding="utf-8-sig", newline="") as f:
        r = csv.reader(f)
        try:
            header = next(r)
        except StopIteration:
            return [], []
        rows = [dict(zip(header, row)) for row in r if len(row) == len(header)]
    return header, rows


def md_to_html(md):
    """Small, dependency-free renderer for the subset used by these archives."""
    lines = md.split("\n")
    out, i = [], 0
    in_code, code_buf = False, []
    in_list = None
    para = []

    def inline(s):
        s = esc(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
                   r'<a class="ext" href="\2" target="_blank" rel="noopener">\1</a>', s)
        s = re.sub(r"\[(SRC-\d{4})\]", r'<span class="src">\1</span>', s)
        return s

    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append(f"</{in_list}>")
            in_list = None

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush_para(); flush_list()
            if in_code:
                out.append("<pre><code>" + esc("\n".join(code_buf)) + "</code></pre>")
                code_buf, in_code = [], False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line); i += 1; continue
        if not line.strip():
            flush_para(); flush_list(); i += 1; continue
        if line.startswith("---") and i < 3:
            i += 1
            while i < len(lines) and lines[i].strip() != "---":
                i += 1
            i += 1; continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush_para(); flush_list()
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1; continue
        if re.match(r"^\s*[-*]\s+", line):
            flush_para()
            if in_list != "ul":
                flush_list(); out.append("<ul>"); in_list = "ul"
            out.append("<li>" + inline(re.sub(r"^\s*[-*]\s+", "", line)) + "</li>")
            i += 1; continue
        if re.match(r"^\s*\d+\.\s+", line):
            flush_para()
            if in_list != "ol":
                flush_list(); out.append("<ol>"); in_list = "ol"
            out.append("<li>" + inline(re.sub(r"^\s*\d+\.\s+", "", line)) + "</li>")
            i += 1; continue
        if line.startswith(">"):
            flush_para(); flush_list()
            out.append("<blockquote>" + inline(line.lstrip("> ")) + "</blockquote>")
            i += 1; continue
        if line.lstrip().startswith("|") and i + 1 < len(lines) and re.match(
                r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1]):
            flush_para(); flush_list()
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            body = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                body.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append('<div class="table-wrap"><table><thead><tr>' +
                       "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr></thead><tbody>")
            for row in body:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
            out.append("</tbody></table></div>")
            continue
        para.append(line.strip())
        i += 1
    flush_para(); flush_list()
    if in_code:
        out.append("<pre><code>" + esc("\n".join(code_buf)) + "</code></pre>")
    return "\n".join(out)


def page(title, body, depth=0, active=""):
    up = "../" * depth
    nav = "".join(
        f'<a class="{"on" if href == active else ""}" href="{up}{href}">{zh}<span style="opacity:.6;font-size:.78em"> {en}</span></a>'
        for href, zh, en in NAV)
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<link rel="stylesheet" href="{up}assets/style.css">
</head><body class="wide">
<header class="top"><div class="top-in">
  <div class="brand">{esc(title)}<small>2026 archive · bilingual</small></div>
  <nav class="main">{nav}</nav>
</div></header>
<div class="layout"><main>
{body}
</main></div>
<footer><div class="in">
  <p>Every CSV row carries <code>SRC-####|https://...</code>; <code>unknown</code> is a value, not a gap.</p>
  <p>每个 CSV 行均带 <code>SRC-####|https://...</code>；<code>unknown</code> 是取值，不是缺失。</p>
</div></footer>
</body></html>"""


def render_cell(col, val):
    if col == "source_urls" or col in ("url", "speech_url", "video_url", "source_url", "original_image_url"):
        m = re.match(r"^(SRC-\d{4})\|(https?://\S+)$", val)
        if m:
            return f'<a class="src" href="{esc(m.group(2))}" target="_blank" rel="noopener">{m.group(1)}</a>'
        if val.startswith(("http://", "https://")):
            return f'<a class="ext" href="{esc(val)}" target="_blank" rel="noopener">{esc(val[:70])}</a>'
    return esc(val)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    slug = argv[1]
    out = None
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    case_dir = slug if os.path.isdir(slug) else os.path.join(ROOT, slug)
    meta = __import__("json").load(open(os.path.join(case_dir, "_staging", "case_meta.json"), encoding="utf-8"))
    site = out or os.path.join(case_dir, "site")
    if os.path.isdir(site) and out is None:
        shutil.rmtree(site)
    os.makedirs(os.path.join(site, "assets"), exist_ok=True)
    shutil.copyfile(os.path.join(TOOLS, "case_style.css"), os.path.join(site, "assets", "style.css"))

    result_header, results = read_rows(os.path.join(case_dir, "07_electoral_context/election_results.csv"))
    events_h, events = read_rows(os.path.join(case_dir, "02_campaign_events/campaign_events.csv"))
    polls_h, polls = read_rows(os.path.join(case_dir, "07_electoral_context/polling.csv"))
    images_h, images = read_rows(os.path.join(case_dir, "04_visual_archive/image_archive.csv"))
    sources_h, sources = read_rows(os.path.join(case_dir, "09_sources/sources.csv"))

    total_rows = 0
    for folder in os.listdir(case_dir):
        sub = os.path.join(case_dir, folder)
        if not os.path.isdir(sub) or folder in ("site", "_staging"):
            continue
        for name in os.listdir(sub):
            if name.endswith(".csv"):
                total_rows += max(0, sum(1 for _ in open(os.path.join(sub, name),
                                                         encoding="utf-8-sig")) - 1)

    # Decisive contest: prefer race ids containing GENERAL; otherwise the latest dated race with a winner.
    general = [r for r in results if "GENERAL" in r.get("race_id", "").upper()]
    if not general and results:
        winners = [r for r in results if r.get("winner") == "yes"]
        if winners:
            latest = max(r.get("election_date", "") for r in winners)
            general = [r for r in results if r.get("election_date") == latest]
    final_ids = {r.get("race_id") for r in general if r.get("winner") == "yes"} or \
                {r.get("race_id") for r in general}
    finals = [r for r in results if r.get("race_id") in final_ids
              and not r.get("candidate", "").lower().startswith(("total", "write-in"))]

    def fmt_votes(v):
        return f"{int(v):,}" if str(v).isdigit() else str(v)

    def result_line(name):
        for r in finals:
            if r.get("candidate") == name:
                return fmt_votes(r.get("votes", "unknown")) + " votes · " + r.get("percentage", "unknown") + "%"
        return "result not on this page"

    cand_cards = "".join(
        '<div class="card"><h3>' + esc(c["name"]) + '<br><small style="color:var(--muted);font-weight:400">'
        + esc(c["party"]) + "</small></h3><p>" + esc(result_line(c["name"]))
        + '</p><p><a href="data/election_results.html">结果行 / result row</a></p></div>'
        for c in meta["candidates"])

    gallery = ""
    pics = [r for r in images if r.get("local_filename") not in ("unknown", "", None)]
    img_out = os.path.join(site, "assets", "img")
    os.makedirs(img_out, exist_ok=True)
    for r in pics[:8]:
        src = os.path.join(case_dir, r["local_filename"])
        if not os.path.exists(src):
            src = os.path.join(case_dir, "04_visual_archive", r["local_filename"])
        if not os.path.exists(src):
            continue
        ext = os.path.splitext(src)[1].lower() or ".jpg"
        name = r.get("image_id", "img") + ext
        shutil.copyfile(src, os.path.join(img_out, name))
        gallery += (f'<figure><img src="assets/img/{esc(name)}" alt="{esc(r.get("candidate_id",""))}" '
                    f'loading="lazy"><figcaption><b>{esc(r.get("candidate_id",""))}</b> '
                    f'{esc(r.get("clothing_notes") if r.get("clothing_notes") not in ("unknown", "", None) else r.get("image_date", ""))}'
                    f'</figcaption></figure>')
    gallery_block = f'<h2>图像 / Images</h2><div class="gal">{gallery}</div>' if gallery else ""

    stats = [
        (total_rows, "CSV 行数 / rows"), (len(sources), "来源 / sources"),
        (len(events), "活动 / events"), (len(results), "结果行 / results"),
        (len(polls), "民调 / polls"), (len(images), "图像 / images"),
    ]
    stat_html = "".join(f"<div class='stat'><b>{n:,}</b><span>{esc(l)}</span></div>" for n, l in stats)

    cards = "".join(
        f'<a class="card" href="data/{os.path.splitext(os.path.basename(rel))[0]}.html">'
        f'<h3>{zh}<br><small style="color:var(--muted);font-weight:400">{en}</small></h3>'
        f'<p>{len(read_rows(os.path.join(case_dir, rel))[1])} rows</p></a>'
        for rel, zh, en in MAIN_DATASETS)

    res_rows = ""
    for r in finals:
        cells = "".join(f"<td>{render_cell(c, r.get(c,''))}</td>" for c in
                        ("race_name", "candidate", "party"))
        cells += f"<td>{esc(fmt_votes(r.get('votes','')))}</td>"
        cells += "".join(f"<td>{render_cell(c, r.get(c,''))}</td>" for c in ("percentage", "winner"))
        res_rows += "<tr>" + cells + "</tr>"

    doc_links = ""
    for rel, label in (("README.md", "README"), ("research_gaps.md", "research gaps")):
        if os.path.exists(os.path.join(case_dir, rel)):
            doc_links += f'<a href="docs/{os.path.splitext(rel)[0]}.html">{label}</a> '
    read_line = (f'<p style="margin-top:1rem">Read the case narrative and limits in {doc_links}</p>'
                 if doc_links else "")

    body = f"""
<div class="hero">
  <h1>{esc(meta["race_name"])}<span class="zh" style="font-size:1rem">{esc(meta["race_name_zh"])}</span></h1>
  <p>{esc(meta["candidates"][0]["name"])} ({esc(meta["candidates"][0]["party"][:3])}) vs
     {esc(meta["candidates"][1]["name"])} ({esc(meta["candidates"][1]["party"][:3])}) · election day {esc(meta["election_date"])}</p>
  <p><span class="tag">{total_rows:,} CSV rows</span><span class="tag">{len(sources)} sources</span>
     <span class="tag">{len(events)} events</span><span class="tag">EN + 中文</span></p>
</div>
<div class="method" style="background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:0 0 1.4rem">
  <p><strong>研究切入点 / Research hook.</strong> {esc(meta.get("phenomenon_zh", ""))} {esc(meta.get("phenomenon_en", ""))}</p>
  <p style="color:var(--muted);font-size:.9em">This is a question the archive is meant to inform, not a finding. The
  repository-level note <code>2026-image-and-message-notes.md</code> records what the evidence can and cannot support.</p>
</div>
<div class="stats">{stat_html}</div>
<h2>候选人 / Candidates</h2>
<div class="cards">{cand_cards}</div>
<h2>大选结果 / General result</h2>
<div class="table-wrap"><table><thead><tr><th>Race</th><th>Candidate</th><th>Party</th><th>Votes</th><th>%</th><th>Winner</th></tr></thead>
<tbody>{res_rows}</tbody></table></div>
{gallery_block}
<h2>档案分区 / Datasets</h2>
<div class="cards">{cards}</div>
{read_line}
"""
    write(os.path.join(site, "index.html"), page(meta["race_name_zh"], body, 0, "index.html"))

    # dataset index + pages
    all_csv = []
    for base, dirs, files in os.walk(case_dir):
        dirs[:] = [x for x in dirs if x not in ("site", "_staging", "mirrors")]
        for name in sorted(files):
            if name.endswith(".csv") and not base.endswith("09_sources"):
                all_csv.append(os.path.relpath(os.path.join(base, name), case_dir).replace(os.sep, "/"))
    idx_cards = ""
    page_names = {}
    used = set()
    for rel in all_csv:
        base = os.path.splitext(os.path.basename(rel))[0]
        parent = os.path.basename(os.path.dirname(rel))
        name = base
        if name in used:
            name = f"{parent}_{base}"
        used.add(name)
        page_names[rel] = name
        h, rows = read_rows(os.path.join(case_dir, rel))
        idx_cards += (f'<a class="card" href="{name}.html">'
                      f'<h3>{esc(os.path.basename(rel))}</h3><p>{esc(rel)} · {len(rows)} rows · {len(h)} columns</p></a>')
    write(os.path.join(site, "data", "index.html"),
          page("数据 / Data", f"<h1>数据 / Data</h1><div class='cards'>{idx_cards}</div>", 1, "data/index.html"))

    for rel in all_csv:
        h, rows = read_rows(os.path.join(case_dir, rel))
        head = "".join(f"<th>{esc(c)}</th>" for c in h)
        body_rows = ""
        for r in rows:
            body_rows += "<tr>" + "".join(f"<td>{render_cell(c, r.get(c,''))}</td>" for c in h) + "</tr>"
        write(os.path.join(site, "data", page_names[rel] + ".html"),
              page(os.path.basename(rel),
                   f'<div class="crumb"><a href="index.html">数据 / Data</a> / {esc(rel)}</div>'
                   f'<h1>{esc(os.path.basename(rel))}</h1><p class="meta">{len(rows)} rows · {len(h)} columns · '
                   f'<a href="../../{esc(rel.replace(os.sep, "/"))}">raw CSV</a></p>'
                   f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body_rows}</tbody></table></div>',
                   1, "data/index.html"))

    # video keyframes + face identity
    vdir = os.path.join(case_dir, "10_video_frames")
    _, vids = read_rows(os.path.join(vdir, "video_sources.csv"))
    _, kfs = read_rows(os.path.join(vdir, "keyframes.csv"))
    _, kid = read_rows(os.path.join(vdir, "keyframes_identity.csv"))
    _, fsum = read_rows(os.path.join(vdir, "video_face_summary.csv"))
    idmap = {r["frame_id"]: r for r in kid}
    summap = {r["slug"]: r for r in fsum}
    kf_out = os.path.join(site, "assets", "kf")
    vcards, kgal = "", ""
    by_slug = {}
    for r in kfs:
        by_slug.setdefault(r["slug"], []).append(r)
    for v in vids:
        slug = v["slug"]
        s = summap.get(slug, {})
        vcards += (f'<a class="card" href="{esc(v.get("url",""))}" target="_blank" rel="noopener">'
                   f'<h3>{esc(v.get("title","")[:90])}</h3><p>{esc(v.get("channel",""))} · '
                   f'{esc(v.get("upload_date",""))} · {esc(v.get("duration_s",""))}s · '
                   f'{esc(s.get("frames_with_face","unknown"))}/{esc(s.get("frames_extracted","unknown"))} frames with faces</p></a>')
        frames = by_slug.get(slug, [])[:6]
        if not frames:
            continue
        thumbs = ""
        for f in frames:
            src = os.path.join(case_dir, "10_video_frames", f["file"])
            if not os.path.exists(src):
                continue
            outdir = os.path.join(kf_out, slug)
            os.makedirs(outdir, exist_ok=True)
            fn = os.path.basename(f["file"])
            shutil.copyfile(src, os.path.join(outdir, fn))
            ident = idmap.get(f["frame_id"], {})
            label = ident.get("identity", "unknown")
            sim = ident.get("identity_sim", "")
            thumbs += (f'<figure><img src="../assets/kf/{esc(slug)}/{esc(fn)}" loading="lazy" alt="{esc(label)}">'
                       f'<figcaption><b>{esc(label)}</b> {esc(sim)} · {esc(f.get("timecode",""))}</figcaption></figure>')
        kgal += (f'<h2>{esc(slug)}</h2><p class="meta">{esc(v.get("kind",""))} · '
                 f'{esc(summap.get(slug,{}).get("mean_largest_face_pct","unknown"))}% mean face area · '
                 f'{esc(summap.get(slug,{}).get("max_faces","unknown"))} max faces</p>'
                 f'<div class="gal">{thumbs}</div>')
    if not vids and not kfs:
        vbody = ("<h1>视频 / Video</h1><p>This case archive has no downloaded video corpus yet. "
                 "The speech-video index records links only.</p>")
    else:
        vbody = (f'<h1>视频 / Video</h1><p class="meta">{len(vids)} videos · {len(kfs)} keyframes · '
                 f'{len(kid)} identity rows</p>'
                 f'<h2>视频来源 / Video sources</h2><div class="cards">{vcards}</div>'
                 f'<h2>关键帧与人脸识别 / Keyframes and face identity</h2>'
                 f'<p class="meta">SFace cosine similarity against licensed portraits; `unknown` means no '
                 f'match cleared the threshold (0.363) and margin (0.05).</p>{kgal}')
    write(os.path.join(site, "video", "index.html"),
          page("视频 / Video", vbody, 1, "video/index.html"))

    # docs
    docs = []
    for base, _, files in os.walk(case_dir):
        if "site" in base.split(os.sep) or "_staging" in base.split(os.sep):
            continue
        for name in files:
            if name.endswith(".md"):
                p = os.path.join(base, name)
                docs.append((os.path.relpath(p, case_dir).replace(os.sep, "/"), p))
    docs.sort()
    doc_cards = ""
    for rel, p in docs:
        title = os.path.basename(rel)[:-3]
        doc_cards += (f'<a class="card" href="{title}.html"><h3>{esc(title)}</h3>'
                      f'<p>{esc(rel)}</p></a>')
        text = open(p, encoding="utf-8-sig").read()
        write(os.path.join(site, "docs", title + ".html"),
              page(title, f'<div class="crumb"><a href="index.html">文档 / Docs</a> / {esc(rel)}</div>'
                          + md_to_html(text), 1, "docs/index.html"))
    write(os.path.join(site, "docs", "index.html"),
          page("文档 / Docs", f"<h1>文档 / Docs</h1><div class='cards'>{doc_cards}</div>", 1, "docs/index.html"))

    # sources
    rows_html = ""
    for r in sources:
        rows_html += ("<tr><td><span class='src'>" + esc(r.get("source_id", "")) + "</span></td>"
                      f"<td><a class='ext' href='{esc(r.get('url',''))}' target='_blank' rel='noopener'>"
                      f"{esc(r.get('title','')[:90])}</a></td>"
                      f"<td>{esc(r.get('publisher',''))}</td><td>{esc(r.get('publication_date',''))}</td>"
                      f"<td>{esc(r.get('source_tier',''))}</td><td>{esc(r.get('source_type',''))}</td></tr>")
    write(os.path.join(site, "sources", "index.html"),
          page("来源 / Sources",
               f"<h1>来源 / Sources</h1><p class='meta'>{len(sources)} sources</p>"
               f"<div class='table-wrap'><table><thead><tr><th>ID</th><th>Title / URL</th><th>Publisher</th>"
               f"<th>Date</th><th>Tier</th><th>Type</th></tr></thead><tbody>{rows_html}</tbody></table></div>",
               1, "sources/index.html"))

    print(f"{slug}: site built at {site} ({total_rows} rows, {len(sources)} sources, {len(docs)} docs)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
