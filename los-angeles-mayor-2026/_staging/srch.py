import urllib.request, urllib.parse, re, sys

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'


def get(u):
    req = urllib.request.Request(u, headers={
        'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'en-US,en;q=0.9'})
    r = urllib.request.urlopen(req, timeout=25)
    return r.read().decode('utf-8', 'ignore')


q = sys.argv[1]
print('--- ddg lite body sample ---')
try:
    d = get('https://lite.duckduckgo.com/lite/?q=' + urllib.parse.quote(q))
    print(re.sub(r'<[^>]+>', ' ', d)[:600].strip())
except Exception as e:
    print('ERR ddg', e)
print('--- bing ---')
try:
    d = get('https://www.bing.com/search?q=' + urllib.parse.quote(q))
    print('len', len(d))
    links = re.findall(r'<h2><a href="(https?://[^"]+)"', d)
    for l in links[:20]:
        print('  ', l)
except Exception as e:
    print('ERR bing', e)
