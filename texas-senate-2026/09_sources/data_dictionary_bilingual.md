---
title: "Bilingual data dictionary — all CSV datasets"
title_zh: "双语数据字典 —— 全部 CSV 数据集"
language: en+zh
compiled_by: Lead Research Agent
last_updated: 2026-11-10
status: complete
coverage_note: >-
  English-Chinese reference for every CSV field name and controlled-vocabulary value in
  texas-senate-2026/. The CSVs themselves intentionally keep English field names and English
  vocabulary values so that they stay machine-readable and schema-stable; this document is
  where their Chinese equivalents live.
---

# Bilingual data dictionary / 双语数据字典

**Why this file exists.** The CSV datasets are the machine-readable backbone of the
archive: their field names and controlled-vocabulary values stay in English so that
the data remains schema-stable, joinable and validatable. Translating values *inside*
cells (for example turning `verified` into 已核实) would break every validator, join and
script. This document is therefore the Chinese reading layer: every field name, every
controlled value and every measurement caveat is glossed here, so a Chinese-speaking
analyst can read any CSV accurately without the data being mutated.

**本文件的作用。** CSV 数据集是本档案的机器可读骨架：字段名与受控词表取值一律保持英文，以保证结构稳定、可连接、可校验。若把单元格里的取值翻译成中文（例如把 `verified` 写成"已核实"），所有校验脚本、表连接与自动化都会失效。因此本文件充当"中文阅读层"：逐字段、逐取值给出中文释义，并说明全部度量口径陷阱，使中文读者能准确读懂任何一张 CSV，而数据本身不被改写。

---

## 1. Reading rules / 阅读规则

1. **字段名与取值保持英文**，中文释义见下文表格；不要在原 CSV 内改写成中文。
   Field names and values stay English; look up the Chinese gloss here. Never translate
   inside the CSV.
2. **`unknown` 表示"未能查明"**，不是 0、不是"无"、不是"否"。凡见 `unknown`，即表示该事实
   在本档案的检索范围内无法确立，须保持不确定。
   `unknown` means "not established" — not zero, not none, not no.
3. **同一行内的数字不得跨行相加**，除非该表明确声明同一口径（详见第 6 节）。
   Never sum numbers across rows of different measurement constructs (§6).
4. **凡字段内出现 `SRC-####|URL` 形式**，表示该行引用了 `09_sources/sources.csv` 中的来源条目；
   `|` 之前是来源编号，之后是该来源的 URL 副本，便于离线阅读。
   `SRC-####|URL` pairs point into `09_sources/sources.csv`.
5. **核实状态字段**在各表中一致使用四个取值，见 §4.1。
   The verification field uses the same four values in every table (§4.1).

## 2. ID schemes / 编号体系

| Prefix / 前缀 | Meaning / 含义 | Example / 示例 |
|---|---|---|
| `TAL-EVT-####` | 塔拉里科阵营事件的唯一编号 / Talarico-campaign event | `TAL-EVT-0012` |
| `PAX-EVT-####` | 帕克斯顿阵营事件 / Paxton-campaign event | `PAX-EVT-0007` |
| `JNT-EVT-####` | 双方共同出现的活动（如辩论邀请类） / joint or cross-campaign item | `JNT-EVT-0001` |
| `TAL-SPC-####` / `PAX-SPC-####` | 演讲条目编号 / speech record | `TAL-SPC-1105` |
| `TAL-IMG-####` / `PAX-IMG-####` | 影像条目编号 / image record | `PAX-IMG-0808` |
| `TAL-AD-####` / `PAX-AD-####` / `EXT-AD-####` | 广告编号：候选人阵营／外部团体 / ad record: campaign / outside group | `EXT-AD-0004` |
| `TAL-SM-####` / `PAX-SM-####` | 社交媒体帖子编号 / social-media post record | `TAL-SM-0003` |
| `FIN-####` | 财务条目编号 / finance record | `FIN-0042` |
| `SRC-####` | 来源总表编号 / master source record | `SRC-0168` |
| `MC-####` | 媒体覆盖条目编号 / media-coverage record | `MC-0021` |

编号一经分配不再改变；已废弃编号（如 `PAX-IMG-0801`）不得复用。
IDs are permanent; retired IDs (e.g. `PAX-IMG-0801`) must not be reused.

## 3. Dataset-by-dataset field glosses / 逐表字段释义

