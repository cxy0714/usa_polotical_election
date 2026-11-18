---
title: "Research gaps — 2026 Ohio Senate special election"
title_zh: "研究缺口 — 2026年俄亥俄州联邦参议员特别选举"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Every known gap is listed with its cause and the specific source that would close it.
---

# Research gaps / 研究缺口

## 1. County-level results do not exist in retrievable form / 县级结果不可得

**Gap.** `07_electoral_context/county_results.csv` has the required header and **zero rows**.
**Cause.** The Wikipedia article renders county results only as two SVG maps
(`2026 United States Senate special election in Ohio results map by county.svg` and the
Democratic-primary equivalent). It gives a list of seven counties that flipped Republican to
Democratic (Delaware, Erie, Lake, Mahoning, Portage, Trumbull, Wood) but no table of votes by
county. The Ohio Secretary of State results portal returned HTTP 403 on every attempt, and so did
the two official canvass spreadsheets on `publicfiles.ohiosos.gov` (the May primary and the
November general election files, including a Senate-specific extract); the AP, Politico and
Columbus Dispatch results pages returned 403/402.
**What would close it.** The Ohio Secretary of State's official canvass by county
(`ohiosos.gov`), or the AP county file; either would supply 88 county rows.

**缺口。** `county_results.csv` 只有表头，零行数据。**原因。** 条目仅以两张SVG地图呈现县级结果，
另列出7个由共和党翻转为民主党的县（特拉华、伊利、莱克、马霍宁、波蒂奇、特朗布尔、伍德），
但无逐县票数表；俄亥俄州务卿结果门户每次均返回403，美联社、Politico、哥伦布快报的结果页返回403/402。
**如何补齐。** 州务卿官方逐县计票文件。

## 2. No joint debate is documented / 未见联合辩论记载

**Gap.** The brief asked to check whether Ohio had at least one general-election debate. This
archive found **none**. There is no `debate` row in `campaign_events.csv`.
**Cause.** The Wikipedia article contains no occurrence of "debate". The only traces are a
WDTN headline dated 2026-10-30 ("Ohio's Senate candidates debate rising costs ahead of midterms",
body unretrievable) and a BGSU/YouGov poll whose write-up says fieldwork went into the field
"before the question of debates became a campaign issue" while 54% of Ohioans said it was very
important that the Senate candidates debate (SRC-1148).
That phrasing implies a dispute about debates, not that one occurred.
**What would close it.** A debate sponsorship page (league, TV station, or university), or the
C-SPAN/Ohio Channel schedule for October 2026.

**缺口。** 简报要求核查俄亥俄是否至少举行过一场大选辩论；本档案未发现任何一场，因此事件表中无
`debate` 行。**原因。** 条目中无“debate”字样；仅有两条线索：2026-10-30 WDTN 标题（正文不可得），
以及鲍林格林州立大学/YouGov 民调提到实地调查在“辩论是否成为竞选议题之前”已完成，而54%的俄亥俄人
认为参议员候选人辩论“非常重要”。这只说明存在关于辩论的争议，并不证明辩论发生。
**如何补齐。** 辩论主办方页面，或2026年10月 C-SPAN/Ohio Channel 节目表。

## 3. Television advertising creative was not retrievable / 电视广告素材不可得

**Gap.** `05_campaign_media/advertisements.csv` documents 8 ads, but only one has a video URL
that loaded (a Commons-hosted campaign video, PD). The rest are documented from reporting,
FEC/outside-group releases and OCJ fact-checks, with `video_url` = `unknown`.
**Cause.** Ad libraries (Meta, Google) and YouTube require JavaScript or block the archiver;
the campaign sites are JS shells; the 10TV video page returned 403.
**What would close it.** Meta Ad Library and Google Political Ads Transparency Report exports
for the two committees, plus a working YouTube download of the NRSC and AFP Action spots.

**缺口。** 广告表记录8条，但仅1条含可访问视频链接。**原因。** 广告库需JavaScript或被屏蔽；
竞选网站为JS外壳；电视台视频页403。**如何补齐。** Meta 广告库与 Google 政治广告透明度报告导出。

## 4. AP and Politico originals are paywalled or blocked / 美联社与Politico原文不可达

**Gap.** The AP story on the result and Politico's coverage are cited only through mirrors
(Boston Herald for AP; none for Politico).
**Cause.** apnews.com and politico.com return 403 to the archiver; the Internet Archive captures
of Politico render an interstitial.
**What would close it.** Institutional access, or an AP member-paper mirror for each specific
story.

**缺口。** 美联社与Politico报道仅通过转载（波士顿先驱报载美联社稿）引用。**原因。** 两家站点
均返回403，Politico的存档页只显示插入页。**如何补齐。** 机构订阅或成员报转载。

