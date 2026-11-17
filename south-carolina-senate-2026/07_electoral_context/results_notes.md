---
title: "Results notes — provenance, integrity checks and reading rules"
title_zh: "结果说明——来源、完整性校验与阅读规则"
candidate_id: both
compiled_by: Lead Research Agent
last_updated: 2026-11-12
status: in_progress
coverage_note: "County table verified against statewide totals; certification status unknown; one source typo corrected and one prose/table discrepancy left unresolved."
---

# Results notes — provenance, integrity checks and reading rules / 结果说明——来源、完整性校验与阅读规则

## 1. Provenance: projected, not certified / 1. 来源：预测值，非认证值

Every figure in [`election_results.csv`](election_results.csv) and
[`county_results.csv`](county_results.csv) is transcribed from the Wikipedia results tables, which
in turn cite the New York Times results page and the South Carolina Election Commission. CBS News
"projects" Andrews the winner. **No state certification (scvotes.gov canvass) was retrieved in this
pass**, so the whole file is `partially verified` — including the general-election totals.

[`election_results.csv`](election_results.csv) 与 [`county_results.csv`](county_results.csv) 中的每个数字都转录自维基百科结果表，而这些表又引用《纽约时报》结果页与南卡罗来纳州选举委员会。CBS 新闻「预测」安德鲁斯胜选。**本次未取得州级认证（scvotes.gov 的官方计票）**，因此整份文件——包括大选总票数——均标记为 `partially verified`。

The article's own `last_update` field reads *November 11, 2026, 12:27 AM*, which is the moment the
transcribed tables were last consistent with each other.

条目自身的 `last_update` 字段为 *2026 年 11 月 11 日 12:27（美东）*，即所转录表格彼此一致的最后时点。

## 2. Integrity checks actually run / 2. 实际执行的完整性校验

Rather than trusting the county table, four checks were run and their results are recorded here:

不是直接信任县表，而是执行了四项校验，结果记录如下：

| Check / 校验 | Result / 结果 |
|---|---|
| Sum of 46 county Andrews votes vs statewide | 1,044,001 = 1,044,001 ✅ |
| Sum of 46 county Graham votes vs statewide | 952,191 = 952,191 ✅ |
| Sum of 46 county total_votes vs statewide total | 2,041,487 = 2,041,487 ✅ (after the fix in §3) |
| Sum of other_votes (Whitener + Hackett + write-in) | 45,295 = 23,585 + 16,811 + 4,899 ✅ |

The county table is therefore internally consistent with the statewide result, and the two
candidate columns are the strongest part of the dataset: they reconcile to the vote, not to a
percentage.

因此县表与全州结果内部自洽，两位候选人的票数列是整份数据中最可靠的部分：它们与总票数对得上，而非只与百分比对得上。

## 3. One source typo, corrected by arithmetic / 3. 一处源数据笔误，以算术修正

The row for **Edgefield** writes its total as `10.821` — a decimal point where the table's own
convention uses a thousands separator. Its five component cells are 4,593 + 5,972 + 127 + 101 + 28 =
**10,821**, which is the value carried in `county_results.csv`. The correction is this one cell; it
was not applied silently, and it is the reason the third check above passes.

**Edgefield** 一行的总数写作 `10.821`——该表的惯例是用千位分隔符，此处却写成了小数点。其五个分项单元格为 4,593 + 5,972 + 127 + 101 + 28 = **10,821**，这正是 `county_results.csv` 中所载的值。修正仅涉及这一个单元格；它并非静默套用，也正是上表第三项校验得以通过的原因。

## 4. One discrepancy left unresolved / 4. 一处未解决的差异

The article's analysis paragraph states that Andrews "won a total of 25 counties". The county table
yields **24**: Allendale, Bamberg, Barnwell, Berkeley, Calhoun, Charleston, Clarendon, Colleton,
Darlington, Dillon, Dorchester, Fairfield, Florence, Greenville, Hampton, Jasper, Lee, Marion,
Marlboro, Orangeburg, Richland, Sumter, Williamsburg and York. Graham carried the other 22.

