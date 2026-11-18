import urllib.request, re

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'


def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': UA, 'Accept': 'application/xml'})
    r = urllib.request.urlopen(req, timeout=40)
    return r.read().decode('utf-8', 'ignore')


urls = []
for sm in ['post-sitemap.xml', 'post-sitemap3.xml', 'post-sitemap4.xml']:
    try:
        d = get('https://calmatters.org/' + sm)
        urls.extend(re.findall(r'<loc>(.*?)</loc>', d))
    except Exception as e:
        print('ERR', sm, e)

hits = [u for u in urls if '/2026/' in u and re.search(r'(mayor|karen-bass|nithya|raman|los-angeles)', u, re.I)
        and 'en-espanol' not in u]
print('hits', len(hits))
for h in sorted(set(hits)):
    print(' ', h)
