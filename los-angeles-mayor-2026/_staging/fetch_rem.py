import csv, json, os, re, sys, time, urllib.error, urllib.request
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(BASE)
MIRRORS = os.path.join(BASE, 'mirrors')
LOG = os.path.join(BASE, 'fetch_log.csv')
UA = 'Mozilla/5.0 (research archive)'


def safe(tag, url):
    ext = '.html'
    low = url.lower()
    if low.endswith('.pdf'):
        ext = '.pdf'
    return re.sub(r'[^A-Za-z0-9_.-]', '_', tag)[:80] + ext


items = json.load(open(sys.argv[1], encoding='utf-8'))
timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 12

with open(LOG, 'a', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    for it in items:
        url, tag = it['url'], it.get('tag', 'x')
        out = os.path.join(MIRRORS, safe(tag, url))
        status, body = 'ERR', b''
        req = urllib.request.Request(url, headers={
            'User-Agent': UA,
            'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9'})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                status = r.status
                body = r.read()
        except urllib.error.HTTPError as e:
            status = e.code
            try:
                body = e.read()
            except Exception:
                body = b''
        except Exception as e:  # noqa: BLE001
            status = type(e).__name__
        if body:
            open(out, 'wb').write(body)
            saved = os.path.relpath(out, CASE).replace('\\', '/')
        else:
            saved = 'unknown'
        w.writerow([url, status, len(body),
                    datetime.now().astimezone().isoformat(timespec='seconds'), saved])
        f.flush()
        print(status, len(body), url[:100], flush=True)
        time.sleep(0.3)
