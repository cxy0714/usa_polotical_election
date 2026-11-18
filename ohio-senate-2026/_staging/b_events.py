"""Build 02_campaign_events/campaign_events.csv."""
import sys

sys.path.insert(0, "_staging")
from b_common import ref, write_csv  # noqa: E402

FIELDS = ["event_id", "candidate_id", "event_date", "event_time", "event_title",
          "event_category", "city", "venue", "state_region", "event_status",
          "campaign_phase", "stated_purpose", "observable_function",
          "analyst_interpretation", "target_audience", "main_messages", "policy_issues",
          "speech_summary", "transcript_url", "video_url", "photo_urls", "media_coverage",
          "opponent_reference", "visual_notes", "source_urls", "verification_status",
          "analyst_notes"]

U = "unknown"
END_MAIN = ("endorsement announcement; no candidate speech was retrieved for this item")
END_SPEECH = "unknown — the retrieved report covers the endorsement, not a speech text"
END_FUNC = "coalition signalling and endorsement accumulation"
END_INTERP = ("Endorsement events are treated here as evidence of elite consolidation "
              "rather than as persuasion events; the archive does not infer crowd size or "
              "message content that the report does not state.")

EVENTS = [
    # ------------------------- Sherrod Brown ------------------------------
    dict(candidate_id="BROWN", event_date="2025-03-24", event_time=U,
         event_title="Press conference launching the Dignity of Work Institute",
         event_category="press_conference", city=U, venue=U, state_region="statewide",
         event_status="held", campaign_phase="pre_launch",
         stated_purpose="Launch a nonprofit to advocate for workers' policy interests",
         observable_function="policy-vehicle launch before the campaign",
         analyst_interpretation="Reads as the message-building step that preceded the "
         "August launch: the affordability frame was institutionalised before it was "
         "campaigned on.",
         target_audience="reporters; labour and advocacy networks",
         main_messages="Corporate profits and executive pay rose while wages stagnated; "
         "\"people can't keep up no matter how hard they work\"",
         policy_issues="Economy; Labor",
         speech_summary="Opening statement plus a survey release; Brown: \"We see what's "
         "happened over the last 40 years... Corporate profits have soared, executive "
         "compensation has exploded, and productivity keeps going up and up, but wages "
         "aren't rising along with it.\"",
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Ohio Capital Journal, 2025-03-25",
         opponent_reference="none", visual_notes="unknown — no image retrieved",
         source_urls=ref("ocj36_former_ohio_u_s_sen_sherrod_brown_launch"),
         verification_status="verified",
         analyst_notes="Date is the reported Monday press conference (2025-03-24); the "
         "article is dated 2025-03-25."),
    dict(candidate_id="BROWN", event_date="2025-08-18", event_time=U,
         event_title="Campaign launch for the 2026 Senate special election",
         event_category="launch", city=U, venue=U, state_region="statewide",
         event_status="held", campaign_phase="launch",
         stated_purpose="Announce a challenge to appointed Sen. Jon Husted",
         observable_function="entry into the race",
         analyst_interpretation="The launch inverted the usual challenger framing: Brown "
         "ran as the known quantity against an appointee he portrayed as unelected.",
         target_audience="statewide media; Democratic base",
         main_messages="Comeback and accountability framing; the seat was appointed, not "
         "elected", policy_issues="Democracy; Economy",
         speech_summary="unknown — the retrieved launch coverage does not quote a speech",
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: News and Sentinel, 2025-08-18",
         opponent_reference="yes — Husted described as an appointee",
         visual_notes="unknown", source_urls=ref("ref063_www_newsandsentinel"),
         verification_status="verified", analyst_notes="City not stated in the retrieved text."),
    dict(candidate_id="BROWN", event_date="2025-09-22", event_time=U,
         event_title="UFCW Local 1059 endorsement", event_category="endorsement_event",
         city=U, venue=U, state_region="statewide", event_status="held",
         campaign_phase="primary", stated_purpose=END_MAIN, observable_function=END_FUNC,
         analyst_interpretation=END_INTERP, target_audience="union members",
         main_messages=END_MAIN, policy_issues="Labor", speech_summary=END_SPEECH,
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Ohio Capital Journal, 2025-09",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("wiki_ohio"), verification_status="partially verified",
         analyst_notes="Recorded in the article's endorsement list; the original UFCW "
         "release was not retrieved."),
    dict(candidate_id="BROWN", event_date="2025-10-07", event_time=U,
         event_title="IUPAT endorsement", event_category="endorsement_event",
         city=U, venue=U, state_region="national", event_status="held",
         campaign_phase="primary", stated_purpose=END_MAIN, observable_function=END_FUNC,
         analyst_interpretation=END_INTERP, target_audience="painters and allied trades",
         main_messages=END_MAIN, policy_issues="Labor", speech_summary=END_SPEECH,
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 release retrieved: IUPAT, 2025-10-07",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("ref066_www_iupat_org_2025_10_07_iupat_endorses_sherrod_brown_f"),
         verification_status="verified", analyst_notes="National union release."),
    dict(candidate_id="BROWN", event_date="2025-11-03", event_time=U,
         event_title="UAW endorsement", event_category="endorsement_event",
         city=U, venue=U, state_region="statewide", event_status="held",
         campaign_phase="primary", stated_purpose=END_MAIN, observable_function=END_FUNC,
         analyst_interpretation=END_INTERP, target_audience="auto workers",
         main_messages=END_MAIN, policy_issues="Labor", speech_summary=END_SPEECH,
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Chronicle-Telegram, 2025-11-03",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("ref072_chroniclet_com_news_448231_uaw_endorses_democrat_sherro"),
         verification_status="verified", analyst_notes="UAW's early endorsement was the "
         "first big labour signal of the cycle."),
    dict(candidate_id="BROWN", event_date="2025-12-15", event_time=U,
         event_title="United Steelworkers endorsement", event_category="endorsement_event",
         city=U, venue=U, state_region="statewide", event_status="held",
         campaign_phase="primary", stated_purpose=END_MAIN, observable_function=END_FUNC,
         analyst_interpretation=END_INTERP, target_audience="steel and manufacturing workers",
         main_messages=END_MAIN, policy_issues="Labor", speech_summary=END_SPEECH,
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Chronicle-Telegram, 2025-12-15",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("ref029_chroniclet_com_news_452022_2026_us_senate_race_united_s"),
         verification_status="verified",
         analyst_notes="Same story also records the Cleveland Building Trades endorsement "
         "of Husted — the labour split is documented on both sides."),
    dict(candidate_id="BROWN", event_date="2025-12-17", event_time=U,
         event_title="Columbus small-business affordability roundtable",
         event_category="small_business_visit", city="Columbus", venue=U,
         state_region="Central", event_status="held", campaign_phase="primary",
         stated_purpose="Discuss affordability with Columbus small business owners",
         observable_function="listening-format retail politics",
         analyst_interpretation="The roundtable format let Brown make the affordability "
         "argument in a non-rally setting, which suits a candidate whose weakness was "
         "long tenure rather than name recognition.",
         target_audience="small business owners; local press",
         main_messages="Cost of doing business and cost of living", policy_issues="Economy",
         speech_summary="unknown — the report summarises the discussion but quotes no remarks",
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Ohio Capital Journal, 2025-12-22",
         opponent_reference="yes — the report notes Husted was appointed earlier in 2025",
         visual_notes="A photograph of Brown at the roundtable was published by OCJ",
         source_urls=ref("ocj33_ohio_democrat_sherrod_brown_talks_affordability_at_colu"),
         verification_status="verified",
         analyst_notes="Date inferred from the report's 'Wednesday' plus the 2025-12-22 "
         "publication; flagged as partially verified in the notes rather than hidden."),
    dict(candidate_id="BROWN", event_date="2026-02-16", event_time=U,
         event_title="Ohio AFL-CIO endorsement", event_category="labor_event",
         city=U, venue=U, state_region="statewide", event_status="held",
         campaign_phase="primary", stated_purpose=END_MAIN, observable_function=END_FUNC,
         analyst_interpretation=END_INTERP, target_audience="state federation members",
         main_messages=END_MAIN, policy_issues="Labor", speech_summary=END_SPEECH,
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 listing retrieved: Wikipedia endorsement list",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("wiki_ohio"), verification_status="partially verified",
         analyst_notes="The cited local coverage (WFMJ) returned HTTP 429 at retrieval, so "
         "the date rests on the encyclopedia's citation."),
    dict(candidate_id="BROWN", event_date="2026-03-02", event_time=U,
         event_title="Ohio Democratic Party endorsement", event_category="party_event",
         city=U, venue=U, state_region="statewide", event_status="held",
         campaign_phase="primary", stated_purpose="Party endorsement of statewide candidates",
         observable_function="party consolidation",
         analyst_interpretation="A state party endorsement this early mainly signals that no "
         "serious primary opposition was tolerated.",
         target_audience="party activists", main_messages="Party unity behind the ticket",
         policy_issues="Democracy", speech_summary=END_SPEECH,
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Statehouse News Bureau, 2026-03-02",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("ref059_www_statenews_org_government_politics_2026_03_02_oh"),
         verification_status="verified", analyst_notes="Endorsement covered alongside the "
         "governor's race."),
    dict(candidate_id="BROWN", event_date="2026-05-05", event_time=U,
         event_title="Democratic primary night", event_category="watch_party",
         city=U, venue=U, state_region="statewide", event_status="held",
         campaign_phase="election_day", stated_purpose="Await and claim the primary result",
         observable_function="result-claiming",
         analyst_interpretation="The primary was not the contest; the 89.4% share matters "
         "mainly as a demonstration of base consolidation before the general.",
         target_audience="supporters; press", main_messages="Nomination secured; the general "
         "starts now", policy_issues="Democracy",
         speech_summary="unknown — the retrieved primary-night report describes the result "
         "rather than quoting a victory speech",
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Ohio Capital Journal, 2026-05-05",
         opponent_reference="yes — Husted named as the Republican nominee",
         visual_notes=U, source_urls=ref("ocj08_brown_wins_ohio_dem_u_s_senate_primary"),
         verification_status="verified",
         analyst_notes="Vote counts: Brown 712,106 (89.40%), Kincaid 84,405 (10.60%)."),
    dict(candidate_id="BROWN", event_date="2026-10-12", event_time=U,
         event_title="Joint discussion of Social Security fixes", event_category="other",
         city=U, venue=U, state_region="statewide", event_status="held",
         campaign_phase="general", stated_purpose="Discuss how to fix Social Security",
         observable_function="issue-specific joint appearance",
         analyst_interpretation="Any joint appearance is notable in a race where no formal "
         "debate is documented; it shows the campaigns would share a stage on a "
         "retail-friendly issue.",
         target_audience="older voters", main_messages="Protect Social Security",
         policy_issues="Economy", speech_summary="unknown — the retrieved summary does not "
         "quote either candidate", transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Ohio Capital Journal, 2026-10-12",
         opponent_reference="yes — both candidates participated",
         visual_notes=U, source_urls=ref("ocj19_ohio_us_senate_candidates_discuss_how_to"),
         verification_status="partially verified",
         analyst_notes="Format, venue and city are not described in the retrieved text; the "
         "row records the appearance, not an inferred rally."),
    dict(candidate_id="BROWN", event_date="2026-10-24", event_time=U,
         event_title="Cleveland rally", event_category="rally",
         city="Cleveland", venue="Public Auditorium and Conference Center",
         state_region="Northeast", event_status="held", campaign_phase="early_voting",
         stated_purpose="Get-out-the-vote rally in the campaign's largest Democratic region",
         observable_function="mass mobilisation in the base's densest county",
         analyst_interpretation="Cuyahoga County is the Democratic vote bank; a Cleveland "
         "rally in the final ten days is base-turnout logistics, not persuasion.",
         target_audience="Cuyahoga County Democrats", main_messages="Cost of living; "
         "corporate power", policy_issues="Economy; Democracy",
         speech_summary="unknown — the retrieved source is a photograph caption, not a "
         "transcript", transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 photo caption retrieved: Columbus Dispatch via Yahoo, 2026-10-18 "
         "(caption dated 2026-10-24)",
         opponent_reference=U, visual_notes="Photograph shows Brown looking toward the crowd "
         "behind the stage while delivering remarks",
         source_urls=ref("b4_yahoo_keyissues"), verification_status="partially verified",
         analyst_notes="Documented only through a dated press photograph caption; no "
         "attendance figure was reported."),
    dict(candidate_id="BROWN", event_date="2026-10-26", event_time=U,
         event_title="Dayton get-out-the-vote rally with Amy Acton and John Legend",
         event_category="rally", city="Dayton", venue="The Brightside Music and Event Venue",
         state_region="Southwest", event_status="held", campaign_phase="gotv",
         stated_purpose="Final-week turnout push with the Democratic gubernatorial nominee",
         observable_function="joint ticket mobilisation with a celebrity surrogate",
         analyst_interpretation="Pairing with Acton let Brown borrow the governor race's "
         "volunteer network; the celebrity surrogate signals an entertainment-style "
         "turnout event rather than a policy stop.",
         target_audience="Montgomery County Democrats; young voters",
         main_messages="\"We, together, are going to make it all cost less\" (Acton); "
         "leaders who think about all Ohioans (Legend)",
         policy_issues="Economy; Healthcare",
         speech_summary="Brown spoke at a packed ballroom and promised to lower costs, "
         "combat political corruption and take on \"powerful interests, billionaires and bad "
         "actors\", per the Dayton Daily News report.",
         transcript_url=U, video_url=U, photo_urls="unknown",
         media_coverage="1 report retrieved: Dayton Daily News, 2026-10-26",
         opponent_reference=U,
         visual_notes="Photographs show Brown and Acton waving after speaking; the ballroom "
         "is described as packed",
         source_urls=ref("ref129_www_daytondailynews_com_local_acton_brown_make_final_e"),
         verification_status="verified",
         analyst_notes="Crowd described qualitatively as \"hundreds of cheering audience "
         "members\" and a \"capacity\" room; no official count exists."),
    dict(candidate_id="BROWN", event_date="2026-10-28", event_time=U,
         event_title="\"Fighting For Ohio\" rally at the Woodward Theater",
         event_category="rally", city="Cincinnati", venue="Woodward Theater, Over-the-Rhine",
         state_region="Southwest", event_status="held", campaign_phase="gotv",
         stated_purpose="Final-week rally in Hamilton County",
         observable_function="urban base mobilisation",
         analyst_interpretation="Two rallies in three days across the state's two biggest "
         "Democratic counties is a turnout map, not a persuasion schedule.",
         target_audience="Hamilton County Democrats", main_messages="unknown",
         policy_issues="Economy", speech_summary="unknown — documented through a dated "
         "photograph caption only", transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 photo caption retrieved: Columbus Dispatch via Yahoo, 2026-10-18",
         opponent_reference=U,
         visual_notes="Caption describes Brown giving a speech at the rally",
         source_urls=ref("b4_yahoo_keyissues"), verification_status="partially verified",
         analyst_notes="No attendance figure reported."),
    dict(candidate_id="BROWN", event_date="2026-11-03", event_time=U,
         event_title="Victory remarks after the Senate result",
         event_category="victory_speech", city=U, venue=U, state_region="statewide",
         event_status="held", campaign_phase="election_day",
         stated_purpose="Claim the result and set up the return to Washington",
         observable_function="result-claiming and mandate framing",
         analyst_interpretation="The victory text is thin in the retrieved record; the "
         "campaign's post-election message was carried mostly by interviews the following "
         "week.",
         target_audience="supporters; national press",
         main_messages="\"put working people first\" (Dayton Daily News headline, 2026-11-04)",
         policy_issues="Economy; Labor",
         speech_summary="Reported as a promise to \"put working people first\"; no full text "
         "retrieved", transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="3 reports retrieved: Cleveland.com, WLWT, Boston Herald (AP)",
         opponent_reference=U, visual_notes=U,
         source_urls=ref("b4_cle_result"), verification_status="partially verified",
         analyst_notes="City and venue for the remarks were not retrievable; the 10TV video "
         "page returned HTTP 403."),
    # -------------------------- Jon Husted --------------------------------
    dict(candidate_id="HUSTED", event_date="2025-01-17", event_time="15:47",
         event_title="Appointment to the U.S. Senate announced by Gov. Mike DeWine",
         event_category="appointment_announcement", city="Columbus", venue="Ohio Statehouse",
         state_region="Central", event_status="held", campaign_phase="pre_launch",
         stated_purpose="Announce the gubernatorial appointment to the vacant Senate seat",
         observable_function="transfer of incumbency",
         analyst_interpretation="This is the event that created the incumbency Husted "
         "defended in 2026; every later 'incumbent' reference in this archive dates to "
         "2025-01-17 (announcement) and 2025-01-21 (oath).",
         target_audience="statewide press; Republican donors",
         main_messages="\"I wanted someone who knew Ohio\" (DeWine); \"We have worked to make "
         "Ohio great again\" (Husted)",
         policy_issues="Democracy", speech_summary="DeWine and Husted spoke; Husted framed "
         "the appointment as continuity with Trump and Vance.",
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="2 reports retrieved: Ohio Capital Journal, 2025-01-17; NBC4, 2025-01-09",
         opponent_reference="none", visual_notes="unknown",
         source_urls=ref("ocj25_ohio_lt_gov_jon_husted_to_replace_jd_vance_in_u_s_senat"),
         verification_status="verified",
         analyst_notes="Time 15:47 is the OCJ publication timestamp, used here as the "
         "closest available marker; it is not the speaking time."),
    dict(candidate_id="HUSTED", event_date="2025-01-21", event_time=U,
         event_title="Sworn in as U.S. Senator by Vice President JD Vance",
         event_category="swearing_in", city="Washington", venue="U.S. Capitol",
         state_region="national", event_status="held", campaign_phase="pre_launch",
         stated_purpose="Take the oath of office", observable_function="incumbency begins",
         analyst_interpretation="The oath date is the defensible start of Husted's Senate "
         "tenure; the brief's 2025-01-14 is unsupported by every retrieved record.",
         target_audience="Senate; press", main_messages="unknown",
         policy_issues="Democracy", speech_summary="unknown — no remarks retrieved",
         transcript_url=U, video_url=U,
         photo_urls="https://upload.wikimedia.org/wikipedia/commons/f/f4/"
                    "Jon_Husted_sworn_in_by_JD_Vance_%282025%29.jpg",
         media_coverage="1 photograph and 1 report retrieved (Commons file; NBC4)",
         opponent_reference="none",
         visual_notes="Photograph shows Vance administering the oath; Commons file dated "
         "2025-01-21",
         source_urls=ref("husted_sworn_in_2025"), verification_status="verified",
         analyst_notes="This image is the strongest independent corroboration of the oath "
         "date in the archive."),
    dict(candidate_id="HUSTED", event_date="2025-04-09", event_time=U,
         event_title="Senate campaign launch, same day as Trump's endorsement",
         event_category="launch", city=U, venue=U, state_region="statewide",
         event_status="held", campaign_phase="launch",
         stated_purpose="Launch the 2026 campaign with presidential backing",
         observable_function="launch under a presidential umbrella",
         analyst_interpretation="Launching on the day of Trump's endorsement made the "
         "campaign a referendum on Trump's standing in Ohio rather than on Husted's record.",
         target_audience="Republican primary electorate", main_messages="Trump-aligned "
         "continuity", policy_issues="Economy; Immigration",
         speech_summary="unknown — the AP copy was read through a Wayback capture of the "
         "launch story", transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="2 reports retrieved: Spectrum News 1, 2025-04-09; AP via Wayback",
         opponent_reference="yes — framed against Brown's expected entry",
         visual_notes=U,
         source_urls=ref("ref014_web_archive_org_web_20250410091543_https_apnews_com_art"),
         verification_status="verified", analyst_notes="City not stated in the retrieved text."),
    dict(candidate_id="HUSTED", event_date="2025-08-21", event_time=U,
         event_title="Northwest Ohio Building Trades Council endorsement",
         event_category="labor_event", city=U, venue=U, state_region="Northwest",
         event_status="held", campaign_phase="primary", stated_purpose=END_MAIN,
         observable_function=END_FUNC, analyst_interpretation=END_INTERP,
         target_audience="building trades members", main_messages=END_MAIN,
         policy_issues="Labor", speech_summary=END_SPEECH, transcript_url=U, video_url=U,
         photo_urls=U, media_coverage="1 report retrieved: The Blade, 2025-08-21",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("ref035_www_toledoblade_com_local_politics_2025_08_21_northwes"),
         verification_status="verified", analyst_notes="Regional building-trades endorsement."),
    dict(candidate_id="HUSTED", event_date="2025-09-12", event_time=U,
         event_title="Operating Engineers Locals 18 and 66 endorsement",
         event_category="labor_event", city=U, venue=U, state_region="statewide",
         event_status="held", campaign_phase="primary", stated_purpose=END_MAIN,
         observable_function=END_FUNC, analyst_interpretation=END_INTERP,
         target_audience="operating engineers", main_messages=END_MAIN,
         policy_issues="Labor", speech_summary=END_SPEECH, transcript_url=U, video_url=U,
         photo_urls=U, media_coverage="1 report retrieved: NBC News, 2025-09-12",
         opponent_reference="yes — reported as a union Husted took from Brown",
         visual_notes=U, source_urls=ref("ref032_www_nbcnews_com_politics_2026_election"),
         verification_status="verified",
         analyst_notes="NBC framed the endorsement as unions betting early on Republicans; "
         "the Axios scoop cited by Wikipedia was not retrieved."),
    dict(candidate_id="HUSTED", event_date="2026-01-07", event_time=U,
         event_title="Ohio Attorney General Dave Yost endorsement",
         event_category="endorsement_event", city=U, venue=U, state_region="statewide",
         event_status="held", campaign_phase="primary", stated_purpose=END_MAIN,
         observable_function=END_FUNC, analyst_interpretation=END_INTERP,
         target_audience="statewide Republican officeholders", main_messages=END_MAIN,
         policy_issues="Democracy", speech_summary=END_SPEECH, transcript_url=U, video_url=U,
         photo_urls=U, media_coverage="1 report retrieved: ABC 6, 2026-01-07",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("ref022_abc6onyourside_com_news_local_husted_announces_endorsem"),
         verification_status="verified", analyst_notes="First statewide-officeholder "
         "endorsement of the sequence."),
    dict(candidate_id="HUSTED", event_date="2026-01-09", event_time=U,
         event_title="Ohio Treasurer Robert Sprague endorsement",
         event_category="endorsement_event", city=U, venue=U, state_region="statewide",
         event_status="held", campaign_phase="primary", stated_purpose=END_MAIN,
         observable_function=END_FUNC, analyst_interpretation=END_INTERP,
         target_audience="statewide Republican officeholders", main_messages=END_MAIN,
         policy_issues="Democracy", speech_summary=END_SPEECH, transcript_url=U, video_url=U,
         photo_urls=U, media_coverage="1 report retrieved: Chronicle-Telegram, 2026-01-09",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("ref021_chroniclet_com_news_453974_ohio_treasurer_robert_spragu"),
         verification_status="verified", analyst_notes="Sprague was himself a 2026 statewide "
         "candidate."),
    dict(candidate_id="HUSTED", event_date="2026-01-16", event_time=U,
         event_title="U.S. Rep. David Taylor endorsement", event_category="endorsement_event",
         city=U, venue=U, state_region="Southwest", event_status="held",
         campaign_phase="primary", stated_purpose=END_MAIN, observable_function=END_FUNC,
         analyst_interpretation=END_INTERP, target_audience="congressional delegation",
         main_messages=END_MAIN, policy_issues="Democracy", speech_summary=END_SPEECH,
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Chronicle-Telegram, 2026-01-16",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("ref019_chroniclet_com_news_454656_ohio_gop_congressman_endorse"),
         verification_status="verified", analyst_notes="Region assigned by the member's "
         "district rather than by any stated event location."),
    dict(candidate_id="HUSTED", event_date="2026-01-23", event_time=U,
         event_title="U.S. Rep. Bob Latta endorsement", event_category="endorsement_event",
         city=U, venue=U, state_region="Northwest", event_status="held",
         campaign_phase="primary", stated_purpose=END_MAIN, observable_function=END_FUNC,
         analyst_interpretation=END_INTERP, target_audience="congressional delegation",
         main_messages=END_MAIN, policy_issues="Democracy", speech_summary=END_SPEECH,
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Chronicle-Telegram, 2026-01-23",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("ref018_chroniclet_com_news_455338_us_rep_bob_latta_endorses_fe"),
         verification_status="verified", analyst_notes="Region assigned by district."),
    dict(candidate_id="HUSTED", event_date="2026-02-21", event_time=U,
         event_title="State Auditor Keith Faber endorsement",
         event_category="endorsement_event", city=U, venue=U, state_region="statewide",
         event_status="held", campaign_phase="primary", stated_purpose=END_MAIN,
         observable_function=END_FUNC, analyst_interpretation=END_INTERP,
         target_audience="statewide Republican officeholders", main_messages=END_MAIN,
         policy_issues="Democracy", speech_summary=END_SPEECH, transcript_url=U, video_url=U,
         photo_urls=U, media_coverage="1 report retrieved: Chronicle-Telegram, 2026-02-21",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("ref020_chroniclet_com_news_458211_state_auditor_keith_faber_en"),
         verification_status="verified",
         analyst_notes="Completes the sweep of Ohio's Republican statewide officeholders."),
    dict(candidate_id="HUSTED", event_date="2026-03-22", event_time=U,
         event_title="Local Ohio House Republicans' endorsement",
         event_category="endorsement_event", city=U, venue=U, state_region="statewide",
         event_status="held", campaign_phase="primary", stated_purpose=END_MAIN,
         observable_function=END_FUNC, analyst_interpretation=END_INTERP,
         target_audience="state legislators", main_messages=END_MAIN, policy_issues="Democracy",
         speech_summary=END_SPEECH, transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Chronicle-Telegram, 2026-03-22",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("ref024_chroniclet_com_news_460999_local_ohio_house_republica"),
         verification_status="verified", analyst_notes="Group endorsement, not a single member."),
    dict(candidate_id="HUSTED", event_date="2026-05-04", event_time=U,
         event_title="Record-setting county sheriff endorsements announced",
         event_category="endorsement_event", city=U, venue=U, state_region="statewide",
         event_status="held", campaign_phase="primary",
         stated_purpose="Announce endorsements from 75 Ohio county sheriffs",
         observable_function="law-enforcement coalition signalling",
         analyst_interpretation="Sheriffs are the most local law-enforcement brand in Ohio "
         "and the endorsement set is explicitly framed as a record — a claim only the "
         "campaign asserts.",
         target_audience="rural and exurban voters", main_messages="Law and order; border "
         "security", policy_issues="Immigration; Other", speech_summary=END_SPEECH,
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Highland County Press, 2026-05-04",
         opponent_reference="none", visual_notes=U, source_urls=ref("ref025_www_highlandcount"),
         verification_status="partially verified",
         analyst_notes="The \"record\" framing is the campaign's; no independent tally was "
         "retrieved."),
    dict(candidate_id="HUSTED", event_date="2026-05-05", event_time=U,
         event_title="Republican primary night (unopposed)",
         event_category="watch_party", city=U, venue=U, state_region="statewide",
         event_status="held", campaign_phase="election_day",
         stated_purpose="Await the primary result", observable_function="result-claiming",
         analyst_interpretation="An unopposed primary produced 736,413 votes — a useful "
         "measure of the Republican floor in a midterm.",
         target_audience="supporters", main_messages="unknown",
         policy_issues="Democracy", speech_summary="unknown — no remarks retrieved",
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 record retrieved: article primary results table",
         opponent_reference="none", visual_notes=U, source_urls=ref("wiki_ohio"),
         verification_status="verified",
         analyst_notes="Wikipedia's Jon Husted biography says he \"won the Republican "
         "nomination in March 2026\"; the canvass date is 2026-05-05 and that discrepancy is "
         "recorded as conflicting sources in results_notes.md."),
    dict(candidate_id="HUSTED", event_date="2026-07-10", event_time=U,
         event_title="Associated Builders and Contractors of Ohio endorsement",
         event_category="endorsement_event", city=U, venue=U, state_region="statewide",
         event_status="held", campaign_phase="general", stated_purpose=END_MAIN,
         observable_function="merit-shop coalition signalling",
         analyst_interpretation="ABC is the non-union contractors' association; its "
         "endorsement is the counterweight to Brown's building-trades support.",
         target_audience="non-union contractors", main_messages=END_MAIN,
         policy_issues="Labor", speech_summary=END_SPEECH, transcript_url=U, video_url=U,
         photo_urls=U, media_coverage="1 report retrieved: Chronicle-Telegram, 2026-07-10",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("ref028_chroniclet_com_news_470613_abc_of_ohio_endorses_jon_hus"),
         verification_status="verified", analyst_notes="Filed under Labor because the "
         "endorsing body is a labour-market organisation."),
    dict(candidate_id="HUSTED", event_date="2026-09-25", event_time=U,
         event_title="U.S. Chamber endorsement and manufacturing tour stop",
         event_category="workplace_visit", city=U, venue=U, state_region="statewide",
         event_status="held", campaign_phase="general",
         stated_purpose="Accept the Chamber endorsement at a manufacturing facility",
         observable_function="business-coalition validation at a factory gate",
         analyst_interpretation="C-SPAN catalogued the stop as \"tours manufacturing "
         "facility, receives campaign endorsement\" — the visual grammar of the Husted "
         "argument (jobs, not culture war).",
         target_audience="business owners; manufacturing workers",
         main_messages="Manufacturing and permitting reform", policy_issues="Economy; Labor",
         speech_summary="unknown — the C-SPAN record was not retrievable in body form",
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="2 records retrieved: U.S. Chamber release, 2026-09-25; C-SPAN "
         "program page (HTTP 202, no body)",
         opponent_reference="none", visual_notes=U,
         source_urls=ref("ref125_www_uschamber_com_improving_government_u_s_chamber_endo"),
         verification_status="partially verified",
         analyst_notes="The C-SPAN page returned 202 with no content; city and facility are "
         "therefore unknown."),
    dict(candidate_id="HUSTED", event_date="2026-10-12", event_time=U,
         event_title="Youngstown rally headlined by President Donald Trump",
         event_category="rally", city="Youngstown", venue="Covelli Centre",
         state_region="Northeast", event_status="held", campaign_phase="general",
         stated_purpose="Trump rally to boost Husted in the Mahoning Valley",
         observable_function="presidential surrogate mobilisation",
         analyst_interpretation="The Valley is the most competitive Democratic-held region "
         "in the state; a Trump rally there is aimed at the crossover voters Brown needed.",
         target_audience="Mahoning Valley working-class voters",
         main_messages="\"My opponent, Sherrod Brown, has been in office for over 50 years. "
         "Can you name one thing that he's done to make your life better?\"",
         policy_issues="Economy; Energy; Immigration",
         speech_summary="Husted delivered a version of his standard stump speech, per the "
         "Tribune Chronicle's account of the same speech two days later.",
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="2 reports retrieved: Tribune Chronicle, 2026-10-15; IBTimes UK, "
         "2026-10-12 (Trump's remarks)",
         opponent_reference="yes — Brown by name, repeatedly",
         visual_notes=U,
         source_urls=ref("b4_trib_mahoning"), verification_status="partially verified",
         analyst_notes="Date fixed by the Tribune Chronicle's \"Monday\" reference against "
         "its 2026-10-15 publication (Thursday event)."),
    dict(candidate_id="HUSTED", event_date="2026-10-15", event_time=U,
         event_title="Mahoning County Republican Party headquarters rally",
         event_category="rally", city="Boardman", venue="Mahoning County Republican Party "
         "headquarters", state_region="Northeast", event_status="held",
         campaign_phase="general", stated_purpose="County party rally with Gov. Mike DeWine",
         observable_function="county-level party mobilisation",
         analyst_interpretation="DeWine's presence tied Husted back to the governor who "
         "appointed him — helpful with institutional Republicans, unhelpful with the "
         "anti-establishment primary electorate he had already won.",
         target_audience="Mahoning County Republicans", main_messages="\"We changed the "
         "state... we took a state that was dying and made it a state that's now growing "
         "again\"; Brown \"has been in office for over 50 years\"",
         policy_issues="Economy; Energy; Immigration",
         speech_summary="Husted argued the race is a choice between moving forward and going "
         "back, blamed Brown for \"radical environmental policies that closed 23 power "
         "plants\", and said midterms are hard because turnout is lower.",
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Tribune Chronicle, 2026-10-15",
         opponent_reference="yes — the \"50 years\" and \"23 power plants\" lines",
         visual_notes="Photograph shows Husted talking with a supporter after the event",
         source_urls=ref("b4_trib_mahoning"), verification_status="verified",
         analyst_notes="Crowd size not reported; the venue is a party headquarters, not a "
         "mass rally site."),
    dict(candidate_id="HUSTED", event_date="2026-10-28", event_time=U,
         event_title="Trump rally in Chillicothe", event_category="rally",
         city="Chillicothe", venue=U, state_region="Southeast", event_status="held",
         campaign_phase="gotv", stated_purpose="Final-week presidential rally for Husted",
         observable_function="presidential surrogate mobilisation in a rural region",
         analyst_interpretation="Chillicothe is also the Kenworth plant town Husted uses as "
         "his manufacturing proof point; message and venue were deliberately the same story.",
         target_audience="southeast Ohio manufacturing and rural voters",
         main_messages="\"Here's the deal, he's been in office for over 50 years\"; "
         "\"Protecting American manufacturing is the America First agenda\" (posted to X)",
         policy_issues="Economy; Immigration",
         speech_summary="Husted repeated the 50-years attack and tied Kenworth's 1,000 added "
         "jobs to the America First agenda, per Cleveland.com.",
         transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 report retrieved: Cleveland.com, 2026-10-31",
         opponent_reference="yes — the 50-years line and the immigration question",
         visual_notes=U, source_urls=ref("b4_cle_clash"), verification_status="verified",
         analyst_notes="Venue not named in the retrieved report; only the city."),
    dict(candidate_id="HUSTED", event_date="2026-10-29", event_time=U,
         event_title="Republican Bus Tour rally at ACiQ",
         event_category="rally", city="Vandalia", venue="ACiQ", state_region="Southwest",
         event_status="held", campaign_phase="gotv",
         stated_purpose="Statewide bus tour stop in the Dayton media market",
         observable_function="tour stop mobilisation",
         analyst_interpretation="A bus tour in the final week is scheduling efficiency: "
         "several media markets in a day, each with a local-news hook.",
         target_audience="Montgomery County Republicans", main_messages="unknown",
         policy_issues="Economy", speech_summary="unknown — documented through a dated "
         "photograph caption only", transcript_url=U, video_url=U, photo_urls=U,
         media_coverage="1 photo caption retrieved: Columbus Dispatch via Yahoo, 2026-10-18",
         opponent_reference=U, visual_notes="Caption describes Husted speaking at the rally",
         source_urls=ref("b4_yahoo_keyissues"), verification_status="partially verified",
         analyst_notes="Same date and market as Brown's Dayton rally three days earlier — "
         "the two campaigns were contesting the same media market."),
    dict(candidate_id="HUSTED", event_date="2026-11-03", event_time=U,
         event_title="Concession after the Senate result", event_category="concession_speech",
         city=U, venue=U, state_region="statewide", event_status="held",
         campaign_phase="election_day", stated_purpose="Acknowledge the result",
         observable_function="result-acceptance",
         analyst_interpretation="The concession is documented as a video page (10TV) whose "
         "body could not be retrieved; this archive therefore records the fact of the "
         "concession without quoting it.",
         target_audience="supporters; press", main_messages="unknown",
         policy_issues="Democracy", speech_summary="unknown — the 10TV video page returned "
         "HTTP 403", transcript_url=U,
         video_url="https://www.10tv.com/video/news/politics/elections/"
                   "senator-jon-husted-loses-the-2026-midterm-election/"
                   "530-5a0af209-82f5-4d66-85f1-715e0bf37b2a",
         photo_urls=U, media_coverage="1 video page identified: 10TV (403 at retrieval)",
         opponent_reference=U, visual_notes=U, source_urls=ref("b4_wlwt_result"),
         verification_status="partially verified",
         analyst_notes="Video URL is recorded as a pointer, not as retrieved content; the "
         "WLWT result story is the cited source."),
]


def main():
    rows = []
    for i, e in enumerate(EVENTS, 1):
        r = dict(e)
        r["event_id"] = f"EV-{i:03d}"
        rows.append(r)
    write_csv("02_campaign_events/campaign_events.csv", FIELDS, rows)
    print("BROWN", sum(1 for r in rows if r["candidate_id"] == "BROWN"),
          "HUSTED", sum(1 for r in rows if r["candidate_id"] == "HUSTED"))


if __name__ == "__main__":
    main()
