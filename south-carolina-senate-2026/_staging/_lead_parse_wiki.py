#!/usr/bin/env python3
"""Parse the mirrored wikitext into clean tabular data.

Outputs (all under _staging/mirrors/):
  county_results_parsed.csv   one row per county from section 58's results table
  election_boxes.csv          every {{Election box}} candidate/total row, with its section

The point is to hand downstream streams and the Lead a parsed file instead of making them
re-read 21 KB of wiki-table markup. Nothing here invents data: every value is a cell that
exists in the mirrored wikitext.

Run: python _staging/_lead_parse_wiki.py
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SECT = os.path.join(HERE, "mirrors", "sections")
OUT = os.path.join(HERE, "mirrors")


def clean_cell(s):
    s = s.strip()
    if s.startswith("|"):
        s = s[1:]
    s = re.sub(r"^style=\"[^\"]*\"\s*\|", "", s)
    s = re.sub(r"^align=\"?[a-z]+\"?\s*\|", "", s)
    s = re.sub(r"^bgcolor=\"[^\"]*\"\s*\|", "", s)
    s = s.replace("'''", "").replace("''", "")
    # [[Target|Display]] -> Display ; [[Target]] -> Target
    s = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"\[\[([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\{\{[^}]*\}\}", "", s)
    s = s.strip().strip("|").strip()
    return s


def num_or_unknown(s):
    s = s.replace(",", "").replace("&nbsp;", "").strip()
    s = s.replace("%", "").replace("+", "").replace("−", "-")
    if re.fullmatch(r"-?\d+(\.\d+)?", s):
        return s
    return "unknown"


def parse_counties():
    raw = open(os.path.join(SECT, "58.wikitext"), encoding="utf-8").read()
    rows = []
    cur = None
    for line in raw.splitlines():
        if line.startswith("|-"):
            if cur:
                rows.append(cur)
            cur = []
            continue
        if cur is None or not line.startswith("|"):
            continue
        if line.startswith("|}") or line.startswith("|+"):
            continue
        # a data row: first cell is the county, then 12 numeric cells
        cur.append(clean_cell(line))
    if cur:
        rows.append(cur)

    out = []
    for cells in rows:
        if len(cells) < 13:
            continue
        county = cells[0]
        if not county or county.lower().startswith(("county", "total")):
            continue
        vals = [num_or_unknown(c) for c in cells[1:13]]
        # layout after county: A#,A%,G#,G%,W#,W%,H#,H%,WI#,WI%,M#,M%
        rec = {
            "county": county,
            "andrews_votes": vals[0], "andrews_pct": vals[1],
            "graham_votes": vals[2], "graham_pct": vals[3],
            "whitener_votes": vals[4], "whitener_pct": vals[5],
            "hackett_votes": vals[6], "hackett_pct": vals[7],
            "writein_votes": vals[8], "writein_pct": vals[9],
            "margin_votes": vals[10], "margin_pct": vals[11],
            "total_votes": num_or_unknown(cells[13]) if len(cells) > 13 else "unknown",
        }
        out.append(rec)
    return out


BOX = re.compile(r"\{\{Election box[^{}]*?\}\}", re.S)


def parse_boxes():
    out = []
    for fn in sorted(os.listdir(SECT)):
        if not fn.endswith(".wikitext"):
            continue
        n = int(fn.split(".")[0])
        raw = open(os.path.join(SECT, fn), encoding="utf-8").read()
        for m in BOX.finditer(raw):
            blob = m.group(0)

            def field(name):
                mm = re.search(r"\|\s*" + name + r"\s*=\s*([^\n|}]+)", blob)
                return clean_cell(mm.group(1)) if mm else "unknown"

            cand = field("candidate")
            votes = num_or_unknown(field("votes"))
            pct = num_or_unknown(field("percentage"))
            kind = "total" if "total" in blob.split("\n")[0] else "candidate"
            if kind == "total":
                cand = "TOTAL"
            if cand == "unknown" and kind == "candidate":
                continue
            out.append({"section": n, "kind": kind, "candidate": cand,
                        "votes": votes, "percentage": pct})
    return out


def main():
    counties = parse_counties()
    p1 = os.path.join(OUT, "county_results_parsed.csv")
    with open(p1, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["county", "andrews_votes", "andrews_pct",
                                          "graham_votes", "graham_pct", "whitener_votes",
                                          "whitener_pct", "hackett_votes", "hackett_pct",
                                          "writein_votes", "writein_pct", "margin_votes",
                                          "margin_pct", "total_votes"], lineterminator="\n")
        w.writeheader()
        w.writerows(counties)
    print(f"county_results_parsed.csv: {len(counties)} counties")
    if counties:
        tot = sum(int(r["andrews_votes"]) for r in counties if r["andrews_votes"].isdigit())
        totg = sum(int(r["graham_votes"]) for r in counties if r["graham_votes"].isdigit())
        print(f"  Andrews county-vote sum: {tot:,}   Graham county-vote sum: {totg:,}")
        print(f"  statewide reported:      1,044,001      952,191")

    boxes = parse_boxes()
    p2 = os.path.join(OUT, "election_boxes.csv")
    with open(p2, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["section", "kind", "candidate", "votes", "percentage"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(boxes)
    print(f"election_boxes.csv: {len(boxes)} rows")
    per = {}
    for b in boxes:
        if b["kind"] == "candidate":
            per.setdefault(b["section"], []).append(b)
    for n in sorted(per):
        names = ", ".join(f"{b['candidate']} {b['percentage']}%" for b in per[n][:4])
        print(f"  section {n:02d}: {len(per[n])} candidates — {names}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
