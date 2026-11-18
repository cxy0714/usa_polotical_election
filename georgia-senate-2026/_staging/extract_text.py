"""Convert saved HTML mirrors to plain text for inspection.

Usage: python _staging/extract_text.py [pattern]
Writes <mirror>.txt beside each .html and prints a summary line.
"""
import glob, html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MIR = os.path.join(HERE, 'mirrors')
TAG = re.compile(r'<(script|style|noscript|svg)[^>]*>.*?</\1>', re.S | re.I)
DROP = re.compile(r'<[^>]+>')


def to_text(raw):
    t = TAG.sub(' ', raw)
    t = re.sub(r'<br\s*/?>', '\n', t, flags=re.I)
    t = re.sub(r'</(p|div|h[1-6]|li|tr)>', '\n', t, flags=re.I)
    t = DROP.sub(' ', t)
    t = html.unescape(t)
    t = re.sub(r'[ \t\u00a0]+', ' ', t)
    t = re.sub(r'\n\s*\n+', '\n', t)
    return t.strip()


def main(pat='*.html'):
    for p in sorted(glob.glob(os.path.join(MIR, pat))):
        raw = open(p, encoding='utf-8', errors='replace').read()
        txt = to_text(raw)
        out = p.rsplit('.', 1)[0] + '.txt'
        open(out, 'w', encoding='utf-8', newline='\n').write(txt)
        title = re.search(r'<title[^>]*>(.*?)</title>', raw, re.S | re.I)
        print('%-46s %7d chars  %s' % (os.path.basename(out), len(txt),
                                       (title.group(1).strip()[:90] if title else '(no title)')))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '*.html')
