# -*- coding: utf-8 -*-
"""election_context.md, results_notes.md, candidate_comparison.md"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CASE, KEY

K = lambda k: KEY[k]


def put(rel, text):
    p = os.path.join(CASE, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(text)


FM = """---
title: %s
title_zh: %s
%scompiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: %s
coverage_note: %s
---

"""

put("07_electoral_context/election_context.md", FM % (
    "Electoral context — 2026 Iowa U.S. Senate race", "选举背景——2026 年艾奥瓦州联邦参议员选举", "",
    "complete",
    "Strong on the seat's structural change; thin on county-level turnout and on the governor's race coattails.")
    + """# Electoral context — 2026 Iowa U.S. Senate race / 选举背景

## 1. An open seat created in a single afternoon / 一个下午形成的空缺席位

English: On 2 September 2025 Sen. Joni Ernst released a video saying she would not seek a third term, citing a
wish to "give back" time to her family. Within hours, Rep. Ashley Hinson announced on WHO Radio's Simon Conway
show that she was running (`{f018}`), and the Democratic field — already five candidates deep, including Josh
Turek, who had launched on 12 August 2025 (`{f080}`) — was suddenly contesting a seat with no incumbent.

中文：2025 年 9 月 2 日，参议员 Joni Ernst 发布视频宣布不寻求第三任期，理由是希望把时间"还"给家庭。数小时内，众议员 Ashley Hinson 在 WHO 电台 Simon Conway 节目中宣布参选（`{f018}`）；民主党方面已有五名候选人（包括 2025 年 8 月 12 日启动的 Josh Turek，`{f080}`），一夜之间变成了无现任者的开放席位争夺。

## 2. Why the seat mattered nationally / 为何该席位具有全国意义

English: Iowa had not elected a Democrat to the Senate since 2008. Turek's win is recorded as one of eight
Democratic Senate flips in states Donald Trump carried in 2024, and the ABC News voter poll found that roughly
one in ten 2024 Trump voters backed him (`{f195}`). The result therefore belongs to a national pattern rather
than to a purely Iowa story — but the county table shows the pattern was uneven inside the state.

中文：艾奥瓦自 2008 年以来未再选出民主党参议员。Turek 的胜利被记录为民主党在 2024 年特朗普获胜州中翻盘的八个参议院席位之一，ABC 新闻选民调查显示约每十名 2024 年特朗普选民中就有一人支持他（`{f195}`）。因此这一结果属于全国性模式，而非纯粹的艾奥瓦故事——但县级数据表显示该模式在州内并不均匀。

## 3. The money asymmetry / 资金不对称

English: The FEC snapshots in `06_campaign_finance/campaign_finance.csv` show the Democratic nominee
out-raising the Republican by the final stretch: $24,290,521 to $14,147,973 as of 14 October 2026, with
$3,072,851 against $2,172,989 cash on hand. Outside money ran the other way in volume: the Des Moines Register
headline put total outside spending in the race at $137M, including a $20M Senate Leadership Fund buy for
Hinson (`{dmr_superpac}`, headline only). Those are separate 口径 and are never summed in this archive.

中文：`06_campaign_finance/campaign_finance.csv` 的 FEC 快照显示，进入最后阶段时民主党提名人筹款反超共和党人：截至 2026 年 10 月 14 日为 24,290,521 美元对 14,147,973 美元，手头现金 3,072,851 对 2,172,989。外部资金则相反：据《得梅因纪事报》标题，该场选举的外部支出总额为 1.37 亿美元，其中包含支持 Hinson 的 2000 万美元 Senate Leadership Fund 投放（`{dmr_superpac}`，仅标题）。两者口径不同，本档案从不相加。

## 4. Two primaries with different shapes / 两场形态不同的初选

