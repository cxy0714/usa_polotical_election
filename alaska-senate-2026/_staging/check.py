# -*- coding: utf-8 -*-
"""Post-build consistency checks that the contract validator does not cover."""
import csv, io, os, re

CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rows(rel):
    with io.open(os.path.join(CASE, rel), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


srcs = rows("09_sources/sources.csv")
print("sources:", len(srcs), "unique ids:", len({s["source_id"] for s in srcs}),
      "unique urls:", len({s["url"] for s in srcs}))

# 1. every source url appears in the fetch log
log = io.open(os.path.join(CASE, "_staging", "fetch_log.csv"), encoding="utf-8-sig").read()
missing = [s["source_id"] for s in srcs if s["url"] not in log]
print("sources whose url is not in fetch_log:", len(missing), missing[:10])

# 2. every fetch_log saved_file exists
with io.open(os.path.join(CASE, "_staging", "fetch_log.csv"), encoding="utf-8-sig", newline="") as f:
    fl = list(csv.DictReader(f))
print("fetch_log rows:", len(fl),
      "non-200:", sum(1 for r in fl if r["http_status"] != "200"))
absent = []
for r in fl:
    sf = r["saved_file"]
    if sf and sf not in ("unknown", "not_saved") and not os.path.exists(os.path.join(CASE, sf)):
        absent.append(sf)
print("logged files missing on disk:", len(absent), absent[:5])

# 3. every source_urls cell resolves
bad = []
for rel in ["01_candidates/policy_positions.csv", "02_campaign_events/campaign_events.csv",
            "03_speeches/speech_archive.csv", "03_speeches/speech_video_index.csv",
            "05_campaign_media/advertisements.csv", "05_campaign_media/social_media.csv",
            "06_campaign_finance/campaign_finance.csv",
            "07_electoral_context/election_results.csv", "07_electoral_context/polling.csv"]:
    ids = {s["source_id"] for s in srcs}
    for r in rows(rel):
        if "source_urls" not in r:
            continue
        sid = r["source_urls"].split("|")[0]
        if sid not in ids:
            bad.append((rel, sid))
print("unresolvable source ids:", len(bad), bad[:5])

# 4. README table vs election_results
res = {r["candidate"]: r for r in rows("07_electoral_context/election_results.csv")
       if r["race_id"] == "AK-SEN-2026-GEN"}
readme = io.open(os.path.join(CASE, "README.md"), encoding="utf-8").read()
mism = []
for cand, r in res.items():
    if cand == "Total votes cast for U.S. Senator":
        continue
    if "{:,}".format(int(r["votes"])) not in readme or r["percentage"] not in readme:
        mism.append(cand)
print("README/result mismatches:", mism)

# 5. downloaded images exist and are under 2 MB
imgs = [r for r in rows("04_visual_archive/image_archive.csv") if r["local_filename"] != "unknown"]
for r in imgs:
    p = os.path.join(CASE, r["local_filename"])
    ok = os.path.exists(p)
    size = os.path.getsize(p) if ok else -1
    print("  image", r["image_id"], ok, size, "OK" if 0 < size < 2 * 1024 * 1024 else "CHECK")

# 6. front matter on every md
for root, dirs, files in os.walk(CASE):
    if "_staging" in root:
        continue
    for fn in files:
        if fn.endswith(".md"):
            rel = os.path.relpath(os.path.join(root, fn), CASE)
            head = io.open(os.path.join(root, fn), encoding="utf-8").read(400)
            if not head.startswith("---\ntitle:"):
                print("  front matter problem:", rel, head[:40].replace("\n", " "))

# 7. forbidden placeholders in text deliverables
for root, dirs, files in os.walk(CASE):
    if "_staging" in root:
        continue
    for fn in files:
        if fn.endswith(".md"):
            rel = os.path.relpath(os.path.join(root, fn), CASE)
            t = io.open(os.path.join(root, fn), encoding="utf-8").read()
            for bad in ("TODO", "TBD", "N/A", "FIXME"):
                if bad in t:
                    print("  placeholder", bad, "in", rel)
