import csv, re, urllib.error, urllib.request
from datetime import datetime
import os

BASE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(BASE)
LOG = os.path.join(BASE, 'fetch_log.csv')
UA = 'Mozilla/5.0 (research archive)'

urls = [
    'https://www.nbcnews.com/politics/2026-general-elections/los-angeles-mayor-results',
    'https://www.cnn.com/election/2026/results/los-angeles-mayor',
    'https://www.nbcnews.com/politics/2026-elections/los-angeles-mayor-runoff-results',
]
with open(LOG, 'a', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    for u in urls:
        st, body = 'ERR', b''
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=15)
            st, body = r.status, r.read()
        except urllib.error.HTTPError as e:
            st = e.code
            body = e.read() if e.fp else b''
        except Exception as e:  # noqa
            st = type(e).__name__
        print(st, len(body), u)
        for k in [b'615,264', b'504,959', b'615264', b'504959', b'1,120,223']:
            print('   ', k, k in body)
        w.writerow([u, st, len(body), datetime.now().astimezone().isoformat(timespec='seconds'), 'unknown'])
