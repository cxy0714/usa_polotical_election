"""Build advertisements, social_media, media_coverage, campaign_finance,
election_results, county_results and polling."""
import csv
import sys

sys.path.insert(0, "_staging")
from b_common import ref, write_csv  # noqa: E402

U = "unknown"

# --------------------------------------------------------------- adverts ---
AD_FIELDS = ["ad_id", "candidate_id", "sponsor", "sponsor_type", "release_date", "title",
             "platform", "length_seconds", "issue_or_message", "main_visual_elements",
             "narration_soundtrack", "candidate_appearance", "main_claims", "video_url",
             "transcript_url", "fact_check", "media_coverage", "source_urls",
             "verification_status", "notes"]

ADS = [
    dict(candidate_id="BROWN", sponsor="Sherrod Brown campaign", sponsor_type="candidate_campaign",
         release_date=U, title="Data-center ad (one of three, quoted spot)",
         platform="television and digital (per OCJ)", length_seconds=U,
         issue_or_message="Husted recruited data centers that raise Ohioans' electricity bills",
         main_visual_elements=U, narration_soundtrack=U, candidate_appearance=U,
         main_claims="\"(Jon) Husted is a chief reason Ohio has so many of those centers. He "
         "force-fed the massive energy-sucking facilities.\"",
         video_url=U, transcript_url=U,
         fact_check="No independent check of the ad's numbers was retrieved; Brown's \"200 in "
         "Ohio\" figure is his own count.",
         media_coverage="Ohio Capital Journal, 2026-08-21",
         source_urls=ref("ocj31_leaked_memo_about_data_centers_shows_gop_worried_about"),
         verification_status="verified",
         notes="OCJ reports three Brown spots all dealing with data centers; only this one is "
               "quoted, so the other two appear as separate rows without a quoted script."),
    dict(candidate_id="BROWN", sponsor="Sherrod Brown campaign", sponsor_type="candidate_campaign",
         release_date=U, title="Data-center ad (second of three)", platform="television and digital",
         length_seconds=U, issue_or_message="data centers and utility costs",
         main_visual_elements=U, narration_soundtrack=U, candidate_appearance=U,
         main_claims="Not retrieved — OCJ states only that three Brown spots dealt with data "
         "centers, quoting one.",
         video_url=U, transcript_url=U, fact_check="not applicable",
         media_coverage="Ohio Capital Journal, 2026-08-21",
         source_urls=ref("ocj31_leaked_memo_about_data_centers_shows_gop_worried_about"),
         verification_status="partially verified",
         notes="Exists per OCJ; creative and claims not retrieved."),
    dict(candidate_id="BROWN", sponsor="Sherrod Brown campaign", sponsor_type="candidate_campaign",
         release_date=U, title="Data-center ad (third of three)", platform="television and digital",
         length_seconds=U, issue_or_message="data centers and utility costs",
         main_visual_elements=U, narration_soundtrack=U, candidate_appearance=U,
         main_claims="Not retrieved — see the quoted spot for the series' argument.",
         video_url=U, transcript_url=U, fact_check="not applicable",
         media_coverage="Ohio Capital Journal, 2026-08-21",
         source_urls=ref("ocj31_leaked_memo_about_data_centers_shows_gop_worried_about"),
         verification_status="partially verified",
         notes="Exists per OCJ; creative and claims not retrieved."),
    dict(candidate_id="HUSTED", sponsor="National Republican Senatorial Committee",
         sponsor_type="outside_pac", release_date="2026-08-05",
         title="Soposki crash ad", platform="television", length_seconds="30",
         issue_or_message="Immigration and a fatal Ohio crash",
         main_visual_elements="Footage of the April 2026 multi-vehicle crash on Interstate 71 in "
         "Delaware County that killed three people (per OCJ)",
         narration_soundtrack=U, candidate_appearance=U,
         main_claims="\"Sherrod Brown opened our borders to dangerous illegals. The consequences "
         "were deadly... Because of him, Ohioans paid the price.\"",
         video_url=U, transcript_url=U,
         fact_check="OCJ reports the family of the victims asked the NRSC to take the ad down, "
         "saying \"our grief is not raw material for a campaign\".",
         media_coverage="Ohio Capital Journal, 2026-08-28",
         source_urls=ref("ocj40_family_asks_national_republican_senatorial_committee_to"),
         verification_status="verified",
         notes="Release date approximated as early August: OCJ (2026-08-28) says the NRSC "
               "\"started airing an ad earlier this month\". Recorded as an approximation in "
               "notes rather than as a precise date."),
    dict(candidate_id="HUSTED", sponsor="Senate Leadership Fund", sponsor_type="outside_pac",
         release_date=U, title="Transgender-surgery attack ads (series featuring Aldaco)",
         platform=U, length_seconds=U,
         issue_or_message="Transgender surgery for minors",
         main_visual_elements=U, narration_soundtrack=U, candidate_appearance="none — testimonial ad",
         main_claims="\"Sherrod Brown supports sex changes for minors, irreversible surgery on "
         "kids like me\" (on-camera testimonial by Aldaco).",
         video_url=U, transcript_url=U,
         fact_check="OCJ found Aldaco is not an Ohioan, was 19 at the time of surgery and was "
         "treated in Texas — the ad's \"kids like me\" premise does not hold.",
         media_coverage="Ohio Capital Journal, 2026-10-06",
         source_urls=ref("ocj09_woman_accusing_sherrod_brown_of_forcing_transgender_sur"),
         verification_status="verified",
         notes="SLF is described by OCJ as one of the main groups supporting Republicans."),
    dict(candidate_id="HUSTED", sponsor="Americans for Prosperity Action",
         sponsor_type="outside_pac", release_date="2026-09-10", title="Common Sense",
         platform="digital and streaming", length_seconds=U,
         issue_or_message="Husted's record versus Brown's party",
         main_visual_elements=U, narration_soundtrack=U, candidate_appearance=U,
         main_claims="Husted cut red tape and delivered results; Brown will not stand up to "
         "\"the socialist agenda taking root in his own party\".",
         video_url=U, transcript_url=U, fact_check="not applicable",
         media_coverage="AFP Action release, 2026-09-10",
         source_urls=ref("ref121_afpaction_com_new_afp_action_ads_put_ohios_choice_in_fo"),
         verification_status="verified",
         notes="Part of a $1.4 million digital/streaming buy inside a $9 million Ohio programme."),
    dict(candidate_id="HUSTED", sponsor="Americans for Prosperity Action",
         sponsor_type="outside_pac", release_date="2026-09-10", title="Taking Root",
         platform="digital and streaming", length_seconds=U,
         issue_or_message="Socialism and the cost of living",
         main_visual_elements=U, narration_soundtrack=U, candidate_appearance=U,
         main_claims="\"Socialism is taking root in Sherrod Brown's party... Ohioans are paying "
         "more for groceries, housing, and energy.\"",
         video_url=U, transcript_url=U, fact_check="not applicable",
         media_coverage="AFP Action release, 2026-09-10",
         source_urls=ref("ref121_afpaction_com_new_afp_action_ads_put_ohios_choice_in_fo"),
         verification_status="verified",
         notes="Second spot in the same buy."),
    dict(candidate_id="HUSTED", sponsor="unknown (posted by Donald Trump)",
         sponsor_type="unknown", release_date="2026-10-29",
         title="VOTE FOR JON HUSTED!!!", platform="social video (vertical)",
         length_seconds="27.7",
         issue_or_message="get-out-the-vote appeal",
         main_visual_elements="unknown — frames not inspected",
         narration_soundtrack=U, candidate_appearance=U,
         main_claims="Only the title is documented: an exhortation to vote for Husted.",
         video_url="https://upload.wikimedia.org/wikipedia/commons/e/ec/"
                   "VOTE_FOR_JON_HUSTED%21%21%21.webm",
         transcript_url=U, fact_check="not applicable",
         media_coverage="Wikimedia Commons file record (public domain)",
         source_urls=ref("video_vote_for_husted_2026"),
         verification_status="partially verified",
         notes="27.7-second 1080x1920 public-domain video dated 2026-10-29 and credited on "
               "Commons to Donald Trump; sponsor and platform are inferred from the credit and "
               "the aspect ratio, which is why sponsor_type is unknown."),
]

