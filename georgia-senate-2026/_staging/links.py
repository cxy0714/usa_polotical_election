"""List article links + anchor titles found in saved mirrors (for URL discovery)."""
import glob, html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MIR = os.path.join(HERE, 'mirrors')
A = re.compile(r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>', re.S | re.I)


def clean(s):
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def main(args):
    pat = args[0] if args else '*.html'
    host = args[1] if len(args) > 1 else ''
    seen = {}
    for p in glob.glob(os.path.join(MIR, pat)):
        raw = open(p, encoding='utf-8', errors='replace').read()
        for u, t in A.findall(raw):
            if host and host not in u:
                continue
            t = clean(t)
            if len(t) < 18:
                continue
            if u not in seen or len(t) > len(seen[u]):
                seen[u] = t
    out = args[2] if len(args) > 2 else ''
    lines = [u + '\t' + t[:120] for u, t in sorted(seen.items())]
    if out:
        with open(os.path.join(HERE, out), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines) + '\n')
    else:
        print('\n'.join(lines))


if __name__ == '__main__':
    main(sys.argv[1:])
