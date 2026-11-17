---
title: "Research gaps — what could not be retrieved, and why"
title_zh: "研究缺口——无法检索的内容及其原因"
compiled_by: Lead Research Agent
last_updated: 2026-11-12
status: complete
coverage_note: "Environment failures are recorded as environment failures. Nothing here is a content judgement about either campaign."
---

# Research gaps / 研究缺口

## 1. Environmental limits / 1. 环境限制

| Limit / 限制 | Effect on this archive / 对本档案的影响 |
|---|---|
| `drannieandrews.com` and `darlinegraham.com` return HTTP 403 (Cloudflare) | No campaign schedule, platform page, press release or ad library from either side. Every "what the campaign said" cell rests on third-party reporting. |
| `dgraham.senate.gov` and the NRLC release also 403 | Graham's own Senate communications are absent; her positions rest on one bill, one vote, four committee assignments, one debate remark. |
| Shell TLS is broken (`SEC_E_NO_CREDENTIALS`) for `curl.exe` and `Invoke-WebRequest` | Only Python `urllib` with an explicit User-Agent reached the network. Bulk HTML retrieval of 300+ outlets was not practical, so coverage bodies were largely not read. |
| No `web_search` tool in this session (no API key) | Discovery relied on yt-dlp search and a Wikipedia citation crawl. Anything not cited by the race article or searchable on YouTube is outside the archive. |
| Wikimedia 429s during image download | 41 of 48 images stored locally; the other 7 are link-only. |
| No vision-language model locally | Frames are described by measurable properties (scene position, face count, box area), not captions. |
| No `ffprobe`; ffmpeg 4.3.1 | Duration and streams were taken from yt-dlp metadata rather than probe output. |

| 限制 | 影响 |
|---|---|
| `drannieandrews.com` 与 `darlinegraham.com` 返回 HTTP 403（Cloudflare） | 双方都没有竞选日程、政纲页面、新闻稿或广告库。「竞选方说了什么」的单元格全部依赖第三方报道。 |
| `dgraham.senate.gov` 与 NRLC 稿件同样 403 | 格雷厄姆本人的参议院通联缺失；其立场只能依赖一项法案、一次表决、四项委员会任命、一句辩论发言。 |
| shell 的 TLS 损坏（`SEC_E_NO_CREDENTIALS`），`curl.exe` 与 `Invoke-WebRequest` 均不可用 | 只有带显式 User-Agent 的 Python `urllib` 能连网。对 300+ 家媒体批量抓取 HTML 不现实，因此报道正文大多未读。 |
| 本会话无 `web_search` 工具（无 API key） | 发现渠道限于 yt-dlp 搜索与维基百科引用爬取。未被该条目引用、也无法在 YouTube 搜到的内容，均在本档案之外。 |
| 下载图片时遭遇维基媒体 429 | 48 张图片中 41 张本地保存，其余 7 张仅存链接。 |
| 本地无视觉语言模型 | 帧只以可测量属性描述（场景位置、人脸数量、框面积），不做解说词。 |
| 无 `ffprobe`；ffmpeg 4.3.1 | 时长与流信息取自 yt-dlp 元数据，而非 probe 输出。 |

## 2. Content gaps by dataset / 2. 按数据集列出的内容缺口

**Events (28 of 70).** No campaign calendars, so no town halls, county visits, church appearances
or GOTV events. Fourteen rows carry `venue = unknown`, twenty-six carry `event_time = unknown`.
Crowd sizes appear in no retrieved source and are never estimated.

**活动（28 行，目标 70）。** 没有竞选日程，因此没有市政厅、县域走访、教会露面或催票活动。14 行 `venue = unknown`，26 行 `event_time = unknown`。任何已检索来源都没有人数，本档案从不估算。

**Finance (5 of 30).** Four FEC snapshots are quoted in the sources (2026-03-31, 07-22, 08-05,
10-14). Quarterly line items, individual-vs-PAC splits and disbursement detail are all `unknown`.
The large March figure belongs to Lindsey Graham's committee and is flagged as such.

**财务（5 行，目标 30）。** 来源引用了四个 FEC 时点（2026-03-31、07-22、08-05、10-14）。季度明细、个人捐款与 PAC 捐款的拆分、支出明细均为 `unknown`。3 月的大额数字属于林赛·格雷厄姆的委员会，已如此标注。

**Advertising (3 rows).** No creative, script, flight dates or placement data. Two rows are
outside-money transfers; one is an ad attributed to Andrews by a PinkNews report. The archive can
say money moved; it cannot say what the money said.

**广告（3 行）。** 没有创意、脚本、投放日期或媒介数据。两行是外部资金转账，一行是 PinkNews 报道归于安德鲁斯的广告。档案能说明资金流动，不能说明资金说了什么。

