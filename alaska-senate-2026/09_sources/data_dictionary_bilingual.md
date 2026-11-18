---
title: "Alaska 2026 case archive — bilingual data dictionary"
title_zh: "阿拉斯加 2026 案例档案 — 双语文数据字典"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: "Defines every column and every controlled vocabulary used in the case's 15 CSVs."
---

# Data dictionary / 数据字典

## How to read these tables

Every CSV is UTF-8, comma-separated, RFC 4180 quoting, LF line endings, with a single header row. All
files share four conventions: `unknown` means "not published or not retrieved" and is never a blank;
`source_urls` carries exactly one `SRC-####|https://…` pair resolving in `09_sources/sources.csv`;
dates are ISO `YYYY-MM-DD` or `unknown`; no cell is empty.

所有 CSV 均为 UTF-8、逗号分隔、RFC 4180 引号规则、LF 换行、单行表头。四个通用约定：`unknown` 表示
"未公布或未取得"，绝不留空；`source_urls` 只含一个可在 `09_sources/sources.csv` 解析的
`SRC-####|https://…`；日期为 ISO `YYYY-MM-DD` 或 `unknown`；任何单元格均不空白。

## Common columns

| Column | Meaning (English) | 含义（中文） |
|---|---|---|
| `candidate_id` | `PELTOLA` or `SULLIVAN`; matches `case_meta.json` | `PELTOLA` 或 `SULLIVAN`；与 `case_meta.json` 一致 |
| `source_urls` | One source id and its URL, e.g. `SRC-0001|https://…` | 一个来源编号及其 URL |
| `verification_status` | `verified`, `partially verified`, `unverified`, `conflicting sources` | 已核实 / 部分核实 / 未核实 / 来源冲突 |
| `notes` / `analyst_notes` | Prose explaining provenance, caveats, or why a cell is `unknown` | 说明来源、告诫，或某格为何为 `unknown` |
| `event_id` | Foreign key into `02_campaign_events/campaign_events.csv`; `unknown` when no coded event exists | 指向活动表的键；无对应活动时为 `unknown` |
| `issue` | Controlled topic vocabulary (see below) | 受控议题词表（见下） |
| `period` | Reporting period: ISO date, `YYYY-Qn`, or `unknown` | 报告期：ISO 日期、`YYYY-Qn` 或 `unknown` |

## `09_sources/sources.csv` (124 rows)

| Column | Meaning | 含义 |
|---|---|---|
| `source_id` | `SRC-0001` … `SRC-0124`, unique | 唯一来源编号 |
| `url` | Canonical URL that was retrieved | 实际抓取的规范 URL |
| `title` | Page or article title as published | 页面或文章原标题 |
| `publisher` | Outlet, agency or platform | 媒体、机构或平台 |
| `publication_date` | Publication date, ISO or `unknown` | 发布日期 |
| `event_date` | Date of the event the source describes, if any | 所述事件的日期（如有） |
| `access_date` | `2026-11-18` for every row | 全部为 2026-11-18 |
| `source_tier` | `T1` official, `T2` newsroom of record, `T3` campaign/party/advocacy/reference | 一级官方 / 二级主流媒体 / 三级竞选、政党、倡议、参考 |
| `source_type` | Controlled vocabulary (see below) | 受控类型词表 |
| `relevant_quote_or_info` | The sentence or fact the source supplies | 该来源提供的语句或事实 |
| `reliability_notes` | Known bias, paywall, 403, or extraction caveat | 已知倾向、付费墙、403 或抽取告诫 |
| `used_by` | Which archive files cite it | 被哪些档案文件引用 |

## `01_candidates/policy_positions.csv` (31 rows: Peltola 15, Sullivan 16)

