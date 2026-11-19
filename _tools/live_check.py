#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe the deployed GitHub Pages demo: portal, case entry pages, video pages and assets.

    python _tools/live_check.py https://cxy0714.github.io/usa_polotical_election/

Only same-origin links are followed; every URL is requested once (HEAD, falling back to
GET). Prints a summary and the first broken targets.
"""
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "Mozilla/5.0 (compatible; archive-link-check)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:  # noqa: BLE001
        return 0, str(e).encode()


def links(html, base):
    out = set()
    for m in re.finditer(r'(?:href|src)="([^"#?]+)', html):
        u = urllib.parse.urljoin(base, m.group(1))
        out.add(u)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    base = sys.argv[1] if len(sys.argv) > 1 else "https://cxy0714.github.io/usa_polotical_election/"
    if not base.endswith("/"):
        base += "/"
    roots = [base, base + "site/index.html"]
    # every case entry page plus its video page
    status, html = get(base + "site/index.html")
    portal = html.decode("utf-8", "replace")
    case_entries = sorted({u for u in links(portal, base + "site/index.html")
                           if "/cases/" in u and u.endswith("/index.html")})
    seeds = roots + case_entries + [u.replace("index.html", "video/index.html") for u in case_entries]
    todo, seen, broken = [], set(), []
    for s in seeds:
        if s not in seen:
            seen.add(s)
            todo.append(s)
    # one level of assets/links from the seeds
    for s in list(todo):
        code, body = get(s)
        if code != 200:
            broken.append((s, code))
            continue
        for u in links(body.decode("utf-8", "replace"), s):
            if not u.startswith(base) or u in seen:
                continue
            seen.add(u)
            todo.append(u)
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda u: (u, get(u)[0]), todo))
    broken += [(u, c) for u, c in results if c != 200 and (u, c) not in broken]
    print(f"checked {len(todo)} urls from {base}")
    print(f"broken: {len(broken)}")
    for u, c in broken[:25]:
        print(f"  {c} {u}")


if __name__ == "__main__":
    main()
