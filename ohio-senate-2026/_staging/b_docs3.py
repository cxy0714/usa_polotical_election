# -*- coding: utf-8 -*-
"""Build the remaining narrative documents (timelines, analyses, notes)."""
import csv
import sys

sys.path.insert(0, "_staging")
from doc_lib import write  # noqa: E402

FM = """---
title: {title}
title_zh: {zh}
{cand}compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: {note}
---

"""


def fm(title, zh, note, cand=None):
    c = f"candidate_id: {cand}\n" if cand else ""
    return FM.format(title=title, zh=zh, note=note, cand=c)


events = list(csv.DictReader(open("02_campaign_events/campaign_events.csv", encoding="utf-8")))


def timeline(cid, title, zh, note, intro):
    rows = [e for e in events if e["candidate_id"] == cid]
    rows.sort(key=lambda r: r["event_date"])
    out = [fm(title, zh, note, cid), f"# {title}\n", intro.strip() + "\n",
           "| Date | Event | Type | Phase | Venue | Status | Source |",
           "|---|---|---|---|---|---|---|"]
    for e in rows:
        venue = e["venue"] if e["venue"] != "unknown" else "unknown"
        city = "" if e["city"] == "unknown" else f", {e['city']}"
        out.append(f"| {e['event_date']} | {e['event_title']} | {e['event_category']} | "
                   f"{e['campaign_phase']} | {venue}{city} | {e['event_status']} | "
                   f"{e['source_urls'].split('|')[0]} |")
    out.append("\n## 中文摘要\n")
    out.append(zh + "\n")
    out.append("表中每一行都来自 `campaign_events.csv` 的同一条记录；日期、场地与状态在两张表之间"
               "完全一致，因此时间线可以作为事件表的阅读视图，而不是第二套事实。\n")
    return "\n".join(out)


write("02_campaign_events/brown_timeline.md", timeline(
    "BROWN", "Sherrod Brown campaign timeline, 2025-2026",
    "谢罗德·布朗竞选时间线（2025—2026）",
    "Chronological view of the 15 Brown events in campaign_events.csv; no event is added here "
    "that is not in the table.",
    "The timeline begins with Brown's March 2025 press conference launching the Dignity of Work "
    "Institute — message infrastructure built a year before the election — and runs through "
    "result night. Endorsement events are dated to the day the union or group announced, not to "
    "the day Brown appeared with it."))

write("02_campaign_events/husted_timeline.md", timeline(
    "HUSTED", "Jon Husted campaign timeline, 2025-2026",
    "乔恩·赫斯特德竞选时间线（2025—2026）",
    "Chronological view of the 20 Husted events in campaign_events.csv. Husted's incumbency is "
    "dated everywhere: appointed 2025-01-17, sworn in 2025-01-21.",
    "Husted's timeline starts with the appointment and the oath, because both are campaign "
    "facts: he entered the race as the sitting senator. The launch row is dated 2025-04-09, the "
    "day Trump endorsed him."))

write("02_campaign_events/event_coverage_gaps.md", fm(
    "Event coverage gaps and what the event record cannot show",
    "竞选活动记录的缺口",
    "Documents which event types are thin or missing, and why, so downstream users do not read "
    "absence as inactivity.") + """
# Event coverage gaps

## What the table covers well

The 35 rows in `campaign_events.csv` are heavy on endorsement events (17 of 35) and on the final
three weeks of rallies. That reflects the sources: union and trade-association releases are
dated, published and archived, and late-October rally coverage was abundant.

## What is thin

**Routine retail politics is almost absent.** Neither campaign published a public event
calendar, and Ohio political coverage does not report every county fair stop or plant walk. The
archive therefore records seven `community_visit`, `small_business_visit` or `workplace_visit`
rows against what were certainly dozens of such stops. Absence in this table is an artefact of
coverage, not evidence that the candidates stayed home.

**Fundraisers are not documented at all.** No closed-press fundraiser in Ohio was reported with
a date and venue in a retrievable source. There is no `fundraiser` row, and none should be
inferred from the finance totals.

**Debates are absent, and this is the single largest gap.** No source retrieved for this archive
documents a Brown-Husted debate: no date, no venue, no sponsor, no transcript. What the record
does contain is evidence of a dispute about debates — a WDTN headline dated 2026-10-30 whose
article body could not be retrieved — and a Bowling Green State University/YouGov poll, fielded
before debates became an issue, in which 54% of respondents called debates "very important".
No `debate` or `debate_invitation` row was created, because a headline is not enough to fix a
date and venue.

**Early-voting events are undercounted.** Two `early_voting_event` rows exist; both campaigns
ran turnout operations across all 88 counties for four weeks.

## What cannot be recovered at all

Crowd sizes. Where a source printed an estimate ("hundreds", "more than 1,000"), the number is
recorded in `crowd_size_estimate` with the source's own hedging; where no estimate was printed,
the cell says `unknown`. Do not sum these cells.

## 中文摘要

事件表长于 endorsement（35 行中 17 行）与最后三周的集会，因为工会与行业协会的新闻稿有确定日期
且被存档。日常零售式竞选活动（县集市、工厂走访）几乎没有记录：两个竞选团队都没有公布公开活动
日历。募款活动完全没有记录。最大的缺口是辩论：本档案检索到的材料中没有任何一场布朗—赫斯特德
辩论的日期、场地或主办方；只有一条 2026-10-30 的 WDTN 标题（正文无法获取）显示辩论曾成为争议
议题。因此没有创建 debate 行——一条标题不足以确定日期与场地。人群规模只能照抄来源的估计，未
印出估计的一律记为 unknown，且不可加总。
""")

