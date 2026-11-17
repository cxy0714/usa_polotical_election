#!/usr/bin/env python3
"""Merge the Texas and South Carolina case-study sites into one browsable archive.

Approach: each case's `site/` folder is copied intact into `site/cases/<case>/`, which works because
every page in both builds links relatively (assets/, events/, docs/ ...). A shared top bar is then
injected after <body> on every copied page so a reader can move between cases and back to the portal
without touching either case's content. Nothing in the case folders is rewritten except that bar.

The portal home is generated here: one comparison table plus a card per case, both read from the
cases' own CSVs so the numbers cannot drift from the data.

Run: python _tools/build_portal.py
"""
import csv
import html
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
CASES = [
    ("texas", "texas-senate-2026", "Texas Senate 2026", "2026 德克萨斯州联邦参议员选举",
     "Paxton, Cornyn, Talarico and Crockett - a primary fought on the incumbent's record, with a "
     "statewide runoff and a general-election frame built around the Abbott endorsement.",
     "帕克斯顿、科宁、塔拉里科与克罗克特——围绕现任者记录的初选，一场全州决选，以及以大选框架展开的选战。"),
    ("south-carolina", "south-carolina-senate-2026", "South Carolina Senate 2026",
     "2026 南卡罗来纳州联邦参议员选举",
     "Andrews versus Darline Graham: a sitting senator dies mid-cycle, his sister is appointed, and "
     "the state elects its first Democratic senator since 1998.",
     "安德鲁斯对达琳·格雷厄姆：一位在任参议员在选举周期中途去世，其妹受任命，该州选出 1998 年以来首位民主党参议员。"),
]


def esc(v):
    return html.escape(str(v), quote=False)


