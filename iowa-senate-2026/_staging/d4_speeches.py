# -*- coding: utf-8 -*-
"""speech_archive.csv, speech_video_index.csv and the two communication analyses."""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CASE, S, write

SPH = ["speech_id", "candidate_id", "event_id", "date", "speech_title", "speech_url",
       "transcript_url", "duration", "main_topics", "major_quotes", "rhetorical_devices",
       "opponent_references", "personal_story_elements", "policy_claims", "source_urls",
       "source", "verification_status"]

VID = ["video_id", "candidate_id", "video_url", "date", "duration", "event_type", "main_topics",
       "relevant_timestamps", "transcript_available", "visual_observations", "completeness",
       "source_urls", "verification_status"]

SP = []


def sp(sid, cid, eid, date, title, surl, turl, dur, topics, quotes, devices, opp, story, claims,
       src, source, ver):
    SP.append([sid, cid, eid, date, title, surl, turl, dur, topics, quotes, devices, opp, story,
               claims, S(src), source, ver])


# ------------------------------- Turek -------------------------------
sp("TUR-SPC-0001", "TUREK", "TUR-EVT-0001", "2025-08-12", "Launch video: \"Underdog\"",
   "unknown", "unknown", "unknown",
   "Biography|Disability|Public services|American Dream",
   "\"I knew nothing would come easy, but I never doubted my right to the American dream.\" [unknown] | \"Sitting in my wheelchair nine years old, watching the Olympics, I dreamed of winning gold for my country, too. In 2016 I did just that.\" [unknown]",
   "First-person bildungsroman; direct address to camera; the wheelchair appears as a stated fact of the narrator's life, not as a symbol",
   "None", "Spina bifida attributed to Agent Orange; 21 surgeons before 12; Goodwill clothes and the wrong-colour lunch ticket; two Paralympic golds",
   "Free summer lunch and Area Education Agencies helped his family; public services as the ladder",
   "f036", "KCCI / Iowa Capital Dispatch report of the launch video", "partially verified")
sp("TUR-SPC-0002", "TUREK", "TUR-EVT-0002", "2026-06-02", "Primary-night victory remarks",
   "unknown", "unknown", "unknown",
   "Primary result|American Dream|General election",
   "\"Iowa sure does love an underdog, and we have done it tonight.\" [unknown] | \"My story is truly the American dream.\" [unknown] | \"In no other country on earth could someone born into a working-class family from Council Bluffs, Iowa, who went to the Goodwill, shared clothes, had the wrong color lunch ticket, who was born with my disability of spina bifida due to my father's exposure to Agent Orange in Vietnam, who had 21 surgeons before the age of 12, be able to represent the United States in four Paralympic games and bring home two gold medals, and represent their community in the legislature. Only in America is that possible.\" [unknown]",
   "Repetition of \"underdog\"; anaphora on \"who\"; escalation from deprivation to medals; the closing pledge to \"protect that American dream for future generations\"",
   "None by name",
   "The fullest version of the biography speech: 21 surgeons, Goodwill, lunch ticket, Agent Orange, four Paralympic Games, two golds",
   "Pledges to protect the American Dream for future generations; no costed policy",
   "f132", "Iowa Capital Dispatch (Robin Opsahl)", "verified")
sp("TUR-SPC-0003", "TUREK", "TUR-EVT-0003", "2026-08-29", "Polk County Steak Fry remarks",
   "unknown", "unknown", "unknown",
   "Cost of living|Farm bankruptcies|Health care|Water quality|Term limits",
   "\"And really, Iowa, we have hit the bottom. This is not the state that we know. This is not the state we grew up in.\" [unknown] | \"This is not what Iowans want. Iowans want to have a senator that is going to fight for them. Fight for Iowa. Fight for Iowans. Fight for the middle class. Fight for our workers. Not just look out for the billionaires and the large corporations.\" [unknown]",
   "Anaphora (\"Fight for ...\"); declinist framing (\"we have hit the bottom\"); second-person plural address to the state",
   "Attacked Hinson's voting record on health care, food programmes, tariffs and tax breaks",
   "Working-class Council Bluffs childhood referenced indirectly through the state-of-Iowa frame",
   "Record farm bankruptcies due to tariffs and war; rising cancer diagnoses; declining schools; term limits",
   "f130", "Iowa Capital Dispatch (Joanna Schroeder photo)", "verified")
