# -*- coding: utf-8 -*-
"""campaign_finance.csv, election_results.csv, county_results.csv, polling.csv."""
import csv
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CASE, S, URL, KEY, write

FIN = ["finance_id", "candidate_id", "period", "report_type", "reporting_deadline", "receipts",
       "individual_contributions", "pac_contributions", "disbursements", "cash_on_hand", "debts_owed",
       "source_urls", "verification_status", "notes"]

RT = "FEC campaign-finance snapshot"
NOTE = "Figures transcribed from the FEC summary table as reproduced by the race article; the underlying FEC page returned HTTP 403 to this archive."

rows = [
    ["TUR-FIN-0001", "TUREK", "2026-Q1", RT, "unknown", 2808701, "unknown", "unknown", 2051221, 757480,
     "unknown", S("wiki"), "partially verified",
     "Pre-primary snapshot dated 2026-04-18. " + NOTE],
    ["TUR-FIN-0002", "TUREK", "2026-Q3", RT, "unknown", 24290521, "unknown", "unknown", 21217670,
     3072851, "unknown", S("wiki"), "partially verified",
     "Snapshot dated 2026-10-14. " + NOTE],
    ["HIN-FIN-0001", "HINSON", "2026-Q1", RT, "unknown", 7267266, "unknown", "unknown", 2679198,
     6516143, "unknown", S("wiki"), "partially verified",
     "Pre-primary snapshot dated 2026-04-18. " + NOTE],
    ["HIN-FIN-0002", "HINSON", "2026-Q3", RT, "unknown", 14147973, "unknown", "unknown", 13903059,
     2172989, "unknown", S("wiki"), "partially verified",
     "Snapshot dated 2026-10-14. " + NOTE],
    ["CAR-FIN-0001", "CARLIN", "2026-Q1", RT, "unknown", 293966, "unknown", "unknown", 279387, 14578,
     "unknown", S("wiki"), "partially verified",
     "Republican primary rival, pre-primary snapshot. " + NOTE],
    ["ERN-FIN-0001", "ERNST", "2026-Q1", RT, "unknown", 6954692, "unknown", "unknown", 5485942,
     1997164, "unknown", S("wiki"), "partially verified",
     "The retiring incumbent's committee, not a 2026 Senate campaign. " + NOTE],
    ["WAH-FIN-0001", "WAHLS", "2026-Q1", RT, "unknown", 3167670, "unknown", "unknown", 2112265,
     1055405, "unknown", S("wiki"), "partially verified",
     "Democratic primary rival. " + NOTE],
    ["SAG-FIN-0001", "SAGE", "2026-Q1", RT, "unknown", 1432562, "unknown", "unknown", 1432459, 102,
     "unknown", S("wiki"), "partially verified",
     "Withdrawn Democratic candidate whose spending nearly equalled receipts. " + NOTE],
    ["NOR-FIN-0001", "NORRIS", "2026-Q1", RT, "unknown", 363563, "unknown", "unknown", 363563, 0,
     "unknown", S("wiki"), "partially verified", "Withdrawn Democratic candidate. " + NOTE],
    ["SCH-FIN-0001", "SCHOLTEN", "2026-Q1", RT, "unknown", 213415, "unknown", "unknown", 205271, 8144,
     "unknown", S("wiki"), "partially verified", "Withdrawn Democratic candidate. " + NOTE],
    ["LAE-FIN-0001", "LAEHN", "2026-Q3", RT, "unknown", 83667, "unknown", "unknown", 74632, 9035,
     "unknown", S("wiki"), "partially verified",
     "Libertarian nominee, snapshot dated 2026-10-14. " + NOTE],
]
write("06_campaign_finance/campaign_finance.csv", FIN, rows)

# ------------------------------- election results -------------------------------
ER = ["race_id", "race_name", "election_date", "candidate", "party", "votes", "percentage", "winner",
      "source_urls", "verification_status", "notes"]

ER_ROWS = [
    ["IA-SEN-2026-R-PRI", "Republican primary for U.S. Senate in Iowa", "2026-06-02", "Ashley Hinson",
     "Republican", 153059, 74.2, "yes", S("wiki"), "verified",
     "Election-box figures; the night-of projection reported 74% to 26%."],
    ["IA-SEN-2026-R-PRI", "Republican primary for U.S. Senate in Iowa", "2026-06-02", "Jim Carlin",
     "Republican", 53196, 25.8, "no", S("wiki"), "verified",
     "Rounded percentages sum to 100.0; votes sum to the published total of 206,255."],
    ["IA-SEN-2026-D-PRI", "Democratic primary for U.S. Senate in Iowa", "2026-06-02", "Josh Turek",
     "Democratic", 120287, 62.7, "yes", S("wiki"), "verified",
     "The night-of count with 99% reporting was reported as 62.6% to 37.4%."],
    ["IA-SEN-2026-D-PRI", "Democratic primary for U.S. Senate in Iowa", "2026-06-02", "Zach Wahls",
     "Democratic", 71663, 37.3, "no", S("wiki"), "verified",
     "Votes sum to the published total of 191,950."],
    ["IA-SEN-2026-GEN", "2026 United States Senate election in Iowa", "2026-11-03", "Josh Turek",
     "Democratic", 688746, 50.56, "yes", S("nbcapi"), "verified",
     "NBC News results feed; matches the reported total of 1,362,337."],
    ["IA-SEN-2026-GEN", "2026 United States Senate election in Iowa", "2026-11-03", "Ashley Hinson",
     "Republican", 631482, 46.35, "no", S("nbcapi"), "verified",
     "Margin 4.21 points."],
    ["IA-SEN-2026-GEN", "2026 United States Senate election in Iowa", "2026-11-03", "Thomas Laehn",
     "Libertarian", 42109, 3.09, "no", S("nbcapi"), "verified",
     "Libertarian nominee; qualified by petition after submitting nearly 10,000 signatures on 2026-06-02."],
]
write("07_electoral_context/election_results.csv", ER, ER_ROWS)

