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
    cite = re.search(r'<cite[^>]*>(.*?)</cite>', b, re.S)
    href = re.search(r'<h2[^>]*>\s*<a[^>]+href="([^"]+)"', b, re.S)
    h = href.group(1) if href else ''
    u = re.search(r'&amp;u=a1([A-Za-z0-9%_\-]+)', h)
    real = ''
    if u:
        import base64
        try:
            s = u.group(1)
            s += '=' * (-len(s) % 4)
            real = base64.urlsafe_b64decode(s).decode('utf-8', 'ignore')
        except Exception:
            real = ''
    print('CITE:', re.sub(r'<[^>]+>', '', cite.group(1)).strip()[:80] if cite else '?', '| REAL:', real[:120])
