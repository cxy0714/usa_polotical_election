# -*- coding: utf-8 -*-
"""Fetch YouTube oEmbed metadata for candidate/outlet videos already referenced in mirrors."""
import csv
import json
import os
import urllib.parse
import urllib.request

STAGE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIR = os.path.join(STAGE, 'mirrors')
LOG = os.path.join(STAGE, 'fetch_log.csv')

IDS = ['7ZO5OMrnfXM', 'iR5HD6oCjz0', 'fkZkM7EH-VY', 'NH9_bZQ7AyA', 'B-dA-DYMJwQ', 'I41TFtz_ywA',
       'zDzoC0EtlVk', 'taKInZXZz5M', '8jN4-CMiv8I', 'lNXuCMcvV6Q', '0dsZMCqCphY', 'pDfm9RaIIv4',
       'Xwx8pne2Q5A', 'VeIZaNcwcok', 'UTPlKwkryEk', 'Lrum87XgwWA', 'CdQ31tLGfzQ', 'vOHCq3Ode5E']

UA = {'User-Agent': 'Mozilla/5.0 (research archive)'}
out = {}
for vid in IDS:
    url = 'https://www.youtube.com/oembed?format=json&url=' + urllib.parse.quote(
        'https://www.youtube.com/watch?v=' + vid, safe='')
    fn = 'oembed_' + vid + '.json'
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read()
            status = r.status
        open(os.path.join(MIR, fn), 'wb').write(body)
        j = json.loads(body.decode('utf-8'))
        out[vid] = j
        print(vid, status, j.get('author_name'), '|', j.get('title'))
    except Exception as e:
        status = 'error'
        print(vid, 'ERR', e)
    with open(LOG, 'a', encoding='utf-8', newline='') as f:
        csv.writer(f, lineterminator='\n').writerow(
            [url, status, len(body) if status != 'error' else 0, '2026-11-18T14:20:00+08:00',
             '_staging/mirrors/' + fn if status != 'error' else 'unknown'])

json.dump(out, open(os.path.join(STAGE, 'oembed.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
