---
title: "Data Dictionary (Bilingual) — 2026 Los Angeles Mayoral Case"
title_zh: "数据字典（双语）— 2026 年洛杉矶市长案例"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: "Defines every dataset, column, controlled vocabulary and derived field so the archive can be queried without reading the generator code."
---

# Data dictionary / 数据字典

## 1. Inventory / 文件清单

| File | Rows | What it holds / 内容 |
|---|---:|---|
| `09_sources/sources.csv` | 90 | Every retrieved source: id, url, title, publisher, dates, tier, type, the quote used, reliability notes, which datasets cite it |
| `01_candidates/policy_positions.csv` | 32 | 16 issue positions per candidate, with the candidate's own wording and an opponent-criticism field |
| `01_candidates/bass/career_timeline.csv` | 10 | Bass offices and campaign milestones |
| `01_candidates/raman/career_timeline.csv` | 7 | Raman offices and campaign milestones |
| `02_campaign_events/campaign_events.csv` | 33 | 15 Bass + 18 Raman event-level rows; joint events appear once per candidate |
| `03_speeches/speech_archive.csv` | 13 | 6 Bass + 7 Raman speeches, with quotes, rhetorical devices and policy claims |
| `03_speeches/speech_video_index.csv` | 15 | Full debates, campaign videos, issue videos and interviews, with completeness |
| `04_visual_archive/image_archive.csv` | 15 | Licensed Commons files plus link-only press photography |
| `05_campaign_media/advertisements.csv` | 6 | Campaign ads and independent-expenditure ads |
| `05_campaign_media/social_media.csv` | 8 | Campaign video posts with verified titles |
| `05_campaign_media/media_coverage.csv` | 26 | Press coverage with framing and reliability notes |
| `06_campaign_finance/campaign_finance.csv` | 12 | 7 candidate-committee rows + 5 independent-expenditure rows |
| `07_electoral_context/election_results.csv` | 16 | 14 primary + 2 runoff candidate rows |
| `07_electoral_context/county_results.csv` | 0 | Header only — see `results_notes.md` §6 |
| `07_electoral_context/polling.csv` | 8 | Reconcilable runoff polls |

## 2. The `source_urls` cell / `source_urls` 单元格

Format: `SRC-####|https://…` — exactly one pair per cell, no whitespace. The `SRC-####` must resolve in
`09_sources/sources.csv`, and the URL must be identical to that row's `url` (trailing slashes ignored).
Corroboration for a row goes in `notes`, `reliability_notes` or `verification_status`, never in a second
pair. Every source row in turn must appear in `_staging/fetch_log.csv` with `http_status = 200`; blocked
and paywalled pages are logged there and reported in `research_gaps.md`, never cited.

格式：`SRC-####|https://…`——每格恰好一对，不含空白。`SRC-####` 必须在
`09_sources/sources.csv` 中可解析，且 URL 与该行 `url` 完全一致（忽略末尾斜杠）。行内交叉印证写入
`notes`、`reliability_notes` 或 `verification_status`，绝不加第二对。每个来源行又必须出现在
`_staging/fetch_log.csv` 且 `http_status = 200`；被封锁与付费墙页面只记录于彼处并在
`research_gaps.md` 中报告，绝不引用。

## 3. `unknown` / `unknown` 的语义

`unknown` = "no retrieved source establishes this". It is a value, never a zero, never "no". Numeric
columns may contain it (e.g. `debts_owed`, `other_pct`, `individual_contributions`). Text columns may
contain it (e.g. `venue`, `author`, `clothing_notes`). No row is deleted because a field is unknown.

`unknown` = "没有已获取来源可确立此项"。它是取值，绝不是零、绝不是"否"。数字列可含之（如
`debts_owed`、`other_pct`、`individual_contributions`），文本列亦可含之（如 `venue`、`author`、
`clothing_notes`）。任何行都不因某字段未知而删除。

## 4. Controlled vocabularies / 受控词表

