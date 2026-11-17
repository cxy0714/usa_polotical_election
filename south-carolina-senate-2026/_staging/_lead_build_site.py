#!/usr/bin/env python3
"""Build the static site for the South Carolina case study.

Deliberately small and dependency-light: `markdown` for the prose pages, hand-written HTML for the
data tables, one CSS file and one JS file for filtering and column sorting. No templating engine,
no build step, no server — the output is a folder of relative links that opens from disk.

Output: site/index.html, site/data/*.html, site/docs/*.html, site/about.html, site/assets/*

Run: python _staging/_lead_build_site.py
"""
import csv
import html
import json
import os
import re
import sys
from urllib.parse import quote

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "site")

CASE_TITLE_EN = "South Carolina Senate 2026"
CASE_TITLE_ZH = "2026 南卡罗来纳州联邦参议员选举"
SUBTITLE_EN = "A primary-source archive of the Andrews-Graham race"
SUBTITLE_ZH = "安德鲁斯对格雷厄姆之战的原始史料档案"

GROUPS = [
    ("candidates", "Candidates / 候选人"),
    ("events", "Campaign events / 竞选活动"),
    ("speeches", "Speeches / 演讲"),
    ("visual", "Visual archive / 视觉档案"),
    ("media", "Campaign media / 媒体与广告"),
    ("finance", "Campaign finance / 竞选财务"),
    ("electoral", "Electoral context / 选举语境"),
    ("video", "Video and audio / 影音层"),
    ("sources", "Sources / 来源"),
]

DATASETS = [
    ("01_candidates/policy_positions.csv", "candidates", "Policy positions", "政策立场",
     "51 rows, 34 for Andrews and 17 for Graham. Andrews has no legislative record, so that column is unknown throughout her rows."),
    ("01_candidates/andrews/career_timeline.csv", "candidates", "Andrews career timeline", "安德鲁斯生涯年表",
     "20 dated milestones."),
    ("01_candidates/graham/career_timeline.csv", "candidates", "Graham career timeline", "格雷厄姆生涯年表",
     "24 dated milestones."),
    ("02_campaign_events/campaign_events.csv", "events", "Campaign events", "竞选活动",
     "32 documented events in 17 categories. Venues, times and crowd sizes are unknown almost everywhere."),
    ("03_speeches/speech_archive.csv", "speeches", "Speech archive", "演讲档案",
     "24 speeches and speech-like appearances."),
    ("03_speeches/speech_video_index.csv", "speeches", "Speech video index", "演讲视频索引",
     "22 rows mapping speeches to video."),
    ("04_visual_archive/image_archive.csv", "visual", "Image archive", "图片档案",
     "52 photographs and campaign visuals with licence and resolution."),
    ("05_campaign_media/media_coverage.csv", "media", "Media coverage register", "媒体报道登记",
     "55 coverage rows with outlet, author, title and framing."),
    ("05_campaign_media/advertisements.csv", "media", "Advertisements and outside money", "广告与外部资金",
     "3 rows. Two are independent-expenditure transfers, not ad creative."),
    ("05_campaign_media/social_media.csv", "media", "Social media", "社交媒体",
     "3 documented posts; two are second-hand and one has no retrievable body."),
    ("06_campaign_finance/campaign_finance.csv", "finance", "Campaign finance", "竞选财务",
     "5 FEC snapshots for the two principals. Never summed with outside spending."),
    ("06_campaign_finance/other_candidates_finance.csv", "finance", "Other candidates' finance", "其他候选人财务",
     "15 rows for the other filed candidates."),
    ("07_electoral_context/election_results.csv", "electoral", "Election results", "选举结果",
     "26 rows covering the primaries, the runoff and the general."),
    ("07_electoral_context/county_results.csv", "electoral", "County results", "县级结果",
     "46 counties; they sum exactly to the statewide total."),
    ("07_electoral_context/polling.csv", "electoral", "General-election polling", "大选民调",
     "20 rows including forecasters."),
    ("07_electoral_context/primary_polling.csv", "electoral", "Primary polling", "初选民调",
     "6 rows."),
    ("09_sources/exit_poll_2026.csv", "electoral", "Exit poll", "出口民调",
     "45 subgroups across 15 groups."),
    ("09_sources/sources.csv", "sources", "Sources", "来源",
     "370 sources with tier, type and a computed used_by citation map."),
    ("10_video_frames/keyframes.csv", "video", "Keyframes", "关键帧",
     "300 scene-change frames with face counts and boxes."),
    ("10_video_frames/video_face_summary.csv", "video", "Per-video face summary", "逐视频人脸汇总",
     "27 videos: frames extracted, frames with faces, largest face share."),
    ("10_video_frames/video_sources.csv", "video", "Video corpus", "视频语料",
     "27 downloaded videos with local filenames and byte sizes."),
    ("11_speech_audio/audio_metrics.csv", "video", "Audio metrics", "音频指标",
     "27 videos: mean level, silence ratio, caption word count and rate."),
]