# ----------------------------------------------------------------- social --
SOC_FIELDS = ["post_id", "candidate_id", "platform", "account_handle", "post_date",
              "post_type", "content_summary", "media_included", "engagement_notes", "url",
              "verification_status", "notes"]

SOCIAL = [
    dict(candidate_id="HUSTED", platform="X", account_handle="Jon Husted (campaign account)",
         post_date="2026-10-28", post_type="text",
         content_summary="\"Protecting American manufacturing is the America First agenda.\"",
         media_included="unknown", engagement_notes="unknown",
         url=U, verification_status="partially verified",
         notes="Quoted by Cleveland.com; the post itself was not retrieved (x.com blocks the "
               "archiver), so the handle is described rather than given."),
    dict(candidate_id="HUSTED", platform="X", account_handle="unknown",
         post_date="2025-07-15", post_type="photo post, later deleted",
         content_summary="A photograph of Husted laughing with lobbyists, taken down after "
         " criticism.", media_included="photograph", engagement_notes="unknown",
         url=U, verification_status="verified",
         notes="Documented in OCJ; the post no longer exists, so no URL can be given."),
    dict(candidate_id="HUSTED", platform="X", account_handle="Office of Senator Jon Husted",
         post_date="2025-01-16", post_type="text with photograph",
         content_summary="\"With @anduriltech's move to Ohio, more than 4,000 jobs will be "
         "created at the facility alone, with an expected total of more than 8,500 including "
         "indirect jobs.\"", media_included="photograph",
         engagement_notes="unknown", url=U, verification_status="partially verified",
         notes="Text quoted in the Commons file description for the accompanying image; the "
               "post UUID is not recoverable."),
    dict(candidate_id="HUSTED", platform="Facebook", account_handle="Office of Senator Jon Husted",
         post_date="2025-01-28", post_type="photo post",
         content_summary="Meeting with Kelly Loeffler, then nominee for a cabinet-level post.",
         media_included="photograph", engagement_notes="unknown", url=U,
         verification_status="partially verified",
         notes="Commons file description states the image came from the office's Facebook post; "
               "the post URL is not recorded there."),
    dict(candidate_id="HUSTED", platform="X", account_handle="Donald Trump",
         post_date="2026-10-29", post_type="video",
         content_summary="27.7-second vertical video titled \"VOTE FOR JON HUSTED!!!\".",
         media_included="video", engagement_notes="unknown",
         url="https://upload.wikimedia.org/wikipedia/commons/e/ec/"
             "VOTE_FOR_JON_HUSTED%21%21%21.webm",
         verification_status="partially verified",
         notes="The Commons record credits the work to Donald Trump and dates it 2026-10-29; "
               "the platform is inferred from the vertical format. Recorded also in "
               "advertisements.csv."),
    dict(candidate_id="BROWN", platform="campaign website", account_handle="Friends of Sherrod Brown",
         post_date=U, post_type="logo/branding asset",
         content_summary="Official 2026 campaign logo, released as public domain.",
         media_included="graphic", engagement_notes="not applicable", url=U,
         verification_status="partially verified",
         notes="Included as a social/branding artefact because no Brown social post was "
               "retrievable; the logo file itself is catalogued in image_archive.csv."),
]

