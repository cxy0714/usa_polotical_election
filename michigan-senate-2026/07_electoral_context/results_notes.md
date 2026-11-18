---
title: Results notes — arithmetic reconciliation
title_zh: 结果说明——算术核对
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: All published figures reconcile except a three-vote discrepancy in the general-election total; no county table exists, so county_results.csv is header-only.
---

## The published result table

| Race / 选举 | Candidate / 候选人 | Party / 政党 | Votes / 票数 | Share / 得票率 | Winner / 当选 |
|---|---|---|---|---|---|
| Democratic primary, 2026-08-04 | Abdul El-Sayed | Democratic | 744,952 | 48.45 | yes |
| Democratic primary, 2026-08-04 | Haley Stevens | Democratic | 731,160 | 47.55 | no |
| Democratic primary, 2026-08-04 | Mallory McMorrow (withdrawn) | Democratic | 61,516 | 4.00 | no |
| Republican primary, 2026-08-04 | Mike Rogers | Republican | 883,328 | 100.0 | yes |
| General, 2026-11-03 | Abdul El-Sayed | Democratic | 2,520,895 | 52.54 | yes |
| General, 2026-11-03 | Mike Rogers | Republican | 2,181,111 | 45.46 | no |
| General, 2026-11-03 | Lydia Christensen | Libertarian | 49,707 | 1.04 | no |
| General, 2026-11-03 | Tim Long | U.S. Taxpayers | 26,550 | 0.55 | no |
| General, 2026-11-03 | Douglas P. Marsh | Green | 12,564 | 0.26 | no |
| General, 2026-11-03 | Walter P. Kristy | Natural Law | 7,262 | 0.15 | no |

All figures transcribed from the race article, which cites the Michigan Department of State and the AP [SRC-0001].

中文：上表为公布的完整结果表，全部数字转录自该选举条目，其来源为密歇根州州务卿与美联社 [SRC-0001]。

## Democratic primary: the arithmetic closes

The three candidate totals sum to 1,537,628 votes. Recomputed shares are 48.45%, 47.55% and 4.00%, which sum to 100.00% and match the published shares exactly. The winner's margin is 13,792 votes, or 0.90 points of the primary electorate (13,792 / 1,537,628 = 0.90%). McMorrow's 61,516 votes — 4.00% — were cast for a candidate who had suspended her campaign on July 5, 2026, and are larger than the winner's margin: the withdrawn candidate's residual vote was 4.5 times the margin of victory [SRC-0001] [SRC-0033].

中文：三位候选人票数合计 1,537,628 票。重算得票率为 48.45%、47.55% 与 4.00%，合计 100.00%，与公布值完全一致。胜者优势为 13,792 票，占初选选民总数的 0.90%（13,792 / 1,537,628 = 0.90%）。麦克莫罗的 61,516 票（4.00%）投给了一位已于 2026 年 7 月 5 日暂停竞选的候选人，且其票数大于胜者优势：退选候选人的残余票数是胜选差距的 4.5 倍 [SRC-0001] [SRC-0033]。

## General election: a three-vote discrepancy

The six candidate totals sum to **4,798,089** votes, while the published total for the race is **4,798,086** — a discrepancy of three votes. This archive does not adjust any candidate figure to close the gap. Recomputed shares from the candidate totals are 52.54%, 45.46%, 1.04%, 0.55%, 0.26% and 0.15%, summing to 100.00% and matching every published share, so the discrepancy sits in the reported total rather than in any candidate's tally. Most likely cause: a canvass total reported at a different moment from the candidate figures. The margin is 339,784 votes, or 7.08 points (339,784 / 4,798,086 = 7.08%), which matches the `margin_pct` recorded in `_staging/case_meta.json` [SRC-0001].

中文：六位候选人票数合计 **4,798,089** 票，而该选举公布的总票数为 **4,798,086** 票，相差三票。本档案不调整任何候选人数字以弥合差额。按候选人票数重算的得票率为 52.54%、45.46%、1.04%、0.55%、0.26% 与 0.15%，合计 100.00%，且与每一项公布值一致，故差额位于公布的总票数而非任何候选人的票数。最可能的原因是：计票汇总数与候选人数字取自不同时点。胜选差距为 339,784 票，即 7.08 个百分点（339,784 / 4,798,086 = 7.08%），与 `_staging/case_meta.json` 中记录的 `margin_pct` 一致 [SRC-0001]。

## The minor-party share

The four minor candidates together took 96,083 votes, or 2.00% (96,083 / 4,798,089 = 2.00%). None exceeded 1.04%, so no minor candidate affected the outcome; but the 2.00% combined share is larger than the 1.04% the Libertarian nominee received and is worth recording separately from the two-party margin [SRC-0001].

中文：四位小党候选人合计 96,083 票，占 2.00%（96,083 / 4,798,089 = 2.00%）。无人超过 1.04%，因此没有小党候选人影响结果；但合计 2.00% 大于自由党提名人的 1.04%，值得与两党差距分开记录 [SRC-0001]。

## Why county_results.csv is header-only

