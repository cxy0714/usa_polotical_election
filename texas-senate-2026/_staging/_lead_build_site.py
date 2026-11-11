#!/usr/bin/env python3
"""Build a fully static, offline-readable bilingual website for texas-senate-2026.

Design goals
  * opens by double-clicking site/index.html (no server, no CDN, no fetch())
  * every Markdown deliverable becomes a page with breadcrumb, section TOC, prev/next
  * bilingual reading modes: side-by-side / English only / Chinese only
  * every CSV dataset becomes a filterable HTML table plus a link to the raw file
  * licensed images render as a gallery with licence and photographer credit
  * a client-side search index spanning all headings and paragraphs

Run:  python _staging/_lead_build_site.py
Output: texas-senate-2026/site/
"""
import csv
import html
import json
import os
import re
import shutil
import sys
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
CJK = re.compile(r"[\u4e00-\u9fff]")


# ----------------------------------------------------------------------------- helpers
def esc(s):
    return html.escape(s, quote=False)


def esc_keep_br(s):
    s = esc(s)
    return s.replace("&lt;br&gt;", "<br>").replace("&lt;br/&gt;", "<br>")


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def slug(s):
    s = re.sub(r"[`*_\[\]()#|]", "", s)
    s = re.sub(r"[^\w\u4e00-\u9fff /-]+", "", s)
    s = s.strip().lower().replace(" ", "-").replace("/", "-")
    s = re.sub(r"-{2,}", "-", s)
    return s[:60] or "section"


FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)


def parse_front_matter(txt):
    m = FM_RE.match(txt)
    if not m:
        return {}, txt
    raw, body = m.group(1), txt[m.end():]
    data = {}
    key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if re.match(r"^\s+\S", line) and key:  # folded continuation
            data[key] = (data.get(key, "") + " " + line.strip()).strip()
            continue
        km = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if km:
            key = km.group(1)
            val = km.group(2).strip()
            if val in (">-", ">", "|"):
                data[key] = ""
            else:
                data[key] = val.strip('"').strip("'")
    return data, body


# ----------------------------------------------------------------------------- markdown
SRC_REL = ""      # repo-relative path of the markdown file being rendered


def inline(text, pages=None, here=None):
    """Inline markdown -> html. Code spans are stashed first so emphasis around them survives."""
    spans = []

    def stash(m):
        spans.append(m.group(1))
        return "\x00%d\x00" % (len(spans) - 1)

    s = re.sub(r"`([^`]+)`", stash, text)
    s = esc_keep_br(s)

    s = re.sub(
        r"!\[([^\]]*)\]\(([^)\s]+)\)",
        lambda m: '<img src="%s" alt="%s" loading="lazy">' % (asset_url(m.group(2)), esc(m.group(1))),
        s,
    )

    def link(m):
        label, url = m.group(1), m.group(2)
        url = url.replace("&amp;", "&")
        href = asset_url(url)
        if re.fullmatch(r"SRC-\d{4}", label.strip()):
            info = SOURCES.get(label.strip(), {})
            tip = info.get("publisher") or info.get("title") or ""
            return ('<a class="src" href="%s" target="_blank" rel="noopener" title="%s">%s</a>'
                    % (href, esc(tip[:120]), label))
        if href.startswith("http"):
            return '<a class="ext" href="%s" target="_blank" rel="noopener">%s</a>' % (href, label)
        return '<a href="%s">%s</a>' % (href, label)

    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: "<code>" + esc(spans[int(m.group(1))]) + "</code>", s)
    return s


def asset_url(url):
    """Resolve a repo-relative asset/link for the page currently being rendered."""
    url = url.strip()
    if url.startswith(("http://", "https://", "mailto:", "#")):
        return url
    frag = "#" + url.split("#", 1)[1] if "#" in url else ""
    target = url.split("#")[0]
    repo_target = os.path.normpath(os.path.join(os.path.dirname(SRC_REL), target)).replace(os.sep, "/")
    page_dir = os.path.dirname(os.path.join(SITE, HERE_PAGE))
    if repo_target.lower().endswith(".md") and repo_target in PAGES:
        return os.path.relpath(os.path.join(SITE, PAGES[repo_target]), page_dir).replace(os.sep, "/") + frag
    if os.path.exists(os.path.join(ROOT, repo_target)):
        return os.path.relpath(os.path.join(ROOT, repo_target), page_dir).replace(os.sep, "/") + frag
    return url + frag


SOURCES = {}   # SRC-#### -> {"url", "publisher", "title"}
TOKEN_RE = re.compile(r"(https?://[^\s<>\"']+|\bSRC-\d{4}\b)")


def load_sources():
    path = os.path.join(ROOT, "09_sources", "sources.csv")
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            SOURCES[r["source_id"]] = {
                "url": (r.get("url") or "").strip(),
                "publisher": (r.get("publisher") or "").strip(),
                "title": (r.get("title") or "").strip(),
            }
    return len(SOURCES)


def _link_token(m):
    """One pass, one regex: either a bare URL or an SRC-#### chip. Never re-process the result."""
    tok = m.group(0)
    if tok.startswith("http"):
        url = tok
        trail = ""
        while url and url[-1] in ").,;:!?":
            trail = url[-1] + trail
            url = url[:-1]
        if len(url) < 12:
            return tok
        return ('<a class="ext" href="%s" target="_blank" rel="noopener">%s</a>%s'
                % (html.escape(url), html.escape(url if len(url) <= 88 else url[:85] + "…"), trail))
    info = SOURCES.get(tok)
    if not info or not info["url"].startswith("http"):
        return tok
    tip = info["publisher"] or info["title"]
    return ('<a class="src" href="%s" target="_blank" rel="noopener" title="%s">%s</a>'
            % (html.escape(info["url"]), html.escape(tip[:120]), tok))


def linkify(fragment):
    """Linkify SRC-#### ids and bare URLs in text nodes only."""
    parts = re.split(r"(<code>.*?</code>|<pre>.*?</pre>|<a\b.*?</a>)", fragment, flags=re.S)
    out = []
    for part in parts:
        if part.startswith(("<code>", "<pre>", "<a")):
            out.append(part)
            continue
        for seg in re.split(r"(<[^>]+>)", part):
            if seg.startswith("<"):
                out.append(seg)
            else:
                out.append(TOKEN_RE.sub(_link_token, seg))
    return "".join(out)


def parse_blocks(body):
    lines = body.splitlines()
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        # fenced code
        if line.lstrip().startswith("```"):
            i += 1
            buf = []
            while i < n and not lines[i].lstrip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            blocks.append({"type": "code", "raw": "\n".join(buf)})
            continue
        # heading
        hm = re.match(r"^(#{1,6})\s+(.*)$", line)
        if hm:
            blocks.append({"type": "h", "level": len(hm.group(1)), "raw": hm.group(2).strip()})
            i += 1
            continue
        # hr
        if re.match(r"^(\s*)([-*_])\s*\2\s*\2[\s\2]*$", line) or line.strip() in ("---", "***", "___"):
            blocks.append({"type": "hr"})
            i += 1
            continue
        # table
        if line.strip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            header = split_row(line)
            aligns = []
            for cell in split_row(lines[i + 1]):
                c = cell.strip()
                aligns.append("right" if c.endswith(":") and not c.startswith(":") else "center" if c.startswith(":") and c.endswith(":") else "left")
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            blocks.append({"type": "table", "header": header, "aligns": aligns, "rows": rows})
            continue
        # blockquote
        if line.lstrip().startswith(">"):
            buf = []
            while i < n and (lines[i].lstrip().startswith(">") or not lines[i].strip()):
                if lines[i].lstrip().startswith(">"):
                    buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                elif buf and buf[-1].strip():
                    buf.append("")
                i += 1
            blocks.append({"type": "quote", "raw": "\n".join(buf)})
            continue
        # list
        if re.match(r"^\s*([-*+]|\d+\.)\s+", line):
            items, i = parse_list(lines, i)
            blocks.append({"type": "list", "items": items})
            continue
        # paragraph
        buf = [line]
        i += 1
        while i < n:
            nxt = lines[i]
            if not nxt.strip():
                break
            if re.match(r"^(#{1,6})\s", nxt) or nxt.lstrip().startswith(("```", ">", "|")) or re.match(r"^\s*([-*+]|\d+\.)\s+", nxt):
                break
            if nxt.strip() in ("---", "***", "___"):
                break
            buf.append(nxt)
            i += 1
        blocks.append({"type": "p", "raw": "\n".join(buf).strip()})
    return blocks


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    cells, cur, depth = [], [], 0
    in_code = False
    for ch in s:
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    cells.append("".join(cur).strip())
    return cells


