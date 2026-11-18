"""Turn saved mirrors into plain text + a manifest (title, published date, size).

Also attempts a minimal PDF text extraction (FlateDecode + Tj/TJ operators).
"""
import os, re, json, csv, html, zlib, glob

CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(CASE, "_staging", "mirrors", "pages")
TEXT = os.path.join(CASE, "_staging", "mirrors", "text")
os.makedirs(TEXT, exist_ok=True)


def html_to_text(s):
    s = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?is)<!--.*?-->", " ", s)
    s = re.sub(r"(?is)<br\s*/?>", "\n", s)
    s = re.sub(r"(?is)</(p|div|h\d|li|tr|section|article|blockquote)>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\u00a0]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s)
    return s.strip()


def meta(s, name):
    m = re.search(r'(?is)<meta[^>]+(?:property|name)=["\']%s["\'][^>]+content=["\']([^"\']*)' % re.escape(name), s)
    if not m:
        m = re.search(r'(?is)<meta[^>]+content=["\']([^"\']*)["\'][^>]+(?:property|name)=["\']%s["\']' % re.escape(name), s)
    return html.unescape(m.group(1)).strip() if m else ""


def pdf_text(b):
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", b, re.S):
        raw = m.group(1)
        try:
            d = zlib.decompress(raw)
        except Exception:
            continue
        if b"Tj" not in d and b"TJ" not in d:
            continue
        for tm in re.finditer(rb"\((?:\\.|[^\\()])*\)", d):
            t = tm.group(0)[1:-1]
            t = re.sub(rb"\\([()\\])", rb"\1", t)
            out.append(t.decode("latin-1", "ignore"))
        out.append("\n")
    return re.sub(r"\n{2,}", "\n", "".join(out))


rows = []
for p in sorted(glob.glob(os.path.join(PAGES, "*"))):
    name = os.path.basename(p)
    base, ext = os.path.splitext(name)
    raw = open(p, "rb").read()
    if ext == ".pdf":
        txt = pdf_text(raw)
        title, pub = "", ""
    elif ext in (".html", ".mhtml") or raw[:200].lower().find(b"<html") >= 0:
        s = raw.decode("utf-8", "ignore")
        title = meta(s, "og:title") or meta(s, "twitter:title")
        if not title:
            m = re.search(r"(?is)<title[^>]*>(.*?)</title>", s)
            title = html_to_text(m.group(1)) if m else ""
        pub = meta(s, "article:published_time") or meta(s, "datePublished")
        if not pub:
            m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', s)
            pub = m.group(1) if m else ""
        txt = html_to_text(s)
    else:
        txt = raw.decode("utf-8", "ignore")
        title = pub = ""
    with open(os.path.join(TEXT, base + ".txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    rows.append(dict(file=name, base=base, kind=ext, title=title.strip(), published=pub.strip()[:30],
                     chars=len(txt)))

with open(os.path.join(CASE, "_staging", "mirror_manifest.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["file", "base", "kind", "title", "published", "chars"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(len(rows), "mirrors; empty text:", sum(1 for r in rows if r["chars"] < 200))
for r in rows[:8]:
    print(r["chars"], r["kind"], r["title"][:80])
