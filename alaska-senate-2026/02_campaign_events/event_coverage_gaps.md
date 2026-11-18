---
title: "Alaska 2026 — campaign event coverage gaps"
title_zh: "阿拉斯加 2026 — 竞选活动报道缺口"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: "Explains which event categories are missing, which are thin, and why the AFN convention is a hole in the middle of the case."
---

# Event coverage gaps / 活动报道缺口

## The shape of the evidence

`campaign_events.csv` holds 30 rows: 14 for Peltola, 16 for Sullivan. Of these, 16 are documented
appearances, 11 are endorsement announcements, and 3 are unverified placeholders (two AFN rows and
Peltola's written victory statement). Five occasions are recorded once per candidate — the primary
day, the AOGA forum, the Kodiak debate, Debate for the State and the AFN convention — so the file
describes **25 distinct dated occasions**, not 30.

`campaign_events.csv` 共 30 行：佩尔托拉 14 行、沙利文 16 行。其中 16 条为有据可查的露面、11 条为
背书公告、3 条为未核实占位（两行 AFN 与佩尔托拉的书面胜选声明）。有五个场合按候选人各记一行——
初选日、AOGA 论坛、科迪亚克辩论、Debate for the State 与 AFN 大会——因此文件描述的是
**25 个不同日期场合**，而非 30 个。

## What is missing, by category

| Category | Rows | Why the number is low |
|---|---:|---|
| `rally` | 2 | Only the Juneau rally (Peltola) and the Wasilla Trump rally (Sullivan) have enough detail to code; neither has a venue or crowd. |
| `town_hall` | 0 | Peltola's town halls against the Kroger merger are described by AFGE (SRC-0094) but no single event with a date and city was retrieved. |
| `meet_and_greet`, `small_business_visit`, `workplace_visit` | 0 | Standard Alaska campaign stops are not covered event-by-event by the outlets retrieved. |
| `fundraiser` | 0 | No fundraiser was reported with a date and host. |
| `early_voting_event`, `gotv_event` | 0 | Sealaska's GOTV campaign is recorded as an endorsement announcement (SRC-0102); no candidate GOTV event was retrieved. |
| `watch_party`, `election_eve` | 0 | Not reported in the retrieved corpus. |
| `concession_speech` | 0 | Sullivan had not conceded by 2026-11-18 (SRC-0056). |
| `victory_speech` | 1 | Peltola's is a written statement, coded `unverified` as an event. |
| `press_conference`, `interview_*`, `podcast`, `livestream` | 0 | These were not coded as events; several are better represented in `05_campaign_media/media_coverage.csv`. |

## The AFN hole

The Alaska Federation of Natives' 60th convention began 2026-10-22 (SRC-0077). AFN is the central
Alaska Native political gathering of the cycle, and both candidates had obvious reasons to appear:
Peltola as the first Alaska Native woman in Congress, Sullivan as the candidate endorsed by the
ANCSA Regional Association (SRC-0104). No retrieved report documents either one speaking there. Two
rows (PEL-EVT-09, SUL-EVT-16) exist as `unverified` placeholders with explicitly hedged titles
("candidate appearance not documented"), and this file records why they are placeholders rather than
events. Filling this gap is the single highest-value addition to the archive.

阿拉斯加原住民联合会（AFN）第 60 届大会于 2026-10-22 开幕（SRC-0077）。AFN 是本周期阿拉斯加原住民
政治的核心场合，两位候选人都有明显理由出席：佩尔托拉是国会首位阿拉斯加原住民女性，沙利文则获
ANCSA 区域协会背书（SRC-0104）。但没有任何已取得报道记录其中一人在此发言。两行
（PEL-EVT-09、SUL-EVT-16）作为 `unverified` 占位存在，标题明确保留（"候选人露面未记载"），
本文件说明其为何只是占位而非事件。补齐这一缺口是档案中最有价值的增补。

## Debates: three, all joint, all documented

| Date | Venue / host | Moderator(s) | Video |
|---|---|---|---|
| 2026-08-27 | Alaska Oil and Gas Association annual conference, Anchorage | not reported (the House forum that day was moderated by Tara Sweeney) | vimeo.com/1225063686 (SRC-0118) |
| 2026-09-12 | Kodiak Chamber of Commerce fishery debate | not reported | youtube.com/watch?v=53yBygyYrlk (SRC-0116) |
| 2026-10-15 | "Debate for the State", Alaska Public Media studio, Anchorage | Lori Townsend (APM news director), with Liz Ruskin and Wil Courtney on the panel (SRC-0024) | youtube.com/watch?v=1nyBxC-uups (SRC-0117) |

The 2026-10-15 panel details come from ADN's account, which names Townsend and refutes Sullivan's
claim that Peltola received questions in advance. The other two debates' moderator names were not in
the retrieved reporting and are left `unknown` rather than inferred from the host organisation.

2026-10-15 的主持人信息来自 ADN 报道，报道点名汤森并驳斥沙利文"佩尔托拉提前拿到问题"的说法。
另外两场辩论的主持人姓名未见于已取得报道，故记 `unknown`，不依据主办机构推断。

## Documented appearances by phase

| Phase | Peltola | Sullivan | Note |
|---|---:|---:|---|
| pre_launch / launch | 3 | 2 | Peltola's Pride parade appearance (date unknown), launch video and the SEIU 775 endorsement; Sullivan's Lincoln Day launch and Trump endorsement |
| primary | 2 | 6 | Endorsement-heavy: five of Sullivan's six are releases |
| general | 8 | 8 | Three debates, two rallies, one surrogate rally, plus endorsement releases |
| election_day | 0 | 0 | No candidate event on 2026-11-03 was retrieved; the primary-day rows are coded `primary` |
| post_election | 1 | 0 | Peltola's written victory statement; no Sullivan event |

The imbalance in the primary phase is a source artifact: Sullivan's team pushed endorsement releases
steadily through the spring and summer, while Peltola's endorsements were announced by the groups
themselves on fewer dates.

初选阶段的不平衡是信息来源差异：沙利文团队春夏持续发布背书稿，而佩尔托拉的背书多由团体自行在
较少日期公布。

## What would close the remaining gaps

1. Campaign event calendars or press advisories (not retrieved; sites returned 403 or had no calendar).
2. Local TV and radio coverage of stops in Bethel, Nome, Utqiagvik, Ketchikan and Sitka — none of
   which appears in the retrieved corpus at all, a geographic bias worth stating plainly.
3. AFN's convention program and video archive.
4. Sullivan's post-election remarks, whenever they occur.

1. 竞选活动日历或媒体通告（未取得；网站 403 或无日历）。
2. 对贝瑟尔、诺姆、乌特恰维克、凯奇坎、锡特卡等地停留的地方电视与广播报道——这些地点在已取得
   语料中完全缺席，这一地理偏差值得明确说明。
3. AFN 大会议程与视频存档。
4. 沙利文的选后表态（待其发生）。