def parse_list(lines, i):
    n = len(lines)
    items = []
    while i < n:
        m = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", lines[i])
        if not m:
            break
        indent = len(m.group(1))
        ordered = bool(re.match(r"^\d+\.", m.group(2)))
        text = m.group(3)
        i += 1
        cont = []
        while i < n:
            if not lines[i].strip():
                # allow one blank line inside a list only if next is a list item at deeper indent
                if i + 1 < n and re.match(r"^(\s*)([-*+]|\d+\.)\s+", lines[i + 1]):
                    i += 1
                    continue
                break
            nm = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", lines[i])
            if nm and len(nm.group(1)) <= indent:
                break
            if nm and len(nm.group(1)) > indent:
                break
            if re.match(r"^(#{1,6})\s", lines[i]):
                break
            cont.append(lines[i].strip())
            i += 1
        if cont:
            text += " " + " ".join(cont)
        items.append({"order": ordered, "depth": indent, "raw": text})
        # nested items
        while i < n:
            nm = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", lines[i])
            if nm and len(nm.group(1)) > indent:
                sub, i = parse_list(lines, i)
                items.extend(sub)
                continue
            break
    return items, i


# ----------------------------------------------------------------------------- rendering
PAGES = {}      # repo-relative md path -> site-relative html path
HERE_PAGE = ""  # page currently being rendered (site-relative)


def render_page(body, here_page, title_en, title_zh):
    global HERE_PAGE
    HERE_PAGE = here_page
    blocks = parse_blocks(body)
    # first pass: html + language tag
    rendered = []
    for b in blocks:
        t = b["type"]
        if t == "h":
            b["html"] = "<h%d id=\"%s\">%s</h%d>" % (b["level"], slug(re.sub(r"<[^>]+>", "", b["raw"])), esc(b["raw"]), b["level"])
            b["lang"] = "zh" if CJK.search(b["raw"]) else "en"
        elif t == "p":
            b["html"] = "<p>%s</p>" % inline(b["raw"], PAGES, here_page)
            b["lang"] = "zh" if CJK.search(b["raw"]) else "en"
        elif t == "quote":
            inner = []
            for para in re.split(r"\n\s*\n", b["raw"]):
                if para.strip():
                    inner.append("<p>%s</p>" % inline(para.strip().replace("\n", " "), PAGES, here_page))
            b["html"] = "<blockquote>%s</blockquote>" % "".join(inner)
            b["lang"] = "zh" if CJK.search(b["raw"]) else "en"
        elif t == "list":
            def build(items, idx, depth):
                out = []
                tag = "ol" if items[idx]["order"] else "ul"
                out.append("<%s>" % tag)
                while idx < len(items) and items[idx]["depth"] >= depth:
                    it = items[idx]
                    if it["depth"] > depth:
                        sub, idx = build(items, idx, it["depth"])
                        out.append(sub)
                        continue
                    lang = "zh" if CJK.search(it["raw"]) else "en"
                    idx += 1
                    if idx < len(items) and items[idx]["depth"] > depth:
                        tag2 = "ol" if items[idx]["order"] else "ul"
                        out.append('<li class="%s">%s<%s>' % (lang, inline(it["raw"]), tag2))
                        while idx < len(items) and items[idx]["depth"] > depth:
                            sub, idx = build(items, idx, items[idx]["depth"])
                            out.append(sub)
                        out.append("</li>")
                    else:
                        out.append('<li class="%s">%s</li>' % (lang, inline(it["raw"])))
                out.append("</%s>" % tag)
                return "".join(out), idx

            if b["items"]:
                html_list, _ = build(b["items"], 0, b["items"][0]["depth"])
            else:
                html_list = ""
            b["html"] = html_list
            b["lang"] = "zh" if CJK.search(" ".join(i["raw"] for i in b["items"])) else "en"
        elif t == "table":
            al = b["aligns"]
            h = "".join('<th style="text-align:%s">%s</th>' % (al[i] if i < len(al) else "left", esc_keep_br(c)) for i, c in enumerate(b["header"]))
            rows = []
            for r in b["rows"]:
                cells = []
                for i, c in enumerate(r):
                    cells.append('<td style="text-align:%s">%s</td>' % (al[i] if i < len(al) else "left", inline(c, PAGES, here_page) if "`" in c or "**" in c or "](" in c else esc_keep_br(c)))
                rows.append("<tr>%s</tr>" % "".join(cells))
            b["html"] = '<div class="table-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (h, "".join(rows))
            b["lang"] = "mix"
        elif t == "code":
            b["html"] = "<pre><code>%s</code></pre>" % esc(b["raw"])
            b["lang"] = "en"
        else:
            b["html"] = "<hr>"
            b["lang"] = "mix"
        rendered.append(b)

    # second pass: pair EN paragraph/quote with following ZH block of same type
    out = []
    idx = 0
    while idx < len(rendered):
        b = rendered[idx]
        nxt = rendered[idx + 1] if idx + 1 < len(rendered) else None
        if (
            nxt
            and b["type"] in ("p", "quote")
            and b["type"] == nxt["type"]
            and b["lang"] == "en"
            and nxt["lang"] == "zh"
        ):
            out.append('<div class="pair"><div class="col en">%s</div><div class="col zh">%s</div></div>' % (b["html"], nxt["html"]))
            idx += 2
            continue
        if b["type"] == "h":
            out.append(b["html"])
        else:
            out.append('<div class="blk %s">%s</div>' % (b["lang"], b["html"]))
        idx += 1
    return linkify("\n".join(out))


# ----------------------------------------------------------------------------- page shell
NAV = [
    ("index.html", "首页", "Home"),
    ("events/index.html", "事件", "Events"),
    ("candidates/index.html", "候选人", "Candidates"),
    ("speeches/index.html", "演讲", "Speeches"),
    ("visual/index.html", "影像", "Images"),
    ("video/index.html", "视频帧", "Video frames"),
    ("media/index.html", "媒体与资金", "Media & Money"),
    ("context/index.html", "选举背景", "Context"),
    ("compare/index.html", "对比分析", "Comparison"),
    ("sources/index.html", "来源与缺口", "Sources & Gaps"),
    ("about.html", "关于档案", "About"),
]