### 3.1 `02_campaign_events/campaign_events.csv` — 93 rows / 93 行

核心交付物：双方全部有据可查的竞选活动。The core deliverable: every publicly
documented campaign activity for both candidates.

| Field / 字段 | Chinese / 中文 | Notes / 说明 |
|---|---|---|
| `event_id` | 事件编号 | 见 §2 |
| `candidate_id` | 候选人 | `TALARICO` / `PAXTON` |
| `event_date` | 日期 | `YYYY-MM-DD`；不确定时为 `unknown` |
| `event_time` | 时间 | 24 小时制；多数为 `unknown` |
| `event_title` | 事件名称 | 尽量用原文标题 |
| `event_category` | 事件类别 | 见 §4.2 |
| `city` | 城市 | 英文原名 |
| `venue` | 场地 | 英文原名；未载明为 `unknown` |
| `state_region` | 州内区域 | 见 §4.3 |
| `event_status` | 活动状态 | 见 §4.4 |
| `campaign_phase` | 竞选阶段 | 见 §4.5 |
| `stated_purpose` | 宣称目的 | 阵营自己陈述的目的 |
| `observable_function` | 可观察功能 | 从报道可观察到的实际功能 |
| `analyst_interpretation` | 分析者解读 | 推断，前缀 `INTERPRETATION:` |
| `target_audience` | 目标受众 | 依证据编码 |
| `main_messages` | 主要讯息 | 多条以 `;` 分隔 |
| `policy_issues` | 涉及议题 | 对应 `policy_positions.csv` 的 `issue` |
| `speech_summary` | 讲话摘要 | 转述，非逐字稿 |
| `transcript_url` | 文字稿链接 | 多数 `unknown` |
| `video_url` | 视频链接 | 多数 `unknown` |
| `photo_urls` | 照片出处 | 多为图片说明文字所载摄影者 |
| `media_coverage` | 相关报道 | `MC-####` 或媒体名 |
| `opponent_reference` | 是否提及对手 | `yes` / `no` / `unknown` |
| `visual_notes` | 视觉记录 | 只写"报道/图注明确记载"的视觉细节 |
| `source_urls` | 来源 | `SRC-####|URL` |
| `verification_status` | 核实状态 | 见 §4.1 |
| `analyst_notes` | 分析者备注 | 冲突、缺口、退役理由等 |

### 3.2 `01_candidates/policy_positions.csv` — 146 rows / 146 行

| Field / 字段 | Chinese / 中文 | Notes / 说明 |
|---|---|---|
| `position_id` | 立场编号 | |
| `candidate_id` | 候选人 | |
| `issue` | 议题 | 12 类，见 §4.6 |
| `subissue` | 子议题 | 自由文本 |
| `position_summary` | 立场摘要 | 档案自身的归纳 |
| `candidate_statement` | 候选人原话 | 英文原文 |
| `statement_date` | 表述日期 | 多数 `unknown` |
| `context` | 语境 | 在何种场合、回应何种问题 |
| `source_urls` | 来源 | |
| `legislative_record` | 立法/履职记录 | 与口头立场可能不一致，故单列 |
| `position_changed` | 立场是否变化 | `yes` / `no` / `unknown` |
| `change_notes` | 变化说明 | |
| `opponent_criticism` | 对手批评 | 仅记录"有据可查的批评" |
| `fact_check` | 事实核查 | 有核查来源者注明 |
| `verification_status` | 核实状态 | |

### 3.3 `03_speeches/speech_archive.csv` — 32 rows / 32 行

| Field / 字段 | Chinese / 中文 | Notes / 说明 |
|---|---|---|
| `speech_id` | 演讲编号 | |
| `candidate_id` | 候选人 | |
| `event_id` | 对应事件 | 多数 `unknown`（演讲与事件未能一一对应） |
| `date` | 日期 | |
| `speech_title` | 演讲标题 | |
| `speech_url` | 演讲链接 | |
| `transcript_url` | 文字稿 | 仅 1 份为真实文字稿 |
| `duration` | 时长 | |
| `main_topics` | 主要议题 | |
| `major_quotes` | 关键引语 | 英文原文 |
| `rhetorical_devices` | 修辞手法 | 分析者标注 |
| `opponent_references` | 对手提及 | |
| `personal_story_elements` | 个人叙事要素 | |
| `policy_claims` | 政策主张 | |
| `source_urls` | 来源 | |
| `source` | 主要依据 | 报道来源名称 |
| `verification_status` | 核实状态 | |

