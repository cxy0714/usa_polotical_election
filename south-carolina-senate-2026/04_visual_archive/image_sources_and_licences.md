# 04 · Visual archive / 影像档案

Every row in `image_archive.csv` is one photograph of Andrews or Graham, with the page it came from,
the licence under which it may be held, and the file on disk when the archive actually has a copy.

`image_archive.csv` 的每一行都是一张安德鲁斯或格雷厄姆的照片，附来源页面、可持有的许可、以及（真的拿到文件时的）本地路径。

## Where the photographs come from / 照片来源

| Source / 来源 | Rows / 行数 | Licence / 许可 | Stored? / 是否存盘 |
|---|---|---|---|
| Wikimedia Commons | 48 | Public domain, CC0, CC BY 4.0 | 是 / yes |
| SC Daily Gazette (States Newsroom) | 7 | CC BY-ND 4.0 | 是，未裁剪 / yes, unmodified |

Totals by candidate: Graham 36, Andrews 19. That is the whole public-domain-plus-CC pool for these
two people as of 2026-11-18 — not a sampling choice.

按候选人：格雷厄姆 36 张，安德鲁斯 19 张。这就是截至 2026-11-18 这两位候选人可公开持有（公有领域 + CC）的全部照片池，不是抽样选择的结果。

## Why so few / 为什么这么少

Both candidates entered national photography late: Andrews announced on 2025-05-29 and has been
photographed mainly by county Democratic parties; Darline Graham was appointed on 2026-07-13, so her
photographic record begins with an official portrait, a swearing-in frame and a handful of 2026 news
assignments. There is no long tenure to mine, which is the difference from the Texas case, where
Paxton's decade as attorney general supplies 98 rows.

两位候选人进入全国性影像视野都很晚：安德鲁斯 2025-05-29 才宣布参选，照片主要来自县民主党部；达琳·格雷厄姆
2026-07-13 才被任命，影像记录从官方肖像、宣誓就职和少量 2026 年新闻拍摄开始。没有长期任期可挖——这正是与德州案例
的差别：帕克斯顿十年总检察长任内提供了 98 行。

## Sources probed and rejected / 已探查但无法采用的渠道

| Channel / 渠道 | Result / 结果 |
|---|---|
| Wikimedia Commons, category + search + the two Wikipedia articles' images | 20 files for Andrews, 20 for Graham; all already archived — exhausted / 已穷尽 |
| Openverse (aggregates Flickr, museums, etc.) | 0 results for either name / 两个名字均 0 结果 |
| State Newsroom network (SC Daily Gazette) | 7 photographs usable; 9 further candidate-article photos failed the face gate / 7 张可用，另 9 张未通过人脸校验 |
| senate.gov delegation page | page lists members, exposes no portrait files / 不提供肖像文件 |
| graham.senate.gov | host unreachable from this network / 本网络不可达 |
| congress.gov | HTTP 403 without a session / 无会话时 403 |
| annieandrews.com, campaign social accounts | JavaScript-rendered and all rights reserved; nothing storable / JS 渲染且版权保留，不可存盘 |
| AP, Reuters, Post and Courier, The State, Greenville News, TV affiliates | all rights reserved; recordable as link-and-credit rows only, never as files / 版权保留，只能记「仅链接与署名」行 |

The Texas archive keeps 15 such link-only rows. For South Carolina none were added yet, because a
caption cannot be written without seeing the photograph, and the model used here has no vision. That
is a gap to close by hand, not by inference.

德州档案保留了 15 行这类「仅链接」记录。南卡尚未添加，因为看不到照片就写不出说明，而本模型没有视觉能力。
这处缺口应当人工补齐，而不是靠推断填。

## Two gates before a file is stored / 存盘前的两道校验

1. **Relevance.** The article must be about the candidate (slug or title), and the licence must permit
   storage: public domain, CC0, CC BY, CC BY-SA, or CC BY-ND with no modification.
2. **Identity.** The photograph must contain that candidate's face according to the same SFace test
   used for the video frames: cosine ≥ 0.55 against the archive's reference photographs, with a 0.05
   margin over the other candidate. The stricter floor is used here because a news photograph carries
   no context — the first harvest accepted a picture of Lindsey Graham standing beside Tim Scott as
   "Annie Andrews" at cosine 0.367, which is why the gate was raised.

1. **相关性**：文章必须关于该候选人，且许可允许存盘（公有领域、CC0、CC BY、CC BY-SA，或允许但不改动的 CC BY-ND）。
2. **身份**：照片里必须是该候选人的脸，判定沿用视频帧那套 SFace 检验：相对档案参照照余弦 ≥ 0.55，且领先另一候选人 0.05。
   这里用更严的门槛，因为新闻照片没有上下文——第一轮曾把「林赛·格雷厄姆与蒂姆·斯科特合影」按 0.367 判成安德鲁斯，
   门槛因此上调。

CC BY-ND forbids derivatives, so news files are stored exactly as published: no cropping, no resizing.
The `notes` column carries the article title the file came from.

CC BY-ND 禁止演绎，所以新闻照片按原样保存：不裁剪、不缩放。`notes` 列记录文件出自哪篇文章。

## Scripts / 脚本

| Script | What it does |
|---|---|
| `_staging/_lead_scout_images.py` | read-only probe of Commons search, categories and both Wikipedia articles |
| `_staging/_lead_probe_images.py` | read-only probe of official, campaign and news pages, with licence hints |
| `_staging/_lead_harvest_states_newsroom.py` | collects SC Daily Gazette candidate articles and their photographs into a review CSV |
| `_staging/_lead_add_images.py` | downloads, face-verifies and appends rows (images + source registrations) |
| `_staging/_lead_reverify_news_images.py` | re-checks existing news rows at the strict 0.55 gate and drops failures |
| `_staging/_lead_restore_sources.py` | keeps the news source rows in `_staging/_lead_sources_images.csv`, which `_lead_merge_sources.py` reads |
