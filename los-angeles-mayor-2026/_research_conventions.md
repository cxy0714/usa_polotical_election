---
title: "Research Conventions — 2026 Los Angeles Mayoral Case"
title_zh: "研究方法约定 — 2026 年洛杉矶市长案例"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: "Documents the non-obvious encoding decisions a reader or validator cannot infer from the CSVs alone."
---

# Research conventions / 研究方法约定

## 1. Source citation / 来源引用

Every `source_urls` cell holds exactly one `SRC-####|https://…` pair. The validator's pattern admits a
single pair per cell, so corroboration is never stacked inside the cell: it is described in the row's
`notes`, `reliability_notes` or `verification_status`. `09_sources/sources.csv` is the registry; the
`used_by` column lists which datasets cite the source, computed after the tables were built.

每个 `source_urls` 单元格只含一个 `SRC-####|https://…` 对：校验器的正则只接受单对，因此交叉印证
不堆在单元格里，而写入该行的 `notes`、`reliability_notes` 或 `verification_status`。
`09_sources/sources.csv` 是登记表，`used_by` 列在表格建成后计算得出。

## 2. Joint debates are two rows / 联合辩论拆为两行

Five events were joint (both candidates on the same stage). Each gets one row per candidate
(`BAS-EVT-####` and `RAM-EVT-####`) with identical `event_date`, `event_time` and `venue`, and each
row names its counterpart in `analyst_notes` ("Joint event; the Raman counterpart row is …"). This was
chosen over a shared `JNT-EVT-####` id because every downstream query filters by `candidate_id`, and a
neutral id would have dropped out of both filters.

五场联合活动按候选人各建一行（`BAS-EVT-####` 与 `RAM-EVT-####`），日期、时间、场地完全一致，
并在 `analyst_notes` 中互指对方行。之所以不用共享的 `JNT-EVT-####`，是因为所有下游查询都按
`candidate_id` 过滤，中立 id 会在两个过滤条件中同时消失。

## 3. `unknown` is a value, not a zero / `unknown` 是取值，不是零

`unknown` means "no retrieved source establishes this". It is never a stand-in for zero, for "no", or
for a number that could be computed. Numeric columns carry `unknown` where the number was not
published (e.g. `debts_owed` in every finance row, `other_pct` in candidate-only polls). Row-level
absence of a measurable (crowd size, ad duration) is `unknown` even when the qualitative fact is known.

`unknown` 意为"没有已获取来源可以确立此项"，绝不是零、"否"或可计算数值的替代。数字列在未公布时
写 `unknown`（如全部财务行的 `debts_owed`、两选一民调中的 `other_pct`）；可测量值缺失（人数、广告
时长）即使定性事实明确，也记 `unknown`。

## 4. Date conventions / 日期约定

