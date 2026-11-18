# -*- coding: utf-8 -*-
"""Regenerate the two political_positions.md memos directly from policy_positions.csv."""
import csv
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(HERE)

rows = list(csv.DictReader(open(os.path.join(CASE, "01_candidates/policy_positions.csv"), encoding="utf-8")))

ZH = {
    "Medicaid": "医疗补助", "Medicare": "联邦医保", "Public option": "公共医保选项",
    "Social Security financing": "社保融资", "Rural health care": "农村医疗",
    "Food assistance (SNAP)": "食品补助（SNAP）", "Federal codification": "联邦立法（罗诉韦德）",
    "Iowa six-week ban": "艾奥瓦六周禁令", "Second Amendment": "持枪权", "Border security": "边境安全",
    "Framing": "表述框架", "Ethanol and E15": "乙醇与 E15", "Data centers and electricity rates": "数据中心与电价",
    "Tariffs": "关税", "Farm bill": "农业法案", "Farm equipment right-to-repair": "农机维修权",
    "Country-of-origin labeling": "原产地标识", "Cost of living": "生活成本",
    "Disability policy and the ADA": "残疾政策与 ADA", "Artificial intelligence": "人工智能",
    "Transgender rights": "跨性别权利", "Transgender rights (advertising)": "跨性别权利（广告）", "Unions": "工会", "Term limits": "任期限制",
    "Gaza aid conditions": "加沙援助条件", "Iran war": "伊朗战争", "Public schools and AEAs": "公立学校与 AEA",
    "Medicaid and the OBBBA": "医疗补助与 OBBBA", "Social Security": "社会保障",
    "Legal status": "堕胎合法性", "Planned Parenthood funding": "计生拨款",
    "Interest-group alignment": "利益团体背书", "Firearms": "枪械", "Ethanol": "乙醇",
    "Agriculture and the farm bill": "农业与农业法案", "Taxes": "税收",
    "Foreign ownership of farmland": "农地外资", "Data centers and AI": "数据中心与 AI",
    "LGBTQ policy": "LGBTQ 政策", "China competition": "对华竞争",
    "Election administration": "选举管理", "Schools": "学校",

}

def table(cid):
    out = ["| Position id | Issue | Subissue | Recorded position (English) | 中文要点 | Status |",
           "|---|---|---|---|---|---|"]
    for r in rows:
        if r["candidate_id"] != cid:
            continue
        out.append("| `%s` | %s | %s | %s | %s | %s |" % (
            r["position_id"], r["issue"], r["subissue"], r["position_summary"],
            ZH.get(r["subissue"], r["subissue"]), r["verification_status"]))
    return "\n".join(out)


HEAD_T = """# Josh Turek — political positions / 政治立场

**中文摘要**：以下表格逐条对应 `01_candidates/policy_positions.csv` 中的 TUR 行。只记录在已抓取页面中确实出现的立场；查不到的立场标记为 unknown 或列入 `research_gaps.md`，不作推断。

**Reading rule / 阅读规则**：Ernst 在 2025 年 5 月市民大会上回应医疗补助削减时说"we are all going to die"，那句话是本案的背景，不是 Turek 的立场，因此只作为语境出现，不构成 TUR 的任何一行。

"""
TAIL_T = """
## Notes / 说明

1. **Disability is a documented fact, not a metaphor.** 出生即患脊柱裂、终身使用轮椅，这是新闻来源与其竞选团队记录的事实。档案不据此推断其体能、耐力或任何活动的无障碍安排；没有来源描述时一律写 `unknown`。
2. **Transgender rights is the least reducible row.** 他在未成年人变性手术、相关医疗补助与跨性别女性参加女子体育上持保守立场，却投票反对学校的代词告知法案与厕所法案，其竞选团队把厕所限制与残疾人和异性照护者的法律风险联系起来。档案不把它归结为单一标签。
3. **Gaps.** 未找到关于 K-12 教育经费、学校选择或枪械许可制度的表述。
4. **Paywalled evidence.** `TUR-POS-0003/0007/0008` 依赖《得梅因纪事报》标题与维基百科转述，该报对本档案抓取返回 402（付费墙），已在 `sources.csv` 记录。
"""

HEAD_H = """# Ashley Hinson — political positions / 政治立场

**中文摘要**：以下表格逐条对应 `01_candidates/policy_positions.csv` 中的 HIN 行。凡未在已抓取页面中找到表述的议题，一律记为 unknown 并列入 `research_gaps.md`。

"""
TAIL_H = """
## Notes / 说明

1. **Gaps are not neutrality.** 枪械（`HIN-POS-0006`）、教育（`HIN-POS-0018`）、选举管理（`HIN-POS-0017`）三行均为 unknown：抓取页面中没有她的相关表述，且 NRA-PVF 评分页在本档案的存档副本中未渲染候选人评级，因此不写任何评级。
2. **One genuine conflict.** LGBTQ 一行为 `conflicting sources`：竞选报道称她反对 LGBTQ 运动，而 Newsweek 的"获 LGBT 共和党组织背书的共和党人"名单又列入她。档案保留两种来源，不替读者裁决。
3. **Self-reported claims.** 社保一行主要依据其竞选团队通讯主任的邮件声明，档案将其与 2020 年她"可以考虑提高退休年龄"的表述并列，而不把声明当作结论。
4. **Endorsement as evidence.** 乙醇、农业两行依据的是利益团体的背书/认定文件，不是她本人的政策表述，已在 `candidate_statement` 中标注。
"""

for cid, head, tail, rel in ((("TUREK"), HEAD_T, TAIL_T, "01_candidates/turek/political_positions.md"),
                             (("HINSON"), HEAD_H, TAIL_H, "01_candidates/hinson/political_positions.md")):
    body = head + table(cid) + tail
    io.open(os.path.join(CASE, rel), "w", encoding="utf-8", newline="\n").write(body)
    print("wrote", rel, len(body))