# ------------------------------------------------- communication analyses --
write("03_speeches/brown_communication_analysis.md", fm(
    "Sherrod Brown: communication analysis",
    "谢罗德·布朗的传播分析",
    "Based on the eight Brown entries in speech_archive.csv plus media_coverage.csv; every "
    "quoted phrase is traceable to a retrieved source.", "BROWN") + """
# Sherrod Brown: communication analysis

## The register

Brown speaks in short declaratives and then lands a number. The Dignity of Work launch is the
model: "Corporate profits have soared, executive compensation has exploded, and productivity
keeps going up and up, but wages aren't rising along with it, and the cost of living just keeps
getting more expensive," followed by the summary line, "In a nutshell, people can't keep up no
matter how hard they work." The triple anaphora does the argumentative work; the plain-language
summary tells the audience what they just heard.

## The enemy is a category, then a person

Across 2026 the abstraction is "corporations and billionaires", and the person is Husted. The
closing-week formulation is explicit: "He's a special interest guy in Washington... The system is
more rigged than before... I'll stand up to big tech. I'll stand up to the oil companies."
The "golden boy" line — "Corporations and billionaires may try to buy this election for their
golden boy, Jon Husted. But there are more of us than there are of them" — is the campaign's
whole populist frame in two sentences: money versus numbers.

## Data centers as the signature issue

Data centers are the one policy area where Brown's communication is specific rather than
thematic: "Husted's been the front guy on all these data centers, 200 in Ohio, getting huge
over-the-top tax breaks, and raising utility rates." The number is his own count, not an
official statistic, and the archive flags it as the candidate's figure. The campaign ran three
television spots on the same theme.

## Where the record contradicts the message

Two inconsistencies are documented rather than smoothed. First, Brown's protectionist history —
opposition to NAFTA, support for the 2018 washing-machine tariffs, a vote for the USMCA — sits
against 2026 rhetoric about tariffs hurting farmers ("Farmers can't afford a new tractor or a
new combine... because of the tariffs"). Second, in 2015 he praised an Amazon data center in
central Ohio; in 2026 data centers are his central attack. Both are recorded in
`policy_positions.csv` notes and in `research_gaps.md`.

## What is missing

No full transcript of any 2026 Brown speech was retrievable. The archive holds quotations
embedded in reporting, which means the analysis above describes his message as reported, not his
rhetoric as delivered. Duration, applause lines and audience interaction are unknown for every
Brown row.

## 中文摘要

布朗的语体是短句加数字：先三段式排比（利润上升、薪酬爆炸、生产率上升而工资不动），再用一句
大白话收束（"in a nutshell, people can't keep up"）。敌人先是类别（企业与亿万富翁），再落到
具体的人（赫斯特德）："golden boy" 与 "there are more of us than there are of them" 两句就是
整个民粹框架。数据中心是他唯一具体的政策议题，但"200 家"是他自己的计数，档案已标注。两处矛
盾照实记录：2015 年他曾称赞俄亥俄中部的亚马逊数据中心；长期保护主义记录与 2026 年"关税伤害
农民"的说法并存。本档案没有任何一场 2026 年布朗演讲的全文，因此以上分析描述的是"被报道的讯
息"，而非"现场修辞"。
""")

