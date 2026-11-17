#!/usr/bin/env python3
"""Lead QA validator for the south-carolina-senate-2026 archive.

Checks, per CSV:
  - header matches the conventions contract exactly
  - every row has the same field count as the header
  - no blank cells (conventions require explicit 'unknown')
  - controlled-vocabulary values are legal
  - every row carries a source token: 'SRC-####' plus at least one URL
  - date-looking columns match ISO shapes or the literal 'unknown'
  - 'unknown' is lowercase (an uppercase Unknown is a hard failure)
Prints a compact report and exits non-zero if any hard failures are found.

Run: python _staging/_lead_validate.py
"""
import csv
import os
import re
import sys
from collections import Counter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

EVENTS = ("event_id,candidate_id,event_date,event_time,event_title,event_category,city,venue,"
          "state_region,event_status,campaign_phase,stated_purpose,observable_function,"
          "analyst_interpretation,target_audience,main_messages,policy_issues,speech_summary,"
          "transcript_url,video_url,photo_urls,media_coverage,opponent_reference,visual_notes,"
          "source_urls,verification_status,actor_note,vacancy_context,analyst_notes")

CAREER = ("entry_id,candidate_id,start_date,end_date,role_or_event,organization,location,"
          "description,source_urls,verification_status")

POSITIONS = ("position_id,candidate_id,issue,subissue,position_summary,candidate_statement,"
             "statement_date,context,source_urls,legislative_record,position_changed,change_notes,"
             "opponent_criticism,fact_check,verification_status")

SPEECH = ("speech_id,candidate_id,event_id,date,speech_title,speech_url,transcript_url,duration,"
          "main_topics,major_quotes,rhetorical_devices,opponent_references,personal_story_elements,"
          "policy_claims,source_urls,source,verification_status")

VIDEO_INDEX = ("video_id,candidate_id,video_url,date,duration,event_type,main_topics,"
               "relevant_timestamps,transcript_available,visual_observations,completeness,"
               "source_urls,verification_status")

IMAGES = ("image_id,candidate_id,image_date,event_id,event_category,source_name,source_url,"
          "original_image_url,photographer,copyright_status,license,local_filename,image_resolution,"
          "framing,camera_angle,image_quality,face_visibility,body_visibility,clothing_notes,notes,"
          "verification_status")

ADS = ("ad_id,candidate_id,sponsor,sponsor_type,release_date,title,platform,length_seconds,"
       "issue_or_message,main_visual_elements,narration_soundtrack,candidate_appearance,main_claims,"
       "video_url,transcript_url,fact_check,media_coverage,source_urls,verification_status,notes")

SOCIAL = ("post_id,candidate_id,platform,account_handle,post_date,post_type,content_summary,"
          "media_included,engagement_notes,url,verification_status,notes")

MEDIA = ("coverage_id,candidate_id,event_id,publication_date,outlet,author,title,url,source_tier,"
         "coverage_type,key_framing,notable_quotes,framing_of_candidate,mentions_opponent,"
         "reliability_notes")

FINANCE = ("finance_id,candidate_id,period,report_type,reporting_deadline,receipts,"
           "individual_contributions,pac_contributions,disbursements,cash_on_hand,debts_owed,"
           "source_urls,verification_status,notes")

RESULTS = ("race_id,race_name,election_date,candidate,party,votes,percentage,winner,source_urls,"
           "verification_status,notes")

COUNTY = ("county_id,county,candidate_andrews_votes,candidate_graham_votes,other_votes,andrews_pct,"
          "graham_pct,total_votes,source_urls,verification_status")

POLLING = ("poll_id,pollster,sponsor,field_start,field_end,population,sample_size,margin_of_error,"
           "andrews_pct,graham_pct,other_pct,undecided_pct,leader,margin,source_urls,"
           "verification_status,notes")

