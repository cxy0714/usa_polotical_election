#!/usr/bin/env python3
"""Cross-checks the batch-2 case archives before the site build.

For every case:
  * every source URL appears in `_staging/fetch_log.csv` with a 2xx status (Wikipedia mirrors count)
  * no unused source ids, no source id cited but absent from sources.csv (validator covers the latter)
  * no hedging language inside factual CSV cells ("probably", "likely", "appears to", ...)
  * README's result table mentions the winning candidate's vote total from election_results.csv
  * case_meta candidate ids appear in the data
Prints a report and exits non-zero if a hard check fails.
"""
import csv
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH2 = ["michigan-senate-2026", "alaska-senate-2026", "iowa-senate-2026",
          "ohio-senate-2026", "georgia-senate-2026", "los-angeles-mayor-2026"]
if len(sys.argv) > 1:
    BATCH2 = sys.argv[1:]
HEDGES = re.compile(r"\b(probably|likely|presumably|appears to|seems to|may have|might have|"
                    r"is believed to|reportedly)\b", re.I)


def rows(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    hard = []
    for case in BATCH2:
        d = os.path.join(ROOT, case)
        if not os.path.isdir(d):
            hard.append(f"{case}: missing folder")
            continue
        meta = json.load(open(os.path.join(d, "_staging", "case_meta.json"), encoding="utf-8"))
        sources = rows(os.path.join(d, "09_sources", "sources.csv"))
        log = rows(os.path.join(d, "_staging", "fetch_log.csv"))
        fetched = {r["url"].rstrip("/") for r in log if r.get("http_status", "").startswith("2")}

        missing = [s["source_id"] for s in sources if s["url"].rstrip("/") not in fetched]
        print(f"\n{case}: {len(sources)} sources, {len(log)} fetch rows, {len(missing)} not in a 2xx fetch")
        for sid in missing[:8]:
            s = next(x for x in sources if x["source_id"] == sid)
            print(f"   not-fetched {sid} {s['url'][:110]}")
        if len(missing) > max(3, len(sources) // 5):
            hard.append(f"{case}: {len(missing)} sources lack a successful fetch record")

        cited = set()
        for base, _, files in os.walk(d):
            if "_staging" in base.split(os.sep) or "site" in base.split(os.sep):
                continue
            for name in files:
                if not name.endswith(".csv") or name == "sources.csv":
                    continue
                for r in rows(os.path.join(base, name)):
                    for m in re.findall(r"SRC-\d{4}", r.get("source_urls", "")):
                        cited.add(m)
        unused = [s["source_id"] for s in sources if s["source_id"] not in cited]
        if unused:
            print(f"   unused sources: {len(unused)} (ok, but they should justify their place)")

        for base, _, files in os.walk(d):
            if "_staging" in base.split(os.sep) or "site" in base.split(os.sep):
                continue
            for name in files:
                if not name.endswith(".csv") or name == "sources.csv":
                    continue
                p = os.path.join(base, name)
                for i, r in enumerate(rows(p), start=2):
                    for col, val in r.items():
                        if col in ("analyst_interpretation", "notes", "analyst_notes", "reliability_notes",
                                   "key_framing", "change_notes", "framing_of_candidate", "population",
                                   "sample_type", "title", "headline", "notable_quotes", "relevant_quote_or_info"):
                            continue
                        if HEDGES.search(val or ""):
                            hard.append(f"{case}/{name}:{i} hedging in {col}: {val[:90]!r}")
                            break

        res = rows(os.path.join(d, "07_electoral_context", "election_results.csv"))
        generals = [r for r in res if r.get("race_id", "").endswith("GENERAL") and r.get("winner") == "yes"]
        readme = open(os.path.join(d, "README.md"), encoding="utf-8-sig").read()
        for g in generals:
            votes = g.get("votes", "")
            if votes not in readme.replace(",", ""):
                hard.append(f"{case}: README does not contain winner total {votes} for {g.get('candidate')}")

        # county arithmetic: county sums should reconcile to the statewide general-election totals
        county = rows(os.path.join(d, "07_electoral_context", "county_results.csv"))
        if county and generals:
            gen = [r for r in res if r.get("race_id") == generals[0].get("race_id")]
            for r in gen:
                if r.get("votes") in ("unknown", ""):
                    continue
                total = int(r["votes"])
                keys = [k for k in county[0] if k.endswith("_votes") and k != "other_votes"]
                idx = meta["candidates"].index(next(c for c in meta["candidates"] if c["name"] == r["candidate"]))
                col = keys[idx] if idx < len(keys) else None
                if not col:
                    continue
                s = sum(int(x[col]) for x in county if x.get(col, "unknown").isdigit())
                diff = abs(s - total) / total if total else 0
                print(f"   county sum {r['candidate']}: {s:,} vs statewide {total:,} ({diff:.2%})")
                if diff > 0.02:
                    hard.append(f"{case}: county table does not reconcile for {r['candidate']} ({s:,} vs {total:,})")

        for cand in meta["candidates"]:
            n = 0
            for base, _, files in os.walk(d):
                if "_staging" in base.split(os.sep) or "site" in base.split(os.sep):
                    continue
                for name in files:
                    if name.endswith(".csv"):
                        for r in rows(os.path.join(base, name)):
                            if cand["id"] in (r.get("candidate_id", ""), r.get("candidate", "")):
                                n += 1
            print(f"   {cand['id']}: {n} rows")
            if n == 0:
                hard.append(f"{case}: candidate {cand['id']} has no rows")

        # Clothing claims need a text source; a text-only compiler cannot observe a photograph.
        images = rows(os.path.join(d, "04_visual_archive", "image_archive.csv"))
        claims = [r for r in images if not r.get("clothing_notes", "unknown").lower().startswith("unknown")]
        for r in claims:
            print(f"   CLOTHING {r.get('image_id')} {r.get('candidate_id')}: {r.get('clothing_notes')[:120]}")
            print(f"            src={r.get('source_url','')[:110]} notes={r.get('notes','')[:100]}")

    print(f"\nhard issues: {len(hard)}")
    for h in hard[:40]:
        print("  FAIL", h)
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