### 3.4 `03_speeches/speech_video_index.csv` — 31 rows / 31 行

| Field / 字段 | Chinese / 中文 | Notes / 说明 |
|---|---|---|
| `video_id` | 视频编号 | |
| `candidate_id` | 候选人 | |
| `video_url` | 视频链接 | |
| `date` | 日期 | |
| `duration` | 时长 | |
| `event_type` | 活动类型 | 见 §4.7 |
| `main_topics` | 主要议题 | |
| `relevant_timestamps` | 相关时间点 | 有明确时间码者方记录 |
| `transcript_available` | 是否有文字稿 | `yes` / `no` |
| `visual_observations` | 视觉观察 | **均为外部描述，非本档案目视所得** |
| `completeness` | 完整度 | 见 §4.8 |
| `source_urls` | 来源 | |
| `verification_status` | 核实状态 | |

### 3.5 `04_visual_archive/image_archive.csv` — 116 rows / 116 行

| Field / 字段 | Chinese / 中文 | Notes / 说明 |
|---|---|---|
| `image_id` | 影像编号 | |
| `candidate_id` | 候选人 | |
| `image_date` | 拍摄日期 | 部分为近似日期 |
| `event_id` | 对应事件 | 仅 15 行可对应到 2026 竞选事件 |
| `event_category` | 事件类别 | |
| `source_name` | 来源机构 | |
| `source_url` | 来源页面 | |
| `original_image_url` | 原图链接 | |
| `photographer` | 摄影者 | 署名信息 |
| `copyright_status` | 版权状态 | 见 §4.9 |
| `license` | 许可协议 | `CC BY-SA 4.0` 等，英文原名 |
| `local_filename` | 本地文件名 | 仅链接行为 `unknown` |
| `image_resolution` | 原始分辨率 | 依原图元数据 |
| `framing` | 构图 | **全部 `unknown`**（未目视） |
| `camera_angle` | 机位角度 | **全部 `unknown`**（未目视） |
| `image_quality` | 影像质量分级 | 依原始分辨率，非观感评价 |
| `face_visibility` | 面部可见度 | **全部 `unknown`**（未目视） |
| `body_visibility` | 身体可见度 | **全部 `unknown`**（未目视） |
| `clothing_notes` | 着装记录 | **全部 `unknown`**：无来源描述着装 |
| `notes` | 备注 | |
| `verification_status` | 核实状态 | |

⚠ **该表不含任何外貌、面部几何或着装判断。** 详见 `04_visual_archive/visual_analysis_*.md`。
This table contains no appearance, facial-geometry or clothing judgement.

### 3.6 `05_campaign_media/advertisements.csv` — 23 rows / 23 行

| Field / 字段 | Chinese / 中文 | Notes / 说明 |
|---|---|---|
| `ad_id` | 广告编号 | |
| `candidate_id` | 归属候选人 | 外部团体广告归其攻击对象或受益方，见 `notes` |
| `sponsor` | 投放主体 | 竞选团队或政治行动委员会原名 |
| `sponsor_type` | 投放主体类型 | 见 §4.10 |
| `release_date` | 发布日 | |
| `title` | 标题 | |
| `platform` | 平台 | |
| `length_seconds` | 时长（秒） | |
| `issue_or_message` | 议题/讯息 | |
| `main_visual_elements` | 主要视觉元素 | 依据报道描述 |
| `narration_soundtrack` | 旁白/配乐 | |
| `candidate_appearance` | 候选人是否出镜 | |
| `main_claims` | 主要宣称 | 英文原文，尽量逐字 |
| `video_url` | 视频链接 | |
| `transcript_url` | 文字稿 | |
| `fact_check` | 事实核查结论 | |
| `media_coverage` | 相关报道 | |
| `source_urls` | 来源 | |
| `verification_status` | 核实状态 | |
| `notes` | 备注 | |

### 3.7 `05_campaign_media/social_media.csv` — 12 rows / 12 行

