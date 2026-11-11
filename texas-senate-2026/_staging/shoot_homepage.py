"""Screenshot the archive homepage discovered on the tailnet.

Reads texas-senate-2026/_staging/discovery_result.json (written by
discover_archive.py), opens entry_url in headless Chromium and saves a PNG.

Network notes for this laptop: a local proxy (127.0.0.1:7897) is configured system-wide
and cannot route tailnet addresses (it answers 502), so each launch attempt routes the
tailnet around it — first via an explicit proxy with a bypass list, then fully direct
with the peer IP injected, then the bare IP URL.
"""
import json
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

STAGING = Path(__file__).resolve().parent
DISC = STAGING / "discovery_result.json"
OUT = STAGING / "checks"
PROXY = "http://127.0.0.1:7897"


def peer_ip(host):
    try:
        st = json.loads(subprocess.run(["tailscale", "status", "--json"], capture_output=True, text=True).stdout)
        for p in (st.get("Peer") or {}).values():
            if p.get("HostName") == host:
                return (p.get("TailscaleIPs") or [None])[0]
    except Exception:
        pass
    return None


def main():
    disc = json.loads(DISC.read_text(encoding="utf-8"))
    url = disc["entry_url"]
    dns = disc["dnsname"].rstrip(".")
    ip = peer_ip(disc["host"])
    OUT.mkdir(parents=True, exist_ok=True)

    common = ["--no-sandbox", "--disable-gpu", "--hide-scrollbars"]
    attempts = [
        ("proxy+bypass", dict(proxy={"server": PROXY, "bypass": "100.64.0.0/10, *.ts.net"}),
         common, url),
        ("direct+resolve", dict(proxy={"server": "direct://"}),
         common + (["--host-resolver-rules=MAP %s %s" % (dns, ip)] if ip else []), url),
        ("direct+ip", dict(proxy={"server": "direct://"}), common,
         "http://%s/site/index.html" % ip if ip else url),
    ]

    with sync_playwright() as pw:
        for label, launch_kw, args, target in attempts:
            browser = pw.chromium.launch(headless=True, args=args, **launch_kw)
            ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
            page = ctx.new_page()
            try:
                resp = page.goto(target, wait_until="load", timeout=30_000)
                status = resp.status if resp else None
                if status != 200:
                    print("FAIL attempt=%s: HTTP %s" % (label, status))
                    browser.close()
                    continue
                page.wait_for_timeout(1500)
                shot = OUT / "homepage_sjtu-cxy_1440x900.png"
                page.screenshot(path=str(shot), full_page=False)
                full = OUT / "homepage_sjtu-cxy_full.png"
                page.screenshot(path=str(full), full_page=True)
                print("OK attempt=%s status=%s" % (label, status))
                print("url:", page.url)
                print("title:", page.title())
                print("saved:", shot)
                print("saved:", full)
                browser.close()
                return 0
            except Exception as e:
                print("FAIL attempt=%s: %s: %s" % (label, type(e).__name__, str(e).splitlines()[0]))
                browser.close()
    return 1


if __name__ == "__main__":
    sys.exit(main())
