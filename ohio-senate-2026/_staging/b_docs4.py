# -*- coding: utf-8 -*-
"""Build election_context.md, results_notes.md and candidate_comparison.md."""
import sys

sys.path.insert(0, "_staging")
from doc_lib import render, write  # noqa: E402

FM = """---
title: {title}
title_zh: {zh}
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: {note}
---

"""

CTX = FM.format(
    title="Election context: the 2026 Ohio U.S. Senate special election",
    zh="选举背景：2026 年俄亥俄州联邦参议员特别选举",
    note="Explains the special-election mechanics, the appointment sequence and the national "
         "setting; dates for the appointment are corrected against sources and flagged.") + """
# Election context

## Why there was a special election

Ohio's Class 1 Senate seat was up in 2024, and JD Vance won it. When Vance became vice
president, he resigned the seat effective **2025-01-10** {{ref001_www_nbc4i_com_news_politics_sen_j_d_vance_to_resign_ahe}}. Governor Mike
DeWine announced **on 2025-01-17** that he would appoint Lieutenant Governor Jon Husted
{{ocj25_ohio_lt_gov_jon_husted_to_replace_jd_vance_in_u_s_senat}}, and Husted was **sworn in on
2025-01-21** {{husted_sworn_in_2025}}. The 2026 election is therefore a special election to
complete the remainder of the 2022 term, not a regular Class 1 election; the seat is next up in
the regular cycle in 2028.

The task brief for this archive stated that Husted was "appointed 2025-01-10 and sworn in
2025-01-14". Neither date is supported. 2025-01-10 is the date Vance's resignation took effect;
2025-01-14 is the date of a different inauguration. The corrected sequence is used throughout
this archive and the discrepancy is recorded in `research_gaps.md` and `results_notes.md`.

## The electoral setting

Ohio has moved sharply Republican at the presidential level, and the 2026 environment was
dominated by cost of living. The race drew national money because Senate control was close:
outside groups spent more than $325 million, and AdImpact rated Ohio the most expensive Senate
race in the country {{ocj30_outside_groups_pour_hundreds_of_millions}}. Turnout was nearly 4.56
million votes, with more than 1.7 million cast early — up about 17% on 2022, and split roughly
468,000 Democratic, 432,000 Republican and 807,000 unaffiliated {{ref195_www_calfee_com_newsletters_830}}.

## The candidates on the ballot

Four candidates were on the general-election ballot: Sherrod Brown (Democratic), Jon Husted
(Republican), Bill Redpath (Libertarian) and Greg Levy (Party for Socialism and Liberation). A
second Libertarian, Jeffrey Kanter, was disqualified from the ballot earlier in the year. The
party label for Levy is itself contested: the race article's election box calls him an
independent, while ABC 6 and Cincinnati Magazine name the Party for Socialism and Liberation;
`election_results.csv` follows the party designation reported by the outlets that interviewed
him and flags the conflict.

## The primary

Ohio held its primary on 2026-05-05. Brown won the Democratic primary with 712,106 votes
(89.40%) against Ron Kincaid's 84,405 (10.60%); Husted was unopposed on the Republican side with
736,413 votes. The race article's biography of Husted says he "won the Republican nomination in
March 2026", which conflicts with the 5 May canvass; the canvass governs, and the conflict is
recorded.

## What made this race unusual

Three features distinguish it from a normal Senate race. First, both candidates had long Ohio
records — Brown with 50 years in office (Husted's framing) and Husted with statewide office since
2011 — so the argument was about records rather than introductions. Second, the incumbent was
appointed rather than elected, which let Brown attack him as both an insider and an unratified
choice. Third, a single state-level policy area, data-center siting and the electricity bills
that follow it, became the closing argument of the Democratic campaign
{{ocj31_leaked_memo_about_data_centers_shows_gop_worried_about}}.

## 中文摘要

俄亥俄 Class 1 参议院席位 2024 年由万斯赢得；万斯就任副总统后于 2025-01-10 辞职生效。德温州长
于 2025-01-17 宣布任命副州长赫斯特德，赫斯特德于 2025-01-21 宣誓就职。因此 2026 年选举是填补
2022 年任期剩余部分的特别选举，而非正常换届。任务简报所称"2025-01-10 任命、2025-01-14 宣誓"
两个日期都不成立：前者是万斯辞职生效日，后者是另一场就职典礼的日期。本档案全篇采用更正后的序列，
并把差异记入 research_gaps 与 results_notes。总投票数近 456 万，提前投票超过 170 万（比 2022 年
高约 17%），其中民主党 46.8 万、共和党 43.2 万、无党派约 80.7 万。选票上有四位候选人：布朗、赫
斯特德、Redpath（自由党）、Levy（社会主义与解放党；竞选条目称其为独立人士，此处按受访媒体标注
并记录冲突）。初选于 2026-05-05 举行，布朗以 89.40% 胜出，赫斯特德无人竞争。
"""

