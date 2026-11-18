"""Core documents: README, research_gaps, _research_conventions, data dictionary."""
import sys

sys.path.insert(0, "_staging")
from doc_lib import write  # noqa: E402

FM = """---
title: {en}
title_zh: {zh}
{cand}compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: {status}
coverage_note: {note}
---
"""

README = """---
title: "2026 United States Senate special election in Ohio — case archive"
title_zh: "2026年俄亥俄州联邦参议员特别选举 — 案例档案"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Result, appointments, finance and positioning are solid; county-level results and any joint debate are not documented in retrievable sources.
---

# 2026 Ohio U.S. Senate special election / 2026年俄亥俄州联邦参议员特别选举

## 1. What this archive covers / 本档案覆盖范围

This case covers the 2026 special election to fill the U.S. Senate seat vacated by JD Vance
when he became vice president. The seat was filled by gubernatorial appointment on
2025-01-17 and the appointee, Jon Husted, defended it in a special election held concurrently
with the 2026 general election on 2026-11-03. Sherrod Brown, who had lost this same seat in
2024, won it back. The archive holds 15 CSVs (candidates, events, speeches, visuals, campaign
media, finance, electoral context) plus bilingual analysis documents, and logs every retrieval
in {{wiki_ohio}} and {{ref047_www_fec_gov_data_elections_senate_OH_2026}}.

本案例研究2026年俄亥俄州联邦参议员特别选举：JD·范斯就任副总统后留下的参议院席位先由州长
任命填补（2025年1月17日宣布），被任命者乔恩·赫斯特德在2026年11月3日与中期选举同日举行的
特别选举中捍卫该席位。2024年失去该席位的谢罗德·布朗重新赢回。档案包含15个CSV数据集与中英
双语分析文档。

## 2. Documented result / 已记录的结果

| Candidate / 候选人 | Party / 政党 | Votes / 得票 | Share / 得票率 | Winner |
|---|---|---|---|---|
| Sherrod Brown | Democratic | 2,302,669 | 50.01% | yes |
| Jon Husted (incumbent) | Republican | 2,080,064 | 45.17% | no |
| Bill Redpath | Libertarian | 128,341 | 2.79% | no |
| Greg Levy | Party for Socialism and Liberation | 93,786 | 2.04% | no |
| **Total** | | **4,604,860** | **100.00%** | |

Vote counts are the article's canvass table ({{wiki_ohio}}); the percentages are those printed
there and they sum to 100.01 after rounding, which is discussed in
`07_electoral_context/results_notes.md`. A law-firm election newsletter gives Husted 45.15% and
Levy 2.05% instead ({{wiki_ohio}} cites it as its own results source), so the two decimal
disagreements are recorded rather than smoothed over.

上表票数取自条目中的计票表；条目自身打印的百分比四舍五入后合计为100.01%，该差异在
`results_notes.md` 中说明。一家律所选举通讯给出的赫斯特德得票率为45.15%、利维为2.05%，
这一冲突已记录而非被抹平。

## 3. Structural facts this archive establishes / 本档案确立的结构性事实

**1. The appointment, not the election, created the incumbency.** Vance resigned effective
2025-01-10; Gov. Mike DeWine announced Husted's appointment on 2025-01-17 and Husted took the
oath on 2025-01-21 ({{ocj25_ohio_lt_gov_jon_husted_to_replace_jd_vance_in_u_s_senat}},
{{husted_sworn_in_2025}}). Every "incumbent" label in this archive is dated to those two days.
The task brief's "appointed 2025-01-10 / sworn in 2025-01-14" matches neither the resignation
date nor any retrieved record, and is corrected here.

**2. Money ran one way and the polls did not.** Through 2026-09-30 Brown had raised
$68,409,200 to Husted's $19,894,786 ({{wiki_ohio}}), yet the race was rated a toss-up all year
and the final margin was 4.84 points. Outside spending exceeded $500 million
({{b4_cle_clash}}), so candidate receipts were a minority of the money in the race.

**3. Data centers became the sleeper issue.** A leaked NRSC memo called data centers "the anchor
hanging around Husted's neck" and the race "a dead heat" ({{ocj31_leaked_memo_about_data_centers_shows_gop_worried_about}}).
Brown built his closing argument on Husted's recruitment of them — despite having praised an
Amazon data center in a 2015 release ({{b4_yahoo_keyissues}}).

**4. Labour split rather than labour consolidation.** Brown held the UAW, Steelworkers, IUPAT,
IFPTE, CWA, the Ohio Federation of Teachers and the Ohio AFL-CIO; Husted took the Operating
Engineers, Boilermakers, Cleveland Building Trades, ABC of Ohio and the state FOP
({{ref072_chroniclet_com_news_448231_uaw_endorses_democrat_sherro}},
{{ref032_www_nbcnews_com_politics_2026_election}},
{{ref028_chroniclet_com_news_470613_abc_of_ohio_endorses_jon_hus}}). A Republican carrying
building trades and the Boilermakers is the unusual part.

**5. A split-ticket state.** Brown won 50.01% in a state Trump carried three times, and
Democrats swept the Ohio governor, secretary of state and treasurer races in the same election
({{wiki_ohio}}). The Senate result was part of a state-level Democratic wave, not an isolated
personal comeback.

## 4. Folder map / 目录结构

| Path | Contents |
|---|---|
| `01_candidates/policy_positions.csv` | 30 issue rows (16 Brown, 14 Husted) with verbatim statements where retrieved |
| `01_candidates/brown/`, `01_candidates/husted/` | biography, political_positions, career_timeline per candidate |
| `02_campaign_events/campaign_events.csv` | 35 dated events (15 Brown, 20 Husted) |
| `03_speeches/` | speech_archive.csv, speech_video_index.csv, two communication analyses |
| `04_visual_archive/` | image_archive.csv, downloaded Commons portraits, image notes |
| `05_campaign_media/` | advertisements.csv, social_media.csv, media_coverage.csv |
| `06_campaign_finance/campaign_finance.csv` | FEC-derived finance periods |
| `07_electoral_context/` | election_results, county_results, polling, election_context, results_notes |
| `08_comparative_analysis/candidate_comparison.md` | cross-candidate comparison |
| `09_sources/` | sources.csv, data_dictionary_bilingual.md |
| `_staging/` | fetch log, mirrors, text extractions, build scripts |

## 5. What is strong vs thin / 强项与薄弱环节

Strong: the result arithmetic and its internal inconsistencies; the appointment chronology; the
finance asymmetry; the issue positions, because both campaigns answered a structured issue
questionnaire that was retrieved in full ({{b4_yahoo_keyissues}}); the union and county-party
endorsement record.

Thin: county-level results (no table exists in the article — only two SVG maps); any joint
debate (nothing in the retrieved corpus documents one); crowd sizes (almost never reported);
speech transcripts (no campaign publishes them, and the video pages that would carry them
returned 403); television advertising (no ad URLs were retrievable, so six of the eight ad rows
are documented through reporting rather than the creative itself).

强项：结果算术及其内部矛盾、任命时间线、筹款不对称、议题立场（两阵营均回答了结构化议题问卷且全文可获取）、
工会与县党 endorsement 记录。薄弱：县级结果（条目仅有地图SVG、无表格）、联合辩论（现有语料无任何记载）、
现场人数（几乎无报道）、演讲全文（无竞选发布，视频页403）、电视广告（广告链接不可得，8条中6条依据报道而非广告本身）。

## 6. Validation status / 校验状态

`python _tools/validate_case.py ohio-senate-2026` reports **0 hard failures**. Remaining soft
warnings, and every place where the archive is short of a target, are listed with their cause in
`research_gaps.md`. No cell contains a placeholder; `unknown` is used as a value wherever the
retrieved record does not state the fact.

校验脚本报告 **0 个硬失败**。其余软警告及所有未达目标的项均在 `research_gaps.md` 中列明原因。
所有单元格均无占位符；凡检索记录未载明的事实一律填 `unknown`。

## 7. Reading paths / 阅读路径

1. Result first: `07_electoral_context/results_notes.md` → `election_results.csv` → `polling.csv`.
2. Why it happened: `08_comparative_analysis/candidate_comparison.md` → `policy_positions.csv`.
3. How it was fought: `02_campaign_events/campaign_events.csv` → `05_campaign_media/media_coverage.csv`.
4. Money: `06_campaign_finance/campaign_finance.csv` → `b4_cle_clash` (total-spending context).
5. Method and provenance: `_research_conventions.md` → `09_sources/sources.csv`.

## 8. Provenance note / 来源说明

`sources.csv` holds 180+ entries, all retrieved on 2026-11-18 and mirrored under `_staging/`
with a row in `_staging/fetch_log.csv` recording status and byte count. Sources that returned
403/402 (AP, Politico, the Ohio Secretary of State, several TV stations) are recorded in the
fetch log as failures and are **not** cited as content; where their reporting was needed, a
syndicated mirror that did load is cited instead and the substitution is stated in
`reliability_notes`.

`sources.csv` 收录180余条来源，均于2026-11-18抓取并镜像保存，抓取日志记录状态与字节数。
返回403/402的来源仅作为失败记录，绝不作为内容引用；确需其报道时改用可访问的转载版本，并在
`reliability_notes` 中说明替换关系。
"""