sp("TUR-SPC-0004", "TUREK", "TUR-EVT-0004", "2026-09-09", "Scottish Rite Park Social Security remarks",
   "unknown", "unknown", "unknown",
   "Social Security|Medicare|Medicaid|Health-care closures",
   "\"This is in a state with a healthcare crisis, a mental health crisis, and a cancer crisis. Voting to cut healthcare (means) the downstream effects are ... less services, less supports, less facilities. This is fundamentally wrong.\" [unknown] | \"I give each and every Iowa senior my pledge - I will do everything I can to protect Medicare, Medicaid, and Social Security, and expand it to all of you.\" [unknown]",
   "Triple crisis list; the \"downstream effects\" chain; a direct pledge ritual (\"I give each and every Iowa senior my pledge\")",
   "Said Hinson voted to cut the programmes; her campaign rejected it the same day",
   "Not biographical; the audience's own circumstances carry the story",
   "842 closed health-care entities; $452 million SSA cut claim (attributed to O'Malley); lifting the payroll-tax cap",
   "f124", "Iowa Capital Dispatch", "verified")
sp("TUR-SPC-0005", "TUREK", "JNT-EVT-0001", "2026-10-07", "First U.S. Senate debate - Turek turns",
   "unknown", "unknown", "unknown",
   "AI and data centers|China|Tariffs|Immigration|Voting record",
   "\"I am absolutely in favor of some regulations on data centers.\" [unknown] | \"I agree we should not cede the ground to China.\" [unknown] | \"What the tariffs have done is, it's led to a decimation of markets.\" [unknown]",
   "Concession-then-pivot (\"I agree ... but\"); farmer-as-victim framing; numbers used sparingly",
   "\"When he is showing up to vote, it's wrong for Iowa\" - Hinson's counter-line, quoted in the same coverage",
   "Bipartisan record claimed; no new biography material",
   "Data-center tax breaks; electricity rates; strategic tariffs only",
   "f085", "Newsweek debate report", "partially verified")
sp("TUR-SPC-0006", "TUREK", "JNT-EVT-0002", "2026-10-13", "Second U.S. Senate debate - Turek turns",
   "unknown", "unknown", "unknown",
   "Agriculture|Tariffs|E15|Farm bill|Right to repair|Foreign farmland",
   "\"Our farmers rely on open markets and free trade more than any other group.\" [unknown] | \"What the tariffs have done is, it's led to a decimation of markets.\" [unknown]",
   "Synecdoche (farmers stand for the state); policy list delivered as a checklist (E15, COOL, right to repair, farm bill)",
   "Said Hinson voted for tax breaks for billionaires and had not shown up for farmers",
   "None", "Year-round E15; mandatory country-of-origin labelling; federal right-to-repair; farm bill before adjournment",
   "f077", "The Daily Iowan (Associated Press contributed)", "verified")
sp("TUR-SPC-0007", "TUREK", "TUR-EVT-0015", "2026-06-01", "KCRG-TV9 closing interview before the primary",
   "unknown", "unknown", "unknown",
   "Biography|Electability|Independents",
   "\"I'm uniquely the American Dream. In no other country on Earth could someone who's gone through ...\" [unknown] (the retrieved page truncates the quotation)",
   "Electability framing; biography as proof of appeal to moderates",
   "Contrasted with Zach Wahls in the primary and with Hinson in the general",
   "Paralympic record; working-class origins",
   "No new policy claims in the retrieved excerpt",
   "f017", "KCRG-TV9", "partially verified")
sp("TUR-SPC-0008", "TUREK", "TUR-EVT-0005", "2026-09-21", "Remarks to reporters on data centers, Des Moines",
   "unknown", "unknown", "unknown",
   "Data centers|Corporate taxes|Electricity rates",
   "\"We want to make sure large corporations are paying their fair share, not getting tax breaks.\" [unknown] | \"I think also making sure we've got strong guardrails to make sure they are not driving up the energy rate to the end user.\" [unknown]",
   "Corporate-accountability frame; \"guardrails\" as the operative metaphor",
   "None by name", "None", "No tax incentives for data-center operators; ratepayer protection",
   "usat_datacenter", "USA Today (quotation reproduced in the Wikipedia citation)", "partially verified")
