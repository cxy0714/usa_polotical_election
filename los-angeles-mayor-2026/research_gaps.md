---
title: "Research Gaps — 2026 Los Angeles Mayoral Case"
title_zh: "研究缺口 — 2026 年洛杉矶市长案例"
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: "Every gap below is a real absence in the retrieved record, with its cause and the specific document that would close it; none is a placeholder for work not attempted."
---

# Research gaps / 研究缺口

## A. Official records / 官方记录

**G1. No official canvass for either round.** The county registrar (`results.lavote.gov`,
`www.lavote.gov`, `content.lavote.gov`) returned `URLError` on every attempt, and the city clerk's
election pages publish candidate lists rather than vote totals. Consequence: the primary rests on the
NBC News results page [SRC-0021] and the runoff on the Wikipedia table [SRC-0001], which is why the
runoff rows are `partially verified`. Closing it: the Los Angeles County Registrar-Recorder's certified
statement of votes, or the city clerk's official canvass PDF for the Nov. 3, 2026 election.

**G1. 两轮选举均无官方计票文件。** 县选务处（`results.lavote.gov`、`www.lavote.gov`、
`content.lavote.gov`）全部返回 `URLError`；市书记官选举页面只公布候选人名单而非票数。后果：
初选依赖 NBC News 结果页 [SRC-0021]，决选依赖维基百科表 [SRC-0001]，因此决选行标为
`partially verified`。弥补方式：洛县选务处认证计票声明，或市书记官 2026-11-03 官方计票 PDF。

**G2. Two one-vote discrepancies are unresolved.** NBC News gives Juanita Lopez 13,033 and Bryant
Acosta 3,471; the Wikipedia table gives 13,032 and 3,470 (and a total of 853,892 instead of 853,894).
Both tables are internally self-consistent. The archive records the NBC figures, flags both rows
`conflicting sources`, and does not adjust anything. Closing it: the official canvass (see G1).

**G2. 两处一票差异未解决。** NBC News 记 Juanita Lopez 13,033、Bryant Acosta 3,471；维基表记
13,032 与 3,470（总数为 853,892 而非 853,894）。两表内部各自自洽。档案采用 NBC 数字，两行标
`conflicting sources`，不作任何调整。弥补方式：官方计票（见 G1）。

**G3. Write-in candidates are certified but uncounted here.** The city clerk lists two certified write-ins
(griselda diaz, misael ortega) whose votes do not appear in any retrieved results table, so the published
total excludes them and the archive cannot state their share. Closing it: the canvass's write-in
appendix.

**G3. 补写候选人已获认证但票数缺失。** 市书记官列出两名获认证的补写候选人（griselda diaz、
misael ortega），其票数不见于任何已获取结果表，故公布总数不含其票，档案也无法给出份额。
弥补方式：计票文件的补写附录。

**G4. No turnout or registration denominator.** No retrieved source published ballots cast, registered
voters, or turnout rate for either round; the Wikipedia infobox carries `volume = 0`. The archive records
turnout as `unknown` in `election_context.md` rather than computing a share from an assumed denominator.

**G4. 缺少投票率与登记选民基数。** 任何已获取来源都未公布两轮的投票数、登记选民数或投票率；
维基信息框为 `volume = 0`。档案在 `election_context.md` 中将投票率记为 `unknown`，不以假设基数
反推比例。

## B. Geography / 地理分布

**G5. No precinct, council-district or neighbourhood results.** The L.A. Times precinct map is both
metered and client-rendered [SRC-0053]; nothing else publishes sub-city totals. Consequence:
`county_results.csv` is a header-only file — the race is citywide, so a county table would be a
category error — and no district-level claim is made anywhere in the archive. What would close it: the
registrar's precinct-level returns, which would allow the "Raman won renters' districts, Bass won
homeowner districts" hypothesis to be tested instead of asserted.

**G5. 缺少选区、市议会分区或社区级结果。** 洛杉矶时报的选区地图既有付费墙又由前端渲染 [SRC-0053]，
其他来源不发布市域以下合计。后果：`county_results.csv` 仅为表头文件（该选举为全市范围，县级表
属范畴错误），档案中不作任何分区级论断。弥补方式：县选务处的选区级计票，可用以检验而非断言
"Raman 赢租客区、Bass 赢自住业主区"的假设。

## C. Broadcast and transcript material / 广播与文字稿

**G6. No debate transcripts.** Five debates/forums have full video (three via YouTube uploads by the
hosts, two via NBCLA), but none has a published transcript, and this build did not transcribe audio.
Consequence: `speech_archive.csv` quotes only what written reporting quoted verbatim; several rows
carry `major_quotes = unknown`. Closing it: manual transcription of `VID-0001` … `VID-0005`, or the
hosts' caption tracks.

