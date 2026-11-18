---
title: "Alaska 2026 U.S. Senate — research gaps"
title_zh: "阿拉斯加 2026 联邦参议员选举 — 研究缺口"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: "Lists every known gap with cause and remedy; the largest are the missing concession, AFN appearances and ad creatives."
---

# Research gaps / 研究缺口

Each entry gives the gap, why it exists, and what would close it. Gaps are not papered over in the
datasets: the affected cells say `unknown` and the row's `verification_status` reflects the shortfall.

每条缺口说明"缺什么、为何缺、如何补"。数据集中不以猜测填补：相关单元格写 `unknown`，
`verification_status` 标注实际状态。

## 1. No concession speech or concession event

Sullivan neither conceded nor gave a public speech on 2026-11-17. NBC reported that his campaign
"said the senator would have more to say by the end of this week"; his spokesman's only quoted line
was that "Alaskans deserve a complete and accurate count" (SRC-0056). No `concession_speech` row
exists in `campaign_events.csv` or `speech_archive.csv` — the category is defined in the contract
but the event was not documented, and inventing one would violate the honesty rule.

**Cause:** the concession had not happened by the archive's compile date (2026-11-18).
**Would close it:** post-18 November coverage from ADN, Alaska Public Media, NBC or the campaign's
video channels; or a certified results statement from the Division of Elections.

沙利文在 2026-11-17 既未认输，也未发表公开演讲。NBC 报道其团队称"参议员本周晚些时候会有更多表态"，
其发言人唯一被引用的说法是"阿拉斯加人理应得到完整、准确的计票"（SRC-0056）。因此档案中没有
`concession_speech` 记录——合同定义了该类别，但事件确实未被记录，虚构即违反诚实规则。
原因：截至 2026-11-18 认输尚未发生。补齐：11 月 18 日之后的 ADN、Alaska Public Media、NBC 报道，
或竞选团队视频渠道，或选举委员会的认证声明。

## 2. The Alaska Federation of Natives convention is a hole in the middle of the race

The 60th AFN convention is the single most important Alaska Native political venue of the cycle. The
archive knows only that it "begins October 22" — from a Data for Progress polling release (SRC-0077)
— and that AFN issued a "Calls for Full Participation" statement noted in a Delta Discovery sidebar
(SRC-0069). No retrieved report documents either candidate speaking, appearing or being endorsed at
the convention. Two placeholder rows (PEL-EVT-09, SUL-EVT-16) are marked `event_status=unverified`
and explicitly labelled "candidate appearance not documented"; they exist to mark the hole, not to
claim attendance.

**Cause:** AFN coverage was not among the retrieved article set, and the convention's own agenda and
livestream pages were not fetched.
**Would close it:** AFN's convention program and video archive; Alaska Public Media's AFN coverage;
ADN's "AFN convention" tag; the campaigns' October schedules.

第 60 届 AFN 大会是本周期最重要的阿拉斯加原住民政治场合，但档案仅从 Data for Progress 民调稿
（SRC-0077）得知其"10 月 22 日开始"，并从 Delta Discovery 边栏（SRC-0069）得知 AFN 发布了
"Calls for Full Participation" 声明。没有任何已取得的报道记载两位候选人在大会上发言、露面或获
背书。两行占位记录（PEL-EVT-09、SUL-EVT-16）标为 `unverified`，并明确注明"候选人露面未记载"——
它们的作用是标记缺口，而非声称出席。

## 3. Rally venues, crowd sizes and staging

Alaska reporting rarely quantifies crowds. The Vance rally is "several hundred people" in a hangar at
Fairbanks International Airport (SRC-0025); the Wasilla Trump rally has a date and city from an AP
photo caption but no venue or crowd (SRC-0062); the Peltola Juneau rally has a date and a quote but no
venue or crowd (SRC-0062). `visual_notes` and `venue` cells are `unknown` in those rows.

**Cause:** Alaska outlets describe rallies qualitatively; pool reports were not retrieved.
**Would close it:** AP pool reports, campaign live-streams, and local TV footage with venue signage.

阿拉斯加报道很少给出集会人数。Vance 集会是费尔班克斯国际机场机库中的"数百人"（SRC-0025）；
Wasilla 特朗普集会的日期与城市来自 AP 图片说明，场地与人数均无（SRC-0062）；佩尔托拉朱诺集会有
日期与引语，但无场地与人数（SRC-0062）。相关行的 `venue`、`visual_notes` 均记为 `unknown`。

## 4. No paid-ad creative was retrieved