**Social (3 rows).** Two posts are documented second-hand and one X status has no retrievable
body. No engagement metrics exist anywhere in the corpus.

**社交（3 行）。** 两条为二手记录，一条 X 帖无法检索正文。整个语料中没有任何互动指标。

**Media coverage (55 rows).** Titles, authors and framings are present for 55 of the 334
candidate-specific URLs the race article cites; the remaining coverage is registered in
`sources.csv` without per-row framing. Bodies were not read for most outlets.

**媒体报道（55 行）。** 该条目引用的 334 条候选人相关 URL 中，55 条具备标题、作者与框架；其余媒体登记在 `sources.csv`，没有逐行框架。多数媒体正文未读。

**Speeches.** Transcripts exist for most videos via YouTube captions, but a machine transcript is
not a transcript of record; `transcript_available` records what exists rather than what is
authoritative. No paid transcript service was used.

**演讲。** 多数视频通过 YouTube 字幕获得文本，但机器转写不等于权威逐字稿；`transcript_available` 记录的是「存在什么」，而非「何为权威」。未使用付费转写服务。

**Video.** 27 videos, 1.47 GB, capped at 22 keyframes each (scene threshold 0.30), so an hour-long
debate is sampled at roughly one frame every 2.7 minutes. That is enough to characterise staging
and face presence, not enough for shot-level editing analysis.

**视频。** 27 个视频、1.47 GB，每个上限 22 帧（场景阈值 0.30），因此一小时的辩论约每 2.7 分钟取一帧。这足以刻画舞台与人脸出现，但不足以做镜头级剪辑分析。

## 3. Conflicts left unresolved / 3. 未解决的冲突

| Conflict / 冲突 | Handling / 处理 |
|---|---|
| Lindsey Graham's death dated 2026-07-11 in the race article, 2026-07-12 in the Act article | Both recorded; `07-11` used in the event table because it is the date the race article and the CBS piece agree on. |
| Andrews's tenure at MUSC: "14 years" in one source, "about 15 years" in her own words | Biography says "about 15 years, per her own account" and flags the discrepancy. |
| Trump's endorsement of Darline Graham dated 2026-07-13 (race article) vs 2026-07-17 (Politico URL) | Both recorded in `social_media.csv`; the post date is left unresolved. |
| Counties won by Andrews: 24 in the county table, 25 in the article's prose | The table governs `county_results.csv`; the prose claim is recorded as an unresolved conflict in `results_notes.md`. |
| Graham's July bill: S.5025 (revised Russia sanctions) vs the enacted H.R. 5334 | Recorded as S.5025 with a note that it was not the enacted version. |

| 冲突 | 处理 |
|---|---|
| 林赛·格雷厄姆逝世日期：条目作 2026-07-11，法案条目作 2026-07-12 | 两者均记录；活动表采用 `07-11`，因为该条目与 CBS 报道一致。 |
| 安德鲁斯在 MUSC 的年限：一处称 14 年，她本人称约 15 年 | 传记写「据其本人说法约 15 年」，并标注差异。 |
| 特朗普对达琳·格雷厄姆的背书日期：条目作 2026-07-13，Politico URL 作 2026-07-17 | 均记录于 `social_media.csv`；帖子日期留作未决。 |
| 安德鲁斯赢下的县数：县表 24 个，条目正文 25 个 | `county_results.csv` 以县表为准；正文说法作为未决冲突记录于 `results_notes.md`。 |
| 格雷厄姆 7 月法案：S.5025（修订版俄罗斯制裁）与已生效的 H.R. 5334 | 记为 S.5025，并注明其非生效版本。 |

## 4. What would close the biggest gaps / 4. 弥补最大缺口所需

1. A browser session with residential TLS that can reach the two campaign sites — this alone would
   fill the events, ads and message columns.
2. FEC bulk data (`fec.gov/data`) for line-item receipts and disbursements, which would replace
   five snapshot rows with a real finance table.
3. A paid transcript service for the four debates, which would make the speech layer citable at
   the sentence level.
4. A local vision-language model for frame captioning, which would let the visual layer describe
   staging rather than count faces.

1. 一个能访问两个竞选网站的住宅 TLS 浏览器会话——仅此一项就能填补活动、广告与讯息列。
2. FEC 批量数据（`fec.gov/data`）的逐笔收支，可把五个时点行变成真正的财务表。
3. 针对四场辩论的付费转写服务，可使演讲层可逐句引用。
4. 本地视觉语言模型用于帧解说，可使视觉层描述舞台而非统计人脸。

## Sources / 来源

- [SRC-2108] `https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_South_Carolina`
- `_staging/B_gaps.md` — the positions stream's own gap log
