"""Open pages of the tailnet archive node in a real browser and verify what loaded.

Answers "can the page actually be opened?" without needing to look at pixels: every
network response is recorded, so a missing image or stylesheet shows up as a failing
URL rather than as an aesthetic judgement.

    python texas-senate-2026/_staging/check_remote_pages.py
    python texas-senate-2026/_staging/check_remote_pages.py site/video/frames.html
"""
import json
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

STAGING = Path(__file__).resolve().parent
DISC = STAGING / "discovery_result.json"
PROXY = "http://127.0.0.1:7897"
DEFAULT_PAGES = [
    "site/index.html",
    "site/events/index.html",
    "site/video/index.html",
    "site/video/frames.html",
    "site/visual/gallery.html",
    "site/compare/candidate-comparison.html",
    "site/sources/gaps.html",
]


def peer_ip(host):
    try:
        st = json.loads(subprocess.run(["tailscale", "status", "--json"], capture_output=True, text=True).stdout)
        for p in (st.get("Peer") or {}).values():
            if p.get("HostName") == host:
                return (p.get("TailscaleIPs") or [None])[0]
    except Exception:
        pass
    return None


def main(pages):
    disc = json.loads(DISC.read_text(encoding="utf-8"))
    base = disc["entry_url"].rsplit("/site/", 1)[0]
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-gpu"],
            proxy={"server": PROXY, "bypass": "100.64.0.0/10, *.ts.net"},
        )
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        print("%-42s %-5s %-6s %-7s %-8s %s" % ("page", "http", "imgs", "bad", "console", "title"))
        failures_total = 0
        for rel in pages:
            url = base + "/" + rel
            page = ctx.new_page()
            bad, imgs, errors = [], 0, []

            def on_response(r):
                nonlocal imgs
                if r.status >= 400:
                    bad.append("%s %s" % (r.status, r.url))
                ctype = (r.headers or {}).get("content-type", "")
                if ctype.startswith("image/"):
                    imgs += 1

            page.on("response", on_response)
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            try:
                resp = page.goto(url, wait_until="domcontentloaded", timeout=30_000)
                page.wait_for_timeout(900)
                try:
                    page.wait_for_function(
                        "() => [...document.images].every(i => i.complete)", timeout=90_000)
                except Exception:
                    pass
                status = resp.status if resp else None
                title = page.title()
                total_imgs = page.evaluate("() => document.images.length")
                broken_imgs = page.evaluate(
                    "() => [...document.images].filter(i => i.complete && i.naturalWidth === 0).length")
                imgs = max(imgs, total_imgs)
                if broken_imgs:
                    bad.append("%d broken <img>" % broken_imgs)
            except Exception as e:
                status, title = None, "EXC: %s" % type(e).__name__
            failures_total += len(bad)
            print("%-42s %-5s %-6d %-7d %-8d %s" % (rel, status, imgs, len(bad), len(errors), title[:46]))
            for b in bad[:4]:
                print("      failing:", b[:120])
            page.close()
        browser.close()
        print("\ntotal failing resources:", failures_total)
    return 0 if failures_total == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or DEFAULT_PAGES))
