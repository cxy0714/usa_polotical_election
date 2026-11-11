# 10_video_frames — 视频帧与人脸识别集

**English** — Frames cut from 26 publicly available videos, with every face detected
and matched against the licensed candidate photographs already in `04_visual_archive/`.
This closes the largest documentary gap in the archive — framing, staging and venue
were `unknown` — without inventing anything: the files below are real frames, the
identity call is a scored nearest-neighbour match, and the limits are listed in §7.

**中文** — 本目录是从 26 段公开视频中截取的帧，画面中的人脸全部经过检测，并与
`04_visual_archive/` 中已有的候选人有授权照片做匹配。它填补了档案中最大的文献缺口
（此前"取景／舞台／场地"均为 `unknown`），且不虚构任何内容：下面是真实帧，身份判定是
带分数的最邻近匹配，局限见第 7 节。

---

## 1. Source videos / 来源视频

26 videos downloaded 2026-11-10/11, published between 2026-07-28 and 2026-11-04. 2 are official
campaign channels; the rest are network/station news packages or wire-service feeds.
A further 3 configured videos could not be downloaded (§7.1).

**Official campaign channels / 官方竞选频道**

| Video ID | Channel | Upload | Kind | Title |
|---|---|---|---|---|
| `F169Ei20N6g` | James Talarico (official campaign) | 2026-10-19 | tour_launch | James Talarico Kicks Off "Clear Eyes, Full Hearts" Tour |
| `9RUJdj83quk` | Ken Paxton for Senate (official campaign) | 2026-09-23 | rally_speech | WATCH: Ken Paxton Gives Remarks at Cypress Rally |

**News / wire packages / 新闻与通讯社**

| Video ID | Channel | Upload | Kind | Title |
|---|---|---|---|---|
| `bGW8aWXKdEc` | NBC DFW | 2026-10-30 | tour_stop | Thousands gather for James Talarico's 'Clear Eyes, Full Hearts' tour in Dallas |
| `Ab7QjD4dB50` | CNN | 2026-11-04 | victory_speech | 'This is a win the size of Texas': Talarico's full victory speech |
| `t3BVsDWgNGo` | KVUE | 2026-10-19 | news_package | Talarico holds 'Clear Eyes, Full Hearts' rally; Paxton makes 'Come and Take It' tour stops |
| `Br3kA5QQDQw` | CBS TEXAS | 2026-10-18 | tour_launch | Ken Paxton kicks off statewide bus tour ahead of early voting in Texas Senate race |
| `puVR9bfMcls` | KHOU 11 | 2026-10-21 | rally | Texas Senate race: Paxton rallies in Conroe amid tight polls |
| `Qk3xvHejQYU` | Associated Press | 2026-11-03 | final_rally | LIVE: Ken Paxton speaks at a rally in Allen, Texas |
| `35-u_mTo-w8` | NBC DFW | 2026-11-03 | rally | Ken Paxton rallies Collin County Republicans in final push before Texas Senate election |
| `h14iskBaBSI` | PBS NewsHour | 2026-11-04 | concession_speech | WATCH: Republican Ken Paxton speaks after losing Texas Senate race |
| `vW1QJCc0_Hw` | CBS TEXAS | 2026-10-19 | rally | James Talarico holds Plano rally ahead of Texas senate election |
| `PWow10eQp-o` | KENS 5 | 2026-10-25 | rally | James Talarico visits San Antonio on 'Clear Eyes, Full Hearts' campaign tour |
| `0nXJYOIZ4Fk` | Angie A (third-party upload) | 2026-10-30 | rally_speech | James Talarico for Texas Rally: Clear Eyes, Full Hearts |
| `qbQzb0sz2OI` | CBS TEXAS | 2026-11-04 | watch_party | James Talarico supporters erupt in celebration at Austin watch party |
| `63Eb4VlhxSE` | KXAN | 2026-11-04 | news_clip | Crowds cheer as AP projects James Talarico wins the U.S. Senate race in Texas |
| `7oqcGDWT4Os` | CBS TEXAS | 2026-11-03 | final_rally | Ken Paxton holds final campaign rally in Allen ahead of midterm elections |
| `YE4pIbpZhAE` | CBS TEXAS | 2026-07-28 | rally | Paxton, Abbott rally North Texas Republicans as Texas Senate race heats up |
| `O7TIsfy4PEQ` | NBC DFW | 2026-11-04 | concession_speech | Full speech: Ken Paxton concedes U.S. Senate race to James Talarico |
| `7c8BeNjXyks` | USA TODAY | 2026-11-04 | concession_speech | Ken Paxton concession speech on midterm election loss to James Talarico |
| `Ln7A66zGNYo` | CBS19 | 2026-10-21 | rally | Talarico rallies supporters in Tyler as Texas Senate race tightens |
| `ufXizbHdU9c` | CBS19 | 2026-10-20 | news_package | Talarico rallies in Tyler as Paxton tours Texas amid tightening Senate race |
| `M8x0ZGVlBhI` | 25 News KXXV | 2026-09-17 | tour_stop | Democratic Senate candidate James Talarico makes campaign stop at Baylor University |
| `aU8yJGKC3DE` | Good Morning America | 2026-11-04 | news_clip | James Talarico wins Texas Senate race |
| `O6HogoPDp4Y` | KETK NBC | 2026-11-01 | rally_speech | Ken Paxton speaks at tense United States Senate campaign rally in Tyler |
| `dOg1d2XSBoQ` | CBS19 | 2026-11-02 | rally | Ken Paxton rallies supporters in Tyler as Senate race enters final stretch |
| `8B6h7IWjCok` | FOX 4 Dallas-Fort Worth | 2026-09-09 | convention_speech | FULL: Ken Paxton's 2026 RNC Midterm Convention Speech |