DOCS = [
    ("README.md", "Overview", "总览", "start"),
    ("08_comparative_analysis/candidate_comparison.md", "Candidate comparison", "候选人对比", "analysis"),
    ("02_campaign_events/event_coverage_gaps.md", "Event coverage gaps", "活动覆盖缺口", "analysis"),
    ("07_electoral_context/election_context.md", "Electoral context", "选举语境", "analysis"),
    ("07_electoral_context/results_notes.md", "Results and reconciliation", "结果与对账", "analysis"),
    ("03_speeches/communication_analysis_andrews.md", "Communication analysis: Andrews", "传播分析：安德鲁斯", "analysis"),
    ("03_speeches/communication_analysis_graham.md", "Communication analysis: Graham", "传播分析：格雷厄姆", "analysis"),
    ("01_candidates/andrews/biography.md", "Biography: Andrews", "传记：安德鲁斯", "candidate"),
    ("01_candidates/andrews/political_positions.md", "Positions: Andrews", "立场：安德鲁斯", "candidate"),
    ("01_candidates/graham/biography.md", "Biography: Graham", "传记：格雷厄姆", "candidate"),
    ("01_candidates/graham/political_positions.md", "Positions: Graham", "立场：格雷厄姆", "candidate"),
    ("02_campaign_events/andrews_timeline.md", "Timeline: Andrews", "时间线：安德鲁斯", "candidate"),
    ("02_campaign_events/graham_timeline.md", "Timeline: Graham", "时间线：格雷厄姆", "candidate"),
    ("09_sources/data_dictionary_bilingual.md", "Data dictionary", "数据字典", "method"),
    ("research_gaps.md", "Research gaps", "研究缺口", "method"),
    ("_research_conventions.md", "Research conventions", "研究规范", "method"),
]

KEY_FACTS = [
    ("Result", "结果", "Andrews 1,044,001 (51.14%) to Graham 952,191 (46.64%); total 2,041,487."),
    ("First", "首次", "The first Democrat elected to the U.S. Senate from South Carolina since 1998."),
    ("Sequence", "序列",
     "Lindsey Graham died 2026-07-11; his sister Darline was appointed 2026-07-13 and sworn in 07-14; "
     "she won a ten-candidate special primary and a runoff before losing the general."),
    ("Money", "资金",
     "As of 2026-10-14 Andrews had raised $24,216,841 to Graham's $1,917,646, a 12.6:1 ratio. "
     "Outside money favoured Graham: Senate Leadership Fund $5M, MAGA Inc. $827,000."),
    ("Debates", "辩论", "Graham took part in four televised debates; Andrews in one."),
    ("Coalition", "联盟",
     "Andrews won independents 63-32, 18-44 year-olds 66-29 and Black voters 85-12 (18% of the "
     "electorate), while losing 65+ voters 45-54 and rural voters 48-51."),
]


def rel(target, depth):
    return "../" * depth + target


