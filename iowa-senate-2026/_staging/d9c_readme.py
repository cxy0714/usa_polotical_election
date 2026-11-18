# -*- coding: utf-8 -*-
"""README.md, research_gaps.md, _research_conventions.md"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CASE, KEY

K = lambda k: KEY[k]


def put(rel, text):
    io.open(os.path.join(CASE, rel), "w", encoding="utf-8", newline="\n").write(text)


put("README.md", """---
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
general election, 33 campaign events, 44 documented policy positions, 16 speech units, 12 images, 5
advertisements, 7 social posts, 28 coverage items, 11 finance rows, 7 result rows, all 99 counties and 11
general-election polls. Nothing outside this race is described.

中文：本档案覆盖 2026 年艾奥瓦州联邦参议员开放席位选举：民主党人 Josh Turek（州众议员、四届残奥选手）对阵共和党人 Ashley Hinson（三届联邦众议员）。涵盖两场初选、大选、33 场竞选活动、44 条政策立场、16 条演说记录、12 张图片、5 条广告、7 条社媒记录、28 条媒体报道、11 条资金记录、7 条结果记录、全部 99 个县以及 11 份大选民调。不描述本场选举之外的任何内容。

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

**a. The county table reconciles exactly.** All 99 counties sum to 688,746 / 631,482 / 42,109 and to
1,362,337 — no residual, no rounding slack. The six-vote gap against the article's election box is a
snapshot difference between two published versions, documented rather than smoothed.

**b. The documentary record is asymmetric, not the campaign record.** Turek has more dated events (17 to 14)
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

**e. Only one ad exchange is documented in detail.** Five advertisement rows exist: three Turek spots and two
headline-level outside buys. The substantive exchange — Turek's "I-35" immigration ad and Hinson's attack on
it — is visible only because the attack was delivered at a fundraiser that a reporter covered.

中文摘要：(a) 99 县合计与全州总数完全吻合；(b) 文献记录不对称：Turek 活动更多但无可下载官方肖像，Hinson 有公有领域国会肖像；(c) Hinson 的言语记录比日程更薄，七条演说中五条为转述，四场大型活动由代理人主导；(d) 资金在两个口径上方向相反，本档案从不将竞选收支与外部支出相加；(e) 只有一组广告攻防有详细记录。

## 4. Folder map / 目录结构

```
01_candidates/      policy_positions.csv (44), turek/ and hinson/ each with biography.md,
                    political_positions.md and career_timeline.csv (24 / 17)
02_campaign_events/ campaign_events.csv (33), turek_timeline.md, hinson_timeline.md,
                    event_coverage_gaps.md
03_speeches/        speech_archive.csv (16), speech_video_index.csv (10), two communication analyses
04_visual_archive/  image_archive.csv (12), 4 downloaded files, image_sources_and_licences.md
05_campaign_media/  advertisements.csv (5), social_media.csv (7), media_coverage.csv (28)
06_campaign_finance/campaign_finance.csv (11)
07_electoral_context/ election_results.csv (7), county_results.csv (99), polling.csv (11),
                    election_context.md, results_notes.md
08_comparative_analysis/ candidate_comparison.md
09_sources/         sources.csv (108), data_dictionary_bilingual.md
_staging/           case_meta.json, fetch_log.csv, mirrors/, derivation scripts (d0-d9)
```

## 5. Strong vs thin / 强项与薄弱

| Strong / 强 | Thin / 弱 |
|---|---|
| County-level general-election data, fully reconciled / 县级大选数据，完全吻合 | No county-level primary results / 无县级初选数据 |
| Event chronology for both candidates, 33 rows / 两位候选人的活动年表，33 行 | Crowd and venue detail for only 11 of 33 events / 33 场中仅 11 场有人数或场地细节 |
| Verbatim quotation base for Turek (8 of 9 speeches) / Turek 的原话基础（9 条中 8 条） | Hinson's own ad creative: zero rows / Hinson 本人的广告素材：零记录 |
| Finance across 11 committees and 2 snapshots / 11 个委员会、2 个时点的资金数据 | Individual vs PAC contribution splits: unknown / 个人与 PAC 捐款拆分：unknown |
| County-table arithmetic and the six-vote variance explained / 县级算术与六票差异已解释 | Primary polling numbers not retrievable / 初选民调数字未能取得 |

## 6. Validation status / 校验状态

English: `python _tools/validate_case.py iowa-senate-2026` reports **0 hard failures**. The only soft warning
is `advertisements.csv: 5 rows, target 6`, explained in `research_gaps.md` (gap 6). Every `SRC-####` cited in
every CSV resolves in `09_sources/sources.csv`, and every cited URL matches its registered URL.

