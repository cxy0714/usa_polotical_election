---
title: "Research Conventions — Case Study 001 (2026 Texas U.S. Senate)"
title_zh: "研究规范——案例研究 001（2026 年得克萨斯州联邦参议员选举）"
language: en+zh
---

# Research Conventions — Case Study 001 (2026 Texas U.S. Senate) / 研究规范——案例研究 001（2026 年得克萨斯州联邦参议员选举）

中文前言：本文件以中英双语呈现，两个语言版本具有同等约束力。凡中文译文与英文原文在含义、范围或强度上出现任何分歧，一律以英文原文为准；中文译文不得被援引以削弱、扩大或替代英文规则。

**This file is the integration contract. Every agent must follow it exactly so the Lead can merge datasets without rework.**

**本文件是整合契约。每位分析员都必须严格遵守，以便负责人（Lead）能够在不返工的情况下合并数据集。**

Working root: `texas-senate-2026/`
Reference date for "access date" fields: use the actual date you performed the search (ISO 8601).

工作根目录：`texas-senate-2026/`
「访问日期」（access date）字段的参考日期：使用你实际执行检索当天的日期（ISO 8601）。

---

## 0. Non-negotiable rules / 0. 不可谈判的规则

1. **Never invent** a date, venue, quotation, dollar figure, endorsement, photo URL or poll number. If it is not in a source you actually retrieved, it does not go in the archive.
   **绝不虚构**任何日期、场地、引语、金额、背书、照片 URL 或民调数字。若某项内容不在你实际检索到的来源中，它就不能进入本档案。
2. **Unknown is a value.** Use `unknown` (lowercase) in CSV cells and `⚠ unknown` in Markdown. Never leave a cell blank when a value is expected; never substitute a guess.
   **`unknown` 是一个取值。** 在 CSV 单元格中使用 `unknown`（小写），在 Markdown 中使用 `⚠ unknown`。在应有取值时绝不将单元格留空；绝不以猜测替代。
3. **Every row carries at least one source.** The `source_urls` / `source_url` cell holds one or more `SRC-####` ids from `09_sources/sources.csv`, plus the raw URL for the most important one. Format: `SRC-0007|https://...`.
   **每一行至少携带一个来源。** `source_urls` / `source_url` 单元格存放一个或多个来自 `09_sources/sources.csv` 的 `SRC-####` 编号，并附上其中最重要一条的原始 URL。格式：`SRC-0007|https://...`。
4. **Separate what was said from what an analyst infers.** Stated purpose, observable function and analyst interpretation are three distinct columns/sections.
   **把「所述」与「分析者所推断」区分开来。** 陈述目的（stated purpose）、可观察功能（observable function）与分析者解读（analyst interpretation）是三个彼此独立的列／章节。
5. **Announcement ≠ event.** A press release announcing a rally is an *announcement* row (`event_status = announced`). Only mark `held` when there is evidence it took place. Verified cancellations go in with `event_status = cancelled` and the cancellation source.
   **宣布不等于活动。** 宣布一场集会的新闻稿是一行*宣布*记录（`event_status = announced`）。只有在有证据表明活动确实发生时，才标记为 `held`。经核实的取消以 `event_status = cancelled` 记录，并附上取消的来源。
6. **Distinguish campaign-produced material from independent media.** Ads/videos made by the campaign, by an outside PAC, or by a news outlet get different `sponsor_type` values.
   **区分竞选团队制作的材料与独立媒体。** 由竞选团队、外部政治行动委员会（outside PAC）或新闻机构制作的广告／视频，分别使用不同的 `sponsor_type` 取值。
7. **Copyright:** do **not** download copyrighted news photographs into the repo. Record metadata + source URL only. Download only assets that are public domain (e.g. official U.S. government / Texas Legislature portraits, federal works) or explicitly licensed. When in doubt: link, don't copy.
   **版权：** **不要**将受版权保护的新闻照片下载到仓库中。只记录元数据＋来源 URL。仅下载属于公有领域（例如美国政府／得克萨斯州议会的官方肖像、联邦作品）或已获明确许可的素材。存疑时：只链接，不复制。
