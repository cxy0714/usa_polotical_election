---
title: "Results Notes — 2026 Los Angeles Mayoral Election"
title_zh: "结果说明 — 2026 年洛杉矶市长选举"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: "Documents how every number in election_results.csv was obtained and reconciled, including the two one-vote discrepancies and the single-source runoff."
---

# Results notes / 结果说明

## 1. What the numbers rest on / 数字的依据

**Primary.** Every candidate row comes from the NBC News live-results page [SRC-0021], whose saved HTML
embeds a results JSON with each candidate's vote total. The fourteen rows sum to **853,894**, which is the
total that page publishes; no row was adjusted to make the sum work.

**初选。** 每位候选人的数据来自 NBC News 实时结果页 [SRC-0021]，其保存的 HTML 内嵌含各候选人票数的
结果 JSON。十四行合计 **853,894**，正是该页公布的总数；没有任何一行被调整以凑总数。

**Runoff.** Every runoff figure in this environment comes from the Wikipedia results table [SRC-0001]. The
AP live-results project page [SRC-0022] served no static figures (its data loads client-side), and every
lateral attempt to confirm the runoff totals failed: the county registrar returned `URLError`, the NBC
runoff-result URLs returned 404, and a CNN election page that returned 200 (4.7 MB) contained none of the
runoff totals. The two runoff rows are therefore `partially verified`, and the archive says so in
`election_results.csv` rather than upgrading them.

**决选。** 本环境中所有决选数字均来自维基百科结果表 [SRC-0001]。AP 实时结果项目页 [SRC-0022] 未提供
静态数字（数据由前端加载），而所有横向核实决选总数的尝试均失败：县选务处返回 `URLError`，NBC 的
决选结果 URL 返回 404，一份返回 200（4.7 MB）的 CNN 选举页不含任何决选总数。因此两行决选数据为
`partially verified`，档案在 `election_results.csv` 中如实标注，而不升级其状态。

## 2. Arithmetic checks performed / 已执行的算术校验

| Check | Result |
|---|---|
| Primary candidate votes sum to published total (853,894) | passes exactly |
| Primary shares recomputed from votes ÷ 853,894, rounded to 0.1 | pass; published top-three shares (34.3 / 29.0 / 25.5) match exactly |
| Runoff votes sum to published total (1,120,223) | passes exactly |
| Runoff shares recomputed (615,264 ÷ 1,120,223 = 54.92%; 504,959 ÷ 1,120,223 = 45.08%) | pass, round to 54.9 / 45.1 |
| Runoff margin vs. primary margin | 110,305 vs. 44,812 (opposite signs) |

**Percentages for candidates outside the published top three are computed**, not quoted: the NBC page
prints shares only for Bass, Raman and Pratt. Each such row's `notes` says the percentage is computed from
votes ÷ total. This is arithmetic on two published numbers, not an estimate.

**前三名之外的候选人百分比是计算值**，不是引用值：NBC 页面只公布 Bass、Raman 与 Pratt 的份额。
每一此类行的 `notes` 均注明百分比由"票数 ÷ 总数"计算。这是对两个公布数字的算术，不是估算。

## 3. The two one-vote discrepancies / 两处一票差异

| Candidate | NBC News [SRC-0021] | Wikipedia [SRC-0001] | Archive records |
|---|---:|---:|---|
| Juanita Lopez | 13,033 | 13,032 | 13,033, `conflicting sources` |
| Bryant Acosta | 3,471 | 3,470 | 3,471, `conflicting sources` |
| Total | 853,894 | 853,892 | 853,894 |

Both tables are internally consistent: the Wikipedia candidate list sums to its own 853,892 total, and the
NBC list sums to 853,894. The difference is therefore not a dropped candidate but a two-vote divergence in
totals, most plausibly a late batch or a transcription difference. The archive does **not** average, adjust
or choose a "likely" figure; it records the news-service numbers, flags the two rows, and leaves resolution
to the official canvass (`research_gaps.md` G1, G2).

两表各自自洽：维基候选人名单加总等于其 853,892，NBC 名单加总等于 853,894。因此差异不是漏掉某位
候选人，而是总数上两票的分歧，最可能是晚间批次或转录差异。档案**不**取平均、不调整、也不选一个
"更可能"的数字；它记录通讯社数字、标注两行，把裁决留给官方计票（`research_gaps.md` G1、G2）。

## 4. Write-in candidates / 补写候选人

The city clerk certified two write-in candidates for the primary (griselda diaz, misael ortega)
[SRC-0002]. Their votes appear in no retrieved results table, so the published 853,894 excludes them and
the archive cannot state their share. The fourteen named candidates are therefore all candidates with
published totals, not all candidates on the ballot.

市书记官为初选认证了两名补写候选人（griselda diaz、misael ortega）[SRC-0002]。其票数不见于任何
已获取结果表，故公布的 853,894 不含其票，档案也无法给出其份额。因此十四位具名候选人是"有公布票数
的候选人"，而非"选票上的全部候选人"。

## 5. Missing denominators / 缺失的分母

Turnout, ballots cast and registered voters are not published in any retrieved source for either round
(the Wikipedia infobox carries `volume = 0`). The archive records turnout as `unknown` and does not divide
the vote totals by an assumed electorate. Consequently no claim in this archive compares 2026 turnout with
2022 or 2020.

两轮的投票率、投票数与登记选民数在任何已获取来源中均未公布（维基信息框为 `volume = 0`）。档案将
投票率记为 `unknown`，不以假设的选民基数去除总票数。因此本档案中没有任何论断把 2026 年投票率与
2022 或 2020 年相比。

## 6. Why county_results.csv is header-only / 为什么 county_results.csv 只有表头

The Los Angeles mayor is elected citywide, by voters inside the city boundary, not by county voters. A
county-level table would aggregate a jurisdiction that does not decide this race, and every plausible
county-level number (countywide registration, countywide turnout) would be a category error. The file is
therefore present with its full header and zero rows, and this note is its explanation. The correct
sub-city unit — council district or precinct — could not be retrieved (`research_gaps.md` G5), which is
why no district table replaces it.

洛杉矶市长由全市选民选出，选民范围为市界之内，而非全县选民。县级表会汇总一个并不决定本选举的
辖区，任何看似合理的县级数字（全县登记数、全县投票率）都属范畴错误。因此该文件保留完整表头、
零行数据，本说明即为其解释。正确的市域以下单位——市议会分区或选区——无法获取
（`research_gaps.md` G5），因此也没有分区表替代它。

## 7. Reading the winner column / 如何读 `winner` 列

`winner = yes` marks advancement in the primary (two rows) and election in the runoff (one row). It does
not mark a plurality lead. Where a source described Bass as "leading" on primary night before counting
finished, that is a count-order statement, not a result; the archive records the final table only.

`winner = yes` 在初选中表示晋级（两行），在决选中表示当选（一行），不表示得票领先。若有来源在
初选夜计票未完成时称 Bass "领先"，那是计票顺序的陈述而非结果；档案只记录最终表。