sp("TUR-SPC-0009", "TUREK", "unknown", "unknown", "Interview with Jon Stewart",
   "unknown", "unknown", "unknown",
   "Party strategy|Prairie populism|Economic message",
   "\"If we're going to once again win in prairie states, it's got to be with an economic populist message, a prairie populist message ... not just being the lesser of two evils-being a corporate Democrat.\" [unknown]",
   "Self-labelling (\"prairie populist\"); antithesis (\"not just the lesser of two evils\")",
   "Criticised corporate Democrats rather than Republicans", "Regional identity (prairie states)",
   "Economic populism as the route back to competitiveness in Iowa",
   "wiki", "Wikipedia citing the September 2026 interview", "partially verified")

# ------------------------------- Hinson -------------------------------
sp("HIN-SPC-0001", "HINSON", "HIN-EVT-0001", "2025-09-02", "WHO Radio launch interview (Simon Conway show)",
   "unknown", "unknown", "unknown",
   "Campaign launch|Ernst retirement|House record",
   "(paraphrase) Announced the Senate campaign on the show and released a slate of endorsements the same hour.",
   "Talk-radio conversational format; endorsement list read as proof of party consolidation",
   "Framed the race as a choice between Republican governance and Democratic control",
   "House tenure presented as the qualification",
   "No policy detail in the retrieved summary",
   "f018", "Bleeding Heartland", "partially verified")
sp("HIN-SPC-0002", "HINSON", "HIN-EVT-0003", "2026-07-25", "Ankeny roundtable remarks on children's online safety",
   "unknown", "unknown", "unknown",
   "AI chatbots|Child safety|Federal regulation",
   "(paraphrase) Took questions from Iowa parents alongside Sen. Cruz on what Congress can do to protect children online.",
   "Surrogate-led format: Cruz carried the legislative argument",
   "None in the retrieved report", "Parent-of-young-children framing implied by the audience, not stated",
   "TAKE IT DOWN Act; AI-chatbot regulation vs industry incentives",
   "f107", "Iowa Capital Dispatch (Robin Opsahl)", "partially verified")
sp("HIN-SPC-0003", "HINSON", "HIN-EVT-0005", "2026-08-29", "Ashley's BBQ Bash remarks",
   "unknown", "unknown", "unknown",
   "Party unity|Record|Fundraising",
   "(paraphrase) Spoke to more than 1,000 donors after Cruz's keynote; the report carries no verbatim Hinson quotation.",
   "Instrumental performance: opened the event playing violin with other performers",
   "Cruz attacked Democratic candidates as \"Marxists and Islamists\"",
   "No biography material in the retrieved report", "No policy claims retrieved",
   "f103", "Iowa Capital Dispatch (Robin Opsahl)", "partially verified")
sp("HIN-SPC-0004", "HINSON", "HIN-EVT-0007", "2026-09-19", "Whiskey River small-business roundtable remarks",
   "unknown", "unknown", "unknown",
   "OBBBA tax cuts|Tips and overtime|Affordability",
   "(paraphrase) Argued that keeping Republicans in Congress is needed so Democrats cannot reverse the tips and overtime tax cuts.",
   "Worker-testimony format: the roundtable participants supplied the anecdotal evidence",
   "Barrasso said Democrats want to end the tax changes",
   "No biography material", "Tips and overtime exemptions; OBBBA",
   "f106", "Iowa Capital Dispatch (Robin Opsahl)", "partially verified")
sp("HIN-SPC-0005", "HINSON", "JNT-EVT-0001", "2026-10-07", "First U.S. Senate debate - Hinson turns",
   "unknown", "unknown", "unknown",
   "Voting record|Immigration|Tariffs|Affordability",
   "\"When he is showing up to vote, it's wrong for Iowa, he's too liberal for this state.\" [unknown]",
   "Attendance-as-character attack; state-ideology framing (\"too liberal for this state\")",
   "Direct attack on Turek's missed House votes", "No biography material",
   "Claims Turek's record is out of step; defends tariffs as leverage",
   "f085", "Newsweek debate report", "partially verified")
sp("HIN-SPC-0006", "HINSON", "JNT-EVT-0002", "2026-10-13", "Second U.S. Senate debate - Hinson turns",
   "unknown", "unknown", "unknown",
   "Tariffs|Farmland|Foreign ownership|Rural health care|Social Security",
   "\"Nobody loves tariffs, but what I like even less is an unlevel playing field for Americans and for our farmers.\" [unknown]",
   "Concession-then-justification; \"level playing field\" as the recurring trade metaphor",
   "Said Turek had not shown up for votes that would help farmers",
   "No biography material", "Blocking foreign purchases of farmland near sensitive sites; tariffs as leverage on China and Canada",
   "f077", "The Daily Iowan (Associated Press contributed)", "verified")