URLs are in `video_sources.csv`.

## 2. Method / 方法

1. **Sampling** — every 0.5 s for videos ≤ 120 s, every 1.0 s above that
   (**6,939** face crops kept in total).
2. **Detection** — OpenCV YuNet (ONNX, 232 KB), score ≥ 0.55, face side ≥ 64 px,
   up to 3 faces per sampled frame.
3. **Identity** — OpenCV SFace (ONNX, 38.7 MB). Embeddings are L2-normalised and
   compared by cosine against **62 reference embeddings** built from the archive's own
   licensed candidate photographs (`04_visual_archive/talarico/campaign/` 7 files,
   `04_visual_archive/paxton/campaign/` 69 files; 62 usable).
4. **Decision rule** — class-balanced best-per-class cosine; a label is assigned only if
   `best ≥ 0.40` **and** `best − second-best ≥ 0.05`, otherwise `unknown`.
5. **Reference sanity check** — same-class mean cosine **0.499**, cross-class mean
   **0.123**. The two reference pools are cleanly separated.
6. **De-duplication** — each surviving candidate frame gets a 64-bit DCT perceptual hash
   and a torso-region colour signature. Within a video, a frame is dropped when the hash
   is within 12 bits of an accepted frame (near-identical framing) or when the torso colour
   matches within 12 RGB units and the hash within 20 bits. Across videos only a
   near-identical image (≤ 6 bits) counts as a duplicate, so different venues survive.
   At most 3 frames per video per outfit-colour bucket are kept.
7. **Selection floor** — `identity_sim ≥ 0.62`, `sharpness ≥ 40`, `face width ≥ 80 px`;
   max 8 per video, 2.5 s minimum spacing. Result: **150 candidates → 67 kept frames
   (31 Talarico / 36 Paxton); 83 redundant frames removed**.
8. **Measurements** — shot scale from face-width / frame-width ratio; face box in source
   pixels; Laplacian sharpness; mean grey brightness; mean RGB of the region below the
   face (a crude torso proxy, **not** a clothing classification).

Scripts: `../_staging/vision/{extract_faces,recognize_faces,curate}.py`;
config: `../_staging/vision/videos.json`; models cached in `../_staging/vision/models/`.

## 3. What the identity pass found / 身份识别结果

