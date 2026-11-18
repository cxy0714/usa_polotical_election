import re, sys, html

p = sys.argv[1]
raw = open(p, 'rb').read().decode('utf-8', 'ignore')
# crude text extraction
raw = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', raw)
raw = re.sub(r'(?is)<br\s*/?>', '\n', raw)
raw = re.sub(r'(?is)</p>', '\n\n', raw)
txt = re.sub(r'(?s)<[^>]+>', ' ', raw)
txt = html.unescape(txt)
txt = re.sub(r'[ \t\xa0]+', ' ', txt)
txt = re.sub(r'\n\s*\n+', '\n\n', txt)
print(txt.strip()[:int(sys.argv[2]) if len(sys.argv) > 2 else 4000])
