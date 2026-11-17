---
title: "Research Conventions — Case Study 002 (2026 South Carolina U.S. Senate)"
title_zh: "研究规范——案例研究 002（2026 年南卡罗来纳州联邦参议员选举）"
language: en+zh
last_updated: 2026-11-12
---

# Research Conventions — Case Study 002 (2026 South Carolina U.S. Senate) / 研究规范——案例研究 002（2026 年南卡罗来纳州联邦参议员选举）

中文前言：本文件以中英双语呈现，两个语言版本具有同等约束力。凡中文译文与英文原文在含义、范围或强度上出现任何分歧，一律以英文原文为准；中文译文不得被援引以削弱、扩大或替代英文规则。

**This file is the integration contract for `south-carolina-senate-2026/`. It is a sibling of Case Study 001 (`texas-senate-2026/`) and deliberately reuses its data contract, with the five additions listed in §1.1.**

**本文件是 `south-carolina-senate-2026/` 的整合契约。它与案例研究 001（`texas-senate-2026/`）同源，刻意复用其数据契约，并加入第 1.1 节列出的五项扩展。**

Working root: `south-carolina-senate-2026/`
Reference date for "access date" fields: the actual date you performed the search (ISO 8601). Today is **2026-11-12** for most work in this session.

工作根目录：`south-carolina-senate-2026/`
「访问日期」（access date）字段的参考日期：使用你实际执行检索当天的日期（ISO 8601）。本次工作大多数情况下的「今天」为 **2026-11-12**。

---

## 0. The race, for orientation / 0. 选情速览（用于定位）

| Item / 项目 | Value / 取值 |
|---|---|
| Race / 选举 | 2026 U.S. Senate, South Carolina (Class 2) / 2026 年南卡罗来纳州联邦参议员（第 2 组） |
| Election day / 投票日 | 2026-11-03 |
| Democratic nominee / 民主党提名人 | **Annie Andrews** — pediatrician, MUSC; 2022 nominee for SC-01 / 儿科医生，2022 年 SC-01 提名人 |
| Republican nominee / 共和党提名人 | **Darline Graham** (Darline Lettie Graham Nordone) — appointed 2026-07-13, sworn in 07-14, sister of Lindsey Graham / 2026-07-13 受任命、07-14 宣誓就职，林赛·格雷厄姆之妹 |
| Result / 结果 | Andrews 1,044,001 (51.14%) — Graham 952,191 (46.64%) / 安德鲁斯 1,044,001 票（51.14%）— 格雷厄姆 952,191 票（46.64%） |
| Minor nominees / 小党提名 | Mark Hackett (Constitution), Kasie Whitener (Libertarian), Catherine Fleming Bruce (write-in) / 宪法党、自由党、写名候选人 |
| Structural peculiarity / 结构特殊性 | The Republican nominee changed **after** the June primary: Lindsey Graham won the 06-09 primary, died 07-11, and a special primary + runoff (08-11, 08-25) nominated his sister. / 共和党提名人在 6 月初选**之后**发生更替：林赛·格雷厄姆赢下 06-09 初选、07-11 去世，经 08-11 特别初选与 08-25 决选改由其妹出线。 |

This last row is the single most important structural fact of Case Study 002 and must be carried by
every timeline, comparison table and coverage register. It has no counterpart in Case Study 001.

最后一行是案例研究 002 最重要的结构性事实，必须体现在每一份时间线、对比表与报道登记中。案例研究 001 中没有对应情形。

---

## 1. Non-negotiable rules / 1. 不可谈判的规则

1. **Never invent** a date, venue, quotation, dollar figure, endorsement, photo URL or poll number. If it is not in a source you actually retrieved, it does not go in the archive.
   **绝不虚构**任何日期、场地、引语、金额、背书、照片 URL 或民调数字。若某项内容不在你实际检索到的来源中，它就不能进入本档案。
