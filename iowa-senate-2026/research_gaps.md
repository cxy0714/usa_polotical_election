---
title: Research gaps
title_zh: 研究缺口
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Eleven gaps, each with its cause and the step that would close it; the weakest are Hinson's ad creative, county-level primary returns and Turek's licensed imagery.
---

# Research gaps / 研究缺口

## 1. No county-level primary results

**Gap / 缺口**: `county_results.csv` covers the general election only. / `county_results.csv` 只覆盖大选。
**Cause / 原因**: The county geometry in the NBC payload is tied to the general-election race; no primary
county table was published in a page this archive could read. / NBC 数据中的县级几何只绑定大选场次；可读取的页面没有公布初选县级表。
**Closing it / 补足方式**: The Iowa Secretary of State's official canvass (blocked here: 403) or the AP
primary feed would carry county-level primary returns. / 艾奥瓦州务卿官方计票（本批次被 403 拒绝）或 AP 初选数据源可提供县级初选结果。

## 2. Hinson's own advertising is undocumented

**Gap / 缺口**: `advertisements.csv` holds three Turek spots and two headline-level outside buys; no Hinson
campaign ad creative was retrieved. / 广告表有三条 Turek 广告与两条标题级外部投放；未取得 Hinson 本人的广告素材。
**Cause / 原因**: Her ad launches were reported inside event coverage rather than as standalone ad stories,
and no ad-library page was retrieved. / 她的广告发布多在活动报道中被顺带提及，未作为独立报道出现；也未取得广告库页面。
**Closing it / 补足方式**: Meta and Google political ad libraries, or the campaign's YouTube channel
listing, would give titles, dates and scripts. / Meta 与 Google 政治广告库，或竞选团队的 YouTube 频道列表，可提供标题、日期与脚本。

## 3. No crowd or venue detail for two-thirds of events

**Gap / 缺口**: 22 of 33 event rows carry no crowd figure and several carry an unnamed venue. / 33 场活动中 22 场无人数记录，若干场无具名场地。
**Cause / 原因**: The covering reports are quote-led; only the large set-piece events got crowd numbers. / 报道以引述为主，只有大型活动才报人数。
**Closing it / 补足方式**: Local TV packages, pool photos and county-party Facebook posts would supply
staging and headcounts. / 地方电视台报道、联合采访照片与县党部脸书帖可提供现场与人数。

## 4. The "Fighting for Iowa Tour" has no dates

**Gap / 缺口**: Hinson's website advertises a tour; no stop could be dated or located. / Hinson 官网宣传一项巡回活动，但无任何一站可确定日期或地点。
**Cause / 原因**: Only the site navigation and a sign-up form were retrievable. / 只能取得网站导航与报名表单。
**Closing it / 补足方式**: The tour's own landing page or a dated press release. / 巡回活动专页或有日期的新闻稿。

## 5. No primary polling numbers

**Gap / 缺口**: Primary polls exist (an NRSC poll, a Public Policy Polling survey, a Bedrock poll) but no
topline could be read. / 初选民调确实存在（NRSC、PPP、Bedrock 各一），但读取不到具体数字。
**Cause / 原因**: The pages carrying them were blocked or were headline-only. / 载有数字的页面被拒或仅有标题。
**Closing it / 补足方式**: The pollsters' own PDF releases. / 民调机构自己的 PDF 发布稿。

## 6. The ad record is thin, and it is one-sided

**Gap / 缺口**: Nine ad rows exist but all seven candidate rows are Turek's; there is **no Hinson campaign ad
creative at all**. / 广告表有 9 条，但七条候选人广告全部属于 Turek；**完全没有 Hinson 本人的广告素材**。
**Cause / 原因**: Turek's spots were covered as news (one report even printed a script verbatim); hers were
not, and outside spending is reported only at headline level. / 可读文本中的广告记录本就稀薄：外部支出只有标题级报道，她的素材未出现在已抓取页面中。
**Closing it / 补足方式**: Ad-library exports (Meta, Google, Snapchat) or a single AdImpact report would close
this in one step. / 广告库导出（Meta、Google、Snapchat）或一份 AdImpact 报告即可一步补足。

## 7. Turek has no downloadable official portrait

**Gap / 缺口**: All four Iowa Legislature portraits are "Copyrighted free use", outside the four permitted
licences. / 四张州议会肖像均为 "Copyrighted free use"，不在允许的四种授权内。
**Cause / 原因**: Licence policy, not availability. / 原因在授权政策，而非可得性。
**Closing it / 补足方式**: A campaign-released photo under CC BY, or a written permission from the Iowa
Legislature. / 竞选团队以 CC BY 发布的照片，或州议会的书面许可。

## 8. Paywalled and blocked outlets

**Gap / 缺口**: Des Moines Register (HTTP 402), The New York Times, Politico, AP and USA Today (403/402),
`sos.iowa.gov` (403) and the state results application (JavaScript shell only). / 《得梅因纪事报》（402）、纽约时报、Politico、AP、今日美国（403/402）、州务卿网站（403）及州结果应用（仅 JS 壳）。
**Cause / 原因**: Paywalls and bot blocking; all are logged in `_staging/fetch_log.csv`. / 付费墙与反爬；均已记录在抓取日志。
**Closing it / 补足方式**: Institutional access to the Register and to the AP feed, or the state's bulk
results download. / 机构订阅《纪事报》与 AP 数据源，或州级批量结果下载。

## 9. Individual vs PAC contribution splits

**Gap / 缺口**: `individual_contributions`, `pac_contributions` and `debts_owed` are `unknown` in every
finance row. / 资金表中个人捐款、PAC 捐款与债务三列全部为 unknown。
**Cause / 原因**: The summary table reproduced by the race article has receipts, disbursements and cash only;
the FEC's own pages returned 403. / 竞赛条目转载的汇总表只有收入、支出与现金三项；FEC 页面返回 403。
**Closing it / 补足方式**: FEC bulk data files (`indiv` and `pas2` extracts) for the relevant committees. / FEC 批量数据文件（indiv 与 pas2 提取）。

## 10. Turek's non-verbal event record

**Gap / 缺口**: No retrieved source describes staging, seating, ramps or how he reaches a lectern. / 已抓取来源均未描述舞台、座位、坡道或他如何上台。
**Cause / 原因**: Political reporting rarely describes access arrangements, and this archive had no video or
image input. / 政治报道很少描述无障碍安排，本档案也没有视频或图像输入。
**Closing it / 补足方式**: Event video and venue access statements; a field observation would settle it. / 活动视频与场地无障碍声明；现场观察可直接解决。

## 11. The "Iowa values" and religion dimension

**Gap / 缺口**: Hinson's religious appearances are documented only through surrogates (Kennedy at a Christian
fundraiser); Turek's faith position is undocumented. / Hinson 的宗教场合只有代理人记录（Kennedy 出席基督教筹款会）；Turek 的信仰立场无记录。
**Cause / 原因**: Neither campaign's own faith-and-values messaging was retrievable beyond site boilerplate. / 除官网套话外，双方信仰与价值观表述均未取得。
**Closing it / 补足方式**: Church-event coverage or the candidates' own statements at faith forums. / 教会活动报道或候选人在信仰论坛上的自述。
