import re, sys, html

p = sys.argv[1]
raw = open(p, 'rb').read().decode('utf-8', 'ignore')
raw = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', raw)
raw = re.sub(r'(?is)<br\s*/?>', '\n', raw)
raw = re.sub(r'(?is)</p>', '\n\n', raw)
txt = re.sub(r'(?s)<[^>]+>', ' ', raw)
txt = html.unescape(txt)
txt = re.sub(r'[ \t\xa0]+', ' ', txt)
txt = re.sub(r'\n\s*\n+', '\n\n', txt).strip()

if len(sys.argv) > 2:
    kw = sys.argv[2]
    before = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    after = int(sys.argv[4]) if len(sys.argv) > 4 else 3000
    i = txt.find(kw)
    if i < 0:
        print('NOT FOUND:', kw)
        print(txt[:1500])
    else:
        print(txt[max(0, i - before): i + after])
else:
    print(txt[:4000])