GAPS = """---
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
county. The Ohio Secretary of State results portal returned HTTP 403 on every attempt, and the
AP, Politico and Columbus Dispatch results pages returned 403/402.
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
important that the Senate candidates debate ({{ref191_www_bgsu_edu_arts_and_sciences_democracy}}).
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
"""

CONV = """---
title: "Research conventions used in this case"
title_zh: "本案例使用的研究规范"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Rules for dates, sourcing, quoting, unknowns and bilingual structure.
---

# Research conventions / 研究规范

## 1. Retrieval and logging / 抓取与日志

Every URL in `09_sources/sources.csv` has a row in `_staging/fetch_log.csv` with its HTTP status,
byte count, timestamp and mirror path. Failures (403, 402, 429, 0) stay in the log and are never
cited as content. A source that is not in the log may not appear in `sources.csv`. Retrieval used
`urllib` with an explicit User-Agent (`Mozilla/5.0 (research archive)`), one request per URL, no
retries against a blocking host.

`sources.csv` 中每个链接在 `_staging/fetch_log.csv` 均有状态、字节数、时间与镜像路径记录。
失败请求保留在日志中且绝不作为内容引用。未入日志者不得进入 `sources.csv`。

## 2. Source tiers / 来源分层

- **T1** official: FEC, Senate/Commons official portraits, campaign websites, government records.
- **T2** journalism: regional dailies, statehouse bureaus, wire services, pollster releases.
- **T3** synthesis: Wikipedia, aggregators, ratings pages, law-firm newsletters.

T3 is used for the spine (dates, tables) but any T3-only fact is marked `partially verified`.
When T2 and T3 disagree, both values are recorded.

**T1** 官方；**T2** 新闻；**T3** 综合（维基、聚合站、评级页）。仅有T3支撑的事实标注 `partially verified`；
T2与T3冲突时两者并记。

## 3. Dates / 日期

`event_date` is the date the event happened, not the publication date; when a report says
"Wednesday" or "Monday", the date is derived from the publication date and the derivation is
stated in `analyst_notes`. Husted's incumbency is **always** dated: announcement 2025-01-17, oath
2025-01-21. `unknown` is written where no record fixes the date.

`event_date` 记事件发生日而非发稿日；由“周三/周一”推算的日期在 `analyst_notes` 中说明推算过程。
赫斯特德的在任起点一律标注：2025-01-17 宣布、2025-01-21 宣誓。

## 4. Quoting / 引语

Quotation marks mean the words appeared inside quotation marks in the retrieved source. Paraphrase
is never placed inside quotation marks. Where a campaign speaks through a spokesperson, the row
says so and the quote is attributed to the spokesperson. No quote is reconstructed from memory or
from a search-result snippet.

引号内文字必须是检索到的原文引号内容；转述绝不加引号；由发言人代述时明确标明。不得凭记忆或搜索摘要
重构引语。

## 5. `unknown` and placeholders / `unknown` 与占位符

`unknown` is a legitimate value and is used whenever the record is silent. `TBD`, `TODO`, `N/A`,
`NA`, `null`, `None` and `-` are forbidden by the validator and do not appear.

凡记录未载明即填 `unknown`；禁用占位符。

## 6. Verification vocabulary / 校验语汇

- `verified` — an official record or two independent T2 sources agree.
- `partially verified` — one T2 source, or T3 corroborated by one T2.
- `conflicting sources` — two retrieved sources disagree; both are reported.
- `unverified` — a single non-independent claim, e.g. a campaign's own attendance or jobs figure.

## 7. Analytic writing / 分析写作

`analyst_interpretation` and `analyst_notes` are clearly separated from observed facts. The
archive does not infer crowd size, enthusiasm, or venue from a photograph, and it does not treat
a headline as a body fact.

`analyst_interpretation` 与 `analyst_notes` 与事实严格分离；不从照片推断人数、气氛或场地；不把标题当作正文事实。

## 8. Bilingual structure / 双语结构

Every `##` section carries an English block followed by its Chinese counterpart. English governs
where the two differ. Chinese text is written for a Chinese-reading researcher, not
machine-translated word for word.

每个 `##` 小节先英文后中文；两版不一致时以英文为准。

## 9. What this archive refuses to do / 本档案拒绝做的事

No composite quotes, no invented venues, no interpolated crowd sizes, no synthesised "typical"
rally description, no imputed policy position from party platform alone. Where a position is
inferred from endorsements rather than a statement, the row says so.

不合成引语、不虚构场地、不插值人数、不臆测立场；仅由 endorsement 推断的立场会明确标注。
"""