# --------------------------------------------------------- media coverage --
MC_FIELDS = ["coverage_id", "candidate_id", "event_id", "publication_date", "outlet",
             "author", "title", "url", "source_tier", "coverage_type", "key_framing",
             "notable_quotes", "framing_of_candidate", "mentions_opponent",
             "reliability_notes"]

COVERAGE = [
    ("BROWN", "EV-016", "ocj25_ohio_lt_gov_jon_husted_to_replace_jd_vance_in_u_s_senat",
     "news_report", "DeWine's appointment of Husted, framed as a governor's legacy choice.",
     "DeWine: \"I wanted someone who knew Ohio.\"", "neutral report", "yes", ""),
    ("BROWN", "EV-002", "ref063_www_newsandsentinel", "news_report",
     "Launch coverage in a southeast Ohio daily.", "unknown", "neutral", "yes", ""),
    ("HUSTED", "EV-018", "ref014_web_archive_org_web_20250410091543_https_apnews_com_art",
     "news_report", "AP launch story read through a Wayback capture.",
     "Trump endorsement the same day", "neutral wire copy", "yes",
     "Original AP URL returned 403; this is an Internet Archive capture."),
    ("HUSTED", "EV-030", "ref125_www_uschamber_com_improving_government_u_s_chamber_endo",
     "news_report", "Chamber endorsement framed as business consensus.", "unknown",
     "favourable", "no", "Advocacy source, not journalism."),
    ("BROWN", "EV-031", "b4_trib_mahoning", "news_report",
     "Husted's Mahoning Valley rally, with DeWine present.", "Husted's \"50 years\" attack",
     "neutral report", "yes", ""),
    ("HUSTED", "EV-033", "b4_cle_clash", "news_report",
     "Closing-argument piece built around the two candidates' final-week stops.",
     "Brown: \"He's a special interest guy in Washington\"; Husted: \"he's been in office for "
     "over 50 years\"", "comparative", "yes", ""),
    ("BROWN", "EV-013", "ref129_www_daytondailynews_com_local_acton_brown_make_final_e",
     "news_report", "Rally coverage centred on surrogates (Acton, John Legend).",
     "\"We, together, are going to make it all cost less\" (Acton)", "favourable", "yes", ""),
    ("BROWN", U, "ocj31_leaked_memo_about_data_centers_shows_gop_worried_about",
     "analysis", "Data centers as the race's sleeper issue, anchored in a leaked NRSC memo.",
     "\"the anchor hanging around Husted's neck\"", "favourable to Brown's framing", "yes", ""),
    ("HUSTED", U, "ocj40_family_asks_national_republican_senatorial_committee_to",
     "news_report", "The NRSC crash ad and the family's objection.", "see advertisements.csv",
     "critical of the NRSC ad", "yes", ""),
    ("BROWN", U, "ocj09_woman_accusing_sherrod_brown_of_forcing_transgender_sur",
     "fact_check", "Fact-check of the SLF testimonial ad.", "see advertisements.csv",
     "defends Brown", "yes", ""),
    ("HUSTED", U, "ocj35_ohio_republican_us_sen_jon_husted_speaks_against_aborti",
     "news_report", "Husted's abortion-pill hearing statement.", "adoption story",
     "critical", "no", ""),
    ("HUSTED", U, "ocj10_ohio_u_s_sen_jon_husted_wants_to_fre",
     "news_report", "Husted's December 2025 call to freeze ACA subsidies.",
     "\"freeze\"", "critical", "no", ""),
    ("HUSTED", U, "ocj21_husted_political_committee_got_nearly_500k_from_a_bank",
     "news_report", "Bank money into a Husted political committee.", "unknown",
     "critical", "no", ""),
    ("HUSTED", U, "ocj37_ohio_republican_u_s_sen_jon_husted_took_gifts_from_jobs",
     "news_report", "Gifts from JobsOhio while lieutenant governor.", "unknown", "critical",
     "no", ""),
    ("HUSTED", U, "ocj16_ohio_republican_u_s_sen_jon_husted_testifies_in_firsten",
     "news_report", "FirstEnergy trial testimony.", "unknown", "critical", "no", ""),
    ("BROWN", U, "ocj36_former_ohio_u_s_sen_sherrod_brown_launch",
     "news_report", "The Dignity of Work Institute as message-building.", "see speech_archive",
     "favourable", "no", ""),
    ("BROWN", U, "b4_yahoo_keyissues", "analysis",
     "Columbus Dispatch issue survey reproduced by Yahoo News.",
     "\"Ohio workers are more productive than ever, but no matter how hard they work, their pay "
     "doesn't keep up\"", "comparative", "yes",
     "Original is a Columbus Dispatch story; the retrieved copy is Yahoo's syndication."),
    ("BROWN", U, "b4_cle_return", "analysis",
     "What Brown's return means for Ohio.", "the farmer/tractor quote", "favourable", "no", ""),
    ("HUSTED", U, "b4_cle_rebuke", "analysis",
     "Analysis reading the result as a rebuke to Husted's corporate ties.", "unknown",
     "critical of Husted", "yes", ""),
    ("BROWN", U, "b4_herald_ap", "news_report",
     "AP result story carried by the Boston Herald.", "unknown", "neutral wire copy", "yes",
     "AP original returned 403; this is the syndicated copy."),
    ("HUSTED", U, "b4_wlwt_result", "news_report",
     "Cincinnati result coverage with a Brown sit-down.", "Brown on guns, tariffs, Iran",
     "neutral", "yes", ""),
    ("BROWN", U, "b4_newsweek_result", "news_report",
     "National magazine result story.", "unknown", "neutral", "yes", ""),
    ("HUSTED", U, "ocj30_outside_groups_pour_hundreds_of_millions", "analysis",
     "Outside spending: AdImpact has Ohio the most expensive Senate race at $325m+.",
     "unknown", "neutral", "yes", ""),
    ("HUSTED", U, "ref138_www_rawstory_com_kasich_husted", "news_report",
     "Kasich withholds his endorsement and doubts Husted holds the seat.", "unknown",
     "critical of Husted", "yes", ""),
    ("BROWN", U, "ocj12_u_s_senate_balance_of_power_falls_to_ohio_several_key_s", "analysis",
     "Ohio as one of a handful of states deciding Senate control.", "unknown", "neutral", "yes",
     ""),
]

