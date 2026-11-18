import urllib.request, urllib.parse, re, sys

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'


def get(u, data=None):
    req = urllib.request.Request(u, data=data, headers={
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'en-US,en;q=0.9',
    })
    r = urllib.request.urlopen(req, timeout=25)
    return r.read().decode('utf-8', 'ignore')


q = sys.argv[1]
d = get('https://lite.duckduckgo.com/lite/?q=' + urllib.parse.quote(q))
print('len', len(d))
links = re.findall(r'href="(https?://[^"]+)"', d)
seen = []
for l in links:
    if 'duckduckgo' in l:
        continue
    if l in seen:
        continue
    seen.append(l)
for l in seen[:25]:
    print(l)