def doc_slug(relpath, seen):
    """Unique slug per doc: biography.md exists for both candidates, so the parent folder qualifies it."""
    if relpath == "README.md":
        return "overview"
    stem = os.path.basename(relpath)[:-3]
    parent = os.path.basename(os.path.dirname(relpath))
    slug = stem
    if slug in seen:
        slug = f"{parent}_{stem}"
    seen.add(slug)
    return slug


def data_slug(relpath, seen):
    """Unique page name per dataset: career_timeline.csv exists for both candidates."""
    stem = os.path.basename(relpath)[:-4]
    slug = stem
    if slug in seen:
        slug = f"{os.path.basename(os.path.dirname(relpath))}_{stem}"
    seen.add(slug)
    return slug


def link_targets():
    """Map repo-relative paths to site pages, so in-document links do not point outside the site."""
    docs = {}
    seen = set()
    for p, en, zh, kind in DOCS:
        docs[p] = f"docs/{doc_slug(p, seen)}.html"
    data = {}
    seen_data = set()
    for p, group, en, zh, desc in DATASETS:
        data[p] = f"data/{quote(data_slug(p, seen_data))}.html"
    return docs, data


def rewrite_links(body, depth):
    """Rewrite ../x.md and ../x.csv links to their site pages; unwrap links that leave the site."""
    docs, data = link_targets()
    prefix = "../" * depth

    anchor_re = re.compile(r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.S)

    def repl(m):
        href, inner = m.group(1), m.group(2)
        if href.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        norm = os.path.normpath(href)
        if norm in docs:
            return f'<a href="{prefix}{docs[norm]}">{inner}</a>'
        if norm in data:
            return f'<a href="{prefix}{data[norm]}">{inner}</a>'
        return inner

    return anchor_re.sub(repl, body)


def md_to_html(path):
    text = open(path, encoding="utf-8").read()
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        text = text[m.end():]
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    return meta, body


def esc(v):
    return html.escape(v if v is not None else "", quote=False)


def page(title, body, depth, active=""):
    css = rel("assets/style.css", depth)
    js = rel("assets/app.js", depth)
    home = rel("index.html", depth)
    nav = [
        ("index.html", "Overview / 总览"),
        ("data/campaign_events.html", "Events / 活动"),
        ("data/county_results.html", "Counties / 县"),
        ("data/sources.html", "Sources / 来源"),
        ("about.html", "Method / 方法"),
    ]
    links = "".join(
        f'<a class="navlink{" on" if href in active else ""}" href="{rel(href, depth)}">{esc(t)}</a>'
        for href, t in nav)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} - {CASE_TITLE_EN}</title>
<link rel="stylesheet" href="{css}">
</head>
<body>
<header class="topbar">
  <a class="brand" href="{home}"><span class="en">{CASE_TITLE_EN}</span><span class="zh">{CASE_TITLE_ZH}</span></a>
  <nav class="nav">{links}</nav>
</header>
<main>
{body}
</main>
<footer class="foot">
  <p>Compiled 2026-11-12 from primary and secondary sources. Every CSV row carries <code>SRC-####|https://...</code>.
  <code>unknown</code> is a value, not a gap.</p>
  <p>2026-11-12 编制。每个 CSV 行均带 <code>SRC-####|https://...</code>；<code>unknown</code> 是取值，不是缺失。</p>