CSS = """
:root{--bg:#fbfaf7;--fg:#1c1b19;--muted:#6b6760;--line:#e3ded4;--accent:#8c2f1e;--accent2:#1f4e5f;--card:#fff;--en:#1c1b19;--zh:#243b4a}
@media (prefers-color-scheme:dark){:root{--bg:#16171a;--fg:#e8e6e1;--muted:#a3a09a;--line:#2e3138;--accent:#e0796a;--accent2:#7fb3c4;--card:#1d1f24;--en:#e8e6e1;--zh:#a9c6d6}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.72 -apple-system,"Segoe UI","Noto Sans SC","Source Han Sans SC","PingFang SC","Microsoft YaHei",sans-serif}
a{color:var(--accent2);text-decoration:none}
a:hover{text-decoration:underline}
header.top{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top-in{max-width:1280px;margin:0 auto;display:flex;align-items:center;gap:1rem;padding:.6rem 1.1rem;flex-wrap:wrap}
.brand{font-weight:700;letter-spacing:.01em;color:var(--fg)}
.brand small{display:block;font-weight:400;color:var(--muted);font-size:.72rem}
nav.main{display:flex;gap:.15rem;flex-wrap:wrap;margin-left:auto}
nav.main a{padding:.28rem .55rem;border-radius:6px;color:var(--muted);font-size:.9rem}
nav.main a.on,nav.main a:hover{background:var(--line);color:var(--fg);text-decoration:none}
.modes{display:flex;gap:.2rem;border:1px solid var(--line);border-radius:8px;padding:.15rem}
.modes button{background:none;border:0;color:var(--muted);font:inherit;font-size:.8rem;padding:.2rem .45rem;border-radius:6px;cursor:pointer}
.modes button.on{background:var(--accent);color:#fff}
.layout{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:250px minmax(0,1fr);gap:2rem;padding:1.6rem 1.1rem 4rem}
aside.toc{position:sticky;top:4.2rem;align-self:start;max-height:calc(100vh - 5rem);overflow:auto;font-size:.86rem;border-left:2px solid var(--line);padding-left:.9rem}
aside.toc h4{margin:.2rem 0 .6rem;font-size:.72rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
aside.toc a{display:block;padding:.18rem 0;color:var(--muted);line-height:1.45}
aside.toc a:hover{color:var(--fg)}
aside.toc a.h3{padding-left:.7rem;font-size:.82rem;opacity:.85}
main{min-width:0}
.crumb{font-size:.8rem;color:var(--muted);margin-bottom:1rem}
.crumb a{color:var(--muted)}
h1{font-size:1.85rem;line-height:1.3;margin:.2rem 0 .4rem}
h1 .zh{display:block;font-size:1.15rem;color:var(--muted);font-weight:500;margin-top:.35rem}
h2{font-size:1.28rem;margin:2.4rem 0 .7rem;padding-top:.6rem;border-top:1px solid var(--line)}
h3{font-size:1.08rem;margin:1.7rem 0 .5rem}
h4{font-size:1rem;margin:1.3rem 0 .4rem}
p{margin:.55rem 0}
code{background:var(--line);padding:.08em .32em;border-radius:4px;font-size:.86em;font-family:ui-monospace,SFMono-Regular,Consolas,monospace}
pre{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem;overflow:auto}
pre code{background:none;padding:0;font-size:.82rem;line-height:1.55}
blockquote{margin:1rem 0;padding:.7rem 1rem;border-left:3px solid var(--accent);background:var(--card);border-radius:0 8px 8px 0}
blockquote p{margin:.35rem 0}
.table-wrap{overflow:auto;margin:1rem 0;border:1px solid var(--line);border-radius:10px;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:.86rem}
th,td{padding:.5rem .65rem;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--line);font-weight:600;position:sticky;top:0;font-size:.8rem;white-space:nowrap}
tbody tr:hover{background:color-mix(in srgb,var(--line) 45%,transparent)}
ul,ol{margin:.5rem 0 .7rem;padding-left:1.35rem}
li{margin:.22rem 0}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:1.6rem;margin:.6rem 0;align-items:start}
.pair .col{min-width:0}
.pair .en{color:var(--en)}
.pair .zh{color:var(--zh);border-left:2px solid var(--line);padding-left:1.1rem;font-size:.97em}
body.mode-en .zh,body.mode-en .pair .zh{display:none}
body.mode-en .pair{grid-template-columns:1fr}
body.mode-zh .en,body.mode-zh .pair .en{display:none}
body.mode-zh .pair{grid-template-columns:1fr}
body.mode-zh li.en,body.mode-zh .blk.en{display:none}
body.mode-en li.zh,body.mode-en .blk.zh{display:none}
.blk.mix{display:block}
.meta{display:flex;gap:1.2rem;flex-wrap:wrap;font-size:.8rem;color:var(--muted);margin:.4rem 0 1.4rem;padding-bottom:.9rem;border-bottom:1px solid var(--line)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(255px,1fr));gap:1rem;margin:1.2rem 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1rem 1.1rem;transition:.15s}
.card:hover{border-color:var(--accent);transform:translateY(-1px)}
.card h3{margin:.1rem 0 .45rem;font-size:1.02rem}
.card p{margin:.2rem 0;color:var(--muted);font-size:.85rem;line-height:1.6}
.card .n{font-size:1.5rem;font-weight:700;color:var(--accent);line-height:1.1}
.stats{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:.8rem;margin:1.2rem 0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.75rem .9rem}
.stat b{display:block;font-size:1.45rem;color:var(--accent);line-height:1.2}
.stat span{font-size:.78rem;color:var(--muted)}
.hero{background:linear-gradient(135deg,color-mix(in srgb,var(--accent) 12%,transparent),color-mix(in srgb,var(--accent2) 12%,transparent));border:1px solid var(--line);border-radius:16px;padding:2rem 1.8rem;margin:0 0 1.6rem}
.hero h1{margin:0 0 .5rem;font-size:2.1rem}
.hero p{color:var(--muted);max-width:62ch}
.search{position:relative;margin:1.2rem 0}
.search input{width:100%;padding:.85rem 1rem;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--fg);font:inherit}
#results{margin-top:.8rem;display:grid;gap:.5rem}
.hit{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.7rem .9rem}
.hit .t{font-weight:600}
.hit .s{font-size:.8rem;color:var(--muted);margin-top:.2rem}
.hit mark{background:color-mix(in srgb,var(--accent) 30%,transparent);color:inherit}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:1rem}
.gal figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.gal img{width:100%;height:210px;object-fit:cover;display:block;background:var(--line)}
.gal figcaption{padding:.55rem .65rem;font-size:.74rem;color:var(--muted);line-height:1.45}
.gal figcaption b{color:var(--fg);font-weight:600;display:block;font-size:.8rem}
.pager{display:flex;justify-content:space-between;gap:1rem;margin:3rem 0 0;padding-top:1.2rem;border-top:1px solid var(--line);font-size:.9rem}
footer{border-top:1px solid var(--line);margin-top:3rem;padding:1.4rem 1.1rem;color:var(--muted);font-size:.8rem}
footer .in{max-width:1280px;margin:0 auto;display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap}
.src{font-family:ui-monospace,Consolas,monospace;font-size:.78em;padding:.02em .32em;border:1px solid var(--line);border-radius:4px;color:var(--accent2);white-space:nowrap;text-decoration:none}
.src:hover{background:color-mix(in srgb,var(--accent2) 14%,transparent);text-decoration:none;border-color:var(--accent2)}
a.ext::after{content:" ↗";font-size:.8em;opacity:.65}
.nolink{display:flex;flex-direction:column;justify-content:center;align-items:center;height:210px;padding:1rem;text-align:center;background:repeating-linear-gradient(45deg,var(--line) 0 6px,transparent 6px 12px);font-size:.8rem;color:var(--muted)}
.shots{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.6rem;margin:1rem 0 1.6rem}
.shots a{display:block;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:var(--card)}
.shots img{width:100%;height:130px;object-fit:cover;display:block}
.shots span{display:block;font-size:.68rem;color:var(--muted);padding:.25rem .35rem;line-height:1.35}
.tag{display:inline-block;font-size:.72rem;padding:.1rem .45rem;border-radius:999px;background:var(--line);color:var(--muted);margin-right:.3rem}
.warn{background:color-mix(in srgb,var(--accent) 9%,transparent);border:1px solid color-mix(in srgb,var(--accent) 35%,transparent);border-radius:10px;padding:.85rem 1rem;margin:1rem 0;font-size:.9rem}
@media(max-width:960px){.layout{grid-template-columns:1fr}aside.toc{display:none}.pair{grid-template-columns:1fr}.pair .zh{border-left:0;padding-left:0;border-top:1px dashed var(--line);padding-top:.6rem}}
@media print{header.top,aside.toc,.modes,.pager,footer{display:none}.pair{display:block}.pair .zh{margin-top:.4rem}}
"""

JS = """
(function(){
  var body=document.body;
  function setMode(m){
    body.classList.remove('mode-en','mode-zh');
    if(m==='en')body.classList.add('mode-en');
    if(m==='zh')body.classList.add('mode-zh');
    document.querySelectorAll('.modes button').forEach(function(b){b.classList.toggle('on',b.dataset.mode===m)});
    try{localStorage.setItem('dsh-mode',m)}catch(e){}
  }
  document.querySelectorAll('.modes button').forEach(function(b){b.addEventListener('click',function(){setMode(b.dataset.mode)})});
  var saved='both'; try{saved=localStorage.getItem('dsh-mode')||'both'}catch(e){}
  setMode(saved);

  // table filter
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

  // search
  var box=document.getElementById('q'), res=document.getElementById('results');
  if(box&&res&&window.SEARCH_INDEX){
    var timer=null;
    function run(){
      var q=box.value.trim().toLowerCase();
      if(q.length<2){res.innerHTML='<div class="hit"><div class="s">输入至少 2 个字符开始检索 / Type at least 2 characters.</div></div>';return;}
      var hits=[];
      SEARCH_INDEX.forEach(function(e){
        var hay=(e.t+' '+e.b).toLowerCase();
        var i=hay.indexOf(q);
        if(i>-1){
          var start=Math.max(0,i-40), frag=e.b.substr(start,150);
          hits.push({t:e.t,u:e.u,b:frag,n:e.n});
        }
      });
      hits=hits.slice(0,40);
      if(!hits.length){res.innerHTML='<div class="hit"><div class="s">没有匹配项 / No matches.</div></div>';return;}
      res.innerHTML=hits.map(function(h){
        var safe=h.b.replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]});
        var re=new RegExp('('+q.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')+')','ig');
        safe=safe.replace(re,'<mark>$1</mark>');
        return '<a class="hit" href="'+h.u+'"><div class="t">'+h.t+'</div><div class="s">'+h.n+' · '+safe+'…</div></a>';
      }).join('');
    }
    box.addEventListener('input',function(){clearTimeout(timer);timer=setTimeout(run,120)});
  }
})();
"""


def shell(here, title_en, title_zh, main_html, toc_html="", crumb="", pager="", extra_head=""):
    depth = here.count("/")
    prefix = "../" * depth if depth else ""
    if 'class="crumb"' in toc_html and not crumb:
        crumb, toc_html = toc_html, ""
    if crumb:
        crumb = re.sub(r'href="(?!(?:https?:|#|\.\./|/))', 'href="' + prefix, crumb)
    nav = []
    for href, zh, en in NAV:
        on = " on" if here == href or (href.endswith("index.html") and here.startswith(href.rsplit("/", 1)[0] + "/") and href != "index.html") else ""
        nav.append(f'<a class="{on.strip()}" href="{prefix}{href}">{zh}<span style="opacity:.6;font-size:.78em"> {en}</span></a>')
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title_zh)} · {esc(title_en)}</title>
<style>{CSS}</style>{extra_head}
</head><body>
<header class="top"><div class="top-in">
  <div class="brand">Texas Senate 2026 <small>案例研究 001 · 双语档案</small></div>
  <nav class="main">{''.join(nav)}</nav>
  <div class="modes" role="group" aria-label="语言模式">
    <button data-mode="both" class="on">双语</button><button data-mode="en">EN</button><button data-mode="zh">中文</button>
  </div>
</div></header>
<div class="layout">
  <aside class="toc">{toc_html}</aside>
  <main>
    {crumb}
    <h1>{esc(title_en)}<span class="zh">{esc(title_zh)}</span></h1>
    {main_html}
    {pager}
  </main>
