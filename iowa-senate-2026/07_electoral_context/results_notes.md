---
title: Results notes — reconciliation and variance
title_zh: 结果说明——核对与差异
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: All arithmetic reconciled; two documented variance points (statewide total and primary percentages) are explained, not smoothed.
---

# Results notes — reconciliation and variance / 结果说明

## 1. General election / 大选

English: The figures used in `election_results.csv` and `county_results.csv` are the NBC News results feed:
Turek 688,746 (50.56%), Hinson 631,482 (46.35%), Laehn 42,109 (3.09%), total 1,362,337. The three candidate
figures sum exactly to the published total, and each percentage recomputes from the votes to two decimals
(50.558, 46.353, 3.091). **County check:** the 99 rows of `county_results.csv` sum to 688,746 / 631,482 /
42,109 and to 1,362,337 — an exact match to the statewide totals, which is the strongest internal check in
this case.

中文：`election_results.csv` 与 `county_results.csv` 采用 NBC 新闻的计票数据：Turek 688,746（50.56%）、Hinson 631,482（46.35%）、Laehn 42,109（3.09%），合计 1,362,337。三名候选人票数精确相加等于公布总数，各百分比按票数重算到两位小数亦一致（50.558、46.353、3.091）。**县级核对**：`county_results.csv` 的 99 行合计为 688,746 / 631,482 / 42,109，总计 1,362,337，与全州总数完全一致——这是本案最强的内部一致性检验。

## 2. Documented variance: six votes / 已记录的差异：六票

English: The race article's election box gives Turek 688,741, Hinson 631,481, Laehn 42,109 and a total of
1,362,331 — six votes fewer than the NBC feed, and internally consistent on its own terms. The archive uses
the NBC figures because they are the county-level source, and records the six-vote difference here rather than
adjusting either figure. A six-vote gap does not change the winner or the margin at two decimals (4.21 points).

中文：竞赛条目的选举信息框给出 Turek 688,741、Hinson 631,481、Laehn 42,109，总计 1,362,331——比 NBC 数据少六票，但其自身内部自洽。档案采用 NBC 数据（因其为县级数据来源），并在此记录六票差异，不改动任何一方数字。六票之差不会改变胜者，也不会改变保留两位小数的差距（4.21 个百分点）。

## 3. Primary percentages / 初选百分比

English: The Republican primary election box gives 74.2 / 25.8 (153,059 / 53,196, total 206,255) and the
Democratic box 62.7 / 37.3 (120,287 / 71,663, total 191,950). Night-of reporting used slightly different
numbers: 74% to 26% for Hinson (`SRC-0040`) and 62.6% to 37.4% for Turek with 99% of precincts counted
(`SRC-0054`). Both sets are recorded; the archive keeps the election-box versions in `election_results.csv` and
notes the night-of versions in `notes` on each row. Recomputation from the votes gives 74.21 / 25.79 and
62.66 / 37.34, which is why the rounded pairs differ by a tenth.

中文：共和党初选信息框为 74.2 / 25.8（153,059 / 53,196，合计 206,255），民主党为 62.7 / 37.3（120,287 / 71,663，合计 191,950）。当晚报道用的是略有不同的数字：Hinson 74% 对 26%（`SRC-0040`），Turek 在 99% 选区计票时为 62.6% 对 37.4%（`SRC-0054`）。两套数字均予记录：`election_results.csv` 采用信息框版本，并在每行 `notes` 注明当晚版本。按票数重算得 74.21 / 25.79 与 62.66 / 37.34，这正是四舍五入后相差零点一个百分点的原因。

## 4. The Libertarian column / 自由意志党一栏

English: Thomas Laehn qualified by petition after submitting nearly 10,000 signatures on 2 June 2026 against a
3,500 requirement. His 3.09% is smaller than the 4.21-point margin, so he did not decide the outcome
arithmetically; the archive states that as arithmetic, not as a claim about his voters.

中文：Thomas Laehn 于 2026 年 6 月 2 日提交近 1 万份签名（门槛 3,500 份）后以请愿方式取得资格。其 3.09% 小于 4.21 个百分点的差距，因此从算术上并未决定结果；档案只陈述这一算术事实，不对其选民做任何推断。

## 5. What could not be reconciled / 无法核对的部分

- No official county canvass from the Iowa Secretary of State could be read: `sos.iowa.gov` returned HTTP 403
  and the results application served a JavaScript shell only. The NBC feed is therefore the county authority
  here, not the state.
- No precinct-level file was retrieved, so the county rows cannot be checked against a second county source.
- The FEC's own pages returned HTTP 403; finance figures come from the summary table reproduced by the race
  article and are marked `partially verified`.
