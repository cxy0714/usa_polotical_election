---
title: "Case Study 001 — 2026 Texas U.S. Senate general election: Talarico vs. Paxton"
title_zh: "案例研究 001 —— 2026 年德克萨斯州联邦参议员大选：塔拉里科对阵帕克斯顿"
subtitle: "American Political Image Lab — primary-source campaign reconstruction archive"
language: en+zh
compiled_by: Lead Research Agent (with five specialist agents)
last_updated: 2026-11-10
research_period: 2026-03 → 2026-11
status: complete
---

# Case Study 001 — 2026 Texas U.S. Senate: James Talarico (D) vs. Ken Paxton (R)
# 案例研究 001 —— 2026 年德州联邦参议员选举：詹姆斯·塔拉里科（民主党）对阵肯·帕克斯顿（共和党）

A reconstruction of the **publicly documented campaign process**, built for a human
analyst who will decide which events, images and arguments deserve emphasis.

本档案是对**公开可查的竞选过程**的一次重构，服务于一位人类研究者——由他来决定哪些事件、哪些影像、哪些论点值得强调。

**This archive collects and organises evidence. It does not conclude which campaign
was better, whose branding was more effective, or whose communication was more
persuasive.** No strategy-effectiveness judgement, no visual-quality ranking and no
sentiment scoring appears anywhere in these files.

**本档案只收集与整理证据，不对哪一方竞选更成功、哪一方的形象包装更有效、哪一方的传播更有说服力下结论。** 全部文件中不含任何竞选效果评判、视觉质量排序或情感倾向打分。

---

## 1. What this is / 这是什么

Ten datasets, 158 research files, a 145-video frame-and-audio layer (face-recognised
frames, scene keyframes, measured speech delivery) and a bilingual offline website
reconstructing the campaign across five parallel research streams, every row carrying its
own sources:

十个数据集、158 份研究材料、一套覆盖 145 段视频的画面与音频层（人脸识别帧、镜头关键帧、演讲交付测量），外加一个离线双语站点，按五条并行的研究线索重构整场竞选；每一行数据都自带来源。

| Stream / 线索 | Dataset(s) / 数据集 | Rows / 行数 |
|---|---|---|
| Candidate background / 候选人背景 | `01_candidates/policy_positions.csv`, 2 biographies, 2 position files, 2 career timelines | **146** policy rows + 60 career events |
| Event reconstruction / 事件重构 | `02_campaign_events/campaign_events.csv` + 2 timelines + coverage-gap register | **93** events |
| Speeches & rhetoric / 演讲与修辞 | `03_speeches/speech_archive.csv`, `speech_video_index.csv`, 24 ten-section analyses, 2 communication analyses, 1 transcript | **32** speeches, **31** videos, **24** analyses |
| Visual archive / 影像档案 | `04_visual_archive/image_archive.csv`, 76 locally measured photos, 2 visual analyses | **116** images |
| Video frames / 视频帧 | `10_video_frames/{frame_index,video_sources,shot_index,video_visual_metrics}.csv`, 106,295 face crops and 1,073 scene keyframes from 145 videos | **172** curated frames |
| Speech audio / 演讲音频 | `11_speech_audio/{delivery_metrics,speech_segments}.csv`, 78 timed transcripts, 93 audio copies | **145** videos measured |
| Media & money / 媒体与资金 | `05_campaign_media/advertisements.csv`, `social_media.csv`, `media_coverage.csv`, `06_campaign_finance/campaign_finance.csv` | **23** ads, **12** posts, **66** coverage items, **69** finance rows |
| Electoral context / 选举背景 | `07_electoral_context/*` (results, polling, election context) | 12 results + 11 polls |
| Comparative synthesis / 对比综合 | `08_comparative_analysis/*` | 3 analyses |
| Sources / 来源 | `09_sources/sources.csv` | **189** unique sources |

## 2. What this is not / 这不是什么

- Not a biography. The biographies exist to support event interpretation, not as a life story.
  不是传记。传记的存在是为解读事件提供背景，而非讲述完整人生。
- Not an election summary. Results are context, not the object of study.
  不是选举综述。选举结果是背景信息，不是研究对象本身。
