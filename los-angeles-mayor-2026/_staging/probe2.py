import urllib.request, re, sys, urllib.parse

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'


def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': UA, 'Accept': 'text/html'})
    r = urllib.request.urlopen(req, timeout=25)
    return r.read().decode('utf-8', 'ignore')


print('=== calmatters search ===')
try:
    d = get('https://calmatters.org/?s=los+angeles+mayor')
    links = set(re.findall(r'href="(https://calmatters\.org/[^"#?]+)"', d))
    for l in sorted(links):
        if 'mayor' in l or 'los-angeles' in l:
            print(' ', l)
except Exception as e:
    print('ERR', e)

print('=== xtown ===')
for u in ['https://xtown.la/', 'https://xtown.la/?s=mayor']:
    try:
        d = get(u)
        print(u, len(d))
        for l in sorted(set(re.findall(r'href="([^"]+)"', d)))[:25]:
            print('   ', l[:120])
    except Exception as e:
        print('ERR', u, e)
