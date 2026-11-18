# -*- coding: utf-8 -*-
"""Career timelines (CSV) and the four candidate documents."""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CASE, S, write

CAR = ["entry_id", "candidate_id", "start_date", "end_date", "role_or_event", "organization",
       "location", "description", "source_urls", "verification_status"]

TUR = [
    ("1979-04-12", "unknown", "Born", "unknown", "Council Bluffs, Iowa",
     "Born Joshua Peter Turek; spina bifida, which he attributes to his father's Agent Orange exposure in Vietnam.",
     "wiki", "verified"),
    ("1997-08-01", "2002-05-31", "Collegiate wheelchair basketball", "Southwest Minnesota State University",
     "Marshall, Minnesota", "Played 1997-2002; school career records of 4,024 points and 1,213 rebounds; four-time NWBA All-American.",
     "wiki", "partially verified"),
    ("2002-05-31", "unknown", "BA in history", "Southwest Minnesota State University", "Marshall, Minnesota",
     "Undergraduate degree completed in 2002.", "wiki", "partially verified"),
    ("unknown", "unknown", "MBA", "DeVry University", "unknown", "Master of Business Administration.", "wiki",
     "partially verified"),
    ("2004-08-13", "2004-08-29", "Paralympic debut", "United States men's national wheelchair basketball team",
     "Athens, Greece", "First of four Paralympic appearances.", "wiki", "partially verified"),
    ("2011-11-12", "2011-11-20", "Parapan American Games gold", "United States national team", "Guadalajara, Mexico",
     "Team gold.", "wiki", "partially verified"),
    ("2012-08-29", "2012-09-09", "Paralympic bronze", "United States national team", "London, United Kingdom",
     "Bronze medal in the men's wheelchair basketball tournament.", "wiki", "partially verified"),
    ("2014-07-01", "2014-07-14", "World Championship silver", "United States national team", "Incheon, South Korea",
     "Silver at the 2014 Men's World Wheelchair Basketball Championship.", "wiki", "partially verified"),
    ("2015-08-07", "2015-08-15", "Parapan American Games gold", "United States national team", "Toronto, Canada",
     "Team gold.", "wiki", "partially verified"),
    ("2016-09-07", "2016-09-18", "Paralympic gold", "United States national team", "Rio de Janeiro, Brazil",
     "Gold medal; the campaign's biography dates the start of its 'gold for my country' story here.", "f036", "verified"),
    ("2018-06-01", "unknown", "Marriage", "unknown", "Council Bluffs, Iowa",
     "Married Jarolin Reyes, whom he met while playing professionally in Spain; year-level date only.", "wiki",
     "partially verified"),
    ("2019-08-23", "2019-09-01", "Parapan American Games gold and Tokyo qualification",
     "United States national team", "Lima, Peru",
     "Team gold; led the team with 18 points in the 67-36 semi-final win over Argentina that qualified the U.S. for Tokyo.",
     "wiki", "partially verified"),
    ("unknown", "unknown", "Professional wheelchair basketball", "Clubs in Italy, France and Spain",
     "Europe", "Played professionally for nearly two decades, including Bidaideak Bilbao BS in Spain.", "wiki",
     "partially verified"),
    ("2020-08-24", "2020-09-05", "Paralympic gold", "United States national team", "Tokyo, Japan",
     "Second consecutive gold medal.", "wiki", "verified"),
    ("unknown", "2022-03-01", "Mobility-equipment fitting", "NuMotion", "unknown",
     "Fitted patients for wheelchairs and worked through insurance denials; the experience is the stated origin of his House candidacy.",
     "wiki", "partially verified"),
    ("2022-03-01", "2022-11-08", "Iowa House candidacy announced", "Turek for Iowa House", "Council Bluffs, Iowa",
     "Announced a run in House District 20.", "wiki", "partially verified"),
    ("2022-11-08", "2022-12-01", "Elected to the Iowa House", "Iowa House of Representatives", "Council Bluffs, Iowa",
     "Won by six votes after a recount requested by Republican nominee Sarah Abdouch.", "wiki", "verified"),
    ("2023-01-09", "unknown", "Assumed office, Iowa House District 20", "Iowa House of Representatives",
     "Des Moines, Iowa", "First permanently disabled member of the Iowa Legislature.", "wiki", "verified"),
    ("2023-06-01", "unknown", "NWBA Hall of Fame induction", "National Wheelchair Basketball Association",
     "unknown", "Inducted in 2023.", "wiki", "partially verified"),
    ("2024-11-05", "unknown", "Re-elected to the Iowa House", "Iowa House of Representatives", "Council Bluffs, Iowa",
     "Won re-election by about five points according to the campaign coverage.", "wiki", "verified"),
    ("2025-08-12", "unknown", "Launched U.S. Senate campaign", "Turek for Iowa", "Council Bluffs, Iowa",
     "Announced with the video \"Underdog\"; fifth declared Democratic candidate.", "f080", "verified"),
    ("2026-06-02", "unknown", "Won the Democratic Senate primary", "Iowa Democratic Party", "statewide",
     "62.6% to 37.4% over Zach Wahls with 99% counted, per the Associated Press projection.", "f132", "verified"),
    ("2026-11-03", "unknown", "Elected to the U.S. Senate", "U.S. Senate", "statewide",
     "Defeated Ashley Hinson; first Democrat to win an Iowa Senate race since 2008.", "f001", "verified"),
    ("2027-01-03", "unknown", "Scheduled to take office", "U.S. Senate", "Washington, D.C.",
     "Senator-elect per the encyclopedic record; swearing-in date is the constitutional start of the term.", "wiki",
     "partially verified"),
]

