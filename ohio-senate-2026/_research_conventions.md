---
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
