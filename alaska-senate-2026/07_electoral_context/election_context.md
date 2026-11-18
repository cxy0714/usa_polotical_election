---
title: "Alaska 2026 — electoral context"
title_zh: "阿拉斯加 2026 — 选举背景"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: "Institutional and national context solid; Alaska's district-level and registered-voter composition details are thin."
---

# Electoral context / 选举背景

## The rules that shaped the race

Alaska uses a **top-four nonpartisan primary** followed by a **ranked-choice general election**. All
candidates appear on one primary ballot regardless of party; the four highest finishers advance; the
general is decided by instant-runoff tabulation unless someone clears 50% on first choices. The system
was adopted by initiative in 2020, and 2026 featured **Ballot Measure 2**, an initiative to repeal it
and return to partisan primaries. The measure failed: NO 147,831 (53.81%) to YES 126,919 (46.19%)
(SRC-0001). Alaska's 40 state house districts — not counties — are the reporting unit for legislative
results, which is why `county_results.csv` is header-only.

阿拉斯加采用**前四名无党派初选**加**排序复选大选**。所有候选人不论党派同列一张初选票，前四名晋级；
大选除首轮过半者外，经即时淘汰计票决定。该制度源于 2020 年公民创制，2026 年同时举行**第 2 号公投**
试图废除并恢复党派初选，结果以反对 147,831 票（53.81%）对赞成 126,919 票（46.19%）未获通过
（SRC-0001）。立法选举结果按 40 个州众议院选区而非县公布，因此 `county_results.csv` 仅有表头。

## The state's partisan baseline

Alaska has not voted Democratic for president since 1964, and one Senate seat has been held by the
Murkowski family since 1981 (SRC-0056). Trump carried the state three times, but never reached 55% of
the vote (SRC-0056). The state's politics are therefore not safely Republican so much as
Republican-leaning with a durable independent streak: a top-four primary with a ranked-choice general
rewards candidates who can win second choices, and Alaska's congressional delegation has alternated.

阿拉斯加自 1964 年以来未在大选中投给民主党总统候选人，其中一个参议院席位自 1981 年起由穆尔科斯基
家族持有（SRC-0056）。特朗普三度拿下该州，但得票从未达到 55%（SRC-0056）。因此该州政治并非稳固
共和党，而是"偏共和党且长期存在独立倾向"：前四名初选加排序复选大选有利于能赢得第二选择的候选人，
其国会代表团也屡有交替。

## The national setting

Democrats entered 2026 needing a net gain to govern comfortably and left with 56 Senate seats, a
result Senate Democratic Leader Chuck Schumer called "a prime position to create a durable majority"
(SRC-0056). Alaska was one of the seats that made that arithmetic work: a Republican-held seat in a
state Trump won, flipped by a former House member. National coverage treated the race as a test of
whether Trump-era Republican branding still worked in a resource-dependent state (SRC-0063, SRC-0055).

民主党在 2026 年需要净增席位才能舒适执政，最终取得 56 个参议院席位；参议院民主党领袖查克·舒默称
这"处于建立持久多数的有利位置"（SRC-0056）。阿拉斯加正是使这一算术成立的关键席位之一：特朗普
赢下的州里一个共和党席位，被一位前众议员翻转。全国报道把这场选举视为对"特朗普时代共和党品牌在
资源型州是否仍有效"的检验（SRC-0063、SRC-0055）。

## What else was on the ballot, and what it shows

The same election produced a Republican House win and a Democratic governor win:

- U.S. House: Nick Begich III (R) 136,215 (47.54%) vs. Bill Hill (independent) 119,689 (41.77%)
  (SRC-0001).
- Governor: Jonathan Kreiss-Tomkins led with 145,268 (51.07%) (SRC-0001); Alaska Beacon reported he
  "clinched" the election on 2026-11-13 while Republican opponents conceded (SRC-0042).

The comparison in `candidate_comparison.md` uses these to show Sullivan running behind his party's
House candidate and Peltola running far ahead of the House independent. Alaska split its tickets in
2026; that is the structural fact most national coverage missed.

