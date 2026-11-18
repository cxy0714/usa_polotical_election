# -*- coding: utf-8 -*-
"""Repair source URLs against the fetch log, dedupe the log, and report."""
import csv, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(HERE)
LOG = os.path.join(HERE, 'fetch_log.csv')

rows = list(csv.DictReader(open(LOG, encoding='utf-8')))
# dedupe by url, keep first
seen = set()
uniq = []
for r in rows:
    u = r['url'].rstrip('/')
    if u in seen:
        continue
    seen.add(u)
    uniq.append(r)
with open(LOG, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['url', 'http_status', 'bytes', 'fetched_at', 'saved_file'], lineterminator='\n')
    w.writeheader()
    w.writerows(uniq)
print('fetch_log rows:', len(rows), '->', len(uniq))

log = {r['url'].rstrip('/'): r for r in uniq}


def find(sub):
    hits = [u for u in log if sub in u]
    return hits


SP = os.path.join(CASE, '09_sources', 'sources.csv')
src = list(csv.DictReader(open(SP, encoding='utf-8')))
fixes = {
    'SRC-0043': 'foxnews.com/politics/trump-backs-maga-champion',
    'SRC-0047': 'cbsnews.com/atlanta/news/gov-brian-kemp-endorses-collins',
    'SRC-0079': 'aarp.org/content/dam/aarp',
}
for rec in src:
    sid = rec['source_id']
    if sid in fixes:
        hits = find(fixes[sid])
        if hits:
            rec['url'] = hits[0]
            print(sid, '->', hits[0])
        else:
            print('NO HIT for', sid, fixes[sid])
    if sid == 'SRC-0083':
        rec['url'] = 'https://www.nbcnews.com/politics/2026-elections/midterms'
        rec['title'] = 'Midterm Elections 2026: Congress Polls, Charts and More'
        rec['publisher'] = 'NBC News'
        rec['publication_date'] = '2026-11-03'
        rec['event_date'] = '2026-11-03'
        rec['relevant_quote_or_info'] = 'NBC News 2026 midterms hub page with the battle-for-control section.'
        rec['reliability_notes'] = 'Hub page; used only for context, no candidate-specific fact.'
        print('SRC-0083 replaced with NBC midterms hub')

with open(SP, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(src[0].keys()), lineterminator='\n')
    w.writeheader()
    w.writerows(src)

missing = [x['source_id'] for x in src if x['url'].rstrip('/') not in log]
print('still missing:', missing)