# --------------------------------------------------------------- finance ---
FIN_FIELDS = ["finance_id", "candidate_id", "period", "report_type", "reporting_deadline",
              "receipts", "individual_contributions", "pac_contributions", "disbursements",
              "cash_on_hand", "debts_owed", "source_urls", "verification_status", "notes"]

FINANCE = [
    ("BROWN", "2026-03-31", "quarterly (Q1 2026)", "2026-04-15", 24471408, 7956946, 16514461,
     "Article's primary-fundraising table, 'as of April 18, 2026', cited to the FEC."),
    ("HUSTED", "2026-03-31", "quarterly (Q1 2026)", "2026-04-15", 10257823, 2017868, 8239954,
     "Article's 'as of April 18, 2026' table, cited to the FEC."),
    ("BROWN", "2026-09-30", "quarterly (Q3 2026)", "2026-10-15", 68409200, 63956397, 4452803,
     "Article's 'as of October 14, 2026' table: cumulative receipts, not a single quarter."),
    ("HUSTED", "2026-09-30", "quarterly (Q3 2026)", "2026-10-15", 19894786, 15655689, 4239097,
     "Article's 'as of October 14, 2026' table."),
    ("REDPATH", "2026-09-30", "quarterly (Q3 2026)", "2026-10-15", 55256, 47000, 8255,
     "Minor-candidate line in the same table."),
    ("LEVY", "2026-09-30", "quarterly (Q3 2026)", "2026-10-15", 132712, 107925, 26916,
     "Minor-candidate line in the same table."),
    ("KINCAID", "2026-03-31", "quarterly (Q1 2026)", "2026-04-15", 41804, 42980, 0,
     "Democratic primary rival; line in the primary-fundraising table."),
    ("ODE", "2026-03-31", "quarterly (Q1 2026)", "2026-04-15", 5001938, 4970194, 31744,
     "Withdrew in November 2025; the article lists him in italics as a withdrawn candidate."),
    ("VOLPE", "2026-03-31", "quarterly (Q1 2026)", "2026-04-15", 4337, 4168, 168,
     "Withdrawn Democratic candidate, listed in italics."),
]

