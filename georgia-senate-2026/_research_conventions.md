---
title: Research conventions used in this case
title_zh: 本案例使用的整理规范
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Records the rules applied to every row so later readers can reproduce or challenge the archive.
---

## Sourcing rule / 来源规则

Every URL cited anywhere in the archive appears in `_staging/fetch_log.csv` with its HTTP status, byte count, timestamp and saved mirror. A source that is not in the log is not cited. `09_sources/sources.csv` holds 99 sources, all with access_date 2026-11-18. SRC-0001

档案中引用的每个链接都出现在 `_staging/fetch_log.csv`，并附 HTTP 状态、字节数、时间戳与镜像文件。未记录的来源不予引用。`09_sources/sources.csv` 共 99 个来源，访问日期均为 2026-11-18。SRC-0001

## One source per row / 每行一个来源

Validator rule: each `source_urls` cell must be exactly one `SRC-####|https://…`. Secondary corroboration is therefore described in notes columns, not stacked in the URL cell. This is why many rows look single-sourced even when two outlets agree.

校验规则：每个 `source_urls` 单元必须是单独一条 `SRC-####|https://…`。因此第二来源的印证写在备注列，而非堆叠在链接单元中。这正是许多行看似单一来源、实有两个媒体一致的原因。

## Never invent / 绝不虚构

Venue, crowd size, time of day, quote wording and dates are recorded only when a source states them. When absent, the value is `unknown`. No row was filled from a party platform, a candidate's general reputation, or a neighbouring case. SRC-0097

场地、人数、时段、引语措辞与日期仅在来源明确时记录；缺失即填 `unknown`。任何行都未依据党纲、候选人一般声誉或相邻案例填充。SRC-0097

## Verification tiers / 核验等级

`verified` means a dated news report or official record states the fact and a second source was checked where possible. `partially verified` means a single outlet or an encyclopedia entry. `unverified` means only an opponent's claim exists. `conflicting sources` is used where two sources disagree on the same fact. SRC-0096

`verified` 指有日期的报道或官方记录明确记载，且尽可能核对第二来源；`partially verified` 指仅单一媒体或百科；`unverified` 指仅有对手主张；`conflicting sources` 用于两来源对同一事实不一致的情况。SRC-0096

## Announcement versus event / 公告与活动之分

Endorsement announcements and debate announcements are recorded as events with `event_status=announced`, because a statement is not a rally. Both debate rows are `held`. SRC-0012 SRC-0043

背书公告与辩论公告作为活动记录，`event_status=announced`，因为声明不等于集会。两场辩论均为 `held`。SRC-0012 SRC-0043

## Quotation handling / 引语处理

AJC body text is deliberately scrambled beyond the opening paragraphs, so AJC items are cited at headline level only and flagged in `reliability_notes`. Georgia Recorder, GPB, CBS, NBC, Slate and the Guardian were readable and are quoted directly. SRC-0049 SRC-0016

AJC 正文在开头段落之后被人为打乱，因此 AJC 条目仅按标题层面引用，并在 `reliability_notes` 中标注。Georgia Recorder、GPB、CBS、NBC、Slate 与《卫报》可读，直接引用。SRC-0049 SRC-0016

## Interpretation is labelled / 解读须标注

Observable staging (teleprompter, coached crowd, rolled-up sleeves) is recorded in the `observable_function` or `visual_notes` field; any inference about intent or effect begins with `INTERPRETATION:` in a separate field. SRC-0018

可观察的舞台安排（提词器、受指导的观众、卷起的袖子）记入 `observable_function` 或 `visual_notes`；关于意图或效果的推断在独立字段中以 `INTERPRETATION:` 开头。SRC-0018
