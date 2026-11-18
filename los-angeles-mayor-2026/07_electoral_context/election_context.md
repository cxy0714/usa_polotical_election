---
title: "Election Context — 2026 Los Angeles Mayoral Election"
title_zh: "选举背景 — 2026 年洛杉矶市长选举"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: "Strong on the rules, calendar, field and polling trajectory; thin on turnout, district geography and the official canvass."
---

# Election context / 选举背景

## 1. The rules that shaped the race / 决定赛制的规则

Los Angeles elects its mayor in a **nonpartisan** contest: no party appears on the ballot, and if no
candidate wins a majority in the June primary the top two advance to a November runoff. In 2026 the
primary fell on **2026-06-02** and the runoff on **2026-11-03** [SRC-0001]. Because the office is
nonpartisan, this archive records `party = Nonpartisan` for every candidate and reconstructs ideology only
from endorsements, issue positions and coalition behaviour — never from a ballot label.

洛杉矶以**无党派**方式选举市长：选票上不列党派，若无人在 6 月初选获得多数，前两名进入 11 月决选。
2026 年初选为 **2026-06-02**，决选为 **2026-11-03** [SRC-0001]。由于该职位无党派，本档案对每位
候选人记 `party = Nonpartisan`，并只从背书、议题立场与联盟行为重建意识形态——绝不用选票标签。

The practical consequences are visible in the data. Fourteen candidates appeared on the primary ballot
[SRC-0021] [SRC-0002]; the top three took 88.8% of the vote between them, so the primary functioned as a
three-way contest with a long tail. The winner of the primary (Bass, 34.3%) did not win the runoff. The
$1,800 per-donor contribution cap for mayor [SRC-0034] pushed much of the race's money into independent
expenditure committees, which is why `campaign_finance.csv` needs a `report_type` column.

这些后果在数据中可见。初选选票上有十四位候选人 [SRC-0021] [SRC-0002]；前三名合计得票 88.8%，
故初选实质是三人之争加一条长尾。初选第一名（Bass，34.3%）并未赢得决选。市长选举单人捐款上限
1,800 美元 [SRC-0034] 把大量资金推向独立支出委员会，这正是 `campaign_finance.csv` 需要
`report_type` 列的原因。

## 2. The field / 候选人阵容

The field was set on the filing deadline of 2026-02-07, when Raman entered "on the last day"
[SRC-0013] [SRC-0039] and Austin Beutner withdrew after his daughter's death [SRC-0031]. Beyond the three
who mattered, the ballot carried ten candidates with published totals ranging from 30,008 (Adam Miller,
3.5%) down to 881 (Nelson Cheng, 0.1%) [SRC-0021]. Two write-in candidates were certified separately and
have no published totals [SRC-0002]. Pratt's 217,977 votes (25.5%) are the single most consequential
number in the primary: they are roughly twice the runoff's final margin.

阵容在 2026-02-07 提交截止日定型：Raman "在最后一天"入场 [SRC-0013] [SRC-0039]，Austin Beutner 在
女儿去世后退出 [SRC-0031]。除三位关键人物外，选票上还有十位候选人，公布票数从 30,008（Adam Miller，
3.5%）到 881（Nelson Cheng，0.1%）[SRC-0021]。另有两名补写候选人获单独认证，无公布票数 [SRC-0002]。
Pratt 的 217,977 票（25.5%）是初选中最重要的单一数字：约为决选最终差额的两倍。

## 3. The calendar that mattered / 关键时间节点

| Date | Event |
|---|---|
| 2024-07-01 | Bass files for reelection [SRC-0037] |
| 2025-01-07 | Palisades and Eaton fires begin — the incumbency's defining vulnerability |
| 2025-11-15 | First reported left challenge to Bass [SRC-0038] |
| 2025-12-13 | Bass launch rally [SRC-0023] |
| 2026-02-07 | Filing deadline; Raman enters, Beutner exits [SRC-0039] [SRC-0031] |
| 2026-05-05 / 05-06 | Two primary debates [SRC-0040] [SRC-0001] |
| 2026-05-13 | Final pre-primary forum canceled [SRC-0041] |
| 2026-06-02 | Primary: Bass 34.3%, Raman 29.0%, Pratt 25.5% [SRC-0021] |
| 2026-08-19 | First runoff debate [SRC-0032] |
| 2026-09-14 → 09-18 | Ad war opens: Raman's Emmy spot, Bass's ICE spot, LAPPL's attack [SRC-0044] |
| 2026-09-26 / 09-29 | South L.A. forum; Jewish Federation forum [SRC-0035] [SRC-0033] |
| 2026-10-13 | Final runoff debate [SRC-0062] |
| 2026-11-03 | Runoff: Raman 54.9%, Bass 45.1% [SRC-0001] |