2. **Unknown is a value.** Use `unknown` (lowercase) in CSV cells and `⚠ unknown` in Markdown. Never leave a cell blank when a value is expected; never substitute a guess.
   **`unknown` 是一个取值。** 在 CSV 单元格中使用 `unknown`（小写），在 Markdown 中使用 `⚠ unknown`。在应有取值时绝不将单元格留空；绝不以猜测替代。
3. **Every row carries at least one source.** The `source_urls` cell holds one or more `SRC-####` ids from `09_sources/sources.csv`, plus the raw URL for the most important one. Format: `SRC-0007|https://...`.
   **每一行至少携带一个来源。** `source_urls` 单元格存放一个或多个来自 `09_sources/sources.csv` 的 `SRC-####` 编号，并附上其中最重要一条的原始 URL。格式：`SRC-0007|https://...`。
4. **Separate what was said from what an analyst infers.** `stated_purpose` / `observable_function` / `analyst_interpretation` are three distinct columns. Interpretation is prefixed `INTERPRETATION:`.
   **把「所述」与「分析者所推断」区分开来。** `stated_purpose`／`observable_function`／`analyst_interpretation` 是三个彼此独立的列。解读须以 `INTERPRETATION:` 为前缀。
5. **Announcement ≠ event.** A press release announcing a rally is an *announcement* row (`event_status = announced`). Only mark `held` when there is evidence it took place. Verified cancellations go in with `event_status = cancelled` and the cancellation source.
   **宣布不等于活动。** 宣布一场集会的新闻稿是一行*宣布*记录（`event_status = announced`）。只有在有证据表明活动确实发生时，才标记为 `held`。经核实的取消以 `event_status = cancelled` 记录，并附上取消的来源。
6. **Distinguish campaign-produced material from independent media.** Campaign, outside PAC and newsroom material get different `sponsor_type` values.
   **区分竞选团队制作的材料与独立媒体。** 竞选团队、外部政治行动委员会与新闻机构的材料使用不同的 `sponsor_type` 取值。
7. **Copyright:** do **not** download copyrighted news photographs into the repo. Record metadata + source URL only. Download only assets that are public domain (official U.S. government / Senate portraits, federal works) or explicitly licensed. When in doubt: link, don't copy.
   **版权：** **不要**将受版权保护的新闻照片下载到仓库中。只记录元数据＋来源 URL。仅下载属于公有领域（美国政府／参议院官方肖像、联邦作品）或已获明确许可的素材。存疑时：只链接，不复制。
8. **No premature conclusions.** Do not rank the candidates, score their branding, or declare a winner of the "communication contest". Descriptive observation only; strategic interpretation must be labelled as interpretation.
   **不作过早结论。** 不得为候选人排名、为其品牌打分，也不得宣布「传播竞赛」的胜者。只作描述性观察；策略性解读必须标注为解读。
9. **Do not write the blog post or video script.** This is an evidence archive.
   不要撰写博客文章或视频脚本。这是一份证据档案。
10. **Graham's incumbency is dated, not assumed.** Any row that treats her as "the incumbent" must carry the appointment date (2026-07-13) in `analyst_notes` or `notes`; she was a sitting senator for 112 days before the election.
    **格雷厄姆的「现任」身份必须标注日期，不得默认。** 任何把她当作「现任参议员」处理的行，都必须在 `analyst_notes`／`notes` 中写明受任命日期（2026-07-13）；她在选举前仅担任参议员 112 天。

### 1.1 Five deliberate extensions over Case Study 001 / 1.1 相对案例研究 001 的五项刻意扩展