| Field / 字段 | Chinese / 中文 | Notes / 说明 |
|---|---|---|
| `post_id` | 帖子编号 | |
| `candidate_id` | 候选人 | 注意政党账号发帖不算候选人本人，见 `notes` |
| `platform` | 平台 | |
| `account_handle` | 账号 | |
| `post_date` | 发布日期 | 部分为近似值 |
| `post_type` | 帖子类型 | 见 §4.11 |
| `content_summary` | 内容摘要 | |
| `media_included` | 是否含图文/视频 | |
| `engagement_notes` | 互动数据 | 多为缺失；有则为阵营宣称 |
| `url` | 链接 | 多数未抓到固定链接 |
| `verification_status` | 核实状态 | |
| `notes` | 备注 | |

### 3.8 `05_campaign_media/media_coverage.csv` — 66 rows / 66 行

| Field / 字段 | Chinese / 中文 | Notes / 说明 |
|---|---|---|
| `coverage_id` | 报道编号 | |
| `candidate_id` | 报道对象 | |
| `event_id` | 对应事件 | 多数 `unknown` |
| `publication_date` | 发表日期 | |
| `outlet` | 媒体 | 共 47 家 |
| `author` | 作者 | |
| `title` | 标题 | |
| `url` | 链接 | |
| `source_tier` | 来源层级 | 见 §4.12 |
| `coverage_type` | 报道类型 | 见 §4.13 |
| `key_framing` | 核心框架 | 分析者归纳，非报道原句 |
| `notable_quotes` | 显著引语 | 英文原文 |
| `framing_of_candidate` | 对候选人的定位 | |
| `mentions_opponent` | 是否提及对手 | |
| `reliability_notes` | 可靠性备注 | 本表不设单一核实字段 |

### 3.9 `06_campaign_finance/campaign_finance.csv` — 69 rows / 69 行

| Field / 字段 | Chinese / 中文 | Notes / 说明 |
|---|---|---|
| `finance_id` | 财务条目编号 | |
| `candidate_id` | 候选人 | |
| `period` | 申报期 | 16 个 FEC 申报期，2025-04-01 → 2026-10-14 |
| `report_type` | 报表类型 | 见 §4.14 |
| `reporting_deadline` | 申报截止日 | |
| `receipts` | 总收入 | 美元 |
| `individual_contributions` | 个人捐款 | 美元 |
| `pac_contributions` | PAC 捐款 | 美元 |
| `disbursements` | 总支出 | 美元 |
| `cash_on_hand` | 期末现金 | 美元 |
| `debts_owed` | 负债 | 双方均为 0 |
| `source_urls` | 来源 | |
| `verification_status` | 核实状态 | |
| `notes` | 备注 | **口径差异在此说明，务必阅读** |

⚠ 本表同时容纳 FEC 申报、FEC 独立支出、AdImpact 广告监测与阵营宣称四类**不可相加**的数据（§6）。
This table mixes four non-summable measurement constructs (§6).

### 3.10 `07_electoral_context/election_results.csv` — 12 rows / 12 行

| Field / 字段 | Chinese / 中文 | Notes / 说明 |
|---|---|---|
| `race_id` | 选举编号 | `TX-SEN-GENERAL` 等 |
| `race_name` | 选举名称 | |
| `election_date` | 选举日 | |
| `candidate` | 候选人 | |
| `party` | 政党 | `Democratic` / `Republican` / `Other` |
| `votes` | 得票数 | |
| `percentage` | 得票率 | |
| `winner` | 是否胜出 | `yes` / `no` / `runoff_advanced` |
| `source_urls` | 来源 | |
| `verification_status` | 核实状态 | |
| `notes` | 备注 | **含部分计票与最终计票的区别，切勿混用** |

### 3.11 `07_electoral_context/polling.csv` — 11 rows / 11 行

| Field / 字段 | Chinese / 中文 | Notes / 说明 |
|---|---|---|
| `poll_id` | 民调编号 | |
| `pollster` | 执行机构 | |
| `sponsor` | 委托方 | 党派委托须注明 |
| `field_start` / `field_end` | 调查起止日 | |
| `population` | 调查对象 | 如 `likely voters`（可能投票者） |
| `sample_size` | 样本量 | |
| `margin_of_error` | 误差范围 | |
| `talarico_pct` / `paxton_pct` | 双方支持率 | |
| `other_pct` / `undecided_pct` | 其他/未决定 | |
| `leader` | 领先者 | |
| `margin` | 差距 | |
| `source_urls` | 来源 | |
| `verification_status` | 核实状态 | |
| `notes` | 备注 | |

### 3.12 `07_electoral_context/county_results.csv` — 0 rows / 0 行（有意留空）