**G6. 辩论无文字稿。** 五场辩论/论坛均有完整视频（三场由主办方上传 YouTube，两场由 NBCLA），
但均无公开文字稿，本次构建也未转写音频。后果：`speech_archive.csv` 只引用书面报道的逐字引语，
数行 `major_quotes` 为 `unknown`。弥补方式：人工转写 `VID-0001`…`VID-0005`，或获取主办方字幕轨。

**G7. The Jewish-community forum's substantive exchange is not transcribed.** LAist hosts the full
1:39:47 audio [SRC-0033] and describes a difference over Gaza, but the archive could not retrieve
verbatim quotes, so RAM-POL-0016 is `partially verified`. Closing it: transcribing the audio.

**G7. 犹太社区论坛的实质交锋未转写。** LAist 提供 1:39:47 完整音频 [SRC-0033] 并描述双方对加沙
问题的差异，但档案未能取得逐字引语，故 RAM-POL-0016 为 `partially verified`。弥补方式：转写音频。

**G8. Television and digital ads have no transcripts and mostly no video files.** Only Raman's
Emmy-themed spot is available in full (its YouTube upload) [SRC-0044]; the Bass ICE spot, the police
union's "Doesn't Get It" and the Streets For All spots are known from the L.A. Times newsletter's
description, so `main_visual_elements` and `narration_soundtrack` are the newsletter's reporting rather
than the archive's viewing. Closing it: the Ethics Commission's independent-expenditure filings, which
attach ad scripts and buy schedules, or the stations' public files.

**G8. 电视与数字广告无文字稿，多数也无视频文件。** 只有 Raman 的艾美奖主题广告有完整视频
（其 YouTube 上传版）[SRC-0044]；Bass 的移民执法广告、警察工会的 "Doesn't Get It"、Streets For All
的广告均只见于洛杉矶时报通讯的描述，因此 `main_visual_elements` 与 `narration_soundtrack` 是
该通讯的报道而非档案的观看结果。弥补方式：伦理委员会的独立支出申报（附广告脚本与投放表），
或电视台公共档案。

