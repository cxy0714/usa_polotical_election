import json, re, os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mirrors', 'wiki_georgia.wikitext')
t = open(p, encoding='utf-8').read()

# split into ref blocks
refs = re.findall(r'<ref[^>]*>(.*?)</ref>', t, re.S)
out = []
seen = set()
for r in refs:
    m = re.search(r'url\s*=\s*(https?://[^\s|}]+)', r)
    if not m:
        continue
    url = m.group(1).strip().rstrip('.,;')
    title = re.search(r'title\s*=\s*([^|]+)', r)
    work = re.search(r'(?:work|website|publisher|newspaper)\s*=\s*([^|]+)', r)
    date = re.search(r'\|\s*date\s*=\s*([^|]+)', r)
    acc = re.search(r'access-date\s*=\s*([^|]+)', r)
    if url in seen:
        continue
    seen.add(url)
    def clean(x):
        if not x: return 'unknown'
        s = x.group(1)
        s = re.sub(r'\[\[([^\]|]*\|)?([^\]]*)\]\]', r'\2', s)
        s = s.replace("{{'}}", "'").replace('{{!}}', '|')
        s = re.sub(r"'''?", '', s)
        s = re.sub(r'\s+', ' ', s).strip(" |'")
        return s or 'unknown'
    out.append(dict(url=url, title=clean(title), work=clean(work), date=clean(date), access=clean(acc)))

json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'refs.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'unique refs')
from collections import Counter
hosts = Counter(re.sub(r'^https?://(www\.)?', '', o['url']).split('/')[0] for o in out)
print(hosts.most_common(30))
