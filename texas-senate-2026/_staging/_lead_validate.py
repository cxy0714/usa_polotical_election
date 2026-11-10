"""Lead QA validator for the texas-senate-2026 archive.

Checks, per CSV:
  - header matches the conventions contract exactly
  - every row has the same field count as the header
  - no blank cells (conventions require explicit 'unknown')
  - controlled-vocabulary values are legal
Prints a compact report and exits non-zero if any hard failures are found.
"""
import csv
import os
import sys
from collections import Counter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

EXPECTED = {
    "02_campaign_events/campaign_events.csv": "event_id,candidate_id,event_date,event_time,event_title,event_category,city,venue,state_region,event_status,campaign_phase,stated_purpose,observable_function,analyst_interpretation,target_audience,main_messages,policy_issues,speech_summary,transcript_url,video_url,photo_urls,media_coverage,opponent_reference,visual_notes,source_urls,verification_status,analyst_notes",
    "02_campaign_events/../01_candidates/policy_positions.csv": "position_id,candidate_id,issue,subissue,position_summary,candidate_statement,statement_date,context,source_urls,legislative_record,position_changed,change_notes,opponent_criticism,fact_check,verification_status",
    "03_speeches/speech_archive.csv": "speech_id,candidate_id,event_id,date,speech_title,speech_url,transcript_url,duration,main_topics,major_quotes,rhetorical_devices,opponent_references,personal_story_elements,policy_claims,source_urls,source,verification_status",
    "03_speeches/speech_video_index.csv": "video_id,candidate_id,video_url,date,duration,event_type,main_topics,relevant_timestamps,transcript_available,visual_observations,completeness,source_urls,verification_status",
    "04_visual_archive/image_archive.csv": "image_id,candidate_id,image_date,event_id,event_category,source_name,source_url,original_image_url,photographer,copyright_status,license,local_filename,image_resolution,framing,camera_angle,image_quality,face_visibility,body_visibility,clothing_notes,notes,verification_status",
    "05_campaign_media/advertisements.csv": "ad_id,candidate_id,sponsor,sponsor_type,release_date,title,platform,length_seconds,issue_or_message,main_visual_elements,narration_soundtrack,candidate_appearance,main_claims,video_url,transcript_url,fact_check,media_coverage,source_urls,verification_status,notes",
    "05_campaign_media/social_media.csv": "post_id,candidate_id,platform,account_handle,post_date,post_type,content_summary,media_included,engagement_notes,url,verification_status,notes",
    "05_campaign_media/media_coverage.csv": "coverage_id,candidate_id,event_id,publication_date,outlet,author,title,url,source_tier,coverage_type,key_framing,notable_quotes,framing_of_candidate,mentions_opponent,reliability_notes",
    "06_campaign_finance/campaign_finance.csv": "finance_id,candidate_id,period,report_type,reporting_deadline,receipts,individual_contributions,pac_contributions,disbursements,cash_on_hand,debts_owed,source_urls,verification_status,notes",
    "07_electoral_context/election_results.csv": "race_id,race_name,election_date,candidate,party,votes,percentage,winner,source_urls,verification_status,notes",
    "07_electoral_context/county_results.csv": "county_id,county,candidate_talarico_votes,candidate_paxton_votes,other_votes,talarico_pct,paxton_pct,total_votes,source_urls,verification_status",
    "07_electoral_context/polling.csv": "poll_id,pollster,sponsor,field_start,field_end,population,sample_size,margin_of_error,talarico_pct,paxton_pct,other_pct,undecided_pct,leader,margin,source_urls,verification_status,notes",
}

# field -> allowed values (None = unconstrained)
VOCAB = {
    "candidate_id": {"TALARICO", "PAXTON"},
    "event_status": {"held", "cancelled", "postponed", "rescheduled", "virtual", "announced", "unverified", "disputed"},
    "campaign_phase": {"pre_launch", "launch", "primary", "runoff", "general", "early_voting", "gotv", "election_day", "post_election"},
    "verification_status": {"verified", "partially verified", "unverified", "conflicting sources"},
    "source_tier": {"T1", "T2", "T3"},
    "coverage_type": {"news_report", "analysis", "op_ed", "fact_check", "interview", "live_blog", "newsletter", "news_video"},
    "sponsor_type": {"candidate_campaign", "authorized_committee", "outside_pac", "party_committee", "unknown"},
    "completeness": {"full", "partial", "clip", "unknown"},
    "copyright_status": {"public_domain", "licensed", "all_rights_reserved_link_only", "unknown"},
    "opponent_reference": {"yes", "no", "unknown"},
}

ISSUE = {"Economy", "Healthcare", "Education", "Immigration", "Abortion", "Gun policy",
         "Energy", "Religion", "Labor", "Democracy", "Foreign policy", "Other"}


def main():
    hard = 0
    soft = 0
    for relp, exp_header in EXPECTED.items():
        path = os.path.normpath(os.path.join(ROOT, relp))
        if not os.path.exists(path):
            print(f"[MISSING] {relp}")
            hard += 1
            continue
        with open(path, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        if not rows:
            print(f"[EMPTY] {relp}")
            hard += 1
            continue
        header = rows[0]
        exp = exp_header.split(",")
        if header != exp:
            print(f"[HEADER-MISMATCH] {relp}")
            print(f"   got: {len(header)} cols, expected {len(exp)}")
            for i, (a, b) in enumerate(zip(header, exp)):
                if a != b:
                    print(f"   col {i}: got {a!r} expected {b!r}")
            if len(header) != len(exp):
                print(f"   extra/got: {header[len(exp):]}")
            hard += 1
            continue

        data = rows[1:]
        nfields = len(header)
        bad_rows = 0
        blankish = 0
        vocab_hits = Counter()
        cand = Counter()
        for r_i, row in enumerate(data, start=2):
            if len(row) != nfields:
                if bad_rows < 5:
                    print(f"[FIELDCOUNT] {relp} line {r_i}: {len(row)} fields (expected {nfields})")
                bad_rows += 1
                continue
            rec = dict(zip(header, row))
            for k, v in rec.items():
                if v is None or str(v).strip() == "":
                    blankish += 1
            for k, allowed in VOCAB.items():
                if k in rec:
                    v = (rec[k] or "").strip()
                    if v and v not in allowed:
                        vocab_hits[(k, v)] += 1
            if "candidate_id" in rec:
                cand[(rec["candidate_id"] or "").strip()] += 1
            if "issue" in rec and (rec.get("issue") or "").strip() not in ISSUE:
                vocab_hits[("issue", (rec.get("issue") or "").strip())] += 1

        status = []
        if bad_rows:
            print(f"[FIELDS] {relp}: {bad_rows} row(s) with wrong field count")
            hard += 1
        if blankish:
            print(f"[BLANKS] {relp}: {blankish} blank cell(s) — conventions require explicit 'unknown'")
            soft += 1
        for (k, v), c in vocab_hits.most_common():
            print(f"[VOCAB] {relp}: {k}={v!r} x{c} not in controlled vocabulary")
            soft += 1
        mix = ", ".join(f"{k or 'EMPTY'}={v}" for k, v in cand.items())
        print(f"[OK] {relp}: {len(data)} rows; candidates: {mix or 'n/a'}")
    print(f"\nTOTAL hard failures: {hard}   soft warnings: {soft}")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