| Source video | Kind | Talarico | Paxton | unknown | no face |
|---|---|---|---|---|---|
| 'This is a win the size of Texas': Talarico's full victory speech | victory_speech | 705 | 0 | 1370 | 2 |
| WATCH: Ken Paxton Gives Remarks at Cypress Rally | rally_speech | 0 | 533 | 0 | 0 |
| LIVE: Ken Paxton speaks at a rally in Allen, Texas | final_rally | 1 | 498 | 23 | 30 |
| FULL: Ken Paxton's 2026 RNC Midterm Convention Speech | convention_speech | 0 | 398 | 3 | 0 |
| James Talarico wins Texas Senate race | news_clip | 237 | 0 | 63 | 0 |
| Talarico rallies supporters in Tyler as Texas Senate race tightens | rally | 73 | 54 | 52 | 5 |
| Talarico holds 'Clear Eyes, Full Hearts' rally; Paxton makes… | news_package | 60 | 60 | 39 | 2 |
| Texas Senate race: Paxton rallies in Conroe amid tight polls | rally | 57 | 55 | 129 | 0 |
| Full speech: Ken Paxton concedes U.S. Senate race to James… | concession_speech | 0 | 110 | 2 | 2 |
| Ken Paxton speaks at tense United States Senate campaign rally in… | rally_speech | 48 | 52 | 161 | 23 |
| WATCH: Republican Ken Paxton speaks after losing Texas Senate race | concession_speech | 0 | 96 | 63 | 8 |
| James Talarico holds Plano rally ahead of Texas senate election | rally | 34 | 39 | 30 | 3 |
| Talarico rallies in Tyler as Paxton tours Texas amid tightening… | news_package | 36 | 32 | 109 | 7 |
| Ken Paxton holds final campaign rally in Allen ahead of midterm… | final_rally | 27 | 38 | 38 | 2 |
| Ken Paxton rallies Collin County Republicans in final push before… | rally | 0 | 65 | 96 | 16 |
| Thousands gather for James Talarico's 'Clear Eyes, Full Hearts'… | tour_stop | 30 | 13 | 109 | 6 |
| James Talarico visits San Antonio on 'Clear Eyes, Full Hearts'… | rally | 40 | 3 | 64 | 16 |
| Ken Paxton kicks off statewide bus tour ahead of early voting in… | tour_launch | 30 | 12 | 93 | 4 |
| Ken Paxton concession speech on midterm election loss to James… | concession_speech | 0 | 41 | 4 | 7 |
| Democratic Senate candidate James Talarico makes campaign stop at… | tour_stop | 31 | 3 | 95 | 2 |
| Paxton, Abbott rally North Texas Republicans as Texas Senate race… | rally | 2 | 18 | 27 | 1 |
| Ken Paxton rallies supporters in Tyler as Senate race enters… | rally | 2 | 17 | 270 | 10 |
| James Talarico Kicks Off "Clear Eyes, Full Hearts" Tour | tour_launch | 10 | 0 | 16 | 0 |
| James Talarico supporters erupt in celebration at Austin watch… | watch_party | 4 | 2 | 194 | 11 |
| Crowds cheer as AP projects James Talarico wins the U.S. Senate… | news_clip | 0 | 5 | 149 | 5 |
| James Talarico for Texas Rally: Clear Eyes, Full Hearts | rally_speech | 0 | 0 | 5 | 2 |

Total: **6,939 crops → 1,427 Talarico / 2,144 Paxton / 3,204 unknown / 164 no face**.

Curated-frame similarity: Talarico median **0.791** (n=31), Paxton median **0.742**
(n=36); the weakest accepted frame is **0.624**.

## 4. Files / 文件

| File | Content |
|---|---|
| `frame_index.csv` | 67 curated frames: identity + similarity, video, event kind, timestamp, face px, shot scale, sharpness, brightness, torso-region RGB, paths |
| `video_sources.csv` | the 26 source videos with channel, upload date, duration, URL |
| `curation_stats.json` | candidate pool size, kept count and per-video kept counts |
| `frames/*.jpg` | full frames (clean + `_annot` with the detected face box and score) |
| `faces/*.jpg` | 256×256 face crops behind each identity call |
| `sheet_talarico_frames.jpg` | 31 Talarico frames, contact sheet |
| `sheet_paxton_frames.jpg` | 36 Paxton frames, contact sheet |
| `sheet_duel.jpg` | top 12 per candidate side by side |
| `sheet_context.jpg` | evenly spaced staging frames from every video (no identity claim) |

