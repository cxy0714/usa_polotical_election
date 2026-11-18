"""Shared helpers for the ohio-senate-2026 builders."""
import csv
import os

SRC = {}
for r in csv.DictReader(open("_staging/srclist.csv", encoding="utf-8")):
    SRC[r["key"]] = (r["src_id"], r["url"])

ACCESS = "2026-11-18"


def _resolve(k):
    if k in SRC:
        return k
    cands = [s for s in SRC if s.startswith(k)]
    if len(cands) == 1:
        return cands[0]
    cands = [s for s in SRC if k in s]
    if len(cands) == 1:
        return cands[0]
    raise KeyError("unknown/ambiguous source key: " + k)


def ref(*keys):
    """Return 'SRC-####|url' for the FIRST key.

    The contract's source_urls cell holds exactly one id plus one URL, so extra
    keys passed here are dropped; cite them in prose instead.
    """
    parts = []
    for k in keys[:1]:
        k = _resolve(k)
        sid, url = SRC[k]
        parts.append(f"{sid}|{url}")
    return ";".join(parts)


def sid(key):
    return SRC[key][0]


def url(key):
    return SRC[key][1]


def write_csv(path, fields, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n",
                           quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            missing = [k for k in fields if k not in r]
            if missing:
                raise KeyError(f"{path}: row missing {missing}")
            for k in fields:
                if r[k] is None or str(r[k]) == "":
                    raise ValueError(f"{path}: empty cell {k} in {r.get(fields[0])}")
            w.writerow(r)
    print(f"wrote {path}: {len(rows)} rows")