HIN = [
    ("1983-06-27", "unknown", "Born", "unknown", "Des Moines, Iowa",
     "Born Ashley Elizabeth Hinson; father a financial adviser, mother a teacher.", "wiki", "verified"),
    ("unknown", "unknown", "High school", "Valley High School", "West Des Moines, Iowa", "Graduated from Valley High School.",
     "wiki", "partially verified"),
    ("unknown", "unknown", "BA in broadcast journalism", "University of Southern California", "Los Angeles, California",
     "Studied broadcast journalism; Pi Beta Phi alumna.", "wiki", "partially verified"),
    ("unknown", "unknown", "Intern", "KABC-TV", "Los Angeles, California", "News and entertainment intern.", "wiki",
     "partially verified"),
    ("unknown", "unknown", "Camera operator and editor", "WOI-TV", "Des Moines, Iowa",
     "Worked on evening newscasts.", "wiki", "partially verified"),
    ("unknown", "2020-01-01", "Anchor and reporter", "KCRG-TV9", "Cedar Rapids, Iowa",
     "More than a decade at KCRG; won two regional Emmy Awards.", "wiki", "partially verified"),
    ("2016-11-08", "2017-01-09", "Elected to the Iowa House, District 67", "Iowa House of Representatives",
     "Cedar Rapids, Iowa", "Defeated Democrat Mark Seidl 62.5%-37.5%.", "wiki", "verified"),
    ("2018-11-06", "2019-01-14", "Re-elected to the Iowa House", "Iowa House of Representatives", "Cedar Rapids, Iowa",
     "Defeated teacher Eric Gjerde 52%-48%; chaired the Judiciary, Public Safety and Transportation committees.",
     "wiki", "verified"),
    ("2019-05-13", "unknown", "Filed paperwork for IA-01", "Hinson for Congress", "Cedar Rapids, Iowa",
     "Filed to challenge first-term Democrat Abby Finkenauer.", "wiki", "partially verified"),
    ("2020-06-02", "unknown", "Won the Republican primary, IA-01", "Republican Party of Iowa", "Cedar Rapids, Iowa",
     "Won the primary; the general election followed in November.", "wiki", "verified"),
    ("2020-11-03", "2021-01-03", "Elected to the U.S. House, IA-01", "U.S. House of Representatives", "Washington, D.C.",
     "Beat Finkenauer 51.2%-48.6%; tied with Mariannette Miller-Meeks as the first Republican woman to represent Iowa in the House.",
     "wiki", "verified"),
    ("2021-01-03", "2023-01-03", "Member, 117th Congress", "U.S. House of Representatives", "Washington, D.C.",
     "Represented Iowa's 1st district through the 117th Congress.", "wiki", "partially verified"),
    ("2022-11-08", "2023-01-03", "Re-elected in IA-02", "U.S. House of Representatives", "Washington, D.C.",
     "After redistricting moved her home in Marion into the 2nd district, she sought and won re-election there.",
     "wiki", "verified"),
    ("2024-11-05", "2025-01-03", "Re-elected in IA-02", "U.S. House of Representatives", "Washington, D.C.",
     "Won a third House term.", "wiki", "verified"),
    ("2025-09-02", "unknown", "Announced U.S. Senate campaign", "Hinson for Iowa", "Des Moines, Iowa",
     "Announced on WHO Radio's Simon Conway show hours after Joni Ernst's retirement video.", "f018", "verified"),
    ("2026-06-02", "unknown", "Won the Republican Senate primary", "Republican Party of Iowa", "statewide",
     "74% to 26% over former state Sen. Jim Carlin.", "f112", "verified"),
    ("2026-11-03", "unknown", "Lost the general election", "Hinson for Iowa", "statewide",
     "631,482 votes (46.36%) to Turek's 688,746 (50.56%).", "nbcapi", "verified"),
]