8. **No premature conclusions.** Do not rank the candidates, score their branding, or declare a winner of the "communication contest". Descriptive observation only; strategic interpretation must be labelled as interpretation.
   **不作过早结论。** 不得为候选人排名、为其品牌打分，也不得宣布 "communication contest"（译：传播竞赛）的胜者。只作描述性观察；策略性解读必须标注为解读。
9. Do not write the blog post or video script. This is an evidence archive.
   不要撰写博客文章或视频脚本。这是一份证据档案。

---

## 1. Identifier schemes (zero-padded, stable, never reused) / 1. 标识符方案（零填充、稳定、永不复用）

| Entity / 实体 | Prefix / 前缀 | Example / 示例 |
|---|---|---|
| Campaign event / 竞选活动 | `TAL-EVT-0001` / `PAX-EVT-0001` | `PAX-EVT-0042` |
| Joint / cross-candidate event (debate, joint appearance) / 联合／跨候选人活动（辩论、联合露面） | `JNT-EVT-0001` | `JNT-EVT-0003` |
| Speech / interview / video appearance / 演讲／采访／视频露面 | `TAL-SPC-0001` / `PAX-SPC-0001` | `TAL-SPC-0011` |
| Advertisement / 广告 | `TAL-AD-0001` / `PAX-AD-0001` / `EXT-AD-0001`（外部团体） | `PAX-AD-0007` |
| Image / 图像 | `TAL-IMG-0001` / `PAX-IMG-0001` | `TAL-IMG-0063` |
| Source / 来源 | `SRC-0001`（单一全局序列，由负责人维护） | `SRC-0128` |

Agents may **reserve blocks** to avoid collisions: A `0001–0499`, B `0500–0799`, C `0800–1099`, D `1100–1399`, E `1400–1699`. Lead uses `1700+` and owns `SRC-*` allocation for integration rows.

分析员可以**预留号段**以避免冲突：A 为 `0001–0499`，B 为 `0500–0799`，C 为 `0800–1099`，D 为 `1100–1399`，E 为 `1400–1699`。负责人使用 `1700+`，并负责整合行中 `SRC-*` 的分配。

Because the global `SRC-*` sequence is Lead-owned, agents should **write their sources to their own staging file** (see §7) using local ids, and the Lead will reconcile into `09_sources/sources.csv`. In the meantime, `source_urls` cells may carry raw URLs prefixed by a local tag, e.g. `SRC-0012|https://...`. Lead will rewrite these to `SRC-####` at integration.

由于全局 `SRC-*` 序列由负责人维护，分析员应**将来源写入各自的过渡文件**（见 §7），使用本地编号，再由负责人归并进 `09_sources/sources.csv`。在此期间，`source_urls` 单元格可携带以本地标签为前缀的原始 URL，例如 `SRC-0012|https://...`。负责人在整合时会将其改写为 `SRC-####`。

---

## 2. Controlled vocabularies (use exactly these strings) / 2. 受控词表（必须使用这些确切字符串）

**candidate_id:** `TALARICO` | `PAXTON`

**candidate_id（候选人 ID）：** 该字段只接受 `TALARICO` 或 `PAXTON` 两个取值，须逐字照用，不得改写。

**event_status:** `held` | `cancelled` | `postponed` | `rescheduled` | `virtual` | `announced` (not yet confirmed as held) | `unverified` | `disputed`

**event_status（活动状态）：** 必须严格使用上述英文取值；其中 `announced` 指尚未确认已实际举行的活动，其余取值沿用英文原词，不得翻译。

**campaign_phase:** `pre_launch` | `launch` | `primary` | `runoff` | `general` | `early_voting` | `gotv` | `election_day` | `post_election`

**campaign_phase（竞选阶段）：** 必须严格使用上述英文取值，不得翻译或改写。

Note: the GOP `runoff` phase applies to Paxton; Talarico's Democratic primary had no runoff phase — for Talarico use `primary` through the runoff calendar period, but record the phase label as `primary`.

注：共和党的 `runoff` 阶段适用于帕克斯顿；塔拉里科的民主党初选没有决选阶段——对塔拉里科而言，在决选对应的日历期间仍沿用 `primary`，但阶段标签记为 `primary`。

