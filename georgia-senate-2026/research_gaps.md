---
title: Research gaps
title_zh: 研究缺口
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Lists every gap that limits use of the archive, its cause, and what would close it.
---

## County-level returns / 县级计票

Gap: `07_electoral_context/county_results.csv` has a header and no rows, so no county vote totals, shares or margins exist in the archive.
Cause: the Secretary of State results site is an Angular single-page application; two guessed API paths returned 404; NBC's county widget renders on the client and its vote cells read "0".
Close it: obtain the certified county canvas from the Secretary of State, or the AP's county feed, or a spreadsheet published by a county-level outlet. SRC-0003

缺口：`07_electoral_context/county_results.csv` 仅有表头，档案中没有县级票数、得票率或差额。
原因：州务卿结果网站为 Angular 单页应用；两个推测的 API 路径均 404；NBC 县级组件在客户端渲染，票数单元显示"0"。
补足：取得州务卿认证的县级计票、美联社县级数据源，或地方媒体公布的表格。SRC-0003

## Advertising creatives / 广告素材

Gap: `advertisements.csv` records buys and titles but no ad video, narration or length; two rows describe spending programmes rather than ads.
Cause: no ad library (Meta, Google, Snap) was accessible, and the outlets that covered the ads described them only in prose.
Close it: pull the Meta and Google political ad libraries for both campaigns, and the Senate Leadership Fund's FCC public files. SRC-0022 SRC-0050

缺口：`advertisements.csv` 记录了购买与标题，但没有广告视频、旁白或时长；其中两行描述的是投放计划而非具体广告。
原因：无法访问广告库（Meta、Google、Snap），报道广告的媒体仅以文字描述。
补足：调取两阵营的 Meta 与 Google 政治广告库，以及参议院领导基金的 FCC 公开文件。SRC-0022 SRC-0050

## Event time, venue and crowd / 活动时间、场地与人数

Gap: 26 of 32 event rows lack a time of day and 19 lack a named venue; only four carry a crowd estimate, two of them campaign-supplied.
Cause: Georgia Recorder and GPB report selectively, and the campaigns' event calendars were not archived.
Close it: local weekly newspapers, pool reports, and archived campaign event pages.

缺口：32 行活动记录中 26 行没有具体时间、19 行没有明确场地；仅 4 行有人数估计，其中 2 个由竞选团队提供。
原因：Georgia Recorder 与 GPB 为选择性报道，竞选活动日历未被存档。
补足：地方周报、随行记者报道与存档的竞选活动页面。

## Collins positions on Medicaid, agriculture, tax and education / 柯林斯在医疗补助、农业、税收与教育上的立场

Gap: five Collins position rows are `unverified` because the only retrieved statement is an Ossoff attack.
Cause: Collins's campaign site was not retrievable and interviews did not cover these issues.
Close it: his campaign issues page (archived), House floor statements, and the Atlanta Press Club debate transcript.

缺口：柯林斯有五条立场记为 `unverified`，因为唯一可获取的表述来自奥索夫的攻击。
原因：柯林斯竞选网站无法获取，采访未涉及这些议题。
补足：其竞选议题页（存档）、众议院院会发言、亚特兰大新闻俱乐部辩论逐字稿。

## Social media content / 社交媒体内容

Gap: X returned a login shell for `@ossoff`, so post text, dates and engagement are missing for both accounts.
Cause: platform login wall.
Close it: the Wayback Machine's captures of the profiles, and the candidates' TikTok and Instagram archives.

缺口：X 对 `@ossoff` 仅返回登录外壳，两个账号的帖文文本、日期与互动数据均缺失。
原因：平台登录墙。
补足：Wayback Machine 的账号存档，以及候选人的 TikTok 与 Instagram 存档。

## Vote-type and precinct data / 投票方式与 precinct 数据

Gap: no early/absentee/election-day breakdown and no precinct returns.
Cause: not published in any retrieved source; the Secretary of State's site would carry both.
Close it: the county canvass files and the state's absentee voter file.

缺口：没有提前投票/邮寄/选举日分解，也没有 precinct 计票。
原因：已获取来源均未公布；州务卿网站应载有这两类数据。
补足：县级计票文件与州缺席选民档案。