for cid, prefix, rows in (("TUREK", "TUR", TUR), ("HINSON", "HIN", HIN)):
    out = []
    for i, r in enumerate(rows, start=1):
        out.append(["%s-CAR-%04d" % (prefix, i), cid] + [r[0], r[1], r[2], r[3], r[4], r[5], S(r[6]), r[7]])
    write("01_candidates/%s/career_timeline.csv" % cid.lower(), CAR, out)

# ------------------------------- documents -------------------------------
IO = lambda p, s: io.open(os.path.join(CASE, p), "w", encoding="utf-8", newline="\n").write(s)

IO("01_candidates/turek/biography.md", """# Josh Turek — biography / 人物传记

**中文摘要**：Josh Turek（1979 年 4 月 12 日生于艾奥瓦州 Council Bluffs）是民主党籍艾奥瓦州众议员（第 20 选区，2023 年起），先天脊柱裂（spina bifida），终身使用轮椅，四届残奥会轮椅篮球运动员，2016 里约、2020 东京两枚金牌、2012 伦敦铜牌。2022 年以 6 票之差经重新计票当选州众议员，成为艾奥瓦州议会首位永久性残疾议员。2025 年 8 月 12 日宣布竞选联邦参议员，2026 年 6 月 2 日以 62.6% 赢得初选，11 月 3 日以 50.56% 当选，成为 2008 年以来首位在艾奥瓦州赢得参议院席位的民主党人。

## Documented biography (English)

Joshua Peter Turek was born on 12 April 1979 in Council Bluffs, Iowa, the third child of John Turek, a Navy veteran of the Vietnam War who later worked as a vocational-school administrator, and Luellen Turek, a social worker and community-college instructor. He was born with spina bifida — a condition he has attributed to his father's wartime exposure to Agent Orange — underwent multiple childhood surgeries to improve his mobility, and has used a wheelchair his entire life. He has said he had 21 surgeons before the age of 12. He graduated from Abraham Lincoln High School in Council Bluffs, took a BA in history at Southwest Minnesota State University in 2002, and later an MBA from DeVry University.

He played wheelchair basketball at Southwest Minnesota State University from 1997 to 2002, setting school career records of 4,024 points and 1,213 rebounds, was a four-time NWBA All-American, and was inducted into the NWBA Hall of Fame in 2023. He played professionally in Italy, France and Spain for nearly two decades, including Bidaideak Bilbao BS. With the U.S. men's national team under coach Ron Lykins he won Parapan American gold in 2011, 2015 and 2019, Paralympic bronze in London 2012, Paralympic gold in Rio 2016 and Tokyo 2020, and World Championship silver in Incheon 2014. He competed at four Paralympic Games, beginning in Athens in 2004.

After retiring from basketball he worked for NuMotion, fitting patients for wheelchairs and navigating insurance coverage. He has said that frustration with insurance denials, and learning that Iowa had never elected a permanently physically disabled state legislator, led him to run. He announced for Iowa House District 20 in March 2022, won the November 2022 election by six votes after a recount requested by his Republican opponent, took office on 9 January 2023, and was re-elected in 2024. In the House he sits on the Health and Human Services Committee and the Health Policy Oversight Committee; he previously sat on Environment and Natural Resources and was ranking member of Veterans Affairs and of the Health and Human Services Appropriations Subcommittee.

He married Jarolin Reyes, whom he met while playing in Spain, in 2018; they live in Council Bluffs. His brother John and sister Elisha also played professional basketball in Europe.

## Disability as documented fact / 关于残疾的事实记录

The archive records Turek's spina bifida and his wheelchair use as documented biographical facts reported by news outlets and by his own campaign. It does not treat the disability as a metaphor for his politics, and it does not infer physical capability, stamina or access arrangements at any event. Where a retrieved source explicitly describes him using a wheelchair, the note appears in the event or image row; where no source describes the setting, the field says `unknown`.

- Born with spina bifida, uses a wheelchair: Iowa Capital Dispatch and KCCI launch coverage (`SRC` f080, f036).
- First permanently disabled member of the Iowa Legislature: AFGE release and Iowa Capital Dispatch (`SRC` f134, f132).
- A supporter's description of him getting out of his wheelchair to knock on doors is a quotation from state Rep. Timi Brown-Powers, not an archive observation (KWQC, `SRC` f052).

## Sources

Wikipedia (T3); Iowa Capital Dispatch launch and primary-night reports (T2); KCCI (T2); The Gazette (T2); AFGE (T1); KWQC (T2); Associated Press headline for the Obama endorsement (T2, blocked).
""")

