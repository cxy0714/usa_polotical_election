---
title: Data dictionary (bilingual)
title_zh: 数据字典（双语）
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Covers every CSV in the case with field definitions, controlled vocabularies and the citation format.
---

## Citation format / 引用格式

Every row carries `source_urls` in the form `SRC-####|https://…`. The id resolves in `09_sources/sources.csv`, and the URL must match that record byte-for-byte after trimming a trailing slash. One row, one source. SRC-0001

每行 `source_urls` 采用 `SRC-####|https://…` 形式。编号可在 `09_sources/sources.csv` 中解析，链接须与记录逐字符一致（去除末尾斜杠后）。一行一个来源。SRC-0001

## Controlled vocabularies / 受控词表

`event_status`: held, cancelled, postponed, rescheduled, virtual, announced, unverified, disputed.
`campaign_phase`: pre_launch, launch, primary, runoff, general, early_voting, gotv, election_day, post_election.
`issue`: Economy, Healthcare, Education, Immigration, Abortion, Gun policy, Energy, Religion, Labor, Democracy, Foreign policy, Other.
`sponsor_type`: candidate_campaign, authorized_committee, outside_pac, party_committee, unknown.
`verification_status`: verified, partially verified, unverified, conflicting sources.
`copyright_status`: public_domain, licensed, all_rights_reserved_link_only, unknown.

`event_status`：held、cancelled、postponed、rescheduled、virtual、announced、unverified、disputed。
`campaign_phase`：pre_launch、launch、primary、runoff、general、early_voting、gotv、election_day、post_election。
`issue`：经济、医疗、教育、移民、堕胎、枪支、能源、宗教、劳工、民主、外交、其他。
`sponsor_type`：候选人竞选、授权委员会、外部 PAC、政党委员会、未知。
`verification_status`：已核实、部分核实、未核实、来源冲突。
`copyright_status`：公有领域、授权使用、保留权利仅链接、未知。

## Key files / 关键文件

`02_campaign_events/campaign_events.csv` — 32 rows; `stated_purpose` is the campaign's framing, `observable_function` what a reporter saw, `analyst_interpretation` starts with `INTERPRETATION:`.
`01_candidates/policy_positions.csv` — 33 rows; `candidate_statement` holds a quote or `unknown`; `fact_check` records whether the claim was independently checked.
`07_electoral_context/polling.csv` — 6 polls; `leader` and `margin` are as published, not computed; `notes` flags the Wikipedia table disagreement.
`04_visual_archive/image_archive.csv` — 13 rows; `local_filename` is a path relative to the case root or `unknown`; `license` must be one of the four open licences.

`02_campaign_events/campaign_events.csv` — 32 行；`stated_purpose` 为竞选方框定，`observable_function` 为记者所见，`analyst_interpretation` 以 `INTERPRETATION:` 开头。
`01_candidates/policy_positions.csv` — 33 行；`candidate_statement` 为引语或 `unknown`；`fact_check` 记录主张是否经独立核查。
`07_electoral_context/polling.csv` — 6 项民调；`leader` 与 `margin` 按原文，不作计算；`notes` 标注与维基表格的分歧。
`04_visual_archive/image_archive.csv` — 12 行；`local_filename` 为相对案例根目录的路径或 `unknown`；`license` 须为四种开放许可之一。

## Numeric conventions / 数字约定

Votes are integers as published, without separators. Percentages are as published to the stated decimals (59.03, 40.97, 55.5). Margins are percentage points. Money is US dollars as reported, unadjusted for inflation. `unknown` is a value, never an empty cell. SRC-0001 SRC-0007

票数为公布的整数，不加千分位。百分比按公布精度（59.03、40.97、55.5）。差额为百分点。金额为报道的美元数值，不作通胀调整。`unknown` 是取值，绝非空单元。SRC-0001 SRC-0007

## File-by-file summary / 逐文件摘要

| File | Rows | 中文说明 |
|---|---|---|
| `01_candidates/ossoff/career_timeline.csv` | 10 | 奥索夫履历年表 |
| `01_candidates/collins/career_timeline.csv` | 10 | 柯林斯履历年表 |
| `01_candidates/policy_positions.csv` | 33 | 双方立场，共 33 条 |
| `02_campaign_events/campaign_events.csv` | 32 | 有日期的竞选活动 |
| `03_speeches/speech_archive.csv` | 13 | 演讲与辩论引语档案 |
| `03_speeches/speech_video_index.csv` | 10 | 视频索引，多为未取得链接 |
| `04_visual_archive/image_archive.csv` | 13 | 图像档案，5 张已本地保存 |
| `05_campaign_media/advertisements.csv` | 6 | 广告与投放记录 |
| `05_campaign_media/social_media.csv` | 7 | 社交帖文记录 |
| `05_campaign_media/media_coverage.csv` | 27 | 媒体报道清单 |
| `06_campaign_finance/campaign_finance.csv` | 8 | 竞选财务 |
| `07_electoral_context/election_results.csv` | 10 | 初选、第二轮与大选结果 |
| `07_electoral_context/county_results.csv` | 0 | 仅表头，县级数据缺失 |
| `07_electoral_context/polling.csv` | 6 | 选前民调 |
| `09_sources/sources.csv` | 99 | 全部来源 |
