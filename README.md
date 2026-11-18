# American Political Image Lab — eight 2026 case studies

A bilingual (English + 中文) primary-source archive of eight 2026 American races, built to study how
candidates present themselves: what they say, where they stand, what the staging looks like, how the
money flows, and what the record does **not** show.

八场 2026 年美国选举的双语原始史料档案，用于研究候选人如何呈现自己：他们说什么、站在哪里、舞台如何布置、资金如何流动，以及记录**没有**显示什么。

## What this repository is / 这是什么

Each case folder reconstructs *the publicly documented campaign process* — documented events,
speeches, policy positions, advertising, finance filings, results, polling and press coverage — with
every CSV row traceable to a numbered source (`SRC-####|https://…`). The archive does not rank the
campaigns, score their branding, or declare a winner of a "communication contest". It is research
material for human-led analysis; it contains no blog post and no video script.

每个案例重建*有公开记录的竞选过程*——活动、演讲、政策立场、广告、财务申报、结果、民调与媒体报道——每一行都可溯源到编号来源（`SRC-####|https://…`）。档案不评判竞选优劣、不为品牌打分，也不宣布「传播竞赛」的胜者。它是供人工分析使用的素材，不含博客文章或视频脚本。

Two rules travel through all eight cases:

- **`unknown` is a value.** It means "not established", never "probably X".
- **Description is separated from inference.** `stated_purpose`, `observable_function` and
  `analyst_interpretation` are distinct columns; interpretation is prefixed `INTERPRETATION:`.

两条规则贯穿八案：**`unknown` 是取值**，意为「未查明」，绝不是「大概是 X」；**描述与推断分离**，三层字段各自独立，推断以 `INTERPRETATION:` 开头。

## The eight cases / 八个案例

| # | Folder / 目录 | Race / 选举 | Nominees / 提名人 | Documented result / 结果 |
|---|---|---|---|---|
| 001 | [`texas-senate-2026/`](texas-senate-2026/README.md) | Texas U.S. Senate | James Talarico (D) / Ken Paxton (R) | Talarico 55.06% / 塔拉里科 55.06% |
| 002 | [`south-carolina-senate-2026/`](south-carolina-senate-2026/README.md) | South Carolina U.S. Senate | Annie Andrews (D) / Darline Graham (R) | Andrews 51.14% / 安德鲁斯 51.14% |
| 003 | [`michigan-senate-2026/`](michigan-senate-2026/README.md) | Michigan U.S. Senate | Abdul El-Sayed (D) / Mike Rogers (R) | El-Sayed 52.54% / 埃尔-赛义德 52.54% |
| 004 | [`alaska-senate-2026/`](alaska-senate-2026/README.md) | Alaska U.S. Senate | Mary Peltola (D) / Dan S. Sullivan (R) | Peltola 50.12% / 佩尔托拉 50.12% |
| 005 | [`iowa-senate-2026/`](iowa-senate-2026/README.md) | Iowa U.S. Senate | Josh Turek (D) / Ashley Hinson (R) | Turek 50.56% / 图雷克 50.56% |
| 006 | [`ohio-senate-2026/`](ohio-senate-2026/README.md) | Ohio U.S. Senate (special) | Sherrod Brown (D) / Jon Husted (R) | Brown 50.01% / 布朗 50.01% |
| 007 | [`georgia-senate-2026/`](georgia-senate-2026/README.md) | Georgia U.S. Senate | Jon Ossoff (D) / Mike Collins (R) | Ossoff 59.03% / 奥索夫 59.03% |
| 008 | [`los-angeles-mayor-2026/`](los-angeles-mayor-2026/README.md) | Los Angeles Mayor | Nithya Raman / Karen Bass (nonpartisan) | Raman 54.9% / 拉曼 54.9% |

Cases 001–002 carry the full video/audio layer built earlier (145 and 27 source videos, curated
frames, speech-delivery measurements). Cases 003–008 are source-and-document archives: events,
positions, money, results, image records and bilingual narrative, **with no frame extraction**.
Each README states that difference rather than implying an equivalence.

案例 001–002 带有早前构建的完整视频／音频层；003–008 是来源与文献档案：活动、立场、资金、结果、影像记录与双语叙述，**不含视频抽帧**。各案 README 明确说明这一差异，而不暗示两者等价。

## Start here / 从这里开始

| | |
|---|---|
| **Browse everything** | open [`site/index.html`](site/index.html) — offline portal over all eight cases, EN/ZH, clickable sources |
| **The method** | [`texas-senate-2026/_research_conventions.md`](texas-senate-2026/_research_conventions.md) and each case's own `_research_conventions.md` |
| **The batch-2 contract** | [`_research/2026/CASE_CONTRACT.md`](_research/2026/CASE_CONTRACT.md) — schemas, controlled vocabularies, depth targets |
| **What the imagery record can and cannot support** | [`2026-image-and-message-notes.md`](2026-image-and-message-notes.md) |
| **Rebuild everything** | `python _tools/build_all.py` (validates 003–008, rebuilds their sites and the portal) |