IO("01_candidates/hinson/biography.md", """# Ashley Hinson — biography / 人物传记

**中文摘要**：Ashley Hinson（1983 年 6 月 27 日生于得梅因）是共和党籍联邦众议员，2017–2021 年任艾奥瓦州众议院第 67 选区议员，此前在 Cedar Rapids 的 KCRG-TV 担任主播与记者十余年。2020 年击败民主党现任议员 Abby Finkenauer 进入国会，代表艾奥瓦州第 1 选区，2022 年改选第 2 选区并连任。2025 年 9 月 2 日宣布竞选联邦参议员，2026 年 6 月 2 日以 74% 赢得初选，11 月 3 日以 46.36% 落败。

## Documented biography (English)

Ashley Elizabeth Hinson was born on 27 June 1983 in Des Moines, Iowa. Her father was a financial adviser and her mother a teacher. She graduated from Valley High School in West Des Moines and studied broadcast journalism at the University of Southern California, where she was a Pi Beta Phi member. She interned at KABC-TV in Los Angeles, worked as a camera operator and editor for WOI-TV in Des Moines, and then spent more than a decade as an anchor and reporter at KCRG-TV in Cedar Rapids, winning two regional Emmy Awards.

In 2016 she ran for Iowa House District 67, based in Linn County, and defeated Democrat Mark Seidl 62.5%-37.5%. She was re-elected in 2018 against teacher Eric Gjerde, 52%-48%, and chaired the Judiciary, Public Safety and Transportation committees.

She filed paperwork in May 2019 to challenge first-term Democrat Abby Finkenauer in Iowa's 1st congressional district, won the June 2020 Republican primary, and won the November 2020 general election 51.2%-48.6%. She is tied with Mariannette Miller-Meeks as the first Republican woman to represent Iowa in the U.S. House. After the 2021 redistricting moved her home in Marion into the 2nd district, she sought and won re-election there in 2022 and again in 2024.

On 2 September 2025, hours after Sen. Joni Ernst released a video announcing her retirement, Hinson announced her Senate candidacy on WHO Radio's Simon Conway show. She won the 2 June 2026 Republican primary 74%-26% over former state Sen. Jim Carlin and lost the 3 November 2026 general election to Josh Turek, 46.36% to 50.56%.

## Notable documented episode / 有据可查的插曲

In July 2020 The New York Times reported that portions of her campaign website had copied text from media articles; Hinson said she had been unaware of the plagiarism when reviewing drafts and that staff would be held accountable. The episode is recorded here because it is documented, not as an assessment of her candidacy.

## Sources

Wikipedia (T3); NBC News, Fox News and Bleeding Heartland on the launch (T2/T3); The Gazette on the primary result and the Carlin endorsement (T2); NBC News results feed (T2).
""")

