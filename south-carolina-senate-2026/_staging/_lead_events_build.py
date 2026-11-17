#!/usr/bin/env python3
"""Build 02_campaign_events/campaign_events.csv and the two timelines.

Design choice worth stating: the archive would rather ship 32 documented events than 70 rows with
invented venues. Every row is anchored to a date that appears in a retrieved source - the race
article's prose or tables, CBS's results piece, a Commons file description, or a video whose
upload metadata was verified with yt-dlp. Where a venue, time or crowd is absent, the cell is
`unknown`, including rows whose only evidence is that a recording of the candidate exists.

Chinese strings live in `zh_events.json` (UTF-8, authored separately) so this file stays ASCII and
cannot be mangled by a text-mode rewrite.

Run: python _staging/_lead_events_build.py
"""
import csv
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "02_campaign_events")
ZH = json.load(open(os.path.join(HERE, "zh_events.json"), encoding="utf-8"))

WIKI = "SRC-2108|https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_South_Carolina"
CBS = "SRC-2111|https://www.cbsnews.com/news/south-carolina-2026-senate-annie-andrews-darline-graham/"
DEBATE = "SRC-2113|https://www.youtube.com/watch?v=cXE2Ik6YxMg"
CM = "SRC-0600|https://commons.wikimedia.org/wiki/File%3A"
GREENVILLE = "SRC-0600|https://commons.wikimedia.org/wiki/File%3AAnnie_Andrews_Greenville_%28cropped_2%29.jpg"
GASGRITS = "SRC-0600|https://commons.wikimedia.org/wiki/File%3AAnnie_Andrews_at_Gas%2C_Grits_and_Groceries_Tour_in_Abbeville_%282026%29_%28cropped%29.jpg"
FORTMILL = "SRC-0600|https://commons.wikimedia.org/wiki/File%3AAnnie_Andrews_Fort_Mill_2026_%28cropped_3%29.png"
MEDIA = "SRC-1140|https://commons.wikimedia.org/wiki/File%3A"

HEADER = ["event_id", "candidate_id", "event_date", "event_time", "event_title", "event_category",
          "city", "venue", "state_region", "event_status", "campaign_phase", "stated_purpose",
          "observable_function", "analyst_interpretation", "target_audience", "main_messages",
          "policy_issues", "speech_summary", "transcript_url", "video_url", "photo_urls",
          "media_coverage", "opponent_reference", "visual_notes", "source_urls",
          "verification_status", "actor_note", "vacancy_context", "analyst_notes"]

E = []


def ev(eid, cand, date, title, cat, city, region, phase, stated, observable, interp, message,
       issues, video, src, verif, actor, vacancy, notes, time="unknown", venue="unknown",
       status="held"):
    E.append([eid, cand, date, time, title, cat, city, venue, region, status, phase, stated,
              observable, interp, "unknown", message, issues, "unknown", "unknown", video,
              "unknown", "unknown", "unknown", "unknown", src, verif, actor, vacancy, notes])


