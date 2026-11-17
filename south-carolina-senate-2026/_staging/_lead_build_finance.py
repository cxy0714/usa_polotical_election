#!/usr/bin/env python3
"""Rebuild 06_campaign_finance/* from the FEC tables quoted in the race article.

The stream that first produced this file mixed up the candidate ids and lost the report periods,
so it is rebuilt here from four documented FEC snapshots:

  2026-03-31  initial-primary reports (both parties)
  2026-07-22  special-primary reports
  2026-08-05  runoff reports
  2026-10-14  general-election reports

Only the two principals go into `campaign_finance.csv`, because its schema restricts candidate_id
to ANDREWS/GRAHAM. Every other filed candidate goes into `other_candidates_finance.csv`, which
keeps the record complete without breaking the contract.

口径 rule (conventions §4): candidate-committee figures are never added to super-PAC independent
expenditures; those live in `05_campaign_media/advertisements.csv` as separate rows.

Run: python _staging/_lead_build_finance.py
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "06_campaign_finance")
WIKI = "SRC-2108|https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_South_Carolina"

HEADER = ["finance_id", "candidate_id", "period", "report_type", "reporting_deadline", "receipts",
          "individual_contributions", "pac_contributions", "disbursements", "cash_on_hand",
          "debts_owed", "source_urls", "verification_status", "notes"]

OTHER_HEADER = ["finance_id", "candidate_name", "party", "period", "receipts", "disbursements",
                "cash_on_hand", "source_urls", "verification_status", "notes"]

# (period, candidate, party, raised, spent, cash_on_hand, note)
REPORTS = [
    ("2026-03-31", "Lindsey Graham", "Republican", "20688173", "21566021", "11613609",
     "the principal committee at this date belonged to the late senator; Darline Graham was not "
     "yet a candidate"),
    ("2026-03-31", "Annie Andrews", "Democratic", "6519296", "3880008", "2639287", "unknown"),
    ("2026-07-22", "Duke Buckner", "Republican", "10960", "10456", "504", "unknown"),
    ("2026-07-22", "Russell Fry", "Republican", "495027", "10441", "484586", "unknown"),
    ("2026-07-22", "Mark Lynch", "Republican", "5919539", "5372977", "546561", "unknown"),
    ("2026-07-22", "Ralph Norman", "Republican", "173610", "2189", "171421", "unknown"),
    ("2026-07-22", "Mark Sanford", "Republican", "206237", "177136", "1352604", "unknown"),
    ("2026-08-05", "Darline Graham", "Republican", "346783", "95351", "251431", "unknown"),
    ("2026-08-05", "Ralph Norman", "Republican", "934892", "697553", "237339", "unknown"),
    ("2026-10-14", "Darline Graham", "Republican", "1917646", "1283216", "634430", "unknown"),
    ("2026-10-14", "Annie Andrews", "Democratic", "24216841", "22507375", "1709466", "unknown"),
    ("2026-10-14", "Catherine Fleming Bruce", "Write-in", "18989", "8258", "10731",
     "write-in candidate; not on the ballot as a party nominee"),
    ("2026-03-31", "Thomas Dismukes", "Republican", "14935", "13125", "1810", "unknown"),
    ("2026-03-31", "Ethan Holliman", "Republican", "20270", "20270", "0", "unknown"),
    ("2026-03-31", "Mark Lynch", "Republican", "5726191", "2398855", "3327336", "unknown"),
    ("2026-03-31", "Paul Dans", "Republican", "1011421", "565237", "446184", "unknown"),
    ("2026-03-31", "Catherine Fleming Bruce", "Democratic", "0", "0", "5030",
     "filed as a Democrat at this date"),
    ("2026-03-31", "Kyle Freeman", "Democratic", "53475", "52239", "1236", "unknown"),
    ("2026-03-31", "Brandon Brown", "Democratic", "69569", "20369", "40709", "unknown"),
    ("2026-03-31", "Christopher Giracello", "Democratic", "0", "0", "0", "unknown"),
]

DEADLINES = {"2026-03-31": "2026-04-15", "2026-07-22": "2026-07-15", "2026-08-05": "2026-08-15",
             "2026-10-14": "2026-10-15"}


def main():
    os.makedirs(OUT, exist_ok=True)
    principal, other = [], []
    counters = {"ANDREWS": 0, "GRAHAM": 0}
    for period, cand, party, raised, spent, coh, note in REPORTS:
        if cand == "Annie Andrews":
            counters["ANDREWS"] += 1
            principal.append([f"AND-FIN-{counters['ANDREWS']:04d}", "ANDREWS", period,
                              "FEC_candidate_committee", DEADLINES[period], raised, "unknown",
                              "unknown", spent, coh, "unknown", WIKI, "partially verified",
                              f"transcribed from the FEC table quoted in the race article "
                              f"({period}); line-item detail not retrieved. {note}"])
        elif cand in ("Darline Graham", "Lindsey Graham"):
            counters["GRAHAM"] += 1
            principal.append([f"GRA-FIN-{counters['GRAHAM']:04d}", "GRAHAM", period,
                              "FEC_candidate_committee", DEADLINES[period], raised, "unknown",
                              "unknown", spent, coh, "unknown", WIKI, "partially verified",
                              f"actor: {'LINDSEY_GRAHAM' if cand == 'Lindsey Graham' else 'DARLINE_GRAHAM'}. "
                              f"transcribed from the FEC table quoted in the race article "
                              f"({period}); line-item detail not retrieved. {note}"])
        else:
            other.append([f"OTH-FIN-{len(other) + 1:04d}", cand, party, period, raised, spent, coh,
                          WIKI, "partially verified",
                          f"non-principal candidate; kept out of campaign_finance.csv because its "
                          f"schema restricts candidate_id to ANDREWS/GRAHAM. {note}"])

    with open(os.path.join(OUT, "campaign_finance.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        w.writerow(HEADER)
        w.writerows(principal)
    with open(os.path.join(OUT, "other_candidates_finance.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        w.writerow(OTHER_HEADER)
        w.writerows(other)
    print(f"campaign_finance.csv: {len(principal)} rows {counters}")
    print(f"other_candidates_finance.csv: {len(other)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
