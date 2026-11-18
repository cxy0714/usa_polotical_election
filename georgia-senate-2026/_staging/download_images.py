# -*- coding: utf-8 -*-
"""Download licensed Commons portraits (<2 MB) into 04_visual_archive and log them."""
import csv, datetime, os, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(HERE)
UA = 'Mozilla/5.0 (research archive)'
LOG = os.path.join(HERE, 'fetch_log.csv')

IMGS = [
    # (local name, candidate dir, Commons file title, width, licence, photographer, file_page, image_date, description)
    ('OSSOFF-portrait-2021.jpg', 'ossoff', 'Jon Ossoff Senate Portrait 2021 (cropped).jpg', 1400,
     'Public domain (U.S. Senate)', 'U.S. Senate Photographic Studio',
     'https://commons.wikimedia.org/wiki/File:Jon_Ossoff_Senate_Portrait_2021_(cropped).jpg', '2021-04-22',
     'Official Senate portrait, seated, plain background'),
    ('OSSOFF-2025-portrait.jpg', 'ossoff', 'Senator Jon Ossoff 2025.jpg', 519,
     'Public domain (Office of Senator Jon Ossoff)', 'Office of Senator Jon Ossoff',
     'https://commons.wikimedia.org/wiki/File:Senator_Jon_Ossoff_2025.jpg', '2025-01-03',
     'Official 2025 portrait from the Senate office'),
    ('COLLINS-portrait-2023.jpg', 'collins', 'Rep. Mike Collins official photo, 118th Congress.jpg', 1200,
     'Public domain (U.S. Congress)', 'United States Congress',
     'https://commons.wikimedia.org/wiki/File:Rep._Mike_Collins_official_photo,_118th_Congress.jpg', '2023-01-03',
     'Official House portrait, suit and tie, neutral background'),
    ('COLLINS-concede-2026.jpg', 'collins', 'U.S. Senate Candidate Mike Collins Concedes U.S. Senate Race in Georgia.jpg', 1280,
     'Public domain (C-SPAN)', 'C-SPAN',
     'https://commons.wikimedia.org/wiki/File:U.S._Senate_Candidate_Mike_Collins_Concedes_U.S._Senate_Race_in_Georgia.jpg', '2026-11-03',
     'Concession speech to supporters, evening of Nov 3, 2026'),
    ('OSSOFF-peanut-academy-2023.jpg', None, '2023 Peanut Leadership Academy with Jon Ossoff 01.jpg', 1600,
     'CC BY 2.0', 'Georgia Peanut Commission',
     'https://commons.wikimedia.org/wiki/File:2023_Peanut_Leadership_Academy_with_Jon_Ossoff_01.jpg', '2023-02-01',
     'Ossoff with Georgia peanut growers (agriculture constituency image)'),
]

rows = list(csv.DictReader(open(LOG, encoding='utf-8')))
have = {r['url'].rstrip('/') for r in rows}


def url_for(title, width):
    base = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(title.replace(' ', '_'))
    return base + ('?width=%d' % width if width else '')


for name, cand, title, width, lic, photo, page, date, desc in IMGS:
    sub = os.path.join(CASE, '04_visual_archive', cand) if cand else os.path.join(CASE, '04_visual_archive')
    os.makedirs(sub, exist_ok=True)
    dest = os.path.join(sub, name)
    url = url_for(title, width)
    if not os.path.exists(dest):
        import time
        body, status = b'', 'error'
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': 'https://commons.wikimedia.org/'})
                with urllib.request.urlopen(req, timeout=60) as r:
                    body = r.read()
                    status = r.status
                break
            except Exception as e:
                print('retry', attempt, name, str(e)[:80])
                time.sleep(20 + 15 * attempt)
        if not body:
            print('FAILED', name)
            continue
        open(dest, 'wb').write(body)
    else:
        body = open(dest, 'rb').read()
        status = 200
    rel = os.path.relpath(dest, CASE).replace('\\', '/')
    print('%-34s %7d bytes  %s  %s' % (name, len(body), status, lic))
    if url.rstrip('/') not in have:
        rows.append(dict(url=url, http_status=str(status), bytes=str(len(body)),
                         fetched_at=datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
                         saved_file=rel))
        have.add(url.rstrip('/'))
    import time
    time.sleep(6)

with open(LOG, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['url', 'http_status', 'bytes', 'fetched_at', 'saved_file'], lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
print('logged', len(rows))