| Column | Allowed values and meaning / 允许值与含义 |
|---|---|
| `event_status` | `held` (a source reports it occurred), `announced` (dated public statement/release, no venue), `cancelled`, `postponed`, `rescheduled`, `virtual`, `unverified`, `disputed` |
| `campaign_phase` | `pre_launch`, `launch`, `primary`, `runoff`, `general`, `early_voting`, `gotv`, `election_day`, `post_election` |
| `event_category` | 40 values; used here: `filing`, `launch`, `announcement`, `debate`, `town_hall`, `q_and_a`, `community_visit`, `labor_event`, `endorsement_event`, `newspaper_interview`, `victory_speech` |
| `issue` | Federal vocabulary only: `Economy`, `Healthcare`, `Education`, `Immigration`, `Abortion`, `Gun policy`, `Energy`, `Religion`, `Labor`, `Democracy`, `Foreign policy`, `Other`. Municipal domains (housing, homelessness, public safety, budget, fires, transit) are `Other`, with the real label in `subissue` |
| `sponsor_type` | `candidate_campaign`, `authorized_committee`, `outside_pac`, `party_committee`, `unknown` |
| `coverage_type` | `news_report`, `analysis`, `op_ed`, `fact_check`, `interview`, `live_blog`, `newsletter`, `news_video` |
| `copyright_status` | `public_domain`, `licensed`, `all_rights_reserved_link_only`, `unknown` |
| `verification_status` | `verified`, `partially verified`, `unverified`, `conflicting sources` — rules in `_research_conventions.md` §8 |
| `source_tier` | `T1` official record/campaign/commission, `T2` professional newsroom with editorial standards, `T3` community/trade/aggregator/encyclopedia |
| `source_type` | `official_campaign`, `official_government`, `candidate_social`, `news_article`, `news_video`, `transcript`, `op_ed`, `fact_check`, `poll`, `press_release`, `event_page`, `photo`, `podcast`, `encyclopedia`, `analysis`, `report`, `data`, `other` |
| `completeness` | `full`, `partial`, `clip`, `unknown` — for videos: `full` = complete event, `clip` = excerpt, `unknown` = duration unreadable |
| `winner` | `yes` (advanced in primary / elected in runoff), `no` |

`issue` 的联邦词表不覆盖市政议题，故住房、无家可归、公共安全、预算、火灾、交通均记 `Other`，
真正的标签在 `subissue`。`verification_status` 的判定规则见 `_research_conventions.md` §8。

## 5. Derived and computed fields / 派生与计算字段

| Field | How it was produced / 生成方式 |
|---|---|
| `election_results.percentage` | Quoted for Bass/Raman/Pratt; **computed** as votes ÷ 853,894 (primary) or ÷ 1,120,223 (runoff) for all others, rounded to 0.1, and flagged in `notes` |
| `polling.margin` | leader's share minus second candidate's share; `0` when `leader = tie`; never negative |
| `polling.leader` | the candidate ahead, or `tie` |
| `campaign_finance.receipts` | For candidate rows: total raised in the period, including matching funds where the commission aggregates them. For IE rows: money received by the outside committee |
| `sources.used_by` | Computed by scanning every CSV's `source_urls` for that id, then every `.md` for the id as text; `narrative_only` means cited in documents but no table row |
| `image_archive.local_filename` | Relative to `04_visual_archive/` when a file was downloaded; `unknown` otherwise |
| campaign events `event_id` | `BAS-EVT-####` / `RAM-EVT-####`; joint events have one row per candidate, cross-referenced in `analyst_notes` |

## 6. Dataset-specific notes / 各数据集说明

**`02_campaign_events`.** `stated_purpose` and `observable_function` are descriptive; every evaluative
sentence is in `analyst_interpretation` and begins with `INTERPRETATION:`. `visual_notes` is `unknown`
wherever the build could not view imagery. `speech_summary` paraphrases only what a retrieved text reports.

**`02_campaign_events`。** `stated_purpose` 与 `observable_function` 为描述性；所有评价性句子都在
`analyst_interpretation` 中并以 `INTERPRETATION:` 开头。凡本次构建无法查看影像，`visual_notes` 即为
`unknown`。`speech_summary` 仅转述已获取文本所述内容。

**`03_speeches`.** `major_quotes` uses `"…"` around verbatim text and records the source's framing when
the quote reached the archive via a columnist. `duration` is `unknown` for every row: no player metadata
was readable.

**`03_speeches`。** `major_quotes` 用引号标出逐字文本，并在引语经由专栏作者转述时记录该框架。
所有行的 `duration` 均为 `unknown`：未能读取任何播放器元数据。

**`04_visual_archive`.** `framing`, `camera_angle`, `image_quality`, `face_visibility`,
`body_visibility` and `clothing_notes` are `unknown` unless a published caption or report states the
detail — this build had no image input. `copyright_status = all_rights_reserved_link_only` marks press
photography that is described and linked but not redistributed.

