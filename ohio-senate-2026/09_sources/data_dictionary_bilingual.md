---
title: "Data dictionary (bilingual)"
title_zh: "数据字典（双语）"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Field-by-field definitions for all 15 CSVs, with the vocabularies the validator enforces.
---

# Data dictionary / 数据字典

## 1. Shared conventions / 通用约定

| Field pattern | Meaning / 含义 |
|---|---|
| `*_id` | Stable identifier; never reused. `SRC-####` for sources, `EV-###` events, `POS-###` positions. |
| `source_urls` | Exactly one `SRC-####|https://…` pair; the id must exist in `sources.csv` and the URL must match it. |
| `verification_status` | `verified`, `partially verified`, `unverified`, `conflicting sources`. |
| dates | ISO `YYYY-MM-DD`; `unknown` when no record fixes the date. |
| `unknown` | A value, not a placeholder. |

`source_urls` 单元格只允许一个 `SRC-####|https://…` 组合，且必须与 `sources.csv` 对应行一致。

## 2. `09_sources/sources.csv`

| Column | Definition |
|---|---|
| `source_id` | `SRC-####`, assigned in retrieval order. |
| `url` | The exact URL retrieved and mirrored. |
| `title` | Page title as served, or a descriptive title where the page is a PDF/API response. |
| `publisher` | Domain owner, mapped from the host. |
| `publication_date` | Date the page states it was published (`unknown` if absent). |
| `event_date` | Date of the event the source documents (may equal `publication_date`). |
| `access_date` | Always `2026-11-18` for this case. |
| `source_tier` | `T1` official, `T2` journalism, `T3` synthesis. |
| `source_type` | `official_government`, `official_campaign`, `news_article`, `poll`, `press_release`, `photo`, `encyclopedia`, `analysis`, `op_ed`, `fact_check`, `other`. |
| `relevant_quote_or_info` | The specific fact or quote this source supplies. |
| `reliability_notes` | Provenance caveats: paywall, syndication, JS shell, 403 mirror substitution. |
| `used_by` | Which dataset or document relies on it. |

## 3. `01_candidates/policy_positions.csv`

| Column | Definition |
|---|---|
| `position_id` | `POS-###`. |
| `candidate_id` | `BROWN` or `HUSTED`. |
| `issue` | Controlled: `Economy`, `Healthcare`, `Education`, `Immigration`, `Abortion`, `Gun policy`, `Energy`, `Religion`, `Labor`, `Democracy`, `Foreign policy`, `Other`. |
| `subissue` | Free text narrowing the issue (e.g. "data centers and electricity bills"). |
| `position_summary` | One-sentence analytic summary. |
| `candidate_statement` | Verbatim quote with attribution, or "no verbatim statement retrieved in this archive". |
| `statement_date` | Date of the statement (`unknown` if the source does not date it). |
| `context` | Where and how the statement was made (interview, survey, hearing, rally). |
| `legislative_record` | Votes, bills, sponsorships relevant to the position. |
| `position_changed` | `yes`, `no`, `partial`, `unknown`. |
| `change_notes` | What changed and when, where documented. |
| `opponent_criticism` | The other campaign's attack on this position. |
| `fact_check` | Independent check of a numeric or factual claim, or `not applicable`. |

## 4. `02_campaign_events/campaign_events.csv`

| Column | Definition |
|---|---|
| `event_id` | `EV-###`. |
| `event_time` | Clock time if reported, else `unknown`. |
| `event_category` | Controlled vocabulary (`rally`, `endorsement_event`, `press_conference`, `swearing_in`, `appointment_announcement`, `victory_speech`, `concession_speech`, `watch_party`, `small_business_visit`, `workplace_visit`, `labor_event`, `party_event`, `other`). |
| `state_region` | `Northeast`, `Northwest`, `Central`, `Southwest`, `Southeast`, `statewide`, `national`, `unknown`. |
| `event_status` | `held`, `announced`, `cancelled`, `postponed`, `rescheduled`, `virtual`, `unverified`, `disputed`. |
| `campaign_phase` | `pre_launch`, `launch`, `primary`, `runoff`, `general`, `early_voting`, `gotv`, `election_day`, `post_election`. |
| `stated_purpose` | What the campaign said the event was for. |
| `observable_function` | What the event actually does mechanically (mobilisation, coalition signalling, result-claiming). |
| `analyst_interpretation` | Clearly-labelled inference. |
| `target_audience` | Whom the event addressed. |
| `main_messages` | Reported message content. |
| `policy_issues` | Issues raised at the event. |
| `speech_summary` | Summary of what was said, or `unknown`. |
| `transcript_url`, `video_url`, `photo_urls` | Direct media URLs or `unknown`. |
| `media_coverage` | Which retrieved reports covered the event. |
| `opponent_reference` | Whether and how the opponent was named. |
| `visual_notes` | What a retrieved photograph shows. |

## 5. `07_electoral_context/election_results.csv`

| Column | Definition |
|---|---|
| `race_id` | `OH-SEN-2026-SPECIAL`, or a per-candidate row id. |
| `candidate` | Candidate name as printed. |
| `party` | `Democratic`, `Republican`, `Libertarian`, `Party for Socialism and Liberation`. |
| `votes` | Integer vote count. |
| `percentage` | Printed share, two decimals, with `%` omitted. |
| `winner` | `yes` / `no`. |

## 6. `07_electoral_context/polling.csv`

