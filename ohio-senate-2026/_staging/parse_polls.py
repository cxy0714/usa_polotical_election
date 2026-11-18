"""Parse the article's individual-poll table into a CSV for inspection."""
import csv
import re

t = open("_staging/mirrors/wiki_ohio.wikitext", encoding="utf-8").read()
lines = t.split("\n")
start = next(i for i, l in enumerate(lines) if "Poll source" in l)
chunk = "\n".join(lines[start:start + 700])
end = chunk.find("\n|}")
chunk = chunk[:end]

MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August",
     "September", "October", "November", "December"], 1)}


def clean(s):
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"\{\{party shading/[^}]+\}\}", "", s)
    s = re.sub(r"\{\{efn\|.*?\}\}", "", s, flags=re.S)
    s = re.sub(r"\{\{[Ss]dash\}\}", "—", s)
    s = re.sub(r"\{\{nbsp\}\}", " ", s)
    s = re.sub(r"'''?", "", s)
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"\[\[([^|\]]*\|)?([^\]]+)\]\]", r"\2", s)
    return s.strip()


def iso_range(txt):
    txt = txt.replace("–", "-").replace("—", "-").strip()
    nums = re.findall(r"([A-Z][a-z]+)\s+(\d{1,2})(?:\s*-\s*(?:([A-Z][a-z]+)\s+)?(\d{1,2}))?,?\s*(\d{4})?", txt)
    if not nums:
        return None, None
    m1, d1, m2, d2, y = nums[0]
    year = int(y) if y else 2026
    a = f"{year:04d}-{MONTHS.get(m1, 1):02d}-{int(d1):02d}"
    if d2:
        b = f"{year:04d}-{MONTHS.get(m2 or m1, MONTHS.get(m1, 1)):02d}-{int(d2):02d}"
    else:
        b = a
    return a, b


rows = []
for block in chunk.split("\n|-")[2:]:
    block = block.strip()
    if not block or block.startswith("|}"):
        continue
    cells = [clean(c) for c in re.split(r"\n\|", block)]
    cells = [c.lstrip("|").strip() for c in cells]
    if not cells:
        continue
    src = cells[0]
    if not src or "colspan" in src:
        continue
    if len(cells) < 6:
        continue
    dates = cells[1]
    sample = cells[2]
    moe = cells[3]
    rest = cells[4:]
    nums = [re.sub(r"[%±]", "", c).strip() for c in rest]
    rows.append([src, dates, sample, moe] + nums)

with open("_staging/polls_raw.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["source", "dates", "sample", "moe", "c1", "c2", "c3", "c4"])
    w.writerows(rows)
for r in rows:
    print(" | ".join(x[:34] for x in r))