</footer>
<script src="{js}"></script>
</body>
</html>
"""


def csv_table(path):
    rows = list(csv.reader(open(path, encoding="utf-8-sig")))
    if not rows:
        return "<p>Empty.</p>"
    header, body = rows[0], [r for r in rows[1:] if r]
    out = ['<div class="tablewrap"><table class="data"><thead><tr>']
    for i, h in enumerate(header):
        out.append(f'<th data-col="{i}">{esc(h)}<span class="sortmark"></span></th>')
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>")
        for i, h in enumerate(header):
            v = r[i] if i < len(r) else ""
            cls = "unk" if v.strip() == "unknown" else ""
            cell = esc(v)
            if v.startswith("http") or "SRC-" in v:
                cell = esc(v)
            out.append(f'<td class="{cls}">{cell}</td>')
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def build_index():
    seen_slugs = set()
    seen_data = set()
    stats = []
    total_rows = 0
    for relpath, group, en, zh, desc in DATASETS:
        p = os.path.join(ROOT, relpath)
        if not os.path.exists(p):
            continue
        n = sum(1 for _ in open(p, encoding="utf-8-sig")) - 1
        total_rows += n
        stats.append((relpath, group, en, zh, desc, n))

    facts = "".join(
        f'<div class="fact"><h3>{esc(en)} <span class="zh">/ {esc(zh)}</span></h3><p>{esc(txt)}</p></div>'
        for en, zh, txt in KEY_FACTS)

    cards = []
    for gid, gtitle in GROUPS:
        items = [s for s in stats if s[1] == gid]
        if not items:
            continue
        links = "".join(
            f'<li><a href="data/{quote(os.path.basename(s[0])[:-4])}.html">{esc(s[2])}'
            f'<span class="zh"> / {esc(s[3])}</span></a> <span class="rows">{s[5]} rows</span>'
            f'<span class="desc">{esc(s[4])}</span></li>'
            for s in items)
        cards.append(f'<section class="card"><h2>{esc(gtitle)}</h2><ul class="ds">{links}</ul></section>')

    doclinks = "".join(
        f'<li><a href="docs/{doc_slug(p, seen_slugs)}.html">'
        f'{esc(en)}<span class="zh"> / {esc(zh)}</span></a></li>'
        for p, en, zh, kind in DOCS)

    body = f"""
<section class="hero">
  <p class="eyebrow">Case Study 002 / 案例研究 002</p>
  <h1>{CASE_TITLE_EN}<span class="zh">{CASE_TITLE_ZH}</span></h1>
  <p class="lede">{SUBTITLE_EN}. {SUBTITLE_ZH}。</p>
  <p class="meta">{total_rows:,} CSV rows · {len(stats)} datasets · 370 sources · 27 videos · 300 keyframes</p>
</section>

<section class="facts">
{facts}
</section>

<section class="cards">
{''.join(cards)}
</section>

<section class="card wide">
  <h2>Written analyses / 分析文档</h2>
  <ul class="docs">{doclinks}</ul>
</section>

<section class="card wide note">
  <h2>How to read the numbers / 如何读这些数字</h2>
  <p>Every table cell of <code>unknown</code> means the retrieved sources do not state that value — it never means zero
  and never means "not applicable". Candidate-committee money and outside independent expenditures are in separate tables
  and are never added together. County rows sum exactly to the statewide total of 2,041,487.</p>
  <p>任何 <code>unknown</code> 单元格都表示已检索来源未给出该值——它从不表示零，也从不表示「不适用」。候选人委员会资金与外部独立支出分表存放，绝不相加。县级行精确加总为全州总数 2,041,487。</p>
</section>
"""
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(
        page("Overview", body, 0, "index.html"))
    print(f"index.html: {len(stats)} datasets, {total_rows} rows")


def build_data_pages():
    os.makedirs(os.path.join(SITE, "data"), exist_ok=True)
    made = 0
    seen_data = set()
    for relpath, group, en, zh, desc in DATASETS:
        src = os.path.join(ROOT, relpath)
        if not os.path.exists(src):
            continue
        n = sum(1 for _ in open(src, encoding="utf-8-sig")) - 1
        body = f"""
<section class="hero small">
  <p class="eyebrow">{esc(group)} · {n} rows</p>
  <h1>{esc(en)}<span class="zh">{esc(zh)}</span></h1>
  <p class="lede">{esc(desc)}</p>
  <p class="meta">File: <code>{esc(relpath)}</code></p>
</section>
<section class="toolbar">
  <input type="search" id="filter" placeholder="Filter rows / 过滤行 - type a county, date, candidate or SRC id">
  <span id="count" class="count"></span>