**event_category:** `launch` | `announcement` | `rally` | `town_hall` | `meet_and_greet` | `community_visit` | `small_business_visit` | `workplace_visit` | `university_visit` | `religious_appearance` | `labor_event` | `party_event` | `county_party_meeting` | `q_and_a` | `interview_tv` | `interview_radio` | `podcast` | `newspaper_interview` | `livestream` | `debate` | `debate_invitation` | `press_conference` | `video_release` | `tour_stop` | `tour_launch` | `tour_finale` | `fundraiser` | `endorsement_event` | `hq_opening` | `early_voting_event` | `gotv_event` | `surrogate_event` | `election_eve` | `watch_party` | `victory_speech` | `concession_speech` | `other`

**event_category（活动类别）：** 完整取值见上方英文行。写入 CSV 时必须逐字使用其中的英文字符串，不得翻译、改写或缩写；中文对照只出现在双语数据字典中。

**verification_status:** `verified` (≥1 independent Tier-2 source or official primary record) | `partially verified` (Tier-3/social only, or primary source only) | `unverified` (single weak claim) | `conflicting sources`

**verification_status（核实状态）：** `verified`（至少一个独立的 Tier-2 来源或官方一手记录） | `partially verified`（仅有 Tier-3／社交来源，或仅有一手来源） | `unverified`（单一薄弱说法） | `conflicting sources`（来源相互冲突）

**source tier:** `T1` primary/official | `T2` established independent media | `T3` supplementary (blogs, newsletters, public calendars, third-party social)

**source tier（来源层级）：** `T1` 一手／官方 | `T2` 成熟的独立媒体 | `T3` 补充性来源（博客、通讯、公开日历、第三方社交内容）

**source_type:** `official_campaign` | `official_government` (SOS, FEC, legislature) | `candidate_social` | `news_article` | `news_video` | `transcript` | `op_ed` | `fact_check` | `poll` | `press_release` | `event_page` | `photo` | `podcast` | `other`

**source_type（来源类型）：** 必须严格使用上述英文取值；其中 `official_government` 指州务卿（SOS）、联邦选举委员会（FEC）、立法机构等官方来源。

**sponsor_type (ads):** `candidate_campaign` | `authorized_committee` | `outside_pac` | `party_committee` | `unknown`

**sponsor_type（广告赞助方类型）：** `candidate_campaign`（候选人竞选团队） | `authorized_committee`（授权委员会） | `outside_pac`（外部政治行动委员会） | `party_committee`（政党委员会） | `unknown`（未查明）

---

## 3. CSV schemas — use these headers verbatim / 3. CSV 模式——必须逐字使用这些表头

CSV rules: UTF-8, RFC-4180 quoting (quote any cell containing comma, quote or newline), `\n` line endings, header row required, no blank cells (use `unknown`).

CSV 规则：UTF-8 编码、RFC-4180 引号处理（凡单元格含逗号、引号或换行，均须加引号）、`\n` 换行、必须有表头行、不得有空单元格（用 `unknown` 填充）。

### `02_campaign_events/campaign_events.csv` / 竞选活动表
```
event_id,candidate_id,event_date,event_time,event_title,event_category,city,venue,state_region,event_status,campaign_phase,stated_purpose,observable_function,analyst_interpretation,target_audience,main_messages,policy_issues,speech_summary,transcript_url,video_url,photo_urls,media_coverage,opponent_reference,visual_notes,source_urls,verification_status,analyst_notes
```
- `event_date` ISO `YYYY-MM-DD`; if only month known use `YYYY-MM` and say so in analyst_notes. If unknown use `unknown`.
- `event_date` 使用 ISO `YYYY-MM-DD`；若只能确定月份，使用 `YYYY-MM` 并在 analyst_notes 中说明。若无法确定，使用 `unknown`。
- `event_time` local Texas time, 24h `HH:MM`, else `unknown`.
- `event_time` 为得克萨斯州当地时间，24 小时制 `HH:MM`；否则 `unknown`。
- `opponent_reference`: `yes` | `no` | `unknown` — did the candidate mention the opponent?
- `opponent_reference`：`yes` | `no` | `unknown`——候选人是否提及对手？
- `state_region`: one of `East Texas` | `North Texas` | `Central Texas` | `South Texas` | `West Texas` | `Gulf Coast` | `Panhandle` | `statewide` | `national` | `unknown`
- `state_region`：取值为以下之一：`East Texas` | `North Texas` | `Central Texas` | `South Texas` | `West Texas` | `Gulf Coast` | `Panhandle` | `statewide` | `national` | `unknown`（须逐字照用，不得翻译）。

