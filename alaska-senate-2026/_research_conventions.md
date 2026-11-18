---
title: "Alaska 2026 U.S. Senate — research conventions"
title_zh: "阿拉斯加 2026 联邦参议员选举 — 研究方法与约定"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: "Rules actually applied in this case: sourcing, quoting, dating, translation, licensing, and what was refused."
---

# Research conventions / 研究约定

## Sourcing and tiers

Every coded claim points to one source in `09_sources/sources.csv` via `SRC-####|url`. The
contract's one-source-per-cell rule is applied literally: when a row rests on several documents, the
`source_urls` cell carries the strongest one, and `analyst_notes` or `notes` names the corroborating
documents in prose. Sources are tiered as follows.

- **T1** — official records: Alaska Division of Elections (SRC-0001 to SRC-0003), FEC (SRC-0004,
  SRC-0005).
- **T2** — Alaska and national newsrooms of record: ADN, Alaska Public Media, Alaska Beacon, AP,
  CNN, NBC, PBS, ABC, Roll Call, Alaska's News Source, Anchorage Press.
- **T3** — party, campaign, advocacy and reference sources: campaign sites, union and trade-association
  releases, AFP Action, NRA-PVF, Wikipedia, pollsters' own releases, Bluesky.

Partisan-leaning outlets (Must Read Alaska, Alaska Watchman, The Alaska Story) are used only for
statements the campaigns themselves made, and are flagged in `reliability_notes`.

每条编码论断都通过 `SRC-####|url` 指向 `09_sources/sources.csv` 中的一个来源。合同"每格一个来源"的
规则被严格执行：若一行依赖多份文件，`source_urls` 放最强的一份，其余佐证在 `analyst_notes` 或
`notes` 中以文字说明。T1 为官方记录（选举委员会、FEC）；T2 为阿拉斯加与全国主流新闻机构；
T3 为政党、竞选团队、倡议组织、维基百科与民调机构自发布稿件。倾向性媒体仅用于候选人自己的表态，
并在 `reliability_notes` 标注。

## Quotes

A quotation appears only if it was read in a retrieved document. Paraphrase is labelled as paraphrase.
Where two syndications of the same wire story differ, the version that was actually retrieved is
cited (usually PBS or ABC carrying AP). On 2026-11-18 one draft position row was rejected because its
quotation ("I'm a life member of the NRA") could not be found anywhere in the retrieved corpus; it was
replaced with the 2026-07-13 NRA-PVF endorsement statement actually on file (SRC-0068).

只有已在取得的文档中读到的语句才作为引语；转述标注为转述。同一通讯社稿件若有多个转载版本，
引用实际取得的版本（通常是 PBS 或 ABC 转载的 AP 稿）。2026-11-18 有一条政策立场草稿因引语
（"我是 NRA 终身会员"）在全部已取得语料中无法找到而被弃用，改用档案中确有的 2026-07-13
NRA-PVF 背书声明（SRC-0068）。

## `unknown` is a value

Empty cells and placeholder strings are prohibited. Where a fact was not published or not retrieved, the cell
says `unknown`. This is deliberate in three places readers notice first: rally venues, crowd sizes,
and paid-ad creative details. Guessing a venue from a city, or a crowd from "packed", was refused.

禁止空白单元格与占位字符串。凡未公布或未取得的事实，单元格写 `unknown`。读者最先注意到的三处是
集会场地、人数与付费广告素材细节——档案拒绝由城市推断场地，或由"挤满"推断人数。

## Dates

- Full ISO dates (`YYYY-MM-DD`) in date columns; `unknown` when the day is not published.
- Partial dates that a source gives only as a month or year are moved into the prose (a career row
  with `start_date=unknown` and a description reading "September 2023" or "early 2024"), because the
  validator requires full ISO dates and inventing a day would be fabrication.
- A story dated the day after an event and saying "on Friday" is dated to that Friday
  (Sullivan's launch: story 2025-03-22 → event 2025-03-21).
- Report timestamps in official PDFs are quoted verbatim rather than converted.

日期列使用完整 ISO 日期，未公布具体日期时写 `unknown`。来源仅给出月份或年份的部分日期写入正文
（如职业时间线中 `start_date=unknown`、描述写"2023 年 9 月"），因为校验器要求完整 ISO 日期，
臆造某一天即属虚构。事件次日报道称"周五"的，按该周五计日期。官方 PDF 的时间戳原样引用，不作时区换算。

## Translation

English governs. Chinese text is a working translation written to be read alongside the English, not
an independent source. Proper names follow the candidates' own usage (`Mary Peltola` 玛丽·佩尔托拉,
`Dan S. Sullivan` 丹·沙利文); the namesake challenger is 小丹尼尔·沙利文 (`Daniel J. Sullivan Jr.`)
and is never merged with the incumbent in either language.