def read_rows(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def frames_of(case_dir):
    """Texas indexes frames in frame_index.csv, South Carolina in keyframes.csv."""
    for name in ("keyframes.csv", "frame_index.csv"):
        rows = read_rows(os.path.join(case_dir, "10_video_frames", name))
        if rows:
            return rows
    return []


def case_stats(case_dir):
    stats = {}
    total_rows, files = 0, 0
    for folder in os.listdir(case_dir):
        sub = os.path.join(case_dir, folder)
        if not os.path.isdir(sub) or folder in ("site", "_staging", ".git"):
            continue
        for name in os.listdir(sub):
            if name.endswith(".csv"):
                p = os.path.join(sub, name)
                total_rows += max(0, sum(1 for _ in open(p, encoding="utf-8-sig")) - 1)
                files += 1
    stats["rows"] = total_rows
    stats["files"] = files
    stats["sources"] = len(read_rows(os.path.join(case_dir, "09_sources", "sources.csv")))
    stats["events"] = len(read_rows(os.path.join(case_dir, "02_campaign_events", "campaign_events.csv")))
    stats["videos"] = len(read_rows(os.path.join(case_dir, "10_video_frames", "video_sources.csv")))
    stats["frames"] = len(frames_of(case_dir))
    res = read_rows(os.path.join(case_dir, "07_electoral_context", "election_results.csv"))
    stats["races"] = len({r.get("race_id") for r in res if r.get("race_id")})
    stats["results_rows"] = len(res)
    return stats


def inject_bar(path, case_label_en, case_label_zh, case_slug):
    text = open(path, encoding="utf-8").read()
    if "archive-portal-bar" in text:
        return False
    rel_dir = os.path.relpath(os.path.dirname(path), SITE)
    depth = 0 if rel_dir == "." else len(rel_dir.split(os.sep))
    up = "../" * depth
    bar = f"""<div class="archive-portal-bar" id="archive-portal-bar">
  <a class="apb-brand" href="{up}index.html">2026 Senate Archive<span>2026 参议院档案</span></a>
  <span class="apb-links">
    <a href="{up}index.html">Portal / 门户</a>
    <a href="{up}cases/texas/index.html">Texas / 德州</a>
    <a href="{up}cases/south-carolina/index.html">South Carolina / 南卡</a>
  </span>
  <span class="apb-here">{esc(case_label_en)} / {esc(case_label_zh)}</span>
</div>
<style>
.archive-portal-bar{{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:baseline;justify-content:space-between;
padding:8px 16px;background:#101216;color:#e9eaee;font:13px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",sans-serif}}
.archive-portal-bar a{{color:#cfd6e4;text-decoration:none}}
.archive-portal-bar a:hover{{color:#fff;text-decoration:underline}}
.apb-brand{{font-weight:700;color:#fff}}
.apb-brand span{{display:block;font-size:11px;color:#98a1b2;font-weight:400}}
.apb-links{{display:flex;gap:14px;flex-wrap:wrap}}
.apb-here{{color:#98a1b2}}
</style>
"""
    text = re.sub(r"(<body[^>]*>)", r"\1\n" + bar.replace("\\", "\\\\"), text, count=1)
    open(path, "w", encoding="utf-8", newline="\n").write(text)
    return True


def relink_case(slug, case_dir):
    """Point out-of-site links at their real files.

    A Texas page linking `../../11_speech_audio/plots/x.png` meant `texas-senate-2026/11_speech_audio/...`
    when it lived in `texas-senate-2026/site/`. After the copy that path no longer resolves, so each such
    href/src is recomputed from the page's original location and rewritten relative to its new one.
    """
    dst = os.path.join(SITE, "cases", slug)
    original_site = os.path.join(ROOT, case_dir, "site")
    changed = 0
    pattern = re.compile(r'(href|src)="([^"]+)"')
    for base, _, files in os.walk(dst):
        for name in files:
            if not name.endswith(".html"):
                continue
            page = os.path.join(base, name)
            rel_to_case = os.path.relpath(page, dst)
            original_page = os.path.join(original_site, rel_to_case)
            text = open(page, encoding="utf-8").read()

            def fix(m):
                nonlocal changed
                attr, href = m.group(1), m.group(2)
                if href.startswith(("http://", "https://", "#", "mailto:", "data:")):
                    return m.group(0)
                resolved = os.path.normpath(os.path.join(os.path.dirname(original_page), href.split("#")[0]))
                if not os.path.exists(resolved):
                    return m.group(0)
                # A target inside the case's own site folder moved with the copy: keep it local
                # instead of pointing back at the original tree, which would leave the served root.
                if resolved.startswith(original_site + os.sep):
                    moved = os.path.join(dst, os.path.relpath(resolved, original_site))
                    new = os.path.relpath(moved, os.path.dirname(page)).replace(os.sep, "/")
                else:
                    new = os.path.relpath(resolved, os.path.dirname(page)).replace(os.sep, "/")
                if new != href:
                    changed += 1
                    return f'{attr}="{new}"'
                return m.group(0)

            new_text = pattern.sub(fix, text)
            dead = re.compile(r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.S)

            def unwrap(m):
                href, inner = m.group(1), m.group(2)
                if href.startswith(("http://", "https://", "#", "mailto:")):
                    return m.group(0)
                target = os.path.normpath(os.path.join(os.path.dirname(page), href.split("#")[0]))
                return m.group(0) if os.path.exists(target) else inner

            new_text = dead.sub(unwrap, new_text)
            if new_text != text:
                open(page, "w", encoding="utf-8", newline="\n").write(new_text)
    print(f"  {slug}: relinked {changed} out-of-site references")
    return changed


def copy_case(slug, case_dir):
    src = os.path.join(ROOT, case_dir, "site")
    dst = os.path.join(SITE, "cases", slug)
    if not os.path.isdir(src):
        print(f"  no site for {case_dir}")
        return 0
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    n = 0
    for base, _, files in os.walk(dst):
        for name in files:
            if name.endswith(".html"):
                path = os.path.join(base, name)
                label = next((c for c in CASES if c[0] == slug), CASES[0])
                n += 1 if inject_bar(path, label[2], label[3], slug) else 0
    print(f"  {slug}: copied to site/cases/{slug}, bar injected on {n} pages")
    return n


OVERRIDES_CSS = """/* shared width override so both cases read at the same measure */
.layout{max-width:1500px}
body.wide .layout{max-width:1500px}
@media (min-width:1560px){.layout,body.wide .layout{max-width:1640px}}
"""


def inject_overrides(slug):
    """Texas pages carry their stylesheet inline; one link before </head> widens them to match SC."""
    dst = os.path.join(SITE, "cases", slug)
    changed = 0
    for base, _, files in os.walk(dst):
        for name in files:
            if not name.endswith(".html"):
                continue
            page = os.path.join(base, name)
            text = open(page, encoding="utf-8").read()
            if "overrides.css" in text:
                continue
            rel_dir = os.path.relpath(os.path.dirname(page), SITE)
            up = "" if rel_dir == "." else "../" * len(rel_dir.split(os.sep))
            link = f'<link rel="stylesheet" href="{up}assets/overrides.css">'
            text = text.replace("</head>", link + "\n</head>", 1) if "</head>" in text else link + "\n" + text
            open(page, "w", encoding="utf-8", newline="\n").write(text)
            changed += 1
    return changed


def portal_css():
    return """:root{--ink:#14161a;--muted:#5d6572;--line:#e2e5ea;--bg:#fbfbfc;--accent:#8a1c1c;--accent2:#0f4c81}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",sans-serif}
main{max-width:1080px;margin:0 auto;padding:34px 22px 70px}
.hero h1{font-size:34px;line-height:1.15;margin:0 0 10px;font-weight:700}
.hero h1 .zh{display:block;font-size:.55em;color:var(--muted);font-weight:400;margin-top:6px}
.hero .lede{font-size:17px;color:#2c3138;max-width:74ch;margin:0 0 6px}
.hero .meta{font-size:13px;color:var(--muted)}
.cases{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:18px;margin:26px 0}
.case{background:#fff;border:1px solid var(--line);border-radius:12px;padding:20px 22px}
.case h2{font-size:22px;margin:0 0 2px}
.case h2 .zh{display:block;font-size:13px;color:var(--muted);font-weight:400;margin-top:3px}
.case p{font-size:14.5px;color:#39404b}
.case .go{display:inline-block;margin-top:8px;background:var(--accent2);color:#fff;text-decoration:none;padding:8px 14px;border-radius:7px;font-size:14px}
.case .go:hover{background:#0c3d68}
table.cmp{width:100%;border-collapse:collapse;font-size:14px;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden}
table.cmp th,table.cmp td{padding:9px 12px;border-bottom:1px solid var(--line);text-align:left}
table.cmp thead th{background:#f3f4f7;font-size:12.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
table.cmp td.num{font-variant-numeric:tabular-nums;text-align:right}
h2.section{font-size:16px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:34px 0 10px}
.foot{border-top:1px solid var(--line);margin-top:40px;padding-top:16px;font-size:12.5px;color:var(--muted)}
.method{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 18px;font-size:14px}
.method p{margin:8px 0}
@media (max-width:560px){.hero h1{font-size:26px}}
"""


def build_portal(stats):
    tx, sc = stats["texas"], stats["south-carolina"]
    cards = []
    for slug, case_dir, en, zh, blurb_en, blurb_zh in CASES:
        s = stats[slug]
        cards.append(f"""<section class="case">
  <h2>{esc(en)}<span class="zh">{esc(zh)}</span></h2>
  <p>{esc(blurb_en)}</p>
  <p>{esc(blurb_zh)}</p>
  <p class="meta">{s['rows']:,} CSV rows · {s['sources']} sources · {s['events']} events · {s['videos']} videos</p>
  <a class="go" href="cases/{slug}/index.html">Open case / 打开案例</a>
</section>""")

    rows = [
        ("CSV rows / CSV 行数", tx["rows"], sc["rows"]),
        ("Datasets / 数据集", tx["files"], sc["files"]),
        ("Sources / 来源", tx["sources"], sc["sources"]),
        ("Documented events / 活动", tx["events"], sc["events"]),
        ("Race rows / 选举结果行", tx["results_rows"], sc["results_rows"]),
        ("Videos / 视频", tx["videos"], sc["videos"]),
        ("Frame records / 帧记录", tx["frames"], sc["frames"]),
    ]
    body_rows = "".join(
        f"<tr><th>{esc(label)}</th><td class='num'>{a:,}</td><td class='num'>{b:,}</td></tr>"
        for label, a, b in rows)

    body = f"""
<section class="hero">
  <h1>2026 United States Senate: two case studies<span class="zh">2026 美国联邦参议员选举：两个案例</span></h1>
  <p class="lede">Two states, one method: every table row traces to a retrieved URL, every inference is
  labelled, and anything the sources do not state is recorded as <code>unknown</code> rather than guessed.</p>
  <p class="lede">两个州，一套方法：每一行都可追溯到已检索的 URL，每一处推断都标注，来源未给出的值记为
  <code>unknown</code> 而非猜测。</p>
  <p class="meta">{tx['rows'] + sc['rows']:,} CSV rows across both cases · {tx['sources'] + sc['sources']} sources</p>
</section>

<section class="cases">
{''.join(cards)}
</section>

<h2 class="section">Side by side / 并排对比</h2>
<table class="cmp">
  <thead><tr><th>Measure / 指标</th><th>Texas / 德州</th><th>South Carolina / 南卡</th></tr></thead>
  <tbody>{body_rows}</tbody>
</table>

<h2 class="section">Shared method / 共同方法</h2>
<div class="method">
<p><strong>Citation contract.</strong> Every CSV row carries <code>SRC-####|https://...</code>; the id resolves in that
case's <code>09_sources/sources.csv</code>. Source tiers T1/T2/T3 are assigned mechanically from the domain, not from an
editorial judgement about accuracy.</p>
<p><strong>Citation contract（中文）.</strong> 每个 CSV 行都带 <code>SRC-####|https://...</code>，其 id 可在该案例的
<code>09_sources/sources.csv</code> 中解析。T1/T2/T3 等级按域名机械判定，而非对准确性的编辑判断。</p>
<p><strong>Where the two cases differ.</strong> Texas documents a contested primary inside a party that holds the seat;
South Carolina documents a vacancy - a death, an appointment, a statutory three-week special primary and a runoff - which
is why its events table carries an <code>actor_note</code> and <code>vacancy_context</code> column that Texas does not
need.</p>
<p><strong>两个案例的差别（中文）.</strong> 德州记录的是在野党内部一场有竞争的初选；南卡记录的是一次空缺——死亡、任命、
法定三周特别初选与决选——因此其活动表带有德州不需要的 <code>actor_note</code> 与 <code>vacancy_context</code> 列。</p>
</div>

<p class="foot">Compiled 2026-11. Both case folders keep their own conventions documents and their own source tables;
nothing is merged at the data level, only at the browsing level.</p>
"""
    home = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>2026 Senate Archive - two case studies</title>
<style>{portal_css()}</style>
</head>
<body>
<main>
{body}
</main>
</body>
</html>
"""
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8", newline="\n").write(home)
    print("portal index.html written")


def audit():
    broken = []
    for base, _, files in os.walk(SITE):
        for name in files:
            if not name.endswith(".html"):
                continue
            p = os.path.join(base, name)
            for href in re.findall(r'href="([^"]+)"', open(p, encoding="utf-8").read()):
                if href.startswith(("http", "#", "mailto")):
                    continue
                from urllib.parse import unquote
                target = os.path.normpath(os.path.join(base, unquote(href)))
                if not os.path.exists(target):
                    broken.append((os.path.relpath(p, SITE), href))
    print(f"internal links broken: {len(broken)}")
    for b in broken[:12]:
        print("   ", b)
    return broken


def main():
    os.makedirs(os.path.join(SITE, "cases"), exist_ok=True)
    os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
    open(os.path.join(SITE, "assets", "overrides.css"), "w", encoding="utf-8", newline="\n").write(OVERRIDES_CSS)
    stats = {}
    for slug, case_dir, *_ in CASES:
        stats[slug] = case_stats(os.path.join(ROOT, case_dir))
        print(f"  {slug}: {stats[slug]}")
    for slug, case_dir, *_ in CASES:
        copy_case(slug, case_dir)
        print(f"  {slug}: width override linked on {inject_overrides(slug)} pages")
        relink_case(slug, case_dir)
    build_portal(stats)
    broken = audit()
    return 0 if not broken else 1


if __name__ == "__main__":
    sys.exit(main())