| Column | Definition |
|---|---|
| `pollster` / `sponsor` | Field house and paying client (separate columns). |
| `field_start` / `field_end` | Fieldwork window, ISO. |
| `population` | `likely voters`, `registered voters`, `adults`. |
| `sample_size` | Integer. |
| `margin_of_error` | As printed (e.g. `3.1`). |
| `brown_pct` / `husted_pct` | Two-way shares as printed. |
| `other_pct` / `undecided_pct` | Remainder, split where the release splits it. |
| `leader` | Candidate leading in that poll. |
| `margin` | Leader's lead in points. |

## 7. `06_campaign_finance/campaign_finance.csv`

`period` is ISO (`2026-09-30`) or `YYYY-Qn`; `report_type` names the filing; `receipts`,
`disbursements`, `cash_on_hand` are integers as printed; `individual_contributions`,
`pac_contributions`, `debts_owed` are `unknown` when the source table omits them.

## 8. `03_speeches/speech_archive.csv` and `speech_video_index.csv`

| Column | Definition |
|---|---|
| `speech_id` | `SP-###`. |
| `event_id` | The `EV-###` this speech belongs to, or `unknown` where the speech was an interview or a statement with no archived event. |
| `speech_url` / `transcript_url` | Direct audio/video or transcript URL; `unknown` where only reporting exists. |
| `duration` | Seconds, as stated in the file metadata; `unknown` where no recording exists. |
| `major_quotes` | Verbatim quotes only. Where the source paraphrases, this cell says so instead of inventing a quote. |
| `rhetorical_devices` | Named devices observed in the quoted passage; `unknown` where nothing is quoted. |
| `source` | What kind of document the quotes come from (report, release, floor record). |

`speech_video_index.csv` uses `video_id` (`VID-###`), `video_url`, `completeness`
(`full`, `partial`, `clip`, `unknown`) and `visual_observations`, which is `unknown` whenever the
archiver did not inspect the file.

## 9. `04_visual_archive/image_archive.csv`

| Column | Definition |
|---|---|
| `image_id` | `IMG-###`. |
| `event_id` | Dated event the image documents, or `unknown`. |
| `source_url` | The Wikimedia Commons **file page** (not the binary URL); the binary is in `original_image_url`. |
| `photographer` | Credit string from the Commons API, required for CC BY / CC BY-SA reuse. |
| `copyright_status` | `public_domain`, `licensed`, `all_rights_reserved_link_only`, `unknown`. |
| `license` | The licence string exactly as the API returns it. |
| `local_filename` | Path under `04_visual_archive/`, or `unknown` for catalogue-only rows. |
| `image_resolution` | `WxH` in pixels, from the API or measured from the downloaded file. |
| `framing` | Read from the Commons title/description only. |
| `clothing_notes`, `camera_angle`, `face_visibility`, `body_visibility` | `unknown` throughout: this build has no image-reading step, and no retrieved caption describes them. |

## 10. `05_campaign_media/` — three tables

`advertisements.csv`: `ad_id` (`AD-###`), `sponsor_type` (controlled: `candidate_campaign`,
`authorized_committee`, `outside_pac`, `party_committee`, `unknown`), `main_claims` (transcript
excerpt or a statement that no script was retrieved), `fact_check`, `video_url` (often `unknown`
because ad libraries were unreachable).

`social_media.csv`: `post_id` (`SOC-###`), `platform`, `account_handle`, `post_date`,
`post_type`, `url`. Where a post could not be retrieved directly, `notes` says how it was
documented — quoted in reporting, quoted in a Commons description, or a post later deleted.

`media_coverage.csv`: `coverage_id` (`MC-###`), `coverage_type` (controlled), and a plain `url`
column (not `source_urls`) holding the article URL; `key_framing` is the analyst's reading of the
article's angle, while `notable_quotes` holds only text the article actually prints.

## 11. `07_electoral_context/county_results.csv`

`county_id`, `county`, `brown_votes`, `husted_votes`, `other_votes`, `brown_pct`, `husted_pct`,
`total_votes`, `source_urls`, `verification_status`. **This file holds a header and zero rows** in
this build: no county vote table was retrievable. See `results_notes.md`, "The county picture".

## 12. `01_candidates/<candidate>/career_timeline.csv`

`entry_id`, `candidate_id`, `start_date` / `end_date` (ISO or `unknown`), `role_or_event`,
`organization`, `location`, `description`, `source_urls`, `verification_status`. Dates for
Husted's Senate service start at 2025-01-21 (the oath), not at the appointment.

## 13. Vocabularies enforced by the validator / 校验器强制词表

`event_status`, `campaign_phase`, `event_category`, `issue`, `sponsor_type`, `coverage_type`,
`copyright_status`, `verification_status`, `source_tier`, `source_type`, `completeness`,
`winner`. `04_visual_archive/image_archive.csv` is the one place where `event_category` is free
text, because images can document things that are not campaign events.

`image_archive.csv` 的 `event_category` 是唯一允许自由文本的枚举列（图片可记录非竞选活动的内容）。

## 14. Bilingual field labels for the main tables / 主要表双语字段

| English | 中文 |
|---|---|
| votes | 得票数 |
| percentage | 得票率 |
| winner | 是否当选 |
| receipts | 收入 |
| disbursements | 支出 |
| cash_on_hand | 期末现金 |
| pollster | 民调机构 |
| sponsor | 委托方 |
| margin_of_error | 误差范围 |
| sample_size | 样本量 |
| field_start / field_end | 实地调查起止日 |
| county | 县 |
| event_category | 活动类型 |
| campaign_phase | 竞选阶段 |
| verification_status | 核实状态 |
| source_tier | 来源层级 |
