import re
from pathlib import Path

SITE = Path("texas-senate-2026/site")
broken = {}
total = 0
for p in SITE.rglob("*.html"):
    html = p.read_text(encoding="utf-8")
    refs = re.findall(r'(?:src|href)="([^"]+)"', html)
    for r in refs:
        if r.startswith(("http", "mailto:", "#", "javascript:", "data:")):
            continue
        tgt = (p.parent / r.split("#")[0]).resolve()
        total += 1
        if not tgt.exists():
            broken.setdefault(str(p.relative_to(SITE)), []).append(r)
print("html pages:", len(list(SITE.rglob('*.html'))))
print("local refs checked:", total)
print("broken:", sum(len(v) for v in broken.values()))
for k, v in list(broken.items())[:15]:
    print(" ", k, "->", v[:5])
