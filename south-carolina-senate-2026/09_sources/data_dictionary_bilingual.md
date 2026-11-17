---
title: "Data dictionary — South Carolina Senate 2026 archive"
title_zh: "数据字典——2026 南卡罗来纳州联邦参议员选举档案"
compiled_by: Lead Research Agent
last_updated: 2026-11-12
status: in_progress
coverage_note: "Documents every delivered CSV column, every controlled vocabulary, the id scheme and the known deviations. Read this before querying anything."
---

# Data dictionary / 数据字典

## 1. How to read any row / 1. 如何读任何一行

Three rules govern every table in this archive.

三条规则支配本档案中的每一张表。

**Rule 1 — `unknown` is a value, not a gap.** A cell reading `unknown` means the retrieved sources
do not state it. It never means "not applicable" and it never means zero. Filtering `unknown` out
silently changes the denominator of any count you compute.

**规则一——`unknown` 是取值，不是缺失。** 单元格为 `unknown` 表示已检索来源未作说明；它从不表示「不适用」，也从不表示零。把 `unknown` 静默过滤掉，会悄悄改变任何计数的分母。

**Rule 2 — every row carries `SRC-####|https://…`.** The token identifies the source, the URL
after the pipe is the retrievable address. Multi-source cells separate entries with `;`. The id
resolves in [`sources.csv`](sources.csv); the token's numeric block tells you which collection
stream produced it (§5).

**规则二——每一行都带 `SRC-####|https://…`。** token 标识来源，竖线后的 URL 是可检索地址；多来源单元格用 `;` 分隔。id 在 `sources.csv` 中解析；token 的号段说明它由哪个采集流产生（见 §5）。

**Rule 3 — inference is labelled.** Anything the analyst concluded rather than read begins with
`INTERPRETATION:`. A sentence without that prefix is a statement about a source.

**规则三——推断有标记。** 分析师得出的、而非读到的内容，都以 `INTERPRETATION:` 开头。没有该前缀的句子是对来源的陈述。

## 2. Files / 2. 文件

| File / 文件 | Rows / 行数 | What it holds / 内容 |
|---|---|---|
| `01_candidates/policy_positions.csv` | 51 | One row per candidate–issue position, with statement date, verbatim where available, and `position_changed`. |
| `01_candidates/andrews/career_timeline.csv` | 20 | Dated career and campaign milestones for Andrews. |
| `01_candidates/graham/career_timeline.csv` | 24 | Dated career and campaign milestones for Graham. |
| `02_campaign_events/campaign_events.csv` | 28 | Documented events, each anchored to a date in a retrieved source. |
| `03_speeches/speech_archive.csv` | 24 | Speeches and speech-like appearances. |
| `03_speeches/speech_video_index.csv` | 22 | Video of each speech, where one exists. |
| `04_visual_archive/image_archive.csv` | 48 | Photographs and campaign visuals, with rights status. |
| `05_campaign_media/media_coverage.csv` | 55 | Coverage register: outlet, author, title, tier, framing. |
| `05_campaign_media/advertisements.csv` | 3 | Documented ad and outside-money entries. |
| `05_campaign_media/social_media.csv` | 3 | Documented social posts. |
| `06_campaign_finance/campaign_finance.csv` | 5 | Principal-candidate FEC snapshots. |
| `06_campaign_finance/other_candidates_finance.csv` | 15 | Every other filed candidate, kept out of the principal table by schema rule. |
| `07_electoral_context/election_results.csv` | 26 | Race-level results, including the primary rounds. |
| `07_electoral_context/county_results.csv` | 46 | All 46 counties. |
| `07_electoral_context/polling.csv` | 20 | General-election polls and forecasters. |
| `07_electoral_context/primary_polling.csv` | 6 | Primary and runoff polling. |
| `09_sources/sources.csv` | 370 | Every source, with tier, type, and a computed `used_by`. |
| `09_sources/exit_poll_2026.csv` | 45 | Exit-poll subgroups, 15 groups. |
| `10_video_frames/keyframes.csv` | see file | One row per extracted keyframe. |
| `10_video_frames/keyframes_identity.csv` | 300 | Per-frame SFace identity match: `ANDREWS`, `GRAHAM`, `unknown`, `other`, `noface`. |
| `10_video_frames/video_face_summary.csv` | 27 | Per-video frame and face counts. |
| `10_video_frames/video_sources.csv` | 27 | The downloaded corpus, with local filenames and byte sizes. |
| `11_speech_audio/audio_metrics.csv` | 27 | Loudness, silence ratio and caption-derived word counts. |

行数为本次交付的实际行数，不是目标行数；未达目标的部分记录在 `research_gaps.md`，不以填充行凑数。

## 3. Column reference / 3. 列说明