条目的分析段落称安德鲁斯「共赢下 25 个县」。县表给出 **24** 个：Allendale、Bamberg、Barnwell、Berkeley、Calhoun、Charleston、Clarendon、Colleton、Darlington、Dillon、Dorchester、Fairfield、Florence、Greenville、Hampton、Jasper、Lee、Marion、Marlboro、Orangeburg、Richland、Sumter、Williamsburg、York。格雷厄姆赢下其余 22 个。

The archive does not pick a winner between the two statements. The likely explanations — a county
counted at a rounding boundary, an error in the prose, or a county the table folds in elsewhere —
cannot be distinguished without the precinct or county canvass. `⚠ unknown`

档案不在两种说法之间择一。可能的解释——某个县处在四舍五入边界、段落有误、或某个县被表格并入他处——在没有选区级或县级官方计票的情况下无法区分。`⚠ unknown`

## 5. How to read the numbers / 5. 如何阅读这些数字

- `andrews_pct` / `graham_pct` are each candidate's share of that county's total votes, as printed.
  They do not sum to 100 with `other_votes`, because the write-in share is small and rounding is per
  cell.
- `other_votes` is a **derived sum** of three documented columns (Whitener, Hackett, write-in); the
  county schema has no separate column for each minor candidate, and the parsed source table that
  carries them is kept at `_staging/mirrors/county_results_parsed.csv`.
- `winner` in `election_results.csv` is a per-row flag, not a certification.
- Party labels are as printed by the source: `Democratic`, `Republican`, `Libertarian`,
  `Constitution`, `Write-in`.

- `andrews_pct`／`graham_pct` 是各候选人在该县总票数中的占比，按原文照录。它们与 `other_votes` 不会恰好合计 100，因为写名票占比很小且逐格四舍五入。
- `other_votes` 是三个有据可查的列（惠特纳、哈克特、写名）的**求和派生值**；县表模式中没有为每位小党候选人单列一列，承载这些原始数据的解析表保存在 `_staging/mirrors/county_results_parsed.csv`。
- `election_results.csv` 中的 `winner` 是逐行标记，不是认证结果。
- 党籍标签按来源原文：`Democratic`、`Republican`、`Libertarian`、`Constitution`、`Write-in`。

## 6. What the exit poll can and cannot support / 6. 出口民调能支撑什么、不能支撑什么

[`../09_sources/exit_poll_2026.csv`](../09_sources/exit_poll_2026.csv) holds 45 subgroups in 15
groups, transcribed from the CNN table. It supports statements of the form "among self-identified
independents, Andrews led 63–32". It does **not** support causal statements, subgroup turnout
estimates, or claims about individual voters, and its subgroup sizes are not published in the
source, so no subgroup margin of error is computable here. `⚠ unknown`

[`../09_sources/exit_poll_2026.csv`](../09_sources/exit_poll_2026.csv) 收录 15 组共 45 个子群，转录自 CNN 表格。它可以支撑「在自认独立人士中，安德鲁斯以 63–32 领先」这类陈述。它**不能**支撑因果陈述、子群投票率估计或关于个体选民的断言；来源未公布各子群样本量，因此此处无法计算任何子群的误差范围。`⚠ unknown`

## 7. Not attempted / 7. 未尝试的内容

- Precinct-level aggregation or mapping.
- Ecological inference from county results to individual behaviour.
- Any turnout comparison with 2020 or 2022 (the baseline figures were not retrievable).
- Certification reconciliation against scvotes.gov.

- 选区级汇总或绘图。
- 由县级结果向个体行为的生态推断。
- 与 2020 或 2022 年的投票率比较（基线数据未能检索）。
- 与 scvotes.gov 认证结果的核对。

## Sources

- [SRC-2108] `https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_South_Carolina`
- [SRC-2111] `https://www.cbsnews.com/news/south-carolina-2026-senate-annie-andrews-darline-graham/`
