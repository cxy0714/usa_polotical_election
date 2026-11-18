---
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
media, finance, electoral context) holding 418 data rows in total, 195 catalogued sources, 21
bilingual documents, and 15 downloaded image files. Every retrieval is logged in
`_staging/fetch_log.csv` with its HTTP status and byte count.

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

Vote counts are the article's canvass table (SRC-1006); the percentages are those printed
there and they sum to 100.01 after rounding, which is discussed in
`07_electoral_context/results_notes.md`. A law-firm election newsletter, which the article cites
as its own results source, gives Husted 45.15% and Levy 2.05% instead (SRC-1182); since
2,080,064 / 4,604,860 = 45.171% and 93,786 / 4,604,860 = 2.037%, the vote counts settle the
argument in favour of the article's 45.17% and 2.04%, and the newsletter's figures are recorded
as a source conflict rather than smoothed over.

上表票数取自条目中的计票表；条目自身打印的百分比四舍五入后合计为100.01%，该差异在
`results_notes.md` 中说明。一家律所选举通讯给出的赫斯特德得票率为45.15%、利维为2.05%，
这一冲突已记录而非被抹平。

## 3. Structural facts this archive establishes / 本档案确立的结构性事实

**1. The appointment, not the election, created the incumbency.** Vance resigned effective
2025-01-10; Gov. Mike DeWine announced Husted's appointment on 2025-01-17 and Husted took the
oath on 2025-01-21 (SRC-1016,
SRC-1178). Every "incumbent" label in this archive is dated to those two days.
The task brief's "appointed 2025-01-10 / sworn in 2025-01-14" matches neither the resignation
date nor any retrieved record, and is corrected here.

**2. Money ran one way and the polls did not.** Through 2026-09-30 Brown had raised
$68,409,200 to Husted's $19,894,786 (SRC-1006), yet the race was rated a toss-up all year
and the final margin was 4.84 points. Total spending in the race passed $500 million
(SRC-1074), of which outside groups accounted for more than $325 million by AdImpact's count
(SRC-1026), so candidate receipts were a minority of the money in the race.

**3. Data centers became the sleeper issue.** A leaked NRSC memo called data centers "the anchor
hanging around Husted's neck" and the race "a dead heat" (SRC-1028).
Brown built his closing argument on Husted's recruitment of them — despite having praised an
Amazon data center in a 2015 release (SRC-1081).

**4. Labour split rather than labour consolidation.** Brown held the UAW, Steelworkers, IUPAT,
IFPTE, CWA, the Ohio Federation of Teachers and the Ohio AFL-CIO; Husted took the Operating
Engineers, Boilermakers, Cleveland Building Trades, ABC of Ohio and the state FOP
(SRC-1054,
SRC-1101,
SRC-1062). A Republican carrying
building trades and the Boilermakers is the unusual part.

**5. A split-ticket state.** Brown won 50.01% in a state Trump carried three times, and
Democrats swept the Ohio governor, secretary of state and treasurer races in the same election
(SRC-1006). The Senate result was part of a state-level Democratic wave, not an isolated
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
finance asymmetry; the issue positions, because a Columbus Dispatch issue survey carried by
Yahoo News was retrieved in full and quotes both candidates at length on affordability, tariffs,
Medicaid, data centers, immigration and the SAVE Act (SRC-1081); the union and county-party
endorsement record.

Thin: county-level results (no table exists in the article — only two SVG maps, and the Ohio
Secretary of State canvass spreadsheets returned 403, so `county_results.csv` is header-only);
any joint debate (nothing in the retrieved corpus documents one); crowd sizes (almost never
reported); speech transcripts (no campaign publishes them, and the video pages that would carry
them returned 403); television advertising (no ad video URLs were retrievable except one
2026-10-29 vertical video, so seven of the eight ad rows are documented through reporting, a
fact-check or a sponsor's own release rather than from the creative).

强项：结果算术及其内部矛盾、任命时间线、筹款不对称、议题立场（两阵营均回答了结构化议题问卷且全文可获取）、
工会与县党 endorsement 记录。薄弱：县级结果（条目仅有地图SVG、无表格）、联合辩论（现有语料无任何记载）、
现场人数（几乎无报道）、演讲全文（无竞选发布，视频页403）、电视广告（广告链接不可得，8条中6条依据报道而非广告本身）。

## 6. Validation status / 校验状态

`python _tools/validate_case.py ohio-senate-2026` reports **0 hard failures and 0 soft
warnings**. Every place where the archive is short of a target is listed with its cause in
`research_gaps.md`. No cell contains a placeholder; `unknown` is used as a value wherever the
retrieved record does not state the fact.

校验脚本报告 **0 个硬失败**。其余软警告及所有未达目标的项均在 `research_gaps.md` 中列明原因。
所有单元格均无占位符；凡检索记录未载明的事实一律填 `unknown`。

## 7. Reading paths / 阅读路径

1. Result first: `07_electoral_context/results_notes.md` → `election_results.csv` → `polling.csv`.
2. Why it happened: `08_comparative_analysis/candidate_comparison.md` → `policy_positions.csv`.
3. How it was fought: `02_campaign_events/campaign_events.csv` → `05_campaign_media/media_coverage.csv`.
4. Money: `06_campaign_finance/campaign_finance.csv` → `06_campaign_finance/finance_notes.md` → SRC-1074 (total-spending context).
5. Method and provenance: `_research_conventions.md` → `09_sources/sources.csv`.

## 8. Provenance note / 来源说明

`sources.csv` holds 195 entries, all retrieved on 2026-11-18 and mirrored under `_staging/`
with a row in `_staging/fetch_log.csv` recording status and byte count. Sources that returned
403/402 (AP, Politico, the Ohio Secretary of State, several TV stations) are recorded in the
fetch log as failures and are **not** cited as content; where their reporting was needed, a
syndicated mirror that did load is cited instead and the substitution is stated in
`reliability_notes`.

`sources.csv` 收录195条来源，均于2026-11-18抓取并镜像保存，抓取日志记录状态与字节数。
返回403/402的来源仅作为失败记录，绝不作为内容引用；确需其报道时改用可访问的转载版本，并在
`reliability_notes` 中说明替换关系。
