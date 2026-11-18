"""Build 01_candidates/: policy_positions.csv + career_timeline.csv per candidate."""
import sys

sys.path.insert(0, "_staging")
from b_common import ref, write_csv  # noqa: E402

PP_FIELDS = ["position_id", "candidate_id", "issue", "subissue", "position_summary",
             "candidate_statement", "statement_date", "context", "source_urls",
             "legislative_record", "position_changed", "change_notes",
             "opponent_criticism", "fact_check", "verification_status"]

NV = "no verbatim statement retrieved in this archive"

POSITIONS = [
    # ---------------- Sherrod Brown -----------------------------------------
    dict(candidate_id="BROWN", issue="Economy", subissue="tariffs and trade",
         position_summary="Opposes the 2025-26 Trump tariff regime as a cost on Ohio "
         "farmers and consumers, while keeping a long protectionist record that supported "
         "some tariffs in the past.",
         candidate_statement="\"Farmers can't afford a new tractor or a new combine. They in "
         "many cases can't even afford spare parts because of the tariffs.\" (Cleveland.com, "
         "2026-11-13); the Dispatch issue survey records that \"Brown and Redpath oppose "
         "Trump's tariffs\".",
         statement_date="2026-11-13",
         context="Post-election interview and the Columbus Dispatch candidate issue survey.",
         source_urls=ref("b4_cle_return", "b4_yahoo_keyissues", "wiki_brown"),
         legislative_record="Voted against NAFTA; supported the 2018 washing-machine tariffs "
         "and USMCA; author of 'Myths of Free Trade' (2006) — per Wikipedia biography.",
         position_changed="partial",
         change_notes="A pro-tariff legislator in 2018 who campaigned in 2026 against the "
         "tariffs in force. The archive records the shift without adjudicating it.",
         opponent_criticism="Husted's spokesperson said Husted backs \"boosting access to "
         "foreign markets\" while ensuring Ohio businesses are treated fairly.",
         fact_check="The $11 billion / $2,200-per-household cost figure in the Dispatch "
         "survey is attributed to the National Taxpayers Union Foundation, an advocacy "
         "group, not an official estimate.",
         verification_status="verified"),
    dict(candidate_id="BROWN", issue="Labor", subissue="unions, UAW and the right to organize",
         position_summary="Union-first campaign built on endorsements from the UAW, "
         "Steelworkers, IUPAT, IFPTE, CWA, the Ohio Federation of Teachers and the Ohio "
         "AFL-CIO; pledges to co-sponsor the Faster Labor Contracts Act.",
         candidate_statement="Teamsters endorsement release: Brown \"introduced the "
         "bipartisan Railway Safety Act\" and \"has committed to co-sponsoring the Faster "
         "Labor Contracts Act in the Senate\".",
         statement_date="2026-07-15",
         context="Ohio Conference of Teamsters 2026 endorsement release.",
         source_urls=ref("ref132_teamster_org_2026_07_ohio_conference_of_teamsters_annou",
                         "ref072_chroniclet_com_news_448231_uaw_endorses_democrat_sherro",
                         "ref029_chroniclet_com_news_452022_2026_us_senate_race_united_s"),
         legislative_record="Railway Safety Act (bipartisan, with JD Vance, 2023); pension "
         "protection for Teamsters retirees; Senate Banking Committee chair 2021-2025.",
         position_changed="no", change_notes="Consistent labor alignment across the cycle.",
         opponent_criticism="Husted campaign argues Brown's long tenure produced no wage "
         "gains; Husted: \"he's been in office for over 50 years\".",
         fact_check="Endorsement claims are sponsor-stated; the Railway Safety Act's failure "
         "in the Senate is documented in the Wikipedia JD Vance article.",
         verification_status="verified"),
    dict(candidate_id="BROWN", issue="Economy", subissue="manufacturing and CHIPS",
         position_summary="Pitches an Ohio manufacturing revival and frames productivity "
         "gains as captured by corporations rather than wages.",
         candidate_statement="\"Ohio workers are more productive than ever, but no matter "
         "how hard they work, their pay doesn't keep up.\" (statement to the Columbus "
         "Dispatch, published 2026-10-18).",
         statement_date="2026-10-18",
         context="Dispatch candidate issue survey.",
         source_urls=ref("b4_yahoo_keyissues", "ocj14_ohios_intel_plant_has_been_stalled"),
         legislative_record="Championed the Dignity of Work Institute after leaving the "
         "Senate (2025-03-25); no 2026 legislative record (not in office during the race).",
         position_changed="unknown", change_notes="unknown",
         opponent_criticism="Husted credits Trump-era tariff protection with Kenworth "
         "adding 1,000 jobs in Chillicothe and calls that \"the America First agenda\".",
         fact_check="The 1,000-job Kenworth figure is the Husted campaign's own claim as "
         "quoted by Cleveland.com; not independently confirmed in this archive.",
         verification_status="partially verified"),
    dict(candidate_id="BROWN", issue="Abortion", subissue="Ohio Issue 1 and federal codification",
         position_summary="Pro-choice; campaigned with abortion-rights groups in a state "
         "whose constitution has protected abortion since Issue 1 (2023).",
         candidate_statement=NV,
         statement_date="unknown",
         context="No 2026 Brown statement on abortion was retrieved; the position is "
         "inferred from endorsements and the state context, which is why it is marked "
         "partially verified.",
         source_urls=ref("wiki_issue1_2023", "ref080_www_lcv_org_media_center_lcv_action",
                         "ref076_thebuckeyeflame_com_2025_12_19_human_rights_campaign_en"),
         legislative_record="Senate record includes support for codifying Roe; not "
         "re-verified from a primary document in this archive.",
         position_changed="unknown", change_notes="unknown",
         opponent_criticism="Husted attacked the abortion pill in a Senate hearing and "
         "cited his own adoption story; he did not contest Issue 1 in this race.",
         fact_check="Issue 1 (2023-11-07) passed 57%-43% per Wikipedia.",
         verification_status="partially verified"),
    dict(candidate_id="BROWN", issue="Gun policy", subissue="access restrictions",
         position_summary="Supports restricting gun access for people with criminal records "
         "or mental-health issues; endorsed by Giffords.",
         candidate_statement="WLWT reports Brown supports \"restricting gun access for "
         "certain people with criminal records and mental-health issues\".",
         statement_date="2026-11-02",
         context="WLWT sit-down published with the result coverage.",
         source_urls=ref("b4_wlwt_result", "ref075_giffords_org_press_release_2025_09_giffor"),
         legislative_record="Giffords endorsement (2025-09-18); Senate votes not re-verified "
         "here.",
         position_changed="unknown", change_notes="unknown",
         opponent_criticism="No Husted gun-policy attack retrieved.",
         fact_check="not applicable", verification_status="partially verified"),
    dict(candidate_id="BROWN", issue="Immigration", subissue="TPS, deportation and border",
         position_summary="Supports deporting immigrants convicted of serious crimes, "
         "extending TPS for Springfield's Haitian community, and a legalization path for "
         "long-resident taxpayers.",
         candidate_statement="\"I, of course, support deportation of those people who have "
         "committed a serious crime... Beyond that, I want to see us work out a real policy "
         "on immigration where people who have been in this country and worked hard and "
         "paid their taxes can continue to contribute to society.\" (reporters, August 2026, "
         "quoted by the Dispatch).",
         statement_date="2026-10-18",
         context="Dispatch issue survey; OCJ also reports Brown pressing DeWine and Ohio's "
         "senators on TPS.",
         source_urls=ref("b4_yahoo_keyissues", "ocj05_ohio_senators_governor_respond_to_cal"),
         legislative_record="Opposed the 2025 executive order on sanctuary jurisdictions; "
         "backed fentanyl-trafficking and human-smuggling penalties and border technology "
         "funding (per the Dispatch survey).",
         position_changed="no", change_notes="Consistent with his Senate record.",
         opponent_criticism="Husted: \"Why do people like Sherrod Brown care more about "
         "people who are illegally in this country than he cares about you?\"",
         fact_check="The Dispatch attributes the legislative record summary to the "
         "campaigns' own descriptions.",
         verification_status="verified"),
    dict(candidate_id="BROWN", issue="Energy", subissue="data centers and electricity bills",
         position_summary="Wants data centers to pay for their own power and opposes "
         "\"out-of-control tax giveaways\"; makes Husted's data-center recruitment the "
         "centre of his closing argument.",
         candidate_statement="\"Husted's been the front guy on all these data centers, 200 "
         "in Ohio, getting huge over-the-top tax breaks, and raising utility rates.\" "
         "(Ohio Capital Journal interview, 2026-08-21)",
         statement_date="2026-08-21",
         context="OCJ story on the leaked NRSC memo.",
         source_urls=ref("ocj31_leaked_memo_about_data_centers_shows_gop_worried_about",
                         "b4_yahoo_keyissues", "b4_cle_clash"),
         legislative_record="No 2026 legislative record; position expressed in ads and "
         "interviews.",
         position_changed="partial",
         change_notes="Brown applauded Amazon's central-Ohio data center in a 2015 release "
         "(per the Dispatch survey) — a documented earlier position.",
         opponent_criticism="Husted says data centers bring jobs and money to rural Ohio; "
         "DeWine defends them as economic development.",
         fact_check="The \"200 in Ohio\" figure is Brown's own count, not an official tally.",
         verification_status="verified"),
    dict(candidate_id="BROWN", issue="Energy", subissue="clean energy and Great Lakes",
         position_summary="Frames environmental protection as an Ohio jobs and public-health "
         "issue; endorsed by the League of Conservation Voters Action Fund.",
         candidate_statement="\"When Norfolk Southern's negligence contaminated East "
         "Palestine, I was there from day one holding them accountable and securing federal "
         "resources.\" (LCV endorsement release)",
         statement_date="2026-02-24",
         context="LCV Action Fund endorsement.",
         source_urls=ref("ref080_www_lcv_org_media_center_lcv_action"),
         legislative_record="Lead-paint and lead-pipe remediation work; Great Lakes "
         "protection, per the same release.",
         position_changed="unknown", change_notes="unknown",
         opponent_criticism="Husted blames Brown for \"radical environmental policies that "
         "closed 23 power plants in the state\" (Boardman rally, 2026-10-15).",
         fact_check="The 23-plant figure is Husted's claim at a rally; not verified here.",
         verification_status="partially verified"),
    dict(candidate_id="BROWN", issue="Other", subissue="rail safety after East Palestine",
         position_summary="Author of the bipartisan Railway Safety Act introduced after the "
         "2023-02-03 Norfolk Southern derailment; returns to the derailment as a "
         "accountability story.",
         candidate_statement="\"I want to see rail safety legislation passed in the next few "
         "weeks.\" (East Palestine press briefing, 2023-02-27, recorded by Wikipedia)",
         statement_date="2023-02-27",
         context="East Palestine derailment response — pre-campaign record.",
         source_urls=ref("wiki_eastpal", "ref132_teamster_org_2026_07_ohio_conference_of_te"),
         legislative_record="Railway Safety Act co-sponsored with JD Vance (2023-03-01); the "
         "bill did not pass.",
         position_changed="no", change_notes="Position unchanged; the bill's failure is the "
         "record.",
         opponent_criticism="No Husted attack on Brown's rail record retrieved.",
         fact_check="Bill failure documented in the Wikipedia JD Vance article.",
         verification_status="verified"),
    dict(candidate_id="BROWN", issue="Healthcare", subissue="ACA subsidies and premiums",
         position_summary="Attacks the lapse of enhanced ACA subsidies and the coverage "
         "losses that followed; frames health costs as an affordability issue.",
         candidate_statement="\"These hospitals are a lifeline for their communities, "
         "especially for low-income families... This will continue to be a priority for me "
         "in the Senate.\" (Dispatch survey, on rural hospitals)",
         statement_date="2026-10-18",
         context="Dispatch issue survey.",
         source_urls=ref("b4_yahoo_keyissues", "ocj10_ohio_u_s_sen_jon_husted_wants_to_fre"),
         legislative_record="Senate record includes ACA defense; not re-verified from a "
         "primary document here.",
         position_changed="no", change_notes="Consistent across the cycle.",
         opponent_criticism="Husted says Brown and Democrats \"created the broken ACA "
         "system\" and offers a two-year subsidy extension with a $5 monthly payment.",
         fact_check="Around 161,000 Ohioans lost or dropped coverage Feb 2025-Feb 2026 per "
         "the Dispatch survey (source not named in the retrieved text).",
         verification_status="partially verified"),
    dict(candidate_id="BROWN", issue="Economy", subissue="tax law and child tax credit",
         position_summary="Calls the 2025 tax law tilted to high earners; backs restoring the "
         "expanded child tax credit.",
         candidate_statement="\"...cutting taxes for working families, not billionaires and "
         "corporations.\" (statement to the Dispatch, 2026-10-18)",
         statement_date="2026-10-18",
         context="Dispatch issue survey.",
         source_urls=ref("b4_yahoo_keyissues", "b4_wlwt_result"),
         legislative_record="Not in office in 2026; no vote on the 2025 law.",
         position_changed="no", change_notes="unknown",
         opponent_criticism="Husted backed the law and cites a projected $3,173 average "
         "saving for Ohioans (Tax Foundation estimate).",
         fact_check="The $3,173 figure is a Tax Foundation estimate cited by the Husted "
         "campaign, not an official score.",
         verification_status="partially verified"),
    dict(candidate_id="BROWN", issue="Economy", subissue="Social Security",
         position_summary="Opposes benefit cuts; discusses solvency fixes at a joint "
         "appearance with Husted.",
         candidate_statement=NV,
         statement_date="unknown",
         context="OCJ reports the two candidates discussed how to fix Social Security on "
         "2026-10-12; the retrieved summary does not quote Brown verbatim.",
         source_urls=ref("ocj19_ohio_us_senate_candidates_discuss_how_to_fix_social_sec"),
         legislative_record="Senate record not re-verified here.",
         position_changed="unknown", change_notes="unknown",
         opponent_criticism="unknown",
         fact_check="not applicable", verification_status="partially verified"),
    dict(candidate_id="BROWN", issue="Democracy", subissue="voting rules and the SAVE Act",
         position_summary="Opposes new federal proof-of-citizenship and photo-ID mandates; "
         "defends early, mail and Election Day voting.",
         candidate_statement="\"We want to make sure that Ohioans' votes are counted, which "
         "means allowing folks to vote early, mail in their ballots and vote on Election "
         "Day.\" (Dispatch survey, 2026-10-18)",
         statement_date="2026-10-18",
         context="Dispatch issue survey; Brown did not address the SAVE America Act directly.",
         source_urls=ref("b4_yahoo_keyissues", "wiki_brown"),
         legislative_record="Former Ohio secretary of state (1983-1991).",
         position_changed="no", change_notes="Consistent with his secretary-of-state record.",
         opponent_criticism="Husted is a staunch SAVE Act supporter and pushed a standalone "
         "photo-ID measure.",
         fact_check="The Dispatch notes Brown \"didn't directly address the legislation\".",
         verification_status="verified"),
    dict(candidate_id="BROWN", issue="Democracy", subissue="money in politics",
         position_summary="Makes record outside spending the explicit villain of his closing "
         "argument.",
         candidate_statement="\"Corporations and billionaires may try to buy this election "
         "for their golden boy, Jon Husted. But there are more of us than there are of "
         "them.\" (Cleveland.com, 2026-10-31)",
         statement_date="2026-10-31",
         context="Closing-argument reporting.",
         source_urls=ref("b4_cle_clash", "ocj30_outside_groups_pour_hundreds_of_millions"),
         legislative_record="Endorsed by End Citizens United (2026-05-12).",
         position_changed="no", change_notes="unknown",
         opponent_criticism="Husted's side argues the spending is independent expenditure, "
         "not campaign money.",
         fact_check="Total race spending exceeds $500 million per Cleveland.com — an "
         "estimate, not an FEC total.",
         verification_status="verified"),
    dict(candidate_id="BROWN", issue="Foreign policy", subissue="war with Iran",
         position_summary="Calls for ending the war with Iran as an inflation and gas-price "
         "measure.",
         candidate_statement="Brown \"rants against Trump's war with Iran\" on the trail "
         "(The Guardian, 2026-11-03) and says ending the war would help lower prices "
         "(WLWT, 2026-11-02).",
         statement_date="2026-11-03",
         context="Result coverage and the WLWT sit-down.",
         source_urls=ref("b4_guardian", "b4_wlwt_result", "ocj06_on_war_with_iran_no_ohio_u"),
         legislative_record="Senate foreign-policy votes not re-verified here.",
         position_changed="unknown", change_notes="unknown",
         opponent_criticism="Brown criticises Husted's votes to continue the war; Husted's "
         "own rationale was not retrieved.",
         fact_check="OCJ (2026-03-05) found no Ohio Senate candidate gave unqualified "
         "support to the war — including Brown.",
         verification_status="verified"),
    dict(candidate_id="BROWN", issue="Other", subissue="surveillance cameras (Flock)",
         position_summary="Opposes corporate-controlled surveillance; wants more facts "
         "before regulating.",
         candidate_statement="Brown called Flock cameras \"another example of corporations "
         "taking control over our communities\" (Dispatch survey, 2026-10-18).",
         statement_date="2026-10-18",
         context="Dispatch issue survey.",
         source_urls=ref("b4_yahoo_keyissues"),
         legislative_record="No record retrieved.",
         position_changed="unknown", change_notes="unknown",
         opponent_criticism="Husted would consider regulating camera placement near "
         "national-security sites.",
         fact_check="not applicable", verification_status="verified"),
    # ---------------- Jon Husted --------------------------------------------
    dict(candidate_id="HUSTED", issue="Economy", subissue="tariffs and trade",
         position_summary="Does not repudiate the tariff regime; frames the answer as market "
         "access, predictability and anti-transshipment enforcement.",
         candidate_statement="\"Ohio relies on the relationship with trading partners like "
         "Canada, but it's got to be fair... They want predictability, but they also don't "
         "want to have China using countries like Canada to import products into Canada and "
         "then moving them into America.\" (reporters, August 2026)",
         statement_date="2026-10-18",
         context="Dispatch issue survey; the campaign says Husted supports \"boosting "
         "access to foreign markets\".",
         source_urls=ref("b4_yahoo_keyissues", "b4_cle_clash"),
         legislative_record="No Senate trade vote retrieved.",
         position_changed="unknown", change_notes="unknown",
         opponent_criticism="Brown says the tariffs raise grocery and equipment costs and "
         "that Husted won't break with Trump on them.",
         fact_check="The campaign's phrasing is reported through spokesperson Amy Natoce; no "
         "Husted quote endorsing the tariffs was retrieved.",
         verification_status="verified"),
    dict(candidate_id="HUSTED", issue="Economy", subissue="manufacturing",
         position_summary="Credits tariff protection and permitting reform with Ohio "
         "manufacturing wins; makes Chillicothe's Kenworth expansion his proof point.",
         candidate_statement="\"Protecting American manufacturing is the America First "
         "agenda.\" (post on X, quoted by Cleveland.com, 2026-10-31)",
         statement_date="2026-10-31",
         context="Closing-argument reporting; the Kenworth claim precedes the 2026-10-28 "
         "Chillicothe rally.",
         source_urls=ref("b4_cle_clash", "ocj14_ohios_intel_plant_has_been_stalled"),
         legislative_record="Permitting-reform bill for energy infrastructure (per the "
         "campaign).",
         position_changed="unknown", change_notes="unknown",
         opponent_criticism="Brown calls the manufacturing message a cover for corporate "
         "tax breaks.",
         fact_check="The 1,000-job Kenworth figure is campaign-stated; not independently "
         "confirmed here.",
         verification_status="partially verified"),
    dict(candidate_id="HUSTED", issue="Economy", subissue="2025 tax law and benefits cliff",
         position_summary="Defends the 2025 tax law and sponsors a bill to smooth the "
         "\"benefits cliff\" for people leaving assistance.",
         candidate_statement=NV,
         statement_date="unknown",
         context="Dispatch survey describes his support and the benefits-cliff bill without "
         "quoting him directly.",
         source_urls=ref("b4_yahoo_keyissues"),
         legislative_record="Backed the 2025 law (no tax on tips/overtime, higher child tax "
         "credit, work requirements); sponsoring the benefits-cliff pilot bill.",
         position_changed="no", change_notes="unknown",
         opponent_criticism="Brown says the law prioritises high earners.",
         fact_check="The $3,173 average saving is a Tax Foundation estimate cited by the "
         "campaign.",
         verification_status="partially verified"),
    dict(candidate_id="HUSTED", issue="Labor", subissue="building trades and public-safety unions",
         position_summary="Carries endorsements from the Operating Engineers, Boilermakers, "
         "ABC of Ohio, the Cleveland Building Trades, the FOP and the Teamsters' rival "
         "building-trades wing — an unusual Republican labour footprint.",
         candidate_statement=NV,
         statement_date="unknown",
         context="Endorsement releases and Wikipedia's endorsement list.",
         source_urls=ref("ref031_boilermakers_org_news_international_brotherhood_of_boil",
                         "ref028_chroniclet_com_news_470613_abc_of_ohio_endorses_jon_hus",
                         "ref030_www_wlwt_com_article_ohio_fop_issues_endorsements_for_r"),
         legislative_record="No labour bill retrieved.",
         position_changed="unknown", change_notes="unknown",
         opponent_criticism="Brown's campaign presents the UAW/Steelworkers endorsements as "
         "the real labour verdict.",
         fact_check="Endorsement claims are sponsor-stated.",
         verification_status="verified"),
    dict(candidate_id="HUSTED", issue="Abortion", subissue="abortion pill and adoption",
         position_summary="Opposes expanded access to the abortion pill; opposes abortion "
         "generally and uses his own adoption story.",
         candidate_statement="At a Senate HELP Committee hearing Husted \"spoke against the "
         "abortion pill\" and \"pointed to his own adoption story, in which he said his "
         "mother could have chosen abortion\" (OCJ, 2026-01-22).",
         statement_date="2026-01-22",
         context="Senate HELP Committee hearing, 'protecting women against dangerous "
         "abortion drugs'.",
         source_urls=ref("ocj35_ohio_republican_us_sen_jon_husted_speaks_against_aborti",
                         "wiki_issue1_2023"),
         legislative_record="Committee participation only; no bill retrieved.",
         position_changed="no", change_notes="Consistent with his state-level record.",
         opponent_criticism="Ohio voters protected abortion in Issue 1 (2023); Brown's side "
         "uses that against him.",
         fact_check="OCJ reports decades of research showing mifepristone is safe and severe "
         "complications rare — a counterweight to the hearing's premise.",
         verification_status="verified"),
    dict(candidate_id="HUSTED", issue="Immigration", subissue="TPS, birthright citizenship, border",
         position_summary="Supports the Trump immigration agenda and says immigration law "
         "\"should be implemented as it was intended\", including TPS and birthright "
         "citizenship.",
         candidate_statement="\"Ohio families deserve a fighter in the U.S. Senate who will "
         "put their safety and well-being first, and stand up for the rule of law – not with "
         "dangerous criminals.\" (spokesperson Amy Natoce, Dispatch survey)",
         statement_date="2026-10-18",
         context="Dispatch issue survey; the candidate statement is issued through his "
         "spokesperson.",
         source_urls=ref("b4_yahoo_keyissues", "ocj05_ohio_senators_governor_respond_to_cal"),
         legislative_record="No immigration bill retrieved.",
         position_changed="no", change_notes="unknown",
         opponent_criticism="Brown calls the crackdown chaotic and defends Springfield's "
         "Haitian community.",
         fact_check="The Dispatch notes ICE has detained people with no criminal record, "
         "contradicting the 'criminals' framing.",
         verification_status="partially verified"),
    dict(candidate_id="HUSTED", issue="Energy", subissue="data centers and large-load power",
         position_summary="Defends data centers as rural jobs and money; sponsors a bill "
         "requiring regulators to consider a large-load cost-allocation blueprint without "
         "mandating it.",
         candidate_statement="No verbatim statement retrieved; the Dispatch survey describes "
         "the bill and the campaign's permitting-reform argument.",
         statement_date="unknown",
         context="Dispatch issue survey; OCJ documents his recruitment of data centers as "
         "lieutenant governor.",
         source_urls=ref("b4_yahoo_keyissues", "ocj31_leaked_memo_about_data_centers_shows",
                         "wiki_husted"),
         legislative_record="Bill requiring state regulators to consider a policy blueprint "
         "making large-load data centers pay for their power.",
         position_changed="partial",
         change_notes="Earlier in 2026 he said data centers need to be more responsible "
         "(OCJ); the bill is the later, weaker instrument.",
         opponent_criticism="Brown calls him the \"face of data centers\" and blames him for "
         "utility bills; the NRSC memo calls data centers \"the anchor hanging around "
         "Husted's neck\".",
         fact_check="The Plain Dealer nickname \"Face of Data Centers\" is reported by "
         "Wikipedia citing the Plain Dealer.",
         verification_status="verified"),
    dict(candidate_id="HUSTED", issue="Healthcare", subissue="ACA subsidies",
         position_summary="Wants a two-year extension of enhanced ACA tax credits paired "
         "with a $5 minimum monthly payment to deter fraud.",
         candidate_statement="\"Husted was not in Congress when Sherrod Brown and Democrats "
         "created the broken ACA system... but he has worked to be part of a thoughtful "
         "solution\" (spokesperson Amy Natoce, Dispatch survey).",
         statement_date="2026-10-18",
         context="Dispatch issue survey.",
         source_urls=ref("b4_yahoo_keyissues", "ocj10_ohio_u_s_sen_jon_husted_wants_to_fre"),
         legislative_record="Introduced the two-year extension bill; backed the OTC-drug "
         "streamlining law.",
         position_changed="partial",
         change_notes="In December 2025 he wanted to \"freeze\" the subsidies (OCJ); by "
         "October 2026 he sponsored a two-year extension.",
         opponent_criticism="Brown says the conditions would raise costs for poor enrollees.",
         fact_check="The $5 minimum payment is described by the campaign as an anti-fraud "
         "measure; no independent analysis retrieved.",
         verification_status="verified"),
    dict(candidate_id="HUSTED", issue="Healthcare", subissue="rural hospitals",
         position_summary="Claims the $50 billion rural-hospital fund as a win and calls it "
         "the most consequential rural-health step in years.",
         candidate_statement="Spokesperson Natoce called the rural hospital funding \"one of "
         "the most consequential steps that Congress has taken to support rural health care "
         "in years\" (Dispatch survey).",
         statement_date="2026-10-18",
         context="Dispatch issue survey.",
         source_urls=ref("b4_yahoo_keyissues"),
         legislative_record="Supported the 2025 law's $50 billion rural hospital fund; Ohio "
         "received more than $200 million per DeWine's office.",
         position_changed="unknown", change_notes="unknown",
         opponent_criticism="Brown says the money does not offset the Medicaid cuts.",
         fact_check="The $200 million Ohio figure is attributed to DeWine's office.",
         verification_status="partially verified"),
    dict(candidate_id="HUSTED", issue="Democracy", subissue="SAVE America Act and photo ID",
         position_summary="Staunch supporter of the SAVE America Act and of a standalone "
         "photo-ID measure; as a former secretary of state he owns the issue.",
         candidate_statement="Husted recorded Senate floor remarks on requiring photo "
         "identification to vote on 2026-07-27 (Commons audio file description).",
         statement_date="2026-07-27",
         context="Senate floor; the Wikipedia infobox links the recording.",
         source_urls=ref("b4_yahoo_keyissues", "wiki_husted", "husted_sworn_in_2025"),
         legislative_record="Pushed the Senate to consider a standalone photo-ID measure.",
         position_changed="no", change_notes="Consistent with his 2011-2019 secretary-of-state "
         "tenure.",
         opponent_criticism="Brown says the push sows distrust and would suppress voting.",
         fact_check="The Dispatch notes the Senate remains deadlocked on the SAVE Act.",
         verification_status="verified"),
    dict(candidate_id="HUSTED", issue="Education", subissue="school choice and charter schools",
         position_summary="Long record of expanding school choice, charter schools and "
         "religious education access in Ohio.",
         candidate_statement=NV,
         statement_date="unknown",
         context="Wikipedia biography and its cited NBC4 piece.",
         source_urls=ref("wiki_husted"),
         legislative_record="State legislative record: income-tax cut and school-choice "
         "expansion as Speaker (2005-2009).",
         position_changed="no", change_notes="unknown",
         opponent_criticism="No 2026 Brown attack on school choice retrieved.",
         fact_check="State-record claims come from a Wikipedia citation of The Daily "
         "Advocate (2007) and NBC4 (2026).",
         verification_status="partially verified"),
    dict(candidate_id="HUSTED", issue="Other", subissue="AI and automation",
         position_summary="Favours progressively replacing human jobs with AI and wants to "
         "attract the data-center build-out that underpins it.",
         candidate_statement="Wikipedia, citing the Plain Dealer: \"During the 2026 campaign, "
         "he favored progressively replacing human jobs with AI.\"",
         statement_date="2026-10-01",
         context="Campaign-period position recorded in the biography.",
         source_urls=ref("wiki_husted", "ref157_netchoice_org_netchoice_echelon_insights"),
         legislative_record="No AI bill retrieved.",
         position_changed="unknown", change_notes="unknown",
         opponent_criticism="Brown's data-center attack is the closest surrogate for an AI "
         "critique; no direct AI attack retrieved.",
         fact_check="The claim rests on a single Wikipedia sentence citing the Plain Dealer; "
         "the Plain Dealer article itself was not retrieved, so the exact wording is "
         "unconfirmed.",
         verification_status="partially verified"),
    dict(candidate_id="HUSTED", issue="Foreign policy", subissue="Iran war and Russia sanctions",
         position_summary="Voted to continue the Iran war (as characterised by Brown); "
         "supported Russia sanctions in 2025 unless Moscow pursued a lasting peace.",
         candidate_statement=NV,
         statement_date="unknown",
         context="Wikipedia biography (Russia sanctions) and Cleveland.com (Iran votes).",
         source_urls=ref("wiki_husted", "b4_cle_clash"),
         legislative_record="2025 Russia sanctions support; Iran war votes.",
         position_changed="unknown", change_notes="unknown",
         opponent_criticism="Brown: \"criticizes Husted's votes to continue the war in Iran\".",
         fact_check="OCJ found no Ohio Senate candidate gave unqualified support to the war; "
         "Husted's precise position was not retrieved.",
         verification_status="partially verified"),
    dict(candidate_id="HUSTED", issue="Other", subissue="the appointment and incumbency question",
         position_summary="Runs as the appointed incumbent, dating his tenure to the "
         "2025-01-17 announcement and the 2025-01-21 oath; his opponents call the seat "
         "\"unelected\".",
         candidate_statement="\"We have worked to make Ohio great again, and I look forward "
         "to working with President Trump and JD Vance to make America great again.\" "
         "(appointment remarks, 2025-01-17, OCJ)",
         statement_date="2025-01-17",
         context="DeWine's appointment announcement at the Ohio Statehouse.",
         source_urls=ref("ocj25_ohio_lt_gov_jon_husted_to_replace_jd_vance_in_u_s_senat",
                         "husted_sworn_in_2025", "ocj39_ohio_incumbent_us_sen_jon_husteds_"),
         legislative_record="Appointed by Gov. Mike DeWine on 2025-01-17; sworn in 2025-01-21.",
         position_changed="no", change_notes="unknown",
         opponent_criticism="OCJ commentary notes the Husted campaign trying to cast Brown as "
         "the incumbent; Brown calls him a special interest insider.",
         fact_check="The brief's dates (appointed 2025-01-10, sworn in 2025-01-14) are wrong: "
         "2025-01-10 is Vance's resignation date; the appointment was announced 2025-01-17 "
         "and the oath administered 2025-01-21.",
         verification_status="verified"),
]


def main():
    rows = []
    for i, p in enumerate(POSITIONS, 1):
        p = dict(p)
        p["position_id"] = f"POS-{i:03d}"
        rows.append(p)
    write_csv("01_candidates/policy_positions.csv", PP_FIELDS, rows)
    n_b = sum(1 for r in rows if r["candidate_id"] == "BROWN")
    n_h = sum(1 for r in rows if r["candidate_id"] == "HUSTED")
    print("BROWN", n_b, "HUSTED", n_h)


if __name__ == "__main__":
    main()
