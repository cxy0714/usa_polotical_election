# -*- coding: utf-8 -*-
"""Check every registry URL against the fetch log and every quote against the mirror."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import CASE, SOURCES, load_log, mirror_text, norm, src_ids  # noqa: E402

log = load_log()
ids = src_ids()
bad_url, bad_quote, ok = [], [], 0
texts = {}
for url, pub, pdate, edate, tier, typ, quote, notes in SOURCES:
    sid = ids[url]
    if url not in log:
        bad_url.append((sid, url))
        continue
    if log[url]['http_status'] != '200':
        bad_url.append((sid, url + ' [status ' + log[url]['http_status'] + ']'))
        continue
    if url not in texts:
        texts[url] = mirror_text(url, log)
    t = texts[url]
    if t is None or t == '':
        sf = log[url]['saved_file']
        if sf.endswith('.wikitext'):
            t = open(os.path.join(CASE, sf), encoding='utf-8').read()
            texts[url] = t
        elif sf.endswith('.pdf'):
            # PDF: only the document title/filename can be checked from the saved bytes
            texts[url] = os.path.basename(sf).replace('_', ' ')
            t = texts[url]
        else:
            bad_quote.append((sid, url, 'no text (binary/non-html)'))
            continue
    if quote and quote != 'unknown' and norm(quote) not in norm(t):
        bad_quote.append((sid, url, quote[:100]))
        continue
    ok += 1

print(f'registry={len(SOURCES)} ok={ok} bad_url={len(bad_url)} bad_quote={len(bad_quote)}')
for x in bad_url:
    print('BADURL ', x[0], x[1])
for x in bad_quote:
    print('BADQUOTE', x[0], x[1][:100], '||', x[2])
