# -*- coding: utf-8 -*-
"""Candidate biographies, career timelines, political-position memos, policy_positions.csv."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CASE, S, write

POS_H = ["position_id", "candidate_id", "issue", "subissue", "position_summary",
         "candidate_statement", "statement_date", "context", "source_urls", "legislative_record",
         "position_changed", "change_notes", "opponent_criticism", "fact_check",
         "verification_status"]

T, H = "TUREK", "HINSON"
P = []


def pos(cid, issue, sub, summary, stmt, sdate, ctx, src, rec, changed, chnote, opp, fact, ver):
    n = len([r for r in P if r[1] == cid]) + 1
    prefix = "TUR" if cid == T else "HIN"
    P.append(["%s-POS-%04d" % (prefix, n), cid, issue, sub, summary, stmt, sdate, ctx, S(src),
              rec, changed, chnote, opp, fact, ver])


# ---------------- Turek ----------------
pos(T, "Healthcare", "Medicaid",
    "Opposes the Medicaid reductions in the 2025 reconciliation law and pledges to reverse them.",
    "\"I give each and every Iowa senior my pledge - I will do everything I can to protect Medicare, Medicaid, and Social Security, and expand it to all of you.\"",
    "2026-09-09", "Remarks to residents at Scottish Rite Park, Des Moines", "f124",
    "Voted against the state-level Medicaid package he describes as a cut; no Senate record.", "no", "unknown",
    "Hinson campaign says she has never cut Social Security and voted for the Social Security Fairness Act.",
    "The pledge is a campaign statement; no costed proposal was published.",
    "partially verified")
pos(T, "Healthcare", "Medicare",
    "Pledges to protect and expand Medicare rather than reduce it.",
    "\"I will do everything I can to protect Medicare, Medicaid, and Social Security, and expand it to all of you.\"",
    "2026-09-09", "Scottish Rite Park senior living center, Des Moines", "f124",
    "unknown", "no", "unknown",
    "Hinson's campaign disputes the premise that she voted to cut the programs.", "Direct quotation, single outlet.",
    "partially verified")
pos(T, "Healthcare", "Public option",
    "Supports a public health insurance option and restoring enhanced ACA subsidies.",
    "No verbatim quotation retrieved; the position is described in the campaign coverage indexed here.",
    "2026-03-10", "Rural health-care listening visit reported by the Des Moines Register", "dmr_turek_health",
    "unknown", "no", "unknown", "unknown",
    "The underlying article is paywalled (HTTP 402); the position is carried by the headline and by Wikipedia's summary.",
    "partially verified")
pos(T, "Healthcare", "Social Security financing",
    "Wants to eliminate the Social Security payroll-tax cap to keep the trust fund solvent.",
    "Called it \"ridiculous\" that regular Americans pay into Social Security year-round while the wealthiest do not pay more past the wage cap.",
    "2026-09-09", "Scottish Rite Park, Des Moines, with Martin O'Malley and Jon Bauman", "f124",
    "unknown", "no", "unknown",
    "Hinson's campaign calls the charge that she cut Social Security false.", "Paraphrase of reported remarks; no bill text.",
    "partially verified")
pos(T, "Healthcare", "Rural health care",
    "Campaigns on rural hospital and clinic closures and links them to Medicaid reductions.",
    "Said as many as 842 \"healthcare entities\" have closed across Iowa since Hinson took national office.",
    "2026-09-09", "Scottish Rite Park, Des Moines", "f124",
    "unknown", "no", "unknown",
    "The 842 figure is the candidate's own count; no state register was retrieved to confirm it.",
    "Candidate-supplied number, not independently verified in this archive.", "unverified")
pos(T, "Healthcare", "Food assistance (SNAP)",
    "Criticises his opponent for voting to cut \"healthcare and food programs\".",
    "\"She stands for cuts to healthcare and food programs, support of tariffs and war and tax breaks to billionaires.\"",
    "2026-08-29", "Polk County Democrats' Steak Fry, Des Moines", "f130",
    "unknown", "no", "unknown",
    "Hinson supported the OBBBA nutrition changes as fiscally responsible.", "Paraphrase of a campaign attack; no SNAP vote in his own record.",
    "partially verified")
pos(T, "Abortion", "Federal codification",
    "Supports federal legislation to restore the protections that Roe v. Wade provided.",
    "No verbatim quotation retrieved; position summarised in the race coverage indexed here.",
    "2026-03-10", "Health-care round of interviews during the primary", "dmr_turek_health",
    "unknown", "no", "unknown",
    "Hinson opposes a legal right to abortion with exceptions for rape, incest and the life of the mother.",
    "Paywalled source; position corroborated by the race article.", "partially verified")
pos(T, "Abortion", "Iowa six-week ban",
    "Says Iowa's six-week abortion ban reduced the availability of OB-GYN services.",
    "No verbatim quotation retrieved; the claim is attributed to him in the race coverage indexed here.",
    "2026-03-10", "Campaign interviews, spring 2026", "dmr_turek_health",
    "unknown", "no", "unknown",
    "Hinson supports the six-week law.", "The OB-GYN claim was not independently fact-checked in the retrieved pages.",
    "unverified")
pos(T, "Gun policy", "Second Amendment",
    "Presents himself as a gun-rights-friendly Democrat; his ads say he voted with Republicans on gun protections.",
    "Ad narration: he \"voted with Republicans more than 700 times on issues including tax cuts and gun rights protections\".",
    "2026-09-09", "Two television ads reviewed by KCCI", "f082",
    "State House votes only; no federal record.", "no", "unknown",
    "no opponent attack on guns retrieved.", "The \"700 times\" figure is the campaign's own tally.",
    "partially verified")
pos(T, "Immigration", "Border security",
    "Runs ads promising to work with President Trump to secure the border and stop the flow of drugs.",
    "\"I'm Josh Turek, and in the U.S. Senate, I'll work with anyone to fix it, including President Trump, to secure the border [and] stop the flow of drugs into Iowa.\"",
    "2026-09-09", "Immigration-focused television ad reviewed by KCCI", "f082",
    "unknown", "no", "unknown",
    "Hinson says he is too liberal for Iowa and cites his missed votes.", "Verbatim ad script; the ad itself was not archived.",
    "partially verified")
pos(T, "Immigration", "Framing",
    "Argues border security should not be a partisan issue.",
    "\"I think that all Iowans recognize that we can have two things be true at the same time. We need to have safe and secure borders. We do.\"",
    "2026-09-09", "Interview with KCCI alongside the ad review", "f082",
    "unknown", "no", "unknown", "unknown", "Verbatim quotation, single outlet.",
    "partially verified")
pos(T, "Energy", "Ethanol and E15",
    "Supports year-round sales of E15 blended gasoline.",
    "No verbatim quotation retrieved; the position is reported from the October 13 debate coverage.",
    "2026-10-13", "Second U.S. Senate debate, WHO-13, Des Moines", "f077",
    "unknown", "no", "unknown",
    "Hinson is endorsed by the Iowa Corn Growers PAC, which weighs ethanol support.", "Position reported, not quoted.",
    "partially verified")
pos(T, "Energy", "Data centers and electricity rates",
    "Opposes tax breaks for data-center operators and wants guardrails so they do not raise residential power rates.",
    "\"We want to make sure large corporations are paying their fair share, not getting tax breaks. I think also making sure we've got strong guardrails to make sure they are not driving up the energy rate to the end user.\"",
    "2026-09-21", "Campaign stop in Des Moines, quoted by USA Today", "usat_datacenter",
    "unknown", "no", "unknown",
    "Hinson favours AI development and an \"AI economy\".", "Quotation reproduced from the paywalled article via the Wikipedia citation; not read on the publisher page.",
    "partially verified")
pos(T, "Economy", "Tariffs",
    "Calls the 2025-26 tariff regime damaging to Iowa farmers and supports only targeted tariffs.",
    "\"Our farmers rely on open markets and free trade more than any other group.\"",
    "2026-10-13", "Second U.S. Senate debate, WHO-13, Des Moines", "f077",
    "unknown", "no", "unknown",
    "Hinson defends tariffs as a counter to unfair trade practices.", "Verbatim debate quotation.",
    "partially verified")
pos(T, "Economy", "Farm bill",
    "Urges Congress to pass a farm bill before adjourning.",
    "No verbatim quotation retrieved; reported from the October 13 debate.", "2026-10-13",
    "Second U.S. Senate debate, WHO-13, Des Moines", "f077",
    "unknown", "no", "unknown",
    "Hinson is rated a \"Friend of Agriculture\" by the Iowa Farm Bureau PAC.", "Position reported, not quoted.",
    "partially verified")
pos(T, "Economy", "Farm equipment right-to-repair",
    "Supports a federal right-to-repair law for agricultural equipment.",
    "No verbatim quotation retrieved; reported from the October 13 debate.", "2026-10-13",
    "Second U.S. Senate debate, WHO-13, Des Moines", "f077",
    "unknown", "no", "unknown", "unknown", "Position reported, not quoted.", "partially verified")
pos(T, "Economy", "Country-of-origin labeling",
    "Supports mandatory country-of-origin labeling for agricultural products.",
    "No verbatim quotation retrieved; reported from the October 13 debate.", "2026-10-13",
    "Second U.S. Senate debate, WHO-13, Des Moines", "f077",
    "unknown", "no", "unknown", "unknown", "Position reported, not quoted.", "partially verified")
pos(T, "Economy", "Cost of living",
    "Makes affordability - food, rent, utilities, health care - the centre of the general-election message.",
    "\"And really, Iowa, we have hit the bottom. This is not the state that we know. This is not the state we grew up in.\"",
    "2026-08-29", "Polk County Democrats' Steak Fry, Des Moines", "f130",
    "unknown", "no", "unknown",
    "Hinson counters with the OBBBA tax cuts on tips and overtime.", "Verbatim quotation.",
    "partially verified")
pos(T, "Other", "Disability policy and the ADA",
    "Treats the Americans with Disabilities Act as the policy that made his own career possible and campaigns as the Legislature's first permanently disabled member.",
    "\"I'm running for Senate because I know firsthand what good public policy can do for an individual, and I'm ready to deliver for Iowa.\"",
    "2026-02-20", "Statement accompanying Tony Coelho's endorsement", "f060",
    "Iowa House: Health and Human Services Committee, Health Policy Oversight Committee; former ranking member, Veterans Affairs.", "no", "unknown",
    "No opponent attack on disability policy retrieved.",
    "Biographical fact: Turek was born with spina bifida and uses a wheelchair; the archive describes it as a documented condition, not a metaphor.",
    "verified")
pos(T, "Other", "Artificial intelligence",
    "Wants AI and data-center oversight, does not want the United States to cede the field to China.",
    "\"I agree we should not cede the ground to China\" ... \"I am absolutely in favor of some regulations on data centers.\"",
    "2026-10-07", "First U.S. Senate debate, Iowa PBS", "f085",
    "unknown", "no", "unknown",
    "Hinson argues an \"AI economy\" is needed to win the race with China.", "Verbatim quotations from debate coverage.",
    "partially verified")
pos(T, "Other", "Transgender rights",
    "Opposes gender-affirming surgery for minors, Medicaid funding for such care and trans women in women's sports, but voted against school notification and restroom bills.",
    "No verbatim quotation retrieved; positions and votes summarised in his Wikipedia article with news citations.",
    "2026-10-31", "State House record and 2026 campaign coverage", "wiki",
    "Iowa House votes against the pronoun-notification bill and the school restroom bill; campaign cited risk to disabled Iowans and caregivers.",
    "no", "unknown",
    "Hinson opposes LGBTQ movements per the race coverage.", "Positions rest on a T3 encyclopedic source; no primary record retrieved.",
    "partially verified")
pos(T, "Other", "Transgender rights (advertising)",
    "Restated the same positions in a paid ad, framing them as fairness plus rules and as a rejection of both extremes.",
    '''"As a kid in a wheelchair, I faced my share of bullying. That's why I believe that no Iowan should face discrimination. As a Paralympian, I also know it's important to have rules. It's why I oppose males competing in female sports, something that is already illegal in Iowa. I'm against taxpayers paying for sex changes too. Anyone tells you any different is lying."''',
    "2026-10-25", "Ad titled Stop the Nonsense, released the Sunday before the final debate", "f201",
    "Ad cites Iowa's existing ban on transgender athletes as already settled law.", "no", "unknown",
    "One Iowa Action called it a dramatic departure from other Democratic candidates and condemned it; Hinson and other Republicans said the ad misrepresented his record.",
    "Ad script printed verbatim by Iowa Capital Dispatch; the criticism from both sides is documented in the same report.",
    "verified")
pos(T, "Labor", "Unions",
    "Collects federal-employee, firefighter and food-worker union endorsements.",
    "No verbatim quotation retrieved; endorsement releases indexed here.", "2026-09-01",
    "AFGE endorsement release", "f134",
    "unknown", "no", "unknown", "unknown", "Endorsement, not a policy commitment.", "partially verified")
pos(T, "Democracy", "Term limits",
    "Supports congressional term limits.",
    "\"Turek said he also agreed there's a need for term limits.\"", "2026-08-29",
    "Polk County Democrats' Steak Fry, Des Moines", "f130",
    "unknown", "no", "unknown", "unknown", "Reported indirectly, not quoted in full.", "partially verified")
pos(T, "Foreign policy", "Gaza aid conditions",
    "Called for conditions on U.S. aid to Israel during the Gaza war.",
    "\"The response at this point has been disproportionate, and I don't think that taxpayer dollars or United States support should be going toward the hurting or killing of children or civilians or certainly not impeding aid going into these areas.\"",
    "2025-08-18", "Statement during the Gaza war", "wiki",
    "unknown", "no", "unknown", "unknown", "Quotation carried by Wikipedia with a news citation; original outlet not retrieved.",
    "partially verified")
pos(T, "Foreign policy", "Iran war",
    "Opposes the 2026 Iran war and ties it to fuel and living costs in Iowa.",
    "Called it an \"unnecessary war\" in July 2026.", "2026-07-01", "Campaign remarks during the Iran war", "wiki",
    "unknown", "no", "unknown", "unknown", "Date is month-level only.", "partially verified")
pos(T, "Education", "Public schools and AEAs",
    "Cites the free summer lunch programme and Area Education Agencies as supports his family used, and attacks the state of Iowa schooling.",
    "Highlighted \"Iowa's declining educational system\" at the Steak Fry.", "2026-08-29",
    "Polk County Democrats' Steak Fry, Des Moines", "f130",
    "unknown", "no", "unknown", "unknown", "Two separate claims from two sources.", "partially verified")

# ---------------- Hinson ----------------
pos(H, "Healthcare", "Medicaid and the OBBBA",
    "Supported the 2025 reconciliation law's Medicaid changes as fiscally responsible.",
    "No verbatim quotation retrieved; the position is attributed to her in the race coverage indexed here.",
    "2026-10-13", "General-election coverage of the Medicaid dispute", "wiki",
    "Voted for the One Big Beautiful Bill Act in the U.S. House.", "no", "unknown",
    "Turek says she voted to cut Medicaid and that 842 Iowa health-care entities have closed.",
    "Position rests on a T3 source plus the Turek campaign's characterisation; her floor statement was not retrieved.",
    "partially verified")
pos(H, "Healthcare", "Social Security",
    "Says she has never cut Social Security and opposes raising the retirement age.",
    "\"Ashley Hinson has never and will never cut a penny from Social Security - she is fighting to protect it for Iowa seniors.\" (campaign communications director Billy Fuerst)",
    "2026-09-09", "Emailed statement responding to Turek's Scottish Rite Park event", "f124",
    "Voted for the Working Families Tax Cuts and the Social Security Fairness Act per her campaign.", "yes",
    "In 2020 she said she was open to raising the retirement age to preserve the programme.",
    "Turek says she voted for $452 million in SSA cuts and to let DOGE drive out staff.",
    "The 2020 openness to a higher retirement age and the 2026 denial are both documented; the campaign's statement is self-reported.",
    "partially verified")
pos(H, "Abortion", "Legal status",
    "Opposes a legal right to abortion, with exceptions for rape, incest and the life of the mother.",
    "No verbatim quotation retrieved; the position is attributed to her in the race coverage indexed here.",
    "2026-10-31", "General-election coverage of abortion politics", "nyt_iowa",
    "State House and U.S. House votes against abortion-rights measures; details unknown.", "no", "unknown",
    "Turek supports codifying Roe and says the six-week ban cut OB-GYN services.",
    "Paywalled source; position corroborated by the race article and by SBA Pro-Life America's endorsement list.",
    "partially verified")
pos(H, "Abortion", "Planned Parenthood funding",
    "Voted to remove several funding streams from Planned Parenthood while saying she supported its non-abortion services.",
    "No verbatim quotation retrieved; Bleeding Heartland documents the 2017 family-planning, 2019 sex-education and Medicaid payment votes.",
    "2019-06-01", "Iowa House and U.S. House record as summarised in a T3 analysis", "f018",
    "Iowa House votes on family planning (2017) and sex education grants (2019); Medicaid payments later.", "no", "unknown",
    "Planned Parenthood Advocates of Iowa endorsed Turek.", "T3 source; vote dates are year-level in the retrieved text.",
    "partially verified")
pos(H, "Abortion", "Interest-group alignment",
    "Listed as an endorsed candidate by SBA Pro-Life America.",
    "No verbatim quotation retrieved; the endorsement listing is the evidence.", "2026-10-15",
    "SBA Pro-Life America 2026 endorsed-candidates page", "f032",
    "unknown", "no", "unknown", "unknown", "Endorsement page did not render her name in the archived copy; the listing is taken from the page as fetched.",
    "unverified")
pos(H, "Gun policy", "Firearms",
    "No gun-policy statement by Hinson was located in the pages retrieved for this archive.",
    "unknown", "2026-11-18", "Gap recorded rather than inferred", "f121",
    "unknown", "unknown", "unknown",
    "Turek's ads say he voted with Republicans on gun-rights protections.",
    "The NRA-PVF Iowa ratings page archived here did not render candidate grades, so no grade is asserted.",
    "unverified")
pos(H, "Immigration", "Border security",
    "Backs border-security enforcement; the Border Patrol agents' union endorsed her on that basis.",
    "\"Iowans deserve safe and secure communities.\"", "2026-10-13",
    "News conference with the National Border Patrol Council, Urbandale", "f116",
    "Voted for House border-security packages; bill numbers unknown.", "no", "unknown",
    "Turek runs ads promising to work with Trump on border security.",
    "Quotation is the sub-headline of the Gazette report.", "partially verified")
pos(H, "Energy", "Ethanol",
    "Backed by the Iowa Corn Growers Association PAC, which weighs ethanol positions in its endorsements.",
    "No verbatim quotation retrieved; the endorsement release is the evidence.", "2026-09-02",
    "Iowa Corn Growers Association PAC 2026 endorsements", "f118",
    "unknown", "no", "unknown",
    "Turek calls for year-round E15 sales and an end to the tariffs.", "Endorsement implies alignment; no direct ethanol statement retrieved.",
    "partially verified")
pos(H, "Economy", "Agriculture and the farm bill",
    "Designated a \"Friend of Agriculture\" by the Iowa Farm Bureau PAC.",
    "No verbatim quotation retrieved; the designation release is the evidence.", "2026-09-02",
    "Iowa Farm Bureau PAC 2026 designations", "f119",
    "unknown", "no", "unknown",
    "Turek urges passage of a farm bill before adjournment.", "Designation, not a policy statement.",
    "partially verified")
pos(H, "Economy", "Tariffs",
    "Defends tariffs as a response to unfair trade practices while acknowledging farmers' uncertainty.",
    "\"Nobody loves tariffs, but what I like even less is an unlevel playing field for Americans and for our farmers.\"",
    "2026-10-13", "Second U.S. Senate debate, WHO-13, Des Moines", "f077",
    "unknown", "no", "unknown",
    "Turek says tariffs decimated markets for Iowa farmers.", "Verbatim debate quotation.",
    "partially verified")
pos(H, "Economy", "Taxes",
    "Campaigns on the OBBBA tax cuts for tips and overtime.",
    "No verbatim quotation retrieved; the Ankeny event coverage reports the argument she and Sen. Barrasso made.",
    "2026-09-19", "Campaign event at Whiskey River, Ankeny", "f106",
    "Voted for the One Big Beautiful Bill Act.", "no", "unknown",
    "Turek calls the law tax breaks for billionaires.", "Position reported, not quoted.",
    "partially verified")
pos(H, "Economy", "Foreign ownership of farmland",
    "Wants to stop foreign adversaries from buying agricultural land near sensitive sites.",
    "No verbatim quotation retrieved; reported from the October 13 debate.", "2026-10-13",
    "Second U.S. Senate debate, WHO-13, Des Moines", "f077",
    "unknown", "no", "unknown", "unknown", "Position reported, not quoted.", "partially verified")
pos(H, "Economy", "Data centers and AI",
    "Favours AI development and an \"AI economy\"; says worker retraining must accompany it.",
    "\"because the truth is: if we don't, China will.\"", "2026-03-20",
    "Op-ed distributed by the NRSC", "f087",
    "unknown", "no", "unknown",
    "Turek wants data-center regulation and no tax breaks for operators.", "Quotation is from her own op-ed.",
    "partially verified")
pos(H, "Other", "LGBTQ policy",
    "Opposes LGBTQ movements per the race coverage, while appearing on an LGBT Republican group's endorsement list.",
    "No verbatim quotation retrieved.", "2026-11-04",
    "Race coverage and a Newsweek endorsement list", "f030",
    "unknown", "no", "unknown",
    "Turek's positions on trans rights are themselves mixed (see TUR rows).",
    "Two sources point in opposite directions; recorded as a conflict rather than resolved.",
    "conflicting sources")
pos(H, "Other", "China competition",
    "Frames AI and trade policy as a contest with China.",
    "\"I agree we should not cede the ground to China\" is Turek's line; Hinson's op-ed says an AI economy is needed \"because the truth is: if we don't, China will\".",
    "2026-10-20", "Voice of America coverage of the China debate in midterms", "f086",
    "unknown", "no", "unknown", "unknown", "Hinson's sentence is quoted in the race article from her op-ed.",
    "partially verified")
pos(H, "Democracy", "Election administration",
    "No position on election administration was located in the retrieved pages.",
    "unknown", "2026-11-18", "Gap recorded rather than inferred", "wiki",
    "unknown", "unknown", "unknown", "unknown", "Recorded as a gap.", "unverified")
pos(H, "Education", "Schools",
    "No K-12 or higher-education position statement was located in the retrieved pages.",
    "unknown", "2026-11-18", "Gap recorded rather than inferred", "wiki",
    "unknown", "unknown", "unknown",
    "Turek attacks \"Iowa's declining educational system\".", "Recorded as a gap; no inference made.",
    "unverified")
pos(H, "Labor", "Unions",
    "No union endorsement of Hinson was located; the U.S. Chamber of Commerce endorsed her.",
    "No verbatim quotation retrieved; the Chamber endorsement is the evidence.", "2026-10-11",
    "U.S. Chamber of Commerce endorsement reported by KCRG", "f123",
    "unknown", "no", "unknown",
    "Turek holds AFGE, firefighter and UFCW endorsements.", "Endorsement, not a policy commitment.",
    "partially verified")

write("01_candidates/policy_positions.csv", POS_H, P)
print("turek positions:", len([r for r in P if r[1] == T]), "hinson:", len([r for r in P if r[1] == H]))