## 5. First measurable observations / 可先说的量化观察

Stated as measurements, not interpretations:

- **Shot scale**: Talarico 22 medium / 9 medium-close / 0 close-up; Paxton 30 medium /
  5 medium-close / 0 close-up. The curation floor is a face ≥ 80 px on ≤720p sources, so
  close-ups are mechanically rare and the difference is partly an artefact of the rule.
- **Face size at selection**: Talarico 92–231 px, Paxton 82–258 px.
- **Torso-region mean RGB** varies far more between videos than between candidates —
  venue lighting dominates any colour comparison.
- **Format split**: official channels publish very differently — Talarico's tour clip is
  640×360 / 75 s (social-first cut), Paxton's Cypress rally is 720p / 20 min (broadcast feed).

## 5.1 The official mark / 官方标志

`assets/talarico_logo.svg` is **`File:James Talarico for Senate logo.svg`** from
Wikimedia Commons, sourced to `jamestalarico.com`. Parsed as vector data:

| Property | Value |
|---|---|
| Canvas | 204 × 52 (ratio ≈ 3.9 : 1, a horizontal wordmark) |
| Paths | 18 (glyph outlines converted to paths; plus one `fill="none"` background) |
| Colours | `black` × 18, `white` × 1, `none` × 1 — **no hex palette, no gradient, no accent colour** |
| Strokes | none |
| Typography | outlined, no live text and no `font-family` declaration |

So the documented mark is a **monochrome black wordmark** with no colour system of its
own: whatever colour the campaign used came from photography and merchandise, not from
the logo file. Two small star-shaped paths sit at the lower corners of the canvas.

**Paxton side: no comparable mark was located.** A Commons namespace search for a Paxton
campaign logo returned nothing usable, and the campaign site served no retrievable
issue/branding pages. This asymmetry must travel with any "brand-system" comparison.

## 6. Reproduction / 复现

```powershell
# first clone only: restore the video + model binaries excluded from Git (~530 MB)
python texas-senate-2026/_staging/vision/fetch_models.py        # YuNet + SFace ONNX
python texas-senate-2026/_staging/vision/download_videos.py     # 26 source videos

python texas-senate-2026/_staging/vision/extract_faces.py     # sampling + detection
python texas-senate-2026/_staging/vision/recognize_faces.py   # SFace identity pass
python texas-senate-2026/_staging/vision/curate.py            # de-duplicated curated set
python texas-senate-2026/_staging/vision/gen_readme.py        # regenerate this file
```

## 7. Limits — read before using / 使用前必读

1. **3 configured videos could not be downloaded**: `N6PubEh2jZg`, `sa1vT9B4Ick`, `DrD_wR6gEU4`. They stalled at 0 bytes or
   at ~5 KB/s during section downloads and were dropped rather than left half-processed.
   They remain registered in `videos.json`, so a retry is one command away.
2. **No audio was analysed.** Nothing here says anything about delivery, tone or pacing;
   all prosody fields in the main archive remain `unknown`.
3. **67 frames from 26 videos is still a small sample.** It cannot support frequency
   claims about either campaign's imagery.
4. **Mixed production contexts.** Official feeds and local-TV packages differ in camera
   position, lighting and graphics; comparing across them confounds source with candidate.
5. **The torso RGB column is a crude region mean**, often capturing background. It is not
   a garment-colour reading.
6. **No facial geometry measurement was performed** beyond the face bounding box. The
   interocular/face-width protocol in the two visual analyses is still unexecuted.
7. **Rights**: these frames are cut from YouTube videos owned by the campaigns and TV
   stations. They are stored for **internal analysis only** and are **not licensed for
   republication**. Any public use requires a licensed still or link-only treatment.