**空表是设计结果，不是错误。** 县级计票通过 JavaScript 交互页面发布，本次检索无法执行；
维基百科条目只有县级地图而无数据表。字段已定义，供后续补齐：
**The empty table is deliberate.** County tabulation was served through JavaScript
interactives that could not be executed. Fields are pre-defined for later completion.

`county_id`（县编号）、`county`（县名）、`candidate_talarico_votes`（塔拉里科得票）、
`candidate_paxton_votes`（帕克斯顿得票）、`other_votes`（其他人得票）、
`talarico_pct`（得票率）、`paxton_pct`（得票率）、`total_votes`（总票数）、
`source_urls`（来源）、`verification_status`（核实状态）。

### 3.13 辅助表 / auxiliary tables

| File / 文件 | Fields / 字段（中文） |
|---|---|
| `01_candidates/*/career_timeline.csv` | `entry_id` 条目编号、`candidate_id` 候选人、`start_date`/`end_date` 起止日期、`role_or_event` 职务或事件、`organization` 机构、`location` 地点、`description` 说明、`source_urls` 来源、`verification_status` 核实状态 |
| `09_sources/sources.csv` | `source_id` 来源编号、`title` 标题、`publisher` 出版方、`url` 链接、`publication_date` 发表日期、`source_tier` 层级、`source_type` 类型、`used_in` 被用于哪些文件、`retrieved_via` 抓取方式、`reliability_notes` 可靠性备注、`accessed_date` 访问日期、`notes` 备注 |

## 4. Controlled vocabularies / 受控词表中文对照

### 4.1 `verification_status` 核实状态（全表通用）

| Value | 中文 | 含义 |
|---|---|---|
| `verified` | 已核实 | 有可靠来源直接支持，且未见冲突 |
| `partially verified` | 部分核实 | 核心事实有据，但细节（时间、场地、原话、数字）不完整或有单一来源 |
| `conflicting sources` | 来源冲突 | 有据可查的来源彼此不一致；冲突原样保留，不做取舍 |
| `unverified` | 未核实 | 有线索但无法以现有工具确立；不得当成已确认事实使用 |

### 4.2 `event_category` 事件类别（18 项）

| Value | 中文 |
|---|---|
| `announcement` | 参选宣布 |
| `launch` | 启动集会 |
| `rally` | 集会 |
| `tour_launch` | 巡回宣传启动 |
| `tour_stop` | 巡回宣传站点 |
| `tour_finale` | 巡回宣传收官 |
| `town_hall` | 市政厅式问答 |
| `debate_invitation` | 辩论邀请/辩论争议条目 |
| `interview_tv` | 电视采访 |
| `university_visit` | 校园活动 |
| `religious_appearance` | 宗教场合露面 |
| `endorsement_event` | 背书活动 |
| `surrogate_event` | 代理人活动 |
| `gotv_event` | 催票活动 |
| `watch_party` | 观选派对 |
| `victory_speech` | 胜选演说 |
| `concession_speech` | 承认败选演说 |
| `other` | 其他 |

### 4.3 `state_region` 州内区域

`Central Texas` 中德州、`East Texas` 东德州、`Gulf Coast` 墨西哥湾沿岸、`North Texas` 北德州、
`Panhandle` 狭长地带、`South Texas` 南德州、`West Texas` 西德州、`national` 全国性、
`statewide` 全州、`unknown` 未查明。

### 4.4 `event_status` 活动状态

| Value | 中文 | 含义 |
|---|---|---|
| `held` | 已举行 | 有证据显示确实发生 |
| `announced` | 已宣布 | 仅见宣布，未见举行证据 |
| `cancelled` | 已取消 | 有明确取消记录（帕克斯顿 5 项） |
| `disputed` | 存疑 | 宣布与执行证据冲突 |

### 4.5 `campaign_phase` 竞选阶段

`launch` 启动期、`primary` 初选期、`runoff` 决选期、`general` 大选期、
`early_voting` 提前投票期、`gotv` 催票期、`post_election` 选后期。

### 4.6 `issue` 议题类别（12 项）

`Abortion` 堕胎、`Democracy` 民主与廉政、`Economy` 经济、`Education` 教育、
`Energy` 能源、`Foreign policy` 外交、`Gun policy` 枪支政策、`Healthcare` 医疗、
`Immigration` 移民、`Labor` 劳工与商业、`Religion` 宗教、`Other` 其他。

### 4.7 `event_type` 视频活动类型（speech_video_index）