中文：`python _tools/validate_case.py iowa-senate-2026` 报告 **0 个硬性失败**。唯一软警告为
`advertisements.csv: 5 rows, target 6`，已在 `research_gaps.md` 第 6 项说明。所有 CSV 中引用的每个
`SRC-####` 均可在 `09_sources/sources.csv` 解析，且所引网址与登记网址一致。

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
""")

put("research_gaps.md", """---
title: Research gaps
title_zh: 研究缺口
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Eleven gaps, each with its cause and the specific step that would close it; one is the source of the only validator warning.
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

## 6. Only five advertisement rows (validator soft warning)

**Gap / 缺口**: Target is 6; the archive ships 5. This is the only soft warning the validator raises. / 目标为 6 条，本档案交付 5 条；这是校验器唯一的软警告。
**Cause / 原因**: The race's ad record is thin in retrievable text: outside spending is reported at
headline level and the campaigns' creative was not published in the pages fetched. / 可读文本中的广告记录本就稀薄：外部支出只有标题级报道，竞选素材未出现在已抓取页面中。
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
""")

put("_research_conventions.md", """---
title: Research conventions applied in this case
title_zh: 本案采用的研究规范
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Rules that governed every row: sourcing, the unknown value, verification ladder, licences, arithmetic and interpretation marking.
---

# Research conventions / 研究规范

## 1. One source per row / 每行一个来源

English: Every CSV row carries exactly one `SRC-####|https://…` pair in `source_urls`. Where an assertion
rests on two pages, the row cites the page that carries the assertion and the second page appears in
`reliability_notes` or `notes`. Joining two ids with a semicolon is forbidden because the validator cannot
resolve it.

中文：每个 CSV 行的 `source_urls` 恰好一组 `SRC-####|https://…`。若某判断依赖两个页面，该行引用承载该判断的页面，
另一个页面写入 `reliability_notes` 或 `notes`。禁止用分号拼接两个编号，因为校验器无法解析。

## 2. `unknown` is a value / `unknown` 是一个值

English: A cell never goes blank and never gets a plausible guess. `unknown` means "no retrieved source
establishes this". It appears in 100+ cells, concentrated in crowd sizes, venue detail, ad lengths, image
framing and finance sub-totals. `None`, `N/A`, `-` and `TBD` are banned by the validator and were removed
wherever they appeared.

中文：单元格不得留空，也不得填入看似合理的猜测。`unknown` 表示"已抓取来源无法确认"。它在 100 多个单元格中出现，
集中于人数、场地细节、广告时长、图片构图与资金分项。`None`、`N/A`、`-`、`TBD` 被校验器禁止，已全部清除。

## 3. Verification ladder / 核实阶梯

| Status / 状态 | Meaning / 含义 |
|---|---|
| `verified` | At least one T1/T2 source states the fact directly and it is not contradicted / 至少一个 T1/T2 来源直接陈述且无矛盾 |
| `partially verified` | Stated by a T3 source, or stated at headline level behind a paywall, or the quotation is truncated / 由 T3 来源陈述，或付费墙后的标题级陈述，或引文被截断 |
| `unverified` | Recorded from a single weak or headline-only source with no corroboration / 仅有单一薄弱或仅标题来源，无旁证 |
| `conflicting sources` | Two sources state incompatible facts; both are recorded / 两个来源陈述互不相容的事实，二者均记录 |

English: Wikipedia-only evidence is never upgraded past `partially verified`. That rule is why the finance
rows (reproduced from an FEC table via the article) and the four link-only Turek portraits are marked as they
are.

中文：仅有维基百科支撑的证据绝不升级到 `partially verified` 以上。资金行（经条目转载的 FEC 表格）与四张仅链接的
Turek 肖像之所以如此标注，正是这条规则的结果。

## 4. Dates and times / 日期与时间

English: Dates are ISO `YYYY-MM-DD` or `unknown`; year-only or month-only evidence becomes `unknown` with the
raw string in `notes`. `event_time` is local `HH:MM` or `unknown` — publication timestamps were never copied
into `event_time`, because a story filed at 6:05 pm does not mean the event began then.

中文：日期一律 ISO 或 `unknown`；只有年份或月份的証据写 `unknown`，原始字符串放入 `notes`。`event_time` 为当地
`HH:MM` 或 `unknown`——绝不把稿件发布时间当作活动开始时间（下午 6:05 发稿不等于活动 6:05 开始）。

## 5. Interpretation is marked / 解读必须标注

English: Any sentence that reads the record rather than reports it begins `INTERPRETATION:`. This applies in
`analyst_interpretation`, in the comparison memo and in the communication analyses. Unmarked text asserts
only what a source states.