- Not a blog post or video script. **No final narrative was written** — that is the human
  researcher's decision.
  不是博客文章，也不是视频脚本。**本档案没有撰写任何最终叙事**——那是人类研究者的决定。
- Not a verdict. There is no ranking of candidates, campaigns, ads or images.
  不是判决书。档案中没有对候选人、竞选活动、广告或影像的任何排序。
- Not padded. Where evidence was thin, files say so and counts are honest (see §7).
  没有注水。凡是证据薄弱之处，文件如实标明，计数保持诚实（见第 7 节）。

## 3. The race, in dates / 这场选举的时间线

| Date / 日期 | Event / 事件 |
|---|---|
| 2025-04-08 | Paxton registers his Senate committee (C00901918) / 帕克斯顿注册联邦参议员竞选委员会（C00901918） |
| 2025-09-09 | Talarico launches his Senate campaign, Round Rock (committee C00919084) / 塔拉里科在 Round Rock 宣布参选（委员会 C00919084） |
| 2026-03-03 | Primaries: Talarico wins outright **52.4%**; Cornyn 41.9% / Paxton 40.8%, runoff forced / 初选：塔拉里科以 **52.4%** 直接胜出；科宁 41.9%、帕克斯顿 40.8%，进入决选 |
| 2026-05-19 | Trump endorses Paxton, one week before the runoff / 特朗普在决选前一周为帕克斯顿背书 |
| 2026-05-26 | Paxton wins runoff **63.8%** — Cornyn first Texas incumbent senator to lose renomination since 1970 / 帕克斯顿以 **63.8%** 赢下决选；科宁成为 1970 年以来首位失去本党提名的德州现任联邦参议员 |
| 2026-10-14 / 10-16 | Both closing tours announced two days apart ("Come and Take It" / "Clear Eyes, Full Hearts") / 双方收官巡回宣传相隔两天先后公布（"Come and Take It" / "Clear Eyes, Full Hearts"） |
| 2026-10-19 | Early voting begins (>7.7 million early votes) / 提前投票开始（提前投票超过 770 万张） |
| 2026-11-02 | Talarico's Austin finale held; Paxton's advertised Alamo finale **cancelled** / 塔拉里科奥斯汀收官集会如期举行；帕克斯顿宣传中的阿拉莫收官集会**取消** |
| 2026-11-03 | **Talarico wins 55.06% (5,447,069) to 42.97% (4,250,664)** — 12-point margin / **塔拉里科以 55.06%（5,447,069 票）对 42.97%（4,250,664 票）胜出**——领先 12 个百分点 |
| 2026-11-09 | Talarico places an "I voted" sticker on the Lorenzo Salgado memorial, Houston; then Senate orientation in Washington / 塔拉里科在休斯敦的洛伦佐·萨尔加多纪念处贴上"I voted"贴纸；随后赴华盛顿参加参议院新议员说明会 |

## 4. Ten research questions, and where the answers live / 十个研究问题及其对应文件

The brief asked ten questions per candidate. Mapping:
研究任务书要求对每位候选人回答十个问题，对应关系如下：

| Question / 问题 | Where answered / 对应文件 |
|---|---|
| 1. What activities did each candidate undertake? / 各候选人开展了哪些活动？ | `02_campaign_events/campaign_events.csv`; 93 rows, TALARICO 49 / PAXTON 44 |
| 2. When and where? / 在何时何地？ | `event_date`, `city`, `venue`, `state_region`; plus `talarico_timeline.md`, `paxton_timeline.md` |
| 3. For what stated purpose? / 宣称的目的是什么？ | Three-layer rule: `stated_purpose` / `observable_function` / `analyst_interpretation`（标注 `INTERPRETATION:`） |
| 4. What did they actually say? / 他们实际说了什么？ | `02_campaign_events`（`speech_summary`, `main_messages`）；`03_speeches/speech_archive.csv`；24 篇关键演讲分析 |
| 5. What positions did they advance? / 他们主张哪些政策立场？ | `01_candidates/policy_positions.csv`（12 个维度，146 行）；每位候选人的 `political_positions.md` |
| 6. Who was the target audience? / 目标受众是谁？ | `target_audience` 字段，依据事件、场地与引语所记载的内容编码 |
| 7. How did they present themselves visually? / 他们的视觉形象如何呈现？ | `04_visual_archive/image_archive.csv`；`visual_analysis_talarico.md`、`visual_analysis_paxton.md`；事件表中的 `visual_notes` |
| 8. How did media report and interpret it? / 媒体如何报道与解读？ | `05_campaign_media/media_coverage.csv`（66 条、47 家媒体）；`media_narrative_timeline.md`（7 个叙事阶段） |
| 9. How did this change over time? / 随时间如何变化？ | `campaign_phase` 编码；`08_comparative_analysis/campaign_timeline_comparison.md` |
| 10. What differed between the campaigns? / 双方竞选有何差异？ | `08_comparative_analysis/candidate_comparison.md` |

