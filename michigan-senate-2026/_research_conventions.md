---
title: Research conventions for this case
title_zh: 本案例的研究约定
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Identifier, tiering, verification and bilingual rules as applied in this case, including the deviations that a future reader must know about.
---

## Scope of work

This archive was built inside `michigan-senate-2026/` only. Shared files under `_research/2026/` were read; no other case folder, no `site/` file and no `_tools/` file was modified. No HTML was produced, and no website build was run.

中文：本档案仅在 `michigan-senate-2026/` 内构建。仅读取了 `_research/2026/` 下的共享文件；未修改任何其他案例目录、`site/` 文件或 `_tools/` 文件。未生成任何 HTML，也未运行网站构建。

## Identifiers

Events use `ELS-EVT-####` and `ROG-EVT-####`; speeches `ELS-SPC-####` / `ROG-SPC-####`; ads `ELS-AD-####` / `ROG-AD-####` with outside spending taking `EXT-AD-####`; images `ELS-IMG-####` / `ROG-IMG-####`; social posts `ELS-SOC-####` / `ROG-SOC-####`; coverage `COV-####`; finance `ELS-FIN-####` / `ROG-FIN-####`; positions `ELS-POS-####` / `ROG-POS-####`; career entries `ELS-CAR-####` / `ROG-CAR-####`; video `ELS-VID-####` / `ROG-VID-####`. Sources use a single `SRC-####` sequence across the case, assigned in registry order and never reused. The three-letter candidate code is `ELS` and `ROG`; no collision occurred, so no four-letter variant was needed.

中文：事件使用 `ELS-EVT-####` 与 `ROG-EVT-####`；演说 `ELS-SPC-####` / `ROG-SPC-####`；广告 `ELS-AD-####` / `ROG-AD-####`，外部支出用 `EXT-AD-####`；影像 `ELS-IMG-####` / `ROG-IMG-####`；社交帖文 `ELS-SOC-####` / `ROG-SOC-####`；报道 `COV-####`；财务 `ELS-FIN-####` / `ROG-FIN-####`；立场 `ELS-POS-####` / `ROG-POS-####`；年表 `ELS-CAR-####` / `ROG-CAR-####`；视频 `ELS-VID-####` / `ROG-VID-####`。来源使用全案例唯一的 `SRC-####` 序列，按登记表顺序分配，绝不重复使用。三位候选人代号为 `ELS` 与 `ROG`，无冲突，故无需四字母变体。

## One source per cell, corroboration in the notes

Contract §1 allows exactly one `SRC-####|https://…` pair in a `source_urls` cell, and the validator compares that URL against the registry, so every CSV cell carries its single primary source. Where a row rests on more than one source, the corroborating material is named in a prose column (`analyst_notes`, `notes`, `reliability_notes` or `fact_check`) and both sources appear in that source's `used_by` list. This is why a row can be `verified` while its `source_urls` cell names only one outlet: the second outlet is in the note.

中文：合同 §1 规定 `source_urls` 单元格只能有一个 `SRC-####|https://…` 对，且校验脚本会将该 URL 与登记表比对，因此每个 CSV 单元格只携带其唯一主来源。若某行依赖多个来源，佐证材料在文字列（`analyst_notes`、`notes`、`reliability_notes` 或 `fact_check`）中指名，且两个来源都会出现在各自来源的 `used_by` 列表中。这就是为何某行可以标为 `verified`，而其 `source_urls` 只写一家媒体：第二家写在注释里。

## Tier assignment is mechanical

`T1` — government domains (`michigan.gov`, `miboecfr`, `fec.gov`, `senate.gov`, `congress.gov`), a campaign's own site, and a trade association announcing its own endorsement. `T2` — established outlets with editorial standards, including specialised ones (Jewish Insider, Bridge Michigan, MLive, Michigan Advance, Crain's). `T3` — Wikipedia, without exception, even where the content is correct. A tier was never raised because a source happened to agree with another source.

中文：`T1`——政府域名（`michigan.gov`、`miboecfr`、`fec.gov`、`senate.gov`、`congress.gov`）、竞选方自身网站、以及行业协会宣布自身背书。`T2`——具备编辑标准的成熟媒体，包括专业媒体（Jewish Insider、Bridge Michigan、MLive、Michigan Advance、Crain's）。`T3`——维基百科，无一例外，即便其内容正确。绝不因某来源恰好与其他来源一致而提升其层级。

## The verification ladder as used here

`verified` requires the fact to be readable first-hand in the primary source: a debate passage printed by the outlet that covered the debate, an official candidate listing, a file's own metadata. `partially verified` is used whenever the fact arrived through an intermediary — most finance figures (Wikipedia citing the FEC, whose own page is JavaScript-rendered), most polls (the Wikipedia table), and every election result (state pages returned 403). `conflicting sources` is used where two retained sources disagree and neither is preferred: the Mitchell Research poll of October 1, and Rogers' post-election statement. `unverified` is used where a fact is asserted without a retrievable account: the AIPAC fundraisers' date, the candidate advertising rows.

中文：`verified` 要求该事实可在一手来源中直接读到：报道该辩论的媒体刊出的段落、官方候选人名录、文件自身元数据。凡经中间环节取得，即用 `partially verified`——多数财务数字（维基百科转引 FEC，而 FEC 自身页面为 JavaScript 渲染）、多数民调（维基百科表格）、以及全部选举结果（州级页面返回 403）。两份保留来源互相矛盾且均不优先时用 `conflicting sources`：10 月 1 日的 Mitchell Research 民调，以及罗杰斯的选后声明。仅被主张而无可取得记述时用 `unverified`：AIPAC 筹款会的日期、候选人广告相关行。

