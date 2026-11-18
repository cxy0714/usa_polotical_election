# -*- coding: utf-8 -*-
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data_events as E

CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLES = {
    "PELTOLA": ("Mary Peltola — campaign timeline", "玛丽·佩尔托拉 — 竞选时间线"),
    "SULLIVAN": ("Dan S. Sullivan — campaign timeline", "丹·沙利文 — 竞选时间线"),
}
ZH_CAT = {
    "launch": "宣布参选", "announcement": "政策发布", "rally": "集会", "debate": "辩论",
    "endorsement_event": "背书", "video_release": "视频发布", "community_visit": "社区活动",
    "other": "选举程序", "surrogate_event": "代理人活动", "victory_speech": "胜选讲话",
}
ZH_STATUS = {"held": "举行", "announced": "宣布", "unverified": "未核实"}


def esc(s):
    return s.replace("|", "/")


for cand, (t_en, t_zh) in TITLES.items():
    rows = [e for e in E.EVENTS if e["candidate_id"] == cand]
    rows.sort(key=lambda r: (r["event_date"] == "unknown", r["event_date"]))
    lines = []
    lines.append("---")
    lines.append('title: "%s"' % t_en)
    lines.append('title_zh: "%s"' % t_zh)
    lines.append("candidate_id: %s" % cand)
    lines.append("compiled_by: Research Agent (batch 2)")
    lines.append("last_updated: 2026-11-18")
    lines.append("status: complete")
    lines.append('coverage_note: "%d dated or undated entries; endorsements are announcements, not rallies, and AFN rows are unverified placeholders."' % len(rows))
    lines.append("---")
    lines.append("")
    lines.append("# %s / %s" % (t_en, t_zh))
    lines.append("")
    lines.append("Every row below is also a row in `campaign_events.csv`. `held` means a retrieved report "
                 "placed the candidate at the event; `announced` means only a release exists; "
                 "`unverified` marks a documented gap, not an attendance claim.")
    lines.append("")
    lines.append("下表每一行同时是 `campaign_events.csv` 中的一行。`held` 表示已取得报道证明候选人到场；"
                 "`announced` 表示仅有新闻稿；`unverified` 标记有据可查的缺口，而非出席声明。")
    lines.append("")
    lines.append("| Date | Event | Category | City | Status | Source |")
    lines.append("|---|---|---|---|---|---|")
    for e in rows:
        lines.append("| %s | %s | %s | %s | %s | %s |" % (
            e["event_date"], esc(e["event_title"]), e["event_category"], esc(e["city"]),
            e["event_status"], e["source_urls"].split("|")[0]))
    lines.append("")
    lines.append("| 日期 | 活动 | 类别 | 城市 | 状态 | 来源 |")
    lines.append("|---|---|---|---|---|---|")
    for e in rows:
        lines.append("| %s | %s | %s（%s） | %s | %s（%s） | %s |" % (
            e["event_date"], esc(e["event_title"]), e["event_category"], ZH_CAT.get(e["event_category"], "其他"),
            esc(e["city"]), e["event_status"], ZH_STATUS.get(e["event_status"], e["event_status"]),
            e["source_urls"].split("|")[0]))
    lines.append("")
    lines.append("## What the timeline shows")
    lines.append("")
    n_held = sum(1 for e in rows if e["event_status"] == "held")
    n_ann = sum(1 for e in rows if e["event_status"] == "announced")
    n_unv = sum(1 for e in rows if e["event_status"] == "unverified")
    n_deb = sum(1 for e in rows if e["event_category"] == "debate")
    lines.append("Of %d entries, %d are documented appearances, %d are endorsement announcements and %d "
                 "are unverified gap markers; %d are joint debates. The cluster of endorsement rows is a "
                 "property of the sources, not of the campaign: Alaska outlets report endorsement releases "
                 "far more reliably than rally logistics." % (len(rows), n_held, n_ann, n_unv, n_deb))
    lines.append("")
    lines.append("%d 条记录中，%d 条为有据可查的露面，%d 条为背书公告，%d 条为未核实缺口标记，%d 场为"
                 "联合辩论。背书记录密集源于信息来源而非竞选本身：阿拉斯加媒体对背书新闻稿的报道"
                 "远比对集会后勤可靠。" % (len(rows), n_held, n_ann, n_unv, n_deb))
    lines.append("")
    path = os.path.join(CASE, "02_campaign_events",
                        "peltola_timeline.md" if cand == "PELTOLA" else "sullivan_timeline.md")
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print(path, len(rows))
