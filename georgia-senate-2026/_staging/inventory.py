import csv, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
MIR = os.path.join(HERE, 'mirrors')
rows = list(csv.DictReader(open(os.path.join(HERE, 'fetch_log.csv'), encoding='utf-8')))
seen = set()
for r in rows:
    u = r['url']
    if u in seen:
        continue
    seen.add(u)
    f = r['saved_file']
    title = ''
    if f.endswith('.html') and os.path.exists(os.path.join(os.path.dirname(HERE), f)):
        raw = open(os.path.join(os.path.dirname(HERE), f), encoding='utf-8', errors='replace').read()
        m = re.search(r'<title[^>]*>(.*?)</title>', raw, re.S | re.I)
        if m:
            title = re.sub(r'\s+', ' ', m.group(1)).strip()[:110]
    print('%s\t%s\t%s\t%s' % (r['http_status'], os.path.basename(f)[:38], title, u[:95]))
