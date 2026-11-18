---
title: 2026 U.S. Senate election in Iowa — case archive
title_zh: 2026 年艾奥瓦州联邦参议员选举——案例档案
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Datasets validated with 0 hard failures; thin on county-level primary results, Hinson's own ad creative and Turek's licensed imagery.
---

# 2026 U.S. Senate election in Iowa — case archive / 2026 年艾奥瓦州联邦参议员选举案例档案

## 1. What this archive covers / 本档案覆盖什么

English: The open-seat 2026 U.S. Senate race in Iowa between Josh Turek (D), a state representative and
four-time Paralympian, and Ashley Hinson (R), a three-term U.S. representative. It covers both primaries, the
general election, 34 campaign events, 45 documented policy positions, 16 speech units, 12 images, 5
advertisements, 7 social posts, 28 coverage items, 11 finance rows, 7 result rows, all 99 counties and 11
general-election polls. Nothing outside this race is described.

中文：本档案覆盖 2026 年艾奥瓦州联邦参议员开放席位选举：民主党人 Josh Turek（州众议员、四届残奥选手）对阵共和党人 Ashley Hinson（三届联邦众议员）。涵盖两场初选、大选、34 场竞选活动、45 条政策立场、16 条演说记录、12 张图片、5 条广告、7 条社媒记录、28 条媒体报道、11 条资金记录、7 条结果记录、全部 99 个县以及 11 份大选民调。不描述本场选举之外的任何内容。

## 2. Documented result / 有据可查的结果

| Candidate / 候选人 | Party / 政党 | Votes / 票数 | Share / 得票率 | Winner / 胜出 |
|---|---|---|---|---|
| Josh Turek | Democratic | 688,746 | 50.56 | yes |
| Ashley Hinson | Republican | 631,482 | 46.35 | no |
| Thomas Laehn | Libertarian | 42,109 | 3.09 | no |
| **Total** | | **1,362,337** | **100.00** | |

Margin: 4.21 percentage points. Source: NBC News results feed (`SRC-0002`), identical to the county table's
sum. The race article's election box differs by six votes on the statewide total; see `results_notes.md`.

差距 4.21 个百分点。来源为 NBC 新闻计票数据（`SRC-0002`），与县级数据表合计完全一致。竞赛条目信息框的全州总数与此相差六票，见 `results_notes.md`。

## 3. Five structural facts this archive establishes / 本档案确立的五项结构性事实

**a. The county table reconciles exactly — and it shows a 15-of-99 win.** All 99 counties sum to 688,746 /
631,482 / 42,109 and to 1,362,337, with no residual and no rounding slack. The six-vote gap against the
article's election box is a snapshot difference between two published versions, documented rather than
smoothed. Turek carried only 15 counties — Polk, Linn, Johnson, Scott, Dallas, Black Hawk, Story, Dubuque,
Pottawattamie, Cerro Gordo, Marshall, Muscatine, Des Moines, Jefferson and Winneshiek — and those 15 gave him
466,998 votes to Hinson's 299,323, while the other 84 counties gave Hinson 332,159 to his 221,748. Those
six suburban and university counties alone netted him 151,915 votes — nearly three times his statewide margin of
57,264 — while the other 93 counties netted him -94,651.

**b. The documentary record is asymmetric, not the campaign record.** Turek has more dated events (18 to 14)
but no downloadable official portrait: his four Legislature portraits carry the licence "Copyrighted free
use", which this project does not permit, so they are link-only. Hinson's congressional portraits are public
domain and three were downloaded. The archive can therefore show one candidate's face and not the other's.

**c. Hinson's spoken record is thinner than her schedule.** Five of seven Hinson speech rows are
paraphrase-only, and four of her largest events were carried by surrogates (Cruz twice, Barrasso, Kennedy).
Turek's nine speech rows carry verbatim quotations in eight cases.

**d. Money ran in opposite directions at two 口径.** By 14 October 2026 Turek had out-raised Hinson
$24,290,521 to $14,147,973, while outside spending in the race was reported at $137M, including a $20M Senate
Leadership Fund buy for Hinson. The archive keeps campaign receipts and outside spending as separate rows and
never sums them.

**e. The ad record is one-sided.** Nine advertisement rows exist: seven Turek items (six spots plus a July
endorsement video) and two headline-level outside buys — and **no Hinson campaign ad creative at all**.
The substantive exchange — Turek's "I-35" immigration ad and Hinson's attack on it — is visible only because
the attack was delivered at a fundraiser that a reporter covered. No Hinson campaign ad creative was
retrievable at all.

中文摘要：(a) 99 县合计与全州总数完全吻合，且 Turek 只赢 15 个县却拿下过半选票；(b) 文献记录不对称：Turek 活动更多但无可下载官方肖像，Hinson 有公有领域国会肖像；(c) Hinson 的言语记录比日程更薄，七条演说中五条为转述，四场大型活动由代理人主导；(d) 资金在两个口径上方向相反，本档案从不将竞选收支与外部支出相加；(e) 只有一组广告攻防有详细记录。

## 4. Folder map / 目录结构

