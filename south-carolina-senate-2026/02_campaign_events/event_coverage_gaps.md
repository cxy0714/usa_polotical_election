---
title: "Event coverage gaps - what the record does not contain"
title_zh: "活动覆盖缺口——记录中不存在的内容"
candidate_id: both
compiled_by: Lead Research Agent
last_updated: 2026-11-12
status: complete
coverage_note: "32 events. The shortfall against the 70-row target is a finding about the sources, not a defect to be padded."
---

# Event coverage gaps / 活动覆盖缺口

## 1. Why this file has 32 rows, not 70 / 1. 为什么是 32 行而不是 70 行

The conventions set a 70-row target. The archive ships 32. The reason is specific: the retrievable record of this race is dominated by election administration, debates and televised speeches, and almost never contains a dated, located appearance with a venue, a time and a crowd. Andrews's campaign calendar was not retrievable at all (her site returns HTTP 403), and Graham's dated appearances beyond the debates are rallies documented through video uploads rather than through a campaign schedule.

研究规范设定的目标是 70 行，本档案交付 32 行。原因是具体的：这场选举可检索到的记录以选举行政事务、辩论与电视讲话为主，几乎从不包含带场地、时间与人数、且有确切日期的竞选露面。安德鲁斯的竞选日程完全无法检索（其网站返回 HTTP 403）；格雷厄姆在辩论之外的确定露面，仅有两场集会，且是通过视频上传而非竞选日程记录下来的。

Filling the gap with plausible rows would destroy the property that makes the dataset usable: that every row traces to something retrieved.

用看似合理的行去填空，会毁掉这份数据集唯一可用的属性：每一行都能追溯到实际检索到的东西。

## 2. What is missing, by type / 2. 按类型列出的缺失

| Missing / 缺失 | Consequence / 影响 |
|---|---|
| Campaign event calendars (both sides) | No meet-and-greets, county visits or church appearances; the two town halls are known only from photo captions. |
| Venues and times for speeches | Most rows carry `venue = unknown` and `event_time = unknown`. |
| Crowd sizes | Published in no retrieved source; never estimated here. |
| The Myrtle Beach rally date | Videos uploaded 2026-08-21/22; the event date is not established. |
| Early-voting / GOTV events | A photo documents an early-voting appearance (2026-10-28); no GOTV programme is recorded. |
| Andrews events between 06-10 and 08-26 | The record jumps from the primary-night speech to a WBTV interview. |

| 缺失 | 影响 |
|---|---|
| 双方竞选活动日程 | 除两场有照片记录的市政厅外，没有见面会、县域走访或教会露面。 |
| 讲话的场地与时间 | 多数行 `venue = unknown`、`event_time = unknown`。 |
| 参与人数 | 任何已检索来源均未公布；本档案从不估算。 |
| 默特尔比奇集会的日期 | 视频上传于 2026-08-21/22；活动日期未能确立。 |
| 提前投票／催票活动 | 有一张照片记录 2026-10-28 的提前投票露面，但没有催票项目的记录。 |
| 安德鲁斯在 06-10 至 08-26 之间的活动 | 记录从初选之夜讲话直接跳到 WBTV 采访。 |

## 3. Asymmetry between the two candidates / 3. 两位候选人之间的不对称

Graham has 19 rows to Andrews's 13, and the imbalance is structural rather than editorial: the vacancy generated appointment, swearing-in, launch, filing-window, floor remarks and runoff events with no Democratic counterpart, plus four debates in which she took part.

格雷厄姆 19 行、安德鲁斯 13 行，这一不平衡是结构性的而非编辑性的：空缺产生了一系列在民主党一方没有对应物的事件——任命、宣誓、启动、登记窗口、决选、院会发言——再加上她参与的四场辩论。安德鲁斯规模更大的竞选，其有日期、有分类的活动反而落在照片说明与视频上传上。

## 4. Rows dated by a recording or a caption / 4. 日期来自影像或说明的行

Several rows are dated by the upload date of a video showing the candidate speaking, or by a Commons file description, not by a campaign schedule. They are `partially verified` for that reason, and the evidence URL is in `video_url` or `photo_urls`. A human analyst should treat those dates as 'not earlier than' rather than exact.

有十行的日期来自显示该候选人讲话的视频上传时间或照片说明，而非竞选日程。正因如此它们标记为 `partially verified`。人工分析者应把它们的日期视为「不早于」而非精确日期。

## Sources

- [SRC-2108] `https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_South_Carolina`
