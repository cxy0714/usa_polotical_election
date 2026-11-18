#!/usr/bin/env python3
"""What can the batch-2 archives actually support about image, styling and staging?

Scans each case for (a) image records whose clothing_notes are not `unknown`,
(b) coverage rows whose framing/quotes mention dress, styling or appearance,
(c) event rows whose visual_notes are not `unknown`. Prints a per-case table and
the matching evidence, so the synthesis document quotes the data rather than
the other way round.

Usage: python _tools/phenomena_report.py
"""
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = [
    ("texas-senate-2026", "Texas"),
    ("michigan-senate-2026", "Michigan"),
    ("alaska-senate-2026", "Alaska"),
    ("south-carolina-senate-2026", "South Carolina"),
    ("iowa-senate-2026", "Iowa"),
    ("ohio-senate-2026", "Ohio"),
    ("georgia-senate-2026", "Georgia"),
    ("los-angeles-mayor-2026", "Los Angeles"),
]
STYLE = re.compile(r"\b(suit|shirt|dress|attire|wardrobe|stylist|styling|appearance|"
                   r"jacket|blazer|tie|boots|jeans|sleeves|grooming|hair)\b", re.I)


def rows(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    if "--json" in sys.argv:
        import json
        out = {}
        for folder, label in CASES:
            d = os.path.join(ROOT, folder)
            imgs = rows(os.path.join(d, "04_visual_archive", "image_archive.csv"))
            events = rows(os.path.join(d, "02_campaign_events", "campaign_events.csv"))
            cov = rows(os.path.join(d, "05_campaign_media", "media_coverage.csv"))
            res = rows(os.path.join(d, "07_electoral_context", "election_results.csv"))
            out[folder] = {
                "label": label,
                "images": len(imgs),
                "clothing": [{"id": r.get("image_id"), "cand": r.get("candidate_id"),
                              "note": r.get("clothing_notes"), "src": r.get("source_url")}
                             for r in imgs if not r.get("clothing_notes", "unknown").lower().startswith("unknown")],
                "style_coverage": [{"id": r.get("coverage_id"), "cand": r.get("candidate_id"),
                                    "outlet": r.get("outlet"), "date": r.get("publication_date"),
                                    "framing": r.get("key_framing"), "url": r.get("url")}
                                   for r in cov if STYLE.search(" ".join(r.get(k, "") for k in
                                   ("key_framing", "notable_quotes", "framing_of_candidate")))],
                "visual_events": [{"id": r.get("event_id"), "cand": r.get("candidate_id"),
                                   "note": r.get("visual_notes")}
                                  for r in events if not r.get("visual_notes", "unknown").lower().startswith("unknown")],
                "results": [{"race": r.get("race_id"), "cand": r.get("candidate"),
                             "votes": r.get("votes"), "pct": r.get("percentage")} for r in res],
            }
        p = os.path.join(ROOT, "_research", "2026", "phenomena.json")
        json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("wrote", p)
        return 0

    print("| Case | image rows | clothing documented | visual_notes documented | coverage style hits |")
    print("|---|---|---|---|---|")
    detail = []
    for folder, label in CASES:
        d = os.path.join(ROOT, folder)
        imgs = rows(os.path.join(d, "04_visual_archive", "image_archive.csv"))
        events = rows(os.path.join(d, "02_campaign_events", "campaign_events.csv"))
        cov = rows(os.path.join(d, "05_campaign_media", "media_coverage.csv"))
        cloth = [r for r in imgs if not r.get("clothing_notes", "unknown").lower().startswith("unknown")]
        vis = [r for r in events if not r.get("visual_notes", "unknown").lower().startswith("unknown")]
        hits = [r for r in cov if STYLE.search(" ".join(r.get(k, "") for k in
                ("key_framing", "notable_quotes", "framing_of_candidate")))]
        print(f"| {label} | {len(imgs)} | {len(cloth)} | {len(vis)} | {len(hits)} |")
        detail.append((label, cloth, hits, vis))

    print("\n## Evidence by case\n")
    for label, cloth, hits, vis in detail:
        print(f"### {label}")
        for r in cloth[:6]:
            print(f"- IMAGE {r.get('image_id')} {r.get('candidate_id')}: {r.get('clothing_notes')[:180]} "
                  f"({r.get('source_url')})")
        for r in hits[:8]:
            print(f"- COVERAGE {r.get('coverage_id')} {r.get('outlet')} {r.get('publication_date')}: "
                  f"{r.get('key_framing','')[:150]} ({r.get('url')})")
        for r in vis[:4]:
            print(f"- EVENT {r.get('event_id')}: {r.get('visual_notes','')[:160]}")
        if not (cloth or hits or vis):
            print("- nothing on dress/styling in the retrieved record")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