### 3.1 `campaign_events.csv`
`event_id` (GRA-/AND-/JNT-EVT-####) · `candidate_id` · `event_date` (ISO or `unknown`) ·
`event_time` · `event_title` · `event_category` · `city` · `venue` · `state_region` ·
`event_status` · `campaign_phase` · `stated_purpose` (what the campaign said it was for) ·
`observable_function` (what the record shows happened) · `analyst_interpretation` ·
`target_audience` · `main_messages` · `policy_issues` · `speech_summary` · `transcript_url` ·
`video_url` · `photo_urls` · `media_coverage` · `opponent_reference` · `visual_notes` ·
`source_urls` · `verification_status` · `actor_note` · `vacancy_context` · `analyst_notes`

`stated_purpose` 与 `observable_function` 必须分开：前者是竞选方的说法，后者是记录显示的实际功能。两者相同的情况本身就是一个发现。

### 3.2 `policy_positions.csv`
`pos_id` · `candidate_id` · `issue` · `position_summary` · `verbatim_quote` · `statement_date` ·
`context` · `source_urls` · `verification_status` · `legislative_record` · `position_changed` ·
`change_notes` · `policy_claims` · `source` · `notes`

`legislative_record` is `unknown` for all 34 Andrews rows because she has held no office; it is a
real record for Graham's Senate votes and bill sponsorships. `position_changed = yes` requires two
dated statements that conflict — not a change of emphasis inferred by the analyst.

`legislative_record` 在安德鲁斯全部 34 行为 `unknown`，因为她未担任过公职；对格雷厄姆的参议院表决与法案联署则是真实记录。`position_changed = yes` 要求两条有日期的陈述相互冲突，而非分析师推断的语气变化。

### 3.3 `county_results.csv`
One row per county: `county`, `andrews_votes`, `andrews_pct`, `graham_votes`, `graham_pct`,
`whitener_votes`, `whitener_pct`, `hackett_votes`, `hackett_pct`, `writein_votes`, `total_votes`,
`winner`, `region`, `source_urls`, `verification_status`, `notes`.

The 46 county totals sum to 2,041,487, which equals the statewide total — the reconciliation is
documented in [`../07_electoral_context/results_notes.md`](../07_electoral_context/results_notes.md).
One source cell for Edgefield literally reads `10.821` (a full stop where a comma belongs); the
component sum is 10,821 and that is what the table records.

46 个县的总和等于全州总数 2,041,487，对账过程见 `results_notes.md`。Edgefield 的来源单元格字面写作 `10.821`（应为逗号处写成句点）；各分项之和为 10,821，表中即记录该值。

### 3.4 `sources.csv`
`source_id` · `url` · `title` · `publisher` · `publication_date` · `event_date` · `access_date` ·
`source_tier` · `source_type` · `relevant_quote_or_info` · `reliability_notes` · `used_by`

`used_by` is computed, not asserted: the merge scans every CSV and Markdown file in the archive for
each `SRC-####` and lists the files that cite it. `unknown` there means the source is registered
background that no delivered row cites.

`used_by` 是计算出来的，不是断言的：合并脚本扫描档案内每个 CSV 与 Markdown 文件中的 `SRC-####`，列出引用它的文件。该列为 `unknown` 表示该来源是已登记的背景资料，没有交付行引用它。

### 3.5 `keyframes_identity.csv`
`frame_id` · `identity` · `identity_sim` · `second_identity` · `second_sim` · `faces` ·
`candidate_faces` · `identity_note`

`identity` is one of `ANDREWS`, `GRAHAM`, `unknown`, `other`, `noface`, `nofile`. It comes from an
SFace cosine comparison against 23 photographs already in `04_visual_archive/` (12 Andrews, 11
Graham), filtered so that only photographs where the candidate's face fills at least 3% of the frame
are used as references. A face is labelled with a candidate only if its best cosine reaches **0.363**
(OpenCV's published SFace threshold) and beats the other candidate by **0.05**. Everything else is
`unknown`, which is why 156 of 300 frames carry no candidate label: a debate frame contains a
moderator, an audience and two candidates, and only the faces that clear both tests are attributed.

Sanity figures from the run: same-class reference pairs average 0.740 cosine, cross-class 0.104. As an
independent check, 136 frames come from videos in which only one candidate appears; 3 of them (2.2%)
carry the other candidate's label, which is the archive's working estimate of the false-positive rate.

`identity` 取值 `ANDREWS`、`GRAHAM`、`unknown`、`other`、`noface`、`nofile`。来源是对
`04_visual_archive/` 中 23 张照片（安德鲁斯 12、格雷厄姆 11）做 SFace 余弦比对，且只采用候选人脸部占画幅
至少 3% 的照片作为参照。只有最佳余弦达到 **0.363**（OpenCV 公布的 SFace 阈值）且领先另一候选人 **0.05**
时，才把该脸标注为某位候选人；其余一律 `unknown`——所以 300 帧里有 156 帧没有候选人标签：一场辩论帧里同时有
主持人、观众与两位候选人，只有通过双重检验的脸才被归属。

本次运行的合理性数据：同类参照对平均余弦 0.740，跨类 0.104。独立检验：来自「只出现一位候选人」视频的 136 帧中，
有 3 帧（2.2%）带上了另一候选人的标签，这就是本档案对误报率的经验估计。

## 4. Controlled vocabularies / 4. 受控词表

| Field / 字段 | Legal values / 合法取值 |
|---|---|
| `candidate_id` | `ANDREWS`, `GRAHAM` |
| `event_status` | `held`, `cancelled`, `postponed`, `rescheduled`, `virtual`, `announced`, `unverified`, `disputed` |
| `campaign_phase` | `pre_launch`, `launch`, `primary`, `special_primary`, `runoff`, `general`, `early_voting`, `gotv`, `election_day`, `post_election` |
| `state_region` | `Upstate`, `Midlands`, `Pee Dee`, `Lowcountry`, `Grand Strand`, `statewide`, `national`, `unknown` |
| `verification_status` | `verified`, `partially verified`, `unverified`, `conflicting sources` |
| `source_tier` | `T1`, `T2`, `T3` |
| `source_type` | `official_campaign`, `official_government`, `candidate_social`, `news_article`, `news_video`, `transcript`, `op_ed`, `fact_check`, `poll`, `press_release`, `event_page`, `photo`, `podcast`, `encyclopedia`, `government_record`, `social_media`, `unknown`, `other` |
| `coverage_type` | `news_report`, `analysis`, `op_ed`, `fact_check`, `interview`, `live_blog`, `newsletter`, `news_video` |
| `sponsor_type` | `candidate_campaign`, `authorized_committee`, `outside_pac`, `party_committee`, `unknown` |
| `completeness` | `full`, `partial`, `clip`, `unknown` |
| `copyright_status` | `public_domain`, `licensed`, `all_rights_reserved_link_only`, `unknown` |
| `vacancy_context` | `pre_vacancy`, `vacancy`, `post_appointment`, `post_runoff`, `general`, `unknown` |
| `winner` | `yes`, `no`, `unknown` |
| `mentions_opponent` / `opponent_reference` | `yes`, `no`, `unknown` |
| `position_changed` | `yes`, `no`, `unknown` |
| `transcript_available` | `yes`, `no`, `unknown` |
| `issue` | `Economy`, `Healthcare`, `Education`, `Immigration`, `Abortion`, `Gun policy`, `Energy`, `Religion`, `Labor`, `Democracy`, `Foreign policy`, `Other` |

`encyclopedia`, `government_record`, `social_media`, `unknown` and `other` were **added to
`source_type` during this build**. The first three were needed because the collection streams
register Wikipedia pages, `.gov` records and social posts as sources, and forcing them into
`news_article` would have misdescribed them. The extension is a documented deviation from the
conventions, not an accident.

`encyclopedia`、`government_record`、`social_media`、`unknown`、`other` 是**本次构建中新增到 `source_type` 的取值**。前三者是必要的：采集流把维基百科页面、`.gov` 记录与社交帖子登记为来源，把它们强行归入 `news_article` 会造成错误描述。该扩展是对研究规范的有记录偏离，不是疏漏。

## 5. Id scheme / 5. 编号规则

| Prefix / 前缀 | Meaning / 含义 |
|---|---|
| `AND-POS-####`, `GRA-POS-####` | policy positions |
| `AND-TL-####`, `GRA-TL-####` | career timelines |
| `AND-EVT-####`, `GRA-EVT-####`, `JNT-EVT-####` | events; `JNT` marks a joint/format event such as a debate |
| `AND-SPC-####`, `GRA-SPC-####` | speeches |
| `AND-IMG-####`, `GRA-IMG-####` | images |
| `COV-####` | media coverage |
| `AD-####`, `EXT-AD-####` | candidate ads, outside-money entries |
| `POST-####` | social posts |
| `AND-FIN-####`, `GRA-FIN-####`, `OTH-FIN-####` | finance; `OTH` keeps non-principal candidates out of the two-value schema |
| `EXIT-####` | exit-poll subgroups |
| `AND-SOC-####` | social entries created by the Lead |

Source blocks: `SRC-0001–0399` candidate research, `0400–0599` candidate/positions stream,
`0600–0799` visual stream, `0800–1099` speeches stream, `1100–1499` media/finance stream,
`1500–1699` electoral stream, `1700–1899` video stream, `1900+` Lead research and the video
corpus registered at `2200+`. Blocks are not contiguous: a stream that produced fewer sources than
its allocation leaves a hole, and holes are harmless because ids are opaque.

来源号段：`0001–0399` 候选人研究、`0400–0599` 候选人/立场流、`0600–0799` 视觉流、`0800–1099` 演讲流、`1100–1499` 媒体/财务流、`1500–1699` 选举流、`1700–1899` 视频流、`1900+` 主研究与 `2200+` 视频语料。号段不连续：产出少于配额的流会留下空号，而空号无害，因为 id 是不透明的。

## 6. Tier rules / 6. 等级规则

`T1` — official records: `.gov` domains (FEC, South Carolina Election Commission, Congress,
Senate), and the state's public broadcaster (SCETV) for debate video. · `T2` — established news
organisations with editorial standards, including the state's major papers and the networks. ·
`T3` — everything else: party and advocacy sites, aggregators, polls published by the sponsoring
firm, social posts, Wikipedia, and unclassified domains.

`T1`——官方记录：`.gov` 域（FEC、南卡选举委员会、国会、参议院），以及辩论视频的州公共广播机构 SCETV。`T2`——有编辑标准的既有新闻机构，包括州内主要报纸与全国电视网。`T3`——其余：政党与倡议组织网站、聚合站、由委托机构自行发布的民调、社交帖子、维基百科，以及未分类域名。

Tier is assigned from the **domain**, mechanically, in the merge script. It describes the venue,
not the accuracy of any particular claim. Wikipedia is `T3` by rule even where it is the most
complete account of the race, and every dataset built from it says so.

等级在合并脚本中由**域名**机械判定。它描述的是发表场所，而非任何具体主张的准确性。按规则维基百科为 `T3`，即使它是这场选举最完整的记述；所有据其构建的数据集都注明了这一点。

## 7. 口径 rules that prevent wrong arithmetic / 7. 防止算错的口径规则

1. Candidate-committee totals and outside independent expenditures are **never summed**. They
   live in `campaign_finance.csv` and `advertisements.csv` respectively.
2. Primary-round vote totals are per-round and cannot be added across rounds: the same voters
   appear in the 08-11 special primary and the 08-25 runoff.
3. County rows sum to the statewide total exactly; any future edit must preserve that identity.
4. Percentages are as published. Where a source publishes only votes, the percentage is derived
   and flagged in `notes`.

1. 候选人委员会总额与外部独立支出**绝不相加**，分别存放于 `campaign_finance.csv` 与 `advertisements.csv`。
2. 各轮初选票数是分轮的，不能跨轮相加：同一批选民同时出现在 08-11 特别初选与 08-25 决选中。
3. 县级行精确加总为全州总数；今后任何修改都必须保持该恒等式。
4. 百分比按来源发表值记录。来源只给票数时，百分比为推算值并在 `notes` 中标注。

## 8. Known deviations from the conventions / 8. 与研究规范的已知偏离

| Deviation / 偏离 | Why / 原因 |
|---|---|
| `campaign_events.csv` has 28 rows against a 70-row target | The record contains almost no dated, located appearances; padding would have broken traceability. Documented in `event_coverage_gaps.md`. |
| `campaign_finance.csv` has 5 rows against a 30-row target | Only four FEC snapshots are quoted in the retrievable sources; quarterly line items are not. Non-principal candidates live in `other_candidates_finance.csv`. |
| `source_type` vocabulary extended | See §4. |
| Video corpus registered at `SRC-2200+`, outside the allocated `1700` block | The video stream delivered no source table; the Lead registered the corpus instead of leaving 27 videos uncitable. |
| No frame captions | No vision-language model was available in this environment; frames are described by measurable properties only. |
| `media_coverage.csv` titles and framings come from the media stream | The Lead's parallel build produced a thinner index and was discarded in favour of the fuller file. |

| 偏离 | 原因 |
|---|---|
| `campaign_events.csv` 为 28 行，目标 70 行 | 记录中几乎没有带日期、带地点的露面；填充会破坏可追溯性。详见 `event_coverage_gaps.md`。 |
| `campaign_finance.csv` 为 5 行，目标 30 行 | 可检索来源只引用了四个 FEC 时点；季度明细未获取。非主要候选人存放于 `other_candidates_finance.csv`。 |
| `source_type` 词表扩展 | 见 §4。 |
| 视频语料登记在 `SRC-2200+`，超出分配的 `1700` 号段 | 视频流未交付来源表；主研究选择登记语料，而不是让 27 个视频无法被引用。 |
| 无帧解说词 | 本环境无视觉语言模型；帧只以可测量属性描述。 |
| `media_coverage.csv` 的标题与框架来自媒体流 | 主研究并行构建的索引更单薄，已弃用，改用更完整的文件。 |

## Sources / 来源

- [SRC-2108] `https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_South_Carolina`
- `_research_conventions.md` — the binding contract this dictionary documents