**`04_visual_archive`。** 除已发表图说或报道明确提及外，`framing`、`camera_angle`、`image_quality`、
`face_visibility`、`body_visibility`、`clothing_notes` 均为 `unknown`——本次构建无图像输入。
`copyright_status = all_rights_reserved_link_only` 标记仅描述并链接、不再分发的新闻摄影。

**`05_campaign_media`.** `advertisements.length_seconds` is `unknown` except Raman's 30-second Emmy spot
(as reported). `main_visual_elements` for the Bass ICE spot and the LAPPL ad is the L.A. Times
newsletter's description, not the archive's viewing. `social_media` rows are campaign YouTube posts whose
titles were verified through oEmbed; engagement counts were not retrievable.

**`05_campaign_media`。** 除 Raman 的 30 秒艾美奖广告（据报）外，`advertisements.length_seconds`
均为 `unknown`。Bass 移民执法广告与 LAPPL 广告的 `main_visual_elements` 来自洛杉矶时报通讯的描述，
而非档案的观看。`social_media` 各行为竞选 YouTube 发布，标题经 oEmbed 核实；互动数据不可获取。

**`06_campaign_finance`.** `period` = reported-through date. `report_type` distinguishes
`primary_cycle_reported_through`, `runoff_cycle_reported_through`,
`independent_expenditure_committee_receipt` and `independent_expenditure_against_candidate`. The last two
are not candidate money; see `_research_conventions.md` §5.

**`06_campaign_finance`。** `period` = 申报截止日。`report_type` 区分初选周期、决选周期、独立支出
委员会收款、以及针对某候选人的独立支出。后两类不是候选人资金；见 `_research_conventions.md` §5。

**`07_electoral_context`.** `party` is `Nonpartisan` throughout by law. `county_results.csv` is header-only
by design (`results_notes.md` §6). `polling.population` is `LV` (likely voters) for all eight rows;
`margin_of_error` is `unknown` where the pollster published none.

**`07_electoral_context`。** `party` 依法一律为 `Nonpartisan`。`county_results.csv` 按设计只有表头
（`results_notes.md` §6）。`polling.population` 八行全为 `LV`（可能投票者）；`margin_of_error` 在
民调机构未公布时为 `unknown`。

## 7. Identifiers / 编号规则

`SRC-0001`–`SRC-0090` (registry order, stable). `BAS-POL-####` / `RAM-POL-####` positions;
`BAS-EVT-####` / `RAM-EVT-####` events; `SPE-BAS-####` / `SPE-RAM-####` speeches; `VID-####` videos;
`IMG-####` images; `AD-####` ads; `SOC-####` social posts; `COV-####` coverage; `FIN-####` finance;
`POLL-####` polls; `BAS-CAR-####` / `RAM-CAR-####` career entries. Race ids `LA-MAYOR-2026-P` and
`LA-MAYOR-2026-R`.

`SRC-0001`–`SRC-0090`（登记顺序，稳定）。立场 `BAS-POL-####`/`RAM-POL-####`；活动
`BAS-EVT-####`/`RAM-EVT-####`；演讲 `SPE-BAS-####`/`SPE-RAM-####`；视频 `VID-####`；图像
`IMG-####`；广告 `AD-####`；社交发布 `SOC-####`；报道 `COV-####`；财务 `FIN-####`；民调
`POLL-####`；履历 `BAS-CAR-####`/`RAM-CAR-####`。选举编号 `LA-MAYOR-2026-P` 与 `LA-MAYOR-2026-R`。

## 8. Joining the tables / 表间连接

`candidate_id` joins everything (`BASS`, `RAMAN`, plus `JOINT`, `PRATT`, `MILLER`, `HUANG` as documented
in `_research_conventions.md` §6). `event_id` joins `campaign_events` to `speech_archive`,
`media_coverage` and `image_archive`. `source_urls` joins any table to `sources.csv`. There is no
`district` key anywhere, because no district-level data was retrieved.

`candidate_id` 连接所有表（`BASS`、`RAMAN`，另加 `JOINT`、`PRATT`、`MILLER`、`HUANG`，见
`_research_conventions.md` §6）。`event_id` 连接 `campaign_events` 与 `speech_archive`、
`media_coverage`、`image_archive`。`source_urls` 连接任意表与 `sources.csv`。任何表中都没有
`district` 键，因为未获取任何分区级数据。