sp("HIN-SPC-0007", "HINSON", "unknown", "2026-03-20", "Op-ed: the AI future should belong to our kids, not Beijing",
   "https://www.nrsc.org/press-releases/ashley-hinson-op-ed-congress-needs-to-ensure-that-the-ai-future-belongs-to-our-kids-not-to-beijing-2026-03-20/",
   "unknown", "unknown",
   "AI|China|Workforce retraining",
   "\"...because the truth is: if we don't, China will.\" [unknown]",
   "Antithesis (our kids / Beijing); national-security framing of a domestic technology issue",
   "China as the implicit adversary", "Children as the stake, not the speaker's own biography",
   "An \"AI economy\"; retraining for workers displaced by AI",
   "f087", "NRSC press release carrying the op-ed", "verified")

write("03_speeches/speech_archive.csv", SPH, SP)
print("turek:", len([r for r in SP if r[1] == "TUREK"]), "hinson:", len([r for r in SP if r[1] == "HINSON"]))

V = [
    ["TUR-VID-0001", "TUREK", "https://www.pbs.org/newshour/politics/watch-live-u-s-senate-candidates-hinson-turek-debate-in-iowa",
     "2026-10-07", "unknown", "debate", "Affordability|Tariffs|AI and data centers|Immigration",
     "unknown", "no", "Not viewed for this archive; the archived page carries the livestream player and the recorded debate.",
     "unknown", S("f193"), "partially verified"],
    ["TUR-VID-0002", "TUREK", "https://www.c-span.org/clip/campaign-2026/josh-turek-says-congress-has-a-role-in-regulating-ai/5206891",
     "2026-09-21", "unknown", "clip", "AI regulation|Data centers",
     "unknown", "no", "Not viewed; the clip page returned HTTP 202 to the fetcher and no player content was archived.",
     "clip", S("f085"), "unverified"],
    ["TUR-VID-0003", "TUREK", "https://www.kcci.com/article/iowa-rep-josh-turek-two-time-paralympian-launches-campaign-for-u-s-senate/65710294",
     "2025-08-12", "unknown", "news package with the \"Underdog\" launch video", "Launch|Biography|Paralympics",
     "unknown", "no", "Not viewed; the article describes the video and quotes its narration.",
     "unknown", S("f036"), "partially verified"],
    ["TUR-VID-0004", "TUREK", "https://iowacapitaldispatch.com/2025/08/12/iowa-rep-josh-turek-two-time-paralympian-launches-campaign-for-u-s-senate/",
     "2025-08-12", "unknown", "news article with embedded launch video", "Launch|Biography|Public services",
     "unknown", "no", "Not viewed; no visual description of the video beyond the narration quoted in the text.",
     "unknown", S("f080"), "partially verified"],
    ["TUR-VID-0005", "TUREK", "https://www.kcrg.com/2026/06/01/iowas-us-senate-candidates-make-final-push-before-tuesdays-primary/",
     "2026-06-01", "unknown", "broadcast interview", "Primary closing argument|Electability",
     "unknown", "no", "Not viewed; the article says the full interview is embedded below the text.",
     "unknown", S("f017"), "partially verified"],
    ["HIN-VID-0001", "HINSON", "https://www.pbs.org/newshour/politics/watch-live-u-s-senate-candidates-hinson-turek-debate-in-iowa",
     "2026-10-07", "unknown", "debate", "Affordability|Tariffs|Immigration|Voting record",
     "unknown", "no", "Same pool feed as TUR-VID-0001; not viewed.",
     "unknown", S("f193"), "partially verified"],
    ["HIN-VID-0002", "HINSON", "https://www.kcrg.com/2026/06/01/iowas-us-senate-candidates-make-final-push-before-tuesdays-primary/",
     "2026-06-01", "unknown", "broadcast interview", "Primary closing argument|Iran war|Cost of living",
     "unknown", "no", "Not viewed; the article states a full Hinson interview is embedded.",
     "unknown", S("f017"), "partially verified"],
    ["HIN-VID-0003", "HINSON", "https://www.newsweek.com/iowa-senate-debate-ashley-hinson-josh-turek-polls-watch-12536792",
     "2026-10-07", "unknown", "debate report with video", "Debate key moments|Polls",
     "unknown", "no", "Not viewed; the report describes the debate as it aired.",
     "unknown", S("f085"), "partially verified"],
    ["HIN-VID-0004", "HINSON", "https://www.kcci.com/article/why-republican-themes-are-showing-up-in-some-iowa-democrats-ads/73659473",
     "2026-09-09", "unknown", "ad-review package", "Campaign advertising|Immigration|Gun rights",
     "unknown", "no", "Not viewed; the article reviews the ad scripts, which are quoted in the text.",
     "unknown", S("f082"), "partially verified"],
    ["HIN-VID-0005", "HINSON", "https://abcnews.com/Politics/democrats-flipped-senate-blue-abc-news-voter-poll/story?id=137840395",
     "2026-11-04", "unknown", "network voter-poll segment", "Coalition|Senate flips",
     "unknown", "no", "Not viewed; the page is a text report on the ABC News voter poll.",
     "unknown", S("f195"), "partially verified"],
]
write("03_speeches/speech_video_index.csv", VID, V)