## 5. Documented findings the analyst can rely on / 研究者可以依赖的有据发现

These are stated as documented facts with sources, not as judgements.
以下内容是以来源为据的事实陈述，不是判断。

1. **No debate occurred.** Five `debate_invitation` rows document the chronology:
   Talarico accepted ≥4 invitations (including FOX/Bret Baier); Paxton's camp said
   negotiations failed because Talarico "always wants something we can't do"; Talarico's
   spokesperson called that "lying" and cited "a personal call to his cellphone";
   Talarico: "literally any time, any place, any network." The CNN–Jubilee event was a
   **solo** voter Q&A, mislabelled a debate by several outlets.

   **没有举行任何辩论。** 五条 `debate_invitation` 记录还原了时间线：塔拉里科接受了至少四场邀请（含 FOX／Bret Baier）；帕克斯顿阵营称谈判失败是因为塔拉里科"总是要一些我们做不到的东西"（译）；塔拉里科的发言人指此为"撒谎"（译），并称帕克斯顿"无视了每一次尝试，包括打到他手机的一通私人电话"（译）；塔拉里科本人则表示"任何时间、任何地点、任何电视台"（译）。CNN–Jubilee 那场活动是**单人**选民问答，被多家媒体误标为辩论。
2. **Paxton was nominated twelve weeks after Talarico**, after a runoff described as
   "vile" and "brutal," with the incumbent he beat declining to campaign for him.

   **帕克斯顿获得提名的时间比塔拉里科晚十二周**，且此前经历了一场被形容为"卑劣"与"残酷"（译）的决选；被他击败的现任参议员拒绝为他助选。
3. **The two closing tours are a controlled comparison.** Announced 2026-10-14 and
   2026-10-16; launched Rockwall airport (10-17, ~200 people) and Plano (10-18);
   both advertised to finish 2026-11-02 — Talarico's Austin finale held, Paxton's Alamo
   finale cancelled two days out.

   **两条收官巡回宣传构成一组可控比较。** 分别于 2026-10-14 与 10-16 公布；起点为 Rockwall 机场（10-17，约 200 人）与 Plano（10-18）；双方都宣称将于 2026-11-02 收官——塔拉里科的奥斯汀收官集会如期举行，帕克斯顿的阿拉莫收官集会在两天前取消。
4. **The paid air war was mostly not the candidate's.** Documented ads: Talarico
   campaign 10, outside PACs 4; **Paxton campaign 1**, outside PACs 8. AdImpact puts
   outside groups at **92%** of Paxton's ad support vs **23%** of Talarico's.

   **付费广告战主要并非候选人自身所为。** 有据可查的广告：塔拉里科竞选团队 10 支、外部政治行动委员会 4 支；**帕克斯顿竞选团队仅 1 支**、外部政治行动委员会 8 支。AdImpact 数据显示，外部团体占帕克斯顿广告投放支持的 **92%**，而塔拉里科一方为 **23%**。
5. **Money, as filed:** through 2026-10-14 Talarico's committee reported
   **$146,349,912** receipts / $9,922,857 cash on hand; Paxton's **$22,319,359** /
   $4,784,408. **Both reported $0 debt.**

   **按申报口径的资金情况：** 截至 2026-10-14，塔拉里科委员会报告收入 **146,349,912 美元**、手头现金 9,922,857 美元；帕克斯顿为 **22,319,359 美元**、4,784,408 美元。**双方均申报零负债。**