def build():
    ev("GRA-EVT-0001", "GRAHAM", "2025-01-14", "Lindsey Graham announces he will seek a fourth term",
       "announcement", "unknown", "unknown", "pre_launch",
       "seek re-election to the U.S. Senate", "public announcement by the incumbent",
       "INTERPRETATION: opens the cycle the November 2026 ballot is eventually built on",
       "unknown", "unknown", "unknown", WIKI, "partially verified", "LINDSEY_GRAHAM",
       "pre_vacancy", "the incumbent, not the eventual nominee; kept because the vacancy starts here")
    ev("GRA-EVT-0002", "GRAHAM", "2025-03-26", "Trump endorses Lindsey Graham for re-election",
       "endorsement_event", "unknown", "national", "pre_launch",
       "unknown", "endorsement announced; no venue documented",
       "INTERPRETATION: the endorsement later transfers to his sister, which is why it is logged",
       "unknown", "unknown", "unknown", WIKI, "partially verified", "LINDSEY_GRAHAM",
       "pre_vacancy", "same endorser reappears for Darline Graham in July 2026")

    ev("AND-EVT-0001", "ANDREWS", "2025-05-29", "Launches with the 'Unafraid' video",
       "launch", "unknown", "statewide", "launch",
       "announce a challenge to Lindsey Graham, framed around RFK Jr.'s HHS confirmation",
       "campaign launch video published; a text announcement accompanies it",
       "INTERPRETATION: a launch that leads with a clinical/biographical frame rather than a policy list",
       "healthcare; corruption in Washington", "Healthcare; Democracy",
       "https://www.youtube.com/watch?v=J8wMNLaSNW4", WIKI, "verified", "DARLINE_GRAHAM",
       "pre_vacancy", "video 217 s; venue not applicable (online launch)")
    ev("AND-EVT-0002", "ANDREWS", "2026-05-07", "Face the Nation interview on the Senate bid",
       "interview_tv", "unknown", "national", "primary",
       "unknown", "television interview segment, 315 s",
       "INTERPRETATION: the first sustained national-profile interview of the primary phase",
       "unknown", "Healthcare", "https://www.youtube.com/watch?v=3HrgPQKBmjE", WIKI,
       "partially verified", "DARLINE_GRAHAM", "pre_vacancy", "unknown")
    ev("AND-EVT-0003", "ANDREWS", "2026-05-11", "Campaign event at Greenville Technical College",
       "town_hall", "Greenville", "Upstate", "primary",
       "unknown", "campaign event documented by a Commons photograph description",
       "INTERPRETATION: the earliest located Andrews appearance in the corpus, and the only one in the Upstate with a named venue",
       "unknown", "unknown", "unknown", GREENVILLE,
       "partially verified", "unknown", "pre_vacancy",
       "photograph described as the nominee at a campaign event at Greenville Technical College; no crowd or time recorded")
    ev("AND-EVT-0004", "ANDREWS", "2026-06-09", "Wins the Democratic Senate primary with 61.5%",
       "party_event", "statewide", "statewide", "primary",
       "unknown", "primary held; Andrews 226,075 to Brown 110,962 and Freeman 30,374",
       "INTERPRETATION: a decisive margin that let the campaign turn to the general early",
       "unknown", "unknown", "unknown", WIKI, "partially verified", "unknown", "pre_vacancy",
       "total 367,411 votes")
    ev("GRA-EVT-0003", "GRAHAM", "2026-06-09", "Lindsey Graham wins the Republican primary with 56.8%",
       "party_event", "statewide", "statewide", "primary",
       "unknown", "primary held; Lindsey Graham 264,091 of 465,076",
       "INTERPRETATION: a 28.9% challenger signals a restless primary electorate that the special primary then re-tests",
       "unknown", "unknown", "unknown", WIKI, "partially verified", "LINDSEY_GRAHAM", "pre_vacancy",
       "the nominee dies 32 days later; the result is superseded, not voided")
    ev("AND-EVT-0005", "ANDREWS", "2026-06-10", "Primary-night remarks after winning the nomination",
       "victory_speech", "unknown", "statewide", "primary",
       "unknown", "speech delivered and posted; 245 s",
       "INTERPRETATION: frames the general election while the Republican side still has no nominee",
       "unknown", "unknown", "https://www.youtube.com/watch?v=Gg9vZGDT_-I", WIKI,
       "partially verified", "unknown", "pre_vacancy", "venue unknown")

    ev("GRA-EVT-0004", "GRAHAM", "2026-07-11", "Death of Senator Lindsey Graham announced",
       "memorial", "unknown", "unknown", "special_primary",
       "unknown", "death announced; aortic dissection, aged 71",
       "INTERPRETATION: converts a routine re-election into a vacancy, an appointment and a three-week special primary",
       "unknown", "unknown", "unknown", WIKI, "verified", "LINDSEY_GRAHAM", "vacancy",
       "the structural hinge of the entire race")
    ev("GRA-EVT-0005", "GRAHAM", "2026-07-13", "Gov. McMaster appoints Darline Graham to the vacant seat",
       "appointment_announcement", "Columbia", "Midlands", "special_primary",
       "unknown", "appointment announced by the governor; Trump's endorsement follows",
       "INTERPRETATION: an appointment that is simultaneously the campaign's launch asset and the central line of attack against her",
       "unknown", "unknown", "https://www.youtube.com/watch?v=aHqk0nFu9Hc", WIKI, "verified",
       "DARLINE_GRAHAM", "vacancy", "CBS full video 1,355 s")
    ev("GRA-EVT-0006", "GRAHAM", "2026-07-14", "Ceremonially sworn in by Chuck Grassley",
       "swearing_in", "Washington, D.C.", "national", "special_primary",
       "assume the seat", "swearing-in ceremony; formal oath administered earlier in the chamber",
       "INTERPRETATION: incumbency conferred 112 days before the election",
       "unknown", "unknown", "https://www.youtube.com/watch?v=hgtB3mrkR9Q", WIKI, "verified",
       "DARLINE_GRAHAM", "post_appointment", "CBS video 713 s")
    ev("GRA-EVT-0007", "GRAHAM", "2026-07-20", "Announces a campaign for the full six-year term",
       "launch", "unknown", "statewide", "special_primary",
       "seek election in her own right", "announcement made and covered by CBS",
       "INTERPRETATION: separates the appointment from the electoral claim, but only by nine days",
       "unknown", "unknown", "https://www.youtube.com/watch?v=k5ywQhN6mJ8", WIKI, "verified",
       "DARLINE_GRAHAM", "post_appointment", "259 s")
    ev("GRA-EVT-0008", "GRAHAM", "2026-07-21", "Special-primary filing period opens",
       "filing", "Columbia", "Midlands", "special_primary",
       "unknown", "filing window opened at noon",
       "INTERPRETATION: a three-week campaign compressed by statute",
       "unknown", "unknown", "unknown", WIKI, "verified", "unknown", "post_appointment",
       "closes noon 2026-07-28")

    ev("JNT-EVT-0001", "GRAHAM", "2026-08-03", "Special Republican primary debate, Gray Media",
       "debate", "unknown", "statewide", "special_primary",
       "unknown", "five-candidate debate moderated by Judi Gatson",
       "INTERPRETATION: the first of two bracketing debates before the 08-11 vote",
       "unknown", "unknown", "unknown", WIKI, "partially verified", "DARLINE_GRAHAM",
       "post_appointment", "participants: Fry, Graham, Lynch, Norman, Sanford")
    ev("JNT-EVT-0002", "GRAHAM", "2026-08-04", "Special Republican primary debate, Nexstar Media Group",
       "debate", "unknown", "statewide", "special_primary",
       "unknown", "five-candidate debate moderated by Alicia Barnes and Carolyn Murray",
       "INTERPRETATION: second bracketing debate",
       "unknown", "unknown", "unknown", WIKI, "partially verified", "DARLINE_GRAHAM",
       "post_appointment", "same five participants")
    ev("GRA-EVT-0009", "GRAHAM", "2026-08-07", "Floor remarks in support of the Russia sanctions bill",
       "speech", "Washington, D.C.", "national", "special_primary",
       "support the Lindsey O. Graham Sanctioning Russia and Iran Act",
       "Senate floor remarks delivered; audio and a still exist on Commons",
       "INTERPRETATION: the only documented instance of her using the Senate floor as a campaign instrument",
       "Russia sanctions; Iran", "Foreign policy",
       "https://upload.wikimedia.org/wikipedia/commons/4/4b/Sen._Darline_Graham_Delivers_Floor_Remarks_in_support_of_Russia_Sanctions_Bill.wav",
       "SRC-2302|https://upload.wikimedia.org/wikipedia/commons/4/4b/Sen._Darline_Graham_Delivers_Floor_Remarks_in_support_of_Russia_Sanctions_Bill.wav",
       "partially verified", "DARLINE_GRAHAM", "post_appointment",
       "date from the Commons file description; the bill was S.5025, not the enacted H.R. 5334")
    ev("GRA-EVT-0010", "GRAHAM", "2026-08-11", "Special Republican primary, first round",
       "party_event", "statewide", "statewide", "special_primary",
       "unknown", "Graham 109,881 (32.8%) and Norman 82,627 (24.6%) advance from ten candidates",
       "INTERPRETATION: a plurality, not a majority - the runoff was structurally necessary",
       "unknown", "unknown", "unknown", WIKI, "partially verified", "DARLINE_GRAHAM",
       "post_appointment", "total 335,555 votes")
    ev("GRA-EVT-0011", "GRAHAM", "2026-08-12", "Primary-night speech after advancing to the runoff",
       "speech", "unknown", "statewide", "runoff",
       "unknown", "speech delivered and posted by the campaign; 395 s",
       "INTERPRETATION: the campaign's own account of the runoff begins here",
       "unknown", "unknown", "https://www.youtube.com/watch?v=pDsefMH15mU", WIKI,
       "partially verified", "DARLINE_GRAHAM", "post_appointment", "venue unknown")
    ev("JNT-EVT-0003", "GRAHAM", "2026-08-18", "Republican runoff debate, SCETV/Newsmax",
       "debate", "unknown", "statewide", "runoff",
       "unknown", "one-hour televised debate between Graham and Norman; moderators Greta Van Susteren, Van Hipp Jr. and Gavin Jackson",
       "INTERPRETATION: the only head-to-head of the Republican runoff and the source of the competence framing that followed",
       "unknown", "unknown", "https://www.youtube.com/watch?v=fYbTRsRnT6U", WIKI, "verified",
       "DARLINE_GRAHAM", "post_appointment", "full broadcast 3,494 s")
    ev("GRA-EVT-0012", "GRAHAM", "unknown", "Speaks at a Trump rally in Myrtle Beach",
       "surrogate_event", "Myrtle Beach", "Grand Strand", "runoff",
       "unknown", "Graham speaks before Trump at a rally; videos posted 2026-08-21/22",
       "INTERPRETATION: the endorser becomes a physical surrogate in the runoff's final week",
       "unknown", "unknown", "https://www.youtube.com/watch?v=S1-ywnhmKgI", WIKI,
       "partially verified", "DARLINE_GRAHAM", "post_appointment",
       "rally date not established from the retrieved sources; video upload dates only")
    ev("GRA-EVT-0013", "GRAHAM", "2026-08-25", "Wins the Republican runoff 52.4%-47.6%",
       "party_event", "statewide", "statewide", "runoff",
       "unknown", "Graham 193,486 to Norman 175,412",
       "INTERPRETATION: an 18,074-vote margin that leaves the losing half of the primary electorate unconsolidated",
       "unknown", "unknown", "unknown", WIKI, "partially verified", "DARLINE_GRAHAM",
       "post_runoff", "total 368,898 votes")
    ev("GRA-EVT-0014", "GRAHAM", "2026-08-26", "Runoff-night remarks",
       "speech", "unknown", "statewide", "runoff",
       "unknown", "remarks delivered; NBC News clip 202 s",
       "INTERPRETATION: pivots to the general with the Trump wing intact and the Norman wing not",
       "unknown", "unknown", "https://www.youtube.com/watch?v=NJ6S-9WUHIo", WIKI,
       "partially verified", "DARLINE_GRAHAM", "post_runoff", "venue unknown")
    ev("AND-EVT-0006", "ANDREWS", "2026-08-26", "Live streaming-newscast interview with WBTV",
       "interview_tv", "Charlotte", "unknown", "general",
       "unknown", "studio interview, 320 s",
       "INTERPRETATION: the challenger's media strategy runs through local television rather than national studios in this phase",
       "unknown", "unknown", "https://www.youtube.com/watch?v=kNBDrVT4HS4", WIKI,
       "partially verified", "unknown", "post_runoff", "venue is the WBTV studio")

    ev("AND-EVT-0007", "ANDREWS", "2026-09-04", "Kicks off the 'Gas, Grits & Groceries' statewide tour",
       "tour_launch", "unknown", "statewide", "general",
       "unknown", "tour kickoff covered by SCETV; 719 s of coverage",
       "INTERPRETATION: an economic-message tour launched the week after the Republican runoff settled",
       "cost of living; gas prices", "Economy", "https://www.youtube.com/watch?v=_fBpfLXaYMI",
       WIKI, "partially verified", "unknown", "post_runoff",
       "full tour name recovered from a Commons photograph description of a 2026-09-09 stop")
    ev("AND-EVT-0008", "ANDREWS", "2026-09-09", "A stop on the Gas, Grits & Groceries Tour",
       "tour_stop", "unknown", "unknown", "general",
       "unknown", "tour stop documented by a Commons photograph description",
       "INTERPRETATION: confirms the tour ran through early September in unnamed locations",
       "cost of living; groceries", "Economy", "unknown",
       GASGRITS, "partially verified", "unknown",
       "post_runoff", "the description gives the date but not the town")
    ev("JNT-EVT-0004", "ANDREWS", "2026-10-11", "The only general-election debate, SCETV/SCPR",
       "debate", "unknown", "statewide", "general",
       "unknown", "televised debate with Andrews, Graham and Whitener; moderator Gavin Jackson; 3,549 s",
       "INTERPRETATION: with one encounter and three candidates, the format constrained any direct two-way exchange",
       "economy; Iran; AI; debt", "Economy; Foreign policy", DEBATE, WIKI, "verified", "unknown",
       "post_runoff", "the only general-election debate in the race")
    ev("AND-EVT-0009", "ANDREWS", "2026-10-15", "MS NOW interview on the general-election case",
       "interview_tv", "unknown", "national", "general",
       "unknown", "interview segment, 380 s",
       "INTERPRETATION: national-cable framing of the race as a flip opportunity",
       "unknown", "Healthcare", "https://www.youtube.com/watch?v=DN__FMK9Wjw", WIKI,
       "partially verified", "unknown", "post_runoff", "unknown")
    ev("GRA-EVT-0015", "GRAHAM", "2026-10-21", "Trump campaigns for her in Clemson",
       "surrogate_event", "Clemson", "Upstate", "general",
       "unknown", "the president travels to Clemson to campaign for the appointee",
       "INTERPRETATION: an incumbent relying on a surrogate's pull in a college town in the Upstate, three weeks out",
       "unknown", "unknown", "unknown", WIKI, "partially verified", "DARLINE_GRAHAM",
       "post_runoff", "documented through a Commons photograph caption dated 2026-10-21")
    ev("AND-EVT-0010", "ANDREWS", "2026-11-02", "Town hall in Fort Mill, York County",
       "town_hall", "Fort Mill", "Upstate", "general",
       "unknown", "town hall documented by a Commons photograph description",
       "INTERPRETATION: the last located campaign event before election day",
       "unknown", "unknown", "unknown", FORTMILL,
       "partially verified", "unknown", "post_runoff",
       "York County Democratic Party credited as the photographer")

    ev("AND-EVT-0011", "ANDREWS", "2026-11-03", "General election: Andrews 51.14%, Graham 46.64%",
       "party_event", "statewide", "statewide", "election_day",
       "unknown", "2,041,487 votes cast; Andrews 1,044,001 to Graham 952,191",
       "INTERPRETATION: the first Democratic Senate win in the state since 1998",
       "unknown", "unknown", "unknown", WIKI, "partially verified", "unknown", "general",
       "Whitener 23,585; Hackett 16,811; write-in 4,899")
    ev("AND-EVT-0012", "ANDREWS", "2026-11-04", "Victory speech after the race is projected",
       "victory_speech", "unknown", "statewide", "post_election",
       "unknown", "speech delivered; NBC News 743 s, ABC News 735 s",
       "INTERPRETATION: the acceptance frame emphasises healthcare and corruption rather than the seat's national significance",
       "healthcare; corruption", "Healthcare; Democracy",
       "https://www.youtube.com/watch?v=jjw3a1ZO6j4", CBS, "verified", "unknown", "general",
       "two independent network uploads of the same remarks")
    ev("GRA-EVT-0016", "GRAHAM", "2026-11-04", "Concession speech",
       "concession_speech", "unknown", "statewide", "post_election",
       "unknown", "concession delivered; C-SPAN full video 208 s",
       "INTERPRETATION: a 112-day incumbency ends with a concession rather than a recount demand",
       "unknown", "unknown", "https://www.youtube.com/watch?v=XkIF9umio7M", CBS, "verified",
       "DARLINE_GRAHAM", "general", "no recount or contest documented")


