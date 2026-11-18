# -*- coding: utf-8 -*-
"""Final self-checks beyond the validator."""
import csv
import glob
import json
import os
import re

CASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

src = {r['source_id']: r for r in csv.DictReader(open(os.path.join(CASE, '09_sources/sources.csv'), encoding='utf-8'))}
log = {r['url']: r for r in csv.DictReader(open(os.path.join(CASE, '_staging/fetch_log.csv'), encoding='utf-8'))}

print('== sources')
bad = [s for s, r in src.items() if r['url'] not in log or log[r['url']]['http_status'] != '200']
print('sources not logged 200:', bad)
print('tiers:', {t: sum(1 for r in src.values() if r['source_tier'] == t) for t in ('T1', 'T2', 'T3')})
print('access dates:', {r['access_date'] for r in src.values()})

print('== md citations')
missing = set()
for p in glob.glob(os.path.join(CASE, '**', '*.md'), recursive=True):
    for sid in re.findall(r'SRC-\d{4}', open(p, encoding='utf-8').read()):
        if sid not in src:
            missing.add((os.path.basename(p), sid))
print('unresolved md citations:', sorted(missing))

print('== html in md')
html = []
for p in glob.glob(os.path.join(CASE, '**', '*.md'), recursive=True):
    t = open(p, encoding='utf-8').read()
    if re.search(r'<(div|span|br|p|table|img|a)\b', t):
        html.append(os.path.basename(p))
print('files with html tags:', html)

print('== README table vs election_results')
res = list(csv.DictReader(open(os.path.join(CASE, '07_electoral_context/election_results.csv'), encoding='utf-8')))
readme = open(os.path.join(CASE, 'README.md'), encoding='utf-8').read()
miss = []
for r in res:
    row = f"| {r['candidate']} | {r['votes']} | {r['percentage']}% |"
    if row not in readme:
        miss.append(row)
print('rows missing from README:', miss)

print('== per-candidate counts')
ev = list(csv.DictReader(open(os.path.join(CASE, '02_campaign_events/campaign_events.csv'), encoding='utf-8')))
print('events:', {c: sum(1 for r in ev if r['candidate_id'] == c) for c in ('BASS', 'RAMAN')})
pol = list(csv.DictReader(open(os.path.join(CASE, '01_candidates/policy_positions.csv'), encoding='utf-8')))
print('policy:', {c: sum(1 for r in pol if r['candidate_id'] == c) for c in ('BASS', 'RAMAN')})
sp = list(csv.DictReader(open(os.path.join(CASE, '03_speeches/speech_archive.csv'), encoding='utf-8')))
print('speeches:', {c: sum(1 for r in sp if r['candidate_id'] == c) for c in ('BASS', 'RAMAN')})
co = list(csv.DictReader(open(os.path.join(CASE, '05_campaign_media/media_coverage.csv'), encoding='utf-8')))
print('coverage outlets:', sorted({r['outlet'] for r in co}))

print('== images downloaded')
for r in csv.DictReader(open(os.path.join(CASE, '04_visual_archive/image_archive.csv'), encoding='utf-8')):
    if r['local_filename'] != 'unknown':
        p = os.path.join(CASE, '04_visual_archive', r['local_filename'])
        print(' ', r['image_id'], r['license'], os.path.getsize(p), r['local_filename'])

print('== unique ids')
for f, key in [('02_campaign_events/campaign_events.csv', 'event_id'),
               ('03_speeches/speech_archive.csv', 'speech_id'),
               ('01_candidates/policy_positions.csv', 'position_id')]:
    ids = [r[key] for r in csv.DictReader(open(os.path.join(CASE, f), encoding='utf-8'))]
    print(f, len(ids), len(set(ids)))
