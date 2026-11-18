---
title: Data dictionary (bilingual)
title_zh: 数据字典（双语）
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Every file and every non-obvious column is defined; trivial columns are grouped rather than glossed individually.
---

## Conventions that apply to every file

All CSVs are UTF-8 without BOM, RFC-4180 quoted, with `\n` line endings and the exact header order fixed by the case contract. No cell is blank: unknown values are the literal string `unknown`, never `0`, `N/A` or an empty string. Amounts are plain integers in U.S. dollars; percentages are bare numbers such as `52.54` with no `%` sign; all dates are ISO `YYYY-MM-DD`. Multiple values inside one cell are pipe-delimited. `source_urls` cells always take the form `SRC-####|https://…`, and the id resolves to a row in `09_sources/sources.csv`.

中文：所有 CSV 均为无 BOM 的 UTF-8、RFC-4180 引号规则、`\n` 换行，并严格遵循案件合同规定的表头顺序。任何单元格都不留空：未知值一律写为字面量 `unknown`，绝不用 `0`、`N/A` 或空字符串。金额为美元整数；百分比为不带 `%` 号的纯数字（如 `52.54`）；日期一律 ISO `YYYY-MM-DD`。单元格内多值以竖线分隔。`source_urls` 单元格格式恒为 `SRC-####|https://…`，其编号可在 `09_sources/sources.csv` 中解析。

### The five verification values / 五种核验状态