6. **The visual identities quote different cultures.** Talarico named his tour after a
   television motto (*Friday Night Lights*) and later cast the series' actors in an ad;
   Paxton named his after the 1835 Gonzales "Come and Take It" flag and built the tour's
   imagery around a replica of it.

   **双方的视觉识别引用的是不同的文化资源。** 塔拉里科以一句电视剧台词（*Friday Night Lights*）为巡回宣传命名，随后又请该剧演员出演广告；帕克斯顿以 1835 年冈萨雷斯"Come and Take It"旗命名，并围绕该旗复制品构建巡回宣传的视觉意象。
7. **Three named Talarico tours, one named Paxton tour:** "Frontera" (July),
   "New American Dream" (August), "Clear Eyes, Full Hearts" (October) vs "Come and Take It."

   **塔拉里科有三条具名巡回路线，帕克斯顿有一条：** "Frontera"（7 月）、"New American Dream"（8 月）、"Clear Eyes, Full Hearts"（10 月），对应帕克斯顿的 "Come and Take It"。
8. **A documented activity gap, not fabricated events:** Talarico was off the trail for
   about two weeks in early October (flu). No events were invented to fill it.

   **这是有据可查的活动空窗，而非编造事件：** 塔拉里科在 10 月初因流感离开竞选活动约两周。档案没有为填补这段空白而虚构任何活动。

## 6. Directory map / 目录结构

```
texas-senate-2026/
├── README.md                      ← you are here / 本文件
├── research_gaps.md               ← consolidated gap register (read second) / 缺口总登记（建议第二份阅读）
├── _research_conventions.md       ← binding data contract / 具约束力的数据契约
│
├── 01_candidates/
│   ├── policy_positions.csv       ← 146 rows × 15 cols / 146 行 × 15 列
│   ├── talarico/{biography.md, political_positions.md, career_timeline.csv}
│   └── paxton/{biography.md, political_positions.md, career_timeline.csv}
│
├── 02_campaign_events/
│   ├── campaign_events.csv        ← 93 rows × 27 cols — core deliverable / 核心交付物
│   ├── talarico_timeline.md
│   ├── paxton_timeline.md
│   └── event_coverage_gaps.md
│
├── 03_speeches/
│   ├── speech_archive.csv         ← 32 speeches (18 TAL / 14 PAX)
│   ├── speech_video_index.csv     ← 31 video records
│   ├── key_speech_analysis/       ← 24 ten-section analyses / 24 篇十节分析
│   ├── communication_analysis_talarico.md
│   ├── communication_analysis_paxton.md
│   └── transcripts/
│
├── 04_visual_archive/
│   ├── image_archive.csv          ← 116 rows × 21 cols / 116 行 × 21 列
│   ├── talarico/campaign/         ← 7 licensed copies
│   ├── paxton/campaign/           ← 69 licensed copies
│   ├── visual_analysis_talarico.md
│   └── visual_analysis_paxton.md
│
├── 05_campaign_media/
│   ├── advertisements.csv         ← 23 ads (14 TAL / 9 PAX)
│   ├── social_media.csv           ← 12 posts
│   ├── media_coverage.csv         ← 66 items, 47 outlets
│   └── media_narrative_timeline.md
│
├── 06_campaign_finance/
│   └── campaign_finance.csv       ← 69 rows / 69 行
│
├── 07_electoral_context/
│   ├── election_context.md
│   ├── election_results.csv       ← 12 rows
│   ├── polling.csv                ← 11 polls
│   └── county_results.csv         ← header-only BY DESIGN / 有意仅保留表头
│
├── 08_comparative_analysis/
│   ├── campaign_organization.md
│   ├── candidate_comparison.md
│   └── campaign_timeline_comparison.md
│
├── 09_sources/
│   ├── sources.csv                ← 189 unique sources / 189 个唯一来源
│   └── data_dictionary_bilingual.md ← 双语数据字典（CSV 字段与词表中英对照）
│
├── 10_video_frames/               ← 145 段视频 → 106,295 个人脸裁片 → 172 帧精选画面
│   ├── frame_index.csv            ← 逐帧测量值 / per-frame measurements
│   ├── video_sources.csv          ← 每段视频的频道、日期与链接
│   ├── shot_index.csv             ← 1,073 个镜头关键帧（亮度、对比、锐度、色彩丰富度）
│   ├── video_visual_metrics.csv   ← 每段视频的剪辑率、平均镜头长度、运动量
│   ├── frames/ · faces/ · context/  ← curated stills, crops, staging frames
│   └── README.md                  ← method, validation, limits, rights
│
├── 11_speech_audio/               ← 演讲音频与交付测量 / speech delivery layer
│   ├── delivery_metrics.csv       ← 145 段视频：说话占比、停顿、响度、F0、语速、修辞计数
│   ├── speech_segments.csv        ← 2,542 个 60 秒窗口（节奏曲线）
│   ├── transcripts/               ← 78 份带时间码的字幕逐字稿
│   ├── plots/                     ← 93 张波形／VAD／F0 轨迹图
│   ├── audio/                     ← 93 份 64 kbps 单声道副本（本地工作集，未入 Git）
│   └── README.md                  ← method, measured delivery, limits, rights
│
├── site/                          ← offline bilingual website, derived from the files above
│                                    / 离线双语站点，由上述文件生成
└── _staging/                      ← gap registers, source mirrors, build/QA scripts
```

