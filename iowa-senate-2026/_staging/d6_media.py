# -*- coding: utf-8 -*-
"""advertisements.csv, social_media.csv, media_coverage.csv."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CASE, S, URL, KEY, write

ADH = ["ad_id", "candidate_id", "sponsor", "sponsor_type", "release_date", "title", "platform",
       "length_seconds", "issue_or_message", "main_visual_elements", "narration_soundtrack",
       "candidate_appearance", "main_claims", "video_url", "transcript_url", "fact_check",
       "media_coverage", "source_urls", "verification_status", "notes"]

ADS = [
    ["TUR-AD-0001", "TUREK", "Josh Turek for Iowa", "candidate_campaign", "2025-08-12", "Underdog",
     "online video", "unknown", "Biography and launch",
     "No visual description retrieved; the outlets describe the video as narrating his path to the Paralympics.",
     "unknown", "Turek appears and narrates in first person per the reported quotations",
     "That he was born with spina bifida, had 21 surgeries before 12, and won Paralympic gold in 2016 and 2020",
     "unknown", "unknown",
     "Biographical claims are corroborated by Wikipedia and by the campaign coverage; the 21-surgeries figure is the candidate's own.",
     "KCCI; Iowa Capital Dispatch", S("f080"), "partially verified",
     "Launch video rather than a persuasion spot; length and visuals not retrieved."],
    ["TUR-AD-0002", "TUREK", "Josh Turek for Iowa", "candidate_campaign", "2026-08-28", "I-35",
     "television and digital", "unknown", "Immigration and border security",
     "No visual description retrieved.", "unknown", "Turek speaks to camera in the reported script",
     "\"I'll work with anyone to fix it, including President Trump, to secure the border [and] stop the flow of drugs into Iowa\"; ties Interstate 35 to the southern border",
     "unknown", "unknown",
     "Hinson called the ad a misrepresentation and noted Turek's 2024 vote for Senate File 2340; a Turek spokesperson responded that Congress had failed to act.",
     "Iowa Capital Dispatch; KCCI", S("f103"), "verified",
     "Released on the Friday before the August 29 BBQ Bash, where Hinson attacked it."],
    ["TUR-AD-0003", "TUREK", "Josh Turek for Iowa", "candidate_campaign", "unknown",
     "Bipartisan record spot (\"over 700 times\")", "television and digital", "unknown",
     "Bipartisan voting record",
     "No visual description retrieved.", "unknown", "unknown",
     "That he \"voted with Republicans more than 700 times on issues including tax cuts and gun rights protections\"",
     "unknown", "unknown",
     "The 700 figure is the campaign's own count and was not independently checked here.",
     "KCCI", S("f082"), "partially verified",
     "Release date not stated in the retrieved report; grouped with the immigration spot as \"his latest ads\"."],
    ["TUR-AD-0004", "TUREK", "Josh Turek for Iowa", "candidate_campaign", "2026-07-29",
     "Obama endorsement video", "online video", "unknown", "Celebrity endorsement and biography",
     "Not described; the report says the two play basketball in the video.", "unknown",
     "Barack Obama and Turek appear together according to the report",
     "That Obama endorses Turek; no policy claim documented",
     "unknown", "unknown",
     "The endorsement itself is documented; the video's production and distribution are not.",
     "Associated Press (headline) and the encyclopedia entry", S("wiki"), "partially verified",
     "Endorsement video rather than a paid spot; whether it also ran as paid media is not established."],
    ["TUR-AD-0005", "TUREK", "Josh Turek for Iowa", "candidate_campaign", "2026-10-25",
     "Stop the Nonsense", "television and digital", "unknown", "Transgender policy and cost of living",
     "No visual description retrieved.", "unknown", "Turek speaks in the reported script",
     '''"As a kid in a wheelchair, I faced my share of bullying," Turek says in the ad. "That's why I believe that no Iowan should face discrimination. As a Paralympian, I also know it's important to have rules. It's why I oppose males competing in female sports, something that is already illegal in Iowa. I'm against taxpayers paying for sex changes too. Anyone tells you any different is lying."''',
     "unknown", "unknown",
     "One Iowa Action condemned the ad as a policy shift; Hinson and other Republicans said it misrepresented his record.",
     "Iowa Capital Dispatch", S("f201"), "verified",
     "Released on a Sunday; the report prints the ad's script verbatim and quotes both criticisms."],
    ["TUR-AD-0006", "TUREK", "Josh Turek for Iowa", "candidate_campaign", "2026-10-26",
     "Diesel prices ad", "television and digital", "unknown", "Fuel costs for farmers and truckers",
     "No details retrieved; the report only names the subject.", "unknown", "unknown",
     "No claim text retrieved.", "unknown", "unknown", "Not checked.",
     "Iowa Capital Dispatch (mention)", S("f201"), "partially verified",
     "Named in a single sentence as one of two ads released the day after the transgender ad."],
    ["TUR-AD-0007", "TUREK", "Josh Turek for Iowa", "candidate_campaign", "2026-10-26",
     "High health-care costs ad", "television and digital", "unknown", "Health-care costs",
     "No details retrieved; the report only names the subject.", "unknown", "unknown",
     "No claim text retrieved.", "unknown", "unknown", "Not checked.",
     "Iowa Capital Dispatch (mention)", S("f201"), "partially verified",
     "Named in a single sentence as one of two ads released the day after the transgender ad."],
    ["EXT-AD-0001", "HINSON", "Senate Leadership Fund", "outside_pac", "unknown",
     "unknown", "television", "unknown", "Pro-Hinson television buy",
     "No creative retrieved.", "unknown", "unknown",
     "A $20M boost to Hinson from a GOP super PAC, per the Des Moines Register headline",
     "unknown", "unknown",
     "The figure is headline-level only: the Des Moines Register returned HTTP 402 to the fetcher.",
     "The Des Moines Register (headline)", S("dmr_superpac"), "unverified",
     "Recorded separately from campaign receipts; not summed with FEC totals."],
    ["EXT-AD-0002", "HINSON", "Elon Musk's super PAC", "outside_pac", "unknown",
     "unknown", "digital", "unknown", "Pro-Republican digital advertising and voter registration",
     "No creative retrieved.", "unknown", "unknown",
     "Musk's super PAC began spending on digital ads in Senate battlegrounds; the Des Moines Register put total outside spending in the Iowa Senate race at $137M in its headline",
     "unknown", "unknown",
     "NBC reports the digital buy generically; the Iowa-specific total is headline-level from a paywalled page.",
     "NBC News; The Des Moines Register (headline)", S("f117"), "unverified",
     "No ad title, script or buy size for Iowa could be read."],
]
write("05_campaign_media/advertisements.csv", ADH, ADS)

SOCH = ["post_id", "candidate_id", "platform", "account_handle", "post_date", "post_type",
        "content_summary", "media_included", "engagement_notes", "url", "verification_status", "notes"]

SOC = [
    ["TUR-SOC-0001", "TUREK", "x", "unknown", "2025-08-12", "launch video link",
     "Campaign launch announcement pointing to the \"Underdog\" video.", "video link",
     "No engagement metrics retrieved.", URL[KEY["f080"]], "partially verified",
     "x.com blocked the fetcher (HTTP 403); the post is documented through Iowa Capital Dispatch's report of the launch."],
    ["TUR-SOC-0002", "TUREK", "campaign_website", "turek4iowa.com", "2026-10-29", "press release link",
     "\"ICYMI: 'Ashley Hinson, Who Said Millennials are \"Bad at Saving,\" Lived in a Half Million Dollar House Her Parents Bought Her in L.A.'\"",
     "link to release", "No engagement metrics; homepage placement only.", URL[KEY["f200"]], "partially verified",
     "Homepage snapshot 2026-11-18; the release itself was not opened."],
    ["TUR-SOC-0003", "TUREK", "campaign_website", "turek4iowa.com", "2026-10-29", "press release link",
     "\"RECAP: Iowa Veterans Condemn Hinson's Support of Further Escalation of War in Iran\"", "link to release",
     "No engagement metrics.", URL[KEY["f200"]], "partially verified", "Homepage snapshot 2026-11-18."],
    ["TUR-SOC-0004", "TUREK", "campaign_website", "turek4iowa.com", "2026-11-18", "homepage",
     "Site bio: \"two-time Paralympic gold medalist for Team USA and a State Legislator who represents the reddest seat held by a Democrat in the state of Iowa\"; born with spina bifida after his father's Agent Orange exposure; 21 surgeries before 12; four Paralympics.",
     "portrait and site graphics", "No engagement metrics.", URL[KEY["f200"]], "verified",
     "Text of the homepage as retrieved on the access date."],
    ["HIN-SOC-0001", "HINSON", "x", "unknown", "2025-09-02", "announcement post",
     "\"I'm all in. I'm running for the United States Senate to fight alongside President Trump and deliver on the America First agenda\"; \"From securing our border and deporting illegal aliens, to keeping men out of girl's sports and cutting taxes for working families...\"",
     "unknown", "No engagement metrics retrieved.", URL[KEY["f009"]], "verified",
     "Both sentences are quoted verbatim by NBC News from the post; the post URL itself was not retrieved."],
    ["HIN-SOC-0002", "HINSON", "campaign_website", "ashleyhinson.com", "2026-11-18", "homepage",
     "\"Ashley Hinson is a conservative mom on a mission to make Washington run more like the great state of Iowa. She is working alongside President Trump to secure our borders, cut wasteful spending, and put our country back on the path to prosperity.\"",
     "portrait and site graphics", "No engagement metrics.", URL[KEY["f198"]], "verified",
     "Text of the homepage as retrieved on the access date."],
    ["HIN-SOC-0003", "HINSON", "campaign_website", "ashleyhinson.com", "2026-11-18", "endorsement page",
     "\"Ashley has received President Trump's endorsement every election since 2020\", followed by the 2025 endorsement quotation.",
     "unknown", "No engagement metrics.", URL[KEY["f198"]], "verified",
     "Homepage snapshot; the linked endorsement page was not opened."],
]
write("05_campaign_media/social_media.csv", SOCH, SOC)

COVH = ["coverage_id", "candidate_id", "event_id", "publication_date", "outlet", "author", "title",
        "url", "source_tier", "coverage_type", "key_framing", "notable_quotes",
        "framing_of_candidate", "mentions_opponent", "reliability_notes"]


def cov(cid, eid, date, outlet, author, title, src, tier, typ, framing, quotes, fcand, opp, notes):
    n = len(C + 1) if False else len(C) + 1
    C.append(["COV-%04d" % n, cid, eid, date, outlet, author, title, URL[KEY[src]], tier, typ,
              framing, quotes, fcand, opp, notes])


C = []
cov("TUREK", "TUR-EVT-0001", "2025-08-12", "Iowa Capital Dispatch", "Robin Opsahl",
    "Iowa Rep. Josh Turek, two-time Paralympian, launches campaign for U.S. Senate", "f080", "T2",
    "news_report", "Launch framed through the Paralympic biography and public services his family used.",
    "\"I knew nothing would come easy, but I never doubted my right to the American dream.\"",
    "Sympathetic, biography-led", "yes", "Full text retrieved.")
cov("TUREK", "TUR-EVT-0001", "2025-08-12", "KCCI", "Robin Opsahl (Iowa Capital Dispatch)",
    "Iowa Rep. Josh Turek, two-time Paralympian, launches campaign for U.S. Senate", "f036", "T2",
    "news_report", "Same wire story, local-TV framing; notes he is the fifth Democratic candidate.",
    "\"I'm Josh Turek...\" video narration quoted", "Biography-led, neutral", "yes", "Syndicated copy of the ICD report.")
cov("HINSON", "HIN-EVT-0001", "2025-09-02", "NBC News", "Zoë Richards",
    "GOP Rep. Ashley Hinson announces Senate bid for open Iowa seat", "f009", "T2", "news_report",
    "Announcement framed as immediate consolidation behind Trump's agenda.",
    "\"I'm all in. I'm running for the United States Senate to fight alongside President Trump...\"",
    "Straight news, quote-led", "yes", "Full text retrieved.")
cov("HINSON", "HIN-EVT-0001", "2025-09-02", "Fox News", "Paul Steinhauser",
    "Republican rising star Ashley Hinson announces Senate bid in race to succeed Iowa's Ernst", "f020", "T2",
    "news_report", "Frames Hinson as the establishment favourite and lists the Democratic field.",
    "Ernst's \"make 'em squeal\" history quoted at length",
    "Positive, 'rising star' framing", "yes", "Full text retrieved.")
cov("HINSON", "HIN-EVT-0001", "2025-09-07", "Bleeding Heartland", "Laura Belin",
    "Ashley Hinson's Senate rollout: Short-term success, long-term risks", "f018", "T3", "analysis",
    "Argues the rollout was operationally strong but left her exposed on abortion and Planned Parenthood funding.",
    "\"She did claim to support access to non-abortion services at that time, but subsequently voted to take numerous funding streams away...\"",
    "Critical", "yes", "Partisan-leaning blog; used only for documented votes and process detail.")
cov("HINSON", "HIN-EVT-0005", "2026-08-29", "Iowa Capital Dispatch", "Robin Opsahl",
    "Sen. Ted Cruz criticizes Democrats as 'Marxists and Islamists' at Hinson event in Iowa", "f103", "T2",
    "news_report", "Cruz's keynote dominates; Hinson's own remarks appear only as an attack on Turek's ad.",
    "\"I'd laugh too if it wasn't so egregious, right?\"; \"the tale of two Tureks\"",
    "Event coverage; Hinson quoted critically of Turek", "yes", "Full text retrieved.")
cov("TUREK", "TUR-EVT-0003", "2026-08-29", "Iowa Capital Dispatch", "Robin Opsahl",
    "Iowa Democratic candidates push for term limits at Polk County Steak Fry", "f130", "T2", "news_report",
    "Frames the Steak Fry as a Democratic show of force with Whitehouse as the surrogate.",
    "\"And really, Iowa, we have hit the bottom.\"", "Sympathetic, rally-style", "yes", "Full text retrieved.")
cov("TUREK", "TUR-EVT-0004", "2026-09-09", "Iowa Capital Dispatch", "unknown",
    "Turek pledges to protect Social Security at Scottish Rite Park", "f124", "T2", "news_report",
    "Frames the event as an endorsement opportunity and a Social Security contrast.",
    "\"I give each and every Iowa senior my pledge...\"", "Sympathetic", "yes",
    "Full text retrieved; the headline in the archive copy is the site's own.")
cov("HINSON", "HIN-EVT-0003", "2026-07-25", "Iowa Capital Dispatch", "Robin Opsahl",
    "Sen. Ted Cruz calls for regulating kids' use of AI chatbots at Hinson campaign event", "f107", "T2",
    "news_report", "Cruz again carries the policy argument; Hinson is the host, not the speaker.",
    "Cruz on the TAKE IT DOWN Act", "Neutral", "yes", "Full text retrieved.")
cov("HINSON", "HIN-EVT-0007", "2026-09-19", "Iowa Capital Dispatch", "Robin Opsahl",
    "Hinson, Sen. John Barrasso of Wyoming highlight GOP tips, overtime tax cuts", "f106", "T2",
    "news_report", "Affordability answered with worker testimony about the OBBBA tax cuts.",
    "Jacob Carnes on keeping overtime pay", "Neutral-positive", "yes", "Full text retrieved.")
cov("HINSON", "HIN-EVT-0008", "2026-09-19", "Iowa Capital Dispatch", "Robin Opsahl",
    "US Sen. John Kennedy, in Iowa, predicts end of Iran war in 6 months", "f108", "T2", "news_report",
    "Surrogate endorses Hinson at a 1,300-person Christian fundraiser.",
    "Kennedy on inflation and the Iran war", "Neutral", "yes", "Full text retrieved.")
cov("HINSON", "HIN-EVT-0010", "2026-10-13", "The Gazette", "Hailey Peck",
    "Border Patrol union endorses Ashley Hinson for U.S. Senate", "f116", "T2", "news_report",
    "Endorsement framed around border security and law enforcement.",
    "\"Iowans deserve safe and secure communities.\"", "Neutral-positive", "no",
    "Full text retrieved; photo credit Iowa Capital Dispatch.")
cov("TUREK", "JNT-EVT-0001", "2026-10-07", "Newsweek", "Jason Lemon; Anna Commander",
    "Turek, Hinson Clash in Iowa US Senate Debate: Key Moments, Polls", "f085", "T2", "news_report",
    "Debate framed as a clash over tariffs, data centers and voting records.",
    "\"I am absolutely in favor of some regulations on data centers.\"", "Balanced", "yes",
    "Full text retrieved.")
cov("TUREK", "JNT-EVT-0001", "2026-10-07", "PBS NewsHour", "unknown",
    "WATCH: U.S. Senate candidates Hinson, Turek debate in Iowa", "f193", "T2", "news_video",
    "Livestream page; the debate is the record, not the report.",
    "none - video page", "Neutral", "yes", "Player only; not viewed.")
cov("TUREK", "JNT-EVT-0002", "2026-10-13", "The Daily Iowan", "Anna Olson",
    "Hinson, Turek debate farms, Iowa data centers in last debate", "f077", "T2", "news_report",
    "Frames the final debate around agriculture, tariffs and data-center oversight.",
    "\"Our farmers rely on open markets and free trade more than any other group.\"", "Balanced", "yes",
    "Full text retrieved; AP contributed.")
cov("TUREK", "TUR-EVT-0006", "2026-10-15", "The Daily Iowan", "unknown",
    "Andy Kim rallies UI students, community for final early voting push", "f128", "T2", "news_report",
    "Surrogate-led GOTV framing; Turek is not the subject of the report.",
    "Kim on the Senate majority", "Neutral", "yes", "Full text retrieved.")
cov("TUREK", "unknown", "2026-09-09", "KCCI", "Amanda Rooker",
    "Why Republican themes are showing up in some Iowa Democrats' ads", "f082", "T2", "analysis",
    "Analyses Democratic ads that borrow Republican themes; quotes Turek's ad scripts and his interview.",
    "\"We need to have safe and secure borders. We do.\"", "Analytical, mildly critical", "yes",
    "Full text retrieved.")
cov("TUREK", "TUR-EVT-0018", "2026-10-26", "Iowa Capital Dispatch", "Robin Opsahl",
    "Josh Turek ad on transgender issues draws bipartisan criticism", "f201", "T2", "news_report",
    "Frames the ad as a break with Democratic orthodoxy, with criticism from an LGBTQ+ group and from Republicans.",
    '''One Iowa Action: "we unequivocally condemn Josh Turek's recently released campaign ad and the policy shift it represents."''',
    "Critical on this issue, otherwise neutral", "yes",
    "Full text retrieved; prints the ad script verbatim and names two further ads.")
cov("TUREK", "unknown", "2026-08-13", "Iowa Capital Dispatch", "Robin Opsahl",
    "Sen. Mark Kelly calls for Iowans to elect Democrats so Congress can investigate Trump 'corruption'", "f127", "T2",
    "news_report", "Wing Ding coverage centred on Kelly; no Turek remarks retrieved.",
    "Kelly: \"I know what happens when you speak truth to this administration\"", "Neutral", "yes",
    "Full text retrieved.")
cov("HINSON", "HIN-EVT-0011", "2026-10-19", "The Gazette", "unknown",
    "Iowa's Hinson endorsed by former primary challenger, critic", "f112", "T2", "news_report",
    "Frames the endorsement as closing the primary wound.",
    "Carlin: \"I am proud to endorse Hinson\"", "Neutral", "yes", "Full text retrieved.")
cov("HINSON", "unknown", "2026-06-16", "KGAN (CBS2 Iowa)", "Ray Baccari",
    "Jim Carlin tells supporters not to support Ashley Hinson in Senate race", "f149", "T2", "news_report",
    "Post-primary intraparty refusal, framed around values.",
    "Carlin: Hinson \"does not share our values\"", "Critical of Hinson (via Carlin)", "yes",
    "Full text retrieved.")
cov("TUREK", "unknown", "2026-11-04", "KMSP-TV (FOX 9)", "Ashleigh Jackson",
    "Iowa elections: Democrats flip seats, see who won key races", "f001", "T2", "news_report",
    "Result framing: Turek's win as part of a statewide Democratic swing.",
    "\"Democrat Josh Turek defeated Republican Ashley Hinson, flipping the seat...\"", "Neutral", "yes",
    "Full text retrieved.")
cov("TUREK", "unknown", "2026-11-03", "ABC News", "unknown",
    "How Democrats flipped the Senate blue: The ABC News Voter Poll tells the story", "f195", "T2", "analysis",
    "Exit-poll framing: one in ten 2024 Trump voters backed Turek.",
    "\"One in 10 voters who said they backed Trump in 2024 crossed over...\"", "Analytical", "yes",
    "Full text retrieved.")
cov("HINSON", "unknown", "2026-10-01", "Fox News", "unknown",
    "Fox News poll shows Josh Turek leading Rep. Ashley Hinson in Iowa", "f173", "T2", "news_report",
    "Poll report; the outlet's own poll had Turek ahead.",
    "none retrieved in the archived copy", "Neutral", "yes", "Poll page retrieved; toplines in polling.csv.")
cov("HINSON", "unknown", "2026-11-18", "The Des Moines Register", "unknown",
    "Ashley Hinson gets $20M boost from GOP super PAC in Iowa Senate race", "dmr_superpac", "T2",
    "news_report", "Outside-money framing.",
    "headline only", "Neutral", "yes", "HTTP 402 paywall; headline only.")
cov("TUREK", "unknown", "2026-10-30", "The New York Times", "Bayliss Wagner",
    "Democrats, Hopeful All Over the Senate Map, Remain Jittery About Iowa", "nyt_iowa", "T2", "analysis",
    "National framing: Iowa as a race Democrats feared losing.",
    "headline only", "Neutral", "yes", "Blocked by nytimes.com; headline only.")
cov("TUREK", "unknown", "2026-10-21", "The Gazette", "Editorial board",
    "Opinion: Iowa should send Josh Turek to the U.S. Senate", "f147", "T2", "op_ed",
    "Endorsement editorial.",
    "headline only in the archived copy", "Positive", "yes", "Editorial; opinion content.")
cov("HINSON", "unknown", "2026-10-20", "Voice of America", "Lin Feng",
    "From Soybeans to Data Centers, China Debate Hits US Midterm Campaigns", "f086", "T2", "news_report",
    "Frames both candidates' China positioning.",
    "Hinson: \"if we don't, China will\"", "Neutral", "yes", "Full text retrieved.")
cov("TUREK", "unknown", "2025-05-31", "NPR", "unknown",
    "'We all are going to die': Sen. Ernst response to grilling on Medicaid", "f006", "T2", "news_report",
    "Background: the town-hall line that framed the Medicaid debate both candidates inherited.",
    "\"Well, we all are going to die\"", "Neutral (about Ernst)", "no",
    "Full text retrieved; not a Turek or Hinson appearance.")

write("05_campaign_media/media_coverage.csv", COVH, C)
print("coverage rows:", len(C))
