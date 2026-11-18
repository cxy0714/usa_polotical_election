import csv, os, re, html, json

BASE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(BASE)
LOG = os.path.join(BASE, 'fetch_log.csv')

files = {}
for row in csv.DictReader(open(LOG, encoding='utf-8')):
    files[row['url']] = row


def text_of(p):
    raw = open(p, 'rb').read().decode('utf-8', 'ignore')
    title = ''
    m = re.search(r'(?is)<title[^>]*>(.*?)</title>', raw)
    if m:
        title = html.unescape(re.sub(r'\s+', ' ', m.group(1))).strip()
    desc = ''
    for pat in [r'(?is)<meta[^>]+property="og:description"[^>]+content="([^"]*)"',
                r'(?is)<meta[^>]+name="description"[^>]+content="([^"]*)"',
                r'(?is)<meta[^>]+content="([^"]*)"[^>]+name="description"']:
        m = re.search(pat, raw)
        if m:
            desc = html.unescape(m.group(1)).strip()
            break
    body = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', raw)
    body = re.sub(r'(?is)<br\s*/?>', ' ', body)
    txt = re.sub(r'(?s)<[^>]+>', ' ', body)
    txt = html.unescape(txt)
    txt = re.sub(r'[ \t\xa0]+', ' ', txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    return title, desc, txt


out = []
for url, rec in files.items():
    sf = rec['saved_file']
    p = os.path.join(CASE, sf) if sf != 'unknown' else None
    if not p or not os.path.exists(p):
        out.append({'url': url, 'status': rec['http_status'], 'bytes': rec['bytes'],
                    'title': '', 'desc': '', 'body': ''})
        continue
    if p.endswith(('.pdf', '.wikitext')) or 'youtube' in url:
        out.append({'url': url, 'status': rec['http_status'], 'bytes': rec['bytes'],
                    'title': '(binary/non-html)', 'desc': '', 'body': ''})
        continue
    t, d, b = text_of(p)
    out.append({'url': url, 'status': rec['http_status'], 'bytes': rec['bytes'],
                'title': t, 'desc': d, 'body': b})

json.dump(out, open(os.path.join(BASE, 'mirror_report.json'), 'w'), indent=1)
print('rows', len(out))