中文：凡对记录作出解读而非陈述的句子，一律以 `INTERPRETATION:` 开头。该规则适用于 `analyst_interpretation`、
比较报告与传播分析。未标注的文字只陈述来源所述内容。

## 6. No grades, no rankings / 不做评分与排序

English: No row scores a candidate, rates a performance or ranks the two. `framing_of_candidate` describes
tone in words ("sympathetic, biography-led"); it does not assign a number. The NRA-PVF ratings page was
retrieved but its candidate grades did not render, so no grade is recorded anywhere.

中文：任何行都不为候选人评分、评级或排序。`framing_of_candidate` 用文字描述语气（"同情式、传记主导"），不给数字。
NRA-PVF 评分页虽已抓取，但候选人评级未渲染，因此档案中不记录任何评级。

## 7. Disability as fact / 残疾作为事实

English: Turek's spina bifida, wheelchair use and surgical history are recorded exactly as sources state
them — including that he attributes the condition to his father's Agent Orange exposure, which is his
attribution, not an established cause. The archive never uses the disability as an argument, a metaphor or a
proxy for policy positions, and never infers physical capability at any event.

中文：Turek 的脊柱裂、轮椅使用与手术史严格按来源陈述记录——包括他将病因归于父亲在越南接触橙剂，这是他的自述，
而非已确立的因果。档案绝不把残疾当作论据、隐喻或政策立场的代理，也绝不推断其在任何活动中的体能。

## 8. Images / 图片

English: Only public domain, CC0, CC BY or CC BY-SA files are downloaded, and each downloaded file is kept
under 2 MB by requesting a scaled thumbnail. Licence, photographer and Commons file page are recorded per row.
"Copyrighted free use" is not on the list, which is why Turek's Legislature portraits are link-only.

中文：仅下载公有领域、CC0、CC BY 或 CC BY-SA 文件，并通过请求缩放缩略图把每个文件控制在 2 MB 以下。逐行记录授权、
摄影师与共享资源文件页。"Copyrighted free use" 不在允许清单内，因此 Turek 的州议会肖像仅记录链接。

## 9. Money 口径 / 资金口径

English: Campaign receipts (FEC) and outside spending (press-reported) are separate rows and are never summed.
The finance rows reproduce an FEC summary table; the outside-spending figures are headline-level and marked
`unverified`.

中文：竞选收支（FEC）与外部支出（媒体报道）分列不同行，从不相加。资金行转载 FEC 汇总表；外部支出数字为标题级，
标注 `unverified`。

## 10. Arithmetic / 算术

English: Percentages are either published values or recomputed from raw votes, and the row says which.
Reconciliation failures are recorded, not repaired: the six-vote statewide difference between the NBC feed and
the article's election box is written down in `results_notes.md` and both numbers survive.

中文：百分比要么是来源公布值，要么由原始票数重算，行内注明属于哪一种。核对失败只记录、不修补：NBC 数据与条目
选举信息框之间六票的全州差异写入 `results_notes.md`，两个数字都保留。

## 11. Naming and ids / 命名与编号

English: Row ids follow contract §5: `TUR-`, `HIN-` and `JNT-` prefixes with a four-digit sequence, and
`COV-####` / `SRC-####` / `POLL-####` sequences. `candidate_id` uses the case_meta ids `TUREK` and `HINSON`.
Finance ids use three-letter candidate prefixes (`TUR-FIN-0001`), extended to non-nominee committees
(`CAR-FIN-0001` for Carlin) because those rows document the primary.

中文：行编号遵循合同第 5 节：`TUR-`、`HIN-`、`JNT-` 前缀加四位序号，以及 `COV-####`／`SRC-####`／`POLL-####` 序列。
`candidate_id` 使用 case_meta 中的 `TUREK` 与 `HINSON`。资金编号用三字母前缀（`TUR-FIN-0001`），并扩展到非提名人的
委员会（Carlin 用 `CAR-FIN-0001`），因为这些行记录的是初选。

## 12. Fetch logging / 抓取记录

English: Every URL requested — including the ones that failed — is in `_staging/fetch_log.csv` with status and
byte count. 140 of 200 requested URLs returned HTTP 200; the rest are 402/403/429 or JavaScript shells, and
each one that mattered is named in `research_gaps.md`.

中文：每一个被请求的网址（包括失败的）都记录在 `_staging/fetch_log.csv`，含状态码与字节数。200 个请求网址中
140 个返回 200，其余为 402/403/429 或 JavaScript 壳；凡重要的失败均已在 `research_gaps.md` 点名。
""")
print("d9c done")