### `01_candidates/talarico/career_timeline.csv` and `paxton/career_timeline.csv` / 两位候选人的职业时间线表
```
entry_id,candidate_id,start_date,end_date,role_or_event,organization,location,description,source_urls,verification_status
```

### `policy_positions.csv` (Lead merges to `01_candidates/<name>/political_positions.md`; canonical CSV at root of `01_candidates/`) / 政策立场表（由负责人合并至 `01_candidates/<name>/political_positions.md`；规范 CSV 位于 `01_candidates/` 根目录）
```
position_id,candidate_id,issue,subissue,position_summary,candidate_statement,statement_date,context,source_urls,legislative_record,position_changed,change_notes,opponent_criticism,fact_check,verification_status
```
`issue` must be one of: `Economy` | `Healthcare` | `Education` | `Immigration` | `Abortion` | `Gun policy` | `Energy` | `Religion` | `Labor` | `Democracy` | `Foreign policy` | `Other`.

`issue` 必须为以下之一：`Economy` | `Healthcare` | `Education` | `Immigration` | `Abortion` | `Gun policy` | `Energy` | `Religion` | `Labor` | `Democracy` | `Foreign policy` | `Other`（须逐字照用，不得翻译或改写大小写）。

### `03_speeches/speech_archive.csv` / 演讲档案表
```
speech_id,candidate_id,event_id,date,speech_title,speech_url,transcript_url,duration,main_topics,major_quotes,rhetorical_devices,opponent_references,personal_story_elements,policy_claims,source_urls,source,verification_status
```
`major_quotes` — pipe-delimited `"quote" [hh:mm:ss]`. Only verbatim quotes you actually saw/heard in a retrieved source; otherwise paraphrase and mark `(paraphrase)`.

`major_quotes`——以竖线分隔的 `"quote" [hh:mm:ss]`。只收录你在已检索来源中实际看到／听到的逐字引语；否则改写并标注 `(paraphrase)`（译：改写）。

### `03_speeches/speech_video_index.csv` / 演讲视频索引表
```
video_id,candidate_id,video_url,date,duration,event_type,main_topics,relevant_timestamps,transcript_available,visual_observations,completeness,source_urls,verification_status
```
`completeness`: `full` | `partial` | `clip` | `unknown`

`completeness`：`full` | `partial` | `clip` | `unknown`（完整／部分／片段／未查明；写入时须使用英文原词）。

### `05_campaign_media/advertisements.csv` / 广告表
```
ad_id,candidate_id,sponsor,sponsor_type,release_date,title,platform,length_seconds,issue_or_message,main_visual_elements,narration_soundtrack,candidate_appearance,main_claims,video_url,transcript_url,fact_check,media_coverage,source_urls,verification_status,notes
```

### `05_campaign_media/social_media.csv` / 社交媒体表
```
post_id,candidate_id,platform,account_handle,post_date,post_type,content_summary,media_included,engagement_notes,url,verification_status,notes
```

### `05_campaign_media/media_coverage.csv` / 媒体报道表
```
coverage_id,candidate_id,event_id,publication_date,outlet,author,title,url,source_tier,coverage_type,key_framing,notable_quotes,framing_of_candidate,mentions_opponent,reliability_notes
```
`coverage_type`: `news_report` | `analysis` | `op_ed` | `fact_check` | `interview` | `live_blog` | `newsletter` | `news_video`

`coverage_type`：`news_report` | `analysis` | `op_ed` | `fact_check` | `interview` | `live_blog` | `newsletter` | `news_video`（须逐字照用英文原词）。

### `06_campaign_finance/campaign_finance.csv` / 竞选财务表
```
finance_id,candidate_id,period,report_type,reporting_deadline,receipts,individual_contributions,pac_contributions,disbursements,cash_on_hand,debts_owed,source_urls,verification_status,notes
```
Dollar amounts: plain integers, no `$` or commas. `unknown` where not disclosed. Cite FEC filing or reputable reporting on the filing.

金额：使用纯整数，不带 `$` 符号、不加千位逗号。未披露的写 `unknown`。须引用 FEC 申报文件或对该申报的可靠报道。