| # | Extension / 扩展 | Why / 原因 |
|---|---|---|
| 1 | `07_electoral_context/county_results.csv` is **populated**, not header-only / 该表**实际填充**，不再只有表头 | The SC article publishes a full county table; Texas's did not. / 南卡条目公布了完整县级表，德州条目没有。 |
| 2 | `candidate_id` values are `ANDREWS` and `GRAHAM`; Graham rows may use `GRAHAM` for both the brother's and the sister's actions, disambiguated by `actor_note` / 两处「格雷厄姆」以 `actor_note` 区分 | Lindsey Graham's death and nomination are part of the race; conflating them would corrupt the record. / 林赛·格雷厄姆的去世与提名属于本场选举；混同两者会污染记录。 |
| 3 | Debate rows exist and are `held` / 存在且标记为 `held` 的辩论行 | Unlike Texas, SC held at least one general-election debate; do not copy the Texas "no debate" framing. / 与德州不同，南卡至少举行了一场大选辩论；不得照搬德州「无辩论」的框架。 |
| 4 | `state_region` uses SC regions / 区域词表改为南卡分区 | See §2. / 见第 2 节。 |
| 5 | Every dataset row that concerns the vacancy carries `vacancy_context` / 涉空缺的行带 `vacancy_context` | Values: `pre_vacancy` \| `vacancy` \| `post_appointment` \| `post_runoff` \| `general` \| `unknown`. / 取值见左。 |

`actor_note` is a **free-text** cell, not part of the controlled vocabulary: use `LINDSEY_GRAHAM` or
`DARLINE_GRAHAM` when the row's subject is one specific Graham, and `unknown` when a source says only
"Graham".

`actor_note` 是**自由文本**单元格，不属于受控词表：当该行主体是某一位具体的格雷厄姆时，写 `LINDSEY_GRAHAM` 或 `DARLINE_GRAHAM`；来源仅称「Graham」时写 `unknown`。

---

## 2. Controlled vocabularies (use exactly these strings) / 2. 受控词表（必须使用这些确切字符串）

**candidate_id:** `ANDREWS` | `GRAHAM`

**candidate_id（候选人 ID）：** 仅接受 `ANDREWS` 或 `GRAHAM`。

**event_status:** `held` | `cancelled` | `postponed` | `rescheduled` | `virtual` | `announced` | `unverified` | `disputed`

**campaign_phase:** `pre_launch` | `launch` | `primary` | `special_primary` | `runoff` | `general` | `early_voting` | `gotv` | `election_day` | `post_election`

**campaign_phase（竞选阶段）：** 新增 `special_primary`，用于 2026-08-11 特别初选至 08-25 决选前的区间；`runoff` 用于 08-25 决选及其后至大选前。

**event_category:** identical to Case Study 001, plus `swearing_in` | `memorial` | `appointment_announcement` | `filing` | `debate_withdrawal`

**event_category（活动类别）：** 与案例研究 001 相同，另加左列五项。

**event_category, full list:** `launch` | `announcement` | `rally` | `town_hall` | `meet_and_greet` | `community_visit` | `small_business_visit` | `workplace_visit` | `university_visit` | `religious_appearance` | `labor_event` | `party_event` | `county_party_meeting` | `q_and_a` | `interview_tv` | `interview_radio` | `podcast` | `newspaper_interview` | `livestream` | `debate` | `debate_invitation` | `press_conference` | `video_release` | `tour_stop` | `tour_launch` | `tour_finale` | `fundraiser` | `endorsement_event` | `hq_opening` | `early_voting_event` | `gotv_event` | `surrogate_event` | `election_eve` | `watch_party` | `victory_speech` | `concession_speech` | `swearing_in` | `memorial` | `appointment_announcement` | `filing` | `debate_withdrawal` | `other`

**state_region:** `Upstate` | `Midlands` | `Pee Dee` | `Lowcountry` | `Grand Strand` | `statewide` | `national` | `unknown`

**state_region（区域）：** 南卡惯用分区。Columbia 归 `Midlands`，Charleston/Beaufort 归 `Lowcountry`，Greenville/Spartanburg/Clemson 归 `Upstate`，Florence/Myrtle Beach 一带归 `Pee Dee`／`Grand Strand`（Myrtle Beach、Conway、Georgetown 用 `Grand Strand`）。

**verification_status:** `verified` (≥1 independent Tier-2 source or official primary record) | `partially verified` (Tier-3/social only, or primary source only) | `unverified` (single weak claim) | `conflicting sources`

**source tier:** `T1` primary/official | `T2` established independent media | `T3` supplementary

