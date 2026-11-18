import csv, json, os, urllib.request
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(BASE)
LOG = os.path.join(BASE, 'fetch_log.csv')
UA = 'Mozilla/5.0 (research archive)'

info = json.load(open(os.path.join(BASE, 'commons_info.json'), encoding='utf-8'))

PLAN = [
    ('File:Nithya Raman, 2022.jpg', 'raman', 'raman_commons_2022.jpg'),
    ('File:Karen Bass, 20232 (cropped).jpg', 'bass', 'bass_commons_2023.jpg'),
    ('File:Spencer Pratt at Sen Rick Scott Press Conference on Congressional Investigation into Palisades Wildfire (3x4 crop).jpg', 'pratt', 'pratt_commons_2025.jpg'),
    ('File:Nithya Raman and Karen Bass 2023.jpg', 'raman', 'raman_bass_commons_2023.jpg'),
    ('File:Mayor Karen Bass official portrait.jpg', 'bass', 'bass_official_portrait.jpg'),
]

rows = []
for title, sub, fn in PLAN:
    rec = info[title]
    url = rec.get('thumburl') or rec['url']
    outdir = os.path.join(CASE, '04_visual_archive', sub)
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, fn)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
            st = r.status
        open(path, 'wb').write(body)
        rows.append([url, st, len(body), datetime.now().astimezone().isoformat(timespec='seconds'),
                     os.path.relpath(path, CASE).replace('\\', '/')])
        print(st, len(body), fn, rec['license'])
    except Exception as e:
        print('ERR', fn, e)

with open(LOG, 'a', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    for r in rows:
        w.writerow(r)