## 6.1 Static website / 静态站点

`site/index.html` is a derived reading view of the deliverables, generated by
`_staging/_lead_build_site.py`. It needs no server, no network connection and no external
assets: open the file directly in a browser.

`site/index.html` 是上述交付物的派生阅读视图，由 `_staging/_lead_build_site.py` 生成。不需要服务器、不需要联网、不加载任何外部资源，直接在浏览器中打开该文件即可。

- **Bilingual reading modes / 双语阅读模式** — every page switches between side-by-side EN/ZH,
  English only and Chinese only. English sits on the left and Chinese on the right, so the two
  versions can be compared paragraph by paragraph.
  每个页面可在「并排双语 / 仅英文 / 仅中文」三档之间切换；英文在左、中文在右，可逐段对照。
- **Client-side search / 站内检索** — the home page indexes the headings and text of all 45
  bilingual documents.
  首页对全部 45 份双语文档的标题与正文建立索引，输入即搜，不上传任何内容。
- **Datasets as tables / 数据集表格化** — each CSV becomes a filterable table with a download
  link to the raw file, and every table links back to the bilingual data dictionary.
  每个 CSV 渲染为可筛选表格，并提供原始文件下载链接；每张表都回链到双语数据字典。
- **Images load in page / 图片在页面内加载** — the two visual analyses open with an image index
  strip, and the gallery lists all 116 records split by candidate. Locally stored licensed copies
  render inline with photographer, date and licence; the 40 rights-reserved records show a
  "link only" card that jumps to the source page instead of hotlinking an unlicensed copy.
  两篇视觉分析页首各有一条影像索引条，图库按候选人分区列出全部 116 条记录。本地许可副本直接显示，注明摄影者、日期与许可；40 条保留所有权利的记录显示「仅链接」卡片，跳转来源页，不做未授权外链嵌入。
- **Video frames and shot structure / 视频帧与镜头结构** — the gallery shows 172 de-duplicated,
  face-matched frames with similarity, shot scale and timestamp; a companion page indexes 1,073
  scene keyframes and per-video cut rate, shot length, brightness and motion.
  图库陈列 172 帧去重后的识别画面（含相似度、景别与时间码）；另有一页列出 1,073 个镜头关键帧，以及每段视频的剪辑率、镜头长度、亮度与运动量。
- **Speech audio / 演讲音频** — 145 videos measured for speech share, pauses, loudness, F0 and
  caption-derived rate; 78 timed transcripts and 93 waveform/F0 plots are readable in-page. The
  64 kbps audio copies are a local working set and are not committed.
  145 段视频的说话占比、停顿、响度、基频与语速均已测量；78 份带时间码逐字稿与 93 张波形／F0 图可在页内阅读。64 kbps 音频副本属本地工作集，未纳入版本库。
- **Every source is clickable / 来源全可点击** — each `SRC-####` id anywhere in the prose becomes
  a chip that opens the original source in a new tab (with the publisher as tooltip), and bare
  URLs in the CSV tables are clickable too. 2,066 source chips and 1,371 outbound links across
  the site; the source registry table links both the id and the URL.
  正文中出现的每个 `SRC-####` 都变成可点击的编号标签，在新标签页打开原始来源（悬停显示媒体名）；CSV 表格中的网址同样可点击。全站共 2,066 个来源标签、1,371 个外链；来源总表中的编号与网址都带链接。
