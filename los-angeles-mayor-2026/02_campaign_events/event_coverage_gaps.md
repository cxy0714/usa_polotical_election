---
title: "Event Coverage Gaps — 2026 Los Angeles Mayoral Race"
title_zh: "活动报道缺口 — 2026 年洛杉矶市长选举"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: "Explains, event by event, which rows rest on full reporting, which on a headline, and which on a photo caption — the transparency layer for campaign_events.csv."
---

# Event coverage gaps / 活动报道缺口

`campaign_events.csv` has 33 rows. They are not equally evidenced, and the difference matters: an event
known from a full report, an event known from a headline, and an event known from a photo caption are
three different epistemic objects. This file states which is which.

`campaign_events.csv` 共 33 行，证据强度并不相同，而这一差别很重要：由完整报道得知的活动、仅由标题
得知的活动、仅由图片说明得知的活动，是三种不同的认知对象。本文件说明每行属于哪一种。

## 1. Full reporting, quotes and venue / 完整报道、引语与场地（11 rows）

BAS-EVT-0002 (launch rally, [SRC-0023]); BAS-EVT-0011 / RAM-EVT-0008 (Aug. 19 debate, [SRC-0032]);
BAS-EVT-0012 / RAM-EVT-0013 (South L.A. forum, [SRC-0035]); BAS-EVT-0013 / RAM-EVT-0014 (Jewish
Federation forum, [SRC-0033]); BAS-EVT-0014 / RAM-EVT-0016 (Oct. 13 debate, [SRC-0062]); RAM-EVT-0007
(Sylmar carpenters, [SRC-0059]); RAM-EVT-0018 (victory night, [SRC-0064]). These carry verbatim quotes,
stated venues and a date confirmed by the outlet.

BAS-EVT-0002、BAS-EVT-0011 / RAM-EVT-0008、BAS-EVT-0012 / RAM-EVT-0013、BAS-EVT-0013 / RAM-EVT-0014、
BAS-EVT-0014 / RAM-EVT-0016、RAM-EVT-0007、RAM-EVT-0018 属此类，均有逐字引语、明确场地与经媒体确认
的日期。

## 2. Headline-only, metered L.A. Times / 仅标题（洛杉矶时报付费墙）（4 rows）

BAS-EVT-0001 (filing, [SRC-0037]), BAS-EVT-0006 / RAM-EVT-0003 (May 5 debate, [SRC-0040]),
BAS-EVT-0008 (canceled forum, [SRC-0041]), RAM-EVT-0009 (UNITE HERE, [SRC-0048]), RAM-EVT-0010
(DSA, [SRC-0049]), RAM-EVT-0017 (Horvath, [SRC-0050]). The headline states the fact; nothing beyond it is
asserted. For the May 5 debate the venue and moderator come from the Wikipedia debate table, which is
why the row itself is `verified` while its `venue` rests on a `T3` source.

此类行的标题即事实本身，不越过标题作任何断言。5 月 5 日辩论的场地与主持来自维基百科辩论表，
故该行整体为 `verified`，但其 `venue` 依据的是 `T3` 来源。

## 3. Caption-only / 仅图片说明（1 row）

RAM-EVT-0005 (tenant-protections event, 2026-06-01, [SRC-0057]). The only evidence is an Associated Press
photo caption: "Raman speaks during a campaign event about tenant protections with renters in Los
Angeles". No venue, no crowd, no speech content; the row says so and is `partially verified`.

唯一证据是美联社图片说明："Raman 在洛杉矶一场关于租客保护的竞选活动上发言"。无场地、无人数、
无演讲内容；该行如此注明，为 `partially verified`。

## 4. Endorsement releases with no event / 无活动的背书发布（10 rows）

BAS-EVT-0003, 0004, 0005, 0009, 0010; RAM-EVT-0009, 0010, 0011, 0012, 0017. These are dated public
endorsements, not rallies: `event_status = announced`, `venue = unknown`. They are in the events table
because endorsements are the race's real coalition data, not because they looked like events.

这些是有日期的公开背书，不是集会：`event_status = announced`、`venue = unknown`。列入活动表是因为
背书才是这场选举真正的联盟数据，而不是因为它们像活动。

## 5. Format and access problems / 形式与获取问题

**Date conflict.** BAS-EVT-0012 / RAM-EVT-0013: the LAist body says "Saturday", the photo caption says
Sept. 29 (a Tuesday). 2026-09-26 recorded; both rows `conflicting sources` [SRC-0035].

**日期冲突。** BAS-EVT-0012 / RAM-EVT-0013：LAist 正文称"星期六"，图片说明称 9 月 29 日（星期二）。
记录 2026-09-26；两行标 `conflicting sources` [SRC-0035]。

**Attribution slippage.** The line "You want to hear frustrated? I'm frustrated too" is quoted by LAist as
said "at a recent campaign event", not necessarily at the Aug. 19 debate where the archive files it. The
row's `analyst_notes` says so; SPE-BAS-0003 is `partially verified` [SRC-0032].

**归属滑动。** "你想听沮丧的话吗？我也沮丧"被 LAist 引为"在最近一场竞选活动"所说，未必是在档案
归入的 8 月 19 日辩论上。该行 `analyst_notes` 已注明；SPE-BAS-0003 为 `partially verified` [SRC-0032]。

**Cancellation as an event.** BAS-EVT-0008 is a debate that did not happen, kept because the cancellation
is itself a campaign decision — Bass withdrew after committing, Pratt declined on scheduling, Raman
withdrew on May 11 and the forum collapsed the same day [SRC-0041] [SRC-0078].

**取消也是事件。** BAS-EVT-0008 是一场未发生的辩论，保留它是因为取消本身即竞选决策——Bass 在承诺后
退出、Pratt 因日程冲突婉拒、Raman 于 5 月 11 日退出，论坛当日取消 [SRC-0041] [SRC-0078]。

**Venue resting on Wikipedia.** BAS-EVT-0007 / RAM-EVT-0004 (Skirball) and the Oct. 13 NBC4 venue
(Universal City) come from the Wikipedia debate table [SRC-0001]; the NBCLA uploads confirm date and
participants but not the address.

**场地依据维基百科。** BAS-EVT-0007 / RAM-EVT-0004（Skirball）与 10 月 13 日 NBC4 场地（Universal
City）来自维基辩论表 [SRC-0001]；NBCLA 上传视频确认日期与参与者，但不含地址。

## 6. What no source reports / 无来源报道的部分

No crowd size for any event. No fundraising totals per event. No press pool reports. No event-level
security or protest activity. No primary-night watch party for either candidate. Those absences are
listed as G20 and G21 in `research_gaps.md`; the events table does not fill them with estimates.

任何活动都无人数；无单场募款总额；无联合采访报道；无活动层面的安保或抗议信息；两位候选人都无初选夜
观票会。这些缺失在 `research_gaps.md` 中列为 G20 与 G21；活动表不以估算填补。
