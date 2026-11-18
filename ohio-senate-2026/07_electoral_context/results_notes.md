---
title: Results notes: the 2026 Ohio U.S. Senate special election
title_zh: 结果说明：2026 年俄亥俄州联邦参议员特别选举
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Vote counts, rounding, documented conflicts and the county-level gap; percentages are recomputed from the counts wherever the sources disagree.
---


# Results notes

## The result

| Candidate | Party | Votes | Share |
|---|---|---|---|
| Sherrod Brown | Democratic | 2,302,669 | 50.01% |
| Jon Husted | Republican | 2,080,064 | 45.17% |
| Bill Redpath | Libertarian | 128,341 | 2.79% |
| Greg Levy | Party for Socialism and Liberation | 93,786 | 2.04% |
| **Total** | | **4,604,860** | **100.00%** |

Brown won by 222,605 votes, a margin of 4.84 percentage points. The four vote counts sum exactly
to the reported total, which is the strongest internal check available without the official
canvass.

## Rounding, and one documented conflict

The printed percentages sum to 100.01, not 100.00: 50.01 + 45.17 + 2.79 + 2.04. That is ordinary
rounding of four shares that each carry two decimals, not an error in the counts.

Two shares disagree between sources. The Calfee newsletter cited by the race article prints
Husted at **45.15%** and Levy at **2.05%**; the article's election box prints 45.17% and 2.04%.
Recomputed from the vote counts, Husted is 2,080,064 / 4,604,860 = 45.171% and Levy is
93,786 / 4,604,860 = 2.037%. The vote counts are the primary fact and the computed shares match
the article's box, so 45.17 and 2.04 are retained, with the Calfee figures recorded as
`conflicting sources` in `election_results.csv`.

## Turnout and early voting

Nearly 4.56 million Ohioans voted. More than 1.7 million voted early, about 17% more than in
2022, and the early electorate split roughly 468,000 Democratic, 432,000 Republican and 807,000
unaffiliated SRC-1182. The unaffiliated share of early votes is
the single most interesting number in the file: it is larger than the two party blocs combined.

## The county picture, and the gap

**There is no county-results table in this archive.** The race article publishes two county-level
*map* graphics (one for the general election, one for the Democratic primary) but no table of
county vote totals, and the Ohio Secretary of State's canvass spreadsheets returned HTTP 403 to
this archiver. `county_results.csv` is therefore header-only, with zero rows, and that is a
documented gap rather than an omission.

What the maps do support is a list of seven counties that flipped from Republican to Democratic
between the 2024 presidential result and this Senate result: Delaware, Erie, Lake, Mahoning,
Portage, Trumbull and Wood. Those seven names are recorded here and in `research_gaps.md`; the
underlying county totals are not.

## The primary results

Brown 712,106 (89.40%) to Kincaid 84,405 (10.60%) on 2026-05-05; Husted unopposed with 736,413.
The 796,511 Democratic primary votes are 17% of the general-election turnout, which is a normal
drop-off for a non-competitive primary.

## Dates that are corrected here

Husted's appointment and oath are dated 2025-01-17 and 2025-01-21 respectively
SRC-1016SRC-1178. The
brief's alternative dates (2025-01-10, 2025-01-14) are rejected; see `election_context.md`.

## Contested characterisations

The result was read two ways in the coverage. Cleveland.com's analysis framed it as a personal
rebuke of Husted and of his corporate ties SRC-1076; other coverage framed it as Brown's
return to a seat he had held for 18 years. Both readings are recorded in `media_coverage.csv` as
framing, not as findings.

## 中文摘要

布朗以 2,302,669 票（50.01%）胜出，赫斯特德 2,080,064 票（45.17%），Redpath 128,341 票
（2.79%），Levy 93,786 票（2.04%），合计 4,604,860 票，四人票数精确相加等于总数，这是不使用官方
canvass 时最强的内部校验。印刷的百分比相加为 100.01，属四舍五入，不是错误。Calfee 通讯把赫斯特
德记为 45.15%、Levy 记为 2.05%，与条目选举框的 45.17%／2.04% 不同；按票数重算分别为 45.171% 与
2.037%，故保留条目数值并把 Calfee 记为"来源冲突"。投票率近 456 万，提前投票超过 170 万（比 2022
年高约 17%），其中无党派约 80.7 万，超过两党各自份额。**本档案没有县结果表**：条目只有两张县级
地图、没有表格，州务卿的 canvass 电子表格返回 403；`county_results.csv` 因此只有表头、零行，
这是已记录的缺口而非遗漏。地图能支持的只是七个由共和党翻向民主党的县：Delaware、Erie、Lake、
Mahoning、Portage、Trumbull、Wood。赫斯特德的任命与宣誓日期分别为 2025-01-17 与 2025-01-21。