同一场选举同时产生共和党众议员胜选与民主党州长胜选：众议院贝吉奇（共和党）136,215 票（47.54%）
对希尔（独立）119,689 票（41.77%）（SRC-0001）；州长选举克莱斯-汤姆金斯以 145,268 票（51.07%）
领先（SRC-0001），Alaska Beacon 于 2026-11-13 报道其"锁定"胜局、共和党对手承认败选（SRC-0042）。
`candidate_comparison.md` 据此说明沙利文低于本党众议员候选人、佩尔托拉远高于独立候选人。2026 年
阿拉斯加出现了分裂投票——这是全国报道最常忽略的结构性事实。

## Administration of the election under strain

Three controversies touched the count itself:

1. The state removed about 3,000 Alaskans from the voter rolls based in part on "old data"; the
   Legislature's legal adviser warned the delisting might violate federal law (SRC-0030, SRC-0031).
2. The Trump administration sued to block certification of the Senate result if Peltola won, arguing
   ballots cast for the namesake candidate should be segregated. A federal judge rejected the request
   on 2026-11-01; the case was on appeal (SRC-0038, SRC-0039, SRC-0052, SRC-0061).
3. Gov. Mike Dunleavy ordered a state investigation into Peltola's campaign over the namesake
   episode, and the FBI visited a Dan J. Sullivan donor in Petersburg (SRC-0056, SRC-0023).

None of these changed the count: the official summary reports 290,003 ballots cast and 287,896 valid
Senate votes, with all 401 precincts reporting (SRC-0001).

三项争议触及计票本身：其一，州政府依据部分"旧数据"将约 3,000 名阿拉斯加人移出选民名册，议会法律
顾问警告此举可能违反联邦法（SRC-0030、SRC-0031）；其二，特朗普政府起诉，要求在佩尔托拉胜选时
阻止认证参议院结果，并主张把投给同名候选人的选票分离；联邦法官于 2026-11-01 驳回，案件进入上诉
（SRC-0038、SRC-0039、SRC-0052、SRC-0061）；其三，州长迈克·邓利维就同名事件下令调查佩尔托拉
竞选团队，FBI 走访了彼得斯堡的一名小丹尼尔·沙利文捐款人（SRC-0056、SRC-0023）。这些均未改变
计票：官方汇总为投票 290,003 张、有效参议员票 287,896 张，401/401 个投票站报告完毕（SRC-0001）。

## Turnout and the shape of the electorate

Turnout was 47.90% of 605,433 registered voters. The summary does not break the electorate down by
party, district or age, and no exit poll was retrieved. What can be said from the count alone is that
Peltola's coalition was at least 144,302 strong, that it exceeded Sullivan's by 12,458, and that it
was large enough to make the second-choice machinery irrelevant.

投票率为 605,433 名登记选民中的 47.90%。汇总报告未按党派、选区或年龄细分，也未取得出口民调。
仅从计票可确认：佩尔托拉的联盟至少 144,302 人，比沙利文多 12,458 人，且大到足以让第二选择机制
失去意义。

## Why the race is comparative evidence

For cross-case comparison the Alaska 2026 race isolates four variables: an incumbent with a strong
national-security brand; a challenger with local issue ownership (fisheries) and a cost-of-living
message; a same-name ballot manipulation that failed; and a ranked-choice system that was never
triggered because the challenger won outright. Cases where ranked-choice tabulation *does* decide the
winner can be compared against this one to test whether the elimination round itself changes
coalition composition, since here it provably did not.

对跨案例比较而言，阿拉斯加 2026 年选举隔离出四个变量：具强国家安全品牌的现任议员；拥有地方议题
主导权（渔业）与生活成本信息的挑战者；失败的同名选票操纵；以及因挑战者直接过半而从未启动的排序
复选机制。可与"确由排序复选计票决定胜负"的案例对照，检验淘汰轮本身是否改变联盟构成——在本案例中
可以证明它没有。
