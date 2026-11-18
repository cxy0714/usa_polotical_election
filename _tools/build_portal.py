#!/usr/bin/env python3
"""Merge every case-study site into one browsable archive.

Each case's `site/` folder is copied intact into `site/cases/<case>/`; a shared top bar is injected
after <body> so a reader can move between cases and back to the portal. The portal home is generated
from each case's own CSVs so the headline numbers cannot drift from the data.

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

# slug, folder, English label, Chinese label, short bar label, blurb EN, blurb ZH
CASES = [
    ("texas", "texas-senate-2026", "Texas Senate 2026", "2026 德克萨斯州联邦参议员选举", "Texas",
     "Paxton, Cornyn, Talarico and Crockett - a primary fought on the incumbent's record, with a "
     "statewide runoff and a general-election frame built around the Abbott endorsement.",
     "帕克斯顿、科宁、塔拉里科与克罗克特——围绕现任者记录的初选，一场全州决选，以及以大选框架展开的选战。"),
    ("michigan", "michigan-senate-2026", "Michigan Senate 2026", "2026 年密歇根州联邦参议员选举", "Michigan",
     "El-Sayed versus Rogers: an open Democratic seat in a Trump-carried state, a three-way primary "
     "that collapsed into a two-way finish, and the most expensive Senate race in Michigan history.",
     "埃尔-赛义德对罗杰斯：特朗普赢下的州里一个开放的民主党席位，三人民主党初选收缩为两强对决，以及密歇根史上最贵的参议院选战。"),
    ("alaska", "alaska-senate-2026", "Alaska Senate 2026", "2026 年阿拉斯加州联邦参议员选举", "Alaska",
     "Peltola versus Sullivan: ranked-choice Alaska, a same-name ballot challenger, and the first "
     "Alaska Native elected to the Senate.",
     "佩尔托拉对沙利文：排序复选制的阿拉斯加、一位同名 ballot 挑战者，以及首位当选联邦参议员的阿拉斯加原住民。"),
    ("iowa", "iowa-senate-2026", "Iowa Senate 2026", "2026 年艾奥瓦州联邦参议员选举", "Iowa",
     "Turek versus Hinson: a Paralympic athlete and state representative against a Trump-endorsed "
     "congresswoman, in a state that had not elected a Democratic senator since 2008.",
     "图雷克对欣森：一位残奥运动员兼州议员对阵获特朗普背书的国会女议员，而该州自 2008 年以来未选出民主党参议员。"),
    ("ohio", "ohio-senate-2026", "Ohio Senate 2026 (special)", "2026 年俄亥俄州联邦参议员特别选举", "Ohio",
     "Brown versus Husted: a former three-term senator trying to return after defeat, against the "
     "appointed incumbent holding the seat vacated by the vice president.",
     "布朗对赫斯特德：一位被击败后试图重返参议院的三届前参议员，对阵受任命、持有副总统一度空出席位的现任者。"),
    ("georgia", "georgia-senate-2026", "Georgia Senate 2026", "2026 年佐治亚州联邦参议员选举", "Georgia",
     "Ossoff versus Collins: an incumbent Democrat's formal, rally-centred re-election against a "
     "House Republican, ending in an 18-point margin that outpaced every poll.",
     "奥索夫对柯林斯：现任民主党人以正式演讲与大型集会为中心的连任选战，对阵一位共和党众议员，最终以超出所有民调的 18 个百分点获胜。"),
    ("south-carolina", "south-carolina-senate-2026", "South Carolina Senate 2026", "2026 南卡罗来纳州联邦参议员选举", "South Carolina",
     "Andrews versus Darline Graham: a sitting senator dies mid-cycle, his sister is appointed, and "
     "the state elects its first Democratic senator since 1998.",
     "安德鲁斯对达琳·格雷厄姆：一位在任参议员在选举周期中途去世，其妹受任命，该州选出 1998 年以来首位民主党参议员。"),
    ("los-angeles", "los-angeles-mayor-2026", "Los Angeles Mayor 2026", "2026 年洛杉矶市长选举", "Los Angeles",
     "Raman versus Bass: a nonpartisan municipal runoff in which a city councilmember unseated "
     "the incumbent mayor, with a celebrity candidate in the first round and a citywide turnout question.",
     "拉曼对巴斯：一场无党派市政决选，市议员击败现任市长；首轮有一位名人候选人，全市投票率成为问题。"),
]


def esc(v):
    return html.escape(str(v), quote=False)


def read_rows(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def frames_of(case_dir):
    for name in ("keyframes.csv", "frame_index.csv"):
        rows = read_rows(os.path.join(case_dir, "10_video_frames", name))
        if rows:
            return rows
    return []


def case_stats(case_dir):
    stats = {"rows": 0, "files": 0, "sources": 0, "events": 0, "videos": 0, "frames": 0,
             "results_rows": 0, "docs": 0, "images": 0}
    if not os.path.isdir(case_dir):
        return stats
    for folder in os.listdir(case_dir):
        sub = os.path.join(case_dir, folder)
        if not os.path.isdir(sub) or folder in ("site", "_staging", ".git"):
            continue
        for name in os.listdir(sub):
            if name.endswith(".csv"):
                p = os.path.join(sub, name)
                stats["rows"] += max(0, sum(1 for _ in open(p, encoding="utf-8-sig")) - 1)
                stats["files"] += 1
    stats["sources"] = len(read_rows(os.path.join(case_dir, "09_sources", "sources.csv")))
    stats["events"] = len(read_rows(os.path.join(case_dir, "02_campaign_events", "campaign_events.csv")))
    stats["videos"] = len(read_rows(os.path.join(case_dir, "10_video_frames", "video_sources.csv")))
    stats["frames"] = len(frames_of(case_dir))
    stats["results_rows"] = len(read_rows(os.path.join(case_dir, "07_electoral_context", "election_results.csv")))
    stats["images"] = len(read_rows(os.path.join(case_dir, "04_visual_archive", "image_archive.csv")))
    for base, _, files in os.walk(case_dir):
        if "site" in base.split(os.sep) or "_staging" in base.split(os.sep):
            continue
        stats["docs"] += sum(1 for n in files if n.endswith(".md"))
    return stats


def nav_links(up):
    return "".join(f'<a href="{up}cases/{c[0]}/index.html">{esc(c[4])}</a>' for c in CASES)


def inject_bar(path, label_en, label_zh, up):
    text = open(path, encoding="utf-8").read()
    if "archive-portal-bar" in text:
        return False
    bar = f"""<div class="archive-portal-bar" id="archive-portal-bar">
  <a class="apb-brand" href="{up}index.html">2026 Race Archive<span>2026 选举档案</span></a>
  <span class="apb-links">
    <a href="{up}index.html">Portal / 门户</a>
    {nav_links(up)}
  </span>
  <span class="apb-here">{esc(label_en)} / {esc(label_zh)}</span>
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