IO("01_candidates/turek/political_positions.md", """# Josh Turek — political positions / 政治立场

All rows below are mirrored in `01_candidates/policy_positions.csv` (`TUR-POS-####`). Only positions found in a retrieved page are recorded; gaps are marked.

| Issue | Position (English) | 立场（中文） | Evidence |
|---|---|---|---|
| Healthcare — Medicaid | Opposes the OBBBA Medicaid reductions; pledges to reverse them | 反对《One Big Beautiful Bill Act》的医疗补助削减，主张逆转 | `TUR-POS-0001` |
| Healthcare — public option | Supports a public insurance option and restoring enhanced ACA subsidies | 支持公共医保选项与恢复强化版 ACA 补贴 | `TUR-POS-0003` |
| Healthcare — Social Security | Would lift the payroll-tax cap to keep the trust fund solvent | 主张取消社保工资税上限以维持基金偿付能力 | `TUR-POS-0004` |
| Abortion | Would pass a federal law restoring Roe-era protections; says Iowa's six-week ban cut OB-GYN services | 主张以联邦立法恢复 Roe 时期保护；称艾奥瓦六周禁令减少妇产科服务 | `TUR-POS-0007`, `TUR-POS-0008` |
| Guns | Ads say he voted with Republicans on "gun rights protections"; presents himself as gun-friendly | 广告称其在州议会与共和党人一起投票支持持枪权 | `TUR-POS-0009` |
| Immigration | Ads promise to work with Trump to secure the border and stop drugs; calls border security non-partisan | 广告承诺与特朗普合作管控边境；称边境安全非党派议题 | `TUR-POS-0010`, `TUR-POS-0011` |
| Energy — ethanol | Supports year-round E15 sales | 支持全年销售 E15 乙醇汽油 | `TUR-POS-0012` |
| Energy — data centers | No tax breaks for operators; guardrails so they do not raise household power rates | 反对数据中心税收优惠；要求防止推高居民电价 | `TUR-POS-0013` |
| Economy — tariffs | Calls the tariffs damaging to farmers; supports only targeted tariffs | 认为关税伤害农民；仅支持有针对性的关税 | `TUR-POS-0014` |
| Economy — farm bill | Urges Congress to pass a farm bill before adjourning | 呼吁国会在休会前通过农业法案 | `TUR-POS-0015` |
| Economy — right to repair | Supports a federal right-to-repair law for farm equipment | 支持农机的联邦"维修权"立法 | `TUR-POS-0016` |
| Other — disability / ADA | Treats the ADA as the policy that made his career possible; first permanently disabled legislator | 将 ADA 视为其个人经历的关键公共政策 | `TUR-POS-0020` |
| Other — AI | Supports regulating data centers and AI; does not want to cede the field to China | 支持监管数据中心与 AI；不愿把该领域让给中国 | `TUR-POS-0021` |
| Other — transgender rights | Opposes gender-affirming surgery for minors, Medicaid funding for it, and trans women in women's sports; voted against school notification and restroom bills | 反对未成年人变性手术、相关医疗补助及跨性别女性参加女子体育；但反对学校告知与厕所法案 | `TUR-POS-0022` |
| Democracy — term limits | Supports congressional term limits | 支持国会任期限制 | `TUR-POS-0024` |
| Foreign policy — Gaza | Called for conditions on U.S. aid to Israel | 主张对以色列援助附加条件 | `TUR-POS-0025` |
| Foreign policy — Iran | Calls the 2026 Iran war an "unnecessary war" | 称 2026 年伊朗战争为"不必要的战争" | `TUR-POS-0026` |

## Reading notes / 阅读说明

- The Ernst town-hall line "we are all going to die" is background to the Medicaid debate, not a Turek position; it appears only as context in `TUR-POS-0001` and in the event rows.
- `TUR-POS-0022` is the most misreadable row in the case: he holds conservative positions on transgender medicine and sport while voting against two state bills on school notification and restrooms, and his campaign linked the restroom bill to disabled Iowans and opposite-sex caregivers. The archive does not resolve that into a single label.
- No position on K-12 school funding, school choice, or gun licensure was found in the retrieved pages.
""")

