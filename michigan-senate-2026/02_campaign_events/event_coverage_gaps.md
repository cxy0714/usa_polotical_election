---
title: Campaign events — coverage gaps and schedule notes
title_zh: 竞选活动——覆盖缺口与日程说明
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Debates and forums are well documented; rallies, town halls and fundraisers are mostly undated or venue-less because campaign pages returned 403 and local outlets were paywalled.
---

## What the thirty-two rows contain

`02_campaign_events/campaign_events.csv` holds 18 El-Sayed rows (ELS-EVT-0001 to ELS-EVT-0018) and 14 Rogers rows (ROG-EVT-0001 to ROG-EVT-0014). Debates and forums account for twelve of the 32 rows — six in the Democratic primary, two joint general-election debates, two single-candidate broadcasts and two policy forums — because televised events are the only campaign activity that multiple independent outlets reported verbatim [SRC-0015] [SRC-0019] [SRC-0020] [SRC-0036].

中文：`02_campaign_events/campaign_events.csv` 含 18 条赛义德记录（ELS-EVT-0001 至 ELS-EVT-0018）与 14 条罗杰斯记录（ROG-EVT-0001 至 ROG-EVT-0014）。32 条中有 12 条是辩论与论坛——民主党初选六场、两场联合大选辩论、两场单候选人播出、两场政策论坛——因为电视活动是唯一被多家独立媒体逐字报道的竞选活动 [SRC-0015] [SRC-0019] [SRC-0020] [SRC-0036]。

## Event categories represented

| Category / 类别 | El-Sayed | Rogers | Note / 说明 |
|---|---|---|---|
| launch / 启动 | 1 | 1 | Venue unknown for both [SRC-0070] |
| filing / 提交联署 | 1 | 1 | Official dates only [SRC-0005] |
| debate / 辩论 | 7 | 2 | Includes one cancellation for Rogers |
| q_and_a / 政策问答 | 1 | 1 | Detroit Economic Club [SRC-0020] |
| meet_and_greet / 见面会 | 2 | 0 | One documented only by a photo caption |
| university_visit / 校园访问 | 1 | 0 | Michigan Tech, Houghton [SRC-0085] |
| press_conference / 记者会 | 1 | 1 | Spirit of Detroit; "Democrats for Mike Rogers" |
| rally / 集会 | 1 | 0 | Obama rally, Detroit [SRC-0002] |
| surrogate_event / 代理人活动 | 0 | 2 | Kennedy barn party; Trump/Port Huron rally |
| watch_party / 观票会 | 1 | 0 | Majestic Theater, Detroit |
| victory_speech / 胜选演说 | 1 | 0 | Detroit, 2026-11-04 [SRC-0029] |
| announcement / 政策宣布 | 0 | 2 | Gas tax; business endorsements |
| endorsement_event / 背书活动 | 0 | 2 | AGC PAC; business slate |
| fundraiser / 筹款会 | 0 | 1 | AIPAC-hosted, no date |
| other / 其他 | 2 | 1 | Disrupted event; post-election statement |

中文：上表逐类列出两位候选人的事件条数。启动与提交联署两类仅有日期、无场地；辩论类对罗杰斯含一场取消；见面会与校园访问主要依靠图片说明而非新闻报道；代理人活动只出现在罗杰斯一侧；筹款会一条没有确切日期。

## The five gaps, stated plainly

1. **No rally, town hall or GOTV schedule exists for either candidate.** Neither campaign published a public calendar that was retrievable, and the campaign websites returned HTTP 403 [SRC-0082] [SRC-0083]. Every mass-audience event in the file was reconstructed from a news photograph caption or a single report.
2. **Rogers' September and October travel is largely missing.** The file has one rally (Port Huron, where his attendance is not even confirmed) and one surrogate event (Highland Township) for the final six weeks of a statewide race [SRC-0048] [SRC-0062].
3. **El-Sayed's primary schedule is under-sampled outside debates.** The Houghton stop is documented by a Commons photograph description, not by a news report [SRC-0085], and the October 10 disruption is known only from a headline [SRC-0046].
4. **The AIPAC fundraisers have no date.** Wikipedia says Rogers attended four AIPAC-hosted fundraisers in Los Angeles in August 2026; The American Prospect says three, hosted the day after he met AIPAC's board chair [SRC-0003] [SRC-0073]. The row is recorded as `unverified` with the count conflict noted rather than resolved.
5. **Attendance figures do not exist in any retrieved source.** No row has a crowd count, so none is recorded.

