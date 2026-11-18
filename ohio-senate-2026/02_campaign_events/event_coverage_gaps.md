---
title: Event coverage gaps and what the event record cannot show
title_zh: 竞选活动记录的缺口
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Documents which event types are thin or missing, and why, so downstream users do not read absence as inactivity.
---


# Event coverage gaps

## What the table covers well

The 35 rows in `campaign_events.csv` are heavy on endorsement events (17 of 35) and on the final
three weeks of rallies. That reflects the sources: union and trade-association releases are
dated, published and archived, and late-October rally coverage was abundant.

## What is thin

**Routine retail politics is almost absent.** Neither campaign published a public event
calendar, and Ohio political coverage does not report every county fair stop or plant walk. The
archive therefore records seven `community_visit`, `small_business_visit` or `workplace_visit`
rows against what were certainly dozens of such stops. Absence in this table is an artefact of
coverage, not evidence that the candidates stayed home.

**Fundraisers are not documented at all.** No closed-press fundraiser in Ohio was reported with
a date and venue in a retrievable source. There is no `fundraiser` row, and none should be
inferred from the finance totals.

**Debates are absent, and this is the single largest gap.** No source retrieved for this archive
documents a Brown-Husted debate: no date, no venue, no sponsor, no transcript. What the record
does contain is evidence of a dispute about debates — a WDTN headline dated 2026-10-30 whose
article body could not be retrieved — and a Bowling Green State University/YouGov poll, fielded
before debates became an issue, in which 54% of respondents called debates "very important".
No `debate` or `debate_invitation` row was created, because a headline is not enough to fix a
date and venue.

**Early-voting events are undercounted.** Two `early_voting_event` rows exist; both campaigns
ran turnout operations across all 88 counties for four weeks.

## What cannot be recovered at all

Crowd sizes. Where a source printed an estimate ("hundreds", "more than 1,000"), the number is
recorded in `crowd_size_estimate` with the source's own hedging; where no estimate was printed,
the cell says `unknown`. Do not sum these cells.

## 中文摘要

事件表长于 endorsement（35 行中 17 行）与最后三周的集会，因为工会与行业协会的新闻稿有确定日期
且被存档。日常零售式竞选活动（县集市、工厂走访）几乎没有记录：两个竞选团队都没有公布公开活动
日历。募款活动完全没有记录。最大的缺口是辩论：本档案检索到的材料中没有任何一场布朗—赫斯特德
辩论的日期、场地或主办方；只有一条 2026-10-30 的 WDTN 标题（正文无法获取）显示辩论曾成为争议
议题。因此没有创建 debate 行——一条标题不足以确定日期与场地。人群规模只能照抄来源的估计，未
印出估计的一律记为 unknown，且不可加总。
