#!/usr/bin/env python3
"""Build 07_electoral_context/*.csv from the parsed mirrors.

Every number below is transcribed from a parsed table, and every row names the source it came
from (`SRC-####|url`). Where a value is arithmetic on two documented values (e.g. write-in share
= write-in votes / statewide total) the row says so in `notes` — it is never presented as a
reported figure.

Inputs : _staging/mirrors/county_results_parsed.csv, _staging/mirrors/election_boxes.csv
Outputs: 07_electoral_context/{election_results,county_results,polling,primary_polling}.csv

Run: python _staging/_lead_build_electoral.py
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MIR = os.path.join(HERE, "mirrors")
OUT = os.path.join(ROOT, "07_electoral_context")

WIKI = "SRC-2108|https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_South_Carolina"
CBS = "SRC-2111|https://www.cbsnews.com/news/south-carolina-2026-senate-annie-andrews-darline-graham/"

RESULTS_HEADER = ["race_id", "race_name", "election_date", "candidate", "party", "votes",
                  "percentage", "winner", "source_urls", "verification_status", "notes"]
COUNTY_HEADER = ["county_id", "county", "candidate_andrews_votes", "candidate_graham_votes",
                 "other_votes", "andrews_pct", "graham_pct", "total_votes", "source_urls",
                 "verification_status"]
POLL_HEADER = ["poll_id", "pollster", "sponsor", "field_start", "field_end", "population",
               "sample_size", "margin_of_error", "andrews_pct", "graham_pct", "other_pct",
               "undecided_pct", "leader", "margin", "source_urls", "verification_status", "notes"]
PRIMARY_POLL_HEADER = ["poll_id", "race_stage", "pollster", "sponsor", "field_start", "field_end",
                       "population", "sample_size", "margin_of_error", "graham_pct", "norman_pct",
                       "fry_pct", "lynch_pct", "sanford_pct", "other_pct", "undecided_pct",
                       "source_urls", "verification_status", "notes"]

VIA = ("transcribed from the Wikipedia section {n} table; the underlying filing or election-office "
       "tabulation was not independently retrieved in this pass")

DEM = [
    ("Annie Andrews", "Democratic", "226075", "61.5", "yes"),
    ("Brandon Brown", "Democratic", "110962", "30.2", "no"),
    ("Kyle Freeman", "Democratic", "30374", "8.3", "no"),
]
GOP = [
    ("Lindsey Graham", "Republican", "264091", "56.8", "yes"),
    ("Mark Lynch", "Republican", "134360", "28.9", "no"),
    ("Thomas Dismukes", "Republican", "24164", "5.2", "no"),
    ("Pat Herrmann", "Republican", "17448", "3.8", "no"),
    ("Calvin Cowen", "Republican", "14171", "3.0", "no"),
    ("Darius Mitchell", "Republican", "10842", "2.3", "no"),
]
SPECIAL = [
    ("Darline Graham", "Republican", "109881", "32.8", "yes"),
    ("Ralph Norman", "Republican", "82627", "24.6", "no"),
    ("Russell Fry", "Republican", "65955", "19.7", "no"),
    ("Mark Sanford", "Republican", "50136", "14.9", "no"),
    ("Mark Lynch", "Republican", "19892", "5.9", "no"),
    ("Danny Ford II", "Republican", "2804", "0.8", "no"),
    ("Duke Buckner", "Republican", "1583", "0.5", "no"),
    ("Glenda Gail Parker", "Republican", "977", "0.3", "no"),
    ("Samuel Shepherd", "Republican", "931", "0.3", "no"),
    ("Mark Struthers McBride", "Republican", "769", "0.2", "no"),
]
RUNOFF = [
    ("Darline Graham", "Republican", "193486", "52.4", "yes"),
    ("Ralph Norman", "Republican", "175412", "47.6", "no"),
]
GENERAL = [
    ("Annie Andrews", "Democratic", "1044001", "51.14", "yes"),
    ("Darline Graham", "Republican", "952191", "46.64", "no"),
    ("Kasie Whitener", "Libertarian", "23585", "1.16", "no"),
    ("Mark Hackett", "Constitution", "16811", "0.82", "no"),
    ("Write-in (Catherine Fleming Bruce)", "Write-in", "4899", "0.24", "no"),
]

POLLS = [
    ("Trafalgar Group", "Trafalgar Group (R)", "2026-10-31", "2026-11-01", "LV", "1091", "2.9",
     "46", "48", "3", "4", "Graham", "Graham +2", "no undecided cell in source"),
    ("Rasmussen Reports", "Rasmussen Reports (R)", "2026-10-27", "2026-10-31", "LV", "1028", "3.0",
     "47", "50", "unknown", "6", "Graham", "Graham +3", "source shows no third-party column"),
    ("Resonance Media Services", "Resonance Media Services (R)", "2026-10-30", "2026-10-30", "LV",
     "600", "4.0", "46", "45", "3", "7", "Andrews", "Andrews +1", "one-day field window"),
    ("Patinkin Research Strategies", "Patinkin Research Strategies (D)", "2026-10-27", "2026-10-29",
     "LV", "500", "4.4", "48", "43", "8", "unknown", "Andrews", "Andrews +5",
     "source shows no undecided cell"),
    ("New York Times/Siena University", "New York Times/Siena University", "2026-10-19", "2026-10-26",
     "LV", "707", "4.3", "48", "48", "0", "3", "tie", "0", "exact tie in source"),
    ("Targoz Media Research", "Targoz Media Research", "2026-10-16", "2026-10-25", "LV", "895", "2.8",
     "46", "47", "3", "4", "Graham", "Graham +1", "unknown"),
    ("East Carolina University", "East Carolina University", "2026-10-19", "2026-10-24", "LV", "955",
     "3.7", "47", "51", "2", "unknown", "Graham", "Graham +4", "source shows no undecided cell"),
    ("The Citadel", "The Citadel", "2026-10-14", "2026-10-25", "LV", "890", "3.4", "39", "43", "2",
     "15", "Graham", "Graham +4", "first of two Citadel samples (LV)"),
    ("The Citadel", "The Citadel", "2026-10-14", "2026-10-25", "RV", "1009", "unknown", "40", "35",
     "5", "20", "Andrews", "Andrews +5", "second Citadel sample (RV), same field window"),
    ("Impact Research", "Impact Research (D)", "2026-10-15", "2026-10-21", "LV", "800", "3.5", "45",
     "44", "5", "5", "Andrews", "Andrews +1", "unknown"),
    ("Trafalgar Group", "Trafalgar Group (R)", "2026-10-16", "2026-10-18", "LV", "1095", "2.9", "46",
     "49", "5", "1", "Graham", "Graham +3", "unknown"),
    ("Rasmussen Reports", "Rasmussen Reports (R)", "2026-10-05", "2026-10-08", "LV", "837", "3.0",
     "45", "49", "unknown", "6", "Graham", "Graham +4", "source shows no third-party column"),
    ("InsiderAdvantage", "InsiderAdvantage (R)", "2026-09-28", "2026-09-29", "LV", "1200", "2.8",
     "45", "46", "5", "4", "Graham", "Graham +1", "unknown"),
    ("Trafalgar Group", "Trafalgar Group (R)", "2026-09-23", "2026-09-25", "LV", "1087", "2.9", "42",
     "43", "6", "9", "Graham", "Graham +1", "unknown"),
    ("Rasmussen Reports", "Rasmussen Reports (R)", "2026-09-14", "2026-09-14", "LV", "1006", "3.0",
     "43", "48", "unknown", "9", "Graham", "Graham +5", "single-day field window"),
    ("InsiderAdvantage", "InsiderAdvantage (R)", "2026-09-08", "2026-09-09", "LV", "1200", "2.8",
     "43", "45", "3", "9", "Graham", "Graham +2", "unknown"),
    ("Abacus Data", "Abacus Data", "2026-08-26", "2026-08-28", "LV", "306", "unknown", "42", "55",
     "3", "unknown", "Graham", "Graham +13", "small LV sample; no MOE published"),
    ("Abacus Data", "Abacus Data", "2026-08-26", "2026-08-28", "RV", "500", "4.4", "48", "47", "5",
     "unknown", "Andrews", "Andrews +1", "second Abacus sample (RV)"),
    ("Impact Research", "Impact Research (D)", "2026-08-18", "2026-08-24", "LV", "700", "3.7", "41",
     "41", "5", "13", "tie", "0", "exact tie in source"),
    ("Impact Research", "Impact Research (D)", "2026-08-14", "2026-08-22", "LV", "900", "3.3", "42",
     "39", "6", "13", "Andrews", "Andrews +3", "unknown"),
]

PRIMARY_POLLS = [
    ("Trafalgar Group", "special_primary", "Trafalgar Group (R)", "2026-08-08", "2026-08-10", "LV",
     "1027", "2.9", "26", "20", "18", "8", "18", "5", "5"),
    ("Quantus Insights", "special_primary", "Quantus Insights (R)", "2026-08-05", "2026-08-07",
     "LV", "668", "4.0", "33", "20", "20", "8", "17", "2", "unknown"),
    ("co/efficient", "special_primary", "co/efficient (R)", "2026-07-28", "2026-07-30", "LV", "857",
     "3.3", "30", "15", "16", "6", "9", "4", "20"),
    ("Trafalgar Group", "special_primary", "Trafalgar Group (R)", "2026-07-28", "2026-07-30", "LV",
     "989", "2.9", "27", "17", "17", "8", "15", "2", "12"),
    ("Emerson College", "special_primary", "Emerson College", "2026-07-28", "2026-07-29", "LV",
     "500", "4.3", "19", "22", "12", "7", "11", "3", "25"),
    ("Trafalgar Group", "runoff", "Trafalgar Group (R)", "2026-08-22", "2026-08-24", "LV", "1031",
     "2.9", "48", "48", "unknown", "unknown", "unknown", "unknown", "4"),
]


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {path}: {len(rows)} rows")


def build_results():
    rows = []
    for race, name, date, block, sec, extra in [
        ("SC-SEN-2026-DEM-PRIMARY", "South Carolina U.S. Senate Democratic primary", "2026-06-09",
         DEM, "45", "total 367,411 votes"),
        ("SC-SEN-2026-GOP-PRIMARY", "South Carolina U.S. Senate Republican primary", "2026-06-09",
         GOP, "16", "total 465,076 votes; Lindsey Graham died 2026-07-11, after this nomination"),
        ("SC-SEN-2026-GOP-SPECIAL-PRIMARY",
         "South Carolina U.S. Senate Republican special primary (first round)", "2026-08-11",
         SPECIAL, "29", "total 335,555 votes; top two advanced to the 2026-08-25 runoff"),
        ("SC-SEN-2026-GOP-RUNOFF", "South Carolina U.S. Senate Republican special primary runoff",
         "2026-08-25", RUNOFF, "35", "total 368,898 votes"),
        ("SC-SEN-2026-GENERAL", "South Carolina U.S. Senate general election", "2026-11-03",
         GENERAL, "57",
         "total 2,041,487 votes; write-in votes are the sum of the county table's write-in column, "
         "and the write-in percentage is derived from that sum"),
    ]:
        for cand, party, votes, pct, winner in block:
            note = extra
            if cand.startswith("Write-in"):
                note = ("write-in votes = sum of the 46 county write-in cells; percentage derived as "
                        "4,899 / 2,041,487 = 0.24 — not a reported figure")
            rows.append([race, name, date, cand, party, votes, pct, winner, WIKI,
                         "partially verified", f"{note}; {VIA.format(n=sec)}"])
    write_csv(os.path.join(OUT, "election_results.csv"), RESULTS_HEADER, rows)


def build_counties():
    src = os.path.join(MIR, "county_results_parsed.csv")
    rows = []

    def total_of(r):
        """The source table writes Edgefield's total as '10.821' — a typo for 10,821.

        Rather than trusting either the typo or a silent correction, the total is derived from
        the five documented component cells whenever they are all integers and the parsed total
        is not; `results_notes.md` records the single row where this applied.
        """
        raw = r["total_votes"]
        if raw.isdigit():
            return raw
        parts = [r["andrews_votes"], r["graham_votes"], r["whitener_votes"], r["hackett_votes"],
                 r["writein_votes"]]
        if all(p.isdigit() for p in parts):
            return str(sum(int(p) for p in parts))
        return "unknown"

    for i, r in enumerate(csv.DictReader(open(src, encoding="utf-8")), start=1):
        def n(k):
            return r[k] if r[k] not in ("", None) else "unknown"
        def add3():
            vals = [r["whitener_votes"], r["hackett_votes"], r["writein_votes"]]
            if all(v.isdigit() for v in vals):
                return str(sum(int(v) for v in vals))
            return "unknown"
        rows.append([f"SC-CNT-{i:03d}", r["county"], n("andrews_votes"), n("graham_votes"),
                     add3(), n("andrews_pct"), n("graham_pct"), total_of(r), WIKI,
                     "partially verified"])
    write_csv(os.path.join(OUT, "county_results.csv"), COUNTY_HEADER, rows)


def build_polls():
    rows = []
    for i, (pollster, sponsor, fs, fe, pop, n, moe, a, g, o, u, leader, margin, note) in enumerate(
            POLLS, start=1):
        rows.append([f"POLL-{i:03d}", pollster, sponsor, fs, fe, pop, n, moe, a, g, o, u, leader,
                     margin, WIKI, "partially verified",
                     f"{note}; {VIA.format(n='56')}"])
    write_csv(os.path.join(OUT, "polling.csv"), POLL_HEADER, rows)


def build_primary_polls():
    rows = []
    for i, (pollster, stage, sponsor, fs, fe, pop, n, moe, g, no, fr, ly, sa, o, u) in enumerate(
            PRIMARY_POLLS, start=1):
        sec = "33" if stage == "runoff" else "27"
        rows.append([f"PPOLL-{i:03d}", stage, pollster, sponsor, fs, fe, pop, n, moe, g, no, fr, ly,
                     sa, o, u, WIKI, "partially verified", VIA.format(n=sec)])
    write_csv(os.path.join(OUT, "primary_polling.csv"), PRIMARY_POLL_HEADER, rows)


def main():
    os.makedirs(OUT, exist_ok=True)
    build_results()
    build_counties()
    build_polls()
    build_primary_polls()
    return 0


if __name__ == "__main__":
    sys.exit(main())
