# American Political Image Lab — Case Study 001

**2026 Texas U.S. Senate general election: James Talarico (D) vs. Ken Paxton (R)**
Research period March 2026 – November 2026. Bilingual (English + 中文) primary-source archive.

## What this repository is / 这是什么

A reconstruction of *the publicly documented campaign process* — every documented event, speech,
image, advertisement, finance filing and press item of both candidates, each line traceable to a
numbered source. It is research material for a human-led analytical blog and documentary-style
video; it does **not** rank the two campaigns and contains no blog or video script.

对两位候选人全部有据可查的竞选过程的档案：事件、演讲、影像、广告、财务申报与媒体报道，每一行都可溯源到编号来源。它是人工分析写作的素材，**不评判两场竞选孰优孰劣**，也不包含博客或视频脚本。

## Start here / 从这里开始

| | |
|---|---|
| **Full documentation** | [`texas-senate-2026/README.md`](texas-senate-2026/README.md) — directory map, data contract, honest limits |
| **Read it as a website** | open `texas-senate-2026/site/index.html` (offline, no server, 66 pages, EN/ZH side-by-side, clickable sources) |
| **Know the gaps first** | [`texas-senate-2026/research_gaps.md`](texas-senate-2026/research_gaps.md) |
| **Rebuild the site** | `python texas-senate-2026/_staging/_lead_build_site.py` |

## Three cautionary notes / 三条必读前提

1. **No debate took place.** Five records reconstruct the invitations and refusals; the CNN–Jubilee
   event was a solo town hall that several outlets mislabelled as a debate.
   没有辩论。CNN–Jubilee 那场是单人问答，被多家媒体误标为辩论。
2. **Appearance was not measured.** Facial geometry, body proportions and clothing are `unknown`;
   the archive ships a reproducible measurement protocol for a human to execute.
   外貌未测量；档案提供可复现的测量规程，供人工执行。
3. **Money measures cannot be summed.** FEC Schedule E and AdImpact differ by ~10×, and four
   different Talarico "totals" exist. See the bilingual data dictionary §6.
   资金口径不可相加，详见双语数据字典第 6 节。

## Data conventions / 数据约定

- 12 CSV datasets stay English for machine-readability: field names, identifier schemes and
  controlled vocabularies are frozen; Chinese glosses live in
  [`09_sources/data_dictionary_bilingual.md`](texas-senate-2026/09_sources/data_dictionary_bilingual.md).
- All 45 Markdown documents are EN+ZH; English always governs where the two renderings diverge,
  and every quotation keeps its verbatim English original next to the `（译：…）` rendering.
- `unknown` is a value, not a placeholder: it means "not established", never "probably X".

## Licensing / 授权

Photographs stored under `04_visual_archive/` are licensed copies (CC BY / CC BY-SA / CC0 /
public domain) with photographer, date and licence recorded per image. Rights-reserved photographs
are **link-only** records — no unlicensed copy is reproduced. Text and datasets are research
material; cite the `SRC-####` ids in `09_sources/sources.csv`.