</div>
<footer><div class="in">
  <span>American Political Image Lab · 案例研究 001 · 生成于 2026-11-10 · 全部内容可离线阅读</span>
  <span>所有事实均可溯源至 09_sources/sources.csv 的 SRC-#### 编号</span>
</div></footer>
<script src="{prefix}assets/app.js"></script>
</body></html>"""


def build_toc(blocks_html):
    items = re.findall(r'<h([23]) id="([^"]+)">(.*?)</h[23]>', blocks_html, re.S)
    if len(items) < 2:
        return ""
    out = ['<h4>本页目录 / On this page</h4>']
    for lvl, hid, txt in items:
        txt = re.sub(r"<[^>]+>", "", txt)
        cls = "h3" if lvl == "3" else ""
        out.append(f'<a class="{cls}" href="#{hid}">{esc(txt)}</a>')
    return "\n".join(out)


# ----------------------------------------------------------------------------- page specs
def md_page(src_rel, out_rel, crumb_html="", pager="", extra_html=""):
    """Render one Markdown deliverable into out_rel."""
    src = os.path.join(ROOT, src_rel.replace("/", os.sep))
    global SRC_REL
    SRC_REL = src_rel
    txt = read(src)
    fm, body = parse_front_matter(txt)
    title_en = fm.get("title") or os.path.basename(src_rel)
    title_zh = fm.get("title_zh") or title_en
    body = re.sub(r"^#\s+.*\n", "", body, count=1)  # drop duplicate H1
    inner = render_page(body, out_rel, title_en, title_zh)
    toc = build_toc(inner)
    meta = []
    for k, lab in (("status", "状态"), ("last_updated", "更新"), ("compiled_by", "编译"), ("research_period", "研究区间")):
        if fm.get(k):
            meta.append(f'<span>{lab}：{esc(fm[k])}</span>')
    meta.append(f'<span>源文件：<a href="{os.path.relpath(src, os.path.dirname(os.path.join(SITE, out_rel))).replace(os.sep, "/")}">{esc(src_rel)}</a></span>')
    main = '<div class="meta">%s</div>' % "".join(meta)
    if fm.get("coverage_note"):
        main += '<div class="warn"><b>覆盖范围说明 / Coverage note.</b> %s</div>' % inline(fm["coverage_note"], PAGES, out_rel)
    if extra_html:
        main += extra_html
    main += inner
    out = os.path.join(SITE, out_rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(shell(out_rel, title_en, title_zh, main, toc, crumb_html, pager))
    return {"en": title_en, "zh": title_zh, "out": out_rel}


def csv_table(src_rel, table_id, note="", up="../../"):
    src = os.path.join(ROOT, src_rel.replace("/", os.sep))
    with open(src, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    dl = "../../" + src_rel
    if not rows:
        return ('<div class="warn">该数据集目前只有表头、没有数据行——这是有意为之，原因见 '
                '<a href="' + up + 'sources/gaps.html">研究缺口</a>。</div>'
                '<p><a href="' + dl + '" download>下载原始 CSV</a></p>')
    cols = list(rows[0].keys())
    head = "".join("<th>%s</th>" % esc(c) for c in cols)
    body = []
    for r in rows:
        cells = "".join("<td>%s</td>" % linkify(esc_keep_br(r[c])) for c in cols)
        body.append("<tr>%s</tr>" % cells)
    return (note
            + '<div class="search" style="margin:.6rem 0"><input data-filter="%s" placeholder="筛选本表（任意字段） / Filter this table"></div>' % table_id
            + '<div class="table-wrap" style="max-height:76vh"><table id="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (table_id, head, "".join(body))
            + '<div class="warn" style="margin:.8rem 0 0">表中 <b>SRC-####</b> 编号与裸网址都可点击，直接跳转原始来源（新标签页）。</div>'
            + '<div class="meta"><span>%d 行 / rows</span><span><a href="%s" download>下载原始 CSV</a></span>'
              '<span>字段中文释义见 <a href="../sources/dictionary.html">双语数据字典</a></span></div>' % (len(rows), dl))


def write(out_rel, title_en, title_zh, main, toc="", crumb="", pager=""):
    out = os.path.join(SITE, out_rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(out) or SITE, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(shell(out_rel, title_en, title_zh, main, toc, crumb, pager))


def crumb(path_parts):
    parts = []
    for i, (href, zh) in enumerate(path_parts):
        parts.append(f'<a href="{href}">{zh}</a>')
    return '<div class="crumb">' + " › ".join(parts) + "</div>"


# ----------------------------------------------------------------------------- main build
def main():
    print("sources loaded: %d" % load_sources())
    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(os.path.join(SITE, "assets"))
    # GitHub Pages must not run Jekyll over this static export.
    open(os.path.join(SITE, ".nojekyll"), "w", encoding="utf-8").close()

    # ---- page registry (md path -> html path). Must exist before rendering links.
    reg = [
        ("README.md", "about.html"),
        ("research_gaps.md", "sources/gaps.html"),
        ("_research_conventions.md", "sources/conventions.html"),
        ("09_sources/data_dictionary_bilingual.md", "sources/dictionary.html"),
        ("02_campaign_events/talarico_timeline.md", "events/talarico-timeline.html"),
        ("02_campaign_events/paxton_timeline.md", "events/paxton-timeline.html"),
        ("02_campaign_events/event_coverage_gaps.md", "events/coverage-gaps.html"),
        ("01_candidates/talarico/biography.md", "candidates/talarico-biography.html"),
        ("01_candidates/talarico/political_positions.md", "candidates/talarico-positions.html"),
        ("01_candidates/paxton/biography.md", "candidates/paxton-biography.html"),
        ("01_candidates/paxton/political_positions.md", "candidates/paxton-positions.html"),
        ("03_speeches/communication_analysis_talarico.md", "speeches/comm-talarico.html"),
        ("03_speeches/communication_analysis_paxton.md", "speeches/comm-paxton.html"),
        ("05_campaign_media/media_narrative_timeline.md", "media/narrative.html"),
        ("04_visual_archive/visual_analysis_talarico.md", "visual/analysis-talarico.html"),
        ("04_visual_archive/visual_analysis_paxton.md", "visual/analysis-paxton.html"),
        ("10_video_frames/README.md", "video/method.html"),
        ("07_electoral_context/election_context.md", "context/election-context.html"),
        ("08_comparative_analysis/candidate_comparison.md", "compare/candidate-comparison.html"),
        ("08_comparative_analysis/campaign_timeline_comparison.md", "compare/timeline-comparison.html"),
        ("08_comparative_analysis/campaign_organization.md", "compare/organization.html"),
    ]
    for dp, _, fs in os.walk(ROOT):
        if "_staging" in dp or "site" in dp.split(os.sep):
            continue
        for f in fs:
            if re.match(r"^(?:TAL|PAX)-SPC-", f) and f.endswith(".md"):
                rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")
                if "key_speech_analysis" in rel:
                    reg.append((rel, "speeches/" + f.replace(".md", ".html")))
                elif "transcripts" in rel:
                    reg.append((rel, "speeches/transcript-ms-now.html"))
    for rel, out in reg:
        PAGES[os.path.normpath(rel).replace(os.sep, "/")] = out

    # ---- assets
    with open(os.path.join(SITE, "assets", "app.js"), "w", encoding="utf-8") as f:
        f.write(JS)

    search = []

    # ---- about (README)
    info = md_page("README.md", "about.html")
    search.append({"t": "关于本档案 / About", "u": "about.html", "b": "案例研究 001 双语档案说明", "n": "关于"})

    # ---- events
    os.makedirs(os.path.join(SITE, "events"), exist_ok=True)
    for rel, out in [
        ("02_campaign_events/talarico_timeline.md", "events/talarico-timeline.html"),
        ("02_campaign_events/paxton_timeline.md", "events/paxton-timeline.html"),
        ("02_campaign_events/event_coverage_gaps.md", "events/coverage-gaps.html"),
    ]:
        r = md_page(rel, out, crumb([("index.html", "首页"), ("events/index.html", "事件")]))
        search.append({"t": r["zh"], "u": out, "b": r["en"], "n": "事件"})
    with open(os.path.join(ROOT, "02_campaign_events", "campaign_events.csv"), newline="", encoding="utf-8-sig") as fh:
        ev = list(csv.DictReader(fh))
    events_table = csv_table(
        "02_campaign_events/campaign_events.csv", "tbl-events",
        '<div class="warn">这是本档案的核心交付物：<b>93 条</b>事件记录，27 个字段。字段名保持英文以保证机器可读，中文释义见 <a href="../sources/dictionary.html">双语数据字典</a>。每一行的 <code>source_urls</code> 指向 <code>SRC-####</code> 编号。</div>',
    )
    write(
        "events/data.html", "All campaign events (dataset)", "全部竞选事件（数据集）",
        events_table,
        crumb([("index.html", "首页"), ("events/index.html", "事件")]),
    )
    counts = OrderedDict()
    for r in ev:
        counts.setdefault(r["candidate_id"], {"held": 0, "cancelled": 0, "announced": 0, "disputed": 0})
        counts[r["candidate_id"]][r["event_status"]] = counts[r["candidate_id"]].get(r["event_status"], 0) + 1
    ev_index = f"""<div class="hero"><p>事件重构按两条平行的候选人时间线组织，并有完整数据集可筛选。所有活动均标注状态（已举行／已宣布／已取消／存疑），不做推测性补全。</p></div>