DICT = """---
title: "Data dictionary (bilingual)"
title_zh: "数据字典（双语）"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Field-by-field definitions for all 15 CSVs, with the vocabularies the validator enforces.
---

# Data dictionary / 数据字典

## 1. Shared conventions / 通用约定

| Field pattern | Meaning / 含义 |
|---|---|
| `*_id` | Stable identifier; never reused. `SRC-####` for sources, `EV-###` events, `POS-###` positions. |
| `source_urls` | Exactly one `SRC-####|https://…` pair; the id must exist in `sources.csv` and the URL must match it. |
| `verification_status` | `verified`, `partially verified`, `unverified`, `conflicting sources`. |
| dates | ISO `YYYY-MM-DD`; `unknown` when no record fixes the date. |
| `unknown` | A value, not a placeholder. |

`source_urls` 单元格只允许一个 `SRC-####|https://…` 组合，且必须与 `sources.csv` 对应行一致。

## 2. `09_sources/sources.csv`

| Column | Definition |
|---|---|
| `source_id` | `SRC-####`, assigned in retrieval order. |
| `url` | The exact URL retrieved and mirrored. |
| `title` | Page title as served, or a descriptive title where the page is a PDF/API response. |
| `publisher` | Domain owner, mapped from the host. |
| `publication_date` | Date the page states it was published (`unknown` if absent). |
| `event_date` | Date of the event the source documents (may equal `publication_date`). |
| `access_date` | Always `2026-11-18` for this case. |
| `source_tier` | `T1` official, `T2` journalism, `T3` synthesis. |
| `source_type` | `official_government`, `official_campaign`, `news_article`, `poll`, `press_release`, `photo`, `encyclopedia`, `analysis`, `op_ed`, `fact_check`, `other`. |
| `relevant_quote_or_info` | The specific fact or quote this source supplies. |
| `reliability_notes` | Provenance caveats: paywall, syndication, JS shell, 403 mirror substitution. |
| `used_by` | Which dataset or document relies on it. |

## 3. `01_candidates/policy_positions.csv`

| Column | Definition |
|---|---|
| `position_id` | `POS-###`. |
| `candidate_id` | `BROWN` or `HUSTED`. |
| `issue` | Controlled: `Economy`, `Healthcare`, `Education`, `Immigration`, `Abortion`, `Gun policy`, `Energy`, `Religion`, `Labor`, `Democracy`, `Foreign policy`, `Other`. |
| `subissue` | Free text narrowing the issue (e.g. "data centers and electricity bills"). |
| `position_summary` | One-sentence analytic summary. |
| `candidate_statement` | Verbatim quote with attribution, or "no verbatim statement retrieved in this archive". |
| `statement_date` | Date of the statement (`unknown` if the source does not date it). |
| `context` | Where and how the statement was made (interview, survey, hearing, rally). |
| `legislative_record` | Votes, bills, sponsorships relevant to the position. |
| `position_changed` | `yes`, `no`, `partial`, `unknown`. |
| `change_notes` | What changed and when, where documented. |
| `opponent_criticism` | The other campaign's attack on this position. |
| `fact_check` | Independent check of a numeric or factual claim, or `not applicable`. |

## 4. `02_campaign_events/campaign_events.csv`

| Column | Definition |
|---|---|
| `event_id` | `EV-###`. |
| `event_time` | Clock time if reported, else `unknown`. |
| `event_category` | Controlled vocabulary (`rally`, `endorsement_event`, `press_conference`, `swearing_in`, `appointment_announcement`, `victory_speech`, `concession_speech`, `watch_party`, `small_business_visit`, `workplace_visit`, `labor_event`, `party_event`, `other`). |
| `state_region` | `Northeast`, `Northwest`, `Central`, `Southwest`, `Southeast`, `statewide`, `national`, `unknown`. |
| `event_status` | `held`, `announced`, `cancelled`, `postponed`, `rescheduled`, `virtual`, `unverified`, `disputed`. |
| `campaign_phase` | `pre_launch`, `launch`, `primary`, `runoff`, `general`, `early_voting`, `gotv`, `election_day`, `post_election`. |
| `stated_purpose` | What the campaign said the event was for. |
| `observable_function` | What the event actually does mechanically (mobilisation, coalition signalling, result-claiming). |
| `analyst_interpretation` | Clearly-labelled inference. |
| `target_audience` | Whom the event addressed. |
| `main_messages` | Reported message content. |
| `policy_issues` | Issues raised at the event. |
| `speech_summary` | Summary of what was said, or `unknown`. |
| `transcript_url`, `video_url`, `photo_urls` | Direct media URLs or `unknown`. |
| `media_coverage` | Which retrieved reports covered the event. |
| `opponent_reference` | Whether and how the opponent was named. |
| `visual_notes` | What a retrieved photograph shows. |

## 5. `07_electoral_context/election_results.csv`

| Column | Definition |
|---|---|
| `race_id` | `OH-SEN-2026-SPECIAL`, or a per-candidate row id. |
| `candidate` | Candidate name as printed. |
| `party` | `Democratic`, `Republican`, `Libertarian`, `Party for Socialism and Liberation`. |
| `votes` | Integer vote count. |
| `percentage` | Printed share, two decimals, with `%` omitted. |
| `winner` | `yes` / `no`. |

## 6. `07_electoral_context/polling.csv`

| Column | Definition |
|---|---|
| `pollster` / `sponsor` | Field house and paying client (separate columns). |
| `field_start` / `field_end` | Fieldwork window, ISO. |
| `population` | `likely voters`, `registered voters`, `adults`. |
| `sample_size` | Integer. |
| `margin_of_error` | As printed (e.g. `3.1`). |
| `brown_pct` / `husted_pct` | Two-way shares as printed. |
| `other_pct` / `undecided_pct` | Remainder, split where the release splits it. |
| `leader` | Candidate leading in that poll. |
| `margin` | Leader's lead in points. |

## 7. `06_campaign_finance/campaign_finance.csv`

`period` is ISO (`2026-09-30`) or `YYYY-Qn`; `report_type` names the filing; `receipts`,
`disbursements`, `cash_on_hand` are integers as printed; `individual_contributions`,
`pac_contributions`, `debts_owed` are `unknown` when the source table omits them.

## 8. Vocabularies enforced by the validator / 校验器强制词表

`event_status`, `campaign_phase`, `event_category`, `issue`, `sponsor_type`, `coverage_type`,
`copyright_status`, `verification_status`, `source_tier`, `source_type`, `completeness`,
`winner`. `04_visual_archive/image_archive.csv` is the one place where `event_category` is free
text, because images can document things that are not campaign events.

`image_archive.csv` 的 `event_category` 是唯一允许自由文本的枚举列（图片可记录非竞选活动的内容）。

## 9. Bilingual field labels for the main tables / 主要表双语字段

| English | 中文 |
|---|---|
| votes | 得票数 |
| percentage | 得票率 |
| winner | 是否当选 |
| receipts | 收入 |
| disbursements | 支出 |
| cash_on_hand | 期末现金 |
| pollster | 民调机构 |
| sponsor | 委托方 |
| margin_of_error | 误差范围 |
| sample_size | 样本量 |
| field_start / field_end | 实地调查起止日 |
| county | 县 |
| event_category | 活动类型 |
| campaign_phase | 竞选阶段 |
| verification_status | 核实状态 |
| source_tier | 来源层级 |
"""

if __name__ == "__main__":
    write("README.md", README)
    write("research_gaps.md", GAPS)
    write("_research_conventions.md", CONV)
    write("09_sources/data_dictionary_bilingual.md", DICT)