- **Derived by design / 派生视图定位** — the site is a view, never a source. Cite the Markdown
  and CSV files, never the website pages. Deleting `site/` loses only the view.
  站点只是视图，永远不是来源。引用时请指向 Markdown 与 CSV 文件，不要引用网页页面。删除 `site/` 只会失去视图，不损失任何数据。

## 7. Honest limits — read before using / 使用前必读的诚实局限

Full register: [`research_gaps.md`](research_gaps.md). The four that matter most:
完整登记见 [`research_gaps.md`](research_gaps.md)。最重要的四项如下：

1. **County-level election data is absent.** `county_results.csv` is intentionally
   header-only; county tabulation was published via JavaScript interactives that could
   not be executed, and the Wikipedia article carries only county *maps*. No county or
   regional analysis is possible from this archive.

   **县级选举数据缺失。** `county_results.csv` 有意只保留表头；县级统计通过 JavaScript 交互页面发布，无法抓取执行，而维基百科条目只有县级*地图*，没有数据表。因此本档案无法支撑任何县级或区域分析。
2. **Facial geometry, body proportions and clothing are still not measured.** Landmark
   detection was never available, so no distances, proportions or garment classification
   exist. What the frame layer does provide: 172 curated frames with face boxes in source
   pixels, shot scale, sharpness, brightness and a crude torso-colour proxy. Both visual
   analysis files state the limit and supply a measurement protocol for the human analyst.
   **Do not write appearance claims from this archive.**

   **面部几何、身体比例与着装仍未测量。** 始终没有可用的关键点检测，因此不存在距离、比例或服装分类数据。画面层提供的是：172 帧精选画面，附原始像素中的人脸框、景别、锐度、亮度，以及一个粗糙的躯干颜色代理值。两篇视觉分析文件均如实写明这一局限，并为人类研究者提供了完整的测量规程。**请勿依据本档案撰写任何外貌类论断。**
3. **The image target was not met for Talarico (18 vs a 60–100 target), and Paxton's pool
   is context-skewed (68 of 98 from AmericaFest).** Both facts are documented rather than
   padded; any comparative image use must carry them.

   **塔拉里科的影像数量未达目标（18 张，目标为每位候选人 60–100 张），帕克斯顿的图库则在情境上严重偏斜（98 张中 68 张来自 AmericaFest）。** 这两项事实均如实记录而非注水；任何对比性使用影像的场合都必须同时说明它们。
4. **No quotation was verified word-by-word against the audio, though delivery is now
   measured.** Every quotation still comes from printed text. What changed: 145 videos were
   decoded and measured in `11_speech_audio/` (speech share, pause structure, caption-based
   rate, indicative F0), and 78 timed caption transcripts can be used to spot-check wording.
   Emotion, sincerity, emphasis and audience reaction remain unmeasured and unclaimable.

   **引语尚未逐字与音频核对，但交付方式已有测量。** 每一句引语仍来自文字报道。变化在于：`11_speech_audio/` 已解码并测量 145 段视频（说话占比、停顿结构、由字幕推算的语速、仅作指示的基频），另有 78 份带时间码的字幕逐字稿可用于抽查措辞。情绪、真诚度、重音与观众反应仍不可测、不可断言。

Additional documented cautions: FEC Schedule E totals and AdImpact ad-spend totals differ
by roughly an order of magnitude and **must never be summed**; four different Talarico
"totals" measure different things; "three debates scheduled" (Washington Examiner) never
happened; Reuters is absent from the media corpus; Paxton's policy rows are thinner
because his campaign site served no issue pages, not because he talked less.

其他有据可查的警告：FEC 的 Schedule E 独立支出总额与 AdImpact 的广告投放总额相差约一个数量级，**绝不可相加**；塔拉里科存在四种不同的"总额"，各自衡量口径不同；《华盛顿观察家报》所称"三场已排定辩论"从未发生；媒体语料中缺少路透社；帕克斯顿的政策条目较少，原因是他竞选网站未提供议题页面，而不是他谈得更少。

