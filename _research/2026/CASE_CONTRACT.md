# Case contract — 2026 race archives (batch 2)

This file is the binding contract for the six new case folders commissioned on 2026-11-18.
Read it completely before writing anything. It adapts the Case Study 002 contract
(`south-carolina-senate-2026/_research_conventions.md`) to six races collected in one batch.

今天的日期是 **2026-11-18**。所有 `access_date` 用这一天；所有检索必须真实发生。

---

## 1. Honesty rules (non-negotiable)

1. **Never invent** a date, venue, quotation, dollar figure, endorsement, poll number, image URL or
   election result. If it is not in a page you actually retrieved, it does not go in the archive.
2. **`unknown` is a value.** No blank cells. Never guess a city, a crowd size or a precinct number.
3. **Every CSV row carries a source**: `source_urls` = `SRC-####|https://…` (the id first, then the
   single most important URL). The id must exist in that case's `09_sources/sources.csv`.
4. **Do not upgrade verification.** A fact seen only in Wikipedia is `partially verified` unless an
   official record or an independent news article you retrieved says the same thing.
5. **Separate stated purpose / observable function / interpretation.** Interpretation is prefixed
   `INTERPRETATION:`.
6. **Announcement ≠ event.** `event_status=announced` unless there is evidence it happened.
7. **No rankings, no scores, no "who ran a better campaign".** Descriptive record only.
8. **Do not write blog copy or video scripts.**
9. **Copyright:** download only Wikimedia Commons files whose licence is public domain, CC0, CC BY
   or CC BY-SA, and record photographer + licence + file page. Everything else is link-only
   (`copyright_status=all_rights_reserved_link_only`).
10. **Every fetched URL is logged** in `_staging/fetch_log.csv` with `url,http_status,bytes,fetched_at,saved_file`.
    Save the retrieved HTML/wikitext under `_staging/mirrors/`. A source that is not in the fetch log
    may not appear in `sources.csv`.

If a dataset cannot reach its target from retrievable sources, ship fewer rows and record the
shortfall with its cause in `research_gaps.md`. Asymmetry between candidates is a finding.

---

## 2. Folder layout (create exactly this)

```
<slug>/
  README.md                      bilingual, the entry point
  research_gaps.md               bilingual, what is thin and why
  _research_conventions.md       case-specific conventions (adapted from this file)
  01_candidates/
    <cand_lower>/biography.md
    <cand_lower>/career_timeline.csv
    <cand_lower>/political_positions.md
    policy_positions.csv
  02_campaign_events/
    campaign_events.csv
    <cand_lower>_timeline.md      one per candidate
    event_coverage_gaps.md
  03_speeches/
    speech_archive.csv
    speech_video_index.csv
    communication_analysis_<cand_lower>.md   one per candidate
  04_visual_archive/
    image_archive.csv
    <cand_lower>/                 downloaded licensed portraits only
  05_campaign_media/
    advertisements.csv
    social_media.csv
    media_coverage.csv
  06_campaign_finance/
    campaign_finance.csv
  07_electoral_context/
    election_results.csv
    county_results.csv
    polling.csv
    election_context.md
    results_notes.md
  08_comparative_analysis/
    candidate_comparison.md
  09_sources/
    sources.csv
    data_dictionary_bilingual.md
  _staging/
    case_meta.json
    fetch_log.csv
    mirrors/
```

Do **not** create `site/`, `10_video_frames/` or `11_speech_audio/` — the lead builds the shared
site and there is no video pipeline in this batch.

---

## 3. `_staging/case_meta.json`

```json
{
  "slug": "michigan-senate-2026",
  "race_name": "2026 United States Senate election in Michigan",
  "race_name_zh": "2026 年密歇根州联邦参议员选举",
  "election_date": "2026-11-03",
  "case_number": 3,
  "candidates": [
    {"id": "ELSAYED", "name": "Abdul El-Sayed", "party": "Democratic", "lower": "elsayed"},
    {"id": "ROGERS", "name": "Mike Rogers", "party": "Republican", "lower": "rogers"}
  ],
  "county_keys": ["elsayed", "rogers"],
  "poll_keys": ["elsayed", "rogers"],
  "result": {"winner": "ELSAYED", "margin_pct": 7.08, "source": "SRC-0001"},
  "state_regions": ["Southeast", "West", "Mid", "Northern", "statewide", "national", "unknown"]
}
```

`county_keys` / `poll_keys` drive the column names of those two CSVs. Use the candidates' `lower`
values. `state_regions` is the controlled vocabulary for `state_region`.

---

## 4. CSV schemas (headers verbatim; no blank cells)

Amounts are plain integers. Dates ISO `YYYY-MM-DD`. Percentages are numbers like `52.54` (no `%`).
Pipe-delimit multiple values inside a cell. UTF-8, no BOM, `\n` line endings, RFC-4180 quoting.

### `09_sources/sources.csv`
```
source_id,url,title,publisher,publication_date,event_date,access_date,source_tier,source_type,relevant_quote_or_info,reliability_notes,used_by
```
- `source_tier`: `T1` official/primary, `T2` established independent media, `T3` supplementary
  (Wikipedia is `T3`; assign tiers mechanically by domain, not by agreement).
