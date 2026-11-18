import urllib.request, urllib.parse, re, sys

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'


def get(u):
    req = urllib.request.Request(u, headers={
        'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'en-US,en;q=0.9'})
    r = urllib.request.urlopen(req, timeout=25)
    return r.read().decode('utf-8', 'ignore')


q = sys.argv[1]
d = get('https://www.bing.com/search?q=' + urllib.parse.quote(q))
blocks = re.findall(r'<li class="b_algo".*?</li>', d, re.S)
print('blocks', len(blocks))
for b in blocks[:15]:
    m = re.search(r'<a[^>]+href="(https?://[^"]+)"', b)
    t = re.search(r'<h2[^>]*>(.*?)</h2>', b, re.S)
    print((m.group(1) if m else '?')[:120], '|', re.sub(r'<[^>]+>', '', t.group(1))[:90] if t else '')