中文：五处缺口如下。（1）两位候选人均无可取得的大型集会、市政厅或催票日程，竞选网站返回 403 [SRC-0082] [SRC-0083]；所有大型活动均由新闻图片说明或单篇报道重建。（2）罗杰斯 9 月至 10 月的行程大量缺失：全州竞选的最后六周里仅有一场集会（其本人是否到场亦未确认）与一场代理人活动 [SRC-0048] [SRC-0062]。（3）赛义德初选期间除辩论外的行程取样不足：霍顿一站仅有 Commons 图片说明 [SRC-0085]，10 月 10 日的干扰事件仅有标题 [SRC-0046]。（4）AIPAC 筹款会无日期：维基百科称 8 月洛杉矶有四场，The American Prospect 称三场且在其会见 AIPAC 董事会主席次日举办 [SRC-0003] [SRC-0073]，该行记为 `unverified` 并保留分歧。（5）任何已取得材料均无出席人数，故不作记录。

## Date conflicts kept visible

Three rows carry an explicit conflict note rather than a silent choice. El-Sayed's launch is dated April 19, 2025 by Wikipedia while the Semafor report describing it is dated April 17, 2025 and refers to Rogers announcing "this week" [SRC-0002] [SRC-0070]. The MLive forum story carries an April 2026 URL while describing the April 24 forum [SRC-0045]. Rogers' post-election statement is recorded as `conflicting sources` because it thanks supporters without using the word concede [SRC-0003].

中文：有三行明确保留日期分歧而非默默择一。赛义德启动日：维基百科记为 2025 年 4 月 19 日，而描述该事的 Semafor 报道日期为 2025 年 4 月 17 日，并称罗杰斯“本周”宣布 [SRC-0002] [SRC-0070]。MLive 论坛报道的 URL 带 2026 年 4 月日期，却描述 4 月 24 日的论坛 [SRC-0045]。罗杰斯选后声明记为 `conflicting sources`，因其感谢支持者但未使用“认输”一词 [SRC-0003]。

## Event status conventions used here

`held` is used only where a report describes what happened at the event. `announced` is used for written proposals and endorsement releases with no public venue — Rogers' gas tax proposal, his business-endorsement slate and the AGC PAC endorsement [SRC-0013] [SRC-0022] [SRC-0079]. `cancelled` is used for the September 15 Fox 2 debate because Rogers declined that morning and the broadcast proceeded with one candidate [SRC-0049]. `unverified` is used for the AIPAC fundraisers.

中文：`held` 仅用于有报道描述现场情况的活动。`announced` 用于没有公开场地的书面提案与背书发布——罗杰斯的汽油税提案、商界背书名单与 AGC PAC 背书 [SRC-0013] [SRC-0022] [SRC-0079]。`cancelled` 用于 9 月 15 日 Fox 2 辩论，因罗杰斯当日上午拒绝出席、播出仅剩一位候选人 [SRC-0049]。`unverified` 用于 AIPAC 筹款会。

## What would close the gaps

The Michigan Bureau of Elections calendar and the FEC independent-expenditure files would not help — they contain no candidate schedule. What would close these gaps is (a) a working snapshot of either campaign website's events page, (b) the Detroit News and Free Press archives, which returned HTTP 402, and (c) local television archives for September and October 2026, none of which was retrievable in this pass.

中文：密歇根州选举局日历与 FEC 独立支出文件无助于补足——它们不含候选人日程。真正能补足这些缺口的是：（a）任一竞选网站活动页的可取快照；（b）返回 HTTP 402 的《底特律新闻》与《自由新闻》档案；（c）2026 年 9 至 10 月的本地电视档案——本轮均无法取得。
