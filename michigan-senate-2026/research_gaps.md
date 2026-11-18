---
title: Research gaps
title_zh: 研究缺口
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Fourteen gaps are listed with their cause and what would close each; none is a guess dressed as a finding.
---

## How to read this file

Each gap below states what is missing, why it is missing (the concrete retrieval failure, not "sources were unavailable"), and what would close it. Gaps are ordered by how much they weaken the archive, not by how easy they would be to fix. The retrieval record behind every cause is in `_staging/fetch_log.csv`, which holds 168 attempts: 101 returned HTTP 200, 66 failed with 401, 402, 403, 404, 429, a TLS error, an empty response or a refused connection, and one row is a `local` copy of the repository's pre-downloaded wikitext.

中文：下列每处缺口均说明缺什么、为何缺失（具体的获取失败原因，而非笼统的“来源不可得”），以及如何才能补足。缺口按其对档案的削弱程度排序，而非按修补难度排序。每一处原因背后的抓取记录见 `_staging/fetch_log.csv`：共 168 次尝试，101 次返回 HTTP 200，66 次因 401、402、403、404、429、TLS 错误、空响应或连接被拒而失败，另有一行为仓库预先下载的维基文本的 `local` 复制记录。

## 1. No county-level results table

`07_electoral_context/county_results.csv` is header-only. No retrieved source published county vote totals for this election; the race article carries county findings only as prose (30 of 83 counties, five flips). **Cause:** the Michigan Secretary of State results pages returned HTTP 403 on both the general and primary endpoints [SRC-0006] [SRC-0007], and the county-level export sits behind the same host. **What would close it:** a working Department of State county results export, or the AP's county file.

中文：`07_electoral_context/county_results.csv` 仅有表头。已取得的来源均未公布本次选举的县级票数；该选举条目仅以文字叙述县级结果（83 县中 30 个、五个翻转县）。原因：密歇根州州务卿的大选与初选结果页面均返回 HTTP 403 [SRC-0006] [SRC-0007]，县级导出文件位于同一主机之后。补足方式：州务卿的县级结果导出文件，或美联社的县级数据文件。

## 2. No advertising content of any kind

`05_campaign_media/advertisements.csv` has six rows, but only one is a described spot; the other five record flights or campaigns without scripts, visuals or buy data. **Cause:** both campaign websites returned HTTP 403 [SRC-0082] [SRC-0083]; no AdImpact release was retrievable; YouTube ad libraries were not queried in this pass; and the outlets that described the AIPAC-linked ad (CNN, Bridge Michigan) described its content but not its script [SRC-0032]. **What would close it:** the AdImpact or Medium Buying archives for the Michigan media markets, and the FEC's independent-expenditure files with creative attachments.

中文：`05_campaign_media/advertisements.csv` 有六行，但仅一条是已描述的具体广告，其余五条只记录投放批次或广告活动，无脚本、画面或投放数据。原因：两个竞选网站均返回 HTTP 403 [SRC-0082] [SRC-0083]；未能取得任何 AdImpact 发布；本轮未查询 YouTube 广告库；描述 AIPAC 关联广告的媒体（CNN、Bridge Michigan）描述了内容而非脚本 [SRC-0032]。补足方式：密歇根各媒体市场的 AdImpact 或 Medium Buying 档案，以及附有创意的 FEC 独立支出文件。

## 3. No social-media engagement data

The six rows in `05_campaign_media/social_media.csv` record quoted posts and account references; none has a verified URL for a specific post, and none has likes, shares or views. **Cause:** x.com requires authentication and blocked automated access; the campaign accounts were not retrievable; and the quotes came from news reports rather than from the platforms. **What would close it:** API access to the candidates' accounts, or archived snapshots (Wayback Machine captures of the profile pages) for the campaign period.

中文：`05_campaign_media/social_media.csv` 的六行记录被引用的帖文与账号引用；其中没有任何一条拥有可验证的具体帖文链接，也没有点赞、转发或浏览量。原因：x.com 需要身份验证并阻断自动访问；竞选账号无法取得；引语来自新闻报道而非平台本身。补足方式：候选人账号的 API 访问权限，或竞选期间的存档快照（如 Wayback Machine 的账号页面存档）。

## 4. No visual description of any image