write("03_speeches/husted_communication_analysis.md", fm(
    "Jon Husted: communication analysis",
    "乔恩·赫斯特德的传播分析",
    "Based on the six Husted entries in speech_archive.csv and the Oct-Nov rally coverage; the "
    "brief's appointment dates are corrected and dated in-text.", "HUSTED") + """
# Jon Husted: communication analysis

## Incumbency as the spine of the message

Husted was appointed to the Senate on 2025-01-17 and sworn in on 2025-01-21, and every rally
speech in the archive treats that record as the argument. The Mahoning County remarks are the
fullest example: "We took a state that was dying and made it a state that's now growing again,
is now a place that people move to. It's a place where jobs are being created." The anaphora of
"It's a place where..." converts a state-level record into a claim about the future.

## The tenure attack, in one question

His most repeated line is a rhetorical question: "My opponent, Sherrod Brown, has been in office
for over 50 years. Can you name one thing that he's done to make your life better?" It appears
verbatim in both the 2026-10-12 Youngstown and 2026-10-15 Boardman accounts, and in variant form
at Chillicothe: "Here's the deal, he's been in office for over 50 years..." The repetition is
the strategy — a fixed, memorable frame rather than a new argument per stop.

## Two registers: rally and Senate

At rallies the register is second-person and accusatory: "Why do people like Sherrod Brown care
more about people who are illegally in this country than he cares about you?" On the Senate floor
and in committee the register is procedural; the archived floor remarks on photo ID are
62.3 seconds of un-transcribed audio, and the HELP Committee statement on the abortion pill is
reported rather than transcribed. The archive can date both, and can quote neither at length.

## Personal disclosure as warrant

At the January 2026 HELP hearing Husted pointed to his own adoption story, saying his mother
could have chosen abortion. This is the one place in the record where a personal narrative
carries a policy argument, and it is also the campaign's family frame — the same frame that
appears in the 2025 family photograph in `image_archive.csv`.

## Message discipline and its cost

The data-center bill he sponsored requires regulators only to *consider* a blueprint, a gap
between the messaging ("protecting American manufacturing is the America First agenda") and the
legislative text that opponents exploited. His December 2025 call to "freeze" ACA subsidies,
followed by October 2026 sponsorship of a two-year extension, is the second documented
adjustment. Both are recorded as inconsistencies, not as attacks.

## 中文摘要

赫斯特德的讯息骨架就是"在职记录"：2025-01-17 获任命、2025-01-21 宣誓就职，此后每一次集会演说
都把这份记录当作论据。他最常重复的是一句反问——"他当官超过五十年，你能说出一件他让你生活变好
的事吗？"——在 2026-10-12 与 10-15 两场活动的报道中逐字出现。集会语域是第二人称的指责；参议
院语域则是程序性的（院会发言仅存 62.3 秒未转写音频）。个人叙事只在 2026 年 1 月的 HELP 委员会
听证中出现一次（他自己的收养故事）。信息纪律的代价有两处：数据中心法案只要求监管机构"考虑"
蓝图；2025 年 12 月主张"冻结"ACA 补贴，2026 年 10 月却联署两年延期。两处都作为不一致记录，
而非作为攻击。
""")

# --------------------------------------------------------------- visual ----
write("04_visual_archive/visual_archive_notes.md", fm(
    "Visual archive notes",
    "视觉档案说明",
    "18 image records, 15 files downloaded under 2 MB; clothing and composition fields are "
    "deliberately unknown.") + """
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
""")

