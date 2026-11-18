# -*- coding: utf-8 -*-
"""speeches, videos, images, ads, social media, press coverage."""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(HERE)
SRC = {r['source_id']: r['url'] for r in csv.DictReader(open(os.path.join(CASE, '09_sources', 'sources.csv'), encoding='utf-8'))}


def s(i):
    return '%s|%s' % (i, SRC[i])


def W(rel, header, rows):
    p = os.path.join(CASE, rel)
    with open(p, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(header)
        for r in rows:
            assert len(r) == len(header), (rel, r[0], len(r), len(header))
            w.writerow(r)
    print('%-44s %3d rows' % (rel, len(rows)))


# ---------------- speech archive
SH = ['speech_id', 'candidate_id', 'event_id', 'date', 'speech_title', 'speech_url', 'transcript_url',
      'duration', 'main_topics', 'major_quotes', 'rhetorical_devices', 'opponent_references',
      'personal_story_elements', 'policy_claims', 'source_urls', 'source', 'verification_status']
SP = [
 ['OSS-SPC-01', 'OSSOFF', 'OSS-EVT-002', '2026-02-07', 'Atlanta rally speech: "the first light of dawn"',
  'unknown', 'unknown', 'approximately 30 minutes', 'Democracy; cost of living; health care; immigration enforcement',
  '"It feels like every day the depravity deepens"; "the first light of dawn is on the horizon"; "we will overcome this together"',
  'Anaphora ("maybe you fear ..."); direct address to the crowd; closing crescendo',
  'Donald Trump; national Republicans', 'References to Georgia families and rural clinic closures',
  'Says Republicans cut taxes for the rich and closed rural clinics; promises to protect coverage',
  s('SRC-0019'), 'Georgia Recorder report of the speech', 'verified'],
 ['OSS-SPC-02', 'OSSOFF', 'OSS-EVT-004', '2026-06-27', 'Savannah joint rally remarks',
  'unknown', 'unknown', 'unknown', 'Unity; Trump; affordability',
  '"Toys out the stroller"; "we are united for Georgia"',
  'Late-night-monologue structure (three-item Trump list); rolled-up sleeves as a visual cue',
  'Donald Trump; Rick Jackson', 'unknown', 'unknown', s('SRC-0018'), 'Georgia Recorder report', 'verified'],
 ['OSS-SPC-03', 'OSSOFF', 'OSS-EVT-007', '2026-10-08', 'First Senate debate remarks',
  'https://www.youtube.com/watch?v=FDCQ7-OivEM', 'unknown', 'about 60 minutes', 'Tariffs; health care; Iran war; Collins associates',
  '"You\'re not just lying about my record. You\'re lying about a young woman\'s death"; "These tariffs are crushing our state"',
  'Direct accusation; repetition of "lying"; use of a victim\'s name',
  'Mike Collins', 'unknown', 'Tariff repeal; ACA defence; Iran war criticism', s('SRC-0016'), 'Georgia Recorder report', 'verified'],
 ['OSS-SPC-04', 'OSSOFF', 'OSS-EVT-008', '2026-10-13', 'Second debate remarks',
  'unknown', 'unknown', 'unknown', 'Immigration; Epstein; ethics investigation',
  '"You brought dishonor ..."; "Mike, you know I voted for the bill"',
  'Interruption and rebuttal; use of the opponent\'s first name', 'Mike Collins',
  'unknown', 'Defends his Laken Riley Act vote; attacks Collins\'s associates', s('SRC-0017'), 'Georgia Recorder report', 'verified'],
 ['OSS-SPC-05', 'OSSOFF', 'OSS-EVT-010', '2026-10-29', 'Remarks at Atlanta HBCU gathering',
  'unknown', 'unknown', 'unknown', 'Young-voter turnout; democracy',
  '"have already shattered every turnout record for young voters"',
  'Direct address to students; call-and-response', 'Mike Collins', 'unknown', 'unknown', s('SRC-0024'),
  'Georgia Recorder report', 'partially verified'],
 ['OSS-SPC-06', 'OSSOFF', 'OSS-EVT-013', '2026-11-03', 'Victory speech',
  'unknown', 'unknown', 'unknown', 'Justice and progress; unity; health care; affordability; civil rights',
  '"Tonight, we\'ve struck a necessary and undeniable blow on behalf of justice and progress"; "to every Georgian ... I will never stop fighting for you"',
  'Triadic lists; the phrase "justice and progress" repeated; thanks to family and to Bottoms before policy',
  'Donald Trump', 'Thanks his wife and daughters; mentions Bottoms\'s campaign',
  'Promises to protect coverage, lower costs and defend voting rights', s('SRC-0004'), 'Georgia Recorder report', 'verified'],

 ['COL-SPC-01', 'COLLINS', 'COL-EVT-002', '2025-08-19', 'Campaign kickoff rally speech',
  'unknown', 'unknown', 'unknown', 'Trump; immigration; the Laken Riley Act',
  '"With President Trump in the White House and me in the U.S. Senate, the hardworking men and women of this country will not be forgotten anymore"',
  'Plain-spoken populist register; local naming (Butts County); religious framing from the opening pastor',
  'Jon Ossoff', 'Speaks about his trucking business and his family', 'Immigration enforcement; the Laken Riley Act',
  s('SRC-0014'), 'Georgia Public Broadcasting report', 'verified'],
 ['COL-SPC-02', 'COLLINS', 'COL-EVT-008', '2026-06-16', 'Runoff victory remarks',
  'unknown', 'unknown', 'unknown', 'Party unity; defeating Ossoff',
  '"stand united around one mission ... get rid of that Jon Ossoff"',
  'Thank-yous to defeated rivals; repetition of "united"', 'Jon Ossoff; Derek Dooley',
  'Thanks his family and Dooley', 'unknown', s('SRC-0020'), 'Georgia Recorder report', 'verified'],
 ['COL-SPC-03', 'COLLINS', 'COL-EVT-016', '2026-10-16', 'Dalton rally remarks with Trump',
  'unknown', 'unknown', 'unknown', 'Trump; turnout; 2020 election claims',
  '"thank you for your leadership, your backbone"',
  'Direct praise of the president; short declaratives', 'Jon Ossoff', 'unknown',
  'Says Georgia is "red" and that voters must turn out', s('SRC-0023'), 'Georgia Recorder report', 'verified'],
 ['COL-SPC-04', 'COLLINS', 'COL-EVT-014', '2026-10-08', 'First Senate debate remarks',
  'https://www.youtube.com/watch?v=FDCQ7-OivEM', 'unknown', 'about 60 minutes', 'Border; fentanyl; Ossoff\'s biography',
  '"a trust fund kid who\'s never had a job in his life"; "He wanted to keep the borders wide open"',
  'Class-based attack; repetition of "wide open"', 'Jon Ossoff', 'Talks about his trucking company and creating jobs',
  'Claims Ossoff voted to keep borders open', s('SRC-0016'), 'Georgia Recorder report', 'verified'],
 ['COL-SPC-05', 'COLLINS', 'COL-EVT-015', '2026-10-13', 'Second debate remarks',
  'unknown', 'unknown', 'unknown', 'Georgia vs Georgetown; jobs; immigration; ethics',
  '"This is a race between Georgia and Georgetown"',
  'Geographic antithesis; plain-language self-presentation', 'Jon Ossoff',
  'Mentions his family and his business', 'unknown', s('SRC-0017'), 'Georgia Recorder report', 'verified'],
 ['COL-SPC-06', 'COLLINS', 'COL-EVT-010', '2026-08-11', 'Savannah breakfast Q&A answer on Jan. 6 compensation',
  'unknown', 'unknown', 'unknown', 'Jan. 6; "weaponization" of government',
  '"when the federal government harms you, then yes, they have a liability to you. That\'s easy, yes sir."',
  'Conversational register; direct address ("yes sir")', 'Jon Ossoff', 'unknown',
  'Suggests a compensation mechanism for Jan. 6 defendants', s('SRC-0029'), 'Georgia Recorder report', 'verified'],
 ['COL-SPC-07', 'COLLINS', 'COL-EVT-017', '2026-11-03', 'Concession remarks',
  'unknown', 'unknown', 'unknown', 'Service; faith; the president',
  '"It\'s been an honor ... to serve under the leadership of the best president in my lifetime"; "the results may not be what we wanted tonight, but y\'all, that\'s okay."',
  'Southern vernacular ("y\'all"); religious closure', 'Jon Ossoff',
  'Thanks family and staff; invokes the "good Lord"', 'unknown', s('SRC-0004'), 'Georgia Recorder report; C-SPAN frame', 'verified'],
]
W('03_speeches/speech_archive.csv', SH, SP)

# ---------------- video index
VH = ['video_id', 'candidate_id', 'video_url', 'date', 'duration', 'event_type', 'main_topics',
      'relevant_timestamps', 'transcript_available', 'visual_observations', 'completeness',
      'source_urls', 'verification_status']
VD = [
 ['OSS-VID-01', 'OSSOFF', 'https://www.youtube.com/watch?v=FDCQ7-OivEM', '2026-10-08', 'about 60 minutes',
  'debate', 'Tariffs; health care; Iran; Collins associates', 'unknown', 'no',
  'Two-shot studio debate, graphics lower-thirds, both candidates standing at podiums', 'full', s('SRC-0016'), 'verified'],
 ['COL-VID-01', 'COLLINS', 'https://www.youtube.com/watch?v=FDCQ7-OivEM', '2026-10-08', 'about 60 minutes',
  'debate', 'Border; fentanyl; Ossoff biography', 'unknown', 'no', 'Same broadcast; Collins at right-hand podium', 'full',
  s('SRC-0016'), 'verified'],
 ['OSS-VID-02', 'OSSOFF', 'unknown', '2026-11-03', '4 minutes 26 seconds', 'victory_speech',
  'Victory; justice and progress', 'unknown', 'no', 'Evening stage, supporters behind, broadcast lower-third',
  'clip', s('SRC-0004'), 'partially verified'],
 ['COL-VID-02', 'COLLINS', 'unknown', '2026-11-03', 'unknown', 'concession_speech', 'Concession; faith; service',
  'unknown', 'no', 'Headquarters crowd, C-SPAN pool frame', 'clip', s('SRC-0098'), 'partially verified'],
 ['OSS-VID-03', 'OSSOFF', 'unknown', '2026-02-07', 'unknown', 'rally', 'Democracy; cost of living', 'unknown', 'no',
  'Indoor convention-centre rally; crowd behind the speaker', 'clip', s('SRC-0019'), 'partially verified'],
 ['OSS-VID-04', 'OSSOFF', 'unknown', '2026-06-27', 'unknown', 'rally', 'Unity; Trump', 'unknown', 'no',
  'Teleprompter visible in wide shots; produced signage; sleeves rolled up', 'clip', s('SRC-0018'), 'partially verified'],
 ['COL-VID-03', 'COLLINS', 'unknown', '2025-11-12', 'unknown', 'advertisement', 'Shutdown; Ossoff', 'unknown', 'no',
  'AI-generated likeness of Ossoff; digital-only release', 'clip', s('SRC-0092'), 'partially verified'],
 ['COL-VID-04', 'COLLINS', 'unknown', '2026-06-16', 'unknown', 'victory_speech', 'Runoff win; unity', 'unknown', 'no',
  'Historic-home setting, outdoor evening lighting', 'clip', s('SRC-0020'), 'partially verified'],
 ['OSS-VID-05', 'OSSOFF', 'unknown', '2026-10-13', 'unknown', 'debate', 'Immigration; Epstein; ethics', 'unknown', 'no',
  'GPB studio, pool cameras', 'clip', s('SRC-0017'), 'partially verified'],
 ['COL-VID-05', 'COLLINS', 'unknown', '2026-10-16', 'unknown', 'rally', 'Trump; turnout', 'unknown', 'no',
  'Outdoor rally stage with Trump', 'clip', s('SRC-0023'), 'partially verified'],
]
W('03_speeches/speech_video_index.csv', VH, VD)

# ---------------- images
IH = ['image_id', 'candidate_id', 'image_date', 'event_id', 'event_category', 'source_name', 'source_url',
      'original_image_url', 'photographer', 'copyright_status', 'license', 'local_filename',
      'image_resolution', 'framing', 'camera_angle', 'image_quality', 'face_visibility', 'body_visibility',
      'clothing_notes', 'notes', 'verification_status']
BASE = 'https://commons.wikimedia.org/wiki/Special:FilePath/'
IM = [
 ['OSS-IMG-01', 'OSSOFF', '2021-04-22', 'unknown', 'portrait', 'Wikimedia Commons / U.S. Senate',
  'https://commons.wikimedia.org/wiki/File:Jon_Ossoff_Senate_Portrait_2021_(cropped).jpg',
  BASE + 'Jon_Ossoff_Senate_Portrait_2021_%28cropped%29.jpg?width=1400', 'U.S. Senate Photographic Studio',
  'public_domain', 'Public domain (U.S. Senate)', '04_visual_archive/ossoff/OSSOFF-portrait-2021.jpg', '1400x1852',
  'head and shoulders', 'eye level', 'high', 'full', 'head and shoulders', 'dark suit, white shirt, blue tie',
  'Official portrait; downloaded at 1400 px wide, 792 KB.', 'verified'],
 ['OSS-IMG-02', 'OSSOFF', '2023-02-01', 'unknown', 'community_visit', 'Wikimedia Commons / Georgia Peanut Commission',
  'https://commons.wikimedia.org/wiki/File:2023_Peanut_Leadership_Academy_with_Jon_Ossoff_01.jpg',
  BASE + '2023_Peanut_Leadership_Academy_with_Jon_Ossoff_01.jpg?width=1600', 'Georgia Peanut Commission',
  'licensed', 'CC BY 2.0', '04_visual_archive/OSSOFF-peanut-academy-2023.jpg', '1600x1064',
  'group shot', 'eye level', 'high', 'full', 'full', 'dark suit among casual farm wear',
  'Agriculture constituency image; attribution required (CC BY 2.0).', 'verified'],
 ['COL-IMG-01', 'COLLINS', '2023-01-03', 'unknown', 'portrait', 'Wikimedia Commons / U.S. Congress',
  'https://commons.wikimedia.org/wiki/File:Rep._Mike_Collins_official_photo,_118th_Congress.jpg',
  BASE + 'Rep._Mike_Collins_official_photo%2C_118th_Congress.jpg?width=1200', 'United States Congress',
  'public_domain', 'Public domain (U.S. Congress)', '04_visual_archive/collins/COLLINS-portrait-2023.jpg', '1200x1500',
  'head and shoulders', 'eye level', 'high', 'full', 'head and shoulders', 'dark suit, red tie, flag pin',
  'Official House portrait; downloaded at 1200 px wide, 582 KB.', 'verified'],
 ['COL-IMG-02', 'COLLINS', '2026-11-03', 'COL-EVT-017', 'concession_speech', 'Wikimedia Commons / C-SPAN',
  'https://commons.wikimedia.org/wiki/File:U.S._Senate_Candidate_Mike_Collins_Concedes_U.S._Senate_Race_in_Georgia.jpg',
  BASE + 'U.S._Senate_Candidate_Mike_Collins_Concedes_U.S._Senate_Race_in_Georgia.jpg', 'C-SPAN',
  'public_domain', 'Public domain (C-SPAN)', '04_visual_archive/collins/COLLINS-concede-2026.jpg', '1280x720',
  'medium shot at lectern', 'slightly low', 'broadcast', 'full', 'torso', 'dark suit, light shirt, no tie visible',
  'C-SPAN frame of the concession; the only 2026 event image available under an open licence.', 'verified'],
 ['OSS-IMG-03', 'OSSOFF', '2026-06-27', 'OSS-EVT-004', 'rally', 'Georgia Recorder',
  'https://georgiarecorder.com/2026/06/28/ossoff-bottoms-declare-united-for-georgia-at-joint-campaign-rally/',
  'unknown', 'unknown', 'all_rights_reserved_link_only', 'unknown', 'unknown', 'unknown',
  'unknown', 'unknown', 'unknown', 'unknown', 'unknown', 'sleeves rolled up at the podium',
  'Link-only; not downloaded. Staging details from the reporter text.', 'partially verified'],
 ['OSS-IMG-04', 'OSSOFF', '2026-10-28', 'OSS-EVT-009', 'rally', 'Georgia Recorder',
  'https://georgiarecorder.com/2026/11/03/u-s-sen-jon-ossoff-wins-reelection-in-georgia/',
  'unknown', 'Alander Rocha', 'all_rights_reserved_link_only', 'unknown', 'unknown', 'unknown',
  'unknown', 'unknown', 'unknown', 'unknown', 'unknown', 'stage rally with Obama',
  'Link-only; photographer credited in the caption.', 'partially verified'],
 ['OSS-IMG-05', 'OSSOFF', '2026-10-13', 'OSS-EVT-012', 'early_voting_event', 'Georgia Recorder',
  'https://georgiarecorder.com/2026/10/15/ossoff-reports-raising-another-33-million-for-homestretch-of-u-s-senate-reelection-bid/',
  'unknown', 'Maya Homan', 'all_rights_reserved_link_only', 'unknown', 'unknown', 'unknown',
  'unknown', 'unknown', 'unknown', 'unknown', 'unknown', 'casual, voting-booth setting',
  'Link-only; the caption records the venue and date.', 'partially verified'],
 ['COL-IMG-03', 'COLLINS', '2026-09-25', 'COL-EVT-012', 'press_conference', 'Georgia Recorder / GPB',
  'https://georgiarecorder.com/2026/09/25/thune-stumps-for-collins-in-atlanta-as-national-gop-writes-off-governors-race/',
  'unknown', 'Ross Williams', 'all_rights_reserved_link_only', 'unknown', 'unknown', 'unknown', 'unknown',
  'unknown', 'unknown', 'unknown', 'unknown', 'cafe table, reporters around',
  'Link-only.', 'partially verified'],
 ['COL-IMG-04', 'COLLINS', '2026-10-16', 'COL-EVT-016', 'rally', 'Georgia Recorder',
  'https://georgiarecorder.com/2026/10/17/trump-rallies-north-georgia-republicans-as-early-voting-begins/',
  'unknown', 'unknown', 'all_rights_reserved_link_only', 'unknown', 'unknown', 'unknown', 'unknown',
  'unknown', 'unknown', 'unknown', 'unknown', 'outdoor rally stage',
  'Link-only.', 'partially verified'],
 ['COL-IMG-05', 'COLLINS', '2026-10-13', 'COL-EVT-015', 'debate', 'Georgia Recorder / AJC',
  'https://georgiarecorder.com/2026/10/13/collins-ossoff-trade-jabs-over-immigration-iran-and-epstein-in-second-debate/',
  'unknown', 'Miguel Martinez', 'all_rights_reserved_link_only', 'unknown', 'unknown', 'unknown', 'unknown',
  'unknown', 'unknown', 'unknown', 'unknown', 'pool photo, studio debate',
  'Link-only; pool photographer credited.', 'partially verified'],
 ['OSS-IMG-06', 'OSSOFF', '2026-08-05', 'OSS-EVT-006', 'debate_invitation', 'Atlanta News First',  'https://www.atlantanewsfirst.com/2026/08/05/atlanta-news-first-host-exclusive-georgia-us-senate-debate-between-jon-ossoff-mike-collins/',
  'unknown', 'unknown', 'all_rights_reserved_link_only', 'unknown', 'unknown', 'unknown', 'unknown',
  'unknown', 'unknown', 'unknown', 'unknown', 'station branding, debate announcement graphic',
  'Link-only; announcement graphic.', 'partially verified'],
 ['OSS-IMG-07', 'OSSOFF', '2026-02-07', 'OSS-EVT-002', 'rally', 'Georgia Recorder',
  'https://georgiarecorder.com/2026/02/07/ossoff-kicks-off-reelection-bid-with-fiery-speech-in-atlanta/',
  'unknown', 'unknown', 'all_rights_reserved_link_only', 'unknown', 'unknown', 'unknown', 'unknown',
  'unknown', 'unknown', 'unknown', 'unknown', 'indoor rally, crowd behind the speaker',
  'Link-only; used to document the staging of the February rally.', 'partially verified'],
]
W('04_visual_archive/image_archive.csv', IH, IM)

# ---------------- advertisements
AH = ['ad_id', 'candidate_id', 'sponsor', 'sponsor_type', 'release_date', 'title', 'platform',
      'length_seconds', 'issue_or_message', 'main_visual_elements', 'narration_soundtrack',
      'candidate_appearance', 'main_claims', 'video_url', 'transcript_url', 'fact_check',
      'media_coverage', 'source_urls', 'verification_status', 'notes']
AD = [
 ['OSS-AD-01', 'OSSOFF', 'Jon Ossoff for Georgia', 'candidate_campaign', '2026-07-14', 'Epstein files ad',
  'unknown', 'unknown', 'Collins and the Epstein files', 'unknown', 'unknown', 'unknown',
  'Links Collins to the Epstein files release fight', 'unknown', 'unknown', 'unknown', 'AJC',
  s('SRC-0050'), 'partially verified', 'Only the AJC headline and framing are readable; no creative described.'],
 ['COL-AD-01', 'COLLINS', 'Mike Collins for Senate', 'candidate_campaign', '2025-11-12', 'AI-generated Ossoff video',
  'digital', 'unknown', 'Government shutdown; Ossoff', 'AI-generated likeness of Ossoff', 'unknown', 'no',
  'Portrays Ossoff as responsible for the shutdown', 'unknown', 'unknown', 'unknown', 'Access WDUN',
  s('SRC-0092'), 'partially verified', 'Synthetic media; no disclosure label documented in the source.'],
 ['COL-AD-02', 'COLLINS', 'Senate Leadership Fund', 'outside_pac', '2026-09-25', 'Anti-Ossoff TV buy',
  'television', 'unknown', 'Ossoff\'s record', 'unknown', 'unknown', 'unknown', 'unknown', 'unknown', 'unknown',
  'unknown', 'Georgia Recorder', s('SRC-0022'), 'partially verified', 'A $1.7 million weekly buy, not a single ad.'],
 ['COL-AD-03', 'COLLINS', 'One Nation / Senate Leadership Fund', 'outside_pac', '2026-09-25', 'Cumulative Georgia buy',
  'television', 'unknown', 'Ossoff\'s record', 'unknown', 'unknown', 'unknown',
  '$25.9 million spent plus $17.3 million reserved', 'unknown', 'unknown', 'unknown', 'Georgia Recorder',
  s('SRC-0022'), 'partially verified', 'Group-level spending, not a creative.'],
 ['COL-AD-04', 'COLLINS', 'National Republican Senatorial Committee', 'party_committee', '2026-04-01',
  'NRSC million-dollar ad buys', 'television', 'unknown', 'Ossoff\'s record', 'unknown', 'unknown', 'unknown',
  'unknown', 'unknown', 'unknown', 'unknown', 'Georgia Recorder', s('SRC-0017'), 'partially verified',
  'Mentioned in passing; no dates or creative details.'],
 ['OSS-AD-02', 'OSSOFF', 'Jon Ossoff for Georgia', 'candidate_campaign', '2026-10-15', 'Closing TV and GOTV programme',
  'television', 'unknown', 'Turnout and affordability', 'unknown', 'unknown', 'yes',
  'Plans to spend the remaining $26 million on TV and voter contact', 'unknown', 'unknown', 'unknown',
  'Georgia Recorder', s('SRC-0033'), 'partially verified', 'A buy programme, not a specific ad; recorded to document the spending.'],
]
W('05_campaign_media/advertisements.csv', AH, AD)

# ---------------- social media
MH = ['post_id', 'candidate_id', 'platform', 'account_handle', 'post_date', 'post_type',
      'content_summary', 'media_included', 'engagement_notes', 'url', 'verification_status', 'notes']
SO = [
 ['COL-SM-01', 'COLLINS', 'X', '@MikeCollinsGA', '2026-05-28', 'text post',
  'Post about Kamala Harris later described as "Matt Lauer\'s sloppy seconds"', 'unknown', 'unknown',
  'unknown', 'verified', 'Post documented by Slate and by the biography; URL not captured.'],
 ['COL-SM-02', 'COLLINS', 'X', '@MikeCollinsGA', '2024-02-02', 'text post',
  'Suggested a migrant receive "a ticket on Pinochet Air for a free helicopter ride back"', 'unknown', 'unknown',
  'unknown', 'verified', 'Post later reported to concern a man who was misidentified.'],
 ['COL-SM-03', 'COLLINS', 'X', '@MikeCollinsGA', '2025-11-12', 'video post',
  'AI-generated video attacking Ossoff over the shutdown', 'video', 'unknown', 'unknown', 'partially verified',
  'Distributed through the campaign account per Access WDUN.'],
 ['OSS-SM-01', 'OSSOFF', 'X', '@ossoff', '2026-11-03', 'text post', 'Profile page returned a login shell; contents not retrievable',
  'unknown', 'unknown', 'https://x.com/ossoff', 'unverified', 'Access limit recorded, not evidence.'],
 ['OSS-SM-02', 'OSSOFF', 'TikTok', '@jonossoff', 'unknown', 'video post',
  'TikTok presence credited with reaching Generation Z voters', 'video', 'unknown', 'unknown', 'partially verified',
  'Described in the biography; no post-level data retrieved.'],
 ['COL-SM-04', 'COLLINS', 'X', '@MikeCollinsGA', '2026-10-16', 'repost',
  'Amplified Trump rally content from Dalton', 'unknown', 'unknown', 'unknown', 'unverified',
  'Reported indirectly; no post URL.'],
 ['OSS-SM-03', 'OSSOFF', 'X', '@ossoff', '2026-10-08', 'text post',
  'Campaign promoted debate clips and the tariff-repeal line', 'video', 'unknown', 'unknown', 'unverified',
  'Inferred from coverage; no post-level capture.'],
]
W('05_campaign_media/social_media.csv', MH, SO)
