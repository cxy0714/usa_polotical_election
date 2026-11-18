"""Build 01_candidates/{brown,husted}/career_timeline.csv."""
import sys

sys.path.insert(0, "_staging")
from b_common import ref, write_csv  # noqa: E402

FIELDS = ["entry_id", "candidate_id", "start_date", "end_date", "role_or_event",
          "organization", "location", "description", "source_urls", "verification_status"]

BROWN = [
    ("1952-11-09", "1952-11-09", "Born", "—", "Mansfield, Ohio",
     "Sherrod Campbell Brown born in Mansfield, Ohio.", ref("wiki_brown"), "verified"),
    ("1975-01-03", "1983-01-03", "Member, Ohio House of Representatives (61st district)",
     "Ohio House of Representatives", "Ohio",
     "Eight years in the state House before running statewide at age 30.",
     ref("wiki_brown"), "verified"),
    ("1983-01-12", "1991-01-14", "46th Secretary of State of Ohio", "State of Ohio", "Columbus, Ohio",
     "Served two terms under Gov. Dick Celeste; the executive post he later cites in "
     "voting-rights arguments.", ref("wiki_brown", "b4_yahoo_keyissues"), "verified"),
    ("1993-01-03", "2007-01-03", "Member, U.S. House of Representatives (OH-13)",
     "U.S. House of Representatives", "Washington, D.C.",
     "Seven terms representing Ohio's 13th district.", ref("wiki_brown"), "verified"),
    ("2007-01-03", "2025-01-03", "U.S. Senator from Ohio", "U.S. Senate", "Washington, D.C.",
     "Three terms; won in 2006 (56.2%), 2012 (50.7%) and 2018 (53.4%).",
     ref("wiki_brown", "wiki_2024oh"), "verified"),
    ("2015-01-03", "2021-02-03", "Ranking Member, Senate Banking Committee", "U.S. Senate",
     "Washington, D.C.", "Led the Democratic side of the Banking Committee.",
     ref("wiki_brown"), "verified"),
    ("2021-02-03", "2025-01-03", "Chair, Senate Banking Committee", "U.S. Senate",
     "Washington, D.C.", "Chairmanship in the 117th and 118th Congresses; the post that "
     "anchored his Wall Street critique.", ref("wiki_brown", "b4_americanbanker"), "verified"),
    ("2023-02-16", "2023-02-16", "East Palestine derailment response visit", "U.S. Senate",
     "East Palestine, Ohio",
     "Met EPA Administrator Regan, residents and first responders; asked DeWine to declare a "
     "state of emergency.", ref("wiki_eastpal"), "verified"),
    ("2023-03-01", "2023-03-01", "Co-sponsored the bipartisan Railway Safety Act",
     "U.S. Senate", "Washington, D.C.",
     "With JD Vance, after the Norfolk Southern derailment; the bill did not pass.",
     ref("wiki_vance", "wiki_eastpal"), "verified"),
    ("2024-11-05", "2024-11-05", "Lost re-election to Bernie Moreno", "U.S. Senate", "Ohio",
     "Defeated after three terms — the loss that set up the 2026 comeback.",
     ref("wiki_2024oh"), "verified"),
    ("2025-01-03", "2025-01-03", "Left the Senate", "U.S. Senate", "Washington, D.C.",
     "Term ended with the 118th Congress.", ref("wiki_brown"), "verified"),
    ("2025-03-25", "2025-03-25", "Launched the Dignity of Work Institute", "Dignity of Work Institute",
     "unknown", "Nonprofit to advocate for workers' policy interests; announced at a Monday "
     "press conference (2025-03-24).", ref("ocj36_former_ohio_u_s_sen_sherrod_brown_launch"),
     "verified"),
    ("2025-08-18", "2025-08-18", "Announced candidacy in the 2026 Senate special election",
     "Sherrod Brown for Ohio", "Ohio",
     "Entered the race against appointed Sen. Jon Husted.", ref("ref063_www_newsandsentinel"),
     "verified"),
    ("2026-05-05", "2026-05-05", "Won the Democratic primary", "Ohio Democratic Party", "Ohio",
     "712,106 votes (89.40%) to Ron Kincaid's 84,405 (10.60%).",
     ref("ocj08_brown_wins_ohio_dem_u_s_senate_primary", "wiki_ohio"), "verified"),
    ("2026-11-03", "2026-11-03", "Won the U.S. Senate special election", "Sherrod Brown for Ohio",
     "Ohio", "2,302,669 votes (50.01%) to Husted's 2,080,064 (45.17%).",
     ref("wiki_ohio", "b4_herald_ap"), "verified"),
    ("2026-12-15", "2026-12-15", "Assumes office for the remainder of the term", "U.S. Senate",
     "Washington, D.C.",
     "Date given in the Wikipedia infobox as the start of the new Senate term; consistent with "
     "Ohio's December 15 transition rule for appointed seats.",
     ref("wiki_brown", "wiki_ohio"), "partially verified"),
]