## 8. Data conventions / 数据规范

`_research_conventions.md` is the binding contract. Key points:
`_research_conventions.md` 是具约束力的契约。要点如下：

- **IDs:** `TAL-EVT-####`, `PAX-EVT-####`, `JNT-EVT-####`, `TAL-SPC-####`, `PAX-SPC-####`,
  `TAL-AD-####`, `PAX-AD-####`, `EXT-AD-####`, `TAL-IMG-####`, `PAX-IMG-####`, `SRC-####`.
  **编号体系：** 同上，保持英文原样，不得改写。
- **`unknown` is a value.** It means "not established," never "zero" and never "no."
  **`unknown` 是有效取值。** 它表示"未能查明"，绝不是"零"，也绝不是"否"。
- **Three-layer purpose:** `stated_purpose` (what they said) / `observable_function` (what
  it was) / `analyst_interpretation` (inference, prefixed `INTERPRETATION:`).
  **三层目的规则：** `stated_purpose`（宣称目的）／`observable_function`（实际观察到的功能）／`analyst_interpretation`（推断，前缀 `INTERPRETATION:`）。
- **Verification vocabulary:** `verified` / `partially verified` / `conflicting sources` /
  `unverified`. Conflicts are recorded as conflicts, not resolved by preference.
  **核实词表：** `verified`（已核实）／`partially verified`（部分核实）／`conflicting sources`（来源冲突）／`unverified`（未核实）。冲突以冲突记录，不按偏好取舍。
- **CSV format:** UTF-8, RFC-4180 quoting, header row exact, no blank cells.
  **CSV 格式：** UTF-8、RFC-4180 引号规则、表头完全一致、无空白单元格。

Distribution of verification status across principal datasets:
主要数据集的核实状态分布：

| Dataset / 数据集 | verified | partially verified | conflicting | unverified |
|---|---|---|---|---|
| `campaign_events.csv` (93) | 23 | 66 | 3 | 1 |
| `policy_positions.csv` (146) | 90 | 53 | 0 | 3 |
| `speech_archive.csv` (32) | 12 | 12 | 0 | 8 |
| `image_archive.csv` (116) | 101 | 15 | 0 | 0 |
| `advertisements.csv` (23) | 13 | 10 | 0 | 0 |
| `campaign_finance.csv` (69) | 49 | 17 | 2 | 1 |

`media_coverage.csv` carries `source_tier` and `reliability_notes` instead of a single
status field, by design.
`media_coverage.csv` 按设计不设单一核实状态字段，而是使用 `source_tier` 与 `reliability_notes`。

**Note on CSV language / 关于 CSV 语言：** the CSV datasets keep English field names and
controlled-vocabulary values so that they remain machine-readable and schema-stable. Their
Chinese equivalents are provided in
[`09_sources/data_dictionary_bilingual.md`](09_sources/data_dictionary_bilingual.md).

CSV 数据集保留英文字段名与受控词表取值，以保证机器可读与结构稳定；其中文对照见 [`09_sources/data_dictionary_bilingual.md`](09_sources/data_dictionary_bilingual.md)。

## 9. Sources and sourcing policy / 来源与取源规则

`09_sources/sources.csv` holds **189 unique sources** after URL-level de-duplication of
206 agent-registry rows (17 URLs were independently retrieved by more than one stream —
a cross-retrieval signal, recorded in `reliability_notes`).

`09_sources/sources.csv` 在 206 条代理登记记录按 URL 去重后保留 **189 个唯一来源**（其中 17 个 URL 被不止一条研究线索独立抓取到——这是一种交叉印证信号，记录在 `reliability_notes` 中）。

Source tiers: **T1 = 27**, **T2 = 130**, **T3 = 29**, plus **3 pointer-only records**
(stories whose existence is documented but whose URL was not captured — flagged and not
usable as citations until recovered). Types include news articles (138), official campaign
pages (15), news video (10), official government (4), live blogs (4), analysis (4),
transcripts (3) and event pages (3).

