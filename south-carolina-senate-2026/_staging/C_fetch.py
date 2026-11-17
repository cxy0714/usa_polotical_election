"""Stream C (visual archive) fetch helper.

Shell network in this session works only through Python 3.14 + urllib.request with an
explicit User-Agent. Reuse this module; do not shell out to curl.

Usage:
    from C_fetch import get, get_json
"""
import urllib.request
import urllib.parse
import json

UA = "SC-Senate-Archive/1.0 (research)"


def get(url, timeout=40):
    """Return raw bytes for `url`."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout).read()


def get_json(url, timeout=40):
    """Return parsed JSON for `url`."""
    return json.loads(get(url, timeout=timeout).decode("utf-8"))


def api(params):
    """Build a Commons/Wikimedia API URL from a dict of params."""
    return "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)


if __name__ == "__main__":
    import sys
    print(len(get(sys.argv[1] if len(sys.argv) > 1
                  else "https://commons.wikimedia.org/w/api.php?action=query&format=json&meta=siteinfo")))