PRIMARY_POLLING = ("poll_id,race_stage,pollster,sponsor,field_start,field_end,population,"
                   "sample_size,margin_of_error,graham_pct,norman_pct,fry_pct,lynch_pct,"
                   "sanford_pct,other_pct,undecided_pct,source_urls,verification_status,notes")

SOURCES = ("source_id,url,title,publisher,publication_date,event_date,access_date,source_tier,"
           "source_type,relevant_quote_or_info,reliability_notes,used_by")

EXPECTED = {
    "02_campaign_events/campaign_events.csv": EVENTS,
    "01_candidates/policy_positions.csv": POSITIONS,
    "01_candidates/andrews/career_timeline.csv": CAREER,
    "01_candidates/graham/career_timeline.csv": CAREER,
    "03_speeches/speech_archive.csv": SPEECH,
    "03_speeches/speech_video_index.csv": VIDEO_INDEX,
    "04_visual_archive/image_archive.csv": IMAGES,
    "05_campaign_media/advertisements.csv": ADS,
    "05_campaign_media/social_media.csv": SOCIAL,
    "05_campaign_media/media_coverage.csv": MEDIA,
    "06_campaign_finance/campaign_finance.csv": FINANCE,
    "07_electoral_context/election_results.csv": RESULTS,
    "07_electoral_context/county_results.csv": COUNTY,
    "07_electoral_context/polling.csv": POLLING,
    "07_electoral_context/primary_polling.csv": PRIMARY_POLLING,
    "09_sources/sources.csv": SOURCES,
}

CANDIDATES = {"ANDREWS", "GRAHAM"}

VOCAB = {
    "candidate_id": CANDIDATES,
    "event_status": {"held", "cancelled", "postponed", "rescheduled", "virtual", "announced",
                     "unverified", "disputed"},
    "campaign_phase": {"pre_launch", "launch", "primary", "special_primary", "runoff", "general",
                       "early_voting", "gotv", "election_day", "post_election"},
    "state_region": {"Upstate", "Midlands", "Pee Dee", "Lowcountry", "Grand Strand", "statewide",
                     "national", "unknown"},
    "verification_status": {"verified", "partially verified", "unverified", "conflicting sources"},
    "source_tier": {"T1", "T2", "T3"},
    "source_type": {"official_campaign", "official_government", "candidate_social", "news_article", "encyclopedia", "government_record", "social_media", "unknown",
                    "news_video", "transcript", "op_ed", "fact_check", "poll", "press_release",
                    "event_page", "photo", "podcast", "other"},
    "coverage_type": {"news_report", "analysis", "op_ed", "fact_check", "interview", "live_blog",
                      "newsletter", "news_video"},
    "sponsor_type": {"candidate_campaign", "authorized_committee", "outside_pac", "party_committee",
                     "unknown"},
    "completeness": {"full", "partial", "clip", "unknown"},
    "copyright_status": {"public_domain", "licensed", "all_rights_reserved_link_only", "unknown"},
    "opponent_reference": {"yes", "no", "unknown"},
    "vacancy_context": {"pre_vacancy", "vacancy", "post_appointment", "post_runoff", "general",
                        "unknown"},
    "winner": {"yes", "no", "unknown"},
    "mentions_opponent": {"yes", "no", "unknown"},
    "position_changed": {"yes", "no", "unknown"},
    "transcript_available": {"yes", "no", "unknown"},
}

ISSUE = {"Economy", "Healthcare", "Education", "Immigration", "Abortion", "Gun policy", "Energy",
         "Religion", "Labor", "Democracy", "Foreign policy", "Other"}

DATE_FIELDS = {"event_date", "statement_date", "date", "image_date", "release_date", "post_date",
               "publication_date", "reporting_deadline", "start_date", "end_date", "field_start",
               "field_end", "election_date", "publication_date", "event_date", "access_date"}

DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d{4}-\d{2}|\d{4}|unknown)$")
SRC_RE = re.compile(r"SRC-\d{4}")
URL_RE = re.compile(r"https?://")