`advertisements.csv` has six rows, but none is backed by an ad video, script or storyboard. What the
archive has is journalism describing the ads: Roll Call on the NRSC digital spot (SRC-0066), AFP
Action's own release on a "six-figure statewide ad buy" (SRC-0105), NBC quoting one line of a Peltola
ad (SRC-0056), and Beacon/ADN reporting on super-PAC spending to promote fringe candidates
(SRC-0041, SRC-0017). `main_visual_elements`, `narration_soundtrack` and `length_seconds` are
`unknown` across the file.

**Cause:** ad libraries (Meta, Google, AdImpact) require subscriptions or logins, and the campaigns'
YouTube channels returned no retrievable ad URLs; the campaign sites embed no video players.
**Would close it:** Meta Ad Library and Google Ads Transparency queries for the cycle; AdImpact
spend data; the campaigns' YouTube/Vimeo channels.

`advertisements.csv` 有 6 行，但没有任何一则广告的视频、脚本或分镜为依据。档案掌握的是描述广告的
报道：Roll Call 对 NRSC 数字广告的报道（SRC-0066）、AFP Action 自述"六位数全州投放"（SRC-0105）、
NBC 引用佩尔托拉广告中的一句（SRC-0056），以及 Beacon/ADN 对超级政治行动委员会推举边缘候选人的
报道（SRC-0041、SRC-0017）。全表 `main_visual_elements`、`narration_soundtrack`、`length_seconds`
均为 `unknown`。原因：广告库需订阅或登录，竞选团队 YouTube 频道未取得可用广告链接，竞选网站未嵌入
视频播放器。补齐：Meta 广告库、Google 广告透明度查询、AdImpact 数据、候选人 YouTube/Vimeo 频道。

## 5. No machine-readable district-level results

Alaska reports by state house district, not county. `county_results.csv` is header-only by design
(see `results_notes.md`). No district table was retrieved for this race; the official summary
(SRC-0001) is statewide.

**Cause:** the division publishes district results in a separate file/format that was not located;
the primary summary PDF URL returned 404.
**Would close it:** the Division of Elections district-results spreadsheet or API; the state's
precinct-level "cast vote record" for the 2026 general.

阿拉斯加按州众议院选区而非县公布结果。`county_results.csv` 按设计仅有表头（见 `results_notes.md`）。
本次选举未取得选区级表格；官方汇总（SRC-0001）为全州数据。原因：选举委员会另以单独文件/格式公布
选区结果，未能定位；初选汇总 PDF 链接返回 404。补齐：选举委员会选区结果表或 API；2026 年大选的
precinct 级 cast vote record。

## 6. Official primary summary returned HTTP 404

`https://www.elections.alaska.gov/enr26/results/ElectionSummaryReportRPT.pdf` returns 404, so primary
numbers come from the AP results project page (SRC-0064) and the Wikipedia results table (SRC-0006),
both marked `partially verified`. Cross-checks are consistent (Peltola 82,244 / 49.5; Sullivan 68,726 /
41.4; total 166,004), but no official document confirms them.

**Cause:** the URL pattern used for the general-election summary does not exist for the primary.
**Would close it:** the correct primary summary URL from the division's results index page.

该链接返回 404，因此初选数字来自 AP 结果页（SRC-0064）与维基百科结果表（SRC-0006），均标为
`partially verified`。交叉核对一致（佩尔托拉 82,244 / 49.5；沙利文 68,726 / 41.4；合计 166,004），
但无官方文件确认。补齐：从选举委员会结果索引页取得正确的初选汇总链接。

## 7. Paywalls and blocks (all recorded in `_staging/fetch_log.csv`)

| URL / outlet | Status | Consequence |
|---|---|---|
| Associated Press article pages (6) | 403 | quotes taken from syndicated PBS/ABC/ADN copies |
| Reuters | 401 | not used |
| The New York Times (Sept 23 staff-allegation story) | paywall/403 | story known only through ADN's analysis (SRC-0022) and the Wikipedia summary |
| Politico, Axios, The Hill | 403 | headlines only; not used for coded claims |
| Juneau Independent, Native News Online, RealClearPolitics, Trafalgar, NFIB, Center for Politics, Alaska Survey Research site | 403 | excluded from `sources.csv` |
| Ballotpedia | 202, 0 bytes | excluded; no candidate list from it |
| elections.alaska.gov | TLS chain failure (`CERTIFICATE_VERIFY_FAILED`) | retrieved only with an unverified SSL context; both documents logged |

These are not silent omissions: any claim that depended on them was either dropped or sourced to a
retrieved syndication.

上述阻断均记录在 `_staging/fetch_log.csv`。依赖这些页面的论断要么放弃，要么改用已取得的转载版本
（如 PBS/ABC/ADN 对 AP 稿的转载）。

## 8. Poll provenance for the Alaska Survey Research series

