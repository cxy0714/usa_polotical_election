"""Fetch a list of URLs, save mirrors, append _staging/fetch_log.csv.

Usage: python _staging/fetch.py urls.json
urls.json: [{"key": "short_name", "url": "https://..."}, ...]
"""
import csv, datetime, hashlib, json, os, re, sys, time, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MIRRORS = os.path.join(HERE, 'mirrors')
LOG = os.path.join(HERE, 'fetch_log.csv')
UA = 'Mozilla/5.0 (research archive)'
FIELDS = ['url', 'http_status', 'bytes', 'fetched_at', 'saved_file']


def safe(key, url):
    base = re.sub(r'[^A-Za-z0-9._-]+', '_', key)[:60]
    h = hashlib.sha1(url.encode()).hexdigest()[:8]
    return f'{base}_{h}'


def main(path):
    items = json.load(open(path, encoding='utf-8'))
    rows = []
    if os.path.exists(LOG):
        with open(LOG, encoding='utf-8', newline='') as f:
            rows = list(csv.DictReader(f))
    done = {r['url'] for r in rows}
    for it in items:
        url, key = it['url'], it.get('key', 'page')
        fn = safe(key, url)
        target = os.path.join(MIRRORS, fn + '.html')
        status, size, note = 'unknown', 0, ''
        if url in done and os.path.exists(target):
            print(f'SKIP {url}')
            continue
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': UA,
                'Accept': 'text/html,application/xhtml+xml,application/pdf,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read()
                status = resp.status
                ctype = resp.headers.get('Content-Type', '')
                if 'pdf' in ctype:
                    target = os.path.join(MIRRORS, fn + '.pdf')
                elif 'json' in ctype:
                    target = os.path.join(MIRRORS, fn + '.json')
                size = len(body)
                with open(target, 'wb') as f:
                    f.write(body)
        except urllib.error.HTTPError as e:
            status = e.code
            target = 'unknown'
            note = e.reason
            try:
                body = e.read()
                size = len(body)
            except Exception:
                pass
        except Exception as e:
            status = 'error'
            target = 'unknown'
            note = str(e)[:120]
        rel = os.path.relpath(target, os.path.dirname(HERE)).replace('\\', '/') if target != 'unknown' else 'unknown'
        rows.append(dict(url=url, http_status=str(status), bytes=str(size),
                         fetched_at=datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
                         saved_file=rel))
        print(f'{status}\t{size}\t{rel}\t{url}\t{note}')
        time.sleep(0.4)
    with open(LOG, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    print(f'logged {len(rows)} rows -> {LOG}')


if __name__ == '__main__':
    main(sys.argv[1])