### `04_visual_archive/image_archive.csv` / 图像档案表
```
image_id,candidate_id,image_date,event_id,event_category,source_name,source_url,original_image_url,photographer,copyright_status,license,local_filename,image_resolution,framing,camera_angle,image_quality,face_visibility,body_visibility,clothing_notes,notes,verification_status
```
`copyright_status`: `public_domain` | `licensed` | `all_rights_reserved_link_only` | `unknown`. `local_filename` = `unknown` unless an actual permitted copy exists.

`copyright_status`：`public_domain` | `licensed` | `all_rights_reserved_link_only` | `unknown`。除非确实存在获准保存的副本，否则 `local_filename` = `unknown`。

### `07_electoral_context/election_results.csv` / 选举结果表
```
race_id,race_name,election_date,candidate,party,votes,percentage,winner,source_urls,verification_status,notes
```

### `07_electoral_context/county_results.csv` / 县级结果表
```
county_id,county,candidate_talarico_votes,candidate_paxton_votes,other_votes,talarico_pct,paxton_pct,total_votes,source_urls,verification_status
```

### `07_electoral_context/polling.csv` / 民调表
```
poll_id,pollster,sponsor,field_start,field_end,population,sample_size,margin_of_error,talarico_pct,paxton_pct,other_pct,undecided_pct,leader,margin,source_urls,verification_status,notes
```

### `09_sources/sources.csv` (Lead-owned master) / 来源总表（由负责人维护）
```
source_id,url,title,publisher,publication_date,event_date,access_date,source_tier,source_type,relevant_quote_or_info,reliability_notes,used_by
```

---

## 4. Markdown deliverables — required structure / 4. Markdown 交付物——必需结构

Every biography / analysis `.md` starts with YAML front matter:
```yaml
---
title:
candidate_id:
compiled_by:
last_updated:
status: draft | in_progress | complete
coverage_note: <one line on what is solid vs thin>
---
```
Then: sections with `##` headings, inline citations as `[SRC-####]` or raw markdown links, and a final `## Sources` list. Tables are encouraged for chronology.

每一份传记／分析类 `.md` 文件都以 YAML 前置元数据开头：
```yaml
---
title:
candidate_id:
compiled_by:
last_updated:
status: draft | in_progress | complete
coverage_note: <one line on what is solid vs thin>
---
```
随后是：以 `##` 为层级的章节、以 `[SRC-####]` 或原始 Markdown 链接形式给出的行内引用，以及结尾的 `## Sources` 列表。时间线类内容建议使用表格。

---

## 5. Event purpose: the three-layer rule / 5. 活动目的：三层规则

For each event, fill **all three** and never blur them:
- `stated_purpose` — what the campaign/candidate *explicitly said* it was for (quote the press release/announcement or write `unknown`).
- `observable_function` — what the activity *actually was* (e.g. "45-minute stump speech to ~120 people in a union hall, then 10 minutes of press questions").
- `analyst_interpretation` — labelled inference, prefixed `INTERPRETATION:`.

对每一项活动，**三层都必须填写**，且绝不可混淆：
- `stated_purpose`（陈述目的）——竞选团队／候选人*明确表示*该活动所为何事（引用新闻稿／公告，或写 `unknown`）。
- `observable_function`（可观察功能）——该活动*实际是什么*（例如 "45-minute stump speech to ~120 people in a union hall, then 10 minutes of press questions"，译：在工会大厅向约 120 人作 45 分钟竞选演说，随后 10 分钟媒体提问）。
- `analyst_interpretation`（分析者解读）——带标注的推断，以 `INTERPRETATION:` 为前缀。

In Markdown, use a three-row table instead:

在 Markdown 中，改用三行表格：

| Layer / 层级 | Content / 内容 | Evidence / 证据 |
|---|---|---|
| Stated purpose / 陈述目的 | | |
| Observable function / 可观察功能 | | |
| Analyst interpretation / 分析者解读 | | |

---

## 6. Verification workflow / 6. 核实流程

For each important claim: find ≥1 Tier-1 or Tier-2 source. Where two sources conflict, record both and set `verification_status = conflicting sources`, then describe the conflict in `research_gaps.md` (agents append to their own staging gaps file; Lead merges).

