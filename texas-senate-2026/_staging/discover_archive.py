"""Discover the archive node on the tailnet.

Walks `tailscale status --json` Peer entries, requests
http://<DNSName>/.well-known/archive.json (5 s timeout), and reports which node
advertises a name containing "Political Image Lab".
"""
import json
import subprocess
import sys
import urllib.error
import urllib.request

TIMEOUT = 5
PROBE_PATH = "/.well-known/archive.json"
NEEDLE = "political image lab"

# This laptop routes HTTP through a system proxy that cannot resolve tailnet names
# (it answers 502). Tailnet peers must be reached directly, so disable proxies.
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def tailscale_status():
    out = subprocess.run(["tailscale", "status", "--json"], capture_output=True, text=True, timeout=20)
    if out.returncode != 0:
        print("tailscale status failed:", out.stderr.strip(), file=sys.stderr)
        sys.exit(2)
    return json.loads(out.stdout)


def probe(host):
    url = "http://%s%s" % (host, PROBE_PATH)
    req = urllib.request.Request(url, headers={"User-Agent": "archive-discovery/1.0"})
    try:
        with OPENER.open(req, timeout=TIMEOUT) as r:
            body = r.read(65536).decode("utf-8", "replace")
            return {"url": url, "status": r.status, "body": body}
    except urllib.error.HTTPError as e:
        return {"url": url, "status": e.code, "body": e.read(2048).decode("utf-8", "replace") if e.fp else ""}
    except Exception as e:
        return {"url": url, "status": None, "error": "%s: %s" % (type(e).__name__, e)}


def main():
    st = tailscale_status()
    peers = st.get("Peer") or {}
    self_node = st.get("Self") or {}
    print("self: %s (%s)" % (self_node.get("DNSName", "?").rstrip("."), self_node.get("TailscaleIPs")))
    print("peers:", len(peers))

    rows, hit = [], None
    for key, p in peers.items():
        dns = (p.get("DNSName") or "").rstrip(".")
        if not dns:
            rows.append((p.get("HostName", key), "-", "no DNSName", ""))
            continue
        online = p.get("Online")
        res = probe(dns)
        name, entry = "", ""
        if res.get("status") == 200:
            try:
                doc = json.loads(res["body"])
                name = str(doc.get("name", ""))
                entry = str(doc.get("entry_url", ""))
            except json.JSONDecodeError:
                name = "(not json)"
        rows.append((p.get("HostName", key), dns, "online" if online else "offline",
                     res.get("status") or res.get("error", ""), name, entry))
        if name and NEEDLE in name.lower():
            hit = (p.get("HostName", key), dns, name, entry)

    print()
    print("%-22s %-42s %-8s %-28s %s" % ("host", "dnsname", "state", "probe", "advertised name"))
    for r in rows:
        host, dns, state, probe_res, name = r[0], r[1], r[2], str(r[3]), r[4] if len(r) > 4 else ""
        print("%-22s %-42s %-8s %-28s %s" % (host[:22], dns[:42], state[:8], probe_res[:28], name[:40]))

    print()
    if hit:
        host, dns, name, entry = hit
        print("MATCH:", host, name)
        print("entry_url:", entry or "(missing)")
        with open("texas-senate-2026/_staging/discovery_result.json", "w", encoding="utf-8") as fh:
            json.dump({"host": host, "dnsname": dns, "name": name, "entry_url": entry}, fh, ensure_ascii=False, indent=2)
    else:
        print("NO MATCH: no peer advertised a name containing 'Political Image Lab'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