**source_type:** `official_campaign` | `official_government` | `candidate_social` | `news_article` | `news_video` | `transcript` | `op_ed` | `fact_check` | `poll` | `press_release` | `event_page` | `photo` | `podcast` | `other`

**sponsor_type (ads):** `candidate_campaign` | `authorized_committee` | `outside_pac` | `party_committee` | `unknown`

**coverage_type:** `news_report` | `analysis` | `op_ed` | `fact_check` | `interview` | `live_blog` | `newsletter` | `news_video`

**completeness:** `full` | `partial` | `clip` | `unknown`

**copyright_status:** `public_domain` | `licensed` | `all_rights_reserved_link_only` | `unknown`

**vacancy_context:** `pre_vacancy` | `vacancy` | `post_appointment` | `post_runoff` | `general` | `unknown`

---

## 3. Identifier schemes / 3. 标识符方案

| Entity / 实体 | Prefix / 前缀 |
|---|---|
| Campaign event / 竞选活动 | `AND-EVT-0001` / `GRA-EVT-0001` |
| Joint / cross-candidate event / 联合活动 | `JNT-EVT-0001` |
| Speech / interview / 演讲／采访 | `AND-SPC-0001` / `GRA-SPC-0001` |
| Advertisement / 广告 | `AND-AD-0001` / `GRA-AD-0001` / `EXT-AD-0001` |
| Image / 图像 | `AND-IMG-0001` / `GRA-IMG-0001` |
| Social post / 社交帖 | `AND-SOC-0001` / `GRA-SOC-0001` |
| Coverage item / 报道 | `COV-0001` |
| Finance row / 财务行 | `AND-FIN-0001` / `GRA-FIN-0001` |
| Speech analysis doc / 演讲分析文档 | `AND-SPC-####` matching its `speech_id` |
| Source / 来源 | `SRC-0001` (single global sequence) |