Four ASR polls are in `polling.csv` with numbers and sample sizes taken from the Wikipedia polling
table; the Bluesky post URLs render as JavaScript and returned no post text. They are marked
`partially verified`. Data for Progress (two polls), InsiderAdvantage and the AARP-sponsored
Fabrizio/Impact poll were read directly from retrieved pages and are `verified`.

**Cause:** Bluesky's server-rendered HTML carries no post body for logged-out fetches.
**Would close it:** the Bluesky API (`app.bsky.feed.getPostThread`) or ASR's own releases.

`polling.csv` 中四项 ASR 民调的数字与样本量取自维基百科民调表，其 Bluesky 链接为 JS 渲染、未返回
正文，故标为 `partially verified`。Data for Progress 两项、InsiderAdvantage 与 AARP 委托的
Fabrizio/Impact 民调直接读取自已取得页面，标为 `verified`。补齐：Bluesky API 或 ASR 自身发布的稿件。

## 9. No direct candidate social-media posts

`social_media.csv` therefore uses archived campaign emails (SRC-0110, SRC-0111), campaign websites
(SRC-0091, SRC-0092), one union X post (SRC-0112) and one social video known only through ABC's
reporting (SRC-0062). Candidate X/Facebook/Instagram accounts returned 403 or were not fetched.

**Cause:** `x.com` blocks logged-out scraping; no API credentials.
**Would close it:** platform APIs or an archived-posts service.

因此 `social_media.csv` 使用存档竞选邮件、竞选网站、一条工会 X 帖，以及仅通过 ABC 报道得知的
一条社交视频。候选人 X/Facebook/Instagram 账号返回 403 或未抓取。补齐：平台 API 或存档服务。

## 10. Video: three URLs, no transcripts

Ten `speech_video_index.csv` rows cover only three retrieved videos (AOGA forum, Kodiak debate,
Debate for the State). Rows are segment-level entries describing exchanges reported by the press, not
timestamped transcript segments: `relevant_timestamps` and `transcript_available` say so. No captions
or transcripts were retrieved for any video.

**Cause:** YouTube/Vimeo caption endpoints require player parameters not available from the watch
pages; no ASR tooling.
**Would close it:** `yt-dlp` caption download or manual transcription.

10 条视频索引仅覆盖三个已取得视频；各行是按媒体报道描述的"片段级"条目，而非带时间码的转写片段，
`relevant_timestamps` 与 `transcript_available` 已如实标注。未取得任何字幕或转写。补齐：yt-dlp
下载字幕或人工转写。

## 11. Legal documents are second-hand

The DOJ suit, the federal judge's rejection and the appeal are known from news reports (SRC-0038,
SRC-0039, SRC-0052, SRC-0061) — no complaint, order or docket was retrieved. The Alaska Supreme
Court ruling that restored Dan J. Sullivan Jr. to the ballot is likewise known from ADN/APM coverage
(SRC-0015, SRC-0033).

**Cause:** court PDFs and docket pages were outside the fetch list; PACER requires payment.
**Would close it:** the District of Alaska docket and the Alaska Supreme Court opinion PDF.

司法文件均为二手：DOJ 诉讼、联邦法官驳回与上诉只见于新闻报道（SRC-0038、SRC-0039、SRC-0052、
SRC-0061），未取得起诉书、裁定或案卷；阿拉斯加最高法院恢复小丹尼尔·沙利文参选资格的裁决同样只见于
ADN/APM 报道（SRC-0015、SRC-0033）。补齐：阿拉斯加联邦地区法院案卷与州最高法院判决书 PDF。

## 12. A measure-level discrepancy left unreconciled

Ballot Measure 2's official margin is 7.62 points (SRC-0001); the Wikipedia article says "six-point
margin" (SRC-0006). The measure is outside the case's scope, so the archive records both and
reconciles neither. See `results_notes.md`.

第 2 号公投的官方差距为 7.62 个百分点（SRC-0001），维基百科称"约六个百分点"（SRC-0006）。该公投
不属本案例范围，档案并列记录、不作调和。见 `results_notes.md`。

## 13. What is deliberately absent

- No claim about who "really" recruited Dan J. Sullivan Jr.: reporting says "evidence of Peltola's
  involvement is unclear" (SRC-0047) and a donor was visited by the FBI (SRC-0023). The archive
  records the dispute, not a conclusion.
- No crowd-size estimate where none was published.
- No attribution of motive to either campaign beyond what each said on the record.

- 不判断究竟是谁招募了小丹尼尔·沙利文：报道称"佩尔托拉是否参与，证据不明"（SRC-0047），
  且有捐款人被 FBI 走访（SRC-0023）。档案记录争议，不给结论。
- 无报道处不估算人数。
- 除公开表态外，不推断任何一方动机。