| Column | Meaning | 含义 |
|---|---|---|
| `position_id` | `PEL-POS-nn` / `SUL-POS-nn` | 立场编号 |
| `issue` | One of the contract's twelve issue categories | 合同规定的十二个议题类别之一 |
| `subissue` | Free-text specificity, e.g. "Trawl bycatch" | 自由文本细分议题 |
| `position_summary` | The coded position in one sentence | 一句话概括的立场 |
| `candidate_statement` | Verbatim quote, or `unknown` if none exists | 逐字引语；无则 `unknown` |
| `statement_date` | Date of that statement | 该表态的日期 |
| `context` | Where and to whom it was said | 场合与对象 |
| `legislative_record` | Votes or bills that support the coding | 支撑编码的表决或法案 |
| `position_changed` | `yes`/`no`/`unknown` | 立场是否变化 |
| `change_notes` | Explanation when it changed | 变化说明 |
| `opponent_criticism` | How the rival framed it | 对手如何攻击该立场 |
| `fact_check` | Any fact-check found, else `unknown` | 事实核查结论（如有） |

## `01_candidates/<cand>/career_timeline.csv` (10 + 11 rows)

`entry_id`, `start_date`, `end_date`, `role_or_event`, `organization`, `location`, `description`.
`start_date`/`end_date` are full ISO dates or `unknown`; a month-only precision given by a source is
stated in `description` instead of being invented as a day.

日期列只写完整 ISO 日期或 `unknown`；来源仅给出月份的，精度写入 `description`，不臆造具体日。

## `02_campaign_events/campaign_events.csv` (30 rows)

| Column | Meaning | 含义 |
|---|---|---|
| `event_id` | `PEL-EVT-nn` / `SUL-EVT-nn` | 活动编号 |
| `event_date`, `event_time` | ISO date; time almost always `unknown` | 日期；时间几乎均为 `unknown` |
| `event_title` | Descriptive title, not a campaign slogan | 描述性标题，非竞选口号 |
| `event_category` | Controlled vocabulary (see below) | 受控类别词表 |
| `city`, `venue`, `state_region` | Location; `state_region` from the case's region list | 地点；区域取自案例区域表 |
| `event_status` | `held`, `announced`, `unverified`, … (see below) | 状态词表 |
| `campaign_phase` | `pre_launch` … `post_election` | 竞选阶段 |
| `stated_purpose` | What the campaign said it was for | 竞选方自述目的 |
| `observable_function` | What actually happened, as reported | 报道所述的实际功能 |
| `analyst_interpretation` | Archive's reading, explicitly labelled | 档案解读，明确标注为解读 |
| `target_audience` | Reported or inferred audience | 报道或推断的受众 |
| `main_messages` | Message content, quoted where possible | 信息内容，尽量引用 |
| `policy_issues` | Semicolon-separated issue tags | 分号分隔的议题标签 |
| `speech_summary` | What was said | 发言概要 |
| `transcript_url`, `video_url`, `photo_urls` | Media links, `unknown` when none | 媒体链接；无则 `unknown` |
| `media_coverage` | Outlets that covered it | 报道媒体 |
| `opponent_reference` | Whether and how the rival was mentioned | 是否及如何提及对手 |
| `visual_notes` | Staging, signage, crowd, only if reported | 仅在有报道时记录布置、标语、人群 |

## `03_speeches/speech_archive.csv` (12) and `speech_video_index.csv` (10)

`speech_archive.csv`: `speech_id`, `event_id`, `date`, `speech_title`, `speech_url`,
`transcript_url`, `duration`, `main_topics`, `major_quotes`, `rhetorical_devices`,
`opponent_references`, `personal_story_elements`, `policy_claims`, `source`, `verification_status`.
`major_quotes` holds verbatim text with single-quote delimiters; multiple quotes separated by ` / `.

`speech_video_index.csv`: `video_id`, `video_url`, `date`, `duration`, `event_type`, `main_topics`,
`relevant_timestamps`, `transcript_available`, `visual_observations`, `completeness`. Rows are
**segment-level** entries over three videos; `relevant_timestamps` is `unknown` because no timestamps
were verified, and `completeness` is `partial`.

