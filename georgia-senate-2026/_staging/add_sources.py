# -*- coding: utf-8 -*-
"""Append wiki/Commons sources and verify all source URLs are in the fetch log."""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(HERE)
SP = os.path.join(CASE, '09_sources', 'sources.csv')
rows = list(csv.DictReader(open(SP, encoding='utf-8')))
have = {r['source_id'] for r in rows}
ADD = [
 ('SRC-0096', 'https://en.wikipedia.org/wiki/Jon_Ossoff',
  'Jon Ossoff', 'Wikipedia', '2026-11-17', '2026-11-03', 'T3', 'encyclopedia',
  'Ossoff supports abortion rights; supports the John Lewis Voting Rights Act; voted to convict Trump in his second impeachment.',
  'Encyclopedia biography; used for background and positions, cross-checked against news where possible.'),
 ('SRC-0097', 'https://en.wikipedia.org/w/index.php?title=Mike_Collins_(politician)&action=raw',
  'Mike Collins (politician) - wikitext', 'Wikipedia', '2026-11-17', '2026-11-03', 'T3', 'encyclopedia',
  'Collins announced his Senate candidacy on July 27, 2025; described himself as "100 percent pro-life, period. No exceptions."',
  'Raw wikitext of the biography; used for career, positions and campaign chronology.'),
 ('SRC-0098', 'https://commons.wikimedia.org/wiki/File:U.S._Senate_Candidate_Mike_Collins_Concedes_U.S._Senate_Race_in_Georgia.jpg',
  'File:U.S. Senate Candidate Mike Collins Concedes U.S. Senate Race in Georgia.jpg', 'Wikimedia Commons', '2026-11-03', '2026-11-03', 'T1', 'photo',
  'C-SPAN frame of Collins conceding the Senate race on the evening of November 3, 2026.',
  'Commons file page; public domain (C-SPAN).'),
 ('SRC-0099', 'https://commons.wikimedia.org/wiki/File:2023_Peanut_Leadership_Academy_with_Jon_Ossoff_01.jpg',
  'File:2023 Peanut Leadership Academy with Jon Ossoff 01.jpg', 'Wikimedia Commons', '2023-02-01', '2023-02-01', 'T1', 'photo',
  'Ossoff with Georgia peanut growers at the 2023 Peanut Leadership Academy.',
  'Commons file page; CC BY 2.0, Georgia Peanut Commission.'),
]
for t in ADD:
    if t[0] in have:
        continue
    rows.append(dict(source_id=t[0], url=t[1], title=t[2], publisher=t[3], publication_date=t[4],
                     event_date=t[5], access_date='2026-11-18', source_tier=t[6], source_type=t[7],
                     relevant_quote_or_info=t[8], reliability_notes=t[9], used_by='pending'))

with open(SP, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n')
    w.writeheader()
    w.writerows(rows)

log = {x['url'].rstrip('/') for x in csv.DictReader(open(os.path.join(HERE, 'fetch_log.csv'), encoding='utf-8'))}
missing = [(r['source_id'], r['url']) for r in rows if r['url'].rstrip('/') not in log]
print('sources:', len(rows), 'missing from log:', len(missing))
for m in missing:
    print(' ', m)