HUSTED = [
    ("1967-08-25", "1967-08-25", "Born", "—", "Royal Oak, Michigan",
     "Jon Allen Husted born; raised in northwest Ohio; University of Dayton BA and MA.",
     ref("wiki_husted"), "verified"),
    ("2001-01-08", "2009-01-04", "Member, Ohio House of Representatives (41st district)",
     "Ohio House of Representatives", "Ohio",
     "Two terms; led the largest income-tax cut in Ohio history at the time.",
     ref("wiki_husted"), "verified"),
    ("2005-01-03", "2009-01-04", "99th Speaker of the Ohio House", "Ohio House of Representatives",
     "Columbus, Ohio", "Speaker for two General Assemblies; expanded school choice.",
     ref("wiki_husted"), "verified"),
    ("2009-01-05", "2011-01-09", "Member, Ohio Senate (6th district)", "Ohio Senate", "Ohio",
     "One term before running for secretary of state.", ref("wiki_husted"), "verified"),
    ("2011-01-10", "2019-01-14", "50th Secretary of State of Ohio", "State of Ohio",
     "Columbus, Ohio", "Two terms as Ohio's chief elections officer — the credential he "
     "leans on for the SAVE Act and photo-ID push.", ref("wiki_husted", "b4_yahoo_keyissues"),
     "verified"),
    ("2019-01-14", "2025-01-21", "66th Lieutenant Governor of Ohio", "State of Ohio",
     "Columbus, Ohio",
     "Six years under Gov. Mike DeWine; recruited data centers and chaired JobsOhio-related "
     "economic development.", ref("wiki_husted", "wiki_ohio"), "verified"),
    ("2025-01-10", "2025-01-10", "JD Vance resigns the Senate seat", "U.S. Senate",
     "Washington, D.C.", "Vacancy effective 2025-01-10, before Vance's inauguration as vice "
     "president; Gov. DeWine then chose an appointee.",
     ref("ref001_www_nbc4i_com_news_politics_sen_j_d_vance_to_resi", "wiki_vance"), "verified"),
    ("2025-01-17", "2025-01-17", "Appointment announced by Gov. Mike DeWine", "State of Ohio",
     "Columbus, Ohio", "DeWine announced Husted as the appointee at a Statehouse press "
     "conference: \"I wanted someone who knew Ohio.\"",
     ref("ocj25_ohio_lt_gov_jon_husted_to_replace_jd_vance_in_u_s_senat"), "verified"),
    ("2025-01-21", "2025-01-21", "Sworn in as U.S. Senator", "U.S. Senate", "Washington, D.C.",
     "Oath administered by JD Vance; the Commons photograph is dated 2025-01-21.",
     ref("husted_sworn_in_2025", "ref001_www_nbc4i_com_news_politics_sen_j_d_vance_to_resi"),
     "verified"),
    ("2025-04-09", "2025-04-09", "Launched his 2026 Senate campaign", "Jon Husted for U.S. Senate",
     "Ohio", "Launch framed around Trump's endorsement, which came the same day.",
     ref("ref014_web_archive_org_web_20250410091543_https_apnews_com_art",
         "ref015_spectrumnews1_com_oh_cincinnati_news_2025_04_09_trump_e"), "verified"),
    ("2026-01-22", "2026-01-22", "Testified against the abortion pill at a HELP Committee hearing",
     "U.S. Senate HELP Committee", "Washington, D.C.",
     "Cited his own adoption story; the hearing premise was contested by Democrats.",
     ref("ocj35_ohio_republican_us_sen_jon_husted_speaks_against_aborti"), "verified"),
    ("2026-03-11", "2026-03-11", "Testified in the FirstEnergy corruption trial",
     "U.S. District Court (Southern District of Ohio)", "unknown",
     "Appeared after being unable to testify in person on 2026-03-09; distanced himself from "
     "FirstEnergy executives the next day.",
     ref("ocj16_ohio_republican_u_s_sen_jon_husted_testifies_in_firsten",
         "ocj18_ohio_republican_u_s_sen_jon_husted_distanced_himself"), "verified"),
    ("2026-05-05", "2026-05-05", "Won the Republican primary unopposed", "Ohio Republican Party",
     "Ohio", "736,413 votes, 100% of the Republican primary vote.",
     ref("wiki_ohio"), "verified"),
    ("2026-07-27", "2026-07-27", "Senate floor remarks on photo ID for voting", "U.S. Senate",
     "Washington, D.C.", "Recording archived on Commons; part of the SAVE Act push.",
     ref("wiki_husted"), "verified"),
    ("2026-10-14", "2026-10-14", "Campaign-finance report filed (through 2026-09-30)",
     "Jon Husted for U.S. Senate", "Ohio",
     "Raised $19,894,786, spent $15,655,689, $4,239,097 cash on hand.",
     ref("wiki_ohio", "ref047_www_fec_gov_data_elections_senate_OH_2026"), "verified"),
    ("2026-11-03", "2026-11-03", "Lost the special election", "Jon Husted for U.S. Senate",
     "Ohio", "2,080,064 votes (45.17%) to Brown's 2,302,669 (50.01%).",
     ref("wiki_ohio", "b4_herald_ap"), "verified"),
    ("2026-12-15", "2026-12-15", "Term as appointed senator ends", "U.S. Senate",
     "Washington, D.C.", "Ohio's December 15 transition rule; Brown succeeds him.",
     ref("wiki_brown", "wiki_ohio"), "partially verified"),
]


def main():
    for cid, data, path in (("BROWN", BROWN, "01_candidates/brown/career_timeline.csv"),
                            ("HUSTED", HUSTED, "01_candidates/husted/career_timeline.csv")):
        rows = []
        for i, (sd, ed, role, org, loc, desc, src, ver) in enumerate(data, 1):
            rows.append(dict(entry_id=f"{cid[:2]}-CT-{i:02d}", candidate_id=cid,
                             start_date=sd, end_date=ed, role_or_event=role,
                             organization=org, location=loc, description=desc,
                             source_urls=src, verification_status=ver))
        write_csv(path, FIELDS, rows)


if __name__ == "__main__":
    main()