# --------------------------------------------------------------- results ---
RES_FIELDS = ["race_id", "race_name", "election_date", "candidate", "party", "votes",
              "percentage", "winner", "source_urls", "verification_status", "notes"]

RESULTS = [
    ("OH-SEN-2026-SPECIAL", "2026 United States Senate special election in Ohio", "2026-11-03",
     "Sherrod Brown", "Democratic", 2302669, "50.01", "yes",
     "Article's election box; the Calfee newsletter also rounds him to 50.01."),
    ("OH-SEN-2026-SPECIAL", "2026 United States Senate special election in Ohio", "2026-11-03",
     "Jon Husted", "Republican", 2080064, "45.17", "no",
     "conflicting sources: the Calfee newsletter the article cites prints 45.15; computed from "
     "the vote counts, 2,080,064 / 4,604,860 = 45.171%, so 45.17 is retained."),
    ("OH-SEN-2026-SPECIAL", "2026 United States Senate special election in Ohio", "2026-11-03",
     "Bill Redpath", "Libertarian", 128341, "2.79", "no",
     "Calfee also prints 2.79."),
    ("OH-SEN-2026-SPECIAL", "2026 United States Senate special election in Ohio", "2026-11-03",
     "Greg Levy", "Party for Socialism and Liberation", 93786, "2.04", "no",
     "conflicting sources: Calfee prints 2.05; Wikipedia's box labels him an independent while "
     "ABC 6 and Cincinnati Magazine name the Party for Socialism and Liberation."),
    ("OH-SEN-2026-PRIMARY-D", "Ohio Democratic primary for U.S. Senate", "2026-05-05",
     "Sherrod Brown", "Democratic", 712106, "89.40", "yes",
     "Official canvass figures reproduced in the article."),
    ("OH-SEN-2026-PRIMARY-D", "Ohio Democratic primary for U.S. Senate", "2026-05-05",
     "Ron Kincaid", "Democratic", 84405, "10.60", "no",
     "84,405 / 796,511 = 10.597%, printed as 10.60."),
    ("OH-SEN-2026-PRIMARY-R", "Ohio Republican primary for U.S. Senate", "2026-05-05",
     "Jon Husted", "Republican", 736413, "100.00", "yes",
     "Unopposed; total equals his vote."),
]

