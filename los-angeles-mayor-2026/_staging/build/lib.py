# -*- coding: utf-8 -*-
"""Shared helpers for building the Los Angeles case archive."""
import csv
import html
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.dirname(BASE)
CASE = os.path.dirname(STAGE)
sys.path.insert(0, BASE)

from sources_data import SOURCES  # noqa: E402


def norm(s):
    s = html.unescape(s or '')
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    s = s.replace('\u2014', '-').replace('\u2013', '-').replace('\u00a0', ' ')
    s = s.lower()
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def load_log():
    rows = list(csv.DictReader(open(os.path.join(STAGE, 'fetch_log.csv'), encoding='utf-8')))
    return {r['url']: r for r in rows}


def mirror_text(url, log=None):
    log = log or load_log()
    rec = log.get(url)
    if not rec or rec['saved_file'] == 'unknown':
        return None
    p = os.path.join(CASE, rec['saved_file'])
    if not os.path.exists(p) or p.endswith(('.pdf', '.wikitext')):
        return ''
    raw = open(p, 'rb').read().decode('utf-8', 'ignore')
    raw = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', raw)
    t = re.sub(r'(?s)<[^>]+>', ' ', raw)
    t = html.unescape(t)
    t = re.sub(r'(?s)<[^>]+>', ' ', t)
    t = html.unescape(t)
    return re.sub(r'\s+', ' ', t)


def src_ids():
    """SRC-0001 ... in registry order."""
    return {s[0]: 'SRC-%04d' % (i + 1) for i, s in enumerate(SOURCES)}


def cell(*parts):
    """Build a source_urls cell: SRC-####|https://..."""
    ids = src_ids()
    sid = ids[parts[0]]
    return sid + '|' + parts[0]


def write_csv(rel, header, rows):
    path = os.path.join(CASE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(header)
        for r in rows:
            assert len(r) == len(header), (rel, len(r), len(header), r[:2])
            for c in r:
                s = str(c)
                assert s.strip() not in ('', 'TBD', 'TODO', 'N/A', 'NA', 'null', 'None', '-'), (rel, s)
            w.writerow([str(c) for c in r])
    print(f'{rel}: {len(rows)} rows')
