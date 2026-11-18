import json, urllib.parse, urllib.request

UA = 'Mozilla/5.0 (research archive)'
API = 'https://commons.wikimedia.org/w/api.php'


def api(params):
    params = dict(params, format='json')
    u = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(u, headers={'User-Agent': UA})
    r = urllib.request.urlopen(req, timeout=30)
    return json.loads(r.read().decode('utf-8'))


# 1. search for candidate portraits
for q in ['Nithya Raman', 'Karen Bass mayor', 'Spencer Pratt']:
    d = api({'action': 'query', 'list': 'search', 'srsearch': 'filetype:bitmap ' + q,
             'srnamespace': '6', 'srlimit': '12'})
    print('== search:', q)
    for s in d['query']['search']:
        print('   ', s['title'])