IO = lambda p, s: io.open(os.path.join(CASE, p), "w", encoding="utf-8", newline="\n").write(s)

IO("03_speeches/communication_analysis_turek.md", """# Josh Turek — bilingual communication analysis / 双语传播分析

**Scope / 范围**: 9 archived speech units (`TUR-SPC-0001` to `TUR-SPC-0009`), plus the event record and the ad record in this case. No recording was watched for this archive; the analysis works from verbatim quotations printed by the outlets that covered each appearance.

## 1. Register and persona / 语域与人格

English: The default register is first-person, plain, and declinist-then-hopeful: "Iowa has hit the bottom" is immediately followed by "fight for" clauses. He speaks as a witness ("I know firsthand what good public policy can do for an individual") rather than as a legislator reciting bills. Policy detail appears mostly in ads and debates, not in rally speeches.

中文：默认语域是第一人称、口语化、"先讲衰退再讲希望"。他以"见证者"而非"立法者"的身份说话——"我亲身知道好的公共政策能为一个人做什么"。政策细节主要出现在广告与辩论中，而非集会演说。

## 2. The biography unit / 传记段落的固定结构

English: The launch video, the primary-night speech and the closing interview share one narrative arc: working-class Council Bluffs → public services (free summer lunch, Area Education Agencies) → 21 surgeons before 12 → four Paralympic Games → two golds → the State House. The disability is stated as a fact inside the list ("who was born with my disability of spina bifida"), never as a metaphor and never as an appeal for sympathy.

中文：启动视频、初选夜演说与选前专访共用同一条叙事链：Council Bluffs 工人阶级家庭 → 公共补助（免费暑期午餐、AEA）→ 12 岁前 21 次手术 → 四届残奥会 → 两金 → 州议会。残疾是清单中的事实陈述（"born with my disability of spina bifida"），不是隐喻，也不是博取同情的诉求。

## 3. Rhetorical devices / 修辞手法

| Device / 手法 | Instance / 实例 | Effect / 效果 |
|---|---|---|
| Anaphora / 首语重复 | "Fight for Iowa. Fight for Iowans. Fight for the middle class. Fight for our workers." (`TUR-SPC-0003`) | Turns a list of constituencies into a rhythm; 把选民群体变成节奏 |
| Concession-pivot / 先让步再转折 | "I agree we should not cede the ground to China" + data-center regulation (`TUR-SPC-0005`) | Lets him sound hawkish and regulatory at once; 同时显得强硬与主张监管 |
| Corporate-accountability frame / 企业问责框架 | "paying their fair share, not getting tax breaks" (`TUR-SPC-0008`) | Converts a technical rate case into a fairness story; 把电价技术问题转为公平叙事 |
| Pledge ritual / 承诺仪式 | "I give each and every Iowa senior my pledge" (`TUR-SPC-0004`) | Creates a quasi-contract with one audience segment; 与特定选民群体形成准契约 |
| Self-labelling / 自我标签 | "prairie populist" (`TUR-SPC-0009`) | Names a regional identity the national party lacks; 命名一种全国性政党缺乏的地域身份 |

## 4. Audience calibration / 受众调适

English: Three audiences get three different speeches. Seniors get the pledge and the programme-defence (`TUR-SPC-0004`); county Democrats get the declinist state-of-Iowa speech (`TUR-SPC-0003`); primary voters get biography and electability (`TUR-SPC-0007`). The ad track runs a fourth message — a border-security ad that names President Trump approvingly (`TUR-SPC-0008` context, `05_campaign_media/advertisements.csv`).

中文：三类受众三种讲法。老年选民听到承诺与项目辩护；县党部活动听到"州已触底"的州情报；初选选民听到传记与"可胜选性"。广告则传递第四种信息——一支点名特朗普的边境安全广告。

## 5. What the record does not support / 记录不支持的部分

- No crowd-size claim is made here: only the Steak Fry report gives an observable ("standing ovation and hundreds of waving Turek signs"); the others do not.
- No timestamps: no transcript with timing was retrieved, so `major_quotes` carries `[unknown]` rather than invented timecodes.
- No claim about how he physically reaches a stage: no retrieved source describes staging, ramps or seating, so those fields say `unknown`.
""")