IO("01_candidates/hinson/political_positions.md", """# Ashley Hinson — political positions / 政治立场

All rows below are mirrored in `01_candidates/policy_positions.csv` (`HIN-POS-####`).

| Issue | Position (English) | 立场（中文） | Evidence |
|---|---|---|---|
| Healthcare — Medicaid | Supported the 2025 reconciliation law's Medicaid changes as fiscally responsible | 以财政责任为由支持 2025 年和解法案的医疗补助调整 | `HIN-POS-0001` |
| Healthcare — Social Security | Says she has never cut Social Security; opposes raising the retirement age, after saying in 2020 she was open to it | 称从未削减社保、反对提高退休年龄（2020 年曾表示可以考虑） | `HIN-POS-0002` |
| Abortion | Opposes a legal right to abortion, with exceptions for rape, incest and the life of the mother | 反对堕胎合法权利，强暴、乱伦与孕妇生命例外 | `HIN-POS-0003` |
| Abortion — Planned Parenthood | Voted to remove family-planning, sex-education and Medicaid funding streams | 投票取消计生、性教育与医疗补助等拨款 | `HIN-POS-0004` |
| Immigration | Backs border-security enforcement; endorsed by the Border Patrol agents' union | 支持边境执法；获边境巡逻工会背书 | `HIN-POS-0007` |
| Energy — ethanol | Endorsed by the Iowa Corn Growers PAC, which weighs ethanol positions | 获艾奥瓦玉米种植者 PAC 背书（该 PAC 考量乙醇立场） | `HIN-POS-0008` |
| Economy — agriculture | Designated "Friend of Agriculture" by the Iowa Farm Bureau PAC | 获艾奥瓦农场局 PAC "农业之友"认定 | `HIN-POS-0009` |
| Economy — tariffs | Defends tariffs as a counter to unfair trade; "Nobody loves tariffs..." | 为关税辩护，称更不喜欢不公平竞争环境 | `HIN-POS-0010` |
| Economy — taxes | Campaigns on the OBBBA tips and overtime tax cuts | 主打 OBBBA 的小费与加班费减税 | `HIN-POS-0011` |
| Economy — farmland | Would block foreign adversaries from buying farmland near sensitive sites | 主张阻止外国对手购买敏感地区农地 | `HIN-POS-0012` |
| Economy — AI / data centers | Favours AI development and an "AI economy"; retraining for displaced workers | 支持 AI 发展与"AI 经济"，主张为失业工人再培训 | `HIN-POS-0013` |
| Other — China | Frames AI and trade as a contest with China | 将 AI 与贸易框定为对华竞争 | `HIN-POS-0016` |
| Other — LGBTQ | Opposes LGBTQ movements per race coverage, while listed by an LGBT Republican group as endorsed | 报道称其反对 LGBTQ 运动，同时被 LGBT 共和党组织列为背书对象 | `HIN-POS-0014` |

## Reading notes / 阅读说明

- Gun policy (`HIN-POS-0006`), education (`HIN-POS-0018`) and election administration (`HIN-POS-0017`) are recorded as **unknown**: no statement was found in the retrieved pages, and the NRA-PVF ratings page archived here did not render candidate grades. These are gaps, not neutral positions.
- The LGBTQ row is a genuine source conflict (`conflicting sources`): the race coverage says she opposes LGBTQ movements, and a Newsweek list of Republicans endorsed by an LGBT organisation includes her. The archive records both and does not pick one.
- Her campaign's Social Security statement (`HIN-POS-0002`) is self-reported; it is set against her 2020 remark about the retirement age rather than treated as the final word.
""")
print("documents written")
