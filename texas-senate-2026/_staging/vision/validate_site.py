import re
from pathlib import Path

SITE = Path("texas-senate-2026/site")
pages = ["video/index.html", "video/frames.html", "video/data.html", "video/method.html", "index.html"]
bad = []
for rel in pages:
    p = SITE / rel
    if not p.exists():
        bad.append((rel, "MISSING PAGE"))
        continue
    html = p.read_text(encoding="utf-8")
    refs = re.findall(r'(?:src|href)="([^"]+)"', html)
    local = [r for r in refs if not r.startswith(("http", "mailto:", "#", "javascript:"))]
    for r in local:
        tgt = (p.parent / r.split("#")[0]).resolve()
        if not tgt.exists():
            bad.append((rel, r))
    print(f"{rel}: {len(html)} bytes, {len(local)} local refs")
print("\nBROKEN:", len(bad))
for b in bad[:40]:
    print("  ", b)

# quick content checks
idx = (SITE / "video/index.html").read_text(encoding="utf-8")
for probe in ["视频帧集", "47", "11", "Contact sheets", "方法"]:
    print(f"video/index contains {probe!r}:", probe in idx)
fr = (SITE / "video/frames.html").read_text(encoding="utf-8")
print("frame figures in gallery:", fr.count("<figure>"))
print("nav entries on video page:", len(re.findall(r'class="on"', fr)))