English: The Republican primary was a landslide (Hinson 74.2% to Carlin's 25.8%) that nonetheless left a
visible wound: Carlin told supporters in June not to back Hinson (`{f149}`) before endorsing her in October
(`{f112}`). The Democratic primary was a two-candidate contest decided by roughly 25 points for Turek over
Zach Wahls, with the field collapsing to two names on the ballot. Republican primary turnout (206,255) was
higher than Democratic primary turnout (191,950) — a computed comparison from `election_results.csv`, not a
figure any source states.

中文：共和党初选是压倒性胜利（Hinson 74.2% 对 Carlin 25.8%），却留下可见的裂痕：Carlin 六月曾呼吁支持者不要支持 Hinson（`{f149}`），十月才转而背书（`{f112}`）。民主党初选是两人对决，Turek 以约 25 个百分点击败 Zach Wahls，最终选票上只剩两个名字。共和党初选投票数（206,255）高于民主党（191,950）——这是依据 `election_results.csv` 计算得出的比较，没有任何来源直接这样表述。

## 5. The disability first / 残疾的"第一次"

English: Turek is the first permanently physically disabled member of the Iowa Legislature, and — on the
record assembled here — the first Iowan using a wheelchair elected to the U.S. Senate. That is a documented
first, not a campaign slogan: the claim appears in coverage and in his own site biography (`{f200}`), and the
archive treats it as biography rather than as an argument about his politics.

中文：Turek 是艾奥瓦州议会首位永久性身体残疾的议员；按本档案汇集的材料，他也是艾奥瓦州首位使用轮椅当选联邦参议员的人。这是有据可查的"第一次"，不是竞选口号：该表述见于报道与其官网自述（`{f200}`），档案将其视作传记事实，而非对其政治的论证。

## 6. What the context does not explain / 背景无法解释的部分

English: The archive cannot attribute the result to any single factor. It records: an open seat, a national
 Democratic wave in Trump-carried states, a large Democratic money advantage late, a Republican primary that
never fully healed, and a candidate whose biography dominated his own communication. No source retrieved here
offers a decomposition, and none is invented.

中文：本档案不把结果归因于任何单一因素。它记录的是：开放席位、特朗普获胜州中的全国性民主党浪潮、后期民主党显著的资金优势、始终未完全愈合的共和党初选，以及一位以自身传记主导传播的候选人。已抓取来源均未提供因素分解，档案也不虚构分解。
""".format(f018=K("f018"), f080=K("f080"), f195=K("f195"), dmr_superpac=K("dmr_superpac"),
           f149=K("f149"), f112=K("f112"), f200=K("f200")))

put("07_electoral_context/results_notes.md", FM % (
    "Results notes — reconciliation and variance", "结果说明——核对与差异", "", "complete",
    "All arithmetic reconciled; two documented variance points (statewide total and primary percentages) are explained, not smoothed.")
    + """# Results notes — reconciliation and variance / 结果说明

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
numbers: 74% to 26% for Hinson (`{f112}`) and 62.6% to 37.4% for Turek with 99% of precincts counted
(`{f132}`). Both sets are recorded; the archive keeps the election-box versions in `election_results.csv` and
notes the night-of versions in `notes` on each row. Recomputation from the votes gives 74.21 / 25.79 and
62.66 / 37.34, which is why the rounded pairs differ by a tenth.

中文：共和党初选信息框为 74.2 / 25.8（153,059 / 53,196，合计 206,255），民主党为 62.7 / 37.3（120,287 / 71,663，合计 191,950）。当晚报道用的是略有不同的数字：Hinson 74% 对 26%（`{f112}`），Turek 在 99% 选区计票时为 62.6% 对 37.4%（`{f132}`）。两套数字均予记录：`election_results.csv` 采用信息框版本，并在每行 `notes` 注明当晚版本。按票数重算得 74.21 / 25.79 与 62.66 / 37.34，这正是四舍五入后相差零点一个百分点的原因。

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
""".format(f112=K("f112"), f132=K("f132")))

put("08_comparative_analysis/candidate_comparison.md", FM % (
    "Candidate comparison — Turek vs Hinson", "候选人比较——Turek 对 Hinson", "", "complete",
    "Biography, coalition, money, schedule, message and imagery compared; imagery is metadata-only because no image was inspected.")
    + """# Candidate comparison — Turek vs Hinson / 候选人比较

Each cell holds the English reading and its Chinese counterpart. Every figure is sourced in the dataset named
in the row; where a field is unknown it says so rather than averaging.

每个单元格同时给出英文与中文。数字均注明来源数据集；不明之处写 unknown，不用平均值填补。

## 1. Biography / 传记

| Dimension / 维度 | Turek / 图雷克 | Hinson / 辛森 |
|---|---|---|
| Entry into politics / 从政起点 | Wheelchair-basketball career, then mobility-equipment fitting, then a 2022 House race won by six votes after a recount / 轮椅篮球生涯→助行器适配工作→2022 年州众议院选举，重新计票后以 6 票胜出 | Broadcast journalist for more than a decade, then a 2016 Iowa House race, then Congress in 2020 / 十余年电视记者→2016 年州众议院→2020 年进入国会 |
| Firsts / "第一次" | First permanently physically disabled member of the Iowa Legislature / 艾奥瓦州议会首位永久性身体残疾议员 | Tied as first Republican woman to represent Iowa in the U.S. House / 与 Miller-Meeks 并列首位代表艾奥瓦州的共和党女性联邦众议员 |
| Public record / 公共履历 | Iowa House since 2023; Health and Human Services and oversight committees / 2023 年起州众议院，卫生与公众服务及监督委员会 | Iowa House 2017-2021 (chaired Judiciary, Public Safety, Transportation); U.S. House 2021-2027 / 州众议院 2017–2021（掌司法、公共安全、交通委员会）；联邦众议院 2021–2027 |
| Age on election day / 选举日年龄 | 47 / 47 岁 | 43 / 43 岁 |

## 2. Coalition / 选民联盟

| Dimension / 维度 | Turek | Hinson |
|---|---|---|
| Base / 基本盘 | Labor unions (UFCW, AFGE, Teamsters locals), disability and veterans' groups, county Democratic activists / 工会（UFCW、AFGE、卡车司机工会地方分会）、残疾与退伍军人团体、县党部活动人士 | Trump-aligned Republicans, commodity groups (Iowa Corn Growers PAC, Farm Bureau "Friend of Agriculture"), Border Patrol agents' union, Christian conservatives / 特朗普派共和党人、农产品团体（玉米种植者 PAC、农场局"农业之友"）、边境巡逻工会、基督教保守派 |
| Crossover claim / 跨党诉求 | Ads that borrow Republican themes on border security and gun rights (`{f082}`) and a promise to work with Trump on the border (`{f103}`) / 广告借用共和党式的边境与持枪权话语（`{f082}`），并承诺在边境问题上与特朗普合作（`{f103}`） | Affordability delivered through the OBBBA tips and overtime provisions, aimed at working-class voters (`{f106}`) / 以 OBBBA 小费与加班费条款主打生活成本，面向工薪阶层（`{f106}`） |
| Documented weakness / 已记录的弱点 | Missed Iowa House votes made into an attack line (`{f114}`) / 州众议院缺席投票被做成攻击话术（`{f114}`） | A primary rival who refused to endorse for four months (`{f149}`) / 初选对手四个月拒绝背书（`{f149}`） |

## 3. Money / 资金

| Dimension / 维度 | Turek | Hinson |
|---|---|---|
| Receipts to 2026-04-18 / 截至 4 月 18 日收入 | 2,808,701 | 7,267,266 |
| Receipts to 2026-10-14 / 截至 10 月 14 日收入 | 24,290,521 | 14,147,973 |
| Cash on hand 2026-10-14 / 10 月 14 日现金 | 3,072,851 | 2,172,989 |
| Outside support / 外部支持 | Not itemised in a retrievable source / 可查来源未逐项列出 | $20M Senate Leadership Fund buy; $137M total outside spending in the race, headline level (`{dmr_superpac}`) / 2000 万美元 SLF 投放；该场选举外部支出总额 1.37 亿美元（标题级，`{dmr_superpac}`） |

## 4. Schedule / 日程形态

| Dimension / 维度 | Turek | Hinson |
|---|---|---|
| Event count in archive / 档案内活动数 | 17 own + 2 joint / 本人 17 场 + 联合 2 场 | 14 own + 2 joint / 本人 14 场 + 联合 2 场 |
| Dominant format / 主要形式 | Speeches to defined audiences: seniors, county Democrats, students / 面向明确群体的演说：老年选民、县党部、学生 | Surrogate-led roundtables and fundraisers; four surrogate events / 代理人主导的圆桌与筹款会，共四场代理人活动 |
| Crowd figures documented / 有人数记录的活动 | 2 (Wing Ding 750+, Kennedy dinner n/a) / 2 场（Wing Ding 750+） | 2 (BBQ Bash 1,000+, Faith and Freedom 1,300+) / 2 场（烧烤会 1000+、信仰与自由 1300+） |

## 5. Message / 信息主轴

| Dimension / 维度 | Turek | Hinson |
|---|---|---|
| Master frame / 主框架 | "Prairie populism": the state has hit the bottom; fight for workers against billionaires / "草原民粹主义"：州已触底，为工人对抗亿万富翁 | Affordability already delivered plus a security guarantee / 已兑现的生活成本政策 + 安全保证 |
| Biography in the message / 传记在信息中的位置 | Central: the biography *is* the argument for public services / 核心：传记本身就是公共服务的论据 | Peripheral: biography appears as qualification, not as story / 边缘：传记作为资历，而非故事 |
| Trade / 贸易 | Tariffs as market destruction for farmers / 关税摧毁农民市场 | Tariffs as leverage against an unlevel playing field / 关税是对不公平竞争的杠杆 |
| Abortion / 堕胎 | Federal codification; Iowa's six-week ban as a services problem / 联邦立法；六周禁令是服务供给问题 | Opposition to a legal right, with rape, incest and life exceptions / 反对堕胎合法权利，强暴、乱伦与生命例外 |

## 6. Imagery / 影像

| Dimension / 维度 | Turek | Hinson |
|---|---|---|
| Downloadable official portraits / 可下载官方肖像 | None under the permitted licences; the four Legislature portraits are "Copyrighted free use" and therefore link-only / 无符合允许授权的肖像；四张州议会肖像为 "Copyrighted free use"，仅记录链接 | Three public-domain congressional portraits downloaded / 已下载三张公有领域国会肖像 |
| Only permitted photo of the candidate in office / 唯一允许的当选后照片 | A U.S. Senate group photograph dated 2026-11-09 whose caption names him / 2026 年 11 月 9 日的参议院合影，图注列名 | Not applicable / 不适用 |
| Reading / 解读 | INTERPRETATION: the licensing gap is also an imagery gap — his public visual identity is controlled by the state legislature, not by the campaign / 解读：授权缺口同时是影像缺口——他的公共视觉形象由州议会而非竞选团队掌握 | INTERPRETATION: her visual record is federal and public-domain by default, which is why the archive can show her and not him / 解读：她的影像记录属联邦、默认公有领域，因此档案能展示她而不能展示他 |

## 7. What the comparison does not settle / 比较未能解决的部分

English: The archive compares records, not virtues. It does not rank the candidates, score their performances,
or decide whether biography outperformed incumbency. The one asymmetry it establishes firmly is documentary:
Hinson has a public-domain visual record and Turek, in this archive, does not.

中文：本档案比较的是记录，而非优劣。它不为候选人排序、不评分，也不判定"传记"是否胜过"现任资历"。它确凿证明的唯一不对称是文献层面的：Hinson 拥有公有领域的影像记录，而 Turek 在本档案中没有。
""".format(f082=K("f082"), f103=K("f103"), f106=K("f106"), f114=K("f114"), f149=K("f149"),
           dmr_superpac=K("dmr_superpac")))
print("d9a done")
