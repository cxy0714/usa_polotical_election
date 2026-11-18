"""Build 09_sources/sources.csv from _staging/registry.py.

Registry keys are matched against mirror stems fuzzily (the URL-list generator
truncated stems at 70 characters). Unresolved keys abort the build.
"""
import csv
import os
import sys

sys.path.insert(0, "_staging")
import registry  # noqa: E402

ACCESS = "2026-11-18"
FIELDS = ["source_id", "url", "title", "publisher", "publication_date", "event_date",
          "access_date", "source_tier", "source_type", "relevant_quote_or_info",
          "reliability_notes", "used_by"]


def load_stems():
    rows = list(csv.DictReader(open("_staging/fetch_log.csv", encoding="utf-8")))
    m = {}
    for r in rows:
        stem = os.path.splitext(os.path.basename(r["saved_file"]))[0]
        if stem in ("unknown", ""):
            continue
        m.setdefault(stem, r["url"])
    return m


def resolve(key, stems):
    if key in stems:
        return key
    cands = [s for s in stems if s.startswith(key[:60])]
    if len(cands) == 1:
        return cands[0]
    cands = [s for s in stems if key[:40] in s]
    if len(cands) == 1:
        return cands[0]
    return None


def main():
    stems = load_stems()
    stems["wiki_ohio"] = stems["wiki_ohio_live"]
    out = []
    unresolved = []
    pairs = []
    for i, (key, tier, stype, edate, info, notes, used) in enumerate(registry.REGISTRY):
        real = resolve(key, stems)
        if not real:
            unresolved.append(key)
            continue
        pairs.append((key, real))
        url = stems[real]
        sid = f"SRC-{1001 + len(out)}"
        t = registry.title(real)
        if t == "unknown" and key.startswith("wiki_"):
            t = "Wikipedia: " + key
        out.append({
            "source_id": sid,
            "url": url,
            "title": t if t else "unknown",
            "publisher": registry.publisher_for(url),
            "publication_date": registry.pubdate(real),
            "event_date": edate,
            "access_date": ACCESS,
            "source_tier": tier,
            "source_type": stype,
            "relevant_quote_or_info": info,
            "reliability_notes": notes,
            "used_by": used,
        })
    os.makedirs("09_sources", exist_ok=True)
    # ---- append Commons image records not already in the registry ----------
    import json as _json
    if os.path.exists("_staging/images.json"):
        have = {k for k, _real in pairs}
        for rec in _json.load(open("_staging/images.json", encoding="utf-8")):
            if rec["key"] in have:
                continue
            out.append({
                "source_id": f"SRC-{1001 + len(out)}",
                "url": rec["page_url"],
                "title": "Wikimedia Commons file: " + rec["title"].replace("File:", ""),
                "publisher": "Wikimedia Commons",
                "publication_date": rec["date"] if rec["date"] != "unknown" else "unknown",
                "event_date": "unknown",
                "access_date": ACCESS,
                "source_tier": "T1",
                "source_type": "photo",
                "relevant_quote_or_info": (rec.get("desc") or "Commons media file")[:300],
                "reliability_notes": (
                    f"Licence: {rec['license']}; credit: {rec['artist'][:120]}. "
                    "Licence and credit read from the Commons API imageinfo response."),
                "used_by": "",
            })
            pairs.append((rec["key"], rec["key"]))
        # normalise: any image source must point at the Commons FILE PAGE, not the
        # uploaded/thumbnail binary
        page_by_key = {r["key"]: r for r in _json.load(
            open("_staging/images.json", encoding="utf-8"))}
        by_id = {}
        for rec in out:
            by_id[rec["source_id"]] = rec
        for key, real in pairs:
            if key not in page_by_key:
                continue
            rec_img = page_by_key[key]
            for rec in out:
                if rec["url"] == stems.get(real) or rec["url"] in (
                        rec_img["orig_url"], rec_img["page_url"]):
                    rec["url"] = rec_img["page_url"]
                    rec["title"] = "Wikimedia Commons file: " + rec_img["title"].replace(
                        "File:", "")
                    break
    with open("09_sources/sources.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print("wrote", len(out), "sources; unresolved", len(unresolved))
    for u in unresolved:
        print("  UNRESOLVED", u)
    # emit key -> SRC id map for the other builders
    with open("_staging/srclist.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["src_id", "key", "url"])
        for rec, (key, real) in zip(out, pairs):
            w.writerow([rec["source_id"], key, rec["url"]])
    return 0 if not unresolved else 1


if __name__ == "__main__":
    sys.exit(main())