`community_visit` 社区走访、`concession_speech` 败选演说、`gotv_event` 催票、
`interview_tv` 电视采访、`launch` 启动、`podcast` 播客、`rally` 集会、
`religious_appearance` 宗教场合、`tour_finale` 巡回收官、`tour_launch` 巡回启动、
`tour_stop` 巡回站点、`town_hall` 市民问答、`victory_speech` 胜选演说、`video_release` 视频发布。

### 4.8 `completeness` 完整度

`full` 完整、`partial` 部分、`clip` 片段、`unknown` 未查明。

### 4.9 `copyright_status` 版权状态

| Value | 中文 | 使用规则 |
|---|---|---|
| `public_domain` | 公有领域 | 可下载保存 |
| `licensed` | 已获许可（CC） | 可下载保存，须保留署名与许可信息 |
| `all_rights_reserved_link_only` | 保留所有权利，仅链接 | **只记录链接与署名，不复制文件** |

### 4.10 `sponsor_type` 投放主体类型

`candidate_campaign` 候选人竞选团队、`outside_pac` 外部政治行动委员会。

### 4.11 `post_type` 帖子类型

`text post` 纯文字、`photo post` 图片、`video post` 视频、`quote-post with video` 引用配视频、
`reply post` 回复、`merchandise promotion post` 周边商品推广、
`aggregate account performance (not a single post)` 账号整体表现（非单条帖子）、`unknown` 未查明。

### 4.12 `source_tier` 来源层级

| Tier | 中文 | 说明 |
|---|---|---|
| `T1` | 一级 | 官方记录、法院/政府文件、FEC/州务卿、候选人官方发布 |
| `T2` | 二级 | 主流新闻机构报道 |
| `T3` | 三级 | 党派媒体、评论、二手汇编 |
| `pointer_only` | 仅指针 | 确认报道存在但未抓到 URL，补齐前不可引用 |

### 4.13 `coverage_type` 报道类型

`news_report` 新闻报道、`news_video` 新闻视频、`analysis` 分析、`op_ed` 评论、
`fact_check` 事实核查、`live_blog` 实时博客。

### 4.14 `report_type` 财务报表类型

涵盖 FEC 季度/月度申报、选前申报、独立支出（Schedule E）、AdImpact 广告监测数据、
阵营对外宣称数字等；**不同类型不可相加**，`notes` 字段逐行说明口径。

## 5. What "unknown" hides / `unknown` 背后的具体缺口

| Where / 出现位置 | What is missing / 缺失内容 |
|---|---|
| `campaign_events.event_time` | 多数活动的开始时间未载明 |
| `campaign_events.transcript_url` | 无逐字稿；引语来自报道 |
| `image_archive.framing` / `camera_angle` | 未目视图像，无法判断构图与机位 |
| `image_archive.face_visibility` / `body_visibility` / `clothing_notes` | 未目视且无来源描述 |
| `speech_video_index.relevant_timestamps` | 无可靠时间码 |
| `social_media.url` | 未能抓到固定链接 |
| `campaign_finance` 部分行 | 官方逐条申报文件无法抓取 |

## 6. Measurement traps / 度量口径陷阱（务必遵守）

1. **FEC 独立支出（Schedule E）≠ AdImpact 广告投放额。** 两者相差约一个数量级；
   例：某团体 FEC 记录 2,496 万美元，而 AdImpact 口径可达 1.821 亿美元。**绝不可相加或互相替代。**
2. **塔拉里科存在四种"总额"**：阵营宣称累计 1.343 亿、FEC 捐款 1.403 亿、
   FEC 总收入 1.463 亿、含联合筹款委员会约 1.55 亿。各自口径不同。
3. **帕克斯顿第三季度"1,800 万美元"** 含两个联合筹款委员会，主委员会为 1,024.9 万美元。
4. **选举夜 66% 计票的 59.4% 不是结果**，只是部分计票；最终为 55.06%。
5. **帕克斯顿巡回宣传"30+ 站"** 为阵营宣称；某地方媒体称"12 站之一"，两者并存。
6. **"三场已排定辩论"** 系某媒体误报，从未发生，不得列入事件表。

## 7. Sources / 来源

本字典的定义均来自 `_research_conventions.md` 与各数据集实际取值，不引入外部来源。
Definitions derive from `_research_conventions.md` and the datasets' actual values; no
external sources are introduced here.