Every `framing`, `camera_angle`, `clothing_notes`, `face_visibility` and `body_visibility` cell in `04_visual_archive/image_archive.csv` is `unknown` except where the Commons description states it (the logo's lock-up). **Cause:** the compiler of this archive cannot inspect images (the model has no image input), and the retained Commons metadata describes subject and licence but not framing or clothing. **What would close it:** a human or vision-capable pass over the thirteen files, which are stored locally and could be described in an hour.

中文：`04_visual_archive/image_archive.csv` 中除 Commons 描述明确写出的项目（标志的排布方式）外，所有 `framing`、`camera_angle`、`clothing_notes`、`face_visibility`、`body_visibility` 单元格均为 `unknown`。原因：编制本档案的模型无法查看图像（无图像输入能力），而留存的 Commons 元数据描述的是主题与许可，而非构图或着装。补足方式：由人工或具备视觉能力的流程对十三个本地文件进行一次描述，约需一小时。

## 5. No general-election photograph under a free licence

The archive holds no Michigan campaign photograph of either candidate from 2026 under PD/CC0/CC BY/CC BY-SA. **Cause:** Commons' El-Sayed category holds only campaign logos after the 2025 campus photographs, and the Rogers category's newest usable files are 2019 and older; three additional files were refused twice with HTTP 429 by upload.wikimedia.org [SRC-0084] [SRC-0086]. **What would close it:** a licensed photograph from a 2026 event, or permission from a Michigan outlet's photo desk.

中文：本档案没有任何一张 2026 年密歇根竞选现场、且属 PD/CC0/CC BY/CC BY-SA 的两位候选人照片。原因：Commons 的赛义德分类在 2025 年校园照片之后仅有竞选标志；罗杰斯分类中最新可用文件为 2019 年及更早；另有三份文件被 upload.wikimedia.org 两次以 HTTP 429 拒绝 [SRC-0084] [SRC-0086]。补足方式：取得 2026 年某场活动的授权照片，或获得密歇根媒体摄影部门的许可。

## 6. No transcripts and no timestamps

All thirteen speech rows carry `[unknown]` for every quote's timestamp, and all eleven video rows record `transcript_available: no`. **Cause:** YouTube video pages were not retrieved in this pass (only their URLs were taken from the race article's debate table), and no outlet published a full transcript. **What would close it:** downloading the nine debate videos and running transcription, which would also supply the timestamps and crowd reactions this archive lacks.

中文：十三条演说记录中每条引语的时间戳均为 `[unknown]`，十一条视频记录均为 `transcript_available: no`。原因：本轮未取得 YouTube 视频页面（仅从该选举条目的辩论表取得链接），也没有媒体刊出完整文字稿。补足方式：下载九场辩论视频并进行转写，可同时补齐本档案所缺的时间戳与现场反应。

## 7. No campaign schedule for either candidate

The events file was reconstructed from news reports and photograph captions. **Cause:** neither campaign published a retrievable public calendar, and both sites returned HTTP 403 [SRC-0082] [SRC-0083]. **What would close it:** archived snapshots of the events pages, or the local television archives for September and October 2026.

中文：事件表系依据新闻报道与图片说明重建。原因：两位候选人均未公布可取日程，两个网站均返回 HTTP 403 [SRC-0082] [SRC-0083]。补足方式：活动页面的存档快照，或 2026 年 9 至 10 月的本地电视档案。

## 8. Paywalled Michigan outlets

The Detroit News and Detroit Free Press returned HTTP 402 throughout, so their reporting — including the $243 million total that anchors the "most expensive race" claim — is known only through the headline and through other outlets' citation of it [SRC-0073]. **Cause:** metered paywalls. **What would close it:** a subscription or library access to the two outlets' archives.

中文：《底特律新闻》与《底特律自由新闻》全程返回 HTTP 402，因此其报道——包括支撑“最昂贵选举”论断的 2.43 亿美元总额——仅能通过标题与其他媒体的转引得知 [SRC-0073]。原因：计量付费墙。补足方式：订阅或图书馆权限，以访问两家媒体的档案。

## 9. National outlets blocked

AP (403), Politico (403), The Hill (403), Reuters (401), The New York Times (TLS errors) and The Wall Street Journal were unreachable, which is why the archive has no AP write-through, no Politico primary-night reporting and no NYT/Siena release. **Cause:** bot protection and, for the Times, a TLS handshake failure. **What would close it:** an authenticated fetch service or manual retrieval of the specific articles.