# ---------------------------------------------------------------- media ----
write("05_campaign_media/media_notes.md", fm(
    "Campaign media notes: advertising, social and coverage",
    "竞选媒体说明：广告、社交与报道",
    "8 advertisements, 6 social records and 26 coverage items; the NRSC crash ad and the SLF "
    "testimonial ad are the two best-documented paid messages.") + """
# Campaign media notes

## Advertising

Eight rows in `advertisements.csv`. The best-documented paid messages are outside-group ads:
the NRSC's 30-second spot using footage of the April 2026 Interstate 71 crash that killed three
members of the Soposki family, and the Senate Leadership Fund's testimonial ads in which a woman
says "Sherrod Brown supports sex changes for minors, irreversible surgery on kids like me" — an
ad the Ohio Capital Journal fact-checked, finding the speaker was not an Ohioan, was 19 at the
time of surgery, and was treated in Texas.

Brown's side is documented through a single quoted spot and two companions: the Ohio Capital
Journal reports that three Brown ads dealt with data centers and quotes one — "(Jon) Husted is a
chief reason Ohio has so many of those centers. He force-fed the massive energy-sucking
facilities." The other two exist as rows with `unknown` creative, not as reconstructed scripts.

Two AFP Action spots, "Common Sense" and "Taking Root", are documented from the sponsor's own
release, inside a $1.4 million digital and streaming buy in a $9 million Ohio programme.

## The money behind the airwaves

AdImpact, as reported by the Ohio Capital Journal, placed Ohio as the most expensive Senate race
in the country with outside groups spending more than $325 million. That figure is an
ad-tracking estimate, not an FEC total, and is labelled as such.

## Social media

Six rows, and this is the thinnest media file. No campaign social post was retrievable through a
blocked platform, so four of the six rows are documented indirectly — quoted in a Commons file
description, quoted in reporting, or (in one case) a post that was deleted. Each row says how it
was documented. Only the 2026-10-29 vertical video has a stable public URL.

## Coverage

Twenty-six items, weighted toward the Ohio Capital Journal (nine), Cleveland.com (three) and
wire copy carried by the Boston Herald and Yahoo. Two items are syndicated copies because the
original returned 403 (AP) or 402 (the Columbus Dispatch via Yahoo); both are labelled in
`reliability_notes`. Paywalled and blocked outlets — Politico, Axios, the Cincinnati Enquirer,
Reuters — appear only as the subjects of other outlets' reporting, never as cited content.

## 中文摘要

广告表 8 行。记录最完整的是外部团体广告：NRSC 用 2026 年 4 月 I-71 车祸（Soposki 一家三口死亡）
画面制作的 30 秒广告；以及 Senate Leadership Fund 的证言式广告，OCJ 的事实核查发现出镜者并非俄
亥俄居民、手术时已 19 岁、治疗在德州。布朗一方只有一则被引用的数据中心广告，另两则以"创意未知"
的行存在，没有重构脚本。AdImpact 数据（OCJ 报道）称俄亥俄是全国最贵的参议院选战，外部团体支出
超过 3.25 亿美元——这是广告监测估算，不是 FEC 总额。社交媒体只有 6 行，是媒体档案中最薄的一块：
四行是通过 Commons 文件描述、报道引述或被删除的帖子间接记录，每行都注明取证方式。报道 26 条，
以 OCJ 为主；两条为转载副本（AP 原站 403、Dispatch 经 Yahoo 402），均在可靠性备注中标明。
""")

# -------------------------------------------------------------- finance ----
write("06_campaign_finance/finance_notes.md", fm(
    "Campaign finance notes",
    "竞选财务说明",
    "9 rows covering five candidates across two reporting points; only receipts, disbursements "
    "and cash on hand are in the source tables.") + """
# Campaign finance notes

## The two reporting points

The archive holds two snapshots, both taken from the FEC-derived tables in the race article.

**As of 2026-04-18 (period ending 2026-03-31):** Brown had raised $24,471,408, spent $7,956,946
and held $16,514,461. Husted had raised $10,257,823, spent $2,017,868 and held $8,239,954. The
same table lists the Democratic primary field: Ode $5,001,938 raised, Kincaid $41,804, Volpe
$4,337.

**As of 2026-10-14 (period ending 2026-09-30):** Brown $68,409,200 raised, $63,956,397 spent,
$4,452,803 on hand; Husted $19,894,786 raised, $15,655,689 spent, $4,239,097 on hand; Redpath
$55,256 / $47,000 / $8,255; Levy $132,712 / $107,925 / $26,916.

## What the columns mean, and what they do not

The source tables print three numbers per candidate. `individual_contributions`,
`pac_contributions` and `debts_owed` are therefore `unknown` for every row rather than estimated
from the totals. The receipts figure at the October point is cumulative for the cycle, not a
single quarter's intake, and the notes column says so.

## The outside-money gap

Candidate committees are the small part of the picture. AdImpact's estimate, reported by the
Ohio Capital Journal, puts outside-group spending above $325 million in this race — several times
the combined candidate totals. That money flows through committees that file separately, and
none of it appears in `campaign_finance.csv`. A user who reads only the candidate table will
understate total spending by an order of magnitude.

## The spending pattern

Brown raised roughly 3.4 times Husted's total and had spent 96% of what he raised by
2026-09-30, entering the final month with $4.45 million on hand — about the same as Husted's
$4.24 million. The near-identical cash position at the end, against a 3.4x fundraising gap,
is the most striking number in the file.

## 中文摘要

档案只有两个时点：2026-04-18（截至 3 月 31 日）与 2026-10-14（截至 9 月 30 日）。前者布朗募
2,447 万美元、花 796 万、余 1,651 万；赫斯特德募 1,026 万、花 202 万、余 824 万。后者布朗募
6,841 万、花 6,396 万、余 445 万；赫斯特德募 1,989 万、花 1,566 万、余 424 万。来源表只印三个
数字，因此个人捐款、PAC 捐款与负债三列一律记为 unknown，不做推算。10 月的"募款"是本届累计数，
不是单季。最大的缺口是外部资金：AdImpact 估算外部团体支出超过 3.25 亿美元，数倍于两位候选人
之和，且完全不在本表内。最醒目的数字是终点现金几乎相同（445 万 vs 424 万），而募款差距是 3.4 倍。
""")
print("docs written")