对每一项重要主张：找到至少一个 Tier-1 或 Tier-2 来源。若两个来源相互冲突，两者都记录，并设置 `verification_status = conflicting sources`，然后在 `research_gaps.md` 中描述该冲突（分析员将内容追加到各自的过渡空缺文件，由负责人合并）。

Known friction to expect and how to handle:
- Paywalled articles (NYT, WaPo): the search-result snippet and headline may be all you can retrieve. Record what the snippet supports, mark `partially verified`, and note the paywall in `reliability_notes`. Do not fabricate body text.
- `web_fetch` may fail or return nav junk. Retry once; if it still fails, rely on the search-result summary and mark accordingly.
- Social posts are frequently deleted or unretrievable → `unverified`, note "post not retrievable".

可能遇到的已知摩擦及处理方式：
- 付费墙文章（NYT、WaPo）：你可能只能取到搜索结果摘要与标题。记录摘要所能支持的内容，标记为 `partially verified`，并在 `reliability_notes` 中注明付费墙。不得编造正文内容。
- `web_fetch` 可能失败或返回导航等垃圾内容。重试一次；若仍然失败，依据搜索结果摘要，并相应标注。
- 社交帖子经常被删除或无法检索 → 记为 `unverified`，并注明 "post not retrievable"（译：帖子无法检索）。

---

## 7. Staging files (each agent's isolated write scope) / 7. 过渡文件（每位分析员隔离的写入范围）

Each agent writes *only* its own files plus one staging file, to keep parallel writes disjoint:

每位分析员*只*写自己的文件外加一个过渡文件，以保持并行写入互不交叉：

- **Agent A** → `02_campaign_events/*`, staging: `_staging/A_sources.csv`, `_staging/A_gaps.md`
  **A 号分析员** → `02_campaign_events/*`，过渡文件：`_staging/A_sources.csv`、`_staging/A_gaps.md`
- **Agent B** → `01_candidates/**`, `01_candidates/policy_positions.csv`, staging: `_staging/B_sources.csv`, `_staging/B_gaps.md`
  **B 号分析员** → `01_candidates/**`、`01_candidates/policy_positions.csv`，过渡文件：`_staging/B_sources.csv`、`_staging/B_gaps.md`
- **Agent C** → `04_visual_archive/**`, staging: `_staging/C_sources.csv`, `_staging/C_gaps.md`
  **C 号分析员** → `04_visual_archive/**`，过渡文件：`_staging/C_sources.csv`、`_staging/C_gaps.md`
- **Agent D** → `03_speeches/**`, staging: `_staging/D_sources.csv`, `_staging/D_gaps.md`
  **D 号分析员** → `03_speeches/**`，过渡文件：`_staging/D_sources.csv`、`_staging/D_gaps.md`
- **Agent E** → `05_campaign_media/**`, `06_campaign_finance/**`, staging: `_staging/E_sources.csv`, `_staging/E_gaps.md`
  **E 号分析员** → `05_campaign_media/**`、`06_campaign_finance/**`，过渡文件：`_staging/E_sources.csv`、`_staging/E_gaps.md`
- **Lead** → `README.md`, `09_sources/sources.csv`, `07_electoral_context/**`, `08_comparative_analysis/**`, `research_gaps.md`, `_research_conventions.md`
  **负责人（Lead）** → `README.md`、`09_sources/sources.csv`、`07_electoral_context/**`、`08_comparative_analysis/**`、`research_gaps.md`、`_research_conventions.md`

Never edit a file outside your scope. If you need a change elsewhere, message the Lead.

绝不编辑你负责范围之外的文件。若需要在别处改动，请联系负责人。

---

## 8. Coverage-parity requirement (§14.1 of the brief) / 8. 覆盖对等要求（任务书 §14.1）

Every agent must deliver **comparable depth for both candidates**. If Paxton coverage is thinner than Talarico (or vice versa), do not pad with speculation — instead record the asymmetry explicitly in your gaps file with the reason (e.g. "fewer independent event listings; campaign site offline"). Asymmetry is a finding, not a failure.

每位分析员都必须为两位候选人提供**可比的深度**。若帕克斯顿的覆盖比塔拉里科单薄（或相反），不得以推测填充——而应在你的空缺文件中明确记录这一不对称及其原因（例如 "fewer independent event listings; campaign site offline"，译：可独立核查的活动列表更少；竞选网站离线）。不对称是一项发现，而非失败。
