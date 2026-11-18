---
title: Image sources and licences
title_zh: 图片来源与授权
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Four files downloaded under permitted licences; Turek's official portraits are link-only because their licence is not on the allowed list.
---

# Image sources and licences / 图片来源与授权

## What was downloaded / 已下载文件

| File / 文件 | Candidate / 候选人 | Licence / 授权 | Resolution / 分辨率 | Bytes |
|---|---|---|---|---|
| `hinson_2024_official_portrait.jpg` | Hinson | Public domain (U.S. House official portrait) | 1365x2048 (kept at 1100 px) | 188,680 |
| `hinson_official_portrait_cropped2.jpg` | Hinson | Public domain (U.S. House official portrait) | 1004x1362 (kept at 800 px) | 208,800 |
| `hinson_ia02_district_portrait.jpg` | Hinson | Public domain (U.S. House) | 335x410 (kept at 320 px) | 21,930 |
| `senators_elect_schumer_2026_11_09.jpg` | Turek (in group) | Public domain (U.S. Senate) | 4096x2731 (kept at 1600 px) | 793,443 |

中文：实际下载四张，均为公有领域（美国众议院官方肖像、参议院官方合影），全部小于 1 MB。Hinson 的三张为其国会官方肖像的不同版本；Turek 唯一可下载的图像是 2026 年 11 月 9 日当选参议员与参议院少数党领袖舒默的合影，图注明确列出 "Josh Turek (IA)"。

## What was deliberately not downloaded / 有意未下载

Turek's four Iowa Legislature portraits (`Joshua Turek.jpg` and three crops) carry the licence **"Copyrighted free use"**, which is not one of the four licences this project permits for download (PD, CC0, CC BY, CC BY-SA). They are recorded in `image_archive.csv` with `local_filename = unknown` and remain link-only.

中文：Turek 的四张州议会官方肖像授权为 "Copyrighted free use"，不属于本项目允许下载的四种授权，因此仅记录链接，不下载文件。

## Operational note / 操作说明

The Wikimedia thumbnail service returned HTTP 429 (rate limited) for several later requests, so `Ashley Hinson 119th Congress.jpg`, `Ashley Hinson (IA-01).jpg` and the IA-02 portrait were not all retrieved; the two that mattered most for licensing coverage were downloaded first. No image was inspected visually — this archive was compiled without image input — so every framing, lens and clothing field is `unknown` unless the Commons description states it.

中文：维基共享资源的缩略图服务在后续请求中返回 429 限流，部分可下载文件未能取得；本档案在无图像输入的环境下编制，除共享资源说明文字外，构图、镜头与着装字段一律记为 unknown，不作推测。

## Reuse rule / 复用规则

Each row in `image_archive.csv` carries `source_url` (the Commons file page), `original_image_url`, `photographer`, `license` and `copyright_status`. Re-users must check the Commons file page before republication; a public-domain U.S. House portrait still carries a courtesy expectation of credit to the photographer/office named there.