<div class="stats">
  <div class="stat"><b>{len(ev)}</b><span>事件记录</span></div>
  <div class="stat"><b>{sum(1 for r in ev if r['candidate_id']=='TALARICO')}</b><span>塔拉里科</span></div>
  <div class="stat"><b>{sum(1 for r in ev if r['candidate_id']=='PAXTON')}</b><span>帕克斯顿</span></div>
  <div class="stat"><b>{sum(1 for r in ev if r['event_status']=='held')}</b><span>有证据显示已举行</span></div>
  <div class="stat"><b>{sum(1 for r in ev if r['event_status']=='cancelled')}</b><span>已取消</span></div>
</div>
<div class="cards">
  <a class="card" href="talarico-timeline.html"><h3>塔拉里科竞选时间线</h3><p>逐条叙事，含三层目的、视觉记录与来源。</p></a>
  <a class="card" href="paxton-timeline.html"><h3>帕克斯顿竞选时间线</h3><p>含取消站点的完整记录与代理活动。</p></a>
  <a class="card" href="coverage-gaps.html"><h3>事件覆盖缺口</h3><p>哪些活动查不到、为什么查不到。</p></a>
  <a class="card" href="data.html"><h3>事件数据集（可筛选）</h3><p>{len(ev)} 行 × 27 字段，逐行溯源。</p></a>
</div>"""
    write("events/index.html", "Campaign events", "竞选事件", ev_index)
    search.append({"t": "事件 / Events", "u": "events/index.html", "b": "93 条竞选事件时间线与数据集", "n": "事件"})

    # ---- candidates
    os.makedirs(os.path.join(SITE, "candidates"), exist_ok=True)
    for rel, out in [
        ("01_candidates/talarico/biography.md", "candidates/talarico-biography.html"),
        ("01_candidates/talarico/political_positions.md", "candidates/talarico-positions.html"),
        ("01_candidates/paxton/biography.md", "candidates/paxton-biography.html"),
        ("01_candidates/paxton/political_positions.md", "candidates/paxton-positions.html"),
    ]:
        r = md_page(rel, out, crumb([("index.html", "首页"), ("candidates/index.html", "候选人")]))
        search.append({"t": r["zh"], "u": out, "b": r["en"], "n": "候选人"})
    pol = csv_table("01_candidates/policy_positions.csv", "tbl-policy", '<div class="warn">146 条政策立场，12 个议题维度，两位候选人并置。每条含候选人原话、立法记录、对手批评与事实核查。</div>')
    write("candidates/policy-data.html", "Policy positions (dataset)", "政策立场矩阵（数据集）", pol, crumb([("index.html", "首页"), ("candidates/index.html", "候选人")]))
    write(
        "candidates/index.html", "Candidates", "候选人",
        """<div class="hero"><p>两位候选人的背景、履历与政策立场。这些材料用于支撑事件解读，不是完整传记；所有法律程序表述区分「指控／起诉／弹劾／无罪判定／和解」。</p></div>
<div class="cards">
  <a class="card" href="talarico-biography.html"><h3>塔拉里科 · 传记</h3><p>成长、教育、教职、州众议院任期与大选。</p></a>
  <a class="card" href="talarico-positions.html"><h3>塔拉里科 · 政策立场</h3><p>12 维度 80 条，含原话与立法记录对照。</p></a>
  <a class="card" href="paxton-biography.html"><h3>帕克斯顿 · 传记</h3><p>含逐项法律程序记录与治理风格。</p></a>
  <a class="card" href="paxton-positions.html"><h3>帕克斯顿 · 政策立场</h3><p>12 维度 66 条，来源不对称已注明。</p></a>
  <a class="card" href="policy-data.html"><h3>政策立场矩阵（可筛选）</h3><p>146 行 × 15 字段。</p></a>
</div>""",
    )
    search.append({"t": "候选人 / Candidates", "u": "candidates/index.html", "b": "传记与政策立场", "n": "候选人"})

    # ---- speeches
    os.makedirs(os.path.join(SITE, "speeches"), exist_ok=True)
    for rel, out in [
        ("03_speeches/communication_analysis_talarico.md", "speeches/comm-talarico.html"),
        ("03_speeches/communication_analysis_paxton.md", "speeches/comm-paxton.html"),
    ]:
        r = md_page(rel, out, crumb([("index.html", "首页"), ("speeches/index.html", "演讲")]))
        search.append({"t": r["zh"], "u": out, "b": r["en"], "n": "演讲"})
    speech_files = sorted(
        f for f in os.listdir(os.path.join(ROOT, "03_speeches", "key_speech_analysis")) if f.endswith(".md")
    )
    cards = []
    for f in speech_files:
        rel = "03_speeches/key_speech_analysis/" + f
        out = "speeches/" + f.replace(".md", ".html")
        r = md_page(rel, out, crumb([("index.html", "首页"), ("speeches/index.html", "演讲")]))
        search.append({"t": r["zh"], "u": out, "b": r["en"], "n": "演讲分析"})
        cards.append(f'<a class="card" href="{f.replace(".md", ".html")}"><h3>{esc(r["zh"])}</h3><p>{esc(r["en"])}</p></a>')
    tr = os.path.join(ROOT, "03_speeches", "transcripts")
    if os.path.isdir(tr):
        for f in sorted(x for x in os.listdir(tr) if x.endswith(".md")):
            rel = "03_speeches/transcripts/" + f
            out = "speeches/transcript-ms-now.html"
            r = md_page(rel, out, crumb([("index.html", "首页"), ("speeches/index.html", "演讲")]))
            search.append({"t": r["zh"], "u": out, "b": r["en"], "n": "逐字稿"})
            cards.append(f'<a class="card" href="transcript-ms-now.html"><h3>{esc(r["zh"])}</h3><p>{esc(r["en"])}<br><span class="tag">唯一的真实逐字稿</span></p></a>')
    write(
        "speeches/index.html", "Speeches & communication", "演讲与传播",
        f"""<div class="hero"><p>32 条演讲记录、31 条视频索引、24 篇十节分析。引语全部保留英文原文并附中文译文；韵律字段一律 <code>unknown</code>，因为从未核对音视频。</p></div>
<div class="cards">
  <a class="card" href="comm-talarico.html"><h3>塔拉里科 · 传播风格分析</h3><p>13 个维度，含韵律限制说明。</p></a>
  <a class="card" href="comm-paxton.html"><h3>帕克斯顿 · 传播风格分析</h3><p>同一结构，便于对照阅读。</p></a>
  <a class="card" href="data.html"><h3>演讲数据集</h3><p>32 行演讲 + 31 行视频索引。</p></a>
