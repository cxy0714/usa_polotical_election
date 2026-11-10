"""Lead integration: merge agent source registries into 09_sources/sources.csv
and rewrite local source tokens (A-S01 / B-S12 / D-S30 / E-S009 ...) to global SRC-#### ids
across every deliverable.

Usage:
    python _lead_merge_sources.py            # build master + rewrite (agents A,B,C,D,E)
    python _lead_merge_sources.py --report   # only report current token health
"""
import csv
import glob
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
STAGING = os.path.join(ROOT, "_staging")
MASTER = os.path.join(ROOT, "09_sources", "sources.csv")
MAPFILE = os.path.join(STAGING, "_lead_source_map.json")
HEADER = ["source_id", "url", "title", "publisher", "publication_date", "event_date",
          "access_date", "source_tier", "source_type", "relevant_quote_or_info",
          "reliability_notes", "used_by"]
AGENT_ORDER = ["A", "B", "C", "D", "E"]


def norm_url(u):
    u = (u or "").strip()
    if not u or u == "unknown":
        return ""
    u = u.split("#")[0]
    m = re.match(r"^(https?)://([^/]+)(.*)$", u, re.I)
    if not m:
        return u.lower()
    scheme, host, path = m.group(1).lower(), m.group(2).lower(), m.group(3)
    if host.startswith("www."):
        host = host[4:]
    path = path.rstrip("/")
    return f"{scheme}://{host}{path}"


def good(v):
    return v not in (None, "", "unknown")


def load_registries():
    reg = {}
    for a in AGENT_ORDER:
        p = os.path.join(STAGING, f"{a}_sources.csv")
        if not os.path.exists(p):
            continue
        with open(p, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        reg[a] = rows
    return reg


def build():
    reg = load_registries()
    # group by normalized url; preserve agent order then original id order
    groups = {}
    order = []
    for a in AGENT_ORDER:
        for r in reg.get(a, []):
            key = norm_url(r.get("url"))
            if not key:
                key = f"nourl::{a}::{r.get('source_id')}"
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append((a, r))

    sources = []
    remap = {}
    for i, key in enumerate(order, start=1):
        sid = f"SRC-{i:04d}"
        members = groups[key]
        merged = {h: "" for h in HEADER}
        merged["source_id"] = sid
        for field in HEADER[1:]:
            for a, r in members:
                v = (r.get(field) or "").strip()
                if field == "used_by":
                    continue
                if good(v) and not good(merged[field]):
                    merged[field] = v
        merged["url"] = members[0][1].get("url", "").strip()
        used = sorted({a for a, _ in members})
        merged["used_by"] = ";".join(used)
        # note cross-registry duplicates in reliability notes
        if len(members) > 1:
            dup = ", ".join(r.get("source_id", "") for _, r in members)
            note = merged["reliability_notes"]
            extra = f"Retrieved independently by multiple streams ({dup})."
            merged["reliability_notes"] = (note + " " + extra).strip() if good(note) else extra
        for a, r in members:
            remap[r.get("source_id", "")] = sid
        sources.append(merged)

    os.makedirs(os.path.dirname(MASTER), exist_ok=True)
    with open(MASTER, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(sources)

    with open(MAPFILE, "w", encoding="utf-8") as f:
        json.dump(remap, f, indent=1, ensure_ascii=False)

    print(f"[sources.csv] {len(sources)} unique sources from "
          f"{sum(len(v) for v in reg.values())} registry rows "
          f"({len(remap)} local ids mapped)")
    return remap


TOKEN = re.compile(r"\b([A-E])-S(\d{1,3})\b")
EXT = {".csv", ".md"}


def rewrite(remap):
    changed = {}
    missing = {}
    for dirpath, _, files in os.walk(ROOT):
        if "_staging" in dirpath:
            continue
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in EXT:
                continue
            p = os.path.join(dirpath, fn)
            with open(p, encoding="utf-8-sig") as f:
                txt = f.read()
            hits = set(TOKEN.findall(txt))
            if not hits:
                continue
            def sub(m):
                tok = f"{m.group(1)}-S{m.group(2)}"
                if tok in remap:
                    return remap[tok]
                missing.setdefault(p, set()).add(tok)
                return tok
            new = TOKEN.sub(sub, txt)
            if new != txt:
                with open(p, "w", encoding="utf-8", newline="") as f:
                    f.write(new)
                n = sum(1 for _ in TOKEN.finditer(txt))
                changed[os.path.relpath(p, ROOT)] = n
    for p, n in sorted(changed.items()):
        print(f"[rewrite] {p}: {n} token(s)")
    if missing:
        print("\n[UNRESOLVED TOKENS]")
        for p, toks in missing.items():
            print(f"  {os.path.relpath(p, ROOT)}: {sorted(toks)[:12]}")
    return changed, missing


def report():
    toks = {}
    for dirpath, _, files in os.walk(ROOT):
        if "_staging" in dirpath:
            continue
        for fn in files:
            if os.path.splitext(fn)[1].lower() not in EXT:
                continue
            p = os.path.join(dirpath, fn)
            with open(p, encoding="utf-8-sig") as f:
                txt = f.read()
            for m in TOKEN.finditer(txt):
                toks.setdefault(os.path.relpath(p, ROOT), set()).add(m.group(0))
    if not toks:
        print("No local source tokens remain outside _staging.")
    for p, s in sorted(toks.items()):
        print(f"  {p}: {len(s)} distinct local tokens")


if __name__ == "__main__":
    if "--report" in sys.argv:
        report()
    else:
        remap = build()
        rewrite(remap)