| Value / 取值 | Meaning / 含义 |
|---|---|
| `verified` | Read directly in a source that reports it first-hand (a debate transcript passage, an official listing, a photograph's own metadata) / 在直接报道该事实的一手来源中读到（辩论逐字段落、官方名录、照片自身元数据） |
| `partially verified` | Present in a reliable source but reached indirectly — e.g. a figure cited by Wikipedia to the state, or a quote quoted by a second outlet / 出现在可靠来源中但为间接获得，例如维基百科转引州政府数字，或二手媒体转引的引语 |
| `unverified` | Asserted somewhere but no retrieved source establishes it / 有材料提及，但已取得的来源无法证实 |
| `conflicting sources` | Two retrieved sources disagree; both are recorded and neither is chosen / 两份已取得来源互相矛盾；两者均记录，不作取舍 |
| `unknown` | Not established at all / 完全未确定 |

中文：上表定义本档案使用的五种核验状态。`verified` 指直接在报道该事实的一手来源中读到；`partially verified` 指见于可靠来源但为间接获取；`unverified` 指仅被提及而无法证实；`conflicting sources` 指两份来源互相矛盾且均保留；`unknown` 指完全未确定。

### Source tiers / 来源层级

`T1` is official or primary (government, FEC, a campaign's own release, a trade association announcing its own endorsement). `T2` is established independent media. `T3` is supplementary — Wikipedia is always `T3`, assigned mechanically by domain and never upgraded because the content is agreeable.

中文：`T1` 为官方或一手来源（政府、联邦选举委员会、竞选方自身发布、行业协会宣布自身背书）。`T2` 为成熟的独立媒体。`T3` 为补充性来源——维基百科恒为 `T3`，按域名机械判定，绝不因内容“看起来可信”而升级。

## `09_sources/sources.csv` — the source registry / 来源登记表

Twelve columns: `source_id`, `url`, `title`, `publisher`, `publication_date`, `event_date`, `access_date`, `source_tier`, `source_type`, `relevant_quote_or_info`, `reliability_notes`, `used_by`.

`relevant_quote_or_info` holds one short factual line that is actually present in the page (≤200 characters) — never a paraphrase of what the page is about. `used_by` lists the file paths and row ids that cite the source, derived mechanically by scanning the archive rather than maintained by hand.

中文：共十二列。`relevant_quote_or_info` 存放该页面中确实存在的一行简短事实（不超过 200 字符），绝非对页面主题的转述。`used_by` 列出引用该来源的文件路径与行号，由扫描整个档案机械生成，而非手工维护。

## `01_candidates/policy_positions.csv` — positions / 立场

`issue` must be one of `Economy|Healthcare|Education|Immigration|Abortion|Gun policy|Energy|Religion|Labor|Democracy|Foreign policy|Other`. `position_changed` records whether the position moved during the candidate's career (`yes`/`no`/`unknown`); `change_notes` states how. `candidate_statement` holds verbatim wording where available and `unknown` where only a summary exists — the difference between a `verified` and a `partially verified` row is usually exactly this.

中文：`issue` 必须取 12 个受控值之一。`position_changed` 记录该立场在候选人职业生涯中是否发生变化（`yes`/`no`/`unknown`），`change_notes` 说明如何变化。`candidate_statement` 在有原文时存逐字表述，仅有摘要时为 `unknown`——`verified` 与 `partially verified` 的差别通常正在于此。

## `01_candidates/<lower>/career_timeline.csv` — chronology / 年表

`start_date` and `end_date` are ISO dates or `unknown`; an ongoing role gets `end_date: unknown`. `role_or_event` names the job or event, `organization` the institution, `location` the place as stated in the source. Approximate dates are not invented: where a source gives only a year, the row carries `unknown` rather than a fabricated month.

中文：`start_date` 与 `end_date` 为 ISO 日期或 `unknown`；仍在延续的职务其 `end_date` 写 `unknown`。`role_or_event` 为职务或事件名，`organization` 为机构，`location` 为来源所述地点。不虚构近似日期：来源仅给出年份时，该行写 `unknown` 而非编造月份。

## `02_campaign_events/campaign_events.csv` — events / 事件

`event_category` is drawn from the contract's 43-value vocabulary. `event_status`: `held` only when a report describes what happened; `announced` for written proposals and endorsement releases with no public venue; `cancelled` where the invited candidate declined; `unverified` where the event is asserted without a retrievable account. `campaign_phase` separates `primary`, `general`, `gotv`, `election_day` and `post_election`. `analyst_interpretation` always begins with the literal token `INTERPRETATION:` so that inference can never be mistaken for reportage, and `observable_function` describes what could actually be seen or documented.

中文：`event_category` 取自合同的 43 个受控值。`event_status`：`held` 仅用于有报道描述现场情况者；`announced` 用于无公开场地的书面提案与背书发布；`cancelled` 用于受邀候选人拒绝出席者；`unverified` 用于有人主张但无可取得记述者。`campaign_phase` 区分初选、大选、催票、选举日与选后。`analyst_interpretation` 恒以字面标记 `INTERPRETATION:` 开头，以确保推断不会被误当作报道；`observable_function` 描述实际可被看到或记录的内容。

## `03_speeches/speech_archive.csv` — speeches / 演说

`major_quotes` takes the form `"verbatim quote" [hh:mm:ss]`, pipe-delimited; paraphrase is marked `(paraphrase)`. In this case every timestamp is `[unknown]` because no timestamped recording was obtained, and the file says so rather than inventing one. `source` names the outlet whose report supplied the text, which matters because a speech reconstructed from a news report is not a transcript.

中文：`major_quotes` 格式为 `"逐字引语" [hh:mm:ss]`，以竖线分隔；转述标为 `(paraphrase)`。本案中所有时间戳均为 `[unknown]`，因为未取得带时间戳的录音，文件中如实标注而非编造。`source` 指明提供文本的媒体——这很重要，因为依据新闻报道重建的演说不等于文字稿。

## `03_speeches/speech_video_index.csv` — video index / 视频索引

`transcript_available` is `yes`/`no`; `completeness` is `full|partial|clip|unknown`; `relevant_timestamps` is `unknown` where the video could not be viewed. A video row whose URL was taken from another source's table rather than from the video page itself carries `unverified`.

中文：`transcript_available` 取 `yes`/`no`；`completeness` 取 `full|partial|clip|unknown`；无法观看视频时 `relevant_timestamps` 为 `unknown`。若视频链接取自他处表格而非视频页面本身，该行标 `unverified`。

## `04_visual_archive/image_archive.csv` — images / 影像

`copyright_status` distinguishes `public_domain` from `licensed`. `license` must be one of PD, CC0, CC BY or CC BY-SA — the four families the contract permits — and states the specific version where known. `local_filename` is the path of the stored file, relative to the case folder, or `unknown` for link-only rows that were refused (HTTP 429) or exceeded the 2 MB limit. `image_resolution` records the stored file's dimensions, read from the JPEG header rather than from the Commons page.

中文：`copyright_status` 区分 `public_domain` 与 `licensed`。`license` 必须属于 PD、CC0、CC BY 或 CC BY-SA 四种合同允许的许可族，并在已知时写明具体版本。`local_filename` 为已存文件相对案件目录的路径；仅存链接的行（下载被拒 HTTP 429 或超过 2 MB 上限）写 `unknown`。`image_resolution` 记录已存文件的尺寸，系从 JPEG 文件头读出而非抄自 Commons 页面。

## `05_campaign_media/advertisements.csv` — advertising / 广告

`sponsor_type` is `candidate_campaign|authorized_committee|outside_pac|party_committee|unknown`. Outside spending rows use `EXT-` ids and name the actual spender, because attributing an outside ad to a candidate's campaign is the single easiest error to make in this dataset. `candidate_id` on an `EXT-` row names the candidate the ad *concerned*, and `notes` states the direction (for or against).

中文：`sponsor_type` 取 5 个受控值之一。外部支出行使用 `EXT-` 编号并写出实际出资方，因为把外部广告归到候选人竞选团队名下是本数据集中最容易犯的错误。`EXT-` 行的 `candidate_id` 指该广告所涉及的候选人，`notes` 说明其方向（支持或反对）。

## `05_campaign_media/social_media.csv` — social posts / 社交帖文

`platform`, `account_handle` and `url` are `unknown` where a quoted post could not be located on the platform itself; the row still records the post because a verbatim quotation in a reliable outlet is evidence that the post existed. `post_type` distinguishes text posts, video, Reels and written statements.

中文：无法在平台上定位被引用的帖文时，`platform`、`account_handle` 与 `url` 写 `unknown`；该行仍予记录，因为可靠媒体的逐字引用本身即可证明帖文存在。`post_type` 区分文字帖、视频、Reels 与书面声明。

## `05_campaign_media/media_coverage.csv` — coverage / 报道

`source_tier` applies the same T1/T2/T3 rule as the source registry. `coverage_type` is `news_report|analysis|op_ed|fact_check|interview|live_blog|newsletter|news_video`. `key_framing` states how the outlet framed the event in one line; `notable_quotes` carries only quotes the outlet actually printed.

中文：`source_tier` 与来源登记表使用同一 T1/T2/T3 规则。`coverage_type` 取 8 个受控值之一。`key_framing` 用一行说明该媒体如何框定事件；`notable_quotes` 仅收录该媒体确实刊出的引语。

## `06_campaign_finance/campaign_finance.csv` — money / 财务

`period` is the reporting period end date, or `YYYY-Qn` for quarterly filings. `report_type` distinguishes candidate-committee reports from independent-expenditure rows. The two families are never summed: committee rows come from FEC filings and outside-spending rows come from AdImpact, FEC IE filings or press tallies, and `notes` states the accounting basis on every outside-money row. `debts_owed` is `unknown` throughout because no retrieved source itemised it.

中文：`period` 为报告期截止日，季度申报写作 `YYYY-Qn`。`report_type` 区分候选人委员会报告与独立支出行。两类数据绝不相加：委员会行来自 FEC 申报，外部支出行来自 AdImpact、FEC 独立支出申报或媒体统计，且每条外部资金行的 `notes` 均写明核算口径。因无来源逐项列出，`debts_owed` 全部为 `unknown`。

## `07_electoral_context/election_results.csv` — results / 结果

One row per candidate per race. `winner` is `yes` or `no`. `votes` is an integer and `percentage` a bare number. Every row uses final published figures, never night-of call percentages, and every row carries `partially verified` because the state's own results pages returned HTTP 403.

中文：每场选举每位候选人一行。`winner` 取 `yes` 或 `no`。`votes` 为整数，`percentage` 为纯数字。所有行均使用最终公布数字，绝不用判定当晚的百分比；因州务卿自身结果页面返回 HTTP 403，所有行均标 `partially verified`。

## `07_electoral_context/county_results.csv` — counties / 县级结果

Header only. No county-level vote table was published in any retrieved source, and the contract forbids inventing counties, so the file has the required header and zero data rows; the qualitative county findings are recorded in `results_notes.md` instead.

中文：仅有表头。已取得的任何来源均未公布县级票数表，而合同禁止虚构县份，因此该文件仅有规定的表头、无数据行；定性层面的县级发现改记于 `results_notes.md`。

## `07_electoral_context/polling.csv` — polling / 民调

Column names `elsayed_pct` and `rogers_pct` come from `poll_keys` in `case_meta.json`, so they are fixed even for polls taken before both were nominees — which is why primary polls are excluded entirely rather than shoehorned. A candidate not tested gets `unknown`, never `0`. `margin` is the leader's lead in points.

中文：`elsayed_pct` 与 `rogers_pct` 两列名称来自 `case_meta.json` 中的 `poll_keys`，因此即便在两人均未成为提名人之前进行的民调也须沿用该名称——这也是初选民调被整体排除而非强行套用的原因。未被测试的候选人写 `unknown`，绝不写 `0`。`margin` 为领先者的领先点数。

## Markdown conventions / Markdown 约定

Every `.md` file begins with YAML front matter carrying `title`, `title_zh`, `compiled_by`, `last_updated`, `status` and a one-line `coverage_note`. Each `##` section pairs an English passage with its Chinese counterpart, English governing. Source citations appear as `SRC-####` ids that resolve in `09_sources/sources.csv`.

中文：每个 `.md` 文件均以 YAML 前置块开头，含 `title`、`title_zh`、`compiled_by`、`last_updated`、`status` 与一行 `coverage_note`。每个 `##` 小节均以英文段落与其对应中文段落配对，以英文为准。来源引用写作可在 `09_sources/sources.csv` 中解析的 `SRC-####` 编号。