# per-file fields that are exempt from the SRC-token requirement (see conventions)
SRC_EXEMPT = {
    "01_candidates/andrews/career_timeline.csv": set(),
    "01_candidates/graham/career_timeline.csv": set(),
}


def header_of(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        first = f.readline()
    return first.rstrip("\r\n")


def main():
    hard = 0
    soft = 0
    warnings = []

    for relp, exp in EXPECTED.items():
        path = os.path.normpath(os.path.join(ROOT, relp))
        if not os.path.exists(path):
            print(f"[MISSING ] {relp}")
            hard += 1
            continue

        with open(path, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        if not rows:
            print(f"[EMPTY   ] {relp}")
            hard += 1
            continue

        got = ",".join(rows[0])
        if got != exp:
            print(f"[HEADER  ] {relp}")
            print(f"    expected: {exp}")
            print(f"    found   : {got}")
            hard += 1
            continue

        cols = rows[0]
        idx = {name: i for i, name in enumerate(cols)}
        nrows = 0
        for rn, row in enumerate(rows[1:], start=2):
            if not row:
                continue
            nrows += 1
            if len(row) != len(cols):
                print(f"[COLS    ] {relp}:{rn} has {len(row)} fields, expected {len(cols)}")
                hard += 1
                continue
            for name, i in idx.items():
                val = row[i]
                if val.strip() == "":
                    print(f"[BLANK   ] {relp}:{rn} field '{name}' is empty")
                    hard += 1
                if val == "Unknown" or val == "UNKNOWN":
                    print(f"[CASE    ] {relp}:{rn} field '{name}' must be lowercase 'unknown'")
                    hard += 1
                if name in VOCAB and val not in VOCAB[name]:
                    if name == "candidate_id" and val not in CANDIDATES:
                        print(f"[VOCAB   ] {relp}:{rn} candidate_id='{val}'")
                        hard += 1
                    elif name != "candidate_id":
                        print(f"[VOCAB   ] {relp}:{rn} {name}='{val}' not in vocabulary")
                        hard += 1
                if name == "issue" and val not in ISSUE:
                    print(f"[VOCAB   ] {relp}:{rn} issue='{val}'")
                    hard += 1
                if name in DATE_FIELDS and val != "unknown" and not DATE_RE.match(val):
                    print(f"[DATE    ] {relp}:{rn} {name}='{val}' is not ISO or 'unknown'")
                    hard += 1

            # source token requirement (sources.csv registers ids, it does not cite them)
            if relp == "09_sources/sources.csv":
                continue
            src_cell = None
            for cand in ("source_urls", "source_url", "url", "speech_url", "video_url"):
                if cand in idx:
                    src_cell = row[idx[cand]]
                    if SRC_RE.search(src_cell or ""):
                        break
            else:
                src_cell = src_cell or ""
            if not SRC_RE.search(src_cell or ""):
                print(f"[SOURCE  ] {relp}:{rn} has no SRC-#### token")
                hard += 1
            elif not URL_RE.search(src_cell or ""):
                warnings.append(f"{relp}:{rn} SRC token without a raw URL in the same cell")
                soft += 1

        print(f"[OK      ] {relp}: {nrows} rows")

    # sources.csv sanity: unique ids, block consistency
    spath = os.path.normpath(os.path.join(ROOT, "09_sources/sources.csv"))
    if os.path.exists(spath):
        with open(spath, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        ids = [r[0] for r in rows[1:] if r]
        dupes = [k for k, v in Counter(ids).items() if v > 1]
        if dupes:
            print(f"[DUPE    ] sources.csv duplicate ids: {dupes[:10]}")
            hard += len(dupes)
        print(f"[OK      ] 09_sources/sources.csv: {len(ids)} unique sources")

    if warnings:
        print("\nSoft warnings (first 10):")
        for w in warnings[:10]:
            print("  -", w)

    print(f"\nHard failures: {hard}   Soft warnings: {len(warnings)}")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
