# -*- coding: utf-8 -*-
"""Write every contract CSV from the data modules, with the exact validator headers."""
import csv, os, re
import data_sources as DS
import data_core as C
import data_events as E
import data_media as M

CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

H = {
 "09_sources/sources.csv": ["source_id", "url", "title", "publisher", "publication_date",
    "event_date", "access_date", "source_tier", "source_type", "relevant_quote_or_info",
    "reliability_notes", "used_by"],
 "01_candidates/policy_positions.csv": ["position_id", "candidate_id", "issue", "subissue",
    "position_summary", "candidate_statement", "statement_date", "context", "source_urls",
    "legislative_record", "position_changed", "change_notes", "opponent_criticism", "fact_check",
    "verification_status"],
 "02_campaign_events/campaign_events.csv": ["event_id", "candidate_id", "event_date", "event_time",
    "event_title", "event_category", "city", "venue", "state_region", "event_status",
    "campaign_phase", "stated_purpose", "observable_function", "analyst_interpretation",
    "target_audience", "main_messages", "policy_issues", "speech_summary", "transcript_url",
    "video_url", "photo_urls", "media_coverage", "opponent_reference", "visual_notes",
    "source_urls", "verification_status", "analyst_notes"],
 "03_speeches/speech_archive.csv": ["speech_id", "candidate_id", "event_id", "date", "speech_title",
    "speech_url", "transcript_url", "duration", "main_topics", "major_quotes", "rhetorical_devices",
    "opponent_references", "personal_story_elements", "policy_claims", "source_urls", "source",
    "verification_status"],
 "03_speeches/speech_video_index.csv": ["video_id", "candidate_id", "video_url", "date", "duration",
    "event_type", "main_topics", "relevant_timestamps", "transcript_available",
    "visual_observations", "completeness", "source_urls", "verification_status"],
 "04_visual_archive/image_archive.csv": ["image_id", "candidate_id", "image_date", "event_id",
    "event_category", "source_name", "source_url", "original_image_url", "photographer",
    "copyright_status", "license", "local_filename", "image_resolution", "framing", "camera_angle",
    "image_quality", "face_visibility", "body_visibility", "clothing_notes", "notes",
    "verification_status"],
 "05_campaign_media/advertisements.csv": ["ad_id", "candidate_id", "sponsor", "sponsor_type",
    "release_date", "title", "platform", "length_seconds", "issue_or_message",
    "main_visual_elements", "narration_soundtrack", "candidate_appearance", "main_claims",
    "video_url", "transcript_url", "fact_check", "media_coverage", "source_urls",
    "verification_status", "notes"],
 "05_campaign_media/social_media.csv": ["post_id", "candidate_id", "platform", "account_handle",
    "post_date", "post_type", "content_summary", "media_included", "engagement_notes", "url",
    "verification_status", "notes"],
 "05_campaign_media/media_coverage.csv": ["coverage_id", "candidate_id", "event_id",
    "publication_date", "outlet", "author", "title", "url", "source_tier", "coverage_type",
    "key_framing", "notable_quotes", "framing_of_candidate", "mentions_opponent",
    "reliability_notes"],
 "06_campaign_finance/campaign_finance.csv": ["finance_id", "candidate_id", "period", "report_type",
    "reporting_deadline", "receipts", "individual_contributions", "pac_contributions",
    "disbursements", "cash_on_hand", "debts_owed", "source_urls", "verification_status", "notes"],
 "07_electoral_context/election_results.csv": ["race_id", "race_name", "election_date", "candidate",
    "party", "votes", "percentage", "winner", "source_urls", "verification_status", "notes"],
 "07_electoral_context/county_results.csv": ["county_id", "county", "peltola_votes",
    "sullivan_votes", "other_votes", "peltola_pct", "sullivan_pct", "total_votes", "source_urls",
    "verification_status"],
 "07_electoral_context/polling.csv": ["poll_id", "pollster", "sponsor", "field_start", "field_end",
    "population", "sample_size", "margin_of_error", "peltola_pct", "sullivan_pct", "other_pct",
    "undecided_pct", "leader", "margin", "source_urls", "verification_status", "notes"],
 "01_candidates/peltola/career_timeline.csv": C.CAREER if hasattr(C, "CAREER") else
    ["entry_id", "candidate_id", "start_date", "end_date", "role_or_event", "organization",
     "location", "description", "source_urls", "verification_status"],
}
H["01_candidates/sullivan/career_timeline.csv"] = H["01_candidates/peltola/career_timeline.csv"]

MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August", "September",
     "October", "November", "December"], 1)}


def iso_date(s):
    s = (s or "").strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return "%s-%s-%s" % m.groups()
    m = re.search(r"(\d{1,2})\s+([A-Z][a-z]+)\s+(\d{4})", s)
    if m and m.group(2) in MONTHS:
        return "%04d-%02d-%02d" % (int(m.group(3)), MONTHS[m.group(2)], int(m.group(1)))
    return "unknown"


def write(rel, rows, header=None):
    header = header or H[rel]
    path = os.path.join(CASE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            out = []
            for col in header:
                v = r.get(col, "unknown")
                if v is None or (isinstance(v, str) and not v.strip()):
                    v = "unknown"
                if col in ("image_date",):
                    v = iso_date(v)
                out.append(str(v))
            w.writerow(out)
    print("%-50s %d rows" % (rel, len(rows)))


# ---- sources ----
src_rows = []
for s in DS.SOURCES:
    src_rows.append(dict(zip(
        ["source_id", "url", "title", "publisher", "publication_date", "event_date",
         "source_tier", "source_type", "relevant_quote_or_info", "reliability_notes", "used_by"], s),
        access_date=DS.ACCESS))
for cid, title, iid, lic, page in DS.COMMONS:
    meta = [m for m in __import__("json").load(open(
        os.path.join(CASE, "_staging", "commons_candidates.json"), encoding="utf-8"))
        if m["title"] == title][0]
    src_rows.append(dict(source_id=cid, url=page, title=title, publisher="Wikimedia Commons",
                         publication_date=iso_date(meta["date"]), event_date="unknown",
                         access_date=DS.ACCESS, source_tier="T3", source_type="photo",
                         relevant_quote_or_info="Licence: %s; author: %s" % (meta["lic"], meta["artist"]),
                         reliability_notes="Commons file page; licence and author from the MediaWiki API.",
                         used_by="04_visual_archive/image_archive.csv"))
write("09_sources/sources.csv", src_rows)

# ---- candidates ----
write("01_candidates/policy_positions.csv", C.POSITIONS)
for cand, rows in C.CAREERS.items():
    rr = [dict(r, candidate_id=cand.upper()) for r in rows]
    write("01_candidates/%s/career_timeline.csv" % cand.lower(), rr)

# ---- events / speeches / images ----
write("02_campaign_events/campaign_events.csv", E.EVENTS)
write("03_speeches/speech_archive.csv", E.SPEECHES)
write("03_speeches/speech_video_index.csv", E.VIDEOS)
imgs = []
for r in E.IMAGES:
    r = dict(r)
    if r["license"] == "Public domain":
        r["copyright_status"] = "public_domain"
    imgs.append(r)
write("04_visual_archive/image_archive.csv", imgs)

# ---- media / finance ----
write("05_campaign_media/advertisements.csv", M.ADS)
write("05_campaign_media/social_media.csv", M.SOCIAL)
write("05_campaign_media/media_coverage.csv", M.COVERAGE)
write("06_campaign_finance/campaign_finance.csv", M.FINANCE)

# ---- electoral ----
write("07_electoral_context/election_results.csv", M.RESULTS)
write("07_electoral_context/county_results.csv", [])
write("07_electoral_context/polling.csv", M.POLLING)

print("\ncounts: events=%d speeches=%d videos=%d images=%d ads=%d social=%d coverage=%d finance=%d polls=%d src=%d" % (
    len(E.EVENTS), len(E.SPEECHES), len(E.VIDEOS), len(imgs), len(M.ADS), len(M.SOCIAL),
    len(M.COVERAGE), len(M.FINANCE), len(M.POLLING), len(src_rows)))
