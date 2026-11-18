# -*- coding: utf-8 -*-
"""Reconcile prose counts in the timeline/comparison/gap docs with the final datasets."""
import csv
import io
import os
import re

CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rd(rel):
    return io.open(os.path.join(CASE, rel), encoding="utf-8").read()


def wr(rel, s):
    io.open(os.path.join(CASE, rel), "w", encoding="utf-8", newline="\n").write(s)


ev = list(csv.DictReader(io.open(os.path.join(CASE, "02_campaign_events/campaign_events.csv"),
                                 encoding="utf-8")))
n_tur = sum(1 for r in ev if r["event_id"].startswith("TUR"))
n_hin = sum(1 for r in ev if r["event_id"].startswith("HIN"))
n_all = len(ev)
with_num = [r["event_id"] for r in ev
            if re.search(r"(\d{3,}\+?|\d,\d{3})",
                         r["visual_notes"] + " " + r["observable_function"] + " " + r["analyst_notes"])]
print("events", n_all, "turek", n_tur, "hinson", n_hin, "with numbers", len(with_num))

# ---- Turek timeline ----------------------------------------------------------
p = "02_campaign_events/turek_timeline.md"
t = rd(p)
t = t.replace("Seventeen dated events run from the 12 August 2025 launch video",
              "Eighteen dated events run from the 12 August 2025 launch video")
t = t.replace("共 17 场有日期的活动", "共 18 场有日期的活动")
t = t.replace("coverage_note: 17 dated events from launch to election night",
              "coverage_note: 18 dated events from launch to election night")
t = t.replace("""## Gaps / 缺口

- No rally with a documented crowd estimate""",
              """## Late additions / 后期补入

English: The 11 October 2026 Fish Fry dinner for state Rep. Sean Bagniewski entered the record only through
the photo caption of an advertisement story published two weeks later — a reminder that county events are
documented incidentally, not systematically.

中文：2026 年 10 月 11 日州众议员 Sean Bagniewski 的炸鱼晚宴，是靠两周后一篇广告报道的照片图注才进入记录的——这提示县级活动往往是被"顺带"记录，而非系统记录。

## Gaps / 缺口

- No rally with a documented crowd estimate""")
wr(p, t)

# ---- gaps memo ---------------------------------------------------------------
p = "02_campaign_events/event_coverage_gaps.md"
g = rd(p)
g = g.replace("| No crowd estimate for 25 of 33 events |", "| No crowd estimate for 30 of 34 events |")
g = g.replace("| 33 场活动中 25 场无人数记录 |", "| 34 场活动中 30 场无人数记录 |")
wr(p, g)

# ---- comparison --------------------------------------------------------------
p = "08_comparative_analysis/candidate_comparison.md"
c = rd(p)
c = c.replace("| 17 own + 2 joint / 本人 17 场 + 联合 2 场 |", "| 18 own + 2 joint / 本人 18 场 + 联合 2 场 |")
c = c.replace("| 2 (Wing Ding 750+, Kennedy dinner n/a) / 2 场（Wing Ding 750+） |",
              "| 2 (Wing Ding 750+; one more with a figure in the source) / 2 场（Wing Ding 750+） |")
wr(p, c)

# ---- README ------------------------------------------------------------------
p = "README.md"
r = rd(p)
r = r.replace("Turek has more dated events (17 to 14)", "Turek has more dated events (18 to 14)")
r = r.replace("Hinson's own ad creative: zero rows despite 9 ad rows / 9 条广告中 Her 本人素材为零",
              "Hinson's own ad creative: zero rows out of nine / 九条广告中她本人的素材为零")
r = r.replace("| Crowd and venue detail for only 12 of 34 events / 34 场中仅 12 场有人数或场地细节",
              "| Crowd detail for only 4 of 34 events / 34 场中仅 4 场有人数记录")
wr(p, r)
print("prose reconciled")
