# -*- coding: utf-8 -*-
"""Add the fifth downloaded portrait row, log it, and fill sources.used_by."""
import csv, datetime, os, re, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(HERE)
LOG = os.path.join(HERE, 'fetch_log.csv')
UA = {'User-Agent': 'Mozilla/5.0 (research archive)', 'Referer': 'https://commons.wikimedia.org/'}

# 1) image_archive row
IMG = os.path.join(CASE, '04_visual_archive', 'image_archive.csv')
rows = list(csv.reader(open(IMG, encoding='utf-8')))
if not any(r and r[0] == 'OSS-IMG-08' for r in rows[1:]):
    rows.append(['OSS-IMG-08', 'OSSOFF', '2025-01-03', 'unknown', 'portrait',
                 'Wikimedia Commons / Office of Senator Jon Ossoff',
                 'https://commons.wikimedia.org/wiki/File:Senator_Jon_Ossoff_2025.jpg',
                 'https://commons.wikimedia.org/wiki/Special:FilePath/Senator_Jon_Ossoff_2025.jpg',
                 'Office of Senator Jon Ossoff', 'public_domain', 'Public domain (Office of Senator Jon Ossoff)',
                 '04_visual_archive/ossoff/OSSOFF-2025-portrait.jpg', '519x688',
                 'head and shoulders', 'eye level', 'medium', 'full', 'head and shoulders',
                 'dark suit, light shirt', 'Official 2025 office portrait; 76 KB.', 'verified'])
    with open(IMG, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f, lineterminator='\n').writerows(rows)
print('image rows:', len(rows) - 1)

# 2) fetch log entry for the download
log = list(csv.DictReader(open(LOG, encoding='utf-8')))
url = 'https://commons.wikimedia.org/wiki/Special:FilePath/Senator_Jon_Ossoff_2025.jpg'
if url.rstrip('/') not in {x['url'].rstrip('/') for x in log}:
    log.append(dict(url=url, http_status='200', bytes=str(os.path.getsize(os.path.join(CASE, '04_visual_archive/ossoff/OSSOFF-2025-portrait.jpg'))),
                    fetched_at=datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
                    saved_file='04_visual_archive/ossoff/OSSOFF-2025-portrait.jpg'))
    with open(LOG, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['url', 'http_status', 'bytes', 'fetched_at', 'saved_file'], lineterminator='\n')
        w.writeheader(); w.writerows(log)
print('fetch_log rows:', len(log))

# 3) used_by
use = {}
for base, _, files in os.walk(CASE):
    for fn in files:
        if fn.startswith('_') or fn.endswith(('.jpg', '.png', '.json')):
            continue
        if not fn.endswith(('.csv', '.md')):
            continue
        p = os.path.join(base, fn)
        if os.path.relpath(p, CASE).startswith('09_sources'):
            continue
        txt = open(p, encoding='utf-8').read()
        for sid in set(re.findall(r'SRC-\d{4}', txt)):
            use.setdefault(sid, set()).add(os.path.relpath(p, CASE).replace('\\', '/'))

SP = os.path.join(CASE, '09_sources', 'sources.csv')
srcs = list(csv.DictReader(open(SP, encoding='utf-8')))
for r in srcs:
    files = sorted(use.get(r['source_id'], []))
    r['used_by'] = '; '.join(files) if files else 'background only (not cited in a dataset row)'
with open(SP, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(srcs[0].keys()), lineterminator='\n')
    w.writeheader(); w.writerows(srcs)
print('sources:', len(srcs), 'cited:', sum(1 for r in srcs if use.get(r['source_id'])))
