---
title: "Stream B — Gaps and Coverage Notes (candidates and policy positions)"
title_zh: "B 线索——缺口与覆盖说明（候选人与政策立场）"
compiled_by: Stream B (candidates)
last_updated: 2026-11-12
status: complete
---

# Stream B — Gaps and Coverage Notes / B 线索——缺口与覆盖说明

## What shipped / 交付内容

| File / 文件 | Rows / 行数 | State / 状态 |
|---|---|---|
| `01_candidates/policy_positions.csv` | 51 (ANDREWS 34, GRAHAM 17) | complete, validated (15 columns, no blank cells, RFC-4180) |
| `01_candidates/andrews/career_timeline.csv` | 20 | complete, validated (10 columns) |
| `01_candidates/graham/career_timeline.csv` | 24 | complete, validated (10 columns) |
| `01_candidates/andrews/biography.md` | 10 `##` sections | complete, bilingual |
| `01_candidates/andrews/political_positions.md` | 12 `##` sections | complete, bilingual |
| `01_candidates/graham/biography.md` | 10 `##` sections | complete, bilingual |
| `01_candidates/graham/political_positions.md` | 7 `##` sections, blocks (a)–(d) | complete, bilingual |
| `_staging/B_sources.csv` | 53 sources, SRC-0400–SRC-0498 | complete, no dangling ids |

All files are UTF-8 without BOM, LF line endings, and every CSV was parsed with Python's `csv` module to confirm field counts and the absence of blank cells. Every `source_urls` cell carries at least one `SRC-####|https://…` pair.

所有文件均为 UTF-8 无 BOM、LF 换行；每个 CSV 均以 Python `csv` 模块解析核对字段数与空单元格。每行的 `source_urls` 至少包含一组 `SRC-####|https://…`。

## The three biggest gaps / 三个最大缺口

**1. Graham has almost no documented positions of her own — this is the binding constraint on the whole stream.** She had never held elected office before 2026-07-14, and there is no retrievable campaign platform. `darlinegraham.com` and `dgraham.senate.gov` both return HTTP 403, the National Right to Life release also returns 403, and the Washington Post profile of her thin political history is paywalled. Her 17 rows therefore rest on: one bill she introduced (S.5025), one confirmation vote, four committee assignments (jurisdictions, not positions), a debate remark, two endorsement announcements and her administrative career. No verbatim Graham statement exists in this archive on healthcare, Medicaid, Medicare, education, immigration, taxes, tariffs, energy production, agriculture, labour law, judicial philosophy, or abortion.

**1. 格雷厄姆本人的立场记录极少——这是整条线索的硬约束。** 她在 2026-07-14 之前从未担任民选公职，且无可检索的竞选纲领。`darlinegraham.com` 与 `dgraham.senate.gov` 均返回 HTTP 403，全国生命权委员会新闻稿亦返回 403，《华盛顿邮报》关于其政治履历单薄的报道位于付费墙后。她的 17 行仅依据：她提出的一项法案（S.5025）、一次确认表决、四项委员会分配（属管辖范围而非立场）、一句辩论表述、两份背书公告，以及其行政履历。本档案中不存在她在医疗、医疗补助、联邦医疗保险、教育、移民、税收、关税、能源生产、农业、劳动法、司法哲学或堕胎议题上的任何直接表述。

**2. Two anchors in the assignment could not be verified against local text, and one was wrong in substance.** (a) The brief's "2026-08-07 floor remarks on the Lindsey O. Graham Sanctioning Russia and Iran Act" — 2026-08-07 is the date the **Senate passed** H.R. 5334 by 86–11; no floor remarks by Darline Graham on that date were located in any retrieved source, so no such row exists. (b) The brief's "not that informed on national security" remark — the verbatim wording in both the biography and the race article is **"national security is not my thing"**, spoken during a primary runoff debate; the archive records the verbatim form (GRA-POS-0002) and does not reproduce the paraphrase. (c) Related correction: Graham's July 2026 bill was **S.5025**, a revised version of her brother's Sanctioning Russia Act, and it was **not** the version that became law — the enacted text is H.R. 5334. An earlier draft of my own GRA-POS-0001 had conflated these; it has been corrected, and the distinction is now carried in GRA-POS-0001 and in `graham/political_positions.md`.

**2. 任务简报中有两处锚点无法由本地文本证实，其中一处实质有误。** （a）简报所称"2026-08-07 就《林赛·O·格雷厄姆制裁俄罗斯与伊朗法案》所作院会发言"——2026-08-07 实为**参议院以 86 比 11 通过** H.R. 5334 之日；已检索来源中未见达琳·格雷厄姆当日有任何院会发言，故未设该行。（b）简报所称"not that informed on national security"——传记与选情条目中的原文均为 **"national security is not my thing"**，出自初选决选辩论；档案记录原文（GRA-POS-0002），不复述该转述。（c）相关更正：格雷厄姆 2026 年 7 月提出的是 **S.5025**，为其兄《制裁俄罗斯法案》的修订版，且**并非**最终成法的版本——成法文本为 H.R. 5334。我早前草稿中的 GRA-POS-0001 曾将两者混同，现已更正，并在 GRA-POS-0001 与 `graham/political_positions.md` 中保留该区分。

