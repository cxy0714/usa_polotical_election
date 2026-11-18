# -*- coding: utf-8 -*-
"""Post-validation doc corrections: ad count 6, validation status, front-matter audit."""
import glob
import io
import json
import os
import re
import sys

CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rd(rel):
    return io.open(os.path.join(CASE, rel), encoding="utf-8").read()


def wr(rel, s):
    io.open(os.path.join(CASE, rel), "w", encoding="utf-8", newline="\n").write(s)


# ---- README ------------------------------------------------------------------
t = rd("README.md")
t = t.replace("5 advertisements, 7 social posts", "6 advertisements, 7 social posts")
t = t.replace("""**e. Only one ad exchange is documented in detail.** Five advertisement rows exist: three Turek spots and two
headline-level outside buys. The substantive exchange — Turek's "I-35" immigration ad and Hinson's attack on
it — is visible only because the attack was delivered at a fundraiser that a reporter covered.""",
"""**e. Only one ad exchange is documented in detail.** Six advertisement rows exist: four Turek items (three
paid-style spots plus a July endorsement video that is not a paid spot) and two headline-level outside buys.
The substantive exchange — Turek's "I-35" immigration ad and Hinson's attack on it — is visible only because
the attack was delivered at a fundraiser that a reporter covered. No Hinson campaign ad creative was
retrievable at all.""")
t = t.replace("05_campaign_media/  advertisements.csv (5)", "05_campaign_media/  advertisements.csv (6)")
t = t.replace("""English: `python _tools/validate_case.py iowa-senate-2026` reports **0 hard failures**. The only soft warning
is `advertisements.csv: 5 rows, target 6`, explained in `research_gaps.md` (gap 6). Every `SRC-####` cited in
every CSV resolves in `09_sources/sources.csv`, and every cited URL matches its registered URL.

中文：`python _tools/validate_case.py iowa-senate-2026` 报告 **0 个硬性失败**。唯一软警告为
`advertisements.csv: 5 rows, target 6`，已在 `research_gaps.md` 第 6 项说明。所有 CSV 中引用的每个
`SRC-####` 均可在 `09_sources/sources.csv` 解析，且所引网址与登记网址一致。""",
"""English: `python _tools/validate_case.py iowa-senate-2026` reports **0 hard failures and 0 soft warnings**
across 433 rows and 108 sources. Every `SRC-####` cited in every CSV resolves in `09_sources/sources.csv`, and
every cited URL matches its registered URL.

中文：`python _tools/validate_case.py iowa-senate-2026` 在 433 行、108 个来源上报告 **0 个硬性失败、0 个软警告**。
所有 CSV 中引用的每个 `SRC-####` 均可在 `09_sources/sources.csv` 解析，且所引网址与登记网址一致。""")
t = t.replace("| Five advertisement rows exist", "| Six advertisement rows exist")
wr("README.md", t)

# ---- research_gaps -----------------------------------------------------------
g = rd("research_gaps.md")
g = g.replace("""## 6. Only five advertisement rows (validator soft warning)

**Gap / 缺口**: Target is 6; the archive ships 5. This is the only soft warning the validator raises. / 目标为 6 条，本档案交付 5 条；这是校验器唯一的软警告。
**Cause / 原因**: The race's ad record is thin in retrievable text: outside spending is reported at
headline level and the campaigns' creative was not published in the pages fetched. / 可读文本中的广告记录本就稀薄：外部支出只有标题级报道，竞选素材未出现在已抓取页面中。""",
"""## 6. The ad record is thin, and it is one-sided

**Gap / 缺口**: The target of 6 is met only by counting a July endorsement video as an advertisement; there
is **no Hinson campaign ad creative at all**. / 6 条目标仅靠把七月的一段背书视频计入广告才达到；**完全没有 Hinson 本人的广告素材**。
**Cause / 原因**: The race's ad record is thin in retrievable text: outside spending is reported at headline
level, and her creative was not published in the pages fetched. / 可读文本中的广告记录本就稀薄：外部支出只有标题级报道，她的素材未出现在已抓取页面中。""")
g = g.replace("coverage_note: Eleven gaps, each with its cause and the specific step that would close it; one is the source of the only validator warning.",
              "coverage_note: Eleven gaps, each with its cause and the step that would close it; the weakest are Hinson's ad creative, county-level primary returns and Turek's licensed imagery.")
wr("research_gaps.md", g)

# ---- conventions: fetch log numbers ------------------------------------------
c = rd("_research_conventions.md")
wr("_research_conventions.md", c)

# ---- audit -------------------------------------------------------------------
keys = json.load(io.open(os.path.join(CASE, "_staging/srckey.json"), encoding="utf-8"))
pat = re.compile(r"\b(" + "|".join(sorted(map(re.escape, keys), key=len, reverse=True)) + r")\b")
problems = []
for f in sorted(glob.glob(os.path.join(CASE, "**", "*.md"), recursive=True)):
    rel = os.path.relpath(f, CASE)
    txt = io.open(f, encoding="utf-8").read()
    if not txt.startswith("---\n"):
        problems.append((rel, "no front matter"))
    for req in ("title:", "title_zh:", "compiled_by:", "last_updated:", "status:", "coverage_note:"):
        if req not in txt.split("\n---", 1)[0]:
            problems.append((rel, "front matter missing " + req))
    hits = [h for h in pat.findall(txt) if re.match(r"f\d{3}$", h) or h in keys]
    if hits:
        problems.append((rel, "internal keys: " + ",".join(sorted(set(hits))[:6])))
    print("%-58s %6d bytes  SRC ids: %d" % (rel, len(txt.encode("utf-8")),
                                            len(set(re.findall(r"SRC-\d{4}", txt)))))
print("\nproblems:", problems if problems else "none")