PHASES = {
    "andrews": [
        ("Launch and primary", "\u542f\u52a8\u4e0e\u521d\u9009",
         lambda r: r[10] in ("launch", "primary"), "launch_primary"),
        ("General election", "\u5927\u9009\u9636\u6bb5",
         lambda r: r[10] in ("general", "runoff"), "general"),
        ("Election and aftermath", "\u6295\u7968\u65e5\u4e0e\u4f59\u6ce2",
         lambda r: r[10] in ("election_day", "post_election"), "aftermath"),
    ],
    "graham": [
        ("Pre-vacancy: her brother's cycle",
         "\u7a7a\u7f3a\u4e4b\u524d\uff1a\u5176\u5144\u957f\u7684\u9009\u6218",
         lambda r: r[27] == "pre_vacancy", "prevacancy"),
        ("Vacancy and appointment", "\u7a7a\u7f3a\u4e0e\u4efb\u547d",
         lambda r: r[27] == "vacancy", "vacancy"),
        ("Special primary", "\u7279\u522b\u521d\u9009",
         lambda r: r[27] == "post_appointment" and r[10] in ("special_primary", "filing"),
         "special"),
        ("Runoff", "\u51b3\u9009", lambda r: r[10] == "runoff", "runoff"),
        ("General election", "\u5927\u9009\u9636\u6bb5",
         lambda r: r[27] == "post_runoff" or r[10] in ("general", "post_election"), "general"),
    ],
}