</section>
{csv_table(src)}
"""
        name = quote(data_slug(relpath, seen_data))
        open(os.path.join(SITE, "data", f"{name}.html"), "w", encoding="utf-8").write(
            page(f"{en} / {zh}", body, 1, f"data/{name}.html"))
        made += 1
    print(f"data pages: {made}")


def build_docs():
    os.makedirs(os.path.join(SITE, "docs"), exist_ok=True)
    seen = set()
    made = 0
    for relpath, en, zh, kind in DOCS:
        src = os.path.join(ROOT, relpath)
        if not os.path.exists(src):
            print(f"  missing doc {relpath}")
            continue
        meta, body = md_to_html(src)
        title_en = meta.get("title", en)
        slug = doc_slug(relpath, seen)
        body = rewrite_links(body, 1)
        wrapped = (f'<article class="prose"><div class="docmeta">{esc(relpath)} · '
                   f'{esc(meta.get("last_updated", "unknown"))}</div>{body}</article>')
        open(os.path.join(SITE, "docs", f"{slug}.html"), "w", encoding="utf-8").write(
            page(f"{en} / {zh}", wrapped, 1, ""))
        made += 1
    print(f"doc pages: {made}")


def build_about():
    body = """
<section class="hero small">
  <p class="eyebrow">Method / 方法</p>
  <h1>How this archive was built<span class="zh">这套档案是怎么做出来的</span></h1>
</section>
<article class="prose">
<h2>Collection / 采集</h2>
<p>The race article on Wikipedia supplied the skeleton: 63 sections and 534 cited URLs were mirrored to disk, parsed
into county, polling and finance tables, then cross-checked against CBS's results reporting and the FEC tables quoted in
the sources. Video came from yt-dlp searches and a hand-curated list of 27 uploads, downloaded at 720p (480p for the two
hour-long debates).</p>
<p>维基百科的选举条目提供了骨架：63 个章节与 534 条引用 URL 被镜像到本地，解析出县级、民调与财务表，再与 CBS 的结果报道以及来源中引用的 FEC 表格交叉核对。视频来自 yt-dlp 搜索与手工筛选的 27 条上传，720p 下载（两场一小时的辩论为 480p）。</p>

<h2>Verification / 校验</h2>
<p><code>_staging/_lead_validate.py</code> enforces header conformance, field counts, no blank cells, controlled
vocabularies, ISO dates, and the presence of an <code>SRC-####</code> token plus a URL in every row. The archive currently
passes with zero hard failures.</p>
<p><code>_staging/_lead_validate.py</code> 强制表头一致、字段数、无空单元格、受控词表、ISO 日期，以及每行都带
<code>SRC-####</code> 与 URL。档案目前以零硬失败通过。</p>

<h2>Tier rules / 等级规则</h2>
<p><code>T1</code> official records (.gov domains, SCETV debate video); <code>T2</code> established news organisations;
<code>T3</code> everything else, including Wikipedia, advocacy sites and social posts. Tier is assigned from the domain by
the merge script, mechanically — it describes the venue, not the accuracy of a claim.</p>
<p><code>T1</code> 官方记录（.gov 域、SCETV 辩论视频）；<code>T2</code> 既有新闻机构；<code>T3</code> 其余，包括维基百科、倡议组织网站与社交帖子。等级由合并脚本按域名机械判定——它描述发表场所，而非某条主张的准确性。</p>

<h2>What is thin / 单薄之处</h2>
<p>Campaign calendars were unreachable (both campaign sites return HTTP 403), so events, ads and message columns rest on
third-party reporting. Advertising creative, social engagement metrics and FEC line items are absent. These are recorded
as gaps rather than filled with plausible content.</p>
<p>竞选日程无法获取（两个竞选网站均返回 HTTP 403），因此活动、广告与讯息列依赖第三方报道。广告创意、社交互动指标与 FEC 逐笔明细均缺失。这些被记录为缺口，而非用看似合理的内容填充。</p>