英文为准。中文是与英文对照阅读的工作译文，不是独立来源。人名为约定译法；同名挑战者始终写作
"小丹尼尔·沙利文"，任何语言版本都不与现任议员混同。

## Retrieval and evidence trail

- Starting point: `_research/2026/alaska.wikitext` (1,514 lines), copied to
  `_staging/mirrors/wiki_alaska.wikitext` and logged.
- Pages fetched with Python `urllib`, explicit User-Agent, saved under `_staging/mirrors/pages/`,
  text-extracted to `_staging/mirrors/text/`, and logged in `_staging/fetch_log.csv`
  (url, http_status, bytes, fetched_at, saved_file). 166+ rows, 32 non-200.
- `elections.alaska.gov` presents a self-signed certificate in its chain; two documents were
  retrieved with `ssl._create_unverified_context()`, recorded in `_staging/tls_fallback.json`, and
  disclosed in `research_gaps.md`.
- No PDF/HTML parsing libraries were available, so mirrors were text-extracted with regex (HTML) and
  zlib + `Tj` operator scanning (PDF). Extraction artifacts (nav chrome, cookie banners) are ignored
  when quoting.

起点为本地维基百科镜像，复制入 `_staging/mirrors/` 并记录。页面用 Python `urllib` 抓取、带明确
User-Agent、存入 `_staging/mirrors/pages/`、抽取文本至 `_staging/mirrors/text/`，并在
`_staging/fetch_log.csv` 逐条记录（url、状态码、字节数、时间、保存文件）。共 166+ 行，其中 32 条
非 200。`elections.alaska.gov` 证书链含自签名证书，两份文件以不校验 SSL 的方式取得，记录于
`_staging/tls_fallback.json` 并在缺口文档中披露。因无 PDF/HTML 解析库，镜像以正则（HTML）与
zlib + `Tj` 扫描（PDF）提取文本；引用时忽略导航栏、Cookie 提示等抽取噪声。

## Images

Only PD, CC0, CC BY and CC BY-SA images were downloaded, each under 2 MB, with licence, photographer
and Commons file page recorded in `image_archive.csv` and in `sources.csv` (SRC-0119 to SRC-0124).
News photographs are indexed `all_rights_reserved_link_only` with the photographer named from the
caption; they are not downloaded or redistributed.

仅下载 PD、CC0、CC BY、CC BY-SA 图像，单文件均小于 2 MB，许可、摄影者与 Commons 文件页记录于
`image_archive.csv` 与 `sources.csv`（SRC-0119 至 SRC-0124）。新闻照片以
`all_rights_reserved_link_only` 索引，摄影者按图片说明记录，不下载、不再分发。

## Attendance and status

An event is `held` only when a retrieved report places the candidate there. Endorsement releases are
`announced`, not `held`. AFN convention rows are `unverified` placeholders because no retrieved
report documents attendance. A written statement is recorded under `victory_speech` only with
`event_status=unverified` and no venue asserted.

只有已取得报道明确显示候选人到场时，事件才标 `held`。背书新闻稿标 `announced` 而非 `held`。
AFN 大会相关行因无报道证明出席，标 `unverified` 占位。书面声明仅在 `event_status=unverified`
且不指认场地的前提下记入 `victory_speech`。

## Refusals

- No mapping of Alaska house districts to "counties".
- No assignment of the namesake candidate's votes to Sullivan in the official table; the transfer is
  computed only as a labelled counterfactual in `results_notes.md`.
- No claim that ranked-choice tabulation occurred.
- No inference of a concession that did not happen.
- No use of a source that returned 403/401/404 as if it had been read.

- 不把阿拉斯加众议院选区映射为"县"。
- 官方结果表中不把同名候选人票数并入沙利文；仅在 `results_notes.md` 中作为标注的反事实计算。
- 不声称发生过排序复选计票。
- 不推断未曾发生的认输。
- 不把返回 403/401/404 的来源当作已读材料使用。