```
01_candidates/      policy_positions.csv (45), turek/ and hinson/ each with biography.md,
                    political_positions.md and career_timeline.csv (24 / 17)
02_campaign_events/ campaign_events.csv (34), turek_timeline.md, hinson_timeline.md,
                    event_coverage_gaps.md
03_speeches/        speech_archive.csv (16), speech_video_index.csv (10), two communication analyses
04_visual_archive/  image_archive.csv (12), 4 downloaded files, image_sources_and_licences.md
05_campaign_media/  advertisements.csv (9), social_media.csv (7), media_coverage.csv (29)
06_campaign_finance/campaign_finance.csv (11)
07_electoral_context/ election_results.csv (7), county_results.csv (99), polling.csv (11),
                    election_context.md, results_notes.md
08_comparative_analysis/ candidate_comparison.md
09_sources/         sources.csv (111), data_dictionary_bilingual.md
_staging/           case_meta.json, fetch_log.csv, mirrors/, derivation scripts (d0-d9)
```

## 5. Strong vs thin / 强项与薄弱

| Strong / 强 | Thin / 弱 |
|---|---|
| County-level general-election data, fully reconciled / 县级大选数据，完全吻合 | No county-level primary results / 无县级初选数据 |
| Event chronology for both candidates, 34 rows / 两位候选人的活动年表，34 行 | Crowd detail for only 4 of 34 events / 34 场中仅 4 场有人数记录 |
| Verbatim quotation base for Turek (8 of 9 speeches) / Turek 的原话基础（9 条中 8 条） | Hinson's own ad creative: zero rows out of nine / 九条广告中她本人的素材为零 |
| Finance across 11 committees and 2 snapshots / 11 个委员会、2 个时点的资金数据 | Individual vs PAC contribution splits: unknown / 个人与 PAC 捐款拆分：unknown |
| County-table arithmetic and the six-vote variance explained / 县级算术与六票差异已解释 | Primary polling numbers not retrievable / 初选民调数字未能取得 |

## 6. Validation status / 校验状态

English: `python _tools/validate_case.py iowa-senate-2026` reports **0 hard failures and 0 soft warnings**
across 442 rows and 111 sources. Every `SRC-####` cited in every CSV resolves in `09_sources/sources.csv`, and
every cited URL matches its registered URL.

中文：`python _tools/validate_case.py iowa-senate-2026` 在 442 行、111 个来源上报告 **0 个硬性失败、0 个软警告**。
所有 CSV 中引用的每个 `SRC-####` 均可在 `09_sources/sources.csv` 解析，且所引网址与登记网址一致。

## 7. Reading paths / 阅读路径

- **Result and arithmetic first / 先看结果与算术** → `07_electoral_context/election_results.csv`,
  `county_results.csv`, `results_notes.md`
- **Who these people are / 人物** → `01_candidates/*/biography.md`, then
  `08_comparative_analysis/candidate_comparison.md`
- **What they said / 他们说了什么** → `03_speeches/speech_archive.csv`, then the two
  `communication_analysis_*.md`
- **Where they went / 他们去了哪** → `02_campaign_events/*_timeline.md`
- **What it cost / 花了多少钱** → `06_campaign_finance/campaign_finance.csv`, then
  `07_electoral_context/election_context.md` §3
- **Where the record fails / 记录在哪里失败** → `research_gaps.md`, `event_coverage_gaps.md`
- **Method / 方法** → `_research_conventions.md`, `09_sources/data_dictionary_bilingual.md`

## 8. Known limits stated up front / 先行声明的局限

1. Turek's disability is recorded as a documented biographical fact, never as metaphor, and no source
   retrieved here describes staging, ramps or seating at his events — those fields say `unknown`.
2. Paywalled outlets (Des Moines Register 402, NYT and Politico 403, AP 403, USA Today 402) are logged as
   headline-level sources and marked `unverified` or `partially verified`.
3. No image in this archive was inspected visually; framing and clothing fields are metadata-derived.
4. The archive contains no rankings, scores or grades of the candidates.

## Video and news-photo layer (2026-11-18)

- **News photographs:** 29 credited caption rows added to `04_visual_archive/image_archive.csv` from the archived article HTML. All are `all_rights_reserved_link_only`: article URL, caption and credit are stored, the image is not.
- **Video corpus:** 3 uploaded videos, 37 keyframes, 12/37 frames attributed by SFace against the licensed portraits. Details, method and limits: [`10_video_frames/README.md`](10_video_frames/README.md).
- **Identity distribution:** unknown 25, HINSON 12
- **Still no clothing evidence:** no keyframe was read by a vision model and no harvested caption names clothing, so `clothing_notes` remains `unknown` throughout.

- **新闻照片：** 从存档文章 HTML 新增 29 条带署名的图注记录至 `04_visual_archive/image_archive.csv`。全部为 `all_rights_reserved_link_only`：保存文章 URL、图注与署名，不保存图片。
- **视频语料：** 3 段上传视频、37 张关键帧，SFace 对照授权肖像后归属 12/37 帧。方法、限制与逐视频明细见 [`10_video_frames/README.md`](10_video_frames/README.md)。
- **仍无着装证据：** 没有关键帧被视觉模型读取，已采集图注也没有描述着装，`clothing_notes` 全部保持 `unknown`。
