---
title: Campaign events - coverage gaps
title_zh: 竞选活动 — 报道缺口
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Documents what the 32-row event table cannot support; strongest on rallies and debates, weakest on fundraisers and small stops.
---

## What the event table covers / 活动表覆盖范围

`02_campaign_events/campaign_events.csv` holds 32 rows: 13 Ossoff, 19 Collins, with both debates and the debate announcement recorded once per candidate. Every row carries a `stated_purpose`, an `observable_function` and a separate `analyst_interpretation` field.

`02_campaign_events/campaign_events.csv` 共 32 行：奥索夫 13 行、柯林斯 19 行；两场辩论与辩论公告按候选人各记一行。每行分别填写"声明目的""可观察功能"与独立的"分析解读"。

## Time and venue gaps / 时间与场地缺口

Event times are `unknown` for 26 of 32 rows; only the debates, the Savannah breakfast and the two election-night speeches have a part of day. Venues are named for 8 rows and described only by type ("a Buckhead cafe", "a historic home", "a Savannah golf club") for 5 more.

32 行中有 26 行的具体时间记为 `unknown`；仅辩论、萨凡纳早餐会与两场选举夜演讲有大致时段。8 行有明确场地，另有 5 行仅以类型描述（"巴克黑德一家咖啡馆""一栋历史宅邸""萨凡纳一家高尔夫俱乐部"）。

## Crowd and production gaps / 人数与制作缺口

Only four rows carry a crowd figure, and two of those are campaign-supplied (about 1,400 at the February rally; about 800 students at the HBCU visit). No row records stage design, lighting, music or sign counts; the Savannah rally is the only event where a reporter describes the production (teleprompter, coached crowd, rolled-up sleeves).

仅 4 行有人数，其中 2 个为竞选团队提供（2 月集会约 1,400 人；传统黑人大学走访约 800 名学生）。没有任何一行记录舞台设计、灯光、音乐或标语数量；只有萨凡纳集会有记者描述制作细节（提词器、被指导的观众、卷起的袖子）。

## Missing event types / 缺失的活动类型

No Ossoff town hall, county-party meeting, labor event or religious appearance was retrieved. No Collins fundraiser with a documented take was retrieved either; his only recorded fundraiser is described as closed-door. This asymmetry is a gap in retrieval, not evidence that such events did not happen.

未获取到奥索夫的市政厅、县党部会议、劳工活动或宗教露面；柯林斯也没有可查金额的筹款会，唯一记录的一场为闭门。此不对称属检索缺口，不能据此断定此类活动不存在。

## How to close the gaps / 如何补足

The campaign's public event calendar (if archived), pool reports, and local weekly newspapers would add times, venues and crowds; the Georgia Recorder and GPB archives were the main accessible sources and both report selectively.

若能取得竞选公开活动日历存档、随行记者报道与地方周报，可补足时间、场地与人数；本次主要可获取来源为 Georgia Recorder 与 GPB，两者均为选择性报道。