INTROS = {
    "andrews": "Thirteen documented Andrews events. The campaign is thin on dated, located "
               "appearances in the retrieved sources: most of what is documented is a filmed speech, "
               "an interview or a photograph caption, not a rally with a venue. That asymmetry is a "
               "property of the record, not of the campaign.",
    "graham": "Nineteen documented Graham events, in five phases. The first two rows are her "
              "brother's actions, kept because the vacancy sequence starts there; they carry "
              "actor_note = LINDSEY_GRAHAM and are not evidence about her campaign.",
}

TITLES_ZH = {
    "andrews_timeline.md": ("Annie Andrews - campaign timeline",
                            "\u5b89\u59ae\u00b7\u5b89\u5fb7\u9c81\u65af\u2014\u2014\u7ade\u9009\u65f6\u95f4\u7ebf"),
    "graham_timeline.md": ("Darline Graham - campaign timeline",
                           "\u8fbe\u7433\u00b7\u683c\u96f7\u5384\u59c6\u2014\u2014\u7ade\u9009\u65f6\u95f4\u7ebf"),
}


def timeline_md(path, cand):
    key = cand.lower()
    title_en, title_zh = TITLES_ZH[os.path.basename(path)]
    rows = [r for r in E if r[1] == cand]
    rows.sort(key=lambda r: (r[2] == "unknown", r[2]))
    zh = ZH[key]
    lines = ["---", f'title: "{title_en}"', f'title_zh: "{title_zh}"', f"candidate_id: {cand}",
             "compiled_by: Lead Research Agent", "last_updated: 2026-11-12",
             "status: in_progress",
             'coverage_note: "Dates are documented; venues, times and crowd sizes are mostly '
             'unknown. Row-level Chinese glosses cover event titles; the prose is bilingual."',
             "---", "", f"# {title_en} / {title_zh}", "", INTROS[key], "", zh["intro"], ""]
    for head_en, head_zh, test, phase_key in PHASES[key]:
        lines += [f"## {head_en} / {head_zh}", "", zh["phases"][phase_key], "",
                  "| Date / \u65e5\u671f | Event / \u6d3b\u52a8 | Category / \u7c7b\u522b | "
                  "Status / \u72b6\u6001 | Source |", "|---|---|---|---|---|"]
        for r in rows:
            if not test(r):
                continue
            lines.append(f"| {r[2]} | {r[4]} / {ZH['titles'].get(r[0], '(gloss pending)')} | "
                         f"{r[5]} | {r[9]} | [{r[24].split('|')[0]}] |")
        lines.append("")
    lines += ["## Sources / \u6765\u6e90", "",
              "- [SRC-2108] `https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_South_Carolina`",
              "- [SRC-2111] `https://www.cbsnews.com/news/south-carolina-2026-senate-annie-andrews-darline-graham/`",
              ""]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"wrote {path}: {len(rows)} rows")