</div>
<h2>24 篇关键演讲分析 / Key speech analyses</h2>
<div class="cards">{''.join(cards)}</div>""",
    )
    sp = csv_table("03_speeches/speech_archive.csv", "tbl-speech", "")
    sp += '<h2>视频索引 / Video index</h2>' + csv_table("03_speeches/speech_video_index.csv", "tbl-video", "")
    write("speeches/data.html", "Speech datasets", "演讲数据集", sp, crumb([("index.html", "首页"), ("speeches/index.html", "演讲")]))
    search.append({"t": "演讲 / Speeches", "u": "speeches/index.html", "b": "24 篇关键演讲分析、传播风格与数据集", "n": "演讲"})

    # ---- visual
    os.makedirs(os.path.join(SITE, "visual"), exist_ok=True)
    with open(os.path.join(ROOT, "04_visual_archive", "image_archive.csv"), newline="", encoding="utf-8-sig") as fh:
        imgs = list(csv.DictReader(fh))
    licensed = [r for r in imgs if r["local_filename"] != "unknown"]
    n_tal = sum(1 for r in imgs if r["candidate_id"] == "TALARICO")
    n_pax = sum(1 for r in imgs if r["candidate_id"] == "PAXTON")

    def img_caption(r):
        src_link = ""
        u = (r.get("source_url") or "").strip()
        if u.startswith("http"):
            src_link = ' · <a class="ext" href="%s" target="_blank" rel="noopener">来源页</a>' % html.escape(u)
        return ('<figcaption><b>%s · %s</b>%s · %s<br>%s%s</figcaption>'
                % (esc(r["image_id"]), esc(r["candidate_id"]), esc(r["image_date"]),
                   esc(r["photographer"]), esc(r["license"]), src_link))

    def figure(r):
        if r["local_filename"] != "unknown":
            src = "../../04_visual_archive/" + r["local_filename"].replace("\\", "/")
            return ('<figure id="%s"><a href="%s" target="_blank"><img src="%s" alt="%s" loading="lazy"></a>%s</figure>'
                    % (esc(r["image_id"].lower()), esc(src), esc(src),
                       esc(r["image_id"] + " " + r["candidate_id"]), img_caption(r)))
        u = (r.get("source_url") or "").strip()
        link = ('<a class="ext" href="%s" target="_blank" rel="noopener">在来源处查看</a>' % html.escape(u)) \
            if u.startswith("http") else '<span>来源链接不可用</span>'
        return ('<figure id="%s"><div class="nolink"><b>%s</b><span>仅链接 · 未复制 / link only</span>%s</div>%s</figure>'
                % (esc(r["image_id"].lower()), esc(r["image_id"]), link, img_caption(r)))

    def contact_sheet(cand, limit=24):
        rows = [r for r in imgs if r["candidate_id"] == cand]
        local = [r for r in rows if r["local_filename"] != "unknown"]
        cells = []
        for r in local[:limit]:
            src = "../../04_visual_archive/" + r["local_filename"].replace("\\", "/")
            cells.append('<a href="gallery.html#%s"><img src="%s" alt="%s" loading="lazy"><span>%s · %s</span></a>'
                         % (esc(r["image_id"].lower()), esc(src), esc(r["image_id"]),
                            esc(r["image_date"]), esc(r["photographer"][:26])))
        more = ""
        if len(local) > limit:
            more = ('<p class="meta"><span>此处仅列前 %d 张；全部 %d 张本地副本见 <a href="gallery.html">图库</a>。</span></p>'
                    % (limit, len(local)))
        return ('<h2 id="contact-sheet">影像索引 / Image index</h2>'
                '<p>本页直接加载可本地展示的 <b>%d</b> 张影像（该候选人共 %d 条记录，其余 %d 条只保留来源链接）。'
                '点击缩略图可打开原图。<b>这些照片只用于核对「视觉形象」的可观察事实</b>——面部几何、身体比例与着装仍未测量。</p>'
                % (len(local), len(rows), len(rows) - len(local))
                + '<div class="shots">' + "".join(cells) + "</div>" + more)

    for rel, out, cand in [
        ("04_visual_archive/visual_analysis_talarico.md", "visual/analysis-talarico.html", "TALARICO"),
        ("04_visual_archive/visual_analysis_paxton.md", "visual/analysis-paxton.html", "PAXTON"),
    ]:
        r = md_page(rel, out, crumb([("index.html", "首页"), ("visual/index.html", "影像")]), extra_html=contact_sheet(cand))
        search.append({"t": r["zh"], "u": out, "b": r["en"], "n": "影像"})

    gallery = ('<div class="warn">%d 条影像记录全部列出：<b>%d 张</b>为可本地展示的许可副本（点击可看原图），'
               '其余 %d 条为「保留所有权利、仅链接」——只给来源页链接，不复制、不外链嵌入。'
               '注意：塔拉里科 %d 条、帕克斯顿 %d 条，其中帕克斯顿多条来自同一场宣布参选记者会，这一偏斜必须在任何比较性使用中说明。</div>'
               % (len(imgs), len(licensed), len(imgs) - len(licensed), n_tal, n_pax)
               + '<h2 id="tal">塔拉里科 / Talarico — %d 条记录（%d 张本地副本）</h2>' % (n_tal, sum(1 for r in imgs if r["candidate_id"] == "TALARICO" and r["local_filename"] != "unknown"))
               + '<div class="gal">' + "".join(figure(r) for r in imgs if r["candidate_id"] == "TALARICO") + '</div>'
               + '<h2 id="pax">帕克斯顿 / Paxton — %d 条记录（%d 张本地副本）</h2>' % (n_pax, len(licensed) - sum(1 for r in imgs if r["candidate_id"] == "TALARICO" and r["local_filename"] != "unknown"))
               + '<div class="gal">' + "".join(figure(r) for r in imgs if r["candidate_id"] == "PAXTON") + '</div>')
    write("visual/gallery.html", "Image gallery", "影像图库", gallery, crumb([("index.html", "首页"), ("visual/index.html", "影像")]))
    write(
        "visual/index.html", "Visual archive", "影像档案",
        f"""<div class="hero"><p>影像档案记录来源、许可、摄影者与画幅统计；<b>图片在页面内直接加载</b>，可点击看原图或跳转来源页。画面本身的取景与舞台记录现已由<a href="../video/index.html">视频帧集</a>补齐（YuNet 检测 + SFace 身份匹配），但<b>面部几何、身体比例与着装仍未测量</b>；任何外貌论断都不得从本档案直接产生。</p></div>
<div class="stats">
  <div class="stat"><b>{len(imgs)}</b><span>影像记录</span></div>
  <div class="stat"><b>{len(licensed)}</b><span>可本地展示的许可副本</span></div>
  <div class="stat"><b>{n_tal}</b><span>塔拉里科</span></div>
  <div class="stat"><b>{n_pax}</b><span>帕克斯顿</span></div>
</div>
<div class="cards">
  <a class="card" href="analysis-talarico.html"><h3>塔拉里科 · 视觉分析</h3><p>构图、场景、品牌符号与测量规程；页内含影像索引条。</p></a>
  <a class="card" href="analysis-paxton.html"><h3>帕克斯顿 · 视觉分析</h3><p>会议讲台偏斜、旗帜符号与测量规程；页内含影像索引条。</p></a>
  <a class="card" href="gallery.html"><h3>图库</h3><p>{len(imgs)} 条全部列出，其中 {len(licensed)} 张直接显示。</p></a>
  <a class="card" href="data.html"><h3>影像数据集</h3><p>{len(imgs)} 行 × 21 字段，网址可点击。</p></a>
</div>""",
    )
    vis = csv_table("04_visual_archive/image_archive.csv", "tbl-img", '<div class="warn"><code>framing</code>、<code>camera_angle</code>、<code>face_visibility</code>、<code>body_visibility</code>、<code>clothing_notes</code> 全部为 <code>unknown</code>——这是明确的证据限制，不是待办事项。</div>')
    write("visual/data.html", "Image dataset", "影像数据集", vis, crumb([("index.html", "首页"), ("visual/index.html", "影像")]))
    search.append({"t": "影像 / Images", "u": "visual/index.html", "b": "影像档案、图库与视觉分析", "n": "影像"})

    # ---- video frames
    os.makedirs(os.path.join(SITE, "video"), exist_ok=True)
    with open(os.path.join(ROOT, "10_video_frames", "frame_index.csv"), newline="", encoding="utf-8-sig") as fh:
        vframes = list(csv.DictReader(fh))
    with open(os.path.join(ROOT, "10_video_frames", "video_sources.csv"), newline="", encoding="utf-8-sig") as fh:
        vsrc = list(csv.DictReader(fh))
    nf_tal = sum(1 for r in vframes if r["identity"] == "TALARICO")
    nf_pax = sum(1 for r in vframes if r["identity"] == "PAXTON")
    n_official = sum(1 for v in vsrc if "official campaign" in (v.get("channel") or "").lower())

    rm = md_page("10_video_frames/README.md", "video/method.html",
                 crumb([("index.html", "首页"), ("video/index.html", "视频帧")]))
    search.append({"t": rm["zh"], "u": "video/method.html", "b": rm["en"], "n": "视频帧"})

    def vf_caption(row):
        return ('<figcaption><b>%s · %s</b>t=%ss · 相似度 %s · %s<br>%s<br><span class="tag">%s</span></figcaption>'
                % (esc(row["frame_id"].split("_t")[0].upper()), esc(row["identity"]),
                   esc(row["timestamp_s"]), esc(row["identity_sim"]), esc(row["shot_scale"]),
                   esc(row["source_title"]), esc(row["event_kind"])))

    def vf_figure(row):
        src = "../../" + row["frame_path"].replace("\\", "/")
        return ('<figure><a href="%s" target="_blank"><img src="%s" alt="%s" loading="lazy"></a>%s</figure>'
                % (esc(src), esc(src), esc(row["identity"] + " " + row["video_id"]), vf_caption(row)))

    gal_tal = "".join(vf_figure(r) for r in vframes if r["identity"] == "TALARICO")
    gal_pax = "".join(vf_figure(r) for r in vframes if r["identity"] == "PAXTON")
    write("video/frames.html", "Face-matched frame gallery", "人脸识别帧图库",
          '<div class="warn">这些帧来自新闻与官方竞选视频，仅作内部研究参考，<b>未经授权不得公开发布</b>。'
          '识别标签来自 SFace 余弦匹配（阈值与方法见 <a href="method.html">方法页</a>），每张图都标注相似度。</div>'
          '<h2 id="tal">塔拉里科 / Talarico — %d 帧</h2><div class="gal">%s</div>'
          '<h2 id="pax">帕克斯顿 / Paxton — %d 帧</h2><div class="gal">%s</div>'
          % (nf_tal, gal_tal, nf_pax, gal_pax),
          crumb([("index.html", "首页"), ("video/index.html", "视频帧")]))

    vf_data = ('<div class="warn">帧索引：身份、相似度、时间码、景别、人脸像素、清晰度、亮度与躯干区 RGB 均值。'
               '<b>躯干 RGB 是粗测，常混入背景</b>，不能当作"他穿什么"。</div>'
               + csv_table("10_video_frames/frame_index.csv", "tbl-vframes", "", up="../")
               + '<h2>源视频 / Source videos</h2>' + csv_table("10_video_frames/video_sources.csv", "tbl-vsrc", "", up="../"))
    write("video/data.html", "Video frame datasets", "视频帧数据集", vf_data,
          crumb([("index.html", "首页"), ("video/index.html", "视频帧")]))

    sheets = "".join(
        '<figure><a href="../../10_video_frames/%s" target="_blank"><img src="../../10_video_frames/%s" alt="%s" loading="lazy"></a>'
        '<figcaption><b>%s</b>%s</figcaption></figure>' % (f, f, t, t, sub)
        for f, t, sub in [
            ("sheet_duel.jpg", "双人对照缩略图", "每位候选人 12 帧并置"),
            ("sheet_talarico_frames.jpg", "塔拉里科缩略图", "按相似度排序"),
            ("sheet_paxton_frames.jpg", "帕克斯顿缩略图", "按相似度排序"),
            ("sheet_context.jpg", "场景语境缩略图", "每段视频 3 帧，不含身份判定"),
        ])
    write(
        "video/index.html", "Video frame set", "视频帧集",
        f"""<div class="hero"><p>从 {len(vsrc)} 段公开视频（{n_official} 段官方竞选频道、其余为地方电视台新闻包或第三方上传）中每 0.5–1 秒采样，用 YuNet 检测人脸、SFace 与档案内授权照片比对身份，再对<b>同一场景、同一着装</b>的重复帧做感知哈希去重，留下 <b>{len(vframes)}</b> 帧。这是本档案第一次真正拿到两位候选人的画面：此前取景、舞台与着装全部是 <code>unknown</code>。</p></div>