**SRC blocks (to avoid collisions, this replaces Case Study 001's staging-file reconciliation):**
**SRC 号段（用于避免冲突；本档案以此取代案例研究 001 的过渡文件归并流程）：**

| Stream / 线索 | Reserved `SRC-` block / 预留号段 |
|---|---|
| A — events / 事件 | `SRC-0001`–`SRC-0399` |
| B — candidates / 候选人 | `SRC-0400`–`SRC-0599` |
| C — visual / 影像 | `SRC-0600`–`SRC-0799` |
| D — speeches / 演讲 | `SRC-0800`–`SRC-1099` |
| E — media & finance / 媒体与资金 | `SRC-1100`–`SRC-1499` |
| F — electoral context / 选情 | `SRC-1500`–`SRC-1699` |
| Lead — integration & synthesis / 整合与综合 | `SRC-1700`+ |

Write your sources into `_staging/<letter>_sources.csv` with the header in §5 and **only** ids from your
own block. The Lead concatenates the six staging files into `09_sources/sources.csv`. Because ids are
pre-allocated, no token rewriting is required — this is safer than the 001 workflow.

将来源写入 `_staging/<字母>_sources.csv`（表头见第 5 节），并且**只**使用你自己号段内的编号。负责人把六份过渡文件拼接为 `09_sources/sources.csv`。由于号段是预分配的，无需改写标记——这比 001 的流程更稳妥。

---

## 4. CSV schemas — use these headers verbatim / 4. CSV 模式——必须逐字使用这些表头

CSV rules: UTF-8 (no BOM), RFC-4180 quoting, `\n` line endings, header row required, no blank cells
(use `unknown`). Amounts are plain integers without `$` or thousands separators.

CSV 规则：UTF-8（无 BOM）、RFC-4180 引号处理、`\n` 换行、必须有表头行、不得有空单元格（用 `unknown` 填充）。金额为纯整数，不带 `$` 与千位分隔符。

### `02_campaign_events/campaign_events.csv`
```
event_id,candidate_id,event_date,event_time,event_title,event_category,city,venue,state_region,event_status,campaign_phase,stated_purpose,observable_function,analyst_interpretation,target_audience,main_messages,policy_issues,speech_summary,transcript_url,video_url,photo_urls,media_coverage,opponent_reference,visual_notes,source_urls,verification_status,actor_note,vacancy_context,analyst_notes
```
`event_time` is local South Carolina time (Eastern), 24h `HH:MM`.
`event_time` 为南卡当地时间（东部时区），24 小时制 `HH:MM`。

### `01_candidates/policy_positions.csv`
```
position_id,candidate_id,issue,subissue,position_summary,candidate_statement,statement_date,context,source_urls,legislative_record,position_changed,change_notes,opponent_criticism,fact_check,verification_status
```
`issue` ∈ `Economy` | `Healthcare` | `Education` | `Immigration` | `Abortion` | `Gun policy` | `Energy` | `Religion` | `Labor` | `Democracy` | `Foreign policy` | `Other`.

### `01_candidates/<name>/career_timeline.csv`
```
entry_id,candidate_id,start_date,end_date,role_or_event,organization,location,description,source_urls,verification_status
```

### `03_speeches/speech_archive.csv`
```
speech_id,candidate_id,event_id,date,speech_title,speech_url,transcript_url,duration,main_topics,major_quotes,rhetorical_devices,opponent_references,personal_story_elements,policy_claims,source_urls,source,verification_status
```
`major_quotes` — pipe-delimited `"quote" [hh:mm:ss]`. Only verbatim quotes actually seen/heard in a retrieved source; otherwise paraphrase and mark `(paraphrase)`.

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

### `05_campaign_media/social_media.csv`
```
post_id,candidate_id,platform,account_handle,post_date,post_type,content_summary,media_included,engagement_notes,url,verification_status,notes
```

### `05_campaign_media/media_coverage.csv`
```
coverage_id,candidate_id,event_id,publication_date,outlet,author,title,url,source_tier,coverage_type,key_framing,notable_quotes,framing_of_candidate,mentions_opponent,reliability_notes
```

### `06_campaign_finance/campaign_finance.csv`
```
finance_id,candidate_id,period,report_type,reporting_deadline,receipts,individual_contributions,pac_contributions,disbursements,cash_on_hand,debts_owed,source_urls,verification_status,notes
```
**Never sum FEC line items with AdImpact/outside-group spending figures.** Record them in separate rows and say which口径 in `notes`.
**绝不可将 FEC 逐条金额与 AdImpact／外部团体支出额相加。** 分别记行，并在 `notes` 中说明口径。

### `07_electoral_context/election_results.csv`
```
race_id,race_name,election_date,candidate,party,votes,percentage,winner,source_urls,verification_status,notes
```

### `07_electoral_context/county_results.csv`
```
county_id,county,candidate_andrews_votes,candidate_graham_votes,other_votes,andrews_pct,graham_pct,total_votes,source_urls,verification_status
```

### `07_electoral_context/polling.csv`
```
poll_id,pollster,sponsor,field_start,field_end,population,sample_size,margin_of_error,andrews_pct,graham_pct,other_pct,undecided_pct,leader,margin,source_urls,verification_status,notes
```
Primary-era polls that contain neither candidate (e.g. Graham-vs-Norman) go in
`07_electoral_context/primary_polling.csv`. The field was up to ten candidates deep, so the header
keeps one column per candidate that any published poll tested (rather than a generic first/second
pair, which would have silently dropped four candidates):
```
poll_id,race_stage,pollster,sponsor,field_start,field_end,population,sample_size,margin_of_error,graham_pct,norman_pct,fry_pct,lynch_pct,sanford_pct,other_pct,undecided_pct,source_urls,verification_status,notes
```
`race_stage` ∈ `special_primary` | `runoff`. A candidate a poll did not test gets `unknown`, never `0`.
`race_stage` ∈ `special_primary`｜`runoff`。某次民调未测试的候选人填 `unknown`，绝不填 `0`。

### `09_sources/sources.csv` (Lead-owned master) / 来源总表（由负责人维护）
```
source_id,url,title,publisher,publication_date,event_date,access_date,source_tier,source_type,relevant_quote_or_info,reliability_notes,used_by
```

### `_staging/<letter>_sources.csv` (per-stream staging, same columns as above) / 各线索过渡表
Same header as `09_sources/sources.csv`. `used_by` records the stream letter and the ids of the rows
that cite it, e.g. `A: AND-EVT-0007,AND-EVT-0012`.

---

## 5. Markdown deliverables — required structure / 5. Markdown 交付物——必需结构

Every `.md` starts with YAML front matter:
```yaml
---
title:
title_zh:
candidate_id:
compiled_by:
last_updated:
status: draft | in_progress | complete
coverage_note: <one line on what is solid vs thin>
---
```
Then `##` sections, inline citations as `[SRC-####]` or raw markdown links, and a final `## Sources` list.

**Bilingual rule (binding):** every `##` section is written as an English paragraph (or table), followed
immediately by its Chinese counterpart. Structural tables may carry both languages in one cell
(`English / 中文`). English governs where the two diverge.

**双语规则（具约束力）：** 每个 `##` 章节先写英文段落（或表格），紧接着写对应的中文。结构化表格可在同一单元格内并列双语（`English / 中文`）。两者若有分歧，以英文为准。

---

## 6. Event purpose: the three-layer rule / 6. 活动目的：三层规则

Fill **all three**, never blur them:
- `stated_purpose` — what the campaign/candidate *explicitly said* it was for (quote the release, or `unknown`).
- `observable_function` — what the activity *actually was* ("35-minute stump speech to ~80 people in a church hall, then 6 minutes of press questions").
- `analyst_interpretation` — labelled inference, prefixed `INTERPRETATION:`.

For each of the 29 event rows in 001 the same discipline applied; keep it here.
001 中 29 行活动均适用同一纪律；此处照旧。

---

## 7. How to retrieve sources in this session / 7. 本次会话的取源方法

**`web_search` is unavailable (no API key). All retrieval is `web_fetch` on known URLs.** Work from
these anchors, in this order:

**`web_search` 不可用（无 API 密钥）。全部取源依靠对已知 URL 的 `web_fetch`。** 按下列顺序，从这些锚点出发：

1. **Local mirror:** `_staging/mirrors/wiki_sc_senate_2026.wikitext` holds the first ~100 KB of the
   Wikipedia article (sections 1–42). Read it with `read`/`grep`; do not re-fetch it.
   **本地镜像：** 该文件保存维基百科条目开头约 100 KB（第 1–42 节）。用 `read`／`grep` 读取，不要重复抓取。
2. **Section-level fetch for the rest** — the article is ~177 KB, so fetch one section at a time:
   `https://en.wikipedia.org/w/index.php?title=2026_United_States_Senate_election_in_South_Carolina&action=raw&section=N`
   Section index (use it; do not guess):

   | N | Section / 章节 |
   |---|---|
   | 1 | Background |
   | 2–5 | Interim appointment, appointee, considered, declined |
   | 6–12 | Initial Republican primary (candidates, endorsements, fundraising, polling, results) |
   | 13–16 | Initial GOP primary: endorsements / fundraising / polling / results |
   | 17–23 | Special Republican primary: candidates |
   | 24–29 | Special GOP primary: first round (endorsements 25, fundraising 26, polling 27, debates 28, results 29) |
   | 30–35 | Runoff (endorsements 31, fundraising 32, polling 33, debate 34, results 35) |
   | 36–45 | Democratic primary (candidates 37–41, endorsements 42, fundraising 43, polling 44, results 45) |
   | 46–50 | Constitution and Libertarian conventions |
   | 51 | General election (top) |
   | 52 | Predictions |
   | 53 | Post-primary endorsements |
   | 54 | General-election debates |
   | 55 | General-election fundraising |
   | 56 | General-election polling |
   | 57 | General-election results |
   | 58 | **Results by county** |
   | 59 | Analysis |
   | 60 | Exit poll |
   | 62 | References (the URL list — fetch this to harvest outlet links) |
3. **News URLs** harvested from section 62 or from the article body. They are real and fetchable.
   Campaign sites (`drannieandrews.com`, `darlinegraham.com`) return **HTTP 403 (Cloudflare)** — record
   that as a documented gap; do not report their contents as retrieved.
4. **Candidate Wikipedia pages:** `Annie_Andrews`, `Darline_Graham`, `Lindsey_Graham` — same
   `action=raw&section=N` technique.

**Known friction / 已知摩擦：** paywalled outlets (NYT, WaPo) give headline+snippet only → `partially verified` + paywall note. `thestate.com` may be paywalled. `x.com`/Twitter posts are usually unretrievable → `unverified`, "post not retrievable". Do not fabricate body text from a snippet.

付费墙媒体（NYT、WaPo）只能取到标题与摘要 → 记 `partially verified` 并注明付费墙。`thestate.com` 可能同样受限。`x.com`／Twitter 帖通常无法检索 → 记 `unverified`，注明「帖子无法检索」。不得由摘要编造正文。

---

## 8. Staging files and write scope / 8. 过渡文件与写入范围

Each stream writes **only** its own directories plus one staging file:

| Stream | Writes / 写入 | Staging / 过渡 |
|---|---|---|
| A events | `02_campaign_events/*` | `_staging/A_sources.csv`, `_staging/A_gaps.md` |
| B candidates | `01_candidates/**` (incl. `policy_positions.csv`) | `_staging/B_sources.csv`, `_staging/B_gaps.md` |
| C visual | `04_visual_archive/**` | `_staging/C_sources.csv`, `_staging/C_gaps.md` |
| D speeches | `03_speeches/**` | `_staging/D_sources.csv`, `_staging/D_gaps.md` |
| E media+finance | `05_campaign_media/**`, `06_campaign_finance/**` | `_staging/E_sources.csv`, `_staging/E_gaps.md` |
| F electoral | `07_electoral_context/**` | `_staging/F_sources.csv`, `_staging/F_gaps.md` |
| Lead | `README.md`, `09_sources/**`, `08_comparative_analysis/**`, `research_gaps.md`, `_research_conventions.md`, `site/**`, `10_video_frames/**`, `11_speech_audio/**` | `_staging/_lead_*` |

Never edit a file outside your scope. If you need a change elsewhere, say so in your gaps file.
绝不编辑你负责范围之外的文件。若需要在别处改动，写进你的空缺文件。

---

## 9. Depth targets and coverage parity / 9. 深度目标与覆盖对等

Case Study 001 shipped 93 events, 32 speeches, 116 images, 23 ads, 66 coverage items, 69 finance rows
and 189 sources. Aim for **comparable order of magnitude**, not identical counts:

| Dataset | Target minimum / 目标下限 |
|---|---|
| `campaign_events.csv` | 70 rows (≥35 per candidate) |
| `policy_positions.csv` | 80 rows (≥35 per candidate) |
| `speech_archive.csv` | 24 rows (≥10 per candidate) |
| `speech_video_index.csv` | 20 rows |
| `image_archive.csv` | 60 rows (≥25 per candidate) |
| `advertisements.csv` | 14 rows (both campaigns + outside groups) |
| `media_coverage.csv` | 55 rows (≥20 per candidate) |
| `campaign_finance.csv` | 30 rows (≥12 per candidate) |
| `election_results.csv` | ≥10 rows (primaries, special primary, runoff, general) |
| `county_results.csv` | ≥40 rows (46 counties; both-candidate rows) |
| `polling.csv` | ≥8 rows |
| `sources.csv` | ≥120 unique sources |

**Where a target cannot be met from retrievable sources, ship what is documented and record the shortfall
in your gaps file with the reason.** Never pad with invented rows. Asymmetry between the two candidates
is a finding, not a failure.

**若某一下限无法由可检索来源支撑，则交付有据可查的部分，并在空缺文件中记录缺口与原因。** 绝不以虚构行填充。两位候选人之间的覆盖不对称是一项发现，而非失败。