def copy_case(slug, case_dir, label_en, label_zh):
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
                rel_dir = os.path.relpath(os.path.dirname(path), SITE)
                depth = 0 if rel_dir == "." else len(rel_dir.split(os.sep))
                n += 1 if inject_bar(path, label_en, label_zh, "../" * depth) else 0
    print(f"  {slug}: copied, bar injected on {n} pages")
    return n


OVERRIDES_CSS = """/* shared width override so every case reads at the same measure */
.layout{max-width:1500px}
body.wide .layout{max-width:1500px}
@media (min-width:1560px){.layout,body.wide .layout{max-width:1640px}}
"""


def inject_overrides(slug):
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
main{max-width:1180px;margin:0 auto;padding:34px 22px 70px}
.hero h1{font-size:34px;line-height:1.15;margin:0 0 10px;font-weight:700}
.hero h1 .zh{display:block;font-size:.55em;color:var(--muted);font-weight:400;margin-top:6px}
.hero .lede{font-size:17px;color:#2c3138;max-width:80ch;margin:0 0 6px}
.hero .meta{font-size:13px;color:var(--muted)}
.cases{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:18px;margin:26px 0}
.case{background:#fff;border:1px solid var(--line);border-radius:12px;padding:20px 22px}
.case h2{font-size:21px;margin:0 0 2px}
.case h2 .zh{display:block;font-size:13px;color:var(--muted);font-weight:400;margin-top:3px}
.case p{font-size:14.5px;color:#39404b}
.case .hook{font-size:13.2px;color:#2c3138;background:#f6f7f9;border-left:3px solid var(--accent2);padding:6px 10px;border-radius:0 6px 6px 0}
.case .go{display:inline-block;margin-top:8px;background:var(--accent2);color:#fff;text-decoration:none;padding:8px 14px;border-radius:7px;font-size:14px}
.case .go:hover{background:#0c3d68}
table.cmp{width:100%;border-collapse:collapse;font-size:13.5px;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden}
table.cmp th,table.cmp td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left}
table.cmp thead th{background:#f3f4f7;font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
table.cmp td.num{font-variant-numeric:tabular-nums;text-align:right}
h2.section{font-size:16px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:34px 0 10px}
.foot{border-top:1px solid var(--line);margin-top:40px;padding-top:16px;font-size:12.5px;color:var(--muted)}
.method{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 18px;font-size:14px}
.method p{margin:8px 0}
@media (max-width:560px){.hero h1{font-size:26px}}
"""


def build_portal(stats):
    cards = []
    for slug, case_dir, en, zh, short, blurb_en, blurb_zh in CASES:
        s = stats[slug]
        hook = ""
        meta_path = os.path.join(ROOT, case_dir, "_staging", "case_meta.json")
        if os.path.exists(meta_path):
            meta = __import__("json").load(open(meta_path, encoding="utf-8"))
            if meta.get("phenomenon_zh"):
                hook = (f'<p class="hook"><b>研究切入点 / Hook.</b> {esc(meta["phenomenon_zh"])} '
                        f'<span style="color:var(--muted)">{esc(meta.get("phenomenon_en",""))}</span></p>')
        cards.append(f"""<section class="case">
  <h2>{esc(en)}<span class="zh">{esc(zh)}</span></h2>
  <p>{esc(blurb_en)}</p>
  <p>{esc(blurb_zh)}</p>
  {hook}
  <p class="meta">{s['rows']:,} CSV rows · {s['sources']} sources · {s['events']} events · {s['images']} images</p>
  <a class="go" href="cases/{slug}/index.html">Open case / 打开案例</a>
</section>""")

    metrics = [("CSV rows / CSV 行数", "rows"), ("Datasets / 数据集", "files"),
               ("Sources / 来源", "sources"), ("Documented events / 活动", "events"),
               ("Result rows / 结果行", "results_rows"), ("Image records / 图像", "images"),
               ("Docs / 文档", "docs")]
    head = "".join(f"<th>{esc(c[4])}</th>" for c in CASES)
    body_rows = ""
    for label, key in metrics:
        body_rows += f"<tr><th>{esc(label)}</th>" + "".join(
            f"<td class='num'>{stats[c[0]][key]:,}</td>" for c in CASES) + "</tr>"

    total_rows = sum(stats[c[0]]["rows"] for c in CASES)
    total_src = sum(stats[c[0]]["sources"] for c in CASES)
    body = f"""
<section class="hero">
  <h1>2026 American races: eight image-and-message case studies<span class="zh">2026 美国选战：八组形象与讯息案例</span></h1>
  <p class="lede">Eight races, one method: every table row traces to a retrieved URL, every inference is
  labelled, and anything the sources do not state is recorded as <code>unknown</code> rather than guessed.</p>
  <p class="lede">八场选举，一套方法：每一行都可追溯到已检索的 URL，每一处推断都标注，来源未给出的值记为
  <code>unknown</code> 而非猜测。</p>
  <p class="meta">{total_rows:,} CSV rows across eight cases · {total_src} sources · compiled 2026-11</p>
</section>

<section class="cases">
{''.join(cards)}
</section>

<h2 class="section">Side by side / 并排对比</h2>
<div style="overflow:auto"><table class="cmp">
  <thead><tr><th>Measure / 指标</th>{head}</tr></thead>
  <tbody>{body_rows}</tbody>
</table></div>

<h2 class="section">Shared method / 共同方法</h2>
<div class="method">
<p><strong>Citation contract.</strong> Every CSV row carries <code>SRC-####|https://...</code>; the id resolves in that
case's <code>09_sources/sources.csv</code>. Source tiers T1/T2/T3 are assigned mechanically from the domain, not from an
editorial judgement about accuracy. <code>unknown</code> is a recorded value, not a placeholder.</p>
<p><strong>Citation contract（中文）.</strong> 每个 CSV 行都带 <code>SRC-####|https://...</code>，其 id 可在该案例的
<code>09_sources/sources.csv</code> 中解析。T1/T2/T3 等级按域名机械判定，而非对准确性的编辑判断。
<code>unknown</code> 是取值，不是占位符。</p>
<p><strong>What differs between cases.</strong> Two cases (Texas, South Carolina) carry the full video/audio layer built
earlier. The six batch-2 cases are source-and-document archives: events, positions, money, results, imagery records and
bilingual narrative, with no frame extraction. Their README states the depth difference explicitly.</p>
<p><strong>案例之间的差别（中文）.</strong> 德州与南卡两案带有早前构建的完整视频／音频层。第二批六案是来源与文献档案：
活动、立场、资金、结果、影像记录与双语叙述，不含视频抽帧。各案 README 明确说明这一深度差异。</p>
</div>

<p class="foot">Compiled 2026-11. Eight case folders keep their own conventions documents and their own source tables;
nothing is merged at the data level, only at the browsing level.</p>
"""
    home = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>2026 Race Archive - eight case studies</title>
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
    for slug, case_dir, en, zh, *_ in CASES:
        copy_case(slug, case_dir, en, zh)
        print(f"  {slug}: width override linked on {inject_overrides(slug)} pages")
        relink_case(slug, case_dir)
    build_portal(stats)
    broken = audit()
    return 0 if not broken else 1


if __name__ == "__main__":
    sys.exit(main())