<div class="stats">
  <div class="stat"><b>{len(vsrc)}</b><span>源视频</span></div>
  <div class="stat"><b>{len(vframes)}</b><span>精选识别帧</span></div>
  <div class="stat"><b>{nf_tal}</b><span>塔拉里科帧</span></div>
  <div class="stat"><b>{nf_pax}</b><span>帕克斯顿帧</span></div>
  <div class="stat"><b>0.499 / 0.123</b><span>参考库同类／异类余弦</span></div>
</div>
<div class="warn"><b>三条必须先读的说明：</b>① 这些帧裁自 YouTube 上的竞选团队与电视台视频，<b>仅限内部研究</b>，公开使用需换授权素材或做仅链接处理；② 识别标签是带分数的算法判定，<b>不是人工逐帧核对</b>；③ 样本为 {len(vframes)} 帧、{len(vsrc)} 段视频，不能支撑"频率"类论断。</div>
<div class="cards">
  <a class="card" href="frames.html"><h3>识别帧图库</h3><p>{len(vframes)} 帧分候选人陈列，含相似度与景别。</p></a>
  <a class="card" href="method.html"><h3>方法与局限</h3><p>采样、检测、SFace 阈值、验证与版权说明。</p></a>
  <a class="card" href="data.html"><h3>帧索引与源视频（数据集）</h3><p>逐帧测量值 + 每段视频的频道、日期与链接。</p></a>
</div>
<h2>对照缩略图 / Contact sheets</h2>
<div class="gal">{sheets}</div>""",
    )
    search.append({"t": "视频帧 / Video frames", "u": "video/index.html",
                   "b": "YuNet 检测 + SFace 身份匹配的竞选视频帧", "n": "视频帧"})

    # ---- media & finance
    os.makedirs(os.path.join(SITE, "media"), exist_ok=True)
    r = md_page("05_campaign_media/media_narrative_timeline.md", "media/narrative.html", crumb([("index.html", "首页"), ("media/index.html", "媒体与资金")]))
    search.append({"t": r["zh"], "u": "media/narrative.html", "b": r["en"], "n": "媒体"})
    write(
        "media/ads.html", "Advertisements (dataset)", "广告（数据集）",
        csv_table("05_campaign_media/advertisements.csv", "tbl-ads", '<div class="warn">注意区分投放主体：候选人竞选团队 vs 外部政治行动委员会。帕克斯顿一方有据可查的候选人广告仅 1 支，外部团体 8 支。</div>'),
        crumb([("index.html", "首页"), ("media/index.html", "媒体与资金")]),
    )
    write(
        "media/social.html", "Social media (dataset)", "社交媒体（数据集）",
        csv_table("05_campaign_media/social_media.csv", "tbl-social", ""),
        crumb([("index.html", "首页"), ("media/index.html", "媒体与资金")]),
    )
    write(
        "media/coverage.html", "Media coverage (dataset)", "媒体报道（数据集）",
        csv_table("05_campaign_media/media_coverage.csv", "tbl-cov", '<div class="warn">66 条报道、47 家媒体。本表不设单一核实字段，改用 <code>source_tier</code> 与 <code>reliability_notes</code>。</div>'),
        crumb([("index.html", "首页"), ("media/index.html", "媒体与资金")]),
    )
    write(
        "finance/data.html", "Campaign finance (dataset)", "竞选资金（数据集）",
        csv_table("06_campaign_finance/campaign_finance.csv", "tbl-fin", '<div class="warn"><b>绝不可相加：</b>本表同时容纳 FEC 申报、FEC 独立支出（Schedule E）、AdImpact 广告监测与阵营宣称四类口径不同的数据，相差可达一个数量级。</div>'),
        crumb([("index.html", "首页"), ("media/index.html", "媒体与资金")]),
    )
    write(
        "media/index.html", "Media, advertising & money", "媒体、广告与资金",
        """<div class="hero"><p>广告、社交媒体、媒体报道与竞选资金。核心原则：阵营宣称、独立报道、官方申报三类数据在结构上分开记录，不混合、不相加。</p></div>
<div class="cards">
  <a class="card" href="narrative.html"><h3>媒体叙事时间线</h3><p>7 个叙事阶段，含「同一事件、两套说辞」对照。</p></a>
  <a class="card" href="ads.html"><h3>广告（23 支）</h3><p>按投放主体分类，含事实核查。</p></a>
  <a class="card" href="social.html"><h3>社交媒体（12 条）</h3><p>含政党账号与候选人账号的区分。</p></a>
  <a class="card" href="coverage.html"><h3>媒体报道（66 条）</h3><p>47 家媒体，含框架编码。</p></a>
  <a class="card" href="../finance/data.html"><h3>竞选资金（69 条）</h3><p>FEC 申报期 + 独立支出 + AdImpact。</p></a>
</div>""",
    )
    search.append({"t": "媒体与资金 / Media & Money", "u": "media/index.html", "b": "广告、社交、报道与资金", "n": "媒体"})

    # ---- context
    os.makedirs(os.path.join(SITE, "context"), exist_ok=True)
    r = md_page("07_electoral_context/election_context.md", "context/election-context.html", crumb([("index.html", "首页"), ("context/index.html", "选举背景")]))
    search.append({"t": r["zh"], "u": "context/election-context.html", "b": r["en"], "n": "背景"})
    write("context/results.html", "Election results (dataset)", "选举结果（数据集）", csv_table("07_electoral_context/election_results.csv", "tbl-res", '<div class="warn">注意区分<b>选举夜部分计票</b>与<b>最终结果</b>：66% 计票时曾显示 59.4%，那<b>不是</b>结果。</div>'), crumb([("index.html", "首页"), ("context/index.html", "选举背景")]))
    write("context/polling.html", "Polling (dataset)", "民调（数据集）", csv_table("07_electoral_context/polling.csv", "tbl-poll", ""), crumb([("index.html", "首页"), ("context/index.html", "选举背景")]))
    write(
        "context/index.html", "Electoral context", "选举背景",
        """<div class="hero"><p>这场选举的结构：初选、决选、大选、选后期，以及 2026 年中期选举的整体环境。分析提示：德州结果属于全国性浪潮的一部分，不应把胜负完全归因于任何一方的竞选选择。</p></div>
<div class="cards">
  <a class="card" href="election-context.html"><h3>选举背景（全文）</h3><p>四阶段 + 关键日期 + 民调走势 + 已知缺口。</p></a>
  <a class="card" href="results.html"><h3>选举结果数据集</h3><p>含认证结果汇总与部分计票的区分。</p></a>
  <a class="card" href="polling.html"><h3>民调数据集</h3><p>11 条民调与均值。</p></a>
</div>""",
    )
    search.append({"t": "选举背景 / Context", "u": "context/index.html", "b": "选举结构与结果", "n": "背景"})

    # ---- compare
    os.makedirs(os.path.join(SITE, "compare"), exist_ok=True)
    for rel, out in [
        ("08_comparative_analysis/candidate_comparison.md", "compare/candidate-comparison.html"),
        ("08_comparative_analysis/campaign_timeline_comparison.md", "compare/timeline-comparison.html"),
        ("08_comparative_analysis/campaign_organization.md", "compare/organization.html"),
    ]:
        r = md_page(rel, out, crumb([("index.html", "首页"), ("compare/index.html", "对比分析")]))
        search.append({"t": r["zh"], "u": out, "b": r["en"], "n": "对比"})
    write(
        "compare/index.html", "Comparative analysis", "对比分析",
        """<div class="hero"><p>结构性对比：组织、讯息架构、时间线碰撞、视觉识别与资金结构。<b>本档案不作优劣排序</b>——差异被记录，因果关系不作裁定。</p></div>
