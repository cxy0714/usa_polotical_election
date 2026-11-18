"""Build the remaining contract CSVs: speeches, media, finance, electoral context."""
import sys

sys.path.insert(0, "_staging")
from b_common import ref, write_csv  # noqa: E402

U = "unknown"

# --------------------------------------------------------------- speeches --
SP_FIELDS = ["speech_id", "candidate_id", "event_id", "date", "speech_title", "speech_url",
             "transcript_url", "duration", "main_topics", "major_quotes",
             "rhetorical_devices", "opponent_references", "personal_story_elements",
             "policy_claims", "source_urls", "source", "verification_status"]

SPEECHES = [
    dict(candidate_id="BROWN", event_id="EV-001", date="2025-03-24",
         speech_title="Remarks at the launch of the Dignity of Work Institute",
         speech_url=U, transcript_url=U, duration=U,
         main_topics="wages; productivity; cost of living; corporate power",
         major_quotes="\"We see what's happened over the last 40 years. Corporate profits have "
         "soared, executive compensation has exploded, and productivity keeps going up and "
         "up, but wages aren't rising along with it, and the cost of living just keeps getting "
         "more expensive.\" / \"In a nutshell, people can't keep up no matter how hard they "
         "work.\"",
         rhetorical_devices="four-decade frame; anaphora of rising/not-rising; plain-language "
         "summary (\"in a nutshell\")",
         opponent_references="none",
         personal_story_elements="none in the retrieved passage",
         policy_claims="Wage stagnation against rising productivity; a survey of registered "
         "voters commissioned by the institute found a quarter had worked more than one job in "
         "the previous two years",
         source_urls=ref("ocj36_former_ohio_u_s_sen_sherrod_brown_launch"),
         source="Ohio Capital Journal report quoting the press conference",
         verification_status="verified"),
    dict(candidate_id="BROWN", event_id=U, date="2026-02-24",
         speech_title="Statement on the LCV Action Fund endorsement",
         speech_url=U, transcript_url=U, duration=U,
         main_topics="environment; Great Lakes; East Palestine; lead exposure",
         major_quotes="\"Ohioans have a right to clean air, safe drinking water, and a healthy "
         "environment... When Norfolk Southern's negligence contaminated East Palestine, I was "
         "there from day one holding them accountable and securing federal resources.\"",
         rhetorical_devices="rights framing; first-person presence claim (\"I was there\")",
         opponent_references="none",
         personal_story_elements="none",
         policy_claims="Great Lakes protection, clean-energy jobs, lead-paint and lead-pipe "
         "remediation",
         source_urls=ref("ref080_www_lcv_org_media_center_lcv_action"),
         source="LCV Action Fund endorsement release",
         verification_status="verified"),
    dict(candidate_id="BROWN", event_id=U, date="2026-07-15",
         speech_title="Statement on the Ohio Conference of Teamsters endorsement",
         speech_url=U, transcript_url=U, duration=U,
         main_topics="labour; pensions; rail safety; contracts",
         major_quotes="No verbatim Brown quote in the retrieved release; the release states he "
         "\"introduced the bipartisan Railway Safety Act\" and \"has committed to co-sponsoring "
         "the Faster Labor Contracts Act\".",
         rhetorical_devices="not applicable — third-person release",
         opponent_references="none", personal_story_elements="none",
         policy_claims="Railway Safety Act; Teamsters pension protection; Faster Labor "
         "Contracts Act co-sponsorship",
         source_urls=ref("ref132_teamster_org_2026_07_ohio_conference_of_teamsters_annou"),
         source="Ohio Conference of Teamsters release",
         verification_status="partially verified"),
    dict(candidate_id="BROWN", event_id=U, date="2026-08-21",
         speech_title="Interview remarks on data centers and the NRSC memo",
         speech_url=U, transcript_url=U, duration=U,
         main_topics="data centers; utility rates; tax abatements",
         major_quotes="\"Husted's been the front guy on all these data centers, 200 in Ohio, "
         "getting huge over-the-top tax breaks, and raising utility rates.\"",
         rhetorical_devices="synecdoche (Husted as \"the front guy\"); number as evidence "
         "(\"200 in Ohio\"); triple predicate",
         opponent_references="Husted by name, as the agent of the data-center build-out",
         personal_story_elements="none",
         policy_claims="Data-center tax abatements raise residential utility rates; 200 such "
         "facilities in Ohio (Brown's own count)",
         source_urls=ref("ocj31_leaked_memo_about_data_centers_shows_gop_worried_about"),
         source="Ohio Capital Journal one-on-one interview",
         verification_status="verified"),
    dict(candidate_id="BROWN", event_id=U, date="2026-10-31",
         speech_title="Closing-argument remarks at a Westerville stop",
         speech_url=U, transcript_url=U, duration=U,
         main_topics="corporate money; big tech; oil companies; rigged system",
         major_quotes="\"He's a special interest guy in Washington.\" / \"The system is more "
         "rigged than before.\" / \"I'll stand up to big tech. I'll stand up to the oil "
         "companies.\" / \"Corporations and billionaires may try to buy this election for their "
         "golden boy, Jon Husted. But there are more of us than there are of them.\"",
         rhetorical_devices="antithesis (them/us); \"golden boy\" diminution; triple \"I'll "
         "stand up to\"; populist we-they frame",
         opponent_references="Husted named and characterised as a special-interest insider",
         personal_story_elements="none in the retrieved passage",
         policy_claims="Outside money is distorting the race; Brown positions himself against "
         "tech and oil interests",
         source_urls=ref("b4_cle_clash"), source="Cleveland.com closing-argument report",
         verification_status="verified"),
    dict(candidate_id="BROWN", event_id=U, date="2023-02-27",
         speech_title="East Palestine town-hall press briefing",
         speech_url=U, transcript_url=U, duration=U,
         main_topics="rail safety; derailment; regulation",
         major_quotes="\"I want to see rail safety legislation passed in the next few weeks.\"",
         rhetorical_devices="urgency framing; first-person promise",
         opponent_references="none",
         personal_story_elements="residents' accounts relayed, not his own",
         policy_claims="Additional railcar regulations are needed to prevent recurrence",
         source_urls=ref("wiki_eastpal"),
         source="Wikipedia article on the derailment, citing the press briefing",
         verification_status="partially verified"),
    dict(candidate_id="BROWN", event_id="EV-013", date="2026-10-26",
         speech_title="Remarks at the Dayton get-out-the-vote rally",
         speech_url=U, transcript_url=U, duration=U,
         main_topics="cost of living; corruption; public programmes",
         major_quotes="No verbatim Brown quote in the retrieved report; the Dayton Daily News "
         "summarises that he \"promised to lower costs for Ohioans, combat political corruption, "
         "protect important public programs and take on powerful interests, billionaires and bad "
         "actors\".",
         rhetorical_devices="unknown — the report paraphrases rather than quotes",
         opponent_references="generic (\"powerful interests, billionaires and bad actors\")",
         personal_story_elements="unknown",
         policy_claims="Lower costs; protect public programmes; anti-corruption",
         source_urls=ref("ref129_www_daytondailynews_com_local_acton_brown_make_final_e"),
         source="Dayton Daily News report",
         verification_status="partially verified"),
    dict(candidate_id="BROWN", event_id="EV-015", date="2026-11-03",
         speech_title="Victory remarks",
         speech_url=U, transcript_url=U, duration=U,
         main_topics="working people; the result",
         major_quotes="Reported as a promise to \"put working people first\" (Dayton Daily News "
         "headline). No full text retrieved.",
         rhetorical_devices="unknown", opponent_references="unknown",
         personal_story_elements="unknown",
         policy_claims="unknown",
         source_urls=ref("b4_cle_result"), source="Cleveland.com result coverage",
         verification_status="partially verified"),
    dict(candidate_id="HUSTED", event_id="EV-016", date="2025-01-17",
         speech_title="Remarks accepting the Senate appointment",
         speech_url=U, transcript_url=U, duration=U,
         main_topics="continuity; Trump; Vance; Ohio",
         major_quotes="\"We have worked to make Ohio great again\" (as quoted by OCJ). DeWine: "
         "\"I wanted someone who knew Ohio.\"",
         rhetorical_devices="slogan borrowing (\"make Ohio great again\"); continuity frame",
         opponent_references="none",
         personal_story_elements="none in the retrieved passage",
         policy_claims="none specific",
         source_urls=ref("ocj25_ohio_lt_gov_jon_husted_to_replace_jd_vance_in_u_s_senat"),
         source="Ohio Capital Journal report",
         verification_status="verified"),
    dict(candidate_id="HUSTED", event_id=U, date="2026-01-22",
         speech_title="Statement at the Senate HELP Committee hearing on the abortion pill",
         speech_url=U, transcript_url=U, duration=U,
         main_topics="abortion; adoption; drug safety",
         major_quotes="No verbatim quote retrieved; OCJ reports he \"spoke against the abortion "
         "pill\" and \"pointed to his own adoption story, in which he said his mother could have "
         "chosen abortion\".",
         rhetorical_devices="personal disclosure as warrant",
         opponent_references="none",
         personal_story_elements="his own adoption, and his mother's choice",
         policy_claims="Restricting the abortion pill is a women's-safety measure; OCJ notes "
         "decades of research showing mifepristone is safe",
         source_urls=ref("ocj35_ohio_republican_us_sen_jon_husted_speaks_against_aborti"),
         source="Ohio Capital Journal report on the hearing",
         verification_status="verified"),
    dict(candidate_id="HUSTED", event_id=U, date="2026-07-27",
         speech_title="Senate floor remarks on requiring photo ID to vote",
         speech_url="https://upload.wikimedia.org/wikipedia/commons/9/92/"
                    "Jon_Husted_floor_remarks_on_photo_ID_requirement_for_voting.ogg",
         transcript_url=U, duration="62.3",
         main_topics="voting; photo ID; election administration",
         major_quotes="Not transcribed in this archive; the recording is 62.3 seconds of floor "
         "remarks (Congressional Record, Vol. 172, S4278).",
         rhetorical_devices="unknown — audio not transcribed",
         opponent_references="unknown",
         personal_story_elements="unknown",
         policy_claims="Photo ID should be required to vote (the subject of the remarks)",
         source_urls=ref("husted_floor_ogg"),
         source="Public-domain C-SPAN/Congressional Record recording via Wikimedia Commons",
         verification_status="verified"),
    dict(candidate_id="HUSTED", event_id="EV-031", date="2026-10-12",
         speech_title="Remarks at the Youngstown rally headlined by Donald Trump",
         speech_url=U, transcript_url=U, duration=U,
         main_topics="tenure; energy; immigration",
         major_quotes="\"My opponent, Sherrod Brown, has been in office for over 50 years. Can "
         "you name one thing that he's done to make your life better?\"",
         rhetorical_devices="rhetorical question; number as bludgeon",
         opponent_references="Brown by name",
         personal_story_elements="none in the retrieved passage",
         policy_claims="Brown's tenure produced no benefit; environmental policy closed power "
         "plants",
         source_urls=ref("b4_trib_mahoning"),
         source="Tribune Chronicle report (speech described as delivered again two days later)",
         verification_status="partially verified"),
    dict(candidate_id="HUSTED", event_id="EV-032", date="2026-10-15",
         speech_title="Remarks at the Mahoning County Republican Party headquarters",
         speech_url=U, transcript_url=U, duration=U,
         main_topics="state trajectory; energy; immigration; turnout",
         major_quotes="\"We changed the state... we took a state that was dying and made it a "
         "state that's now growing again, is now a place that people move to. It's a place where "
         "jobs are being created.\" / \"My opponent, Sherrod Brown, has been in office for over "
         "50 years. Can you name one thing that he's done to make your life better?\" / \"We "
         "have a tough campaign. Mid-term elections are elections where people maybe aren't as "
         "enthused to get out there and vote.\"",
         rhetorical_devices="before/after contrast; anaphora (\"It's a place where...\"); "
         "rhetorical question",
         opponent_references="Brown by name, twice",
         personal_story_elements="none",
         policy_claims="Ohio's recovery is attributable to Republican governance; closed power "
         "plants and refineries caused higher energy prices; border policy has \"real "
         "consequences\"",
         source_urls=ref("b4_trib_mahoning"), source="Tribune Chronicle report",
         verification_status="verified"),
    dict(candidate_id="HUSTED", event_id="EV-033", date="2026-10-28",
         speech_title="Remarks at the Trump rally in Chillicothe",
         speech_url=U, transcript_url=U, duration=U,
         main_topics="tenure; manufacturing; immigration",
         major_quotes="\"Here's the deal, he's been in office for over 50 years...\" / "
         "\"Protecting American manufacturing is the America First agenda\" (posted to X) / "
         "\"Why do people like Sherrod Brown care more about people who are illegally in this "
         "country than he cares about you?\"",
         rhetorical_devices="colloquial opener (\"Here's the deal\"); second-person accusation; "
         "slogan",
         opponent_references="Brown by name",
         personal_story_elements="none",
         policy_claims="Kenworth added 1,000 jobs in Chillicothe as a result of tariff "
         "protection; Brown's immigration stance endangers Ohioans",
         source_urls=ref("b4_cle_clash"), source="Cleveland.com report",
         verification_status="verified"),
]