def gap_md():
    zh = ZH["gap_doc"]
    p = ["---",
         'title: "Event coverage gaps - what the record does not contain"',
         'title_zh: "\u6d3b\u52a8\u8986\u76d6\u7f3a\u53e3\u2014\u2014\u8bb0\u5f55\u4e2d\u4e0d\u5b58\u5728\u7684\u5185\u5bb9"',
         "candidate_id: both", "compiled_by: Lead Research Agent", "last_updated: 2026-11-12",
         "status: complete",
         'coverage_note: "32 events. The shortfall against the 70-row target is a finding about the '
         'sources, not a defect to be padded."',
         "---", "", "# Event coverage gaps / \u6d3b\u52a8\u8986\u76d6\u7f3a\u53e3", "",
         "## 1. Why this file has 32 rows, not 70 / 1. \u4e3a\u4ec0\u4e48\u662f 32 \u884c\u800c\u4e0d\u662f 70 \u884c",
         "",
         "The conventions set a 70-row target. The archive ships 32. The reason is specific: the "
         "retrievable record of this race is dominated by election administration, debates and "
         "televised speeches, and almost never contains a dated, located appearance with a venue, a "
         "time and a crowd. Andrews's campaign calendar was not retrievable at all (her site returns "
         "HTTP 403), and Graham's dated appearances beyond the debates are rallies documented "
         "through video uploads rather than through a campaign schedule.",
         "", zh["p1"], "",
         "Filling the gap with plausible rows would destroy the property that makes the dataset "
         "usable: that every row traces to something retrieved.",
         "", zh["p2"], "",
         "## 2. What is missing, by type / 2. \u6309\u7c7b\u578b\u5217\u51fa\u7684\u7f3a\u5931", "",
         "| Missing / \u7f3a\u5931 | Consequence / \u5f71\u54cd |", "|---|---|",
         "| Campaign event calendars (both sides) | No meet-and-greets, county visits or church appearances; the two town halls are known only from photo captions. |",
         "| Venues and times for speeches | Most rows carry `venue = unknown` and `event_time = unknown`. |",
         "| Crowd sizes | Published in no retrieved source; never estimated here. |",
         "| The Myrtle Beach rally date | Videos uploaded 2026-08-21/22; the event date is not established. |",
         "| Early-voting / GOTV events | A photo documents an early-voting appearance (2026-10-28); no GOTV programme is recorded. |",
         "| Andrews events between 06-10 and 08-26 | The record jumps from the primary-night speech to a WBTV interview. |",
         "",
         "| \u7f3a\u5931 | \u5f71\u54cd |", "|---|---|",
         "| \u53cc\u65b9\u7ade\u9009\u6d3b\u52a8\u65e5\u7a0b | \u9664\u4e24\u573a\u6709\u7167\u7247\u8bb0\u5f55\u7684\u5e02\u653f\u5385\u5916\uff0c\u6ca1\u6709\u89c1\u9762\u4f1a\u3001\u53bf\u57df\u8d70\u8bbf\u6216\u6559\u4f1a\u9732\u9762\u3002 |",
         "| \u8bb2\u8bdd\u7684\u573a\u5730\u4e0e\u65f6\u95f4 | \u591a\u6570\u884c `venue = unknown`\u3001`event_time = unknown`\u3002 |",
         "| \u53c2\u4e0e\u4eba\u6570 | \u4efb\u4f55\u5df2\u68c0\u7d22\u6765\u6e90\u5747\u672a\u516c\u5e03\uff1b\u672c\u6863\u6848\u4ece\u4e0d\u4f30\u7b97\u3002 |",
         "| \u9ed8\u7279\u5c14\u6bd4\u5947\u96c6\u4f1a\u7684\u65e5\u671f | \u89c6\u9891\u4e0a\u4f20\u4e8e 2026-08-21/22\uff1b\u6d3b\u52a8\u65e5\u671f\u672a\u80fd\u786e\u7acb\u3002 |",
         "| \u63d0\u524d\u6295\u7968\uff0f\u50ac\u7968\u6d3b\u52a8 | \u6709\u4e00\u5f20\u7167\u7247\u8bb0\u5f55 2026-10-28 \u7684\u63d0\u524d\u6295\u7968\u9732\u9762\uff0c\u4f46\u6ca1\u6709\u50ac\u7968\u9879\u76ee\u7684\u8bb0\u5f55\u3002 |",
         "| \u5b89\u5fb7\u9c81\u65af\u5728 06-10 \u81f3 08-26 \u4e4b\u95f4\u7684\u6d3b\u52a8 | \u8bb0\u5f55\u4ece\u521d\u9009\u4e4b\u591c\u8bb2\u8bdd\u76f4\u63a5\u8df3\u5230 WBTV \u91c7\u8bbf\u3002 |",
         "",
         "## 3. Asymmetry between the two candidates / 3. \u4e24\u4f4d\u5019\u9009\u4eba\u4e4b\u95f4\u7684\u4e0d\u5bf9\u79f0",
         "",
         "Graham has 19 rows to Andrews's 13, and the imbalance is structural rather than editorial: "
         "the vacancy generated appointment, swearing-in, launch, filing-window, floor remarks and "
         "runoff events with no Democratic counterpart, plus four debates in which she took part.",
         "", zh["p3"], "",
         "## 4. Rows dated by a recording or a caption / 4. \u65e5\u671f\u6765\u81ea\u5f71\u50cf\u6216\u8bf4\u660e\u7684\u884c",
         "",
         "Several rows are dated by the upload date of a video showing the candidate speaking, or by "
         "a Commons file description, not by a campaign schedule. They are `partially verified` for "
         "that reason, and the evidence URL is in `video_url` or `photo_urls`. A human analyst should "
         "treat those dates as 'not earlier than' rather than exact.",
         "", zh["p4"], "",
         "## Sources", "",
         "- [SRC-2108] `https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_South_Carolina`",
         ""]
    path = os.path.join(OUT, "event_coverage_gaps.md")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(p))
    print(f"wrote {path}")


def main():
    build()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "campaign_events.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        w.writerow(HEADER)
        w.writerows(E)
    widths = {len(r) for r in E}
    print(f"{path}: {len(E)} rows, widths {widths}")
    print("  by candidate:", dict(Counter(r[1] for r in E)))
    print("  by category:", dict(Counter(r[5] for r in E)))
    print("  undated:", sum(1 for r in E if r[2] == "unknown"))
    timeline_md(os.path.join(OUT, "andrews_timeline.md"), "ANDREWS")
    timeline_md(os.path.join(OUT, "graham_timeline.md"), "GRAHAM")
    gap_md()
    return 0 if widths == {len(HEADER)} else 1


if __name__ == "__main__":
    sys.exit(main())