<div class="cards">
  <a class="card" href="candidate-comparison.html"><h3>候选人结构对比</h3><p>13 节：从阵营结构到可安全断言与不可断言清单。</p></a>
  <a class="card" href="timeline-comparison.html"><h3>时间线对比</h3><p>按月、按阶段、10 月逐日碰撞。</p></a>
  <a class="card" href="organization.html"><h3>竞选组织</h3><p>人事、委员会、记录的实质性不对称。</p></a>
</div>""",
    )
    search.append({"t": "对比分析 / Comparison", "u": "compare/index.html", "b": "候选人结构、时间线与组织对比", "n": "对比"})

    # ---- sources
    os.makedirs(os.path.join(SITE, "sources"), exist_ok=True)
    for rel, out in [
        ("research_gaps.md", "sources/gaps.html"),
        ("09_sources/data_dictionary_bilingual.md", "sources/dictionary.html"),
        ("_research_conventions.md", "sources/conventions.html"),
    ]:
        if os.path.exists(os.path.join(ROOT, rel.replace("/", os.sep))):
            r = md_page(rel, out, crumb([("index.html", "首页"), ("sources/index.html", "来源与缺口")]))
            search.append({"t": r["zh"], "u": out, "b": r["en"], "n": "来源"})
    write("sources/registry.html", "Source registry (dataset)", "来源总表（数据集）", csv_table("09_sources/sources.csv", "tbl-src", '<div class="warn">189 个唯一来源。层级：T1 官方记录、T2 主流媒体、T3 党派／评论、pointer_only 仅指针。</div>'), crumb([("index.html", "首页"), ("sources/index.html", "来源与缺口")]))
    write(
        "sources/index.html", "Sources and gaps", "来源与缺口",
        """<div class="hero"><p>可溯源是本档案的评判标准。这里给出 189 个来源、双语数据字典、以及一份把「查不到」逐条写明的缺口登记。</p></div>
<div class="cards">
  <a class="card" href="registry.html"><h3>来源总表（189）</h3><p>层级、类型、用途与可靠性备注。</p></a>
  <a class="card" href="dictionary.html"><h3>双语数据字典</h3><p>所有 CSV 字段与受控词表的中英对照。</p></a>
  <a class="card" href="gaps.html"><h3>研究缺口</h3><p>工具限制、数据缺口、口径陷阱。</p></a>
  <a class="card" href="conventions.html"><h3>数据契约</h3><p>编号体系、词表、三层目的规则。</p></a>
</div>""",
    )
    search.append({"t": "来源与缺口 / Sources & Gaps", "u": "sources/index.html", "b": "来源总表与缺口登记", "n": "来源"})

    # ---- index
    stats = [
        (len(ev), ("事件记录", "events")),
        (146, ("政策立场", "positions")),
        (32, ("演讲记录", "speeches")),
        (24, ("演讲分析", "analyses")),
        (len(imgs), ("影像记录", "images")),
        (len(vframes), ("识别帧", "video frames")),
        (23, ("广告", "ads")),
        (66, ("媒体报道", "coverage items")),
        (69, ("财务条目", "finance rows")),
        (189, ("来源", "sources")),
        (45, ("双语文档", "bilingual docs")),
    ]
    stat_html = "".join(f'<div class="stat"><b>{n}</b><span>{z[0]} · {z[1]}</span></div>' for n, z in stats)
    index_main = f"""<div class="hero">
  <h1 style="font-size:2rem">American Political Image Lab<span class="zh" style="font-size:1rem">案例研究 001 · 2026 年德州联邦参议员选举：塔拉里科 vs. 帕克斯顿</span></h1>
  <div class="pair">
    <div class="col en"><p>A bilingual, line-by-line sourced archive of one campaign process. <b>It collects and organises evidence; it does not judge which side ran a better campaign.</b> What gets narrated, and which events and images deserve emphasis, is left to the researcher.</p></div>
    <div class="col zh"><p>一份中英双语、逐条溯源的竞选过程档案。<b>它收集并组织证据，不评判哪一方更成功。</b>最终如何叙述、强调哪些事件与影像，由研究者决定。</p></div>
  </div>
  <p style="margin-top:.5rem"><span class="tag">93 events</span><span class="tag">146 positions</span><span class="tag">32 speeches</span><span class="tag">116 images</span><span class="tag">{len(vsrc)} videos</span><span class="tag">{len(vframes)} frames</span><span class="tag">189 sources</span><span class="tag">EN + 中文</span></p>
</div>
<div class="search"><input id="q" placeholder="站内检索：输入事件名、城市、人名、关键词…… / Search across the archive"><div id="results"></div></div>
<h2>数据概览 / At a glance</h2>
<div class="stats">{stat_html}</div>
<h2>从这里开始 / Start here</h2>
<div class="cards">
  <a class="card" href="events/index.html"><h3>① 竞选事件 · Events</h3><p><span class="en">Every documented activity of both candidates: date, place, purpose, message, visual record.</span><br><span class="zh">两位候选人全部有据可查的活动：时间、地点、目的、讯息、视觉记录。</span></p></a>
  <a class="card" href="compare/candidate-comparison.html"><h3>② 结构对比 · Comparison</h3><p><span class="en">Structural differences in organisation, message architecture, timelines, money and imagery.</span><br><span class="zh">组织、讯息、时间线、资金与影像的结构性差异。</span></p></a>
  <a class="card" href="sources/gaps.html"><h3>③ 研究缺口 · Gaps</h3><p><span class="en">Read this before deciding which conclusions are safe to write.</span><br><span class="zh">先读这一份，再判断哪些结论可以安全地写。</span></p></a>
  <a class="card" href="about.html"><h3>④ 档案说明 · About</h3><p><span class="en">Directory map, data conventions, limits and reuse rules.</span><br><span class="zh">目录结构、数据约定、局限与复用规则。</span></p></a>
</div>
<h2>三段必须知道的前提 / Three cautionary notes</h2>
<div class="warn"><b>一、没有辩论 / No debate took place.</b><br><span class="en">Five records reconstruct the full sequence of invitations and refusals; the CNN–Jubilee event was a solo town hall that several outlets mislabelled as a debate.</span><br><span class="zh">五条记录还原了辩论邀请与拒绝的完整过程；CNN–Jubilee 那场是单人问答，被多家媒体误标为辩论。</span></div>
<div class="warn"><b>二、外貌仍未测量，但画面已可读 / Appearance still unmeasured, imagery now readable.</b><br><span class="en">The archive now ships a face-detected video frame set (<a href="video/index.html">video frames</a>), so framing and staging are documented. But facial geometry, body proportions and clothing remain unmeasured; the reproducible measurement protocol is still waiting for a human to execute it.</span><br><span class="zh">档案现已附上经人脸检测的视频帧集（<a href="video/index.html">视频帧</a>），取景与舞台布置因此有了记录。但面部几何、身体比例与着装<b>仍未测量</b>；可复现的测量规程仍在等待人工执行。</span></div>
<div class="warn"><b>三、资金口径不可相加 / Money measures cannot be summed.</b><br><span class="en">FEC independent expenditures and AdImpact ad tracking differ by roughly an order of magnitude, and four different Talarico "totals" exist. Section 6 of the data dictionary lists every trap.</span><br><span class="zh">FEC 独立支出与 AdImpact 广告投放相差约一个数量级；塔拉里科存在四种不同的「总额」。数据字典第 6 节列出全部陷阱。</span></div>
<h2>阅读方式 / How to read</h2>
<div class="pair">
  <div class="col en"><p>Each page carries a <b>Both / EN / 中文</b> switch in the top bar. In both mode English sits on the left and Chinese on the right, compared paragraph by paragraph; tables keep bilingual cells. Every quotation stays verbatim in English with a <code>（译：…）</code> rendering so it can be checked against the source.</p></div>
  <div class="col zh"><p>每个页面顶部有 <b>双语 / EN / 中文</b> 三档切换。双语模式下英文在左、中文在右，逐段对照；表格保留双语单元格。所有引语保留英文原文并附<code>（译：…）</code>，便于回查。</p></div>
</div>
<div class="pair">
  <div class="col en"><p>Works offline: the site loads no external resources. Double-click <code>site/index.html</code>.</p></div>
  <div class="col zh"><p>离线可用：本站不依赖任何外网资源，直接双击 <code>site/index.html</code> 即可。</p></div>
</div>"""
    write("index.html", "Case Study 001 — Bilingual archive", "案例研究 001 · 双语档案", index_main)

    # ---- search index
    with open(os.path.join(SITE, "assets", "search-index.js"), "w", encoding="utf-8") as f:
        f.write("window.SEARCH_INDEX=" + json.dumps(search, ensure_ascii=False) + ";")

    n_pages = sum(len(fs) for _, _, fs in os.walk(SITE))
    print(f"built site: {n_pages} files in {SITE}")
    print(f"registered md pages: {len(PAGES)}")


if __name__ == "__main__":
    sys.exit(main())