**3. Andrews has no legislative record and several positions carry no date.** She has never held office, so `legislative_record` is `unknown` in all 34 of her rows by instruction, and nothing in the archive can show how she has voted. Beyond that, her tax positions ("no tax on tips", "no tax on Social Security"), the 2022 vows on Roe, contraception and maternal health, and the term-limits and stock-trading positions exist only as reported summaries: no verbatim text, and no date of adoption. The archive therefore cannot say when she took these positions or whether she still holds them. Abortion is the clearest illustration of the dating problem: her 2022 and 2026 LGBTQ+ statements are both dated and they conflict, which is exactly the kind of change the tax and abortion vows cannot be tested for.

**3. 安德鲁斯没有立法记录，且若干立场无日期。** 她从未担任公职，故按要求其 34 行的 `legislative_record` 均为 `unknown`，档案无法显示她的任何表决。此外，其税收立场（"小费免税""社会保障免税"）、2022 年关于 Roe、避孕与孕产健康的承诺，以及任期限制与禁止炒股的立场，均仅为转述性概述：无直接引语，亦无提出日期。因此档案无法判定其提出时间或是否仍然坚持。堕胎议题最能说明这一日期问题：她 2022 年与 2026 年的 LGBTQ+ 表述均有明确日期且相互冲突——这正是税收与堕胎承诺无法被同样检验的原因。

## Source conflicts recorded, not resolved / 已记录但未解决的来源冲突

| Conflict / 冲突 | Sources / 来源 | Treatment / 处理 |
|---|---|---|
| Lindsey Graham's death date: 2026-07-11 vs 2026-07-12 | Race article says 07-11; the Russia/Iran Act article says "Graham's sudden death on July 12, 2026" | Both recorded; `career_timeline.csv` and the biographies use 07-11 (race article + conventions §0), the conflict is flagged in `B_sources.csv` under SRC-0439 |
| Blanche confirmation vote date | WPDE page dated 2026-08-08; the vote date itself is not stated | `statement_date` and `GRA-TL-0022` start_date are `unknown`, with the reporting date noted in the description |
| Andrews' MUSC tenure length: 14 years vs "about 15 years" | Biography says 14 years at MUSC; she says "about 15 years" as a pediatrician in the 2026-10-28 interview | Timeline uses 14 years (2009–2023); the transcript figure is her own rounding and is quoted as such in the positions file |
| Graham's appointment/term start: appointed 07-13, sworn 07-14, infobox term_start 07-14 | Governor's release, biography, CBS | All three recorded; the 112-day incumbency figure is computed from the 07-14 swearing-in to the 11-03 election |

## Things the Lead must know / 负责人须知

1. **`career_timeline.csv` id scheme is mine.** Conventions §3 does not define a prefix for career timelines; I used `AND-TL-0001…0020` and `GRA-TL-0001…0024`. If the Lead prefers `AND-CAR-` (which the earlier, aborted Stream B draft referenced in its `used_by` column), a rename is needed in both CSVs and in `B_sources.csv`.
2. **`B_sources.csv` was rewritten, not appended.** The pre-existing file (timestamp 20:12) used a different id mapping — SRC-0400 was the Andrews raw wikitext, SRC-0404 the WIS transcript, SRC-0410 the local mirror, etc. — and referenced row ids (`AND-POS-0001..0052`, `GRA-POS-0028`, `AND-CAR-*`, `GRA-CAR-*`) that do not exist in the delivered files. My replacement re-numbers SRC-0400–SRC-0498 to match the delivered CSVs. **Do not merge the old mapping**; it would silently mis-point dozens of citations. If the old file is needed for provenance, it should be treated as a separate document, not concatenated.
3. **Graham rows deliberately include jurisdiction-only rows.** GRA-POS-0005/0006/0007/0016 record committee assignments and say in terms that no stated position was retrieved. They are labelled rather than dropped so that the absence is auditable; if the Lead prefers a positions file free of non-positions, they are the four rows to cut (Graham would then fall to 13 rows).
4. **`political_positions.md` for Graham has a fourth block.** The assignment required three separated blocks — (a) her own statements, (b) her Senate record, (c) positions attributed by association with her brother. The anti-abortion endorsements fit none of the three, so they sit in a separately labelled block (d) "positions attributed to her by endorsing organizations". The three required blocks are intact and independently labelled.
5. **Verification convention I applied.** `verified` only where a Tier-2 outlet was read directly in this session (WIS transcript, WIS NRA report, WPDE, The 19th) or where an official record carries the fact; `partially verified` wherever the claim rests on Wikipedia alone or on a paywalled/unread outlet. This makes most rows `partially verified` — deliberately, not carelessly.
6. **Retrieval failures, for the record.** HTTP 403: `drannieandrews.com` (issue page and home), `darlinegraham.com`, `dgraham.senate.gov`, `nrlc.org`. Paywalled/unread: NYT, WaPo, WSJ. These are recorded as gaps, not reported as retrieved content.

## Not written, and not mine to write / 未撰写且不属本线索范围

`07_electoral_context/` holds the statewide totals for this race (Andrews 1,044,001 / 51.14%; Graham 952,191 / 46.64% per conventions §0); those figures are **not** present in the local mirror I was given, so the biographies say "defeated Darline Graham" without restating vote counts, and Stream F remains the owner of that dataset. County-level tables, exit-poll crosstabs and polling belong to Streams F and E. No event, speech, advertisement or image rows were written by this stream.