# ------------------------------- county results -------------------------------
raw = json.load(io.open(os.path.join(CASE, "_staging/mirrors/api_nbc_iowa_senate.json"), encoding="utf-8"))
areas = []
for race in raw["page"]["races"] if "races" in raw["page"] else []:
    if race.get("areas"):
        areas = race["areas"]
if not areas:
    # search deeper
    def find(o):
        if isinstance(o, dict):
            if "areas" in o and isinstance(o["areas"], list) and o["areas"]:
                return o["areas"]
            for v in o.values():
                r = find(v)
                if r:
                    return r
        elif isinstance(o, list):
            for v in o:
                r = find(v)
                if r:
                    return r
        return None
    areas = find(raw)
print("areas:", len(areas))

CROWS = []
tot_a = tot_b = tot_o = 0
for a in sorted(areas, key=lambda x: x["name"]):
    votes = {c["name"]: c["votes"] for c in a["candidates"]}
    ta = votes.get("Josh Turek", 0)
    hb = votes.get("Ashley Hinson", 0)
    other = a["votes"] - ta - hb
    tot_a += ta
    tot_b += hb
    tot_o += other
    pa = round(ta / a["votes"] * 100, 2)
    pb = round(hb / a["votes"] * 100, 2)
    CROWS.append(["IA-" + a["name"].upper().replace(" ", "_"), a["name"], ta, hb, other, pa, pb,
                  a["votes"], S("nbcapi"), "verified"])

write("07_electoral_context/county_results.csv",
      ["county_id", "county", "turek_votes", "hinson_votes", "other_votes", "turek_pct", "hinson_pct",
       "total_votes", "source_urls", "verification_status"], CROWS)
print("county sums: turek", tot_a, "hinson", tot_b, "other", tot_o, "total", tot_a + tot_b + tot_o)

# ------------------------------- polling -------------------------------
POLL = ["poll_id", "pollster", "sponsor", "field_start", "field_end", "population", "sample_size",
        "margin_of_error", "turek_pct", "hinson_pct", "other_pct", "undecided_pct", "leader", "margin",
        "source_urls", "verification_status", "notes"]

P = [
    ["POLL-0001", "AtlasIntel", "unknown", "2026-10-28", "2026-11-01", "likely voters", 1219, 3.0,
     51, 46, 3, 0, "Turek", 5, S("wiki"), "partially verified",
     "Final pre-election poll in the race article's table; 'other' includes Laehn."],
    ["POLL-0002", "The New York Times/Siena College", "unknown", "2026-10-26", "2026-11-01",
     "likely voters", 705, 4.7, 48, 47, 0, 5, "Turek", 1, S("wiki"), "partially verified",
     "Table lists 0 for other; undecided 5."],
    ["POLL-0003", "GrayHouse", "unknown", "2026-10-28", "2026-10-31", "likely voters", 601, 4.0,
     46, 48, 2, 4, "Hinson", 2, S("wiki"), "partially verified",
     "Republican-linked firm per the race article's table notes (not stated in the row itself)."],
    ["POLL-0004", "Rasmussen Reports", "unknown", "2026-10-27", "2026-10-31", "likely voters", 901, 3.0,
     46, 47, 3, 5, "Hinson", 1, S("wiki"), "partially verified", "Automated telephone poll."],
    ["POLL-0005", "YouGov", "unknown", "2026-10-26", "2026-10-29", "likely voters", 2020, 3.1,
     50, 49, 1, 0, "Turek", 1, S("wiki"), "partially verified", "Online panel."],
    ["POLL-0006", "co/efficient", "unknown", "2026-10-28", "2026-10-28", "likely voters", 1020, 3.1,
     46, 48, 1, 5, "Hinson", 2, S("wiki"), "partially verified", "Single-day field."],
    ["POLL-0007", "Echelon Insights", "unknown", "2026-10-16", "2026-10-23", "likely voters", 403, 6.5,
     45, 43, 7, 3, "Turek", 2, S("wiki"), "partially verified",
     "Smallest sample in the table; 7% other is consistent with the Laehn vote share."],
    ["POLL-0008", "InsiderAdvantage", "unknown", "2026-10-21", "2026-10-22", "likely voters", 1200, 2.8,
     45, 47, "unknown", 8, "Hinson", 2, S("wiki"), "partially verified",
     "Other not reported (dash in the table), so recorded as unknown."],
    ["POLL-0009", "co/efficient", "unknown", "2026-10-15", "2026-10-19", "likely voters", 863, 3.3,
     45, 48, 2, 6, "Hinson", 3, S("wiki"), "partially verified", "Second co/efficient field in October."],
    ["POLL-0010", "Emerson College", "unknown", "2026-08-31", "2026-09-01", "likely voters", 750, 3.6,
     45, 50, 1, 5, "Hinson", 5, S("wiki"), "partially verified",
     "Late-summer poll before the debates."],
    ["POLL-0011", "Global Strategy Group", "unknown", "2026-08-27", "2026-08-31", "likely voters", 800,
     3.5, 46, 42, 6, 6, "Turek", 4, S("wiki"), "partially verified",
     "Democratic-linked firm per the race article's table notes; the only August poll showing Turek ahead."],
]
write("07_electoral_context/polling.csv", POLL, P)
print("done")
