import urllib.request, urllib.parse, re, sys

UA = 'Mozilla/5.0 (research archive)'


def get(u):
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=25)
    return r.read().decode('utf-8', 'ignore')


qs = sys.argv[1:]
for q in qs:
    try:
        d = get('https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q))
        links = re.findall(r'class="result__a"[^>]*href="([^"]+)"', d)
        print('Q:', q, '->', len(links))
        for l in links[:15]:
            if 'uddg=' in l:
                m = re.search(r'uddg=([^&]+)', l)
                if m:
                    l = urllib.parse.unquote(m.group(1))
            print('   ', l)
    except Exception as e:
        print('ERR', q, e)