来源层级：**T1 = 27**、**T2 = 130**、**T3 = 29**，另有 **3 条仅指针记录**（确认报道存在但未抓到 URL，已标注，在补齐链接前不可作为引用依据）。类型包括新闻报道（138）、竞选官方页面（15）、新闻视频（10）、政府官方（4）、实时博客（4）、分析（4）、文字记录（3）与活动页面（3）。

**Copyright policy applied throughout:** text quotes are short and attributed; images are
either (a) public-domain or Creative Commons files downloaded with full licence/attribution
metadata in `image_archive.csv`, or (b) all-rights-reserved news photographs recorded
**link-and-credit only**, never copied. 15 rows are link-only, 3 are public-domain, 98 are
licensed copies with attribution.

**全程执行的版权规则：** 文字引用简短并注明出处；影像分两类——（a）公有领域或知识共享许可文件，下载并在 `image_archive.csv` 中记录完整许可与署名信息；（b）保留所有权利的新闻照片，**仅记录链接与署名**，从不复制。其中 15 行为仅链接、3 行为公有领域、98 行为带署名的许可副本。

## 10. Reproducing and re-validating / 复现与重新校验

All scripts are in `_staging/` and run with the bundled Python (`Pillow`, `NumPy`; no
network libraries beyond `urllib`):
全部脚本位于 `_staging/`，使用随包 Python 运行（含 `Pillow`、`NumPy`；除 `urllib` 外无网络依赖）：

| Script / 脚本 | Purpose / 用途 |
|---|---|
| `_lead_validate.py` | Header/vocabulary/blank-cell validation of all 12 CSVs; exits non-zero on failure / 校验全部 12 个 CSV 的表头、词表与空单元格；失败时返回非零 |
| `_lead_merge_sources.py` | De-duplicates agent source registries into `09_sources/sources.csv` and rewrites local citation tokens to `SRC-####` / 合并去重各线索来源登记，并把本地引用标记改写为 `SRC-####` |
| `_lead_visual_collect.py` | Throttled, batched Wikimedia Commons metadata collection / 限速批量采集维基共享资源元数据 |
| `_lead_visual_build.py` | Builds `image_archive.csv` from the Commons cache; downloads licensed copies / 由缓存生成影像档案并下载许可副本 |
| `_lead_visual_news.py` | Appends verified news-photo credit records as link-only rows / 以仅链接行追加已核实的新闻照片署名记录 |
| `_lead_visual_metrics.py` | Computes sharpness/tonality/frame measurements into `_staging/_visual_metrics.csv` / 计算清晰度、影调与画幅测量值 |

Current state: `_lead_validate.py` reports **0 hard failures, 0 soft warnings**.
当前状态：`_lead_validate.py` 报告 **0 项硬性失败、0 项软性警告**。

## 11. If you want to extend this archive / 如需扩展本档案

Highest-value closures, in order: (1) Texas Secretary of State county canvass →
fills `county_results.csv` and certifies percentages; (2) FEC line-item filings via a real
OpenFEC key → "as filed" money; (3) the campaigns' Eventbrite pages → completes both tour
lists; (4) 8–12 full speech videos → real transcripts and timecodes; (5) an image-capable
analyst → executes the appearance protocol already written.

按价值排序的补齐路径：（1）德州州务卿县级选举认证数据 → 填充 `county_results.csv` 并把百分比升级为"认证口径"；（2）使用真实 OpenFEC 密钥获取 FEC 逐条申报 → 资金数据升级为"按申报口径"；（3）两阵营的 Eventbrite 活动页面 → 补全双方巡回路线清单；（4）8–12 场演讲完整视频 → 生成真实文字稿与时间码；（5）具备图像能力的分析者 → 执行已写好的外貌测量规程。

## 12. Licence and reuse note / 许可与复用说明

Compiled research materials for internal analytical use. Third-party text and images
remain the property of their publishers and are cited, not redistributed, except for the
98 Creative Commons and 3 public-domain images whose licence and attribution are recorded
per row in `image_archive.csv`. Verify the licence before republishing any local copy.

本档案为内部分析用途汇编的研究材料。第三方文字与影像的版权仍属其出版方，档案仅作引用、不作再分发；例外是 98 张知识共享许可与 3 张公有领域影像，其许可与署名信息逐行记录在 `image_archive.csv` 中。重新发布任何本地副本前请先核对许可条款。
