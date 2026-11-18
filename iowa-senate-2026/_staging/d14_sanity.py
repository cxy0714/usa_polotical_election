# -*- coding: utf-8 -*-
"""Final sanity sweep before reporting."""
import collections
import csv
import glob
import io
import os

CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rows(rel):
    return list(csv.DictReader(io.open(os.path.join(CASE, rel), encoding="utf-8", newline="")))


cr = rows("07_electoral_context/county_results.csv")
names = [r["county"] for r in cr]
print("counties", len(cr), "unique", len(set(names)))
bad = [r["county_id"] for r in cr
       if int(r["turek_votes"]) + int(r["hinson_votes"]) + int(r["other_votes"]) != int(r["total_votes"])]
print("county rows where parts != total:", bad)
print("sum turek", sum(int(r["turek_votes"]) for r in cr),
      "sum hinson", sum(int(r["hinson_votes"]) for r in cr),
      "sum other", sum(int(r["other_votes"]) for r in cr),
      "sum total", sum(int(r["total_votes"]) for r in cr))
extreme = sorted(cr, key=lambda r: float(r["hinson_pct"]))[:2] + sorted(cr, key=lambda r: -float(r["hinson_pct"]))[:2]
for r in extreme:
    print("  %-12s turek %5s (%s) hinson %5s (%s)" % (r["county"], r["turek_votes"], r["turek_pct"],
                                                     r["hinson_votes"], r["hinson_pct"]))

pl = rows("07_electoral_context/polling.csv")
for r in pl:
    a, b = r["turek_pct"], r["hinson_pct"]
    lead = "Turek" if float(a) > float(b) else ("Hinson" if float(b) > float(a) else "tie")
    if lead != r["leader"]:
        print("POLL LEADER MISMATCH", r["poll_id"], a, b, r["leader"])

pos = rows("01_candidates/policy_positions.csv")
print("positions by candidate", collections.Counter(r["candidate_id"] for r in pos))
print("issues", collections.Counter(r["issue"] for r in pos).most_common())

src = rows("09_sources/sources.csv")
print("sources", len(src), "tiers", collections.Counter(r["source_tier"] for r in src))
print("types", collections.Counter(r["source_type"] for r in src).most_common(8))
print("paywalled/blocked notes", sum(1 for r in src if r["reliability_notes"].upper().startswith("PAYWALL")))

cov = rows("05_campaign_media/media_coverage.csv")
print("coverage outlets", collections.Counter(r["outlet"] for r in cov).most_common())

imgs = sorted(glob.glob(os.path.join(CASE, "04_visual_archive", "*.jpg")))
print("downloaded images", [(os.path.basename(p), os.path.getsize(p)) for p in imgs])

print("\nfile sizes (KB):")
total = 0
for p in sorted(glob.glob(os.path.join(CASE, "**", "*"), recursive=True)):
    if os.path.isfile(p) and "_staging" not in p:
        total += os.path.getsize(p)
print("non-staging total KB", round(total / 1024))
print("md count", len(glob.glob(os.path.join(CASE, "**", "*.md"), recursive=True)))
print("csv count", len(glob.glob(os.path.join(CASE, "**", "*.csv"), recursive=True)))