- `source_type`: `official_campaign|official_government|candidate_social|news_article|news_video|transcript|op_ed|fact_check|poll|press_release|event_page|photo|podcast|encyclopedia|other`
- `publication_date`/`event_date`: `unknown` when not stated. `access_date` = `2026-11-18`.
- `used_by`: file path(s) or row ids citing it.
- `relevant_quote_or_info`: one short factual line actually present in the page (≤200 chars).

### `01_candidates/policy_positions.csv`
```
position_id,candidate_id,issue,subissue,position_summary,candidate_statement,statement_date,context,source_urls,legislative_record,position_changed,change_notes,opponent_criticism,fact_check,verification_status
```
`issue` ∈ `Economy|Healthcare|Education|Immigration|Abortion|Gun policy|Energy|Religion|Labor|Democracy|Foreign policy|Other`.

### `01_candidates/<lower>/career_timeline.csv`
```
entry_id,candidate_id,start_date,end_date,role_or_event,organization,location,description,source_urls,verification_status
```

### `02_campaign_events/campaign_events.csv`
```
event_id,candidate_id,event_date,event_time,event_title,event_category,city,venue,state_region,event_status,campaign_phase,stated_purpose,observable_function,analyst_interpretation,target_audience,main_messages,policy_issues,speech_summary,transcript_url,video_url,photo_urls,media_coverage,opponent_reference,visual_notes,source_urls,verification_status,analyst_notes
```
`event_time` local time 24h `HH:MM` or `unknown`. `event_category` ∈
`launch|announcement|rally|town_hall|meet_and_greet|community_visit|small_business_visit|workplace_visit|university_visit|religious_appearance|labor_event|party_event|county_party_meeting|q_and_a|interview_tv|interview_radio|podcast|newspaper_interview|livestream|debate|debate_invitation|press_conference|video_release|tour_stop|tour_launch|tour_finale|fundraiser|endorsement_event|hq_opening|early_voting_event|gotv_event|surrogate_event|election_eve|watch_party|victory_speech|concession_speech|swearing_in|appointment_announcement|filing|other`.
`event_status` ∈ `held|cancelled|postponed|rescheduled|virtual|announced|unverified|disputed`.
`campaign_phase` ∈ `pre_launch|launch|primary|runoff|general|early_voting|gotv|election_day|post_election`.

### `03_speeches/speech_archive.csv`
```
speech_id,candidate_id,event_id,date,speech_title,speech_url,transcript_url,duration,main_topics,major_quotes,rhetorical_devices,opponent_references,personal_story_elements,policy_claims,source_urls,source,verification_status
```
`major_quotes` = `"verbatim quote" [hh:mm:ss]` pipe-delimited; paraphrase marked `(paraphrase)`.

### `03_speeches/speech_video_index.csv`
```
video_id,candidate_id,video_url,date,duration,event_type,main_topics,relevant_timestamps,transcript_available,visual_observations,completeness,source_urls,verification_status
```

### `04_visual_archive/image_archive.csv`
```
image_id,candidate_id,image_date,event_id,event_category,source_name,source_url,original_image_url,photographer,copyright_status,license,local_filename,image_resolution,framing,camera_angle,image_quality,face_visibility,body_visibility,clothing_notes,notes,verification_status
```

### `05_campaign_media/advertisements.csv`
```
ad_id,candidate_id,sponsor,sponsor_type,release_date,title,platform,length_seconds,issue_or_message,main_visual_elements,narration_soundtrack,candidate_appearance,main_claims,video_url,transcript_url,fact_check,media_coverage,source_urls,verification_status,notes
```
`sponsor_type` ∈ `candidate_campaign|authorized_committee|outside_pac|party_committee|unknown`.

### `05_campaign_media/social_media.csv`
```
post_id,candidate_id,platform,account_handle,post_date,post_type,content_summary,media_included,engagement_notes,url,verification_status,notes
```

### `05_campaign_media/media_coverage.csv`
```
coverage_id,candidate_id,event_id,publication_date,outlet,author,title,url,source_tier,coverage_type,key_framing,notable_quotes,framing_of_candidate,mentions_opponent,reliability_notes
```
`coverage_type` ∈ `news_report|analysis|op_ed|fact_check|interview|live_blog|newsletter|news_video`.

### `06_campaign_finance/campaign_finance.csv`
```
finance_id,candidate_id,period,report_type,reporting_deadline,receipts,individual_contributions,pac_contributions,disbursements,cash_on_hand,debts_owed,source_urls,verification_status,notes
```
Never sum FEC line items with AdImpact/outside-spending totals; separate rows and state the口径 in `notes`.

### `07_electoral_context/election_results.csv`
```
race_id,race_name,election_date,candidate,party,votes,percentage,winner,source_urls,verification_status,notes
```
Every contested primary, runoff and the general election; one row per candidate per race. `winner` = `yes|no`.