视频索引为三个视频上的**片段级**条目；`relevant_timestamps` 因未核实时间码而为 `unknown`，
`completeness` 为 `partial`。

## `04_visual_archive/image_archive.csv` (12 rows, 6 downloaded)

| Column | Meaning | 含义 |
|---|---|---|
| `image_id` | `PEL-IMG-nnnn` / `SUL-IMG-nnnn` | 图像编号 |
| `image_date` | Date the image was taken, ISO or `unknown` | 拍摄日期 |
| `event_category` | Free text here (portrait, debate, surrogate_event) | 此处为自由文本 |
| `source_name`, `source_url` | Commons file page or news article | Commons 文件页或新闻文章 |
| `original_image_url` | Direct file URL when known | 已知时的直接文件链接 |
| `photographer` | Named photographer or uploader credit | 摄影者或上传者署名 |
| `copyright_status` | `public_domain`, `licensed`, `all_rights_reserved_link_only`, `unknown` | 版权状态 |
| `license` | `Public domain`, `CC0`, `CC BY 2.0`, … or "all rights reserved" | 许可类型 |
| `local_filename` | Path under `04_visual_archive/`, or `unknown` if not downloaded | 本地路径；未下载则为 `unknown` |
| `image_resolution` | `WxH` of the stored file | 存档文件分辨率 |
| `framing`, `camera_angle`, `image_quality` | Visual coding | 视觉编码 |
| `face_visibility`, `body_visibility` | `clear`, `partial`, `unknown` | 面部/身体可见度 |
| `clothing_notes` | Attire, only when visible and relevant | 仅在有意义时记录着装 |

## `05_campaign_media/*.csv` (6 + 7 + 24 rows)

`advertisements.csv`: `ad_id`, `sponsor`, `sponsor_type` (`candidate_campaign`, `authorized_committee`,
`outside_pac`, `party_committee`, `unknown`), `release_date`, `title`, `platform`, `length_seconds`,
`issue_or_message`, `main_visual_elements`, `narration_soundtrack`, `candidate_appearance`,
`main_claims`, `video_url`, `transcript_url`, `fact_check`, `media_coverage`.
`social_media.csv`: `post_id`, `platform`, `account_handle`, `post_date`, `post_type`,
`content_summary`, `media_included`, `engagement_notes`, `url`.
`media_coverage.csv`: `coverage_id`, `publication_date`, `outlet`, `author`, `title`, `url`,
`source_tier`, `coverage_type` (`news_report`, `analysis`, `op_ed`, `fact_check`, `interview`,
`live_blog`, `newsletter`, `news_video`), `key_framing`, `notable_quotes`, `framing_of_candidate`,
`mentions_opponent`, `reliability_notes`.

## `06_campaign_finance/campaign_finance.csv` (8 rows)

`finance_id`, `period`, `report_type` (free text: `quarterly`, `cycle_to_date`, `account_closure`,
`house_cycle_total`, `independent_expenditure_context`), `reporting_deadline`, `receipts`,
`individual_contributions`, `pac_contributions`, `disbursements`, `cash_on_hand`, `debts_owed`.
Amounts are US dollars as whole numbers without separators, exactly as the reporting outlet stated
them; `unknown` where the outlet did not report a figure. No figure was derived by subtraction.

金额为美元整数、不加千分位，与报道原文一致；报道未给出的记为 `unknown`。未通过相减推算任何数字。

## `07_electoral_context/*.csv` (12 + 0 + 8 rows)

- `election_results.csv`: `race_id` (`AK-SEN-2026-GEN`, `AK-SEN-2026-PRIMARY`), `race_name`,
  `election_date`, `candidate`, `party`, `votes`, `percentage`, `winner` (`yes`/`no`), `notes`.
  Includes a `Total votes cast` row for each race; its `winner` is `no` by convention because a total
  is not a candidacy.
- `county_results.csv`: required header, zero rows — Alaska reports by state house district, not
  county (see `results_notes.md`).
