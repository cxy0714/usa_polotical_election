---
title: Results notes and reconciliation
title_zh: 结果说明与数据核对
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Documents the three conflicting statewide totals, the polling miss, and the missing county table; no figure has been adjusted.
---

## Three published totals / 三套公布总数

The Wikipedia infobox gives Ossoff 2,469,037 (59.03%) and Collins 1,713,664 (40.97%), summing to 4,182,701. The same article's results box gives 2,466,422 (59.02%) and 1,712,444 (40.98%), summing to 4,178,866, with the total cell left blank. NBC's live page showed 4,182,642 votes at 99% of expected. The archive uses the infobox figures in `election_results.csv` and records the others here rather than reconciling them. SRC-0001 SRC-0003

维基百科信息框给出奥索夫 2,469,037（59.03%）、柯林斯 1,713,664（40.97%），合计 4,182,701。同一条目的结果框给出 2,466,422（59.02%）与 1,712,444（40.98%），合计 4,178,866，总计栏为空。NBC 实时页在预期 99% 时显示 4,182,642 票。本档案在 `election_results.csv` 采用信息框数字，其余在此记录而不作调平。SRC-0001 SRC-0003

## The polling miss / 民调偏差

The final public averages put Ossoff about 9.4 points ahead; he won by 18.06. Every retrieved public poll understated the margin, the closest being Wick's June survey at +3.8 and the widest Echelon at +15. Two structural explanations are visible in the record: Collins's late consolidation (Trump endorsed two days before the runoff, Kemp on 14 September) and the Republican money gap, but neither is measured here. SRC-0061 SRC-0059 SRC-0001 SRC-0043 SRC-0021

选前公开平均显示奥索夫领先约 9.4 个百分点，实际为 18.06。所有已获取的公开民调都低估了差距，最接近的是 Wick 六月调查 +3.8，最大的是 Echelon +15。记录中可见两点结构性解释：柯林斯较晚完成整合（特朗普在第二轮前两天背书、肯普 9 月 14 日背书）与共和党资金劣势，但本档案未对二者作量化。SRC-0061 SRC-0059 SRC-0001 SRC-0043 SRC-0021

## The missing county table / 缺失的县表

`county_results.csv` is header-only. The Georgia Secretary of State results site (`results.sos.ga.gov`) is an Angular single-page application that returned 22 characters of text and 404 on both guessed API paths; NBC's county table is client-rendered with vote cells reading "0". No alternative machine-readable county file was retrieved. SRC-0003

`county_results.csv` 仅有表头。佐治亚州务卿结果网站（`results.sos.ga.gov`）为 Angular 单页应用，仅返回 22 个字符文本，两个推测的 API 路径均 404；NBC 县级表为客户端渲染，票数单元显示"0"。未取得其他机器可读的县级文件。SRC-0003

## Call timing and concession / 判定时间与承认败选

The Associated Press called the race just under an hour after polls closed; Collins conceded at his campaign headquarters that evening, and Ossoff spoke afterwards. SRC-0097 SRC-0004 SRC-0002

美联社在投票结束不到一小时后判定结果；柯林斯当晚在竞选总部承认败选，奥索夫随后发表讲话。SRC-0097 SRC-0004 SRC-0002

## What would settle it / 如何最终核定

A certified county canvas from the Secretary of State, or the FEC's candidate-finance filings cross-checked against the results, would resolve the 3,835-vote discrepancy between the two Wikipedia tables.

州务卿的县级认证计票，或用 FEC 申报与结果交叉核对，可解决维基两张表之间 3,835 票的差异。
