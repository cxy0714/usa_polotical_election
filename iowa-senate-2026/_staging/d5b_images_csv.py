# -*- coding: utf-8 -*-
"""image_archive.csv + image_sources_and_licences.md"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CASE, S, URL, write

H = ["image_id", "candidate_id", "image_date", "event_id", "event_category", "source_name",
     "source_url", "original_image_url", "photographer", "copyright_status", "license",
     "local_filename", "image_resolution", "framing", "camera_angle", "image_quality",
     "face_visibility", "body_visibility", "clothing_notes", "notes", "verification_status"]

CP = "https://commons.wikimedia.org/wiki/File%3A"
NOTE_NO_VISION = ("Not inspected pixel-by-pixel: this archive was compiled without image input, so framing, "
                  "lens and clothing fields are unknown unless the Commons description states them.")
R = []


def im(iid, cid, date, eid, cat, page, orig, artist, cstatus, lic, local, res, framing, angle,
       quality, face, body, clothing, notes, ver):
    R.append([iid, cid, date, eid, cat, "Wikimedia Commons", CP + page, orig, artist, cstatus, lic,
              local, res, framing, angle, quality, face, body, clothing, notes, ver])


im("HIN-IMG-0001", "HINSON", "2024-01-01", "unknown", "other",
   "Congresswoman_Ashley_Hinson_Official_portrait.jpg",
   "https://upload.wikimedia.org/wikipedia/commons/c/c8/Congresswoman_Ashley_Hinson_Official_portrait.jpg",
   "Office of Congresswoman Ashley Hinson", "public_domain", "Public domain (U.S. House official portrait)",
   "04_visual_archive/hinson_2024_official_portrait.jpg", "1365x2048", "unknown", "unknown", "unknown",
   "unknown", "unknown", "unknown",
   "Official congressional portrait, 119th Congress. Downloaded at 1100 px width (188,680 bytes). "
   + NOTE_NO_VISION, "verified")
im("HIN-IMG-0002", "HINSON", "unknown", "unknown", "other",
   "Ashley_Hinson_Official_portrait_(cropped_2).jpg",
   "https://upload.wikimedia.org/wikipedia/commons/8/8b/Ashley_Hinson_Official_portrait_%28cropped_2%29.jpg",
   "Office of Congresswoman Ashley Hinson", "public_domain", "Public domain (U.S. House official portrait)",
   "04_visual_archive/hinson_official_portrait_cropped2.jpg", "1004x1362", "unknown", "unknown", "unknown",
   "unknown", "unknown", "unknown",
   "Cropped variant of the 117th Congress portrait; Commons gives the year only, so image_date is unknown. "
   "Downloaded at 800 px (208,800 bytes). " + NOTE_NO_VISION, "verified")
im("HIN-IMG-0003", "HINSON", "2022-11-15", "unknown", "other",
   "Ashley_Hinson_(IA-02).jpg",
   "https://upload.wikimedia.org/wikipedia/commons/9/9b/Ashley_Hinson_%28IA-02%29.jpg",
   "U.S. House of Representatives", "public_domain", "Public domain (U.S. House)",
   "04_visual_archive/hinson_ia02_district_portrait.jpg", "335x410", "unknown", "unknown", "unknown",
   "unknown", "unknown", "unknown",
   "District portrait for the 118th Congress after redistricting. Smallest file in the set; downloaded at "
   "320 px (21,930 bytes). " + NOTE_NO_VISION, "verified")
im("TUR-IMG-0001", "TUREK", "2026-11-09", "unknown", "other",
   "Democratic_senators-elect_meet_with_Chuck_Schumer_in_November_2026.jpg",
   "https://upload.wikimedia.org/wikipedia/commons/b/b7/Democratic_senators-elect_meet_with_Chuck_Schumer_in_November_2026.jpg",
   "U.S. Senate", "public_domain", "Public domain (U.S. Senate)",
   "04_visual_archive/senators_elect_schumer_2026_11_09.jpg", "4096x2731", "group photograph", "unknown",
   "unknown", "unknown", "unknown", "unknown",
   "The Commons description lists the senators-elect present, including \"Josh Turek (IA)\", meeting Senate "
   "Minority Leader Chuck Schumer during freshman orientation. Downloaded at 1600 px (793,443 bytes). "
   "Turek's position within the group is not described by the metadata and was not visually checked.",
   "partially verified")
for i, (name, w, h, artist) in enumerate((
        ("Joshua_Turek.jpg", 1500, 2100, "Iowa General Assembly"),
        ("Joshua_Turek_(cropped).jpg", 1200, 1599, "Iowa General Assembly"),
        ("Joshua_Turek_(cropped_2).jpg", 1200, 1683, "Iowa General Assembly"),
        ("Joshua_Turek_(croppedb).jpg", 1034, 1377, "Iowa General Assembly")), start=2):
    im("TUR-IMG-%04d" % i, "TUREK", "2023-01-09", "unknown", "other", name,
       "https://upload.wikimedia.org/wikipedia/commons/unknown", artist, "all_rights_reserved_link_only",
       "Copyrighted free use (Iowa General Assembly portrait)", "unknown", "%dx%d" % (w, h),
       "unknown", "unknown", "unknown", "unknown", "unknown", "unknown",
       "Official Iowa Legislature portrait. The licence is \"Copyrighted free use\", which is not one of the "
       "four licences this archive is allowed to download, so the file is recorded as link-only.",
       "verified")
im("HIN-IMG-0004", "HINSON", "2024-11-18", "unknown", "other", "Ashley_Hinson_119th_Congress.jpg",
   "https://upload.wikimedia.org/wikipedia/commons/9/99/Ashley_Hinson_119th_Congress.jpg",
   "U.S. House of Representatives", "public_domain", "Public domain (U.S. House)", "unknown", "410x513",
   "unknown", "unknown", "unknown", "unknown", "unknown", "unknown",
   "Permitted licence, but the download failed with HTTP 429 from the Wikimedia thumbnail service; recorded "
   "link-only for that operational reason rather than a licensing one.", "verified")
im("HIN-IMG-0005", "HINSON", "2019-01-29", "unknown", "other", "Ashley_Hinson.jpg",
   "https://upload.wikimedia.org/wikipedia/commons/unknown", "Iowa General Assembly",
   "all_rights_reserved_link_only", "Copyrighted free use (Iowa General Assembly portrait)", "unknown",
   "750x1050", "unknown", "unknown", "unknown", "unknown", "unknown", "unknown",
   "State-legislature portrait from her Iowa House years; licence not downloadable.", "verified")
im("HIN-IMG-0006", "HINSON", "2020-12-03", "unknown", "other", "Ashley_Hinson_(IA-01).jpg",
   "https://upload.wikimedia.org/wikipedia/commons/unknown", "U.S. House of Representatives",
   "public_domain", "Public domain (U.S. House)", "unknown", "335x410", "unknown", "unknown", "unknown",
   "unknown", "unknown", "unknown",
   "First congressional portrait for IA-01; download not attempted after the 429 responses.", "verified")
im("HIN-IMG-0007", "HINSON", "unknown", "unknown", "other",
   "Ashley_Hinson,_official_portrait,_117th_Congress_(cropped).jpg",
   "https://upload.wikimedia.org/wikipedia/commons/unknown", "Office of Congresswoman Ashley Hinson",
   "public_domain", "Public domain (U.S. House official portrait)", "unknown", "817x1090", "unknown",
   "unknown", "unknown", "unknown", "unknown", "unknown",
   "117th Congress portrait, cropped; Commons gives the year only.", "verified")

write("04_visual_archive/image_archive.csv", H, R)
print("rows:", len(R))

io.open(os.path.join(CASE, "04_visual_archive/image_sources_and_licences.md"), "w",
        encoding="utf-8", newline="\n").write("""---
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
""")
print("memo written")