- `polling.csv`: `poll_id`, `pollster`, `sponsor`, `field_start`, `field_end`, `population`
  (`LV`/`RV`/`unknown`), `sample_size`, `margin_of_error`, `peltola_pct`, `sullivan_pct`, `other_pct`,
  `undecided_pct`, `leader`, `margin`, `notes`. Percentages are first-round unless `notes` says the
  pollster allocated eliminated candidates.

## Controlled vocabularies

| Field | Allowed values |
|---|---|
| `event_status` | `held`, `cancelled`, `postponed`, `rescheduled`, `virtual`, `announced`, `unverified`, `disputed` |
| `campaign_phase` | `pre_launch`, `launch`, `primary`, `runoff`, `general`, `early_voting`, `gotv`, `election_day`, `post_election` |
| `event_category` | launch, announcement, rally, town_hall, meet_and_greet, community_visit, small_business_visit, workplace_visit, university_visit, religious_appearance, labor_event, party_event, county_party_meeting, q_and_a, interview_tv, interview_radio, podcast, newspaper_interview, livestream, debate, debate_invitation, press_conference, video_release, tour_stop, tour_launch, tour_finale, fundraiser, endorsement_event, hq_opening, early_voting_event, gotv_event, surrogate_event, election_eve, watch_party, victory_speech, concession_speech, swearing_in, appointment_announcement, filing, other |
| `issue` | Economy, Healthcare, Education, Immigration, Abortion, Gun policy, Energy, Religion, Labor, Democracy, Foreign policy, Other |
| `sponsor_type` | `candidate_campaign`, `authorized_committee`, `outside_pac`, `party_committee`, `unknown` |
| `coverage_type` | `news_report`, `analysis`, `op_ed`, `fact_check`, `interview`, `live_blog`, `newsletter`, `news_video` |
| `copyright_status` | `public_domain`, `licensed`, `all_rights_reserved_link_only`, `unknown` |
| `verification_status` | `verified`, `partially verified`, `unverified`, `conflicting sources` |
| `source_tier` | `T1`, `T2`, `T3` |
| `source_type` | official_campaign, official_government, candidate_social, news_article, news_video, transcript, op_ed, fact_check, poll, press_release, event_page, photo, podcast, encyclopedia, other |
| `completeness` | `full`, `partial`, `clip`, `unknown` |
| `winner` | `yes`, `no` |
| `state_region` | Anchorage, Matanuska-Susitna, Fairbanks, Southeast, Kenai Peninsula, Northern, Rural, statewide, national, unknown |

| 字段 | 允许值 |
|---|---|
| `event_status` | 举行、取消、推迟、改期、线上、宣布、未核实、有争议（对应英文枚举） |
| `campaign_phase` | 宣布前、宣布、初选、决选、大选、提前投票、催票、选举日、选后 |
| `issue` | 经济、医疗、教育、移民、堕胎、枪支政策、能源、宗教、劳工、民主、外交、其他 |
| `verification_status` | 已核实、部分核实、未核实、来源冲突 |
| `winner` | 是、否 |

## Integrity summary

| File | Rows | Minimum required |
|---|---:|---:|
| `sources.csv` | 124 | 60 |
| `campaign_events.csv` | 30 | 30 |
| `policy_positions.csv` | 31 | 30 (≥12 per candidate) |
| `speech_archive.csv` | 12 | 12 (≥5 per candidate) |
| `speech_video_index.csv` | 10 | 10 |
| `image_archive.csv` | 12 | 12 |
| `advertisements.csv` | 6 | 6 |
| `social_media.csv` | 7 | 6 |
| `media_coverage.csv` | 24 | 20 |
| `campaign_finance.csv` | 8 | 8 |
| `election_results.csv` | 12 | — |
| `county_results.csv` | 0 | header only, documented |
| `polling.csv` | 8 | 6 |

Validator: `hard failures: 0`.