VID_FIELDS = ["video_id", "candidate_id", "video_url", "date", "duration", "event_type",
              "main_topics", "relevant_timestamps", "transcript_available",
              "visual_observations", "completeness", "source_urls", "verification_status"]

VIDEOS = [
    dict(candidate_id="HUSTED", date="2026-07-27", duration="62.3",
         event_type="Senate floor remarks",
         video_url="https://upload.wikimedia.org/wikipedia/commons/9/92/"
                   "Jon_Husted_floor_remarks_on_photo_ID_requirement_for_voting.ogg",
         main_topics="photo ID for voting", relevant_timestamps=U,
         transcript_available="no", visual_observations="audio only (ogg, no video track)",
         completeness="clip", source_urls=ref("husted_floor_ogg"),
         verification_status="verified"),
    dict(candidate_id="BROWN", date="2022-05-10", duration="255.4",
         event_type="Senate floor remarks (pre-campaign)",
         video_url="https://upload.wikimedia.org/wikipedia/commons/7/7b/"
                   "Sherrod_Brown_on_his_support_for_the_nomination_of_Lisa_Cook_as_Federal_"
                   "Reserve_Governor.ogg",
         main_topics="Federal Reserve nomination", relevant_timestamps=U,
         transcript_available="no", visual_observations="audio only",
         completeness="clip", source_urls=ref("wiki_brown"),
         verification_status="verified"),
    dict(candidate_id="HUSTED", date="2026-10-29", duration="27.7",
         event_type="campaign video/social spot",
         video_url="https://upload.wikimedia.org/wikipedia/commons/e/ec/"
                   "VOTE_FOR_JON_HUSTED%21%21%21.webm",
         main_topics="get-out-the-vote appeal", relevant_timestamps=U,
         transcript_available="no",
         visual_observations="vertical 1080x1920 video; frames not inspected",
         completeness="full", source_urls=ref("video_vote_for_husted_2026"),
         verification_status="partially verified"),
    dict(candidate_id="HUSTED", date="2026-11-03", duration=U,
         event_type="concession",
         video_url="https://www.10tv.com/video/news/politics/elections/"
                   "senator-jon-husted-loses-the-2026-midterm-election/"
                   "530-5a0af209-82f5-4d66-85f1-715e0bf37b2a",
         main_topics="concession", relevant_timestamps=U, transcript_available="no",
         visual_observations=U, completeness="unknown",
         source_urls=ref("b4_wlwt_result"), verification_status="partially verified"),
    dict(candidate_id="HUSTED", date="2026-09-25", duration=U,
         event_type="manufacturing tour and endorsement",
         video_url="https://www.c-span.org/program/campaign-2026/"
                   "sen-jon-husted-r-oh-tours-manufacturing-facility-receives-campaign-"
                   "endorsement/685770",
         main_topics="manufacturing; Chamber endorsement", relevant_timestamps=U,
         transcript_available="no", visual_observations=U, completeness="unknown",
         source_urls=ref("ref125_www_uschamber_com_improving_government_u_s_chamber_endo"),
         verification_status="partially verified"),
    dict(candidate_id="BROWN", date="2026-11-03", duration=U,
         event_type="result-night coverage", video_url=U,
         main_topics="result", relevant_timestamps=U, transcript_available="no",
         visual_observations=U, completeness="unknown",
         source_urls=ref("b4_cle_result"), verification_status="unverified"),
    dict(candidate_id="BROWN", date="2026-10-26", duration=U,
         event_type="rally", video_url=U, main_topics="cost of living",
         relevant_timestamps=U, transcript_available="no", visual_observations=U,
         completeness="unknown",
         source_urls=ref("ref129_www_daytondailynews_com_local_acton_brown_make_final_e"),
         verification_status="unverified"),
    dict(candidate_id="BROWN", date="2026-10-24", duration=U, event_type="rally",
         video_url=U, main_topics="cost of living; corporate power",
         relevant_timestamps=U, transcript_available="no", visual_observations=U,
         completeness="unknown", source_urls=ref("b4_yahoo_keyissues"),
         verification_status="unverified"),
    dict(candidate_id="HUSTED", date="2026-10-12", duration=U, event_type="rally",
         video_url=U, main_topics="tenure attack", relevant_timestamps=U,
         transcript_available="no", visual_observations=U, completeness="unknown",
         source_urls=ref("b4_trib_mahoning"), verification_status="unverified"),
    dict(candidate_id="HUSTED", date="2026-10-15", duration=U, event_type="rally",
         video_url=U, main_topics="state trajectory", relevant_timestamps=U,
         transcript_available="no", visual_observations=U, completeness="unknown",
         source_urls=ref("b4_trib_mahoning"), verification_status="unverified"),
    dict(candidate_id="BROWN", date="2026-05-05", duration=U, event_type="primary night",
         video_url=U, main_topics="nomination", relevant_timestamps=U,
         transcript_available="no", visual_observations=U, completeness="unknown",
         source_urls=ref("ocj08_brown_wins_ohio_dem_u_s_senate_primary"),
         verification_status="unverified"),
    dict(candidate_id="HUSTED", date="2026-01-22", duration=U, event_type="committee hearing",
         video_url=U, main_topics="abortion pill", relevant_timestamps=U,
         transcript_available="no", visual_observations=U, completeness="unknown",
         source_urls=ref("ocj35_ohio_republican_us_sen_jon_husted_speaks_against_aborti"),
         verification_status="unverified"),
]

if __name__ == "__main__":
    rows = []
    for i, s in enumerate(SPEECHES, 1):
        r = dict(s)
        r["speech_id"] = f"SP-{i:03d}"
        rows.append(r)
    write_csv("03_speeches/speech_archive.csv", SP_FIELDS, rows)
    print("BROWN", sum(1 for r in rows if r["candidate_id"] == "BROWN"),
          "HUSTED", sum(1 for r in rows if r["candidate_id"] == "HUSTED"))
    vrows = []
    for i, v in enumerate(VIDEOS, 1):
        r = dict(v)
        r["video_id"] = f"VID-{i:03d}"
        vrows.append(r)
    write_csv("03_speeches/speech_video_index.csv", VID_FIELDS, vrows)