**G9. Debate-stage visuals are unrecorded.** Because this build could not view video or image content,
`visual_notes` is `unknown` for every event and `framing`/`camera_angle`/`clothing_notes` are `unknown`
for every image except where reporting states a detail (the mayor's aquamarine pantsuit, [SRC-0044]).
Closing it: a build with image input, or the hosts' press photos with captions.

**G9. 辩论现场视觉未被记录。** 本次构建无法查看视频或图像内容，故所有活动的 `visual_notes` 为
`unknown`，所有图像的 `framing`/`camera_angle`/`clothing_notes` 为 `unknown`，仅在报道明确提及
细节时例外（市长的水蓝色套装，[SRC-0044]）。弥补方式：具备图像输入的构建，或主办方带说明的新闻照。

## D. The styling question / 造型问题

**G10. No reporting documents campaign styling, stylists, or a "styling team".** The original brief asked
about a "campaign styling team" and image-making. No retrieved source — L.A. Times, LAist, CalMatters,
THR, Deadline, TheWrap, Our Weekly, FOX 11 — mentions a stylist, a glam team, a wardrobe consultant, or
Raman's personal styling. The archive therefore records the *documented* substitutes (official
portraits, ad wardrobe, production grammar) and states plainly that the styling claim is unsupported.
Closing it: fashion/industry trade coverage (WWD, The Cut, THR's style desk), campaign press-kit credits,
or Instagram credit tags — none of which was retrievable here (Instagram and X returned 403/login walls).

**G10. 没有任何报道记录竞选造型、造型师或"造型团队"。** 原始任务问及"竞选造型团队"与形象塑造。
所有已获取来源——洛杉矶时报、LAist、CalMatters、THR、Deadline、TheWrap、Our Weekly、FOX 11——
均未提及造型师、妆造团队、服装顾问或 Raman 的个人造型。因此档案记录**有据可查的替代项**
（官方肖像、广告服装、影像语法），并明言造型说法缺乏支撑。弥补方式：时尚/行业媒体（WWD、The Cut、
THR 时尚版）、竞选新闻资料包署名，或 Instagram 署名标签——本环境均无法获取（Instagram 与 X
返回 403/登录墙）。

## E. Candidate substance and the wider field / 候选人实质与更广泛的候选人阵容

**G11. Bass's second-term agenda has no retrievable body text.** `karenbass.com/term-2-vision` renders
its eight issue sections as JavaScript tabs; only the headings and the page title were extracted
[SRC-0006]. Consequence: BAS-POL-0011 and BAS-POL-0015 are heading-level records, not policy positions.
Closing it: the same page with JS execution, or a PDF version of the agenda.

**G11. Bass 的第二任期议程无正文可取。** `karenbass.com/term-2-vision` 的八个议题板块由 JavaScript
标签页渲染，仅提取到标题与页面题目 [SRC-0006]。后果：BAS-POL-0011 与 BAS-POL-0015 只是标题级记录，
不是政策立场。弥补方式：执行 JS 后抓取同一页面，或议程的 PDF 版本。

**G12. The three non-front-running primary candidates are thin.** Pratt, Miller and Huang appear in
results, finance and two Commons images, but the archive holds no policy positions, no speeches and no
events for them; the only Pratt-specific reporting retrieved is his post-primary video statement
[SRC-0026] and a Guardian piece [SRC-0079]. This is a deliberate scope choice (the case is a two-candidate
comparison) but it limits any claim about *why* Pratt's 217,977 voters split as they did. Closing it:
the Daily News candidate questionnaires (only Logsdon's was retrieved, [SRC-0076]) for all fourteen.

**G12. 三位非领先初选候选人资料单薄。** Pratt、Miller、Huang 出现在结果、财务与两张 Commons 图片中，
但档案没有他们的政策立场、演讲或活动；关于 Pratt 的报道仅得其初选后视频声明 [SRC-0026] 与卫报一篇
[SRC-0079]。这是有意的范围选择（本案为两人对比），但限制了对 Pratt 的 217,977 票如何分流做出论断。
弥补方式：Daily News 对全部十四位候选人的问卷（本次仅取得 Logsdon 的，[SRC-0076]）。

**G13. Several candidate-site sections were never captured.** Raman's issue menu lists DWP, Nightlife,
Street Vendors, Family & Childcare, Climate & Environment, Animal Welfare, Cannabis, Small Business,
Emergency Preparedness and "Save Hollywood Jobs" [SRC-0007] — none of those pages was fetched, so no
position row covers them. Closing it: fetching the remaining issue pages.

**G13. 若干候选人网站板块未被采集。** Raman 的议题菜单列出 DWP、夜生活、街头摊贩、家庭与托育、
气候与环境、动物福利、大麻、小企业、应急准备与"Save Hollywood Jobs" [SRC-0007]，这些页面均未抓取，
故无对应立场行。弥补方式：抓取其余议题页面。

## F. Polling / 民调

**G14. Four of eight runoff polls rest on the Wikipedia table alone.** Impact Research (Oct 2–7),
Tavern Research (Aug 20–25) and Tulchin (Aug) have no retrieved primary document; the Manhattan
Institute's leaned figures were cross-checked against its report but the report's own table was not
extracted. Those rows are `partially verified`. Closing it: the pollsters' own releases (Impact, Tavern
and Tulchin are Democratic firms that rarely publish publicly) or the sponsors' memos.

**G14. 八项决选民调中有四项仅依赖维基表。** Impact Research（10/2–7）、Tavern Research（8/20–25）
与 Tulchin（8 月）无已获取原始文件；Manhattan Institute 的含倾向值虽与其报告交叉核对，但报告表格
未被提取。这些行标 `partially verified`。弥补方式：民调机构自身发布（Impact、Tavern、Tulchin
为民主党机构，通常不公开发布）或委托方备忘录。

**G15. One poll was fabricated and is excluded from the dataset.** A widely shared runoff poll showing
Bass far ahead was retracted by its publisher [SRC-0047] [SRC-0080] [SRC-0081]. `polling.csv` contains
only polls that reconcile arithmetically with their own published components; the fabricated one is
recorded here and in `election_context.md`, never as a row.

**G15. 一项民调系伪造，未纳入数据集。** 一份广为流传、显示 Bass 大幅领先的决选民调被其发布方撤回
[SRC-0047] [SRC-0080] [SRC-0081]。`polling.csv` 只收录与自身公布分项在算术上自洽的民调；该伪造
民调仅记录于本文与 `election_context.md`，不作为数据行。

## G. Money / 资金

**G16. No individual-versus-PAC breakdown, and no IE spending totals.** The Ethics Commission's "totals
by seat" table publishes receipts, matching funds, spending and cash on hand per candidate [SRC-0003],
not the contributor-type split; and it does not aggregate independent expenditures. Consequence:
`individual_contributions` and `pac_contributions` are `unknown` in all twelve finance rows, and the five
IE rows carry the *contribution* to the outside committee rather than its spending. Closing it: the
commission's per-filer Form 460/465 schedules and its independent-expenditure disclosure list.

**G16. 无个人/委员会捐款拆分，也无独立支出合计。** 伦理委员会"按席位合计"表只公布每位候选人的
收入、匹配资金、支出与库存现金 [SRC-0003]，不含按捐款人类型的拆分，也不汇总独立支出。后果：
十二行财务数据的 `individual_contributions` 与 `pac_contributions` 均为 `unknown`，五行独立支出
记录的是对外部委员会的**捐款**而非其支出。弥补方式：委员会按申报人的 460/465 表及其独立支出披露清单。

**G17. The Airbnb-linked $4 million is Wikipedia-only.** FIN-0011 rests on the Wikipedia summary's
"part of nearly $4 million" phrasing; LAist's donor story [SRC-0034] covers the Raman-side committees
in detail but not this transfer. Closing it: the committee's filings or LAist's follow-up reporting.

**G17. 与 Airbnb 相关的 400 万美元仅见于维基百科。** FIN-0011 依据维基摘要"接近 400 万美元的一部分"
的表述；LAist 的捐款报道 [SRC-0034] 详述 Raman 一侧的委员会，但未涉及这笔转账。弥补方式：
该委员会申报文件或 LAist 后续报道。

## H. Blocked and paywalled outlets / 被封锁与付费墙来源

**G18. Ten outlets returned non-200 responses and are excluded as sources.** NYT (`URLError`),
Politico (403), Reuters (401), USA Today (402), AP article pages (403), L.A. Sentinel (403), The Hill
(403), Beverly Press (403), KTLA (403), UCLA Luskin (403), YIMBY LA (404), Envirovoters (`URLError`),
Working Families Party (403), and the Sierra Club Angeles Chapter endorsements page (200 but 212 bytes
of content). Each is logged in `_staging/fetch_log.csv` with its status. Their facts are therefore not in
this archive, which is why the NYT's reporting on Raman's entry is cited only as "not retrievable" in
RAM-EVT-0002. Closing it: a proxy or library access, or an institutional subscription.

**G18. 十家来源返回非 200，未作来源使用。** NYT（`URLError`）、Politico（403）、Reuters（401）、
USA Today（402）、AP 文章页（403）、L.A. Sentinel（403）、The Hill（403）、Beverly Press（403）、
KTLA（403）、UCLA Luskin（403）、YIMBY LA（404）、Envirovoters（`URLError`）、Working Families
Party（403），以及 Sierra Club 洛杉矶分会背书页（200 但仅 212 字节内容）。逐条记录于
`_staging/fetch_log.csv` 及其状态。其事实因此不在本档案内——RAM-EVT-0002 中 NYT 关于 Raman 参选
的报道只能注为"不可获取"。弥补方式：代理/图书馆访问或机构订阅。

**G19. L.A. Times is metered, so most of its 19 cited pages are headline-and-lede only.** Each such row
says so in `reliability_notes`; no fact is taken from a part of the page that did not arrive. Where a
lede did arrive (the two poll stories, the ad-blitz newsletter, the Caruso story), the retrievable
paragraph is quoted. Closing it: a subscription, or the paper's syndicated wire versions.

**G19. 洛杉矶时报有付费墙，故其 19 个被引页面多为标题与导语。** 每行均在 `reliability_notes` 中
注明；不从未能到达的页面部分取任何事实。若导语可用（两篇民调报道、广告通讯、Caruso 报道），
则引用可获取段落。弥补方式：订阅或该报的通讯社转载版本。

## I. Cross-cutting / 跨领域

**G20. No concession speech or concession statement from Bass was located.** The archive has Raman's
victory remarks [SRC-0064] and the outcome headline [SRC-0036], but no Bass concession text, so no
`concession_speech` row exists in `campaign_events.csv`. Closing it: the Nov. 4–5, 2026 coverage or the
campaign's own video.

**G20. 未找到 Bass 的承认败选演讲或声明。** 档案有 Raman 的胜选讲话 [SRC-0064] 与结果标题
[SRC-0036]，但没有 Bass 的败选文本，故 `campaign_events.csv` 中无 `concession_speech` 行。
弥补方式：2026-11-04–05 的报道或竞选团队自有视频。

**G21. No crowd sizes, fundraising-event totals, or volunteer counts beyond campaign claims.** The only
numbers of this kind are the campaign's own (2,000 volunteers, 80,000 doors, [SRC-0014]) and a
columnist's "dozens of working men and women" at Sylmar [SRC-0059]. Closing it: pool reports, fire
department crowd estimates, or the campaign's own event recaps.

**G21. 除竞选方自述外，无人数、募款活动总额或志愿者数量。** 此类数字仅有竞选方自述（2,000 名志愿者、
80,000 扇门，[SRC-0014]）与专栏作者对 Sylmar 现场"数十名工人男女"的描述 [SRC-0059]。弥补方式：
联合采访报道、消防部门人数估计或竞选方活动纪要。
