---
title: "Research Gaps — Case Study 001 (2026 Texas U.S. Senate)"
title_zh: "研究缺口 —— 案例研究 001（2026 年德州联邦参议员选举）"
language: en+zh
compiled_by: Lead Research Agent (merged from all five agents' staging gap registers)
last_updated: 2026-11-10
status: complete
coverage_note: >-
  Consolidated register of what this archive could NOT establish, plus the tool/access
  constraints that caused each gap. Intended to be read alongside the datasets so the human
  researcher knows exactly where the evidence stops. Nothing here is a guess.
---

# Research Gaps / 研究缺口

§14 of the brief requires an explicit register of what could not be located, what is
missing, what is uncertain and what conflicts. This file is that register, merged from
the Lead's own findings and the five agents' staging registers
(`_staging/A_gaps.md`, `B_gaps.md`, `D_gaps.md`, `E_gaps.md`; no `C_gaps.md` exists
because Agent C produced no output and the Lead completed the visual scope — see §7).

任务书第 14 项要求开列一份明确清单，说明哪些材料未能找到、哪些缺失、哪些不确定、哪些彼此冲突。本文件即该清单，由主导研究者的发现与五条代理线索的阶段登记合并而成（`_staging/A_gaps.md`、`B_gaps.md`、`D_gaps.md`、`E_gaps.md`；**不存在 `C_gaps.md`**，因为负责影像的代理 C 未产出任何结果，其范围由主导研究者接手完成——见第 7 节）。

**Nothing here should be read as claiming the campaign was not documented where this
file says "not retrieved."** The distinction is between *absent from the record* and
*absent from what our tools could reach*.

**本文件任何一处"未能检索到"都不等于"该竞选活动没有记录"。** 必须区分两种情形：*记录中本就不存在*，与*我们的检索工具无法触及*。

---

## 0. Validation status of the archive as delivered / 交付时的校验状态

All twelve datasets were checked programmatically (`_staging/_lead_validate.py`):
exact header match against `_research_conventions.md`, per-row field counts, no blank
cells, controlled-vocabulary conformance.

全部十二个数据集均已用脚本校验（`_staging/_lead_validate.py`）：表头与 `_research_conventions.md` 完全一致、逐行字段数正确、无空白单元格、受控词表取值合规。

```
[OK] campaign_events.csv 93 rows (TALARICO=49, PAXTON=44)
[OK] policy_positions.csv 146 rows (80/66)
[OK] speech_archive.csv 32 rows (18/14)
[OK] speech_video_index.csv 31 rows (18/13)
[OK] image_archive.csv 116 rows (18/98)
[OK] advertisements.csv 23 rows (14/9)
[OK] social_media.csv 12 rows
[OK] media_coverage.csv 66 rows (38/28)
[OK] campaign_finance.csv 69 rows (31/38)
[OK] election_results.csv 12 rows
[OK] county_results.csv 0 rows (header only — intentional / 有意留空)
[OK] polling.csv 11 rows
TOTAL hard failures: 0   soft warnings: 0
硬性失败 0 项；软性警告 0 项
```

Defects found and fixed during integration, recorded here for transparency:
`polling.csv` had 17 fields against a 16-field header (Lead's own file — rewritten);
`advertisements.csv` and `social_media.csv` carried an unheadered 20th/12th `notes`
field (contract amended to legalise the useful field, rows requoted);
`media_coverage.csv` used `coverage_type=news_video` outside the vocabulary (vocabulary
extended); `social_media.csv` had three rows with unquoted commas in `notes` (repaired);
one Wikimedia file was a **different Ken Paxton** ("Lawton, OK", 1986) and was removed
(`PAX-IMG-0801` retired — do not reuse).

整合过程中发现并修复的缺陷，一并记录以保持透明：`polling.csv` 出现 17 个字段而表头只有 16 个（属主导研究者自己的文件——已重写）；`advertisements.csv` 与 `social_media.csv` 带有未列入表头的第 20／12 个 `notes` 字段（通过修订契约将该有用字段合法化，并重写引号）；`media_coverage.csv` 使用了词表外的 `coverage_type=news_video`（已扩展词表）；`social_media.csv` 有三行因 `notes` 内逗号未加引号而错位（已修复）；维基共享资源中有一个文件是**另一位同名肯·帕克斯顿**（"Lawton, OK"，1986 年），已移除（`PAX-IMG-0801` 编号作废——不得复用）。

---

## 1. Tool and access constraints that shaped the whole archive / 影响整体档案的工具与访问限制

| Constraint / 限制 | Effect / 后果 | Examples / 例证 |
|---|---|---|
| `web_fetch` returns only the head of many JS-rendered pages / 对许多 JS 渲染页面只能取到开头 | Article bodies unreachable; only headline/snippet facts recorded / 正文不可达，只能记录标题与摘要级事实 | Texas Tribune, NYT, WSJ, NBC results, Houston Public Media |
| HTTP 403 / bot-blocking / 403 与反爬拦截 | Whole sources unavailable / 整条来源不可用 | Axios, `docquery.fec.gov` filing PDFs, ABC27/Sinclair, one Hill article, AFP Fact Check, RealClearPolitics, Newsweek print, Fox News print (404) |
| HTTP 402 / paywalls / 402 与付费墙 | Body text unreachable; snippets only / 正文不可达，仅有摘要 | NYT, Washington Post, WSJ, El Paso Times (one article) |
| JavaScript-only election dashboards / 纯 JS 选举看板 | County/precinct results not extractable at all / 县级与选区结果完全无法提取 | Texas Tribune, NBC, Houston Public Media, Boston Globe, Houston Chronicle interactives |
| No video playback or transcription / 无视频播放与转写能力 | Full-length transcripts impossible; quotations rest on printed reporting / 无法生成完整文字稿，引语只能依赖文字报道 | All candidate video; only one genuine transcript exists (MS NOW, AI-generated) / 全部候选人视频；仅有一份真实文字稿（MS NOW，AI 生成） |
| No image input to the analyst model / 分析模型无图像输入 | Photographs could not be visually inspected by the research agent / 研究代理无法目视检查照片 | All 116 archive rows — see §7 / 全部 116 行，见第 7 节 |
| No CV library (cv2/mediapipe/dlib absent) / 无计算机视觉库 | Facial-landmark and body-proportion measurement not executable / 面部关键点与身体比例测量无法执行 | see §7 / 见第 7 节 |
| Translation-only sources / 仅二手翻译来源 | Quotations are translations of translations / 引语是"译文的译文" | Crusoé (Brazilian outlet) |
| Wikimedia API rate limiting (HTTP 429) / 维基接口限速 | Required throttled, batched requests to build the image archive / 须限速批量请求才能建成影像档案 | Commons enumeration |

---

## 2. Election results and electoral data / 选举结果与选举数据

1. **County-level results — `county_results.csv` is intentionally EMPTY (header only).**
   County and precinct tabulation was published through JavaScript-rendered
   interactives that the retrieval tool could not execute. The Wikipedia race article
   contains only county *maps* (SVG), not a county table. This remains the single
   largest data gap in the archive. A researcher with a browser, or the Texas
   Secretary of State county canvass returns, can close it directly.

   **县级结果——`county_results.csv` 有意为空（仅表头）。** 县与选区级统计通过 JavaScript 渲染的交互页面发布，检索工具无法执行脚本；维基百科条目只有县级*地图*（SVG），没有县级数据表。这是本档案**最大的单项数据缺口**。有浏览器的研究者，或德州州务卿的县级选举认证回报，可直接补齐。
2. **Certified totals — partially closed.** Final figures were obtained from the
   certified-result aggregate in the Wikipedia race article via its raw wikitext:
   **Talarico 5,447,069 (55.06%), Paxton 4,250,664 (42.97%)**. These are recorded in
   `election_results.csv` as `partially verified` because the aggregator, not the
   official canvass, is the source. **The Texas Secretary of State canvass has still
   not been read directly.**

   **认证总票数——部分补齐。** 最终数字取自维基百科该选举条目的认证结果汇总（经原始 wikitext 抓取）：**塔拉里科 5,447,069 票（55.06%）、帕克斯顿 4,250,664 票（42.97%）**。因来源是汇总方而非官方认证，`election_results.csv` 将其标为 `partially verified`（部分核实）。**德州州务卿的官方认证仍未直接读取。**
3. **Certification status.** Whether the state canvass had been certified as of
   2026-11-10 is unknown. The statutory procedure is documented
   ([SOS canvassing guidance](https://www.sos.texas.gov/elections/forms/canvassing-and-post-election-procedures-10-19-23.pdf))
   but no 2026 certification record was retrieved.

   **认证状态。** 截至 2026-11-10 州级认证是否完成，未能查明。法定程序有据可查（[州务卿认证指引](https://www.sos.texas.gov/elections/forms/canvassing-and-post-election-procedures-10-19-23.pdf)），但未检索到 2026 年的认证记录。
4. **Minor-party / independent candidates.** Not established. The two major-party
   percentages sum to 98.03%, implying ~2% went elsewhere or was undervoted, but this
   was not verified; `election_results.csv` carries an explicit `unverified` row.

   **小党与独立候选人。** 未能确立。两大党得票率合计 98.03%，意味着约 2% 流向其他候选人或为废票，但未核实；`election_results.csv` 中有一条明确的 `unverified`（未核实）行。
5. **Daily early-vote returns.** Early voting began 2026-10-19 and "more than 7.7
   million" Texans voted early, but no daily county-level series was retrieved.

   **提前投票逐日数据。** 提前投票于 2026-10-19 开始，"超过 770 万"德州人提前投票，但未检索到县级逐日序列数据。
6. **Democratic primary — final figure now known, earlier reporting differed.** Final
   Talarico share **52.4%** (certified-result aggregate); an earlier count at 91%
   reporting had 53%. Crockett's 45.7% is from that same partial count and does not
   exactly complement 52.4%; treated as approximate.

   **民主党初选——最终数字已确立，早期报道不同。** 塔拉里科最终得票率 **52.4%**（认证结果汇总）；此前计票 91% 时的报道为 53%。克罗克特的 45.7% 来自同一次部分计票，与 52.4% 并非严格互补；按近似值处理。
7. **GOP primary margin conflict — UNRESOLVED.** News From The States (AP, 93% counted)
   reported Cornyn 41.9% / Paxton 40.8% (1.1-point lead). NY Post reported Cornyn
   "topped Paxton by 2.5 percentage points." Both recorded; certified margin unknown.
   Note the aggregate polling going into the primary had *Paxton* ahead by 3.5–6 points,
   so the first-round ordering was itself a polling miss.

   **共和党初选差距冲突——未解决。** News From The States（美联社，计票 93%）报道科宁 41.9%、帕克斯顿 40.8%（领先 1.1 个百分点）。《纽约邮报》称科宁"以 2.5 个百分点领先帕克斯顿"（译）。两者均予记录；认证差距未查明。值得注意的是，初选前的汇总民调显示*帕克斯顿*领先 3.5–6 个百分点，因此首轮排序本身就是一次民调失准。
8. **Runoff — final figure now known.** **63.8%, a margin of more than 25 points**
   (certified-result aggregate), replacing the morning-after projection of "exceeding
   60 percent." Vote totals were not retrieved.

   **决选——最终数字已确立。** **63.8%，领先超过 25 个百分点**（认证结果汇总），取代了选后次日"超过 60%"的预测。得票总数未检索到。
9. **"Drought" framing conflicts.** "First Democratic Senate win since **1988**"
   (Lloyd Bentsen; BBC/AP/NYT), "first statewide win since **1994**" (San Angelo LIVE),
   and "three-decade drought" (NYT headline) all appear. The likeliest reconciliation is
   *Senate seat* vs *any statewide office*, but it is not confirmed. Do not use one
   figure without stating which baseline.

   **"干旱期"表述冲突。** "自 **1988** 年以来首位民主党参议员胜选"（劳埃德·本特森；BBC／美联社／《纽约时报》）、"自 **1994** 年以来首次全州性胜利"（San Angelo LIVE）、"三十年空白"（《纽约时报》标题）三种说法并存。最可能的调和是*参议院席位*与*任何全州公职*之别，但未获确认。引用任一数字时必须说明基线口径。

---

## 3. Campaign events / 竞选活动

10. **Tour stop completeness — improved but still short.** Paxton's "Come and Take It"
    tour was announced as 18 days / 30+ stops; **15 of 19 named cities remain
    schedule-only with no date** because stops were posted to Eventbrite and then
    removed. Talarico's "Clear Eyes, Full Hearts" tour is documented at **12 held stops
    with evidence** out of 20 announced cities, plus 11 schedule-only items (Fort Bend,
    Galveston, San Antonio, Weslaco etc. have no date at all). **Closure route:** the
    campaigns' Eventbrite pages and local outlets.

    **巡回站点完整性——有改善但仍不完整。** 帕克斯顿的 "Come and Take It" 巡回宣传宣布为 18 天／30 余站；**19 个具名城市中有 15 个仅有日程安排而无日期**，因为站点信息曾发布在 Eventbrite 上随后被撤下。塔拉里科的 "Clear Eyes, Full Hearts" 巡回宣传在 20 个宣布城市中有 **12 站有证据证明实际举行**，另有 11 条仅有日程记录（Fort Bend、Galveston、San Antonio、Weslaco 等完全没有日期）。**补齐路径：** 两阵营的 Eventbrite 页面与地方媒体。
11. **No candidate-vs-candidate debate occurred.** There is no debate transcript, no
    joint stage, no head-to-head video. The archive documents the *absence* and its
    negotiation chronology (five `debate_invitation` rows). The CNN–Jubilee event was a
    **solo voter Q&A**, not a debate — several outlets mislabelled it.

    **未发生任何候选人对候选人的辩论。** 没有辩论文字稿、没有同台、没有一对一视频。本档案记录的是这一*缺席*及其协商过程（五条 `debate_invitation` 记录）。CNN–Jubilee 那场活动是**单人**选民问答，并非辩论——多家媒体误标。
12. **"Three debates scheduled" is FALSE and is preserved only as a caution.** Washington
    Examiner (2026-09-02) reported debates scheduled for Sept 22 / Oct 6 / Oct 13; none
    happened. Do not place them in any event table (`_staging/E_gaps.md` §7).

    **"三场已排定辩论"为不实信息，仅作为警示保留。** 《华盛顿观察家报》（2026-09-02）报道辩论排定于 9 月 22 日、10 月 6 日、10 月 13 日；三场均未发生。不得将其写入任何事件表（`_staging/E_gaps.md` 第 7 节）。
13. **Talarico's two-week absence** from the trail (early October, reported as flu) is
    documented by NYT/NY Post/CNN but the exact start and end dates are not pinned. No
    events were invented for that period — it is logged as an activity gap.

    **塔拉里科约两周的活动空窗**（10 月初，报道称为流感）由《纽约时报》《纽约邮报》与 CNN 记载，但确切起止日期未能锁定。该期间没有编造任何事件——只作为"活动缺口"记录。
14. **Trump "virtual vs in-person" conflict — effectively resolved against "virtual."**
    Four in-person Texas trips with Paxton present are documented (Dallas September;
    Denton 2026-10-01; San Antonio 2026-10-07; Corpus Christi + Lubbock 2026-10-27). One
    announced leg — a **Waco 18:00 rally on 10-27** — is logged `disputed`: announced,
    execution unconfirmed.

    **特朗普"线上还是线下"之争——实际已否证"仅线上"说法。** 有据可查的四次亲赴德州行程均有帕克斯顿在场（9 月达拉斯；2026-10-01 丹顿；2026-10-07 圣安东尼奥；2026-10-27 科珀斯克里斯蒂与拉伯克）。其中一段宣布的行程——**10-27 韦科 18:00 集会**——记为 `disputed`（存疑）：已宣布，执行未证实。
15. **Announcement vs occurrence.** Several announced events could not be confirmed as
    having taken place; marked `announced` or `partially verified`, never `held`.

    **宣布与举行之别。** 若干已宣布活动无法证实确实举行；标为 `announced`（已宣布）或 `partially verified`（部分核实），绝不标为 `held`（已举行）。
16. **Nacogdoches ~2026-05-27 rally attribution is ambiguous** — a KWTX preview headline
    concerns Talarico, so no row was created.

    **纳科多奇斯 2026-05-27 前后的集会归属不明**——KWTX 的预告标题指向塔拉里科，因此未建行。
17. **Midland vs Lubbock same-night sequencing is ambiguous.** KOSA says Amarillo and
    Lubbock were "still to come" while the Lubbock A-J reports Lubbock "Tuesday night";
    the Midland row is flagged `conflicting sources` and may be 10-26 rather than 10-27.

    **米德兰与拉伯克同夜先后顺序不明。** KOSA 称阿马里洛与拉伯克"尚待前往"，而《拉伯克阿瓦兰奇报》称拉伯克为"周二晚"；米德兰一行标为 `conflicting sources`（来源冲突），日期可能是 10-26 而非 10-27。
18. **Categories that are empty for BOTH campaigns** despite targeted search: HQ
    openings, closed-door fundraisers, labour events, county-party meetings, podcasts,
    press conferences, election-day GOTV events. These are gaps in the public record,
    not evidence the activities did not occur.

    **双方均为空白的类别**（尽管做过定向检索）：竞选总部开幕、闭门筹款会、劳工活动、县党部会议、播客、记者会、选举日催票活动。这些是公开记录中的缺口，不能当作"活动未发生"的证据。
19. **April 2026 has no dated campaign event for either candidate** — a shared gap.

    **2026 年 4 月双方都没有带日期的竞选活动**——这是共同的缺口。

---

## 4. Campaign organization / 竞选组织

20. **Paxton's campaign manager is unidentified.** Senior advisor Nick Maddux is
    documented; the manager is not. Full staffing: `08_comparative_analysis/campaign_organization.md`.

    **帕克斯顿的竞选经理身份未明。** 高级顾问 Nick Maddux 有据可查，竞选经理则没有。完整人事见 `08_comparative_analysis/campaign_organization.md`。
21. **Campaign headquarters** for both candidates — unknown.

    **双方竞选总部地址**——未查明。
22. **Full staff rosters, field-organisation structure, pollsters, media consultants** —
    not established for either campaign.

    **完整人员名册、地面组织架构、民调机构、媒体顾问**——双方均未确立。
23. **FEC filing PDFs unreachable** (`docquery.fec.gov` 403). Committee IDs and
    registration dates ARE verified (Talarico C00919084 / 2025-09-09; Paxton C00901918 /
    2025-04-08), but line-item detail rests on the FEC summary tables and reporting, not
    the filings themselves.

    **FEC 申报 PDF 无法访问**（`docquery.fec.gov` 返回 403）。委员会编号与注册日期**已核实**（塔拉里科 C00919084／2025-09-09；帕克斯顿 C00901918／2025-04-08），但逐条明细只能依据 FEC 汇总表与新闻报道，而非申报原件。
24. **Axios report on Paxton's primary consultants (2025-04-08) blocked (403)** — its
    existence is known, the names are not.

    **Axios 关于帕克斯顿初选顾问的报道（2025-04-08）被拦截（403）**——知其存在，不知其名单。

---

## 5. Money — the discrepancies that must never be silently merged / 资金：绝不可悄然合并的口径差异

25. **Four different Talarico "totals" exist and are not the same quantity:**
    campaign announcement **$134.3m** cumulative; FEC **contributions $140,307,408**;
    FEC **total receipts $146,349,912**; Texas Tribune figure **~$155m** including joint
    fundraising committees. All four are in `campaign_finance.csv` as separate rows.

    **塔拉里科存在四种不同的"总额"，并非同一计量对象：** 阵营宣布的累计 **1.343 亿美元**；FEC **捐款 140,307,408 美元**；FEC **总收入 146,349,912 美元**；《德州论坛报》所载含联合筹款委员会的 **约 1.55 亿美元**。四者在 `campaign_finance.csv` 中分列为不同行。
26. **Paxton Q2/Q3 confusion.** Campaign figure **$18m** for Q3 (principal + two JFCs)
    vs principal committee **$10,249,117**; Q2 ≈ **$9m**. One outlet (El Paso Times)
    mislabels the $18m as second-quarter money; KWTX/Tribune is unambiguous that it is
    Q3 and doubled Q2. Row flagged `conflicting sources`.

    **帕克斯顿第二／第三季度口径混淆。** 阵营口径第三季度 **1,800 万美元**（主委员会加两个联合筹款委员会），主委员会为 **10,249,117 美元**；第二季度约 **900 万美元**。一家媒体（《埃尔帕索时报》）把 1,800 万误作第二季度；KWTX／《德州论坛报》明确其为第三季度且为第二季度的两倍。该行标为 `conflicting sources`。
27. **THE BIGGEST TRAP — FEC Schedule E vs AdImpact are roughly an order of magnitude
    apart.** Example: "Texans for a Conservative Majority" shows **$24.96m** in FEC
    independent expenditures opposing Paxton, while Texas PAC shows **$182.1m** in
    AdImpact ad spend. These are different measurement constructs, kept in separate,
    differently typed rows. **Never sum them.**

    **最大的陷阱——FEC Schedule E 与 AdImpact 相差约一个数量级。** 例："Texans for a Conservative Majority" 的 FEC 独立支出为 **2,496 万美元**（反对帕克斯顿），而 Texas PAC 的 AdImpact 广告投放为 **1.821 亿美元**。二者是不同的计量构造，已分列于类型不同的行中。**绝不可相加。**
28. **Outside-spending totals do not reconcile.** "Over $214 million" by national
    Republican actors (AdImpact via Texas Tribune, 2026-10-14); Musk-related giving
    traced via FEC at **$158m** ($75m on 2026-09-09 + $83m), but claimed at "nearly
    $190m" / ">$190m" / ">$200m" (Talarico) / ~$150m (translated outlet). Attributed
    claims only; no reconciled total exists.

    **外部支出总额无法对账。** 全国性共和党力量投放"超过 2.14 亿美元"（AdImpact，经《德州论坛报》，2026-10-14）；与马斯克相关的政治捐款按 FEC 追溯为 **1.58 亿美元**（2026-09-09 的 7,500 万＋8,300 万），但各方宣称"近 1.9 亿""超过 1.9 亿""超过 2 亿"（塔拉里科）或约 1.5 亿（一家译文媒体）。仅作带归属的宣称记录；不存在经对账的总额。
29. **AdImpact totals are not filings.** The $573.2m race ad-spend total and the
    $81m/$8m/$3.5m Talarico-side air-war figures are tracking estimates or campaign
    claims.

    **AdImpact 总额不是申报数据。** 5.732 亿美元的竞选广告总额，以及塔拉里科一方 8,100 万／800 万／350 万美元的空中战数字，均为监测估算或阵营宣称。
30. **PAC contribution conflicts.** Talarico: $518,805 vs $518,000 vs $468,806.
    Paxton: $435,150 vs $702,000. Scope and date differences unexplained.

    **PAC 捐款数字冲突。** 塔拉里科：518,805／518,000／468,806 美元三种；帕克斯顿：435,150／702,000 美元两种。统计范围与日期差异未获解释。
31. **Post-general FEC reports unavailable** at time of research; last verified balances
    are **2026-10-14** for both committees. Both reported **$0 debt**.

    **选后 FEC 报告在检索时不可得**；两个委员会最后经核实的余额截止 **2026-10-14**。双方均申报**零负债**。
32. **OpenFEC DEMO_KEY rate limit** (40 calls/hour) prevented splitting primary vs
    general independent expenditures by date; `FIN-EXT` rows are cycle-wide.

    **OpenFEC 的 DEMO_KEY 限速**（每小时 40 次调用）使独立支出无法按日期拆分初选与大选阶段；`FIN-EXT` 各行覆盖整个选举周期。

---

## 6. Media and quotations / 媒体与引语

33. **Paywalled primary reporting** (NYT, WaPo, WSJ, Politico, Dallas Morning News)
    contributed headline-level facts only.

    **付费墙后的核心报道**（《纽约时报》《华盛顿邮报》《华尔街日报》Politico、《达拉斯晨报》）仅贡献标题级事实。
34. **Verbatim quotation limits.** Every quotation in this archive comes from printed
    text. **Nothing was verified against audio or video**, so all prosody fields (pace,
    pitch, pauses, emphasis) are `unknown` across both communication analyses.

    **引语逐字性问题。** 本档案中每一句引语都来自文字文本。**没有任何内容与音频或视频核对过**，因此两篇传播分析中的全部韵律字段（语速、音高、停顿、重音）均为 `unknown`（未查明）。
35. **Timestamps** for speech quotations are largely unavailable; `speech_archive.csv`
    uses `unknown` on many rows rather than inventing timecodes.

    **时间戳**大多不可得；`speech_archive.csv` 在多数行使用 `unknown`，而非编造时间码。
36. **Axios vs Al Jazeera wording differs** in the victory-speech sentence about
    "trillionaire megadonors / corrupt defenders." Quote the outlet you cite; do not
    harmonise them.

    **Axios 与半岛电视台在胜选演说中"万亿富翁金主／腐败辩护者"一句的措辞不同。** 引用哪家就照哪家引，不要擅自统一。
37. **Reuters is absent from the media corpus** — no retrievable Reuters item; recorded
    as a gap, not fabricated.

    **媒体语料中缺少路透社**——未检索到任何可获取的路透社条目；记为缺口，不作虚构。
38. **Leaked Paxton audio (2026-09-24)** is headline-level only; verbatim quotes not
    verified (Independent 403, Newsweek 403, Fox print URL 404).

    **帕克斯顿泄露录音（2026-09-24）**仅有标题级信息；逐字引语未核实（Independent 403、Newsweek 403、Fox 文字版链接 404）。
39. **AFP Fact Check** piece on a "temporary data-entry error" returned 403; findings
    not incorporated.

    **法新社事实核查**关于"临时数据录入错误"的文章返回 403；其结论未纳入。
40. **TIME/Colbert attribution** (~9 million YouTube views, $2.5m in 24 hours, 4,000
    volunteers) is carried via the TIME text retrieved through a mirror, attributed to
    TIME. Treat as a campaign-favourable claim reported by TIME, not as an FEC-verified
    number.

    **《时代》周刊／科尔伯特环节的数字**（YouTube 约 900 万次观看、24 小时内 250 万美元、4,000 名志愿者）经由镜像取得《时代》原文后转录，并注明出自《时代》。应视为《时代》报道的、对阵营有利的宣称，而非 FEC 核实的数字。
41. **CNN/Jubilee faith exchange** quotations were relayed via a partisan outlet
    (Hannity.com) and cross-confirmed by CNN's live post; re-check against CNN video
    before print.

    **CNN／Jubilee 的信仰话题往来**引语经一家党派媒体（Hannity.com）转述，并由 CNN 实时贴文交叉印证；正式刊发前建议对照 CNN 视频复核。
42. **Warm-up speaker ≠ candidate.** Bob Hall's "Freako Talarico" line is a warm-up
    speaker's, not Paxton's (flagged in `D_gaps.md`).

    **暖场发言者不等于候选人本人。** Bob Hall 的 "Freako Talarico" 一语出自暖场发言者，不是帕克斯顿本人（已在 `D_gaps.md` 标注）。

---

## 7. Images and visual record — rewritten after the visual scope was taken over / 影像与视觉记录（接手后重写）

**What happened.** Agent C produced no deliverable after ~75 minutes and was
interrupted; the Lead built the visual archive directly from the Wikimedia Commons API
(throttled, batched `imageinfo` calls) plus verified news-photo credit lines.
`_staging/C_sources.csv` and `C_gaps.md` therefore do not exist; this section replaces
them.

**经过。** 负责影像的代理 C 在约 75 分钟内未产出任何交付物，被中断；主导研究者直接通过维基共享资源 API（限速、批量 `imageinfo` 请求）并辅以已核实的新闻照片署名信息，重建了影像档案。因此 `_staging/C_sources.csv` 与 `C_gaps.md` 均不存在；本节取代其位置。

43. **The 60–100 photograph target per candidate was NOT met for Talarico — and this is
    a documented evidence limit, not padding.** `image_archive.csv` holds **18 Talarico
    rows** (7 CC-licensed copies, 2 public-domain, 9 all-rights-reserved link-only
    records) against **98 Paxton rows** (91 CC-licensed copies, 1 public-domain, 6
    link-only). Commons holds only 14 files in `Category:James Talarico` and its year
    subcategories, 9 of them usable photographs of him. His news photography is
    overwhelmingly agency-licensed (AP/Getty/AFP) and therefore link-only under a
    copyright-clean policy.

    **塔拉里科未达到每位候选人 60–100 张照片的目标——这是有据可查的证据限制，不是注水。** `image_archive.csv` 中塔拉里科 **18 行**（7 张知识共享许可副本、2 张公有领域、9 条保留所有权利的仅链接记录），帕克斯顿 **98 行**（91 张许可副本、1 张公有领域、6 条仅链接）。维基共享资源 `Category:James Talarico` 及其年份子分类仅收录 14 个文件，其中 9 个是他的可用照片。他的新闻摄影绝大多数为通讯社授权（美联社／盖蒂／法新社），在"版权干净"原则下只能记录链接。
44. **The Paxton pool is context-skewed.** **68 of 98** Paxton rows are photographs from
    **AmericaFest** (Turning Point USA, Phoenix, 2024/2025 editions), mostly by Gage
    Skidmore under CC BY-SA 4.0; 3 more are from a Goldwater Institute dinner. Only 5
    rows join a 2026 campaign event and only 5 fall in 2026 at all. The pool depicts him
    as a **conference speaker**, not as a touring Senate candidate.

    **帕克斯顿的图库情境严重偏斜。** **98 行中有 68 行**是 **AmericaFest**（Turning Point USA，凤凰城，2024／2025 年届）的照片，多由 Gage Skidmore 以 CC BY-SA 4.0 拍摄；另有 3 行来自戈德华特研究所晚宴。仅 5 行对应 2026 年竞选活动，仅 5 行落在 2026 年。该图库呈现的是**会议演讲者**，而非巡回竞选的参议员候选人。
45. **Volume asymmetry is not evidence of visual effort.** Comparing the two archives
    would confound *venue* with *candidate*. Any comparative image use must state both
    the volume (18 vs 98) and the skew (68/98 from one conference) alongside the
    images.

    **数量差异不能当作"视觉投入"的证据。** 直接比较两个档案会把*场地*与*候选人*混为一谈。任何对比性使用影像的场合，必须同时说明数量（18 对 98）与偏斜（98 张中 68 张出自同一会议）。
46. **Facial geometry and body proportions were NOT measured.** The Python environment
    has Pillow and NumPy but **no** `cv2`, `mediapipe`, `dlib` or `face_recognition`, and
    the analyst model in this session **cannot accept image input**. No photograph was
    visually inspected by the research agent. Both `visual_analysis_*.md` files state
    this plainly and supply a full landmark/ratio protocol (fWHR, facial index,
    intercanthal ratio, facial thirds, head-height fraction, shoulder-to-head) for the
    human researcher, with lens/lighting/crop caveats.

    **面部几何与身体比例均未测量。** Python 环境有 Pillow 与 NumPy，但**没有** `cv2`、`mediapipe`、`dlib` 或 `face_recognition`；本次会话的分析模型**无法接收图像输入**。研究代理没有目视检查过任何照片。两篇 `visual_analysis_*.md` 均如实说明这一点，并为人类研究者提供完整的标志点／比例测量规程（面部宽高比 fWHR、面部指数、内眦间距比、面部三等分、头高占比、肩宽对头高），同时说明镜头、光照与裁切的干扰。
47. **Clothing and grooming: zero documentary basis.** No retrieved source describes
    either candidate's attire at any event; `campaign_events.csv` has a clothing
    description for **zero** rows of either candidate; `clothing_notes` is `unknown` in
    all 116 image rows. Any claim that a candidate "dressed like a teacher" or "wore
    boots" is unsupported by this archive.

    **着装与仪容：无文献依据。** 没有任何检索到的来源描述过两位候选人在任何活动上的衣着；`campaign_events.csv` 中双方**均无一行**有着装描述；全部 116 行影像的 `clothing_notes` 均为 `unknown`。任何"候选人穿得像老师"或"穿靴子"的说法，在本档案中都没有依据。
48. **What IS measurable was measured.** Frame statistics (dimensions, aspect ratio,
    orientation, Laplacian-variance sharpness, mean luma, contrast, saturation proxy) for
    69 locally held copies are in `_staging/_visual_metrics.csv`; resolution classes are
    computed from original Commons metadata, with the measurement basis (800px
    derivative) stated per row.

    **可以测量的部分已经测量。** 69 张本地副本的画幅统计（尺寸、宽高比、方向、拉普拉斯方差清晰度、平均亮度、对比度、饱和度近似值）见 `_staging/_visual_metrics.csv`；分辨率分级依据共享资源原始元数据计算，每行均注明测量基准（800 像素衍生图）。
49. **Official portrait provenance is uneven** — several "official" images are re-hosted
    by third parties; the authoritative source was not established for either candidate.

    **官方肖像的来源链不整齐**——若干"官方"影像由第三方转托管；双方均未确立权威来源。
50. **One wrong-subject file was caught.** `File:KPaxton.png` describes "Ken Paxton of
    Lawton, OK" (1986), a different person; removed, id `PAX-IMG-0801` retired.

    **已发现并处理一个主体错误的文件。** `File:KPaxton.png` 描述的是"俄克拉何马州劳顿市的肯·帕克斯顿"（1986 年），是另一个人；已移除，`PAX-IMG-0801` 编号作废。
51. **No campaign-supplied photo library was retrieved** for either campaign
    (jamestalarico.com / kenpaxton.com galleries). Paxton's site served site-builder JSON
    (Agent B hit the same wall for issue pages).

    **未取到任何阵营自建的图库**（jamestalarico.com／kenpaxton.com 的图片页）。帕克斯顿的网站返回建站工具 JSON（代理 B 在议题页上也遇到同一障碍）。
52. **Perceptual-hash de-duplication applies to the catalogue, not to downloaded files.**
    Several Commons files are crops/variants of the same underlying photograph (e.g. a
    "centered", a "cropped" and a "3x4 cropped" version of one press conference); this
    is recorded in filenames but not merged into single rows.

    **去重只在目录层面，不在下载文件层面。** 若干共享资源文件是同一张底片的裁切／变体（如某场记者会的"居中版""裁切版""3:4 裁切版"）；这一点记录在文件名中，但未合并为单一行。

---

## 8. Policy and biography source asymmetry / 政策与传记的来源不对称

53. **Paxton's own campaign issue literature does not exist in retrievable form.** His
    site returned site-builder JSON, so all 66 policy rows are documented through the
    attorney-general record and press reporting, not his campaign's own pages. **The
    thinner row counts (Gun, Healthcare, Labor, Religion) reflect source availability,
    not issue emphasis.** `_staging/B_gaps.md` §5 records this; the dataset was not padded.

    **帕克斯顿竞选团队的议题文献不存在可获取形态。** 他的网站返回建站工具 JSON，因此全部 66 条政策记录均通过州检察长履职记录与新闻报道确立，而非其竞选自有页面。**条目较少的议题（枪支、医疗、劳工、宗教）反映的是来源可得性，而非议题权重。** `_staging/B_gaps.md` 第 5 节有记录；数据集未作注水。
54. **Paxton positions left `unverified`, not guessed:** NATO/State/USAID posture, SD-8
    tenure substance, law-practice detail, debate-refusal reasoning.

    **帕克斯顿部分立场标为 `unverified`（未核实）而非猜测：** 对北约／国务院／美国国际开发署的取向、州参议院第 8 选区任期实质、律师执业细节、拒绝辩论的理由。
55. **Talarico biography gaps:** pre-2017 employment detail, seminary enrolment detail,
    and campaign-manager confirmation *inside Agent B's scope* (the manager — Seth
    Krasne — is documented by the Lead via El Paso Times in `campaign_organization.md`;
    Agent B deliberately did not include unverified Lead-supplied leads).

    **塔拉里科传记缺口：** 2017 年以前的任职细节、神学院就读细节，以及在代理 B 范围内对竞选经理的确认（经理 Seth Krasne 由主导研究者经《埃尔帕索时报》在 `campaign_organization.md` 中确立；代理 B 有意不纳入未经核实的、由主导方提供的线索）。
56. **Launch-date conflict.** Talarico's launch is 2025-09-09 (documented), but a
    2025-09-05 preview said he "planned to launch" — marked `conflicting sources`.

    **参选宣布日期冲突。** 塔拉里科于 2025-09-09 宣布参选（有据），但 2025-09-05 的一篇预告称他"计划宣布"——标为 `conflicting sources`。
57. **Age conflict.** 28 (TIME) vs 29 (Wikipedia) at election to the Texas House;
    reconciled via the 1989-05-17 birth date with both readings stated. Also 36 vs 37
    reported age during the campaign (birthday in August 2026).

    **年龄冲突。** 当选德州众议员时，28 岁（《时代》）对 29 岁（维基百科）；已按 1989-05-17 出生日期调和，并同时列出两种读法。竞选期间报道年龄亦有 36 与 37 两说（其生日在 2026 年 8 月）。
58. **Lead-supplied leads that Agent B did not independently verify** (Politico/Ted Cruz,
    Denton Peterbilt, Houston Chronicle, The Root, Spectrum, El Paso staffing) are
    quarantined in `B_gaps.md` §3 for correct attribution. The Lead subsequently
    verified the El Paso Times and Politico items directly; attribution is recorded in
    `campaign_organization.md` and `image_archive.csv`.

    **代理 B 未独立核实的、由主导方提供的线索**（Politico／泰德·克鲁兹、丹顿 Peterbilt、休斯敦纪事报、The Root、Spectrum、埃尔帕索人事）隔离在 `B_gaps.md` 第 3 节以便正确归属。主导研究者随后直接核实了《埃尔帕索时报》与 Politico 的相关条目；归属记录在 `campaign_organization.md` 与 `image_archive.csv` 中。

---

## 9. Source-integrity notes for the human researcher / 给人类研究者的来源完整性提示

59. **Two campaigns, one event, opposite descriptions.** The debate dispute is the
    clearest case: Paxton said negotiations foundered because Talarico "always wants
    something we can't do"; Talarico's spokesperson called that "lying" and said Paxton
    "ignored every single attempt… including a personal call to his cellphone." Both
    recorded, neither adjudicated.

    **同一事件，两套说辞，且完全相反。** 辩论之争最为典型：帕克斯顿称谈判破裂是因为塔拉里科"总是要一些我们做不到的东西"（译）；塔拉里科的发言人指其为"撒谎"（译），并称帕克斯顿"无视了每一次尝试……包括打到他手机的一通私人电话"（译）。两者均予记录，均不裁定真伪。
60. **Partisan-source characterisations** are labelled as such.

    **党派来源的定性表述**均已标注其党派属性。
61. **Campaign-claim vs independent reporting** is separated structurally via
    `report_type` / `sponsor_type` / `coverage_type` / `verification_status` fields.

    **阵营宣称与独立报道**通过 `report_type`／`sponsor_type`／`coverage_type`／`verification_status` 字段在结构上区分。
62. **Tour-size conflict.** Paxton's tour: "30+ stops" (campaign, via Dock Line) vs "one
    of 12 on Paxton's Come and Take It Tour" (KGNS Laredo). Archive uses "30+ planned"
    and flags the "12" as a local-outlet discrepancy.

    **巡回规模冲突。** 帕克斯顿巡回宣传："30 余站"（阵营口径，经 Dock Line）对"帕克斯顿 Come and Take It 巡回的第 12 站"（KGNS 拉雷多）。档案采用"计划 30 余站"，并把"12 站"标为地方媒体的口径差异。
63. **Laredo date conflict.** Paxton's Laredo stop is 2026-10-23 per KGNS (verified) and
    "reported as Oct 24" per a Tribune caption; the row is `conflicting sources` with
    the dedupe reasoning in `analyst_notes`. A third duplicate row was deleted.

    **拉雷多日期冲突。** 帕克斯顿拉雷多站据 KGNS 为 2026-10-23（已核实），而《德州论坛报》图注"报道为 10 月 24 日"；该行标为 `conflicting sources`，去重理由写在 `analyst_notes`。另有一行重复记录已删除。
64. **Tyler is four distinct items**, not one: Vance surrogate (10-13), Talarico rally
    (10-20), a cancelled Paxton October stop, and Paxton's rescheduled 11-01 stop.

    **泰勒市涉及四个不同事项**，而非一件事：万斯的代理活动（10-13）、塔拉里科集会（10-20）、帕克斯顿一场被取消的 10 月站点、以及帕克斯顿改期至 11-01 的站点。
65. **Source registry reconciliation.** 206 agent-registry rows merged into **189 unique
    sources** (`09_sources/sources.csv`) with URL-level de-duplication; 17 URLs were
    independently retrieved by more than one research stream and are marked as such.
    Cross-stream duplicates are a positive integrity signal, not an error.

    **来源登记对账。** 206 条代理登记行经 URL 去重后合并为 **189 个唯一来源**（`09_sources/sources.csv`）；17 个 URL 被不止一条研究线索独立抓取，已作标注。跨线索重复是正向的完整性信号，不是错误。

---

## 10. What would most improve this archive (prioritised) / 最应优先补齐的事项

1. **Texas Secretary of State county canvass** → fills `county_results.csv` and converts
   every percentage from "aggregator-reported" to "certified." Highest value, one action.

   **德州州务卿县级选举认证数据** → 填充 `county_results.csv`，并把每个百分比从"汇总方报道"升级为"官方认证口径"。价值最高，一步到位。
2. **FEC line-item filings** via OpenFEC (with a real API key) or a browser → converts
   `campaign_finance.csv` from "as reported" to "as filed," and lets IEs be split by date.

   **FEC 逐条申报**（用真实 OpenFEC 密钥或浏览器）→ 使 `campaign_finance.csv` 从"按报道"升级为"按申报原件"，并可按日期拆分独立支出。
3. **Campaigns' Eventbrite / event archives** → completes both tour stop lists (15 Paxton
   cities and 11 Talarico cities are currently schedule-only).

   **两阵营的 Eventbrite／活动存档** → 补全双方巡回站点清单（目前帕克斯顿 15 个、塔拉里科 11 个城市仅有日程记录）。
4. **Full video of 8–12 major speeches** → genuine transcripts, timecodes, and the first
   real prosody analysis; converts `partially verified` speech rows to `verified`.

   **8–12 场主要演讲的完整视频** → 生成真实文字稿与时间码，并首次进行真正的韵律分析；把 `partially verified` 的演讲行升级为 `verified`。
5. **An image-capable analyst plus a landmark tool** → executes the facial-geometry and
   body-proportion protocol already written in `visual_analysis_*.md`; also fills the
   clothing columns.

   **具备图像能力者搭配关键点检测工具** → 执行 `visual_analysis_*.md` 中已写好的面部几何与身体比例规程；并可填补着装字段。
6. **AdImpact's underlying report** → reconciles the outside-spending figures, and
   separates FEC Schedule E from ad-spend tracking.

   **AdImpact 的底层报告** → 对账外部支出数字，并区分 FEC Schedule E 与广告投放监测。
7. **Certified GOP primary margin** → resolves the 1.1-pt vs 2.5-pt conflict.

   **共和党初选的认证差距** → 解决 1.1 个百分点对 2.5 个百分点的冲突。
8. **Campaign photo libraries** (official Flickr/site galleries) → would substantially
   close the Talarico image shortfall with properly licensed material.

   **阵营官方图库**（官方 Flickr／网站图片页）→ 将以许可合规的素材大幅缩小塔拉里科的影像缺口。

---

## 11. Agent-level gap registers (preserved for granular detail) / 代理层面的缺口登记（保留细粒度信息）

The Lead merged headline items into the sections above; the staging files retain
per-item granularity (specific missing photo URLs, per-source 403s, quote-level
caveats):

主导研究者已将要点合并入上文各节；阶段文件保留了逐项粒度（具体缺失的照片 URL、逐个来源的 403、引语级注意事项）：

- Event reconstruction: `_staging/A_gaps.md` / 事件重构
- Biography / policy: `_staging/B_gaps.md` / 传记与政策
- Speeches / communication: `_staging/D_gaps.md` / 演讲与传播
- Finance / media: `_staging/E_gaps.md` / 资金与媒体
- **Visual archive: no `C_gaps.md` exists** — Agent C produced no output; §7 above is
  the replacement register.
  **影像档案：不存在 `C_gaps.md`**——代理 C 未产出；上文第 7 节即为替代登记。