中文：美联社（403）、Politico（403）、《国会山报》（403）、路透社（401）、《纽约时报》（TLS 错误）与《华尔街日报》均无法访问，因此本档案没有美联社的完整通稿、没有 Politico 的初选之夜报道、也没有 NYT/Siena 的发布稿。原因：反爬保护，以及《纽约时报》的 TLS 握手失败。补足方式：带身份验证的抓取服务，或手工获取具体文章。

## 10. FEC pages are client-rendered

The FEC candidate and finance pages returned HTML whose tables are drawn by JavaScript, so no figure was read from the Commission itself; all finance rows are transcribed from the race article's tables that cite the FEC, and every one is `partially verified` [SRC-0004]. **Cause:** single-page rendering. **What would close it:** the FEC's bulk data files (`/data/bulk-downloads/`) or the OpenFEC API, which return the same figures as CSV or JSON.

中文：联邦选举委员会的候选人与财务页面返回的表格由 JavaScript 渲染，因此未从委员会本身读到任何数字；所有财务行均转录自该选举条目引用 FEC 的表格，且全部标为 `partially verified` [SRC-0004]。原因：单页渲染。补足方式：FEC 的批量数据文件或 OpenFEC API，二者以 CSV 或 JSON 返回同样的数字。

## 11. Minor-party and down-ballot context

The archive records the four minor candidates' vote totals but no positions, campaigns or nominations process detail. **Cause:** no retrieved source covered them beyond the results table [SRC-0001]. **What would close it:** the Libertarian, Green, UST and Natural Law state parties' convention records.

中文：本档案记录四位小党候选人的得票总数，但未涉及其立场、竞选活动或提名程序细节。原因：除结果表外，无任何已取得来源报道他们 [SRC-0001]。补足方式：自由党、绿党、美国纳税人党与自然法党州级代表大会的记录。

## 12. No exit polls or vote-movement data

The archive can describe the coalition's geography but cannot explain it. **Cause:** no exit poll for this race was published in any retrieved source, and the network exit poll tables were not reachable. **What would close it:** the Edison Research exit poll for Michigan, or the Pew validated-voter file.

中文：本档案可以描述联盟的地理分布，却无法解释其成因。原因：已取得的来源中没有任何本次选举的出口民调，全国性出口民调表格亦无法访问。补足方式：Edison Research 的密歇根出口民调，或皮尤的已验证选民文件。

## 13. One unresolved date and one unresolved count

Two conflicts are recorded rather than resolved: El-Sayed's launch date (April 19 per Wikipedia, April 17 per the Semafor report that describes it) [SRC-0002] [SRC-0070], and the number of AIPAC-hosted fundraisers Rogers attended in August 2026 (four per Wikipedia, three per The American Prospect) [SRC-0003] [SRC-0073]. **Cause:** both conflicts sit behind the paywalls and 403s listed above. **What would close them:** the original launch-day reporting and the FEC/itemised fundraiser disclosures.

中文：两处分歧被记录而非解决：赛义德的启动日期（维基百科为 4 月 19 日，描述该事的 Semafor 报道为 4 月 17 日）[SRC-0002] [SRC-0070]；以及罗杰斯 2026 年 8 月出席的 AIPAC 筹款会场次（维基百科称四场，The American Prospect 称三场）[SRC-0003] [SRC-0073]。原因：两处分歧均位于上文所列的付费墙与 403 之后。补足方式：启动当日的原始报道与 FEC/逐项筹款披露。

## 14. No Rogers policy documents

Rogers' positive agenda is known almost entirely through debate answers, three written statements and the campaign homepage's message line. **Cause:** the campaign site returned HTTP 403 [SRC-0082] and no policy paper was quoted at length by any retrieved outlet. **What would close it:** archived PDFs of the campaign's plans, which the September 17 statement says exist ("I have released plans to ma[k]e that happen") [SRC-0022].

中文：罗杰斯的积极议程几乎只能通过辩论回答、三份书面声明与竞选主页的信息行得知。原因：竞选网站返回 HTTP 403 [SRC-0082]，且无任何已取得媒体长段引用其政策文件。补足方式：该竞选方计划的存档 PDF——9 月 17 日的声明明言这些计划已发布（“我已发布实现这一点的计划”）[SRC-0022]。
