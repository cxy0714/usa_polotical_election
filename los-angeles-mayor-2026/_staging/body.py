import re, sys, html, json

p = sys.argv[1]
before = int(sys.argv[2]) if len(sys.argv) > 2 else 100
after = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
raw = open(p, 'rb').read().decode('utf-8', 'ignore')

headline = ''
for m in re.finditer(r'(?is)<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', raw):
    try:
        d = json.loads(m.group(1).strip())
    except Exception:
        continue
    stack = [d]
    while stack:
        o = stack.pop()
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'headline' and isinstance(v, str) and len(v) > 15:
                    headline = v
                elif isinstance(v, (dict, list)):
                    stack.append(v)
        elif isinstance(o, list):
            stack.extend(o)
    if headline:
        break

body = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', raw)
body = re.sub(r'(?is)<br\s*/?>', ' ', body)
body = re.sub(r'(?is)</(p|div|h[1-6]|li)>', '\n', body)
txt = re.sub(r'(?s)<[^>]+>', ' ', body)
txt = html.unescape(txt)
txt = re.sub(r'(?s)<[^>]+>', ' ', txt)
txt = html.unescape(txt)
txt = re.sub(r'[ \t\xa0]+', ' ', txt)
txt = re.sub(r'\n\s*\n+', '\n', txt).strip()

needle = None
if headline:
    for cand in [headline, headline.replace('’', "'"), re.sub(r'[^\w ]', '', headline)[:40]]:
        if cand and cand in txt:
            needle = cand
            break
if needle:
    i = txt.find(needle)
    print(txt[max(0, i - before): i + after])
else:
    print('[no headline match]', headline)
    print(txt[:after])
