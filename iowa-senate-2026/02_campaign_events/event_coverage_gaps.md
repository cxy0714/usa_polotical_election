---
title: Event coverage gaps
title_zh: 活动记录缺口
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: in_progress
coverage_note: Coverage is event-rich but crowd- and venue-poor: most rows have a date and city, few have a headcount.
---

# Event coverage gaps / 活动记录缺口

## English

| Gap | Why it exists | What would close it |
|---|---|---|
| No crowd estimate for 30 of 34 events | The covering reports describe what was said, not how many attended | Local TV packages and campaign pool photos; a stringer count |
| No venue for the Ankeny roundtable's room or the Whiskey River address | Reports name the host business but not the room | The venue's own event listings |
| The "Fighting for Iowa Tour" has no dates | The campaign website advertises it as a standing feature | The tour's sign-up page or a dated press release |
| No county-party meetings for either candidate | County party sites were not retrieved in this batch | County central-committee calendars |
| No Turek events between 15 October and 3 November | Only the campaign's own release list covers that window | The campaign's public calendar or local paper previews |
| Two Hinson items are surrogate events, not her appearances | Cruz, Barrasso and Kennedy carried them | Pool reports or video of her own remarks |

## 中文

| 缺口 | 原因 | 补足方式 |
|---|---|---|
| 34 场活动中 30 场无人数记录 | 报道描述发言内容，不报人数 | 地方电视台报道、竞选团队公开照片、自由撰稿人计数 |
| Ankeny 圆桌的场地与 Whiskey River 的具体房间不明 | 报道只写主办企业 | 场地方自己的活动公告 |
| "Fighting for Iowa Tour" 无日期 | 仅在其官网上作为常设栏目出现 | 报名页或有日期的新闻稿 |
| 两位候选人均无县党部会议记录 | 本批次未抓取县党部网站 | 县党部中委会议程 |
| Turek 在 10 月 15 日至 11 月 3 日之间无活动 | 该时段只有其官网新闻列表 | 竞选公开日程或地方报纸预告 |
| Hinson 有两场属代理人活动 | Cruz、Barrasso、Kennedy 主导 | 联合采访记录或其本人发言视频 |

## Rule applied / 适用规则

Where a report says an event happened but gives no crowd, the row's `observable_function` describes what was
observable (a press conference, a roundtable with named participants) and `analyst_notes` says the crowd is
unknown. No number is estimated.

中文：若报道确认活动发生但未给人数，则该行只记录可观察到的形式（记者会、有名有姓的圆桌参与者），并在 `analyst_notes` 注明人数不明；本档案不做任何人数估算。
