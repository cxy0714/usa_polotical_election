---
title: Visual archive notes
title_zh: 视觉档案说明
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: 18 image records, 15 files downloaded under 2 MB; clothing and composition fields are deliberately unknown.
---


# Visual archive notes

## What is here

`image_archive.csv` holds 18 records: 11 for Brown, 7 for Husted. Fifteen corresponding files
are downloaded into `brown/` and `husted/`, each under 2 MB. Three records are catalogue-only and
say so: the 2018 lieutenant-governor portrait (7.0 MB original), a 2017 photograph (5.6 MB) and
the 2026 vertical campaign video (19 MB), all above the size ceiling.

## Licensing

Every file is public domain, CC0, CC BY or CC BY-SA, read from the Wikimedia Commons API's
`imageinfo` response, and the licence string in the CSV is the API's own value. Attribution
requirements are recorded in `photographer`; two files (the 2016 DNC photograph under CC BY-SA
3.0 and the 2016 City Club screen capture under CC BY 3.0) require credit when reused.

## Deliberate unknowns

`clothing_notes`, `camera_angle`, `face_visibility` and `body_visibility` are `unknown` for every
row. This build has no image-reading step: nothing in the pipeline opened the pixels, and no
retrieved caption describes what either candidate is wearing. Filling those cells from
imagination would have produced the most confident-looking and least defensible columns in the
archive. `framing` is limited to what the Commons file title or description states (for example
"official portrait" or "screen capture from video"), and `image_resolution` is either the API's
pixel size or, for downloaded files, the measured pixel size.

## What the images can and cannot establish

They establish likeness, dates and licensing. They do not establish crowd size, mood or setting.
Only two records can be tied to a dated campaign event: the oath photograph (2025-01-21) and the
2026-10-29 video, and in both cases the date comes from the Commons metadata rather than from
inspection.

## Portraits for comparison

Three public-domain portraits satisfy the contract's portrait requirement: Brown 2021 (official,
117th Congress), Brown 2009 (earlier official photo) and Husted 2025 (official, 119th Congress).
The two 2025 Husted portraits are the fairest pair for side-by-side comparison, taken within
weeks of each other and both official.

## 中文摘要

`image_archive.csv` 共 18 条记录（布朗 11、赫斯特德 7），已下载 15 个文件，全部小于 2 MB。三条
仅登记未下载：2018 年副州长官方肖像（原始 7.0 MB）、2017 年照片（5.6 MB）、2026 年竖屏竞选视频
（19 MB），均超过体积上限。许可信息取自 Commons API 的 imageinfo，逐字记录。`clothing_notes`、
`camera_angle`、`face_visibility`、`body_visibility` 四列全部为 unknown：本流程没有任何读图步骤，
也没有任何检索到的图注描述衣着；凭想象填写会造出全档案最自信却最不可辩护的列。三张公有领域肖像
（布朗 2021、布朗 2009、赫斯特德 2025）满足合同要求。

## News photograph harvest (2026-11-18)

On 2026-11-18 the archive added **25 credited news-photograph rows** harvested from the article HTML already stored for fact-checking. 15 rows in this file have a local licensed copy; the news rows do not — the photograph is all rights reserved, so only the article URL, caption and credit line are recorded.

按候选人 / by candidate: BROWN 18, HUSTED 7

Top outlets / 主要来源: cleveland.com (4), Los Angeles Daily News (4), NBC News (3), yahoo.com (3), ohiocapitaljournal.com (2), bostonherald.com (2)

Every row is `verification_status = partially verified`: the caption was read in the archived page, but **the image itself was neither downloaded nor viewed**. A caption that names both nominees may describe either of them; rows record the candidate named first in the caption and do not assert who is pictured.

每一行都是 `partially verified`：说明文字确实在读到的存档页面中出现，但**图片本身既未下载也未查看**。同时提到两位候选人的说明文字可能描述其中任何一位；记录取说明中最先出现的候选人，并不断言画面中是谁。

Rows whose caption names no candidate are not harvested; gallery pages, logos, maps and charts are excluded. See `_tools/news_photos.py` for the exact filters.