## What batch 2 collected / 第二批收集了什么

Six new races, each with the same core datasets: `01_candidates` (biographies, career timelines,
positions), `02_campaign_events`, `03_speeches` (archive + video index), `04_visual_archive`
(link-only records plus a small number of licensed portraits), `05_campaign_media` (ads, social,
coverage), `06_campaign_finance`, `07_electoral_context` (results, county results where published,
polling), `08_comparative_analysis`, `09_sources` and bilingual `README.md` / `research_gaps.md`.

| Case | CSV rows | Sources | Documented result |
|---|---:|---:|---|
| [`michigan-senate-2026/`](michigan-senate-2026/README.md) | 410 | 96 | El-Sayed 52.54% / Rogers 45.46% |
| [`alaska-senate-2026/`](alaska-senate-2026/README.md) | 437 | 127 | Peltola 50.12% / Sullivan 45.80% |
| [`iowa-senate-2026/`](iowa-senate-2026/README.md) | 523 | 129 | Turek 50.56% / Hinson 46.35% |
| [`ohio-senate-2026/`](ohio-senate-2026/README.md) | 533 | 196 | Brown 50.01% / Husted 45.17% |
| [`georgia-senate-2026/`](georgia-senate-2026/README.md) | 414 | 115 | Ossoff 59.03% / Collins 40.97% |
| [`los-angeles-mayor-2026/`](los-angeles-mayor-2026/README.md) | 505 | 114 | Raman 54.9% / Bass 45.1% (runoff) |

六个新案例，各含相同核心数据集（候选人、活动、演讲、影像、媒体、财务、选举背景、比较分析、来源），
上表为各案 CSV 行数、来源数与已记录结果。

On 2026-11-18 the six new cases also received the visual layer used by the earlier two: credited
news-photo captions harvested from the archived articles (all link-and-credit only), a downloaded
video corpus, scene keyframes, and a YuNet+SFace pass that attributes frames to the two nominees
(`10_video_frames/`). 19 videos, 228 keyframes and 384 news-photo rows were added; the method and its
limits are in [2026-image-and-message-notes.md](2026-image-and-message-notes.md) §6 and in each
case's `10_video_frames/README.md`.

2026-11-18，六个新案例也补上了先前两案使用的视觉层：从存档文章中采集的带署名新闻图注（均仅链接与署名）、
下载的视频语料、场景关键帧，以及把帧归属到两位提名人的 YuNet+SFace 比对（`10_video_frames/`）。
新增 19 段视频、228 张关键帧与 384 条新闻图片记录；方法与限制见
[2026-image-and-message-notes.md](2026-image-and-message-notes.md) 第 6 节及各案 `10_video_frames/README.md`。

Every case is validated mechanically: header conformance, no blank cells, ISO dates, controlled
vocabularies, and every `SRC-####` resolving in that case's `sources.csv`
(`python _tools/validate_case.py <case>`). Fetched pages are kept locally under
`_staging/mirrors/` as the audit trail but are excluded from git (third-party publisher text);
`_staging/fetch_log.csv` — committed — records every URL, status code and saved file.

每个案例都经过机械校验：表头一致、无空单元格、ISO 日期、受控词表，且每个 `SRC-####` 都能在该案 `sources.csv` 中解析。抓取页面保存在本地 `_staging/mirrors/` 作为审计线索，但不纳入 git（第三方出版方文本）；已提交的 `_staging/fetch_log.csv` 记录每个 URL、状态码与保存文件。

## Data conventions / 数据约定

- CSVs stay English for machine-readability; Chinese glosses live in each case's
  `09_sources/data_dictionary_bilingual.md`.
- Markdown is EN+ZH; English governs where the two diverge; quotations keep the verbatim English
  original next to the `（译：…）` rendering.
- Money口径 are never summed across sources: FEC filings, AdImpact/TV spending and outside-group
  totals sit in separate rows and say which口径 they use.
- Photographs: only public-domain or CC-licensed files are copied; rights-reserved images are
  link-only records. Downloaded portraits record photographer, licence and file page.

## Rebuild / 重建

```bash
# batch-2 data validation + per-case sites + shared portal
python _tools/build_all.py

# a single case
python _tools/validate_case.py michigan-senate-2026
python _tools/build_case_site.py michigan-senate-2026

# the cross-case imagery evidence table
python _tools/phenomena_report.py
```

Case 001–002 keep their own build scripts (`texas-senate-2026/_staging/_lead_build_site.py`,
`south-carolina-senate-2026/_staging/_lead_build_site.py`); the portal copies their `site/` folders
as-is.

## Licensing / 授权

Text and datasets are research material; cite the `SRC-####` ids. Photographs under
`04_visual_archive/` are licensed copies (CC BY / CC BY-SA / CC0 / public domain) with photographer,
date and licence recorded per image. Rights-reserved photographs are link-only records — no
unlicensed copy is reproduced.