IO("03_speeches/communication_analysis_hinson.md", """# Ashley Hinson — bilingual communication analysis / 双语传播分析

**Scope / 范围**: 7 archived speech units (`HIN-SPC-0001` to `HIN-SPC-0007`) plus the event and ad records. Five of the seven rows are paraphrase-only: the retrieved reports describe what she argued without printing a verbatim quotation. That asymmetry with the Turek record is itself a finding.

## 1. Register and persona / 语域与人格

English: The register is conversational and credential-led: she speaks as a sitting member of Congress with a committee record, and she prefers worker and business testimony to her own narration. In the two debates she shifts to a short, adversarial register ("he's too liberal for this state").

中文：语域偏口语、以资历开场：她以现任国会议员与委员会记录说话，偏好让工人和小企业主提供证词，而非自己叙事。两场辩论中转为简短对抗式语域（"he's too liberal for this state"）。

## 2. Message architecture / 信息架构

| Layer / 层次 | Content / 内容 | Where it appears / 出现场合 |
|---|---|---|
| Affordability delivery / 生活成本"已交付" | Tips and overtime tax cuts, worker paychecks | `HIN-SPC-0004`, `HIN-EVT-0007` |
| Trade defence / 贸易辩护 | "Nobody loves tariffs, but ..." | `HIN-SPC-0006` |
| Security / 安全 | Border Patrol endorsement, "safe and secure communities" | `HIN-EVT-0010` |
| Technology and China / 技术与对华 | "if we don't, China will" | `HIN-SPC-0007` |
| Record attack / 记录攻击 | Missed votes, "too liberal" | `HIN-SPC-0005` |

## 3. Rhetorical devices / 修辞手法

| Device / 手法 | Instance / 实例 | Effect / 效果 |
|---|---|---|
| Concessive defence / 让步式辩护 | "Nobody loves tariffs, but what I like even less is an unlevel playing field" | Acknowledges the cost before reframing it as unfairness; 先承认代价再重构为"不公平" |
| Attendance attack / 出席率攻击 | "When he is showing up to vote, it's wrong for Iowa" | Turns a procedural fact into a character claim; 把程序事实变成品格指控 |
| Proxy testimony / 代理证词 | Workers describe their own paychecks (`HIN-EVT-0007`) | Makes the policy claim verifiable-sounding without her asserting it; 让政策主张听起来可核验 |
| National-security framing / 国家安全框架 | Children vs Beijing (`HIN-SPC-0007`) | Raises a domestic tech issue to a geopolitical stake; 把国内技术议题提升为地缘政治赌注 |
| Instrumental performance / 器乐表演 | Played violin with the opening performers at the BBQ Bash (`HIN-EVT-0005`) | Softens a partisan fundraiser into a community event; 把党派筹款会软化为社区活动 |

## 4. Surrogate dependence / 对代理人的依赖

English: Three of the largest Hinson events in this archive are carried by surrogates: Cruz at the roundtable and the BBQ Bash, Barrasso at the small-business roundtable, Kennedy at the Faith and Freedom fundraiser. That is a scheduling fact, not a criticism — but it means the archive's record of her own spoken words is thinner than her event count suggests.

中文：本档案中三场规模最大的 Hinson 活动由代理人主导（Cruz、Barrasso、Kennedy）。这是日程事实，不是评价；但它意味着档案中她本人的言语记录比活动数量所显示的更薄。

## 5. What the record does not support / 记录不支持的部分

- No verbatim quotation exists in the retrieved pages for the launch show, the Ankeny roundtable, the BBQ Bash or the Whiskey River roundtable; those rows are marked `(paraphrase)`.
- No crowd figure is asserted for the Ankeny or Whiskey River events: the reports give none.
- No visual description of her at the Faith and Freedom fundraiser exists, so the row is recorded as a surrogate event.
""")
print("communication analyses written")
