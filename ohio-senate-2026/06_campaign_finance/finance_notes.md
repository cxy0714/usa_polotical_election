---
title: Campaign finance notes
title_zh: 竞选财务说明
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: 9 rows covering five candidates across two reporting points; only receipts, disbursements and cash on hand are in the source tables.
---


# Campaign finance notes

## The two reporting points

The archive holds two snapshots, both taken from the FEC-derived tables in the race article.

**As of 2026-04-18 (period ending 2026-03-31):** Brown had raised $24,471,408, spent $7,956,946
and held $16,514,461. Husted had raised $10,257,823, spent $2,017,868 and held $8,239,954. The
same table lists the Democratic primary field: Ode $5,001,938 raised, Kincaid $41,804, Volpe
$4,337.

**As of 2026-10-14 (period ending 2026-09-30):** Brown $68,409,200 raised, $63,956,397 spent,
$4,452,803 on hand; Husted $19,894,786 raised, $15,655,689 spent, $4,239,097 on hand; Redpath
$55,256 / $47,000 / $8,255; Levy $132,712 / $107,925 / $26,916.

## What the columns mean, and what they do not

The source tables print three numbers per candidate. `individual_contributions`,
`pac_contributions` and `debts_owed` are therefore `unknown` for every row rather than estimated
from the totals. The receipts figure at the October point is cumulative for the cycle, not a
single quarter's intake, and the notes column says so.

## The outside-money gap

Candidate committees are the small part of the picture. AdImpact's estimate, reported by the
Ohio Capital Journal, puts outside-group spending above $325 million in this race — several times
the combined candidate totals. That money flows through committees that file separately, and
none of it appears in `campaign_finance.csv`. A user who reads only the candidate table will
understate total spending by an order of magnitude.

## The spending pattern

Brown raised roughly 3.4 times Husted's total and had spent 96% of what he raised by
2026-09-30, entering the final month with $4.45 million on hand — about the same as Husted's
$4.24 million. The near-identical cash position at the end, against a 3.4x fundraising gap,
is the most striking number in the file.

## 中文摘要

档案只有两个时点：2026-04-18（截至 3 月 31 日）与 2026-10-14（截至 9 月 30 日）。前者布朗募
2,447 万美元、花 796 万、余 1,651 万；赫斯特德募 1,026 万、花 202 万、余 824 万。后者布朗募
6,841 万、花 6,396 万、余 445 万；赫斯特德募 1,989 万、花 1,566 万、余 424 万。来源表只印三个
数字，因此个人捐款、PAC 捐款与负债三列一律记为 unknown，不做推算。10 月的"募款"是本届累计数，
不是单季。最大的缺口是外部资金：AdImpact 估算外部团体支出超过 3.25 亿美元，数倍于两位候选人
之和，且完全不在本表内。最醒目的数字是终点现金几乎相同（445 万 vs 424 万），而募款差距是 3.4 倍。