## Dates, `unknown`, and refusing to round

Dates are ISO. Where a source gives only a year, the cell holds the year's first day and the uncertainty is stated in a note — the alternative, `unknown`, is used only when no date at all is available. Birth dates and event dates are never inferred from context. `unknown` is a legal value in every text column and is used instead of `0`, `N/A` or `TBD`; a percentage is never written as `0` to mean "not tested".

中文：日期一律 ISO。若来源仅给出年份，单元格写该年第一天，并在注释中说明不确定性——只有在完全没有任何日期时才用 `unknown`。出生日期与事件日期绝不依据上下文推断。`unknown` 在所有文本列中均为合法值，用以替代 `0`、`N/A` 或 `TBD`；绝不以 `0` 表示“未测试”的百分比。

## The `local` row in the fetch log

`_staging/fetch_log.csv` records HTTP retrievals with `url,http_status,bytes,fetched_at,saved_file`. One row has `http_status` = `local`: the Wikipedia wikitext mirror copied from `_research/2026/michigan.wikitext` into `_staging/mirrors/wiki_michigan.wikitext`. It is marked `local` rather than given a fake 200 so the log stays truthful about what was fetched over the network and what was copied from the repository.

中文：`_staging/fetch_log.csv` 以 `url,http_status,bytes,fetched_at,saved_file` 记录 HTTP 抓取。其中一行 `http_status` 为 `local`：从 `_research/2026/michigan.wikitext` 复制到 `_staging/mirrors/wiki_michigan.wikitext` 的维基百科维基文本镜像。标为 `local` 而非伪造 200，以使日志如实区分“通过网络抓取”与“从仓库复制”。

## Outside money is never summed with committee money

`06_campaign_finance/campaign_finance.csv` keeps two accounting families in separate rows: candidate-committee receipts and disbursements (FEC basis) and independent expenditures (AdImpact, FEC IE filings or press tallies). No row, note or markdown document adds them together. Where a total is quoted — the $243 million race total — the source and its basis are named and the figure is explicitly excluded from the FEC totals [SRC-0073].

中文：`06_campaign_finance/campaign_finance.csv` 将两类核算分开存放：候选人委员会的收支（FEC 口径）与独立支出（AdImpact、FEC 独立支出申报或媒体统计）。任何行、注释或 Markdown 文档都不将二者相加。引用总额时——如 2.43 亿美元的选举总额——均注明来源与口径，并明确将其排除在 FEC 总额之外 [SRC-0073]。

## Inference is always labelled

`analyst_interpretation` cells begin with the literal token `INTERPRETATION:` and nothing else in the event file is allowed to read as inference. In markdown, interpretive passages are bounded by the paragraph that states the underlying fact, and any sentence beginning "INTERPRETATION" or "This suggests" is followed by the evidence it rests on. No crowd size, venue, quote, dollar figure or date was invented to fill a gap; where a gap existed it was left as `unknown` and written up in `research_gaps.md`.

中文：`analyst_interpretation` 单元格恒以字面标记 `INTERPRETATION:` 开头，事件文件中其他任何内容都不得读作推断。在 Markdown 中，解释性段落由其陈述事实的段落界定；任何以“INTERPRETATION”或“这表明”开头的句子后均附其所依据的证据。绝不为填补缺口而虚构人数、场地、引语、金额或日期；存在缺口时一律留为 `unknown`，并写入 `research_gaps.md`。

## Chinese text and file encoding

Every file in this case is UTF-8 without BOM, written through Python with an explicit `encoding="utf-8"`. PowerShell string cmdlets were avoided for content work because they mangle Chinese text on this machine. Percentages and dates inside Chinese sentences are kept in the same form as the English so that the two can be diffed mechanically.

中文：本案例所有文件均为无 BOM 的 UTF-8，通过 Python 以显式 `encoding="utf-8"` 写入。内容处理中避免使用 PowerShell 的字符串命令，因为其在本机上会破坏中文文本。中文句子中的百分比与日期保持与英文相同的写法，以便二者可被机械比对。

## Build scripts

The data was emitted by scripts in `_staging/_work/`: `b_common.py` holds the 87-source registry and the CSV writer that enforces header order, fills `unknown` and reconstructs each source's `used_by`; `b1.py` writes positions, careers and events; `b2.py` writes speeches, video index and images; `b3.py` writes media, finance, results and polling; `b4_sources.py` regenerates `09_sources/sources.csv` by scanning every file in the case for `SRC-####` citations. Scripts are not part of the deliverable but are retained so the archive can be rebuilt.

中文：数据由 `_staging/_work/` 中的脚本生成：`b_common.py` 保存 87 个来源的登记表，以及强制表头顺序、填充 `unknown` 并重建每个来源 `used_by` 的写入函数；`b1.py` 写入立场、年表与事件；`b2.py` 写入演说、视频索引与影像；`b3.py` 写入媒体、财务、结果与民调；`b4_sources.py` 通过扫描案例内所有文件中的 `SRC-####` 引用来重新生成 `09_sources/sources.csv`。脚本不属交付物，但予保留以便档案可重建。