<h2>Deliverable map / 交付结构</h2>
<ul>
<li><a href="data/sources.html">Sources</a> — 370 rows with a computed citation graph.</li>
<li><a href="docs/data_dictionary_bilingual.html">Data dictionary</a> — every column and vocabulary.</li>
<li><a href="docs/research_gaps.html">Research gaps</a> — what could not be retrieved, and why.</li>
<li><a href="docs/event_coverage_gaps.html">Event coverage gaps</a> — why the events table has 32 rows.</li>
</ul>
</article>
"""
    open(os.path.join(SITE, "about.html"), "w", encoding="utf-8").write(
        page("Method / 方法", body, 0, "about.html"))
    print("about.html")


def build_assets():
    os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
    css = """:root{--ink:#14161a;--muted:#5d6572;--line:#e2e5ea;--bg:#fbfbfc;--accent:#8a1c1c;--accent2:#0f4c81}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",sans-serif}
.topbar{display:flex;flex-wrap:wrap;gap:12px;align-items:baseline;justify-content:space-between;padding:14px 22px;border-bottom:1px solid var(--line);background:#fff;position:sticky;top:0;z-index:5}
.brand{text-decoration:none;color:var(--ink);font-weight:650}
.brand .zh{display:block;font-size:12px;color:var(--muted);font-weight:400}
.nav{display:flex;gap:14px;flex-wrap:wrap}
.navlink{color:var(--muted);text-decoration:none;font-size:14px;padding:4px 2px;border-bottom:2px solid transparent}
.navlink:hover,.navlink.on{color:var(--accent2);border-bottom-color:var(--accent2)}
main{max-width:1180px;margin:0 auto;padding:26px 22px 60px}
.hero{padding:26px 0 18px;border-bottom:1px solid var(--line)}
.hero.small{padding:12px 0 14px}
.eyebrow{text-transform:uppercase;letter-spacing:.09em;font-size:11px;color:var(--accent);margin:0 0 8px}
h1{font-size:32px;line-height:1.18;margin:0 0 10px;font-weight:680}
.hero.small h1{font-size:25px}
h1 .zh,h2 .zh,h3 .zh{display:block;font-size:.58em;color:var(--muted);font-weight:400;margin-top:4px}
.lede{font-size:17px;color:#2c3138;margin:0 0 8px;max-width:70ch}
.meta{font-size:13px;color:var(--muted);margin:0}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px;margin:22px 0}
.fact{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.fact h3{margin:0 0 6px;font-size:14px;letter-spacing:.02em}
.fact p{margin:0;font-size:14px;color:#333}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:16px}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.card.wide{grid-column:1/-1;margin-top:16px}
.card h2{font-size:15px;text-transform:uppercase;letter-spacing:.06em;margin:0 0 10px;color:var(--muted)}
ul.ds,ul.docs{list-style:none;padding:0;margin:0}
ul.ds li{padding:9px 0;border-bottom:1px dashed var(--line)}
ul.ds li:last-child{border-bottom:0}
ul.ds a{color:var(--accent2);text-decoration:none;font-weight:600}
ul.ds .rows{font-size:12px;color:var(--muted);margin-left:8px;white-space:nowrap}
ul.ds .desc{display:block;font-size:13px;color:#4a5160;margin-top:2px}
ul.docs{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:6px 18px}
ul.docs a{color:var(--accent2);text-decoration:none}
.toolbar{display:flex;gap:12px;align-items:center;margin:16px 0 10px;flex-wrap:wrap}
#filter{flex:1 1 340px;padding:9px 12px;border:1px solid var(--line);border-radius:8px;font-size:14px;background:#fff}
.count{font-size:13px;color:var(--muted)}
.tablewrap{overflow:auto;max-height:74vh;border:1px solid var(--line);border-radius:10px;background:#fff}
table.data{border-collapse:collapse;font-size:13px;width:100%}
table.data th{position:sticky;top:0;background:#f3f4f7;text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);white-space:nowrap;cursor:pointer;font-weight:600}
table.data td{padding:7px 10px;border-bottom:1px solid #eef0f3;vertical-align:top;max-width:420px;overflow-wrap:anywhere}
table.data tr:hover td{background:#fcfcfe}
td.unk{color:#9aa2ae;font-style:italic}
.prose{max-width:860px;margin:0 auto}
.prose h2{font-size:21px;margin:30px 0 8px;padding-top:8px;border-top:1px solid var(--line)}
.prose h3{font-size:17px;margin:20px 0 6px}
.prose p{margin:10px 0}
.prose table{border-collapse:collapse;width:100%;font-size:13px;margin:14px 0}
.prose th,.prose td{border:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}
.prose th{background:#f3f4f7}
.prose code{background:#f1f2f5;padding:1px 5px;border-radius:4px;font-size:.9em}
.prose pre{background:#14161a;color:#e8eaf0;padding:12px;border-radius:8px;overflow:auto;font-size:12.5px}
.prose blockquote{border-left:3px solid var(--accent2);margin:12px 0;padding:2px 14px;color:#3a414c}
.prose a{color:var(--accent2)}
.docmeta{font-size:12px;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:8px;margin-bottom:14px}
.foot{border-top:1px solid var(--line);padding:20px 22px;color:var(--muted);font-size:12.5px;max-width:1180px;margin:0 auto}
.note p{font-size:14px}
@media (max-width:640px){h1{font-size:26px}.hero p.lede{font-size:15px}}
"""
    open(os.path.join(SITE, "assets", "style.css"), "w", encoding="utf-8").write(css)

    js = """(function(){
  var table=document.querySelector('table.data');
  var input=document.getElementById('filter');
  var count=document.getElementById('count');
  if(!table) return;
  var rows=[].slice.call(table.querySelectorAll('tbody tr'));
  function apply(){
    var q=(input&&input.value||'').trim().toLowerCase();
    var shown=0;
    rows.forEach(function(tr){
      var hit=!q||tr.textContent.toLowerCase().indexOf(q)>-1;
      tr.style.display=hit?'':'none';
      if(hit) shown++;
    });
    if(count) count.textContent=shown+' / '+rows.length+' rows';
  }
  if(input){input.addEventListener('input',apply);}
  apply();
  var dir={};
  table.querySelectorAll('th').forEach(function(th){
    th.addEventListener('click',function(){
      var i=+th.getAttribute('data-col');
      dir[i]=!dir[i];
      var sorted=rows.slice().sort(function(a,b){
        var av=(a.children[i]||{}).textContent||'', bv=(b.children[i]||{}).textContent||'';
        var an=parseFloat(av.replace(/[^0-9.\\-]/g,'')), bn=parseFloat(bv.replace(/[^0-9.\\-]/g,''));
        var cmp=(!isNaN(an)&&!isNaN(bn))?an-bn:av.localeCompare(bv);
        return dir[i]?cmp:-cmp;
      });
      var tb=table.querySelector('tbody');
      sorted.forEach(function(tr){tb.appendChild(tr);});
      rows=sorted;
      apply();
    });
  });
})();
"""
    open(os.path.join(SITE, "assets", "app.js"), "w", encoding="utf-8").write(js)

    index = {
        "case": CASE_TITLE_EN,
        "docs": [{"title": en, "title_zh": zh, "path": f"docs/{'overview' if p == 'README.md' else os.path.basename(p)[:-3]}.html"}
                 for p, en, zh, _ in DOCS],
        "datasets": [{"title": en, "title_zh": zh, "path": f"data/{os.path.basename(p)[:-4]}.html"}
                     for p, _, en, zh, _ in DATASETS],
    }
    open(os.path.join(SITE, "assets", "search-index.js"), "w", encoding="utf-8").write(
        "window.SEARCH_INDEX=" + json.dumps(index, ensure_ascii=False, indent=1) + ";\n")
    open(os.path.join(SITE, ".nojekyll"), "w", encoding="utf-8").write("")
    print("assets: style.css, app.js, search-index.js, .nojekyll")


def main():
    os.makedirs(SITE, exist_ok=True)
    build_assets()
    build_index()
    build_data_pages()
    build_docs()
    build_about()
    n = sum(len(f) for _, _, f in os.walk(SITE))
    print(f"site built: {n} files -> {SITE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
