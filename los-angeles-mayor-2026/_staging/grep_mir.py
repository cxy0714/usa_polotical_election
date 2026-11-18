import os, re, sys, html

MIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mirrors')
kws = sys.argv[1:]
for fn in sorted(os.listdir(MIR)):
    if not fn.endswith('.html'):
        continue
    raw = open(os.path.join(MIR, fn), 'rb').read().decode('utf-8', 'ignore')
    raw = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', raw)
    txt = re.sub(r'(?s)<[^>]+>', ' ', raw)
    txt = html.unescape(txt)
    txt = re.sub(r'(?s)<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = re.sub(r'\s+', ' ', txt)
    for kw in kws:
        for m in re.finditer(re.escape(kw), txt, re.I):
            s = max(0, m.start() - 160)
            print(f'--- {fn} [{kw}]')
            print('   ', txt[s:m.start() + 240].strip()[:400])
            break
