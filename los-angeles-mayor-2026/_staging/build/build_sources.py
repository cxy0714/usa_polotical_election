# -*- coding: utf-8 -*-
"""Write 09_sources/sources.csv with derived titles and used_by."""
import csv
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import CASE, SOURCES, src_ids  # noqa: E402

REPORT = {r['url']: r for r in json.load(open(os.path.join(CASE, '_staging', 'mirror_report.json'),
                                               encoding='utf-8'))}
OEMBED = json.load(open(os.path.join(CASE, '_staging', 'oembed.json'), encoding='utf-8'))

MANUAL = {
    'https://en.wikipedia.org/w/index.php?title=2026_Los_Angeles_mayoral_election&action=raw':
        '2026 Los Angeles mayoral election (raw wikitext)',
    'https://cityclerk.lacity.org/election/2026_Nominating_Petition_Filing_Status.pdf':
        '2026 Nominating Petition Filing Status',
    'https://www.cygn.al/wp-content/uploads/2026/05/Cygnal-LA-Mayor-Poll-1.pdf':
        'Cygnal LA Mayor Poll',
    'https://www.youtube.com/watch?v=AkuJMniInXQ': 'SOHA May 2026 Mayoral Debate (full video)',
    'https://www.youtube.com/watch?v=8rI3A6alVHM': 'LA mayoral debate live: Watch Karen Bass, Spencer Pratt, Nithya Raman on NBCLA (full video)',
    'https://www.youtube.com/watch?v=fVzKUvSstY4&ra=m': 'SOHA August 2026 Mayoral Debate (full video)',
    'https://www.youtube.com/watch?v=mg8EOrjyMRk&pp=0gcJCY8Co7VqN5tD&ra=m': 'Full debate: Karen Bass vs. Nithya Raman for LA mayor',
    'https://www.youtube.com/watch?v=6I7yezAbueM': '2026 Los Angeles Mayoral Forum (Jewish Federation of Los Angeles, full video)',
    'https://apnews.com/projects/elections-2026/california-los-angeles-mayor-results/':
        'Los Angeles, CA Mayor Nonpartisan Runoff Election Live Results 2026',
}
STRIP = (' | Los Angeles Times', ' - Los Angeles Times', ' - ABC7 Los Angeles', ' – Daily News',
         ' | TheWrap', ' - CalMatters', ' | LAist', ' - CBS Los Angeles', ' | Our Weekly',
         ' | Deadline', ' | The Hollywood Reporter', ' | FOX 11 Los Angeles',
         ' | New York Post', ' | NBC Los Angeles', ' | NBC News', ' | Manhattan Institute',
         ' | Westside Current', ' | La Opinión', ' | Los Angeles Daily News',
         ' | American Federation of Musicians Local 47', ' | Emerson College Polling',
         ' | Crosstown (LA by the Numbers)', ' | NBCLA (YouTube)', ' | CNN',
         ' | Associated Press', ' | Sherman Oaks Homeowners Association (YouTube)',
         ' | Jewish Federation of Los Angeles (YouTube)', ' | California Post')


def title(url):
    if url in MANUAL:
        return MANUAL[url]
    t = (REPORT.get(url) or {}).get('title') or ''
    for s in STRIP:
        if t.endswith(s):
            t = t[:-len(s)]
    if not t:
        m = re.search(r'[?&]v=([A-Za-z0-9_-]{11})', url)
        if m and m.group(1) in OEMBED:
            o = OEMBED[m.group(1)]
            return o.get('title', 'unknown') + ' (video)'
    return t or 'unknown'


# used_by: scan every CSV that carries a source_urls column
used = {}
URL2SID = {s[0].rstrip('/'): 'SRC-%04d' % (i + 1) for i, s in enumerate(SOURCES)}
for p in glob.glob(os.path.join(CASE, '*', '*.csv')) + glob.glob(os.path.join(CASE, '*', '*', '*.csv')):
    rel = os.path.relpath(p, CASE).replace('\\', '/')
    if rel.startswith('09_sources'):
        continue
    rows = list(csv.DictReader(open(p, encoding='utf-8')))
    if not rows:
        continue
    name = rel.split('/')[-1].replace('.csv', '')
    for r in rows:
        for sid in re.findall(r'SRC-\d{4}', r.get('source_urls') or ''):
            used.setdefault(sid, set()).add(name)
        for col, val in r.items():
            if col in ('source_urls', 'url', 'video_url', 'source_url', 'speech_url'):
                u = (val or '').rstrip('/')
                if u in URL2SID:
                    used.setdefault(URL2SID[u], set()).add(name)

ids = src_ids()
header = ['source_id', 'url', 'title', 'publisher', 'publication_date', 'event_date',
          'access_date', 'source_tier', 'source_type', 'relevant_quote_or_info',
          'reliability_notes', 'used_by']
rows = []
for url, pub, pdate, edate, tier, typ, quote, notes in SOURCES:
    sid = ids[url]
    ub = '; '.join(sorted(used.get(sid, {'registry_only'})))
    rows.append([sid, url, title(url), pub, pdate, edate, '2026-11-18', tier, typ, quote, notes, ub])

mdset = set()
for mp in glob.glob(os.path.join(CASE, '**', '*.md'), recursive=True):
    mdset.update(re.findall(r'SRC-\d{4}', open(mp, encoding='utf-8').read()))
for r in rows:
    if r[11] == 'registry_only' and r[0] in mdset:
        r[11] = 'narrative_only'

path = os.path.join(CASE, '09_sources', 'sources.csv')
with open(path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(header)
    for r in rows:
        for c in r:
            assert str(c).strip() not in ('', 'TBD', 'TODO', 'N/A', 'NA', 'null', 'None', '-'), r
        w.writerow(r)

print('sources.csv', len(rows))
unused = [r[0] for r in rows if r[11] == 'registry_only']
print('unused sources:', unused)
print('unknown titles:', [r[0] for r in rows if r[2] == 'unknown'])