## 4. The counting environment / 计票环境

California counts mail ballots incrementally and releases updates in daily batches, so election-night
leads are provisional for days. The Wikipedia account adds that this practice "triggered election
conspiracists, including President Donald Trump" in 2026 [SRC-0001] — a claim that rests on the
encyclopedia alone and is therefore `partially verified`; no wire story retrieved here covers it. This is
also why primary-night "Bass leads" reporting is recorded in `results_notes.md` as a count-order statement
rather than a result.

加州分批计票、按日公布更新，故选举夜的领先数日在数天内都是暂定的。维基百科的叙述补充说，这一做法
在 2026 年"引发电举阴谋论者，包括特朗普总统" [SRC-0001]——该说法仅依赖百科，故为
`partially verified`；本档案未取得任何通讯社报道涉及此事。这也是 `results_notes.md` 把初选夜
"Bass 领先"的报道记为计票顺序陈述而非结果的原因。

## 5. The polling trajectory / 民调轨迹

Eight reconcilable runoff polls are in `polling.csv`. Read as a sequence, they show the incumbent
starting ahead, the challenger taking a consistent mid-runoff lead, and the final poll returning to a tie:
Tulchin (August) Bass +6; Hart (Sept. 1–9) Raman +5; Berkeley IGS (Sept. 15–20) Raman +11; Manhattan
(Sept. 24–Oct. 1) Raman +3 leaned; FM3 and Impact (early October) Raman +2 and +10; McLaughlin (Oct. 15–18)
Raman +8; Berkeley IGS (Oct. 19–25) **tie at 40–40** with 19% undecided [SRC-0028] [SRC-0045] [SRC-0019]
[SRC-0020]. The final result (Raman +9.8) landed between the last two readings, which is a reminder that a
19% undecided share is not noise.

`polling.csv` 收录八项可对账的决选民调。按序阅读可见：现任者起步领先，挑战者在决选中段稳定领先，
最后一项民调回到平手：Tulchin（8 月）Bass +6；Hart（9/1–9）Raman +5；Berkeley IGS（9/15–20）
Raman +11；Manhattan（9/24–10/1）含倾向 Raman +3；FM3 与 Impact（10 月初）Raman +2 与 +10；
McLaughlin（10/15–18）Raman +8；Berkeley IGS（10/19–25）**40–40 平手**，19% 未决 [SRC-0028]
[SRC-0045] [SRC-0019] [SRC-0020]。最终结果（Raman +9.8）落在最后两次读数之间，提醒我们 19% 的
未决比例不是噪声。

## 6. The fabricated poll / 伪造民调

One widely circulated runoff poll showing Bass far ahead was retracted by the company that published it
[SRC-0047], and two outlets traced the operation behind it [SRC-0080] [SRC-0081]. The archive excludes it
from `polling.csv` and mentions it here because its existence is part of the election's information
environment: in the final month, a number that was never a measurement circulated as one.

一份广为流传、显示 Bass 大幅领先的决选民调被其发布公司撤回 [SRC-0047]，两家媒体追查了其背后的
操作 [SRC-0080] [SRC-0081]。档案将其排除在 `polling.csv` 之外，并在此提及，因为它的存在本身是这场
选举信息环境的一部分：在最后一个月，一个从未是测量的数字以测量的身份流通。

## 7. What overlaid the race / 叠加在选举之上的议题

Three exogenous frames ran through every retrieved source. The **January 2025 fires** and the slow
rebuild [SRC-0052] [SRC-0011]; **federal immigration enforcement**, which produced the runoff's most
contested advertisement [SRC-0044]; and the **2028 Olympics**, the deadline against which Raman set her
encampment target [SRC-0008] and against which Bass argued the city could not afford a change of
management [SRC-0062]. A fourth, quieter frame — a roughly $1 billion budget gap [SRC-0073] — supplied the
challenger's fiscal argument and the city controller's endorsement [SRC-0072].

三条外生框架贯穿所有已获取来源。**2025 年 1 月大火**与迟缓的重建 [SRC-0052] [SRC-0011]；
**联邦移民执法**，催生了决选中最具争议的广告 [SRC-0044]；以及 **2028 奥运会**——Raman 以它为营地
目标设定时限 [SRC-0008]，Bass 以它论证城市承受不起管理层更替 [SRC-0062]。第四条更安静的框架——
约 10 亿美元的预算缺口 [SRC-0073]——提供了挑战者的财政论点与市主计长的背书 [SRC-0072]。
