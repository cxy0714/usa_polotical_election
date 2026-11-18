import csv, json, os, urllib.parse, urllib.request
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(BASE)
MIR = os.path.join(BASE, 'mirrors')
LOG = os.path.join(BASE, 'fetch_log.csv')
UA = 'Mozilla/5.0 (research archive)'
API = 'https://commons.wikimedia.org/w/api.php'

FILES = [
    'File:Nithya Raman, 2022.jpg',
    'File:Karen Bass, 20232 (cropped).jpg',
    'File:Karen Bass, 2023.jpg',
    'File:Mayor Karen Bass official portrait.jpg',
    'File:Nithya Raman and Karen Bass 2023.jpg',
    'File:Nithya Raman on the Los Angeles City Council float 2023 (cropped).jpg',
    'File:Spencer Pratt at Sen Rick Scott Press Conference on Congressional Investigation into Palisades Wildfire (3x4 crop).jpg',
    'File:Spencer Pratt in November 2025.jpg',
]


def fetch_api(tag, titles):
    params = {
        'action': 'query', 'format': 'json', 'titles': titles,
        'prop': 'imageinfo',
        'iiprop': 'url|size|mime|extmetadata|user',
        'iiurlwidth': '1200',
    }
    u = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(u, headers={'User-Agent': UA})
    r = urllib.request.urlopen(req, timeout=40)
    body = r.read()
    path = os.path.join(MIR, 'commons_' + tag + '.json')
    open(path, 'wb').write(body)
    return u, r.status, len(body), path


rows = []
for i in range(0, len(FILES), 4):
    chunk = FILES[i:i + 4]
    tag = 'info%d' % (i // 4 + 1)
    u, st, n, path = fetch_api(tag, '|'.join(chunk))
    rows.append([u, st, n, datetime.now().astimezone().isoformat(timespec='seconds'),
                 os.path.relpath(path, CASE).replace('\\', '/')])
    print(st, n, tag)

with open(LOG, 'a', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    for r in rows:
        w.writerow(r)

# parse and dump a compact summary
out = {}
for i in range(1, (len(FILES) + 3) // 4 + 1):
    p = os.path.join(MIR, 'commons_info%d.json' % i)
    if not os.path.exists(p):
        continue
    d = json.load(open(p, encoding='utf-8'))
    for pid, page in d['query']['pages'].items():
        if 'imageinfo' not in page:
            print('MISSING', page.get('title'))
            continue
        ii = page['imageinfo'][0]
        em = ii.get('extmetadata', {})
        out[page['title']] = {
            'url': ii['url'],
            'thumburl': ii.get('thumburl'),
            'width': ii['width'], 'height': ii['height'],
            'bytes': ii['size'], 'mime': ii['mime'],
            'artist': em.get('Artist', {}).get('value', ''),
            'credit': em.get('Credit', {}).get('value', ''),
            'license': em.get('LicenseShortName', {}).get('value', ''),
            'licenseurl': em.get('LicenseUrl', {}).get('value', ''),
            'desc': em.get('ImageDescription', {}).get('value', ''),
            'date': em.get('DateTimeOriginal', {}).get('value', ''),
            'author': ii.get('user', ''),
            'descurl': ii.get('descriptionurl', ''),
        }

json.dump(out, open(os.path.join(BASE, 'commons_info.json'), 'w'), indent=1)
for k, v in out.items():
    print(k, '|', v['license'], '|', v['bytes'], v['width'], 'x', v['height'])