### `07_electoral_context/county_results.csv`
```
county_id,county,<a>_votes,<b>_votes,other_votes,<a>_pct,<b>_pct,total_votes,source_urls,verification_status
```
`<a>`, `<b>` = `county_keys` from case_meta. If no county table is retrievable: keep the header only and
say so in `results_notes.md` (do not invent counties).

### `07_electoral_context/polling.csv`
```
poll_id,pollster,sponsor,field_start,field_end,population,sample_size,margin_of_error,<a>_pct,<b>_pct,other_pct,undecided_pct,leader,margin,source_urls,verification_status,notes
```
`<a>`, `<b>` = `poll_keys`. A candidate not tested gets `unknown`, never `0`. Primary polls where the
nominees were not both tested may be omitted or put in `polling.csv` only if the columns still apply;
otherwise note them in `results_notes.md`.

### `08_comparative_analysis/candidate_comparison.md`
Side-by-side candidacies: biography, coalition, money, schedule, message, imagery. Tables bilingual in
one cell (`English / 中文`).

---

## 5. Identifier schemes

| Entity | Pattern |
|---|---|
| Event | `<CAND3>-EVT-0001`, joint `<JNT>-EVT-0001` |
| Speech | `<CAND3>-SPC-0001` |
| Ad | `<CAND3>-AD-0001`, outside `EXT-AD-0001` |
| Image | `<CAND3>-IMG-0001` |
| Social | `<CAND3>-SOC-0001` |
| Coverage | `COV-0001` |
| Finance | `<CAND3>-FIN-0001` |
| Source | `SRC-0001` (single sequence within the case) |

`<CAND3>` = first three letters of the candidate id (e.g. `ELS`, `ROG`, `PEL`, `SUL`, `TUR`, `HIN`,
`BRO`, `HUS`, `OSS`, `COL`, `RAM`, `BAS`). If two ids collide, use four letters and say so in the
case conventions.

---

## 6. Depth targets (per case)

| Dataset | Target |
|---|---|
| `campaign_events.csv` | **30 rows**, ≥12 per candidate |
| `policy_positions.csv` | **30 rows**, ≥12 per candidate |
| `speech_archive.csv` | 12 rows, ≥5 per candidate |
| `speech_video_index.csv` | 10 rows |
| `image_archive.csv` | 12 rows, ≥3 downloaded licensed portraits in total |
| `advertisements.csv` | 6 rows |
| `social_media.csv` | 6 rows |
| `media_coverage.csv` | 20 rows |
| `campaign_finance.csv` | 8 rows |
| `election_results.csv` | every primary/runoff/general contest, one row per candidate |
| `county_results.csv` | ≥20 rows if the source publishes a county table, else header only |
| `polling.csv` | 6 rows |
| `sources.csv` | **60 unique sources**, all in the fetch log |

Order of magnitude matters less than traceability. Ship what the sources support.

---

## 7. Markdown deliverables

YAML front matter on every `.md`:

```yaml
---
title:
title_zh:
candidate_id:        # omit at case level
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete | in_progress
coverage_note: <one line: what is solid vs thin>
---
```

Then `##` sections. **Bilingual rule:** each `##` section is an English paragraph/table followed by
its Chinese counterpart (or one table with `English / 中文` cells). English governs.

`README.md` must contain: what the archive covers; the documented result table with votes and shares;
3–5 structural facts the archive establishes; folder map; what is strong vs thin; validation status;
reading paths. `research_gaps.md` must list each gap, its cause, and what would close it.

---

## 8. Retrieval workflow

1. Start from the local Wikipedia mirror: `_research/2026/<slug>.wikitext` (already downloaded
   2026-11-18). Copy it into `_staging/mirrors/wiki_<slug>.wikitext` and log it.
2. Fetch the article's reference URLs you need with Python `urllib` and an explicit User-Agent
   (`Mozilla/5.0 (research archive)`); save each response under `_staging/mirrors/`, append to
   `_staging/fetch_log.csv`. `web_fetch` is also allowed; log what it returns.
3. Campaign websites and `x.com` often return 403 / require JS. Record a 403 in the fetch log and a
   gap; never report page content you did not receive.
4. Paywalled outlets (NYT, WaPo, Politico Pro) give headline + snippet only → keep the headline,
   mark `partially verified`, note the paywall.
5. For portraits: use the Wikimedia Commons API / `Special:FilePath`, download only PD/CC0/CC BY/
   CC BY-SA, record licence and photographer, and keep the file under 2 MB.
6. Reconcile election arithmetic before writing results: candidate votes should sum to the published
   total; if they do not, say so in `results_notes.md` rather than adjusting a number.

---

## 9. Self-check before finishing

Run: `python _tools/validate_case.py <slug>` from the repo root. It must print
`0 hard failures`. Soft warnings (missing optional dataset, shortfall) are allowed but must be
explained in `research_gaps.md`.

Also check by hand:
- every `SRC-####` in every CSV resolves in `sources.csv`;
- no `TBD`, `TODO`, `N/A`, empty cells;
- `README.md` result table matches `election_results.csv` exactly;
- each downloaded image's licence is one of the four allowed licences.