RESULTS = FM.format(
    title="Results notes: the 2026 Ohio U.S. Senate special election",
    zh="结果说明：2026 年俄亥俄州联邦参议员特别选举",
    note="Vote counts, rounding, documented conflicts and the county-level gap; percentages are "
         "recomputed from the counts wherever the sources disagree.") + """
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
unaffiliated {{ref195_www_calfee_com_newsletters_830}}. The unaffiliated share of early votes is
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
{{ocj25_ohio_lt_gov_jon_husted_to_replace_jd_vance_in_u_s_senat}}{{husted_sworn_in_2025}}. The
brief's alternative dates (2025-01-10, 2025-01-14) are rejected; see `election_context.md`.

## Contested characterisations

The result was read two ways in the coverage. Cleveland.com's analysis framed it as a personal
rebuke of Husted and of his corporate ties {{b4_cle_rebuke}}; other coverage framed it as Brown's
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
"""

COMPARE = FM.format(
    title="Candidate comparison: Brown and Husted",
    zh="候选人比较：布朗与赫斯特德",
    note="Structured comparison across career, record, message, coalition, money and media; "
         "differences are stated as documented, and unresolved items are marked unknown.") + """
# Candidate comparison

## At a glance

| | Sherrod Brown (D) | Jon Husted (R) |
|---|---|---|
| Age at election | 74 (born 1952-11-09) | 59 (born 1967-08-25) |
| Prior office | U.S. Senator 2007-2025; U.S. House 1993-2007; Ohio Secretary of State 1983-1991; Ohio House 1975-1983 | U.S. Senator from 2025-01-21 (appointed); Lieutenant Governor 2019-2025; Ohio Secretary of State 2011-2019; Ohio Senate 2009-2011; Ohio House 2001-2009 |
| Route onto the ballot | Won a contested primary, 2026-05-05 | Appointed to the seat, 2025-01-17; unopposed primary |
| Core message | The system is rigged for corporations and billionaires | Ohio's turnaround is Republican, and Brown is the past |
| Signature policy fight | Data-center tax abatements and utility bills | Tenure attack; manufacturing and tariffs |
| 2026-09-30 cash on hand | $4,452,803 | $4,239,097 |
| Cycle receipts to 2026-09-30 | $68,409,200 | $19,894,786 |
| Result | 2,302,669 (50.01%) | 2,080,064 (45.17%) |

## Career shape

Brown's career is legislative and cumulative: 1975 in the Ohio House, then Secretary of State,
then eight terms in the U.S. House, then three Senate terms. His self-presentation depends on
that depth — the Dignity of Work frame is presented as four decades of observation, not a new
idea. Husted's career is executive and administrative: Speaker of the Ohio House, Secretary of
State (where he ran elections), then Lieutenant Governor with a portfolio of workforce and
economic development, then an appointed Senate seat. Each man's strongest claim is the other's
weakest: Brown can say he has always fought for workers; Husted can say he has actually run
things.

## The incumbency problem, dated

Husted's incumbency is unusual and must be dated wherever it is asserted: appointed 2025-01-17,
sworn in 2025-01-21. He had never faced Ohio voters for this seat. Brown's counter-attack treats
him as both a Washington insider and an unelected one, which is why the "special interest guy in
Washington" line and the "golden boy" line appear in the same closing speech.

## Where their records collide

**Data centers.** Brown attacks the tax abatements and the electricity bills; Husted sponsored a
bill that requires regulators only to *consider* a blueprint for large-load customers, a gap his
opponents used. This is the clearest case of a policy difference with an audit trail.

**Tariffs.** Husted frames tariffs as protection for manufacturing ("Protecting American
manufacturing is the America First agenda"); Brown attacks them as a cost on farmers. Brown's own
record is protectionist — anti-NAFTA, pro-2018 washing-machine tariffs, pro-USMCA — so the 2026
rhetoric is a shift, documented in `policy_positions.csv`.

**Health care.** Husted said in December 2025 that ACA subsidies should be "frozen"; in October
2026 he sponsored a two-year extension. Brown's position is a straight defence of the ACA.

**Abortion.** Husted told the January 2026 HELP Committee hearing that restricting the abortion
pill is a safety measure, and used his own adoption story as the warrant. Brown's record is
pro-choice with a documented late-career shift toward codifying Roe.

## Coalition and coalition costs

Brown's endorsements are almost entirely labour: UAW, USW, IUPAT, UFCW, CWA, OFT, the Ohio
AFL-CIO, AFGE, Teamsters, firefighters and patrolmen, plus environmental and rights groups (LCV,
Giffords, HRC, MoveOn, JDCA). Husted's are almost entirely officeholders and business: the
attorney general, treasurer, auditor, five members of Congress, 75 sheriffs, ABC of Ohio, the
Operating Engineers, the Boilermakers, the Cleveland Building Trades and the U.S. Chamber. The
two coalitions barely overlap, and the only labour body that endorsed a Republican here was in
the building trades.

## Money, and what it obscured

Brown out-raised Husted by roughly 3.4 to 1 across the cycle, yet entered the final month with
almost identical cash on hand ($4.45m versus $4.24m) because he spent 96% of what he raised.
Outside groups spent more than $325 million, dwarfing both campaigns. Any comparison that stops
at the candidate tables will misdescribe this race.

## Communication, side by side

Brown argues from a category to a person and closes with a we-versus-them line. Husted argues
from a record to a question and repeats the same question at every stop ("Can you name one thing
that he's done to make your life better?"). Brown's numbers are his own counts; Husted's numbers
are state-level statistics. Brown's weakness is that his 2015 praise of an Amazon data center
contradicts his 2026 attack; Husted's is that his data-center bill does less than his message
implies.

## What this comparison cannot settle

No debate record exists, so the two men were never compared side by side in a retrieved
transcript. Crowd sizes are unmeasured. County-level results are unavailable, so the geographic
basis of the 4.84-point margin cannot be reconstructed from this archive.

## 中文摘要

布朗的生涯是立法与累积型的（1975 年州众议院起，历经州务卿、八届联邦众议员、三届参议员），赫
斯特德的生涯是行政与治理型的（州众议院议长、州务卿、副州长、2025 年被任命的参议员）。两人最强
的主张恰好是对方最弱的地方。赫斯特德的"在职"必须标注日期：2025-01-17 获任命、2025-01-21 宣誓，
从未以此席位面对选民。政策碰撞集中在数据中心（布朗攻击税收减免与电费，赫斯特德的法案只要求监管
机构"考虑"蓝图）、关税（赫斯特德视为保护制造业，布朗视为农民成本，而布朗自身保护主义记录与
2026 说法有落差）、医保（赫斯特德 2025 年 12 月主张"冻结"补贴，2026 年 10 月联署两年延期）与堕
胎。联盟几乎不重叠：布朗几乎是工会全体，赫斯特德是州级官员、75 位警长与商会。募款 3.4 倍差距在
终点现金上被抹平（445 万 vs 424 万），因为布朗花掉了 96%。本档案没有辩论记录，也没有县级结果，
因此无法重建 4.84 个百分点差距的地理基础。
"""

write("07_electoral_context/election_context.md", render(CTX))
write("07_electoral_context/results_notes.md", render(RESULTS))
write("08_comparative_analysis/candidate_comparison.md", render(COMPARE))
print("done")