No county-level vote table for this election was published in any source this archive retrieved. The race article reports county outcomes only qualitatively: El-Sayed carried 30 of 83 counties, including nine in the Upper Peninsula and nine north of Grand Rapids, and five counties flipped from Republican to Democratic between 2024 and 2026 — Grand Traverse, Isabella, Kent, Leelanau and Muskegon [SRC-0008] [SRC-0001]. Because the contract forbids inventing counties, `07_electoral_context/county_results.csv` contains the header row and no data rows, and these five flips are recorded here instead. A working Department of State county-results export would close the gap [SRC-0006].

中文：本档案取得的任何来源均未公布本次选举的县级票数表。该选举条目仅定性描述县级结果：赛义德赢得 83 个县中的 30 个，包括上半岛 9 个县与大急流城以北 9 个县；2024 至 2026 年间有五个县由共和党转向民主党——大特拉弗斯、伊莎贝拉、肯特、利拉诺与马斯基根 [SRC-0008] [SRC-0001]。因合同禁止虚构县份，`07_electoral_context/county_results.csv` 仅含表头、无数据行，这五个翻转县改记于此。若能取得州务卿的县级结果导出文件即可补足 [SRC-0006]。

## Primary polls without a place in polling.csv

`07_electoral_context/polling.csv` holds seven general-election polls only. Primary polls were excluded because the nominee pairing was not fixed until August 5, so the `elsayed_pct` / `rogers_pct` columns would not apply. Two primary-era data points are recorded here instead: Axios reported a 12-to-1 spending advantage for Stevens at one point in the primary [SRC-0056], and a Fox News poll of the general election conducted September 24–28 put El-Sayed at 50% and Rogers at 49% among likely voters [SRC-0050]. One polling row carries `conflicting sources`: the Mitchell Research poll of October 1 is published by CBS as 45.6–41.4 but appears in the race article's table as 46–41 with 7% other and 6% undecided [SRC-0037] [SRC-0001]. Candidate shares follow CBS; the other and undecided cells are left `unknown` rather than borrowed from the other account.

The primary-era polling record is excluded from the numbered table but three polls were registered because they frame the general election. A Fox News poll published August 13, 2026 — nine days after the primary — had Rogers ahead of El-Sayed 51% to 47% among registered voters, the only registered-voter snapshot in this archive that shows Rogers leading [SRC-0051]. Metro Times reported in May that a poll showed El-Sayed surging during the primary [SRC-0068], and Punchbowl News reported an internal Fabrizio poll from June 2025 that put Rogers well ahead in a hypothetical Republican primary [SRC-0075]. The Hill reported the Democratic primary as a toss-up after McMorrow's exit [SRC-0054]. None of these is in `polling.csv`, because the file's column names require both nominees to have been tested.

中文：`07_electoral_context/polling.csv` 仅收录七项大选民调。初选民调未收录，因为提名组合直到 8 月 5 日才确定，`elsayed_pct` / `rogers_pct` 两列不适用。两项初选时期的数据改记于此：Axios 报道初选中某一时点史蒂文斯的支出优势为 12 比 1 [SRC-0056]；Fox News 于 9 月 24 至 28 日进行的大选民调显示，在可能选民中赛义德 50%、罗杰斯 49% [SRC-0050]。有一项民调记为 `conflicting sources`：10 月 1 日的 Mitchell Research 民调，CBS 公布为 45.6–41.4，而该选举条目的表格记为 46–41，另有 7% 其他与 6% 未决定 [SRC-0037] [SRC-0001]。候选人得票率依 CBS；其他与未决定两项留为 `unknown`，不借用另一版本。

中文：初选时期的民调记录未列入编号表格，但有三项民调被登记，因为它们为理解大选提供参照。福克斯新闻于 2026 年 8 月 13 日（初选后第九天）发布的民调显示，在登记选民中罗杰斯以 51% 对 47% 领先赛义德——这是本档案中唯一显示罗杰斯领先的登记选民快照 [SRC-0051]。《地铁时报》5 月报道称一项民调显示赛义德在初选中势头上升 [SRC-0068]；Punchbowl News 报道了 2025 年 6 月 Fabrizio 的内部民调，显示罗杰斯在假设性的共和党初选中大幅领先 [SRC-0075]。《国会山报》报道麦克莫罗退选后民主党初选呈胶着状态 [SRC-0054]。这些均未列入 `polling.csv`，因为该文件的列名要求两位提名人均已被测试。

## The night-of numbers are not the certified numbers

Two sets of figures appear across the sources and must not be confused. The AP's call-time percentages — 51.9% to 46.1% with 85% counted — describe a partial count at 2:27 a.m. on November 4 [SRC-0029]. The table above describes the final published count. Every row in `election_results.csv` uses the final figures only.

中文：材料中存在两套数字，不可混淆。美联社判定时的百分比——计票 85% 时 51.9% 对 46.1%——描述的是 11 月 4 日凌晨 2:27 的部分计票 [SRC-0029]。上表描述的是最终公布计票。`election_results.csv` 的每一行仅使用最终数字。