CQ_FIELDS = ["county_id", "county", "brown_votes", "husted_votes", "other_votes", "brown_pct",
             "husted_pct", "total_votes", "source_urls", "verification_status"]

# ----------------------------------------------------------------- polls ---
POLL_FIELDS = ["poll_id", "pollster", "sponsor", "field_start", "field_end", "population",
               "sample_size", "margin_of_error", "brown_pct", "husted_pct", "other_pct",
               "undecided_pct", "leader", "margin", "source_urls", "verification_status",
               "notes"]

# (pollster, sponsor, start, end, pop, n, moe, busted->(brown, husted, other, undec),
#  source key, note)
POLLS = [
    ("Trafalgar Group", "Trafalgar Group (R-leaning)", "2026-10-31", "2026-11-01", "likely voters",
     1092, "2.9", (47, 45, 4, 4), "ref144_www_thetrafalgargroup_org_wp_content_uploads_2026_11_OH",
     "Printed as 45 (Husted) / 47 (Brown) / 4 other / 4 undecided."),
    ("HarrisX", "HarrisX", "2026-10-30", "2026-11-01", "likely voters", 496, "4.4",
     (47, 45, 4, 5), "ref145_www_harrisx_com_posts_final_harrisx_2026_midterm_poll", ""),
    ("Research Co.", "Research Co.", "2026-10-30", "2026-11-01", "likely voters", 450, "4.6",
     (45, 44, 2, 9), "ref146_researchco_ca_2026_11_01_midterms_2026_one", ""),
    ("AtlasIntel", "AtlasIntel", "2026-10-28", "2026-11-01", "likely voters", 1801, "2.0",
     (51, 44, 4, 1), "ref147_atlasintel_org_poll_usa_ohio_atlaspollstergraph_poll_20",
     "Other includes 3% 'other' and 1% 'would not vote'."),
    ("New York Times/Siena", "New York Times", "2026-10-26", "2026-11-01", "likely voters",
     717, "4.4", (49, 44, 0, 7), "wiki_ohio",
     "Tabulated in the article; the Times/Siena topline document itself was not retrieved."),
    ("Rasmussen Reports", "Rasmussen Reports", "2026-10-27", "2026-10-31", "likely voters",
     1119, "3.0", (46, 46, 5, 3), "b4_rasmussen_nov1",
     "Tied at 46; Redpath 3%, Levy 2%."),
    ("ActiVote", "ActiVote", "2026-10-18", "2026-10-31", "likely voters", 400, "4.9",
     (50, 50, U, U), "wiki_ohio",
     "Tied at 50 with no other/undecided columns printed."),
    ("InsiderAdvantage", "InsiderAdvantage", "2026-10-29", "2026-10-30", "likely voters",
     1200, "2.8", (49, 47, 3, 1), "ref152_insideradvantage_com_final_insideradvantage_ohio_survey",
     ""),
    ("YouGov", "YouGov", "2026-10-26", "2026-10-29", "likely voters", 2090, "2.8",
     (50, 48, 2, 1), "ref153_d3nkl3psvxxpe9_cloudfront_net_documents_ttw_oh_20261026", ""),
    ("Suffolk University", "Suffolk University", "2026-10-21", "2026-10-26", "likely voters",
     500, "4.4", (47, 44, 5, 4), "ref154_www_suffolk_edu_media_suffolk_documents_academics_resea",
     ""),
    ("Concord Public Opinion Partners", "Concord", "2026-10-22", "2026-10-24", "likely voters",
     496, "4.5", (46, 42, 8, 4), "ref177_concordpublicopinionpartners_org_polls_ohio_ge_2026",
     ""),
    ("RedBox", "RedBox", "2026-10-20", "2026-10-23", "likely voters", 2998, "4.6",
     (47, 44, 4, 4), "wiki_ohio", "Tabulated in the article; release not retrieved."),
    ("Echelon Insights", "NetChoice", "2026-10-16", "2026-10-23", "likely voters", 508, "5.2",
     (47, 47, 3, 3), "ref157_netchoice_org_netchoice_echelon_insights_poll_voters_ra",
     "Industry-sponsored poll."),
    ("InsiderAdvantage", "InsiderAdvantage", "2026-10-21", "2026-10-22", "likely voters",
     1200, "2.8", (47, 44, 3, 6), "ref169_insideradvantage_com_insideradvantage_ohio_senate_race_",
     ""),
    ("Fox News", "Fox News", "2026-10-15", "2026-10-19", "registered voters", 2005, "2.0",
     (53, 46, U, 2), "ref160_static_foxnews_com_foxnews_com_content_uploads_2026_10_",
     "Registered-voter sample; the only late poll in the table with Brown above 50."),
    ("ActiVote", "ActiVote", "2026-09-26", "2026-10-18", "likely voters", 400, "4.9",
     (50, 50, U, U), "wiki_ohio", "Tied at 50."),
    ("Rasmussen Reports", "Rasmussen Reports", "2026-10-12", "2026-10-14", "likely voters",
     901, "3.0", (47, 49, 2, 2), "ref150_www_rasmussenreports_com_public_content_politics_electi",
     "Husted led by two in mid-October."),
    ("Bowling Green State University/YouGov", "BGSU", "2026-09-29", "2026-10-09",
     "likely voters", 1000, "4.0", (48, 42, 10, U), "ref191_www_bgsu_edu_arts_and_sciences_democracy",
     "Other/undecided printed as a single 10% column."),
    ("SSRS", "CNN", "2026-09-29", "2026-10-05", "likely voters", 760, "4.5",
     (49, 43, 7, 1), "ref166_www_documentcloud_org_documents_28729016_cnn_ohio_poll_", ""),
    ("Marist Poll", "Marist Poll", "2026-09-24", "2026-09-27", "registered voters", 1298, "3.8",
     (51, 43, 1, 4), "ref171_maristpoll_marist_edu_polls_midterm_elections_in_ohio_s", ""),
    ("Suffolk University", "Suffolk University", "2026-09-23", "2026-09-27", "likely voters",
     500, "4.4", (47, 44, 3, 6), "ref172_www_suffolk_edu_media_suffolk_documents_academics_resea",
     ""),
    ("Rasmussen Reports", "Rasmussen Reports", "2026-09-22", "2026-09-23", "likely voters",
     1115, "3.0", (46, 43, 5, 7), "ref150_www_rasmussenreports_com_public_content_politics_electi",
     "Redpath 3%, Levy 2%."),
    ("Trafalgar Group", "Trafalgar Group (R-leaning)", "2026-09-14", "2026-09-16",
     "likely voters", 1085, "2.9", (45, 42, 6, 6),
     "ref174_www_thetrafalgargroup_org_wp_content_uploads_2026_09_OH", ""),
    ("Bowling Green State University/YouGov", "BGSU", "2026-09-01", "2026-09-10",
     "likely voters", 1000, "4.0", (48, 45, 7, U),
     "ref191_www_bgsu_edu_arts_and_sciences_democracy", ""),
    ("Concord Public Opinion Partners", "Concord", "2026-08-29", "2026-08-31", "likely voters",
     504, "4.4", (50, 40, 4, 7), "ref177_concordpublicopinionpartners_org_polls_ohio_ge_2026",
     ""),
    ("Tulchin Research", "Tulchin Research (D-leaning)", "2026-07-29", "2026-08-04",
     "likely voters", 600, "4.0", (47, 43, 4, 6),
     "ref180_www_documentcloud_org_documents_28549388_oh_sen_gov_ag_", ""),
]