## 5. Finance figures are the article's table, not scraped FEC totals / 财务数字来自条目表格

**Gap.** `06_campaign_finance/campaign_finance.csv` reproduces the article's FEC-cited tables
(two periods per candidate). Individual contributions, PAC contributions and debts owed are
`unknown` because the article's tables have only raised / spent / cash on hand.
**Cause.** The FEC candidate pages render totals by JavaScript; the retrieved HTML carries no
numbers. `docquery.fec.gov` filing PDFs were reachable for a minor candidate only.
**What would close it.** The FEC bulk `committee`/`candidate` files or the F2/F3 filings
themselves.

**缺口。** 财务表复现条目所引 FEC 表格（每人两个期间），但个人捐款、PAC捐款、债务均为 `unknown`。
**原因。** FEC 页面由 JavaScript 渲染，抓取的 HTML 无数字。**如何补齐。** FEC 批量数据文件或原始 F3 报表。

## 6. Crowd sizes and rally attendance are almost never reported / 现场人数几乎无报道

**Gap.** Of 35 event rows, only one has a size description ("hundreds", "capacity" room at the
Dayton rally). The rest are `unknown`.
**Cause.** Ohio outlets describe rallies qualitatively; no campaign released attendance counts.
**What would close it.** Pool reports or fire-marshal estimates; neither is published in Ohio.

**缺口。** 35条事件中仅1条有人数描述（代顿集会“数百人”“满场”）。**原因。** 地方媒体报道多为定性描述，
竞选方未发布人数。**如何补齐。** 记者团联合报道或消防部门估算。

## 7. Speech transcripts are absent / 演讲全文缺失

**Gap.** `03_speeches/speech_archive.csv` has 14 rows, but only a handful carry verbatim
quotations and none carries a full transcript; `transcript_url` is `unknown` throughout.
**Cause.** Neither campaign publishes transcripts. C-SPAN catalogued at least one Husted event
(2026-09-25) but the page returned HTTP 202 with no body. The one full recording retrieved is a
62-second Senate floor clip from 2026-07-27 (public domain, Commons).
**What would close it.** C-SPAN closed-captioning exports or the Congressional Record for floor
speeches.

**缺口。** 演讲表14行，仅少数含逐字引语，无完整文字稿。**原因。** 两阵营均不发布文字稿；C-SPAN 页面返回202无正文。
**如何补齐。** C-SPAN 字幕导出或《国会记录》。

## 8. Two decimal disagreements in the published result / 公布结果存在两处小数分歧

**Gap.** Husted is 45.17% in the article's table and 45.15% in the Calfee newsletter the article
cites as its results source; Levy is 2.04% versus 2.05%.
**Cause.** Rounding of the same vote counts at different precisions, or a typo in one table.
**Resolution in this archive.** Vote counts are treated as primary (they sum exactly to
4,604,860 and reproduce 45.17%); the alternative percentages are recorded in
`results_notes.md` rather than silently replaced.

**缺口。** 赫斯特德在条目表格中为45.17%，在条目所引律所通讯中为45.15%；利维2.04%对2.05%。
**本档案处理。** 以票数为准（合计精确等于4,604,860，反算得45.17%），替代百分比在 `results_notes.md` 中记录。

## 9. Minor candidates are thinly covered / 小党候选人资料稀薄

**Gap.** Redpath and Levy appear in `election_results.csv` and in a few rows, but there is no
biography file for either.
**Cause.** The contract scopes candidate folders to the two major-party nominees.
**What would close it.** Optional third-candidate appendix if the repository later wants one.

**缺口。** 雷德帕斯与利维仅出现在结果表与少量行中，无传记文件。**原因。** 合同将候选人目录限定为两大党提名人。

## 10. Date discrepancies inherited from the task brief / 简报中的日期错误

**Gap.** The brief states Husted was "appointed 2025-01-10" and "sworn in 2025-01-14".
**Cause.** 2025-01-10 is the date Vance's resignation took effect; 2025-01-14 is the date
DeWine and Husted were inaugurated as governor and lieutenant governor in 2019, not a Senate
oath.
**Resolution.** The archive uses 2025-01-17 (announcement) and 2025-01-21 (oath) and states the
correction in `results_notes.md`, `01_candidates/husted/career_timeline.csv` and
`08_comparative_analysis/candidate_comparison.md`.

**缺口。** 简报称赫斯特德“2025-01-10获任命、2025-01-14宣誓”。**原因。** 1月10日是范斯辞职生效日，
1月14日是2019年德万与赫斯特德就任州长/副州长的日期。**处理。** 本档案采用1月17日（宣布）与1月21日（宣誓）。
