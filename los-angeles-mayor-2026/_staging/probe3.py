import urllib.request, re, sys

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'


def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': UA, 'Accept': 'text/html,application/xml'})
    r = urllib.request.urlopen(req, timeout=30)
    return r.read().decode('utf-8', 'ignore'), r.status


for u in ['https://calmatters.org/sitemap_index.xml', 'https://calmatters.org/sitemap.xml',
          'https://calmatters.org/robots.txt']:
    try:
        d, s = get(u)
        print('==', u, s, len(d))
        print(d[:800])
    except Exception as e:
        print('ERR', u, e)