def main():
    rows = []
    for i, a in enumerate(ADS, 1):
        r = dict(a)
        r["ad_id"] = f"AD-{i:03d}"
        rows.append(r)
    write_csv("05_campaign_media/advertisements.csv", AD_FIELDS, rows)

    rows = []
    for i, s in enumerate(SOCIAL, 1):
        r = dict(s)
        r["post_id"] = f"SOC-{i:03d}"
        rows.append(r)
    write_csv("05_campaign_media/social_media.csv", SOC_FIELDS, rows)

    import json
    titles = json.load(open("_staging/titles.json", encoding="utf-8"))
    from b_common import SRC, _resolve

    srcrows = {}
    for r in csv.DictReader(open("09_sources/sources.csv", encoding="utf-8")):
        srcrows[r["source_id"]] = r

    rows = []
    for i, (cid, ev, key, ctype, framing, quotes, foca, opp, rel) in enumerate(COVERAGE, 1):
        k = _resolve(key)
        srec = SRC[k]
        tinfo = titles.get(k, {})
        meta = srcrows.get(srec[0], {})
        title = tinfo.get("title") or meta.get("title") or "unknown"
        if " | " in title and len(title) > 60:
            title = title.split(" | ")[0]
        pubdate = (tinfo.get("pubdate") or meta.get("publication_date") or "")[:10]
        rows.append(dict(
            coverage_id=f"MC-{i:03d}", candidate_id=cid, event_id=ev,
            publication_date=pubdate if len(pubdate) == 10 else "unknown",
            outlet=srec[1].split("://")[1].split("/")[0].replace("www.", ""),
            author=tinfo.get("author", "unknown") or "unknown",
            title=title, url=srec[1],
            source_tier=meta.get("source_tier", "T2"),
            coverage_type=ctype, key_framing=framing,
            notable_quotes=quotes, framing_of_candidate=foca, mentions_opponent=opp,
            reliability_notes=rel or "retrieved and mirrored 2026-11-18"))
    write_csv("05_campaign_media/media_coverage.csv", MC_FIELDS, rows)

    rows = []
    for i, (cid, period, rtype, deadline, receipts, disb, coh, note) in enumerate(FINANCE, 1):
        rows.append(dict(
            finance_id=f"FIN-{i:03d}", candidate_id=cid, period=period,
            report_type=rtype, reporting_deadline=deadline, receipts=receipts,
            individual_contributions=U, pac_contributions=U, disbursements=disb,
            cash_on_hand=coh, debts_owed=U,
            source_urls=ref("wiki_ohio"), verification_status="partially verified",
            notes=note + " Individual, PAC and debt totals are not in the source table, so "
                         "they are recorded as unknown rather than estimated."))
    write_csv("06_campaign_finance/campaign_finance.csv", FIN_FIELDS, rows)

    rows = []
    for i, (race, name, date, cand, party, votes, pct, win, note) in enumerate(RESULTS, 1):
        rows.append(dict(race_id=race, race_name=name, election_date=date, candidate=cand,
                         party=party, votes=votes, percentage=pct, winner=win,
                         source_urls=ref("wiki_ohio"),
                         verification_status=("conflicting sources" if "conflicting" in note
                                              else "verified"),
                         notes=note))
    write_csv("07_electoral_context/election_results.csv", RES_FIELDS, rows)

    write_csv("07_electoral_context/county_results.csv", CQ_FIELDS, [])

    rows = []
    for i, (pol, spon, fs, fe, pop, n, moe, shares, key, note) in enumerate(POLLS, 1):
        b, h, o, u = shares
        leader = "Brown" if isinstance(b, int) and isinstance(h, int) and b > h else (
            "Husted" if isinstance(b, int) and isinstance(h, int) and h > b else "tied")
        margin = abs(b - h) if isinstance(b, int) and isinstance(h, int) else U
        rows.append(dict(
            poll_id=f"POLL-{i:03d}", pollster=pol, sponsor=spon, field_start=fs,
            field_end=fe, population=pop, sample_size=n, margin_of_error=moe,
            brown_pct=b, husted_pct=h, other_pct=o, undecided_pct=u,
            leader=leader, margin=margin, source_urls=ref(key),
            verification_status="verified" if key != "wiki_ohio" else "partially verified",
            notes=(note + " " if note else "")
            + "Leader and margin are computed from the printed two-way shares; the source "
              "prints no margin."))
    write_csv("07_electoral_context/polling.csv", POLL_FIELDS, rows)


if __name__ == "__main__":
    main()
