# -*- coding: utf-8 -*-
"""Front matter patching, timeline documents, event-gap memo."""
import csv
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CASE, KEY

FM = """---
title: %s
title_zh: %s
%scompiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: %s
coverage_note: %s
---

"""


def read(rel):
    return io.open(os.path.join(CASE, rel), encoding="utf-8").read()


def put(rel, text):
    p = os.path.join(CASE, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(text)


def front(rel, title, title_zh, status, note, candidate_id=None):
    t = read(rel)
    if t.startswith("---\n"):
        return
    cid = ("candidate_id: %s\n" % candidate_id) if candidate_id else ""
    put(rel, FM % (title, title_zh, cid, status, note) + t)


# ---- fix internal keys in the Turek biography -----------------------------------
p = "01_candidates/turek/biography.md"
t = read(p)
t = t.replace("(`SRC` f080, f036)", "(SRC-%04d, SRC-%04d)" % (int(KEY["f080"][4:]), int(KEY["f036"][4:])))
t = t.replace("(`SRC` f134, f132)", "(SRC-%04d, SRC-%04d)" % (int(KEY["f134"][4:]), int(KEY["f132"][4:])))
t = t.replace("(KWQC, `SRC` f052)", "(KWQC, SRC-%04d)" % int(KEY["f052"][4:]))
put(p, t)

front("01_candidates/turek/biography.md", "Josh Turek — biography", "Josh Turek 人物传记", "complete",
      "Solid on Paralympic and legislative record; family detail and childhood surgeries rest on the candidate's own account.",
      "TUREK")
front("01_candidates/hinson/biography.md", "Ashley Hinson — biography", "Ashley Hinson 人物传记", "complete",
      "Solid on House and state-legislative record; broadcast-career detail is year-level only.", "HINSON")
front("01_candidates/turek/political_positions.md", "Josh Turek — political positions",
      "Josh Turek 政治立场", "complete",
      "14 documented issue areas; no statement found on K-12 funding, school choice or gun licensure.", "TUREK")
front("01_candidates/hinson/political_positions.md", "Ashley Hinson — political positions",
      "Ashley Hinson 政治立场", "complete",
      "Thin on guns, education and election administration: those rows are unknown, not neutral.", "HINSON")
front("03_speeches/communication_analysis_turek.md", "Josh Turek — bilingual communication analysis",
      "Josh Turek 双语传播分析", "complete",
      "Nine speech units with verbatim quotations; no recording viewed, so no timecodes.", "TUREK")
front("03_speeches/communication_analysis_hinson.md", "Ashley Hinson — bilingual communication analysis",
      "Ashley Hinson 双语传播分析", "complete",
      "Seven speech units, five paraphrase-only: her verbatim record is thinner than her event count.", "HINSON")
front("04_visual_archive/image_sources_and_licences.md", "Image sources and licences", "图片来源与授权",
      "complete",
      "Four licensed files downloaded; Turek's official portraits are link-only because of their licence.")

# ------------------------------- timeline docs -------------------------------
ev = list(csv.DictReader(io.open(os.path.join(CASE, "02_campaign_events/campaign_events.csv"),
                                 encoding="utf-8")))
ev.sort(key=lambda r: (r["event_date"], r["event_id"]))


def table(cid_prefixes):
    out = ["| Date | Event id | Event | Category | Place | Status | Source |",
           "|---|---|---|---|---|---|---|"]
    for r in ev:
        if not any(r["event_id"].startswith(p) for p in cid_prefixes):
            continue
        place = r["city"] if r["city"] == "unknown" else "%s, %s" % (r["city"], r["venue"])
        out.append("| %s | `%s` | %s | %s | %s | %s | %s |" % (
            r["event_date"], r["event_id"], r["event_title"], r["event_category"], place,
            r["event_status"], r["source_urls"].split("|")[0]))
    return "\n".join(out)


put("02_campaign_events/turek_timeline.md", FM % (
    "Josh Turek — campaign timeline", "Josh Turek 竞选时间线", "candidate_id: TUREK\n", "complete",
    "17 dated events from launch to election night; venue detail exists for most but not all.")
    + """# Josh Turek — campaign timeline / 竞选时间线

## Overview / 概述

English: Seventeen dated events run from the 12 August 2025 launch video to the 3 November 2026 election. The
record is dense in the general-election phase (August to October 2026) and thin in the primary phase, where
the only clearly documented public events are the primary-night watch party and a closing broadcast interview.

中文：从 2025 年 8 月 12 日启动视频到 2026 年 11 月 3 日大选，共 17 场有日期的活动。大选阶段（2026 年 8–10 月）记录密集，初选阶段较薄，仅有初选夜观选会和一场选前广播专访可明确查证。

## Event table / 活动表

""" + table(["TUR"]) + """

## Structural reading / 结构性解读

English: The schedule is built around **places where a wheelchair is a normal presence** — a senior-living
facility, a university hall, a county party fundraiser, a state-fair-style steak fry — rather than around
workplace tours or factory gates, which is the opposite of the classic Iowa Democratic circuit. Two of the
seventeen events are explicitly framed by reporters as disability-access stories (a supporter describing him
getting out of his chair to knock doors; coverage of his first legislative session), and neither is a campaign
event in the strict sense.

中文：日程围绕"轮椅本就常见"的场所构建——养老社区、大学礼堂、县党部筹款会、州集市式牛排煎饼会——而不是工厂车间与工地门口，这与艾奥瓦民主党的传统路线相反。17 场中有两场被记者明确写成无障碍议题的故事（支持者描述他下轮椅敲门、首個会期的报道），但两者严格来说都不是竞选活动。

## Gaps / 缺口

- No rally with a documented crowd estimate before 29 August 2026; the Steak Fry report gives "hundreds of waving Turek signs" and a standing ovation.
- No county-party meeting date could be verified; the archive records the Steak Fry as a party event instead.
- No public event between 15 October and 3 November 2026 was found, although the campaign's own site lists releases dated 29 October.
""")

put("02_campaign_events/hinson_timeline.md", FM % (
    "Ashley Hinson — campaign timeline", "Ashley Hinson 竞选时间线", "candidate_id: HINSON\n", "complete",
    "Fourteen dated events; several are surrogate-led, and crowd figures exist for only three.")
    + """# Ashley Hinson — campaign timeline / 竞选时间线

## Overview / 概述

English: Fourteen dated items run from the 2 September 2025 radio announcement to the 3 November 2026 result.
The pattern is a front-loaded endorsement sequence (Trump, Grassley, commodity groups, the Border Patrol
union) punctuated by four large surrogate events, then the two debates.

中文：从 2025 年 9 月 2 日电台宣布到 2026 年 11 月 3 日结果，共 14 项有日期的记录。模式是前置的背书序列（特朗普、格拉斯利、农产品团体、边境巡逻工会），穿插四场大型代理人活动，最后是两场辩论。

## Event table / 活动表

""" + table(["HIN"]) + """

## Structural reading / 结构性解读

English: Hinson's calendar is **surrogate-heavy and endorsement-dense**: Cruz appears twice, Barrasso and
Kennedy once each, and the largest crowd (1,300+) belongs to a Kennedy fundraiser in Des Moines rather than to
any Hinson-only event. Only three events in the archive carry a crowd figure at all (1,000+ at the BBQ Bash,
1,300+ at the Faith and Freedom dinner, and the Ankeny roundtable with no figure).

中文：Hinson 的日程"代理人密集、背书密集"：Cruz 出现两次，Barrasso 与 Kennedy 各一次；最大人群（1300+）出现在得梅因的 Kennedy 筹款会，而不是她本人的活动。档案中仅三场活动有人数记录（烧烤会 1000+、信仰与自由晚宴 1300+，Ankeny 圆桌无人数）。

## Gaps / 缺口

- The "Fighting for Iowa Tour" advertised on her website could not be dated or located stop by stop.
- No county-party meeting or small-business visit with a date was retrieved.
- No event between 19 October and 3 November 2026 was found; her final-week schedule is undocumented here.
""")

put("02_campaign_events/event_coverage_gaps.md", FM % (
    "Event coverage gaps", "活动记录缺口", "", "in_progress",
    "Coverage is event-rich but crowd- and venue-poor: most rows have a date and city, few have a headcount.")
    + """# Event coverage gaps / 活动记录缺口

## English

| Gap | Why it exists | What would close it |
|---|---|---|
| No crowd estimate for 25 of 33 events | The covering reports describe what was said, not how many attended | Local TV packages and campaign pool photos; a stringer count |
| No venue for the Ankeny roundtable's room or the Whiskey River address | Reports name the host business but not the room | The venue's own event listings |
| The "Fighting for Iowa Tour" has no dates | The campaign website advertises it as a standing feature | The tour's sign-up page or a dated press release |
| No county-party meetings for either candidate | County party sites were not retrieved in this batch | County central-committee calendars |
| No Turek events between 15 October and 3 November | Only the campaign's own release list covers that window | The campaign's public calendar or local paper previews |
| Two Hinson items are surrogate events, not her appearances | Cruz, Barrasso and Kennedy carried them | Pool reports or video of her own remarks |

## 中文

| 缺口 | 原因 | 补足方式 |
|---|---|---|
| 33 场活动中 25 场无人数记录 | 报道描述发言内容，不报人数 | 地方电视台报道、竞选团队公开照片、自由撰稿人计数 |
| Ankeny 圆桌的场地与 Whiskey River 的具体房间不明 | 报道只写主办企业 | 场地方自己的活动公告 |
| "Fighting for Iowa Tour" 无日期 | 仅在其官网上作为常设栏目出现 | 报名页或有日期的新闻稿 |
| 两位候选人均无县党部会议记录 | 本批次未抓取县党部网站 | 县党部中委会议程 |
| Turek 在 10 月 15 日至 11 月 3 日之间无活动 | 该时段只有其官网新闻列表 | 竞选公开日程或地方报纸预告 |
| Hinson 有两场属代理人活动 | Cruz、Barrasso、Kennedy 主导 | 联合采访记录或其本人发言视频 |

## Rule applied / 适用规则

Where a report says an event happened but gives no crowd, the row's `observable_function` describes what was
observable (a press conference, a roundtable with named participants) and `analyst_notes` says the crowd is
unknown. No number is estimated.

中文：若报道确认活动发生但未给人数，则该行只记录可观察到的形式（记者会、有名有姓的圆桌参与者），并在 `analyst_notes` 注明人数不明；本档案不做任何人数估算。
""")
print("d8 done")
