#!/usr/bin/env python3
"""Validate one case archive produced under _research/2026/CASE_CONTRACT.md.

Usage: python _tools/validate_case.py <case-slug-or-path>

Checks, per CSV:
  * file exists, header matches the contract exactly (candidate-key columns from case_meta.json)
  * RFC-4180 row width, no blank cells, no TBD/TODO/N/A placeholders
  * ISO dates in every *date / field_start / field_end column
  * source_urls cells = SRC-####|https://... and every SRC id resolves in 09_sources/sources.csv
  * controlled vocabularies for the enumerated columns
Plus: unique source ids, source tier/type vocabulary, http(s) URLs, downloaded image licence check.
Exit code 1 on any hard failure.
"""
import csv
import json
import os
import re
import sys

SRC_RE = re.compile(r"^SRC-\d{4}\|https?://\S+$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

ENUMS = {
    "event_status": {"held", "cancelled", "postponed", "rescheduled", "virtual", "announced",
                     "unverified", "disputed"},
    "campaign_phase": {"pre_launch", "launch", "primary", "runoff", "general", "early_voting",
                       "gotv", "election_day", "post_election"},
    "event_category": {"launch", "announcement", "rally", "town_hall", "meet_and_greet",
                       "community_visit", "small_business_visit", "workplace_visit",
                       "university_visit", "religious_appearance", "labor_event", "party_event",
                       "county_party_meeting", "q_and_a", "interview_tv", "interview_radio",
                       "podcast", "newspaper_interview", "livestream", "debate",
                       "debate_invitation", "press_conference", "video_release", "tour_stop",
                       "tour_launch", "tour_finale", "fundraiser", "endorsement_event",
                       "hq_opening", "early_voting_event", "gotv_event", "surrogate_event",
                       "election_eve", "watch_party", "victory_speech", "concession_speech",
                       "swearing_in", "appointment_announcement", "filing", "other"},
    "issue": {"Economy", "Healthcare", "Education", "Immigration", "Abortion", "Gun policy",
              "Energy", "Religion", "Labor", "Democracy", "Foreign policy", "Other"},
    "sponsor_type": {"candidate_campaign", "authorized_committee", "outside_pac",
                     "party_committee", "unknown"},
    "coverage_type": {"news_report", "analysis", "op_ed", "fact_check", "interview", "live_blog",
                      "newsletter", "news_video"},
    "copyright_status": {"public_domain", "licensed", "all_rights_reserved_link_only", "unknown"},
    "verification_status": {"verified", "partially verified", "unverified", "conflicting sources"},
    "source_tier": {"T1", "T2", "T3"},
    "source_type": {"official_campaign", "official_government", "candidate_social", "news_article",
                    "news_video", "transcript", "op_ed", "fact_check", "poll", "press_release",
                    "event_page", "photo", "podcast", "encyclopedia", "analysis", "report",
                    "data", "other"},
    "completeness": {"full", "partial", "clip", "unknown"},
    "winner": {"yes", "no"},
}

BAD_VALUES = {"", "TBD", "TODO", "N/A", "NA", "null", "None", "-"}


def H(*cols):
    return list(cols)


def schema(meta):
    a, b = meta["county_keys"]
    p, q = meta["poll_keys"]
    return {
        "09_sources/sources.csv": H("source_id", "url", "title", "publisher", "publication_date",
                                    "event_date", "access_date", "source_tier", "source_type",
                                    "relevant_quote_or_info", "reliability_notes", "used_by"),
        "01_candidates/policy_positions.csv": H(
            "position_id", "candidate_id", "issue", "subissue", "position_summary",
            "candidate_statement", "statement_date", "context", "source_urls", "legislative_record",
            "position_changed", "change_notes", "opponent_criticism", "fact_check",
            "verification_status"),
        "02_campaign_events/campaign_events.csv": H(
            "event_id", "candidate_id", "event_date", "event_time", "event_title", "event_category",
            "city", "venue", "state_region", "event_status", "campaign_phase", "stated_purpose",
            "observable_function", "analyst_interpretation", "target_audience", "main_messages",
            "policy_issues", "speech_summary", "transcript_url", "video_url", "photo_urls",
            "media_coverage", "opponent_reference", "visual_notes", "source_urls",
            "verification_status", "analyst_notes"),
        "03_speeches/speech_archive.csv": H(
            "speech_id", "candidate_id", "event_id", "date", "speech_title", "speech_url",
            "transcript_url", "duration", "main_topics", "major_quotes", "rhetorical_devices",
            "opponent_references", "personal_story_elements", "policy_claims", "source_urls",
            "source", "verification_status"),
        "03_speeches/speech_video_index.csv": H(
            "video_id", "candidate_id", "video_url", "date", "duration", "event_type",
            "main_topics", "relevant_timestamps", "transcript_available", "visual_observations",
            "completeness", "source_urls", "verification_status"),
        "04_visual_archive/image_archive.csv": H(
            "image_id", "candidate_id", "image_date", "event_id", "event_category", "source_name",
            "source_url", "original_image_url", "photographer", "copyright_status", "license",
            "local_filename", "image_resolution", "framing", "camera_angle", "image_quality",
            "face_visibility", "body_visibility", "clothing_notes", "notes",
            "verification_status"),
        "05_campaign_media/advertisements.csv": H(
            "ad_id", "candidate_id", "sponsor", "sponsor_type", "release_date", "title", "platform",
            "length_seconds", "issue_or_message", "main_visual_elements", "narration_soundtrack",
            "candidate_appearance", "main_claims", "video_url", "transcript_url", "fact_check",
            "media_coverage", "source_urls", "verification_status", "notes"),
        "05_campaign_media/social_media.csv": H(
            "post_id", "candidate_id", "platform", "account_handle", "post_date", "post_type",
            "content_summary", "media_included", "engagement_notes", "url",
            "verification_status", "notes"),
        "05_campaign_media/media_coverage.csv": H(
            "coverage_id", "candidate_id", "event_id", "publication_date", "outlet", "author",
            "title", "url", "source_tier", "coverage_type", "key_framing", "notable_quotes",
            "framing_of_candidate", "mentions_opponent", "reliability_notes"),
        "06_campaign_finance/campaign_finance.csv": H(
            "finance_id", "candidate_id", "period", "report_type", "reporting_deadline",
            "receipts", "individual_contributions", "pac_contributions", "disbursements",
            "cash_on_hand", "debts_owed", "source_urls", "verification_status", "notes"),
        "07_electoral_context/election_results.csv": H(
            "race_id", "race_name", "election_date", "candidate", "party", "votes", "percentage",
            "winner", "source_urls", "verification_status", "notes"),
        "07_electoral_context/county_results.csv": H(
            "county_id", "county", f"{a}_votes", f"{b}_votes", "other_votes", f"{a}_pct",
            f"{b}_pct", "total_votes", "source_urls", "verification_status"),
        "07_electoral_context/polling.csv": H(
            "poll_id", "pollster", "sponsor", "field_start", "field_end", "population",
            "sample_size", "margin_of_error", f"{p}_pct", f"{q}_pct", "other_pct",
            "undecided_pct", "leader", "margin", "source_urls", "verification_status", "notes"),
    }


CAREER = ["entry_id", "candidate_id", "start_date", "end_date", "role_or_event", "organization",
          "location", "description", "source_urls", "verification_status"]

DATE_COLS = {"event_date", "publication_date", "statement_date", "date", "release_date",
             "post_date", "field_start", "field_end", "access_date", "election_date",
             "reporting_deadline", "period", "start_date", "end_date", "image_date",
             "publication_date"}


def fail(list_, path, msg):
    list_.append(f"{path}: {msg}")


def check_file(case_dir, rel, header, sources, fails, warns):
    path = os.path.join(case_dir, rel)
    if not os.path.exists(path):
        fail(fails, rel, "missing file")
        return 0
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            got = next(reader)
        except StopIteration:
            fail(fails, rel, "empty file")
            return 0
        if got != header:
            fail(fails, rel, f"header mismatch\n    expected {header}\n    got      {got}")
            return 0
        n = 0
        for lineno, row in enumerate(reader, start=2):
            n += 1
            if len(row) != len(header):
                fail(fails, rel, f"line {lineno}: {len(row)} fields, expected {len(header)}")
                continue
            rec = dict(zip(header, row))
            for col, val in rec.items():
                if val.strip() in BAD_VALUES:
                    fail(fails, rel, f"line {lineno}: blank/placeholder in {col}")
                if col in DATE_COLS and val not in ("unknown",) and not ISO_RE.match(val):
                    if col == "period" and re.match(r"^\d{4}-Q[1-4]$", val):
                        pass
                    else:
                        fail(fails, rel, f"line {lineno}: non-ISO date in {col}: {val!r}")
                enum = ENUMS.get(col)
                enum_free = rel == "04_visual_archive/image_archive.csv" and col == "event_category"
                if enum and not enum_free and col not in ("source_tier", "source_type") and val not in enum:
                    fail(fails, rel, f"line {lineno}: {col}={val!r} not in vocabulary")
            su = rec.get("source_urls")
            if su is not None:
                if not SRC_RE.match(su):
                    fail(fails, rel, f"line {lineno}: source_urls not SRC-####|https://… : {su!r}")
                else:
                    sid, cited = su.split("|", 1)
                    if sid not in sources:
                        fail(fails, rel, f"line {lineno}: {sid} not in 09_sources/sources.csv")
                    elif sources[sid].get("url", "").rstrip("/") != cited.rstrip("/"):
                        fail(fails, rel,
                             f"line {lineno}: URL for {sid} differs from sources.csv "
                             f"({cited[:80]} vs {sources[sid].get('url','')[:80]})")
            url = rec.get("url")
            if url is not None and url != "unknown" and not url.startswith(("http://", "https://")):
                fail(fails, rel, f"line {lineno}: url not http(s): {url!r}")
    return n


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    case = argv[1]
    case_dir = case if os.path.isdir(case) else os.path.join(root, case)
    if not os.path.isdir(case_dir):
        print(f"no such case: {case_dir}")
        return 2
    meta_path = os.path.join(case_dir, "_staging", "case_meta.json")
    if not os.path.exists(meta_path):
        print(f"missing {meta_path}")
        return 2
    meta = json.load(open(meta_path, encoding="utf-8"))

    fails, warns = [], []
    sources = {}
    src_path = os.path.join(case_dir, "09_sources", "sources.csv")
    if not os.path.exists(src_path):
        fail(fails, "09_sources/sources.csv", "missing file")
    else:
        with open(src_path, encoding="utf-8-sig", newline="") as f:
            for i, rec in enumerate(csv.DictReader(f), start=2):
                sid = rec.get("source_id", "")
                if not re.match(r"^SRC-\d{4}$", sid):
                    fail(fails, "09_sources/sources.csv", f"line {i}: bad id {sid!r}")
                    continue
                if sid in sources:
                    fail(fails, "09_sources/sources.csv", f"line {i}: duplicate {sid}")
                sources[sid] = rec
                if not rec.get("url", "").startswith(("http://", "https://")):
                    fail(fails, "09_sources/sources.csv", f"line {i}: url not http(s)")
                if rec.get("source_tier") not in ENUMS["source_tier"]:
                    fail(fails, "09_sources/sources.csv", f"line {i}: tier {rec.get('source_tier')!r}")
                if rec.get("source_type") not in ENUMS["source_type"]:
                    fail(fails, "09_sources/sources.csv", f"line {i}: type {rec.get('source_type')!r}")
                if rec.get("access_date") != "2026-11-18":
                    warns.append(f"sources.csv {sid}: access_date={rec.get('access_date')!r}")

    counts = {}
    for rel, header in schema(meta).items():
        counts[rel] = check_file(case_dir, rel, header, sources, fails, warns)

    for cand in meta["candidates"]:
        rel = f"01_candidates/{cand['lower']}/career_timeline.csv"
        counts[rel] = check_file(case_dir, rel, CAREER, sources, fails, warns)
        for doc in ("biography.md", "political_positions.md"):
            p = os.path.join(case_dir, "01_candidates", cand["lower"], doc)
            if not os.path.exists(p):
                warns.append(f"missing optional doc {p}")

    for rel in ("README.md", "research_gaps.md", "_research_conventions.md",
                "07_electoral_context/election_context.md",
                "07_electoral_context/results_notes.md",
                "08_comparative_analysis/candidate_comparison.md",
                "09_sources/data_dictionary_bilingual.md"):
        if not os.path.exists(os.path.join(case_dir, rel)):
            warns.append(f"missing document {rel}")

    # downloaded images: licence must be one of the four allowed values
    img_path = os.path.join(case_dir, "04_visual_archive", "image_archive.csv")
    for rec in (csv.DictReader(open(img_path, encoding="utf-8-sig", newline=""))
                if os.path.exists(img_path) else []):
            fn = rec.get("local_filename", "unknown")
            if fn == "unknown":
                continue
            p = os.path.join(case_dir, fn)
            if not os.path.exists(p):
                p = os.path.join(case_dir, "04_visual_archive", fn)
            if not os.path.exists(p):
                fail(fails, "image_archive.csv", f"local file missing: {fn}")
            lic = rec.get("license", "")
            if not re.search(r"(CC0|public domain|\bPD\b|CC BY|CC-BY|copyrighted free use|no known copyright)", lic, re.I):
                fail(fails, "image_archive.csv", f"{rec.get('image_id')}: licence not allowed: {lic!r}")
            if os.path.getsize(p) > 3_000_000:
                warns.append(f"{fn}: larger than 3 MB")

    print(f"case: {meta.get('slug')}  ({len(sources)} sources)")
    total = 0
    for rel, n in counts.items():
        print(f"  {n:5d}  {rel}")
        total += n
    print(f"  {total:5d}  rows total")
    targets = {"campaign_events.csv": 30, "policy_positions.csv": 30, "speech_archive.csv": 12,
               "image_archive.csv": 12, "media_coverage.csv": 20, "sources": 60, "polling.csv": 6,
               "advertisements.csv": 6}
    for name, target in targets.items():
        if name == "sources":
            got = len(sources)
        else:
            got = next((n for rel, n in counts.items() if rel.endswith(name)), 0)
        if got < target:
            warns.append(f"{name}: {got} rows, target {target}")
    print(f"\nhard failures: {len(fails)}")
    for m in fails[:40]:
        print("  FAIL", m)
    print(f"soft warnings: {len(warns)}")
    for m in warns[:20]:
        print("  warn", m)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
