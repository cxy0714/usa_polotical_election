---
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
