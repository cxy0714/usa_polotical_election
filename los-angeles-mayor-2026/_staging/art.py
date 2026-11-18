import re, sys, html, json

p = sys.argv[1]
raw = open(p, 'rb').read().decode('utf-8', 'ignore')

# 1. JSON-LD article body
bodies = []
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
                if k in ('articleBody', 'description', 'headline', 'name') and isinstance(v, str):
                    bodies.append((k, v))
                elif isinstance(v, (dict, list)):
                    stack.append(v)
        elif isinstance(o, list):
            stack.extend(o)

if bodies:
    for k, v in bodies:
        v = re.sub(r'<[^>]+>', ' ', v)
        v = html.unescape(re.sub(r'\s+', ' ', v)).strip()
        print(f'[{k}] {v[:3000]}')
    sys.exit(0)

# 2. fallback: text between headline and end
raw2 = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', raw)
txt = re.sub(r'(?s)<[^>]+>', ' ', raw2)
txt = html.unescape(txt)
txt = re.sub(r'[ \t\xa0]+', ' ', txt)
txt = re.sub(r'\s+', ' ', txt).strip()
print(txt[:3000])
