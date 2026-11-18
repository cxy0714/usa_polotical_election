# -*- coding: utf-8 -*-
"""Final numeric refresh of README + gaps after the ad/event/position additions."""
import io
import os

CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rd(rel):
    return io.open(os.path.join(CASE, rel), encoding="utf-8").read()


def wr(rel, s):
    io.open(os.path.join(CASE, rel), "w", encoding="utf-8", newline="\n").write(s)


t = rd("README.md")
t = t.replace("6 advertisements, 7 social posts, 28 coverage items",
              "9 advertisements, 7 social posts, 29 coverage items")
t = t.replace("It covers both primaries, the\ngeneral election, 33 campaign events, 44 documented policy positions, 16 speech units",
              "It covers both primaries, the\ngeneral election, 34 campaign events, 45 documented policy positions, 16 speech units")
t = t.replace("涵盖两场初选、大选、33 场竞选活动、44 条政策立场",
              "涵盖两场初选、大选、34 场竞选活动、45 条政策立场")
t = t.replace("**e. Only one ad exchange is documented in detail.** Six advertisement rows exist: four Turek items (three\npaid-style spots plus a July endorsement video that is not a paid spot) and two headline-level outside buys.",
              "**e. The ad record is one-sided.** Nine advertisement rows exist: seven Turek items (six spots plus a July\nendorsement video) and two headline-level outside buys — and **no Hinson campaign ad creative at all**.")
t = t.replace("05_campaign_media/  advertisements.csv (6), social_media.csv (7), media_coverage.csv (28)",
              "05_campaign_media/  advertisements.csv (9), social_media.csv (7), media_coverage.csv (29)")
t = t.replace("campaign_events.csv (33)", "campaign_events.csv (34)")
t = t.replace("policy_positions.csv (44)", "policy_positions.csv (45)")
t = t.replace("sources.csv (108)", "sources.csv (111)")
t = t.replace("across 433 rows and 108 sources", "across 442 rows and 111 sources")
t = t.replace("在 433 行、108 个来源上", "在 442 行、111 个来源上")
t = t.replace("| Event chronology for both candidates, 33 rows / 两位候选人的活动年表，33 行",
              "| Event chronology for both candidates, 34 rows / 两位候选人的活动年表，34 行")
t = t.replace("| Crowd and venue detail for only 11 of 33 events / 33 场中仅 11 场有人数或场地细节",
              "| Crowd and venue detail for only 12 of 34 events / 34 场中仅 12 场有人数或场地细节")
t = t.replace("| Hinson's own ad creative: zero rows / Hinson 本人的广告素材：零记录",
              "| Hinson's own ad creative: zero rows despite 9 ad rows / 9 条广告中 Her 本人素材为零")
wr("README.md", t)

g = rd("research_gaps.md")
g = g.replace("""**Gap / 缺口**: The target of 6 is met only by counting a July endorsement video as an advertisement; there
is **no Hinson campaign ad creative at all**. / 6 条目标仅靠把七月的一段背书视频计入广告才达到；**完全没有 Hinson 本人的广告素材**。""",
"""**Gap / 缺口**: Nine ad rows exist but all seven candidate rows are Turek's; there is **no Hinson campaign ad
creative at all**. / 广告表有 9 条，但七条候选人广告全部属于 Turek；**完全没有 Hinson 本人的广告素材**。""")
g = g.replace("**Cause / 原因**: The race's ad record is thin in retrievable text: outside spending is reported at headline\nlevel, and her creative was not published in the pages fetched.",
              "**Cause / 原因**: Turek's spots were covered as news (one report even printed a script verbatim); hers were\nnot, and outside spending is reported only at headline level.")
wr("research_gaps.md", g)
print("numeric refresh done")
