"""Print only substantive paragraphs (long lines) from an extracted mirror text file."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
p = sys.argv[1]
if not os.path.isabs(p):
    p = os.path.join(HERE, 'mirrors', p)
minlen = int(sys.argv[2]) if len(sys.argv) > 2 else 140
for i, line in enumerate(open(p, encoding='utf-8', errors='replace'), 1):
    s = line.strip()
    if len(s) >= minlen:
        print(f'{i}: {s}')