`YYYY-MM-DD` everywhere; `unknown` when only a month or a range is reported. Where a source gives only
a month, the first of the month is recorded **and the row says so** in `notes` or `description`
(e.g. Tulchin's "August 2026" poll → `field_start` 2026-08-01, `field_end` 2026-08-31). Two events are
dated from conflicting text on a single page: the South L.A. forum body says "Saturday" while its photo
caption says Sept. 29; 2026-09-26 is the Saturday consistent with the page's Oct. 3 publication date, so
that date is used and both rows are `conflicting sources`.

统一使用 `YYYY-MM-DD`；只有月份或区间时写 `unknown`。若来源只给月份，则记该月 1 日，**并在
`notes`/`description` 中说明**（如 Tulchin "2026 年 8 月"民调 → `field_start` 2026-08-01、
`field_end` 2026-08-31）。有两处活动日期依据同一页面的矛盾文字：南洛杉矶论坛正文称"星期六"，
图片说明却称 9 月 29 日；与页面 10 月 3 日发布时间相符的星期六是 2026-09-26，故采用该日，
两行均标 `conflicting sources`。

## 5. `period` in campaign_finance / 财务表的 `period`

`period` is the **reported-through** date stamped on the filing aggregate, not a fiscal quarter or an
election cycle. `report_type` carries the cycle and the committee type. Rows whose `report_type`
contains `independent_expenditure` are **not** candidate-committee money: `receipts` there means money
received by the outside committee, `disbursements`/`cash_on_hand`/`debts_owed` are `unknown` because the
aggregate does not publish them, and the candidate named in `candidate_id` is the beneficiary (or, for
`independent_expenditure_against_candidate`, the target).

`period` 是该申报汇总的**截止日**，不是财季或选举周期；周期与委员会类型写在 `report_type` 中。
`report_type` 含 `independent_expenditure` 的行**不是**候选人委员会资金：此时 `receipts` 指外部
委员会收到的款项，`disbursements`/`cash_on_hand`/`debts_owed` 因汇总未公布而记 `unknown`；
`candidate_id` 所指为受益候选人（若为 `…_against_candidate` 则为被针对者）。

## 6. `candidate_id` outside the two principals / 两位主角之外的 `candidate_id`

`case_meta.json` defines `BASS` and `RAMAN`. Three further values appear deliberately: `JOINT` for
shared video and shared coverage rows (used in `speech_video_index.csv` and `media_coverage.csv`),
and `PRATT`, `MILLER`, `HUANG` for field-context rows in `campaign_finance.csv` and
`image_archive.csv`. No filter in the archive assumes exactly two values.

`case_meta.json` 只定义 `BASS` 与 `RAMAN`。另外三个取值是有意引入的：`JOINT` 用于共享视频与共享
报道行（见 `speech_video_index.csv`、`media_coverage.csv`），`PRATT`、`MILLER`、`HUANG` 用于
`campaign_finance.csv` 与 `image_archive.csv` 中的"战场背景"行。档案中没有任何按"仅两个取值"
假设的过滤逻辑。

## 7. Poll fields / 民调字段

`leader` is the candidate ahead, or `tie` when the two published shares are equal; `margin` is the
leader minus the second candidate and is therefore never negative. Published shares sometimes sum to
87–101 because of rounding, omitted undecideds, or two-candidate subsamples; the archive does not
rescale. Each such row states its sum in `notes`, and where a pollster published both an initial and a
"with leaners" line, `notes` records both and the table carries the leaned figure.

`leader` 为领先者，两位公布份额相等时为 `tie`；`margin` 为第一减第二，永不为负。公布份额有时合计
87–101，原因包括四舍五入、未列未决者、或两选一子样本；档案不做归一化。每行在 `notes` 中说明合计，
若民调机构同时公布初始值与"含倾向者"值，`notes` 两者皆记，表内取含倾向值。

## 8. Verification status rules / 核验状态规则

`verified` — an official record, or two independent retrieved sources agree, or the fact is a direct
quotation present in the retrieved page. `partially verified` — one retrieved source only, or a
paywalled page whose lede/headline was all that arrived, or Wikipedia-only. `conflicting sources` —
two retrieved sources disagree on a specific figure or date (the disagreement is recorded in `notes`,
never averaged). `unverified` — published by one campaign and not corroborated at all (kept, labelled).

`verified`——官方记录，或两个独立已获取来源一致，或为已获取页面中的直接引语。`partially verified`——
仅一个已获取来源，或付费墙页面仅得标题/导语，或仅见维基百科。`conflicting sources`——两个已获取
来源在具体数字或日期上不一致（差异写入 `notes`，绝不取平均）。`unverified`——仅一方竞选团队发布、
完全无旁证（保留并标注）。

## 9. Interpretation labels / 解释标签

Any sentence that evaluates rather than reports — staging choices, what an ad "means", why an event was
scheduled — begins with `INTERPRETATION:`. This applies in `analyst_interpretation`,
`observable_function` stay descriptive, and in the Markdown analyses where the label appears inline.
Descriptive columns (`stated_purpose`, `observable_function`, `visual_notes`) never carry inference.

任何评价性而非报道性的句子——活动编排、广告"意味着什么"、为何安排某场活动——一律以
`INTERPRETATION:` 开头。`analyst_interpretation` 如此，Markdown 分析中亦内联标注。
描述性列（`stated_purpose`、`observable_function`、`visual_notes`）不承载推断。

## 10. What is never done / 绝不做的事

No party label other than `Nonpartisan`. No invented venue, crowd size, quote, or number. No HTML in
Markdown. No ranking or scoring of candidates. No image-content claim that was not in the reporting or
the file description — this build could not view image pixels, so visual fields are `unknown` and say
so explicitly. No use of a URL that returned non-200: blocked and paywalled pages appear in
`_staging/fetch_log.csv` and in `research_gaps.md`, never as a source row.

除 `Nonpartisan` 外不使用任何党派标签；不虚构场地、人数、引语或数字；Markdown 中不使用 HTML；
不对候选人排名或打分；不作未见于报道或文件描述的图像内容判断——本次构建无法查看图像像素，
故视觉字段写 `unknown` 并明示原因；非 200 响应的 URL 一律不作来源行，只记入
`_staging/fetch_log.csv` 与 `research_gaps.md`。

## 11. Bilingual rule / 双语规则

Each `##` section is an English block followed by its Chinese counterpart. English governs; the Chinese
is a faithful rendering, not a separate argument. Proper nouns, dataset names and column names stay in
their original form inside Chinese text.

每个 `##` 小节先英文后中文。以英文为准，中文为忠实对译而非另一套论证。专有名词、数据集名与列名
在中文中保持原形。
