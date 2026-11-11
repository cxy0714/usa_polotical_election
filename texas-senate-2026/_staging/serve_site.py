"""Serve the offline bilingual site over HTTP so another machine can view it.

Why this exists: the site is a set of static files, but its pages reference assets
that live OUTSIDE `site/` (curated frames in `10_video_frames/`, licensed photos in
`04_visual_archive/`, source CSVs). So the web root must be the `texas-senate-2026/`
folder, and the entry URL is `/site/index.html` — serving `site/` alone gives 404s on
every image.

Usage
-----
    python texas-senate-2026/_staging/serve_site.py                # 127.0.0.1:8000
    python texas-senate-2026/_staging/serve_site.py --port 8080
    python texas-senate-2026/_staging/serve_site.py --bind 0.0.0.0     # tailnet/LAN
    python texas-senate-2026/_staging/serve_site.py --bind 100.x.y.z   # this Tailscale IP

Then on the viewing machine open http://<server-ip>:<port>/site/index.html

Recommended for Tailscale: keep the default 127.0.0.1 binding and run
    tailscale serve --bg 8000
on the server; Tailscale then exposes https://<machine>.<tailnet>.ts.net/ with a
valid certificate, and no firewall rule is needed.

The server sends `Cache-Control: no-store` so a rebuild is visible on the viewer
without a hard refresh, and refuses to serve `_staging/` (raw video, model weights,
intermediate crops).
"""
import argparse
import http.server
import socketserver
import subprocess
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parents[2] / "texas-senate-2026"
BLOCKED_PREFIXES = ("/_staging/", "/_staging", "/.git")


class Handler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"   # keep-alive: a gallery page pulls ~67 images

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE_ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        super().end_headers()

    def do_GET(self):
        if self.path.startswith(BLOCKED_PREFIXES):
            self.send_error(403, "not served")
            return
        if self.path in ("/", ""):
            self.send_response(302)
            self.send_header("Location", "/site/index.html")
            self.end_headers()
            return
        return super().do_GET()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def tailscale_ip():
    try:
        out = subprocess.run(["tailscale", "ip", "-4"], capture_output=True, text=True, timeout=5)
        ip = out.stdout.strip().splitlines()[0] if out.stdout.strip() else ""
        return ip or None
    except Exception:
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--bind", default="127.0.0.1",
                    help="127.0.0.1 (default), 0.0.0.0, or a specific Tailscale IP")
    args = ap.parse_args(argv)

    if not (SITE_ROOT / "site" / "index.html").exists():
        print("ERROR: site/index.html not found — build it first:", file=sys.stderr)
        print("  python texas-senate-2026/_staging/_lead_build_site.py", file=sys.stderr)
        return 1

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer((args.bind, args.port), Handler) as httpd:
        print("serving %s" % SITE_ROOT)
        print("  local:      http://127.0.0.1:%d/site/index.html" % args.port)
        ts = tailscale_ip()
        if ts:
            print("  tailnet:    http://%s:%d/site/index.html" % (ts, args.port))
        if args.bind == "127.0.0.1":
            print("  (127.0.0.1 only — for remote access run: tailscale serve --bg %d)" % args.port)
        print("Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
