# -*- coding: utf-8 -*-
"""Images, advertising, social video and press coverage."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import cell, write_csv  # noqa: E402
from build_media import ttl  # noqa: E402

CM = 'https://commons.wikimedia.org/wiki/'
FP = CM + 'Special:FilePath/'

IH = ['image_id', 'candidate_id', 'image_date', 'event_id', 'event_category', 'source_name',
      'source_url', 'original_image_url', 'photographer', 'copyright_status', 'license',
      'local_filename', 'image_resolution', 'framing', 'camera_angle', 'image_quality',
      'face_visibility', 'body_visibility', 'clothing_notes', 'notes', 'verification_status']
I = []
NI = 'not assessed — this build could not view image content; only the file\'s own description and the published caption were read'


def im(**k):
    I.append([k.get(h, 'unknown') for h in IH])


im(image_id='IMG-0001', candidate_id='RAMAN', image_date='2022-01-26', event_id='unknown',
   event_category='official_portrait', source_name='Wikimedia Commons',
   source_url=CM + 'File:Nithya_Raman,_2022.jpg',
   original_image_url=FP + 'Nithya_Raman,_2022.jpg',
   photographer='Nithya Raman (Commons author field); credit line points to the CD-4 council office press kit',
   copyright_status='public_domain', license='Public domain',
   local_filename='raman/raman_commons_2022.jpg', image_resolution='2093x2551',
   framing='unknown', camera_angle='unknown', image_quality='unknown',
   face_visibility='unknown', body_visibility='unknown',
   clothing_notes='unknown — ' + NI,
   notes='Council-office portrait, 1.8 MB original; a 640 px thumbnail (321,691 bytes) was downloaded. Commons description: "Nithya Raman is a member of the Los Angeles City Council representing District 4."',
   verification_status='verified')
im(image_id='IMG-0002', candidate_id='BASS', image_date='2023-04-02', event_id='unknown',
   event_category='official_portrait', source_name='Wikimedia Commons',
   source_url=CM + 'File:Karen_Bass,_2023.jpg',
   original_image_url=FP + 'Karen_Bass,_2023.jpg',
   photographer='Office of the Mayor of Los Angeles',
   copyright_status='public_domain', license='Public domain',
   local_filename='bass/bass_commons_2023.jpg', image_resolution='4959x4526',
   framing='unknown', camera_angle='unknown', image_quality='unknown',
   face_visibility='unknown', body_visibility='unknown',
   clothing_notes='unknown — ' + NI,
   notes='Commons description: "Official portrait of Los Angeles Mayor Karen Bass." 5.4 MB original; a 640 px thumbnail (582,951 bytes) was downloaded. Official-portrait status is the single most consequential visual fact in this archive: the incumbent has a civic portrait, the challenger does not.',
   verification_status='verified')
im(image_id='IMG-0003', candidate_id='BASS', image_date='2022-12-12', event_id='unknown',
   event_category='official_portrait', source_name='Wikimedia Commons',
   source_url=CM + 'File:Mayor_Karen_Bass_official_portrait.jpg',
   original_image_url=FP + 'Mayor_Karen_Bass_official_portrait.jpg',
   photographer='City of Los Angeles',
   copyright_status='public_domain', license='Public domain',
   local_filename='bass/bass_official_portrait.jpg', image_resolution='3870x3870',
   framing='unknown', camera_angle='unknown', image_quality='unknown',
   face_visibility='unknown', body_visibility='unknown',
   clothing_notes='unknown — ' + NI,
   notes='Dated to the Dec. 12, 2022 swearing-in day; square 1:1 format, which suits social avatars. 1.0 MB original; a 640 px thumbnail (235,194 bytes) was downloaded.',
   verification_status='verified')
im(image_id='IMG-0004', candidate_id='BASS', image_date='2023-04-02', event_id='unknown',
   event_category='official_portrait', source_name='Wikimedia Commons',
   source_url=CM + 'File:Karen_Bass,_20232_(cropped).jpg',
   original_image_url=FP + 'Karen_Bass,_20232_(cropped).jpg',
   photographer='Office of the Mayor of Los Angeles',
   copyright_status='public_domain', license='Public domain', local_filename='unknown',
   image_resolution='1858x2239', framing='unknown', camera_angle='unknown',
   image_quality='unknown', face_visibility='unknown', body_visibility='unknown',
   clothing_notes='unknown — ' + NI,
   notes='Cropped variant of IMG-0002, portrait 0.83:1 aspect ratio. Not downloaded: the thumbnail endpoint returned HTTP 429 for this file.',
   verification_status='verified')
im(image_id='IMG-0005', candidate_id='JOINT', image_date='2023-11-23', event_id='unknown',
   event_category='joint_appearance', source_name='Wikimedia Commons',
   source_url=CM + 'File:Nithya_Raman_and_Karen_Bass_2023.jpg',
   original_image_url=FP + 'Nithya_Raman_and_Karen_Bass_2023.jpg',
   photographer='Office of Mayor Karen Bass (Flickr)',
   copyright_status='public_domain', license='Public domain', local_filename='unknown',
   image_resolution='1044x1202', framing='unknown', camera_angle='unknown',
   image_quality='unknown', face_visibility='unknown', body_visibility='unknown',
   clothing_notes='unknown — ' + NI,
   notes='Commons description: "Mayor Bass announces funds for new bus shelters and projects that help address severe heat across the city." Documents the pre-rivalry alliance the 2026 race broke. Not downloaded (HTTP 429 on retry).',
   verification_status='verified')
im(image_id='IMG-0006', candidate_id='RAMAN', image_date='2023-01-16', event_id='unknown',
   event_category='parade', source_name='Wikimedia Commons',
   source_url=CM + 'File:Nithya_Raman_on_the_Los_Angeles_City_Council_float_2023_(cropped).jpg',
   original_image_url=FP + 'Nithya_Raman_on_the_Los_Angeles_City_Council_float_2023_(cropped).jpg',
   photographer='Eric Chan',
   copyright_status='licensed', license='CC BY 2.0', local_filename='unknown',
   image_resolution='314x399', framing='unknown', camera_angle='unknown',
   image_quality='unknown', face_visibility='unknown', body_visibility='unknown',
   clothing_notes='unknown — ' + NI,
   notes='Only 314x399 px — below archival reproduction quality. Kingdom Day Parade 2023, City Council float.',
   verification_status='verified')
im(image_id='IMG-0007', candidate_id='PRATT', image_date='2025-11-17', event_id='unknown',
   event_category='portrait', source_name='Wikimedia Commons',
   source_url=CM + 'File:Spencer_Pratt_in_November_2025.jpg',
   original_image_url=FP + 'Spencer_Pratt_in_November_2025.jpg',
   photographer='U.S. Senate Special Committee on Aging (YouTube)',
   copyright_status='public_domain', license='Public domain', local_filename='unknown',
   image_resolution='1920x1080', framing='unknown', camera_angle='unknown',
   image_quality='unknown', face_visibility='unknown', body_visibility='unknown',
   clothing_notes='unknown — ' + NI,
   notes='Third-place primary candidate; screenshot from a Senate committee video. Not downloaded (HTTP 429).',
   verification_status='verified')
im(image_id='IMG-0008', candidate_id='PRATT', image_date='2025-09-10', event_id='unknown',
   event_category='press_conference', source_name='Wikimedia Commons',
   source_url=CM + 'File:Spencer_Pratt_at_Sen_Rick_Scott_Press_Conference_on_Congressional_Investigation_into_Palisades_Wildfire_(3x4_crop).jpg',
   original_image_url=FP + 'Spencer_Pratt_at_Sen_Rick_Scott_Press_Conference_on_Congressional_Investigation_into_Palisades_Wildfire_(3x4_crop).jpg',
   photographer='Sen. Rick Scott (YouTube)',
   copyright_status='public_domain', license='Public domain', local_filename='unknown',
   image_resolution='323x431', framing='unknown', camera_angle='unknown',
   image_quality='unknown', face_visibility='unknown', body_visibility='unknown',
   clothing_notes='unknown — ' + NI,
   notes='Pratt at a Senate press conference on the Palisades fire — the visual bridge between his wildfire-loss persona and his candidacy.',
   verification_status='verified')
im(image_id='IMG-0009', candidate_id='RAMAN', image_date='2026-06-01', event_id='RAM-EVT-0005',
   event_category='campaign_event', source_name='CalMatters (Associated Press photo)',
   source_url='https://calmatters.org/commentary/2026/06/raman-bass-mayor-political-coalitions/',
   original_image_url='unknown',
   photographer='Associated Press (per CalMatters credit)', copyright_status='all_rights_reserved_link_only',
   license='unknown', local_filename='unknown', image_resolution='unknown',
   framing='unknown', camera_angle='unknown', image_quality='unknown',
   face_visibility='unknown', body_visibility='unknown', clothing_notes='unknown — ' + NI,
   notes='Captioned "Raman speaks during a campaign event about tenant protections with renters in Los Angeles". Link-only: no licence for redistribution.',
   verification_status='verified')
im(image_id='IMG-0010', candidate_id='RAMAN', image_date='2026-11-03',
   event_id='RAM-EVT-0018', event_category='election_night',
   source_name='CalMatters (Associated Press photo)',
   source_url='https://calmatters.org/commentary/2026/11/mayor-nithya-raman-bass-los-angeles/',
   original_image_url='unknown', photographer='Associated Press (per CalMatters credit)',
   copyright_status='all_rights_reserved_link_only', license='unknown', local_filename='unknown',
   image_resolution='unknown', framing='unknown', camera_angle='unknown', image_quality='unknown',
   face_visibility='unknown', body_visibility='unknown', clothing_notes='unknown — ' + NI,
   notes='Election-night photograph; the caption is the only visual evidence in the archive for the Greek Theatre event.',
   verification_status='verified')
im(image_id='IMG-0011', candidate_id='JOINT', image_date='2026-08-19', event_id='BAS-EVT-0011',
   event_category='debate', source_name='CalMatters (Associated Press photo)',
   source_url='https://calmatters.org/commentary/2026/10/la-mayoral-debate-friends-feud/',
   original_image_url='unknown', photographer='Associated Press (per CalMatters credit)',
   copyright_status='all_rights_reserved_link_only', license='unknown', local_filename='unknown',
   image_resolution='unknown', framing='unknown', camera_angle='unknown', image_quality='unknown',
   face_visibility='unknown', body_visibility='unknown', clothing_notes='unknown — ' + NI,
   notes='Caption: the two candidates "debate each other at the Sherman Oaks Homeowners Association in Sherman Oaks on Aug. 19, 2026".',
   verification_status='verified')
im(image_id='IMG-0012', candidate_id='JOINT', image_date='2026-08-19', event_id='RAM-EVT-0008',
   event_category='debate', source_name='LAist', source_url='https://laist.com/news/politics/bass-and-raman-face-off-in-first-mayoral-debate-ahead-of-the-general-election',
   original_image_url='unknown', photographer='unknown',
   copyright_status='all_rights_reserved_link_only', license='unknown', local_filename='unknown',
   image_resolution='unknown', framing='unknown', camera_angle='unknown', image_quality='unknown',
   face_visibility='unknown', body_visibility='unknown', clothing_notes='unknown — ' + NI,
   notes='LAist preview carries a debate photograph; the caption text was not preserved in the extracted body.',
   verification_status='partially verified')
im(image_id='IMG-0013', candidate_id='BASS', image_date='2026-09-17', event_id='unknown',
   event_category='advertisement_still', source_name='Los Angeles Times',
   source_url='https://www.latimes.com/california/newsletter/2026-09-19/los-angeles-mayor-ad-blitz-hollywood-ice-homelessness',
   original_image_url='unknown', photographer='unknown',
   copyright_status='all_rights_reserved_link_only', license='unknown', local_filename='unknown',
   image_resolution='unknown', framing='unknown', camera_angle='unknown', image_quality='unknown',
   face_visibility='unknown', body_visibility='unknown',
   clothing_notes='The newsletter describes the mayor in an "aquamarine pantsuit" in the ICE spot — the only documented clothing note in the whole runoff coverage',
   notes='Stills from the 30-second digital spot; link-only. Reporting, not viewing, is the source of the clothing note.',
   verification_status='verified')
im(image_id='IMG-0014', candidate_id='BASS', image_date='2025-12-13', event_id='BAS-EVT-0002',
   event_category='launch_rally', source_name='ABC7 Los Angeles',
   source_url='https://abc7.com/post/mayor-karen-bass-appear-reelection-campaign-rally-downtown-la-today/18283470/',
   original_image_url='unknown', photographer='unknown',
   copyright_status='all_rights_reserved_link_only', license='unknown', local_filename='unknown',
   image_resolution='unknown', framing='unknown', camera_angle='unknown', image_quality='unknown',
   face_visibility='unknown', body_visibility='unknown', clothing_notes='unknown — ' + NI,
   notes='Wire-service rally photograph; link-only, no redistribution licence.',
   verification_status='verified')
im(image_id='IMG-0015', candidate_id='RAMAN', image_date='unknown', event_id='unknown',
   event_category='interview', source_name='The Hollywood Reporter',
   source_url='https://www.hollywoodreporter.com/news/politics-news/nithya-raman-hollywood-position-karen-bass-polls-1236720525/',
   original_image_url='unknown', photographer='unknown',
   copyright_status='all_rights_reserved_link_only', license='unknown', local_filename='unknown',
   image_resolution='unknown', framing='unknown', camera_angle='unknown', image_quality='unknown',
   face_visibility='unknown', body_visibility='unknown', clothing_notes='unknown — ' + NI,
   notes='Trade-paper interview page carries an embedded video and at least one still; link-only.',
   verification_status='partially verified')

write_csv('04_visual_archive/image_archive.csv', IH, I)

# ------------------------------------------------------------------ advertisements
AH = ['ad_id', 'candidate_id', 'sponsor', 'sponsor_type', 'release_date', 'title', 'platform',
      'length_seconds', 'issue_or_message', 'main_visual_elements', 'narration_soundtrack',
      'candidate_appearance', 'main_claims', 'video_url', 'transcript_url', 'fact_check',
      'media_coverage', 'source_urls', 'verification_status', 'notes']
A = []


def ad(**k):
    A.append([k.get(h, 'unknown') for h in AH])


LTAFF = 'https://www.latimes.com/california/newsletter/2026-09-19/los-angeles-mayoral-ad-blitz-hollywood-ice-homelessness'
R_HOU = 'https://www.nithyaforthecity.com/housing'
B_WHY = 'https://karenbass.com/why-im-running'
ad(ad_id='AD-0001', candidate_id='RAMAN', sponsor='Nithya Raman for Mayor', sponsor_type='candidate_campaign',
   release_date='2026-09-14', title='For Your Consideration (Emmy Awards spot)', platform='Television, then social media',
   length_seconds=30, issue_or_message='Change; affordability; an L.A. that loves you back',
   main_visual_elements='Hollywood/Emmy Awards parody: the ad is styled as a awards-season "for your consideration" spot.',
   narration_soundtrack='Narrated by Bob Odenkirk',
   candidate_appearance='Raman appears in the spot per the trade and L.A. Times coverage.',
   main_claims='"L.A. shows the world what it means to be a star"; the campaign offers "Change. Affordability. An L.A. that loves you back."',
   video_url='https://www.youtube.com/watch?v=Lrum87XgwWA', transcript_url='unknown',
   fact_check='No factual claim is testable; the spot is thematic.',
   media_coverage='L.A. Times newsletter; YouTube upload titled "For your consideration: Nithya Raman Emmy Awards ad"',
   source_urls=cell(LTAFF), verification_status='verified',
   notes='Timed to the Emmy broadcast; the YouTube upload is the spot itself, which is why the narration is recorded here rather than inferred.')
ad(ad_id='AD-0002', candidate_id='BASS', sponsor='Re-Elect Karen Bass for Mayor 2026', sponsor_type='candidate_campaign',
   release_date='2026-09-17', title='ICE-response digital spot', platform='Digital (30-second)',
   length_seconds=30, issue_or_message='Standing up to federal immigration enforcement',
   main_visual_elements='Footage from the July 2025 MacArthur Park ICE operations.',
   narration_soundtrack='unknown', candidate_appearance='Bass appears, described by the L.A. Times as wearing an aquamarine pantsuit.',
   main_claims='"When someone comes after your family, you don\'t hesitate ... You stand up. You fight."',
   video_url='unknown', transcript_url='unknown',
   fact_check='The footage is presented as documentary; no date label is reported inside the spot.',
   media_coverage='L.A. Times newsletter', source_urls=cell(LTAFF),
   verification_status='verified',
   notes='The only runoff ad whose candidate wardrobe is documented in press coverage.')
ad(ad_id='AD-0003', candidate_id='RAMAN', sponsor='Los Angeles Police Protective League',
   sponsor_type='outside_pac', release_date='2026-09-18', title="Doesn't Get It",
   platform='Television and digital', length_seconds='unknown',
   issue_or_message='Raman is out of touch on public safety and homelessness',
   main_visual_elements='A girl walking past an encampment, intercut with Raman\'s 2024 Sherman Oaks forum remarks.',
   narration_soundtrack='Child voice: "Walking to school shouldn\'t be scary."',
   candidate_appearance='Raman appears only in the older forum clip.',
   main_claims='Raman said "I don\'t think a kid\'s gonna be safer because a tent is 500 feet away from a school."',
   video_url='unknown', transcript_url='unknown',
   fact_check='The quoted line is from a 2024 forum clip, used out of its original context; the ad\'s framing is the union\'s.',
   media_coverage='L.A. Times newsletter', source_urls=cell(LTAFF),
   verification_status='verified',
   notes='Independent expenditure, not authorised by any candidate. The "walking to school" line mirrors the incumbent\'s own "kids no longer dodge tents on their walk to school" formulation.')
ad(ad_id='AD-0004', candidate_id='BASS', sponsor='Streets For All PAC', sponsor_type='outside_pac',
   release_date='unknown', title='Anti-Bass street-safety spots', platform='Facebook and Instagram',
   length_seconds='unknown', issue_or_message='Bass governs for the rich and powerful; street deaths are rising',
   main_visual_elements='unknown', narration_soundtrack='unknown', candidate_appearance='unknown',
   main_claims='"L.A. deserves a mayor who doesn\'t just listen to the rich and powerful."',
   video_url='unknown', transcript_url='unknown',
   fact_check='No specific numeric claim was reported; the spots are character attacks.',
   media_coverage='L.A. Times newsletter (nearly two dozen spots identified in Ethics Commission filings)',
   source_urls=cell(LTAFF), verification_status='partially verified',
   notes='Release date not reported; recorded as unknown rather than inferred from the newsletter date.')
ad(ad_id='AD-0005', candidate_id='BASS', sponsor='Re-Elect Karen Bass for Mayor 2026',
   sponsor_type='candidate_campaign', release_date='unknown', title='Mayor Karen Bass – Know This',
   platform='YouTube / campaign site', length_seconds='unknown',
   issue_or_message='Incumbent record and second-term purpose',
   main_visual_elements='unknown', narration_soundtrack='unknown',
   candidate_appearance='Bass appears (campaign video).', main_claims='unknown',
   video_url='https://www.youtube.com/watch?v=iR5HD6oCjz0', transcript_url='unknown',
   fact_check='Content not transcribed; no claim recorded.',
   media_coverage='Campaign website embed only', source_urls=cell(B_WHY),
   verification_status='partially verified',
   notes='Exists as a campaign-produced video; no coverage of it was located, so no message is asserted.')
ad(ad_id='AD-0006', candidate_id='RAMAN', sponsor='Nithya Raman for Mayor', sponsor_type='candidate_campaign',
   release_date='unknown', title="Let's lower the rent!",
   platform='YouTube / campaign site', length_seconds='unknown',
   issue_or_message='Triple housing production; eliminate bureaucracy; lower rent',
   main_visual_elements='unknown', narration_soundtrack='unknown',
   candidate_appearance='Raman appears (campaign video).',
   main_claims='As mayor she will "triple housing production and eliminate pointless bureaucracy".',
   video_url='https://www.youtube.com/watch?v=I41TFtz_ywA', transcript_url='unknown',
   fact_check='The tripling target is a pledge, not a result.',
   media_coverage='Campaign website embed only', source_urls=cell(R_HOU),
   verification_status='partially verified',
   notes='Short-form digital video hosted on the campaign\'s housing page; release date unknown.')

write_csv('05_campaign_media/advertisements.csv', AH, A)

# ------------------------------------------------------------------ social media (campaign video channels)
MH = ['post_id', 'candidate_id', 'platform', 'account_handle', 'post_date', 'post_type',
      'content_summary', 'media_included', 'engagement_notes', 'url', 'verification_status', 'notes']
M = []
M.append(['SOC-0001', 'RAMAN', 'YouTube', 'Nithya for Mayor', 'unknown', 'video',
          'Issue video: "Why did homelessness rise in LA?"', 'video', 'unknown',
          'https://www.youtube.com/watch?v=NH9_bZQ7AyA', 'partially verified',
          'Metadata from YouTube oEmbed; view and engagement counts not retrieved.'])
M.append(['SOC-0002', 'RAMAN', 'YouTube', 'Nithya for Mayor', 'unknown', 'video',
          'Issue video: "Nithya\'s Plan for Addressing Encampments in Los Angeles"', 'video', 'unknown',
          'https://www.youtube.com/watch?v=B-dA-DYMJwQ', 'partially verified',
          'Embedded on the campaign homelessness page.'])
M.append(['SOC-0003', 'RAMAN', 'YouTube', 'Nithya for Mayor', 'unknown', 'video',
          'Issue video on rent and housing production', 'video', 'unknown',
          'https://www.youtube.com/watch?v=I41TFtz_ywA', 'partially verified',
          'Title begins "Let\'s lower the rent!".'])
M.append(['SOC-0004', 'RAMAN', 'YouTube', 'Nithya for Mayor', 'unknown', 'video',
          'Issue video: "Nithya Raman\'s Palisades Recovery Plan"', 'video', 'unknown',
          'https://www.youtube.com/watch?v=taKInZXZz5M', 'partially verified',
          'Embedded on the Palisades recovery page.'])
M.append(['SOC-0005', 'RAMAN', 'YouTube', 'Nithya for Mayor', 'unknown', 'video',
          'Tenant-story video about a landlord ultimatum', 'video', 'unknown',
          'https://www.youtube.com/watch?v=8jN4-CMiv8I', 'partially verified',
          'Constituent-casework video; the named tenant is "Hayley" per the title.'])
M.append(['SOC-0006', 'RAMAN', 'YouTube', 'Nithya for Mayor', 'unknown', 'video',
          'Video: "There were more traffic deaths than homicides in 2025. I\'m running to make LA streets safer for all!"',
          'video', 'unknown', 'https://www.youtube.com/watch?v=lNXuCMcvV6Q', 'partially verified',
          'The traffic-death comparison is the campaign\'s claim; no source is given in the title.'])
M.append(['SOC-0007', 'BASS', 'YouTube', 'Re-Elect Karen Bass for Mayor 2026', 'unknown', 'video',
          'Campaign video: "Mayor Karen Bass – Know This"', 'video', 'unknown',
          'https://www.youtube.com/watch?v=iR5HD6oCjz0', 'partially verified',
          'Channel name confirms authorship; content not transcribed.'])
M.append(['SOC-0008', 'RAMAN', 'YouTube', 'Nithya for Mayor', 'unknown', 'video',
          'The Emmy-themed ad uploaded in full: "For your consideration"', 'video', 'unknown',
          'https://www.youtube.com/watch?v=Lrum87XgwWA', 'verified',
          'This upload is the primary evidence for the ad\'s existence and title.'])

write_csv('05_campaign_media/social_media.csv', MH, M)

# ------------------------------------------------------------------ media coverage
CH = ['coverage_id', 'candidate_id', 'event_id', 'publication_date', 'outlet', 'author', 'title',
      'url', 'source_tier', 'coverage_type', 'key_framing', 'notable_quotes',
      'framing_of_candidate', 'mentions_opponent', 'reliability_notes']
C = []


def cov(**k):
    C.append([k.get(h, 'unknown') for h in CH])


cov(coverage_id='COV-0001', candidate_id='RAMAN', event_id='RAM-EVT-0018', publication_date='2026-11-05',
    outlet='Los Angeles Times', author='unknown', title=ttl('https://www.latimes.com/california/story/2026-11-05/nithya-raman-defeats-bass-to-become-next-la-mayor'),
    url='https://www.latimes.com/california/story/2026-11-05/nithya-raman-defeats-bass-to-become-next-la-mayor',
    source_tier='T2', coverage_type='news_report',
    key_framing='The outcome: an incumbent mayor defeated by a council colleague.',
    notable_quotes='unknown', framing_of_candidate='Winner; historic upset.', mentions_opponent='yes',
    reliability_notes='Metered: headline/navigation only. Used for outcome and date, nothing more.')
cov(coverage_id='COV-0002', candidate_id='BASS', event_id='BAS-EVT-0001', publication_date='2024-07-01',
    outlet='Los Angeles Times', author='unknown', title=ttl('https://www.latimes.com/california/story/2024-07-01/mayor-karen-bass-files-paperwork-to-run-for-reelection'),
    url='https://www.latimes.com/california/story/2024-07-01/mayor-karen-bass-files-paperwork-to-run-for-reelection',
    source_tier='T2', coverage_type='news_report',
    key_framing='Early reelection filing by an incumbent clearing the field.',
    notable_quotes='unknown', framing_of_candidate='Front-runner by default.', mentions_opponent='no',
    reliability_notes='Metered; lede paragraphs retrievable.')
cov(coverage_id='COV-0003', candidate_id='RAMAN', event_id='RAM-EVT-0001', publication_date='2025-11-15',
    outlet='Los Angeles Times', author='unknown', title=ttl('https://www.latimes.com/california/newsletter/2025-11-15/la-on-the-record-an-activist-is-challenging-bass-from-the-left'),
    url='https://www.latimes.com/california/newsletter/2025-11-15/la-on-the-record-an-activist-is-challenging-bass-from-the-left',
    source_tier='T2', coverage_type='newsletter',
    key_framing='A left challenge to Bass, framed through the "Mamdani" national story.',
    notable_quotes='unknown', framing_of_candidate='Insurgent possibility.', mentions_opponent='yes',
    reliability_notes='Metered. National-comparison framing is the newsletter\'s, not the archive\'s.')
cov(coverage_id='COV-0004', candidate_id='RAMAN', event_id='RAM-EVT-0003', publication_date='2026-05-05',
    outlet='Los Angeles Times', author='unknown', title=ttl('https://www.latimes.com/california/story/2026-05-05/karen-bass-nithya-raman-head-to-head-mayoral-debate'),
    url='https://www.latimes.com/california/story/2026-05-05/karen-bass-nithya-raman-head-to-head-mayoral-debate',
    source_tier='T2', coverage_type='news_report',
    key_framing='A combative two-person debate inside the incumbent\'s weakest geographic zone.',
    notable_quotes='unknown', framing_of_candidate='Aggressive challenger.', mentions_opponent='yes',
    reliability_notes='Metered; headline retrievable only.')
cov(coverage_id='COV-0005', candidate_id='BASS', event_id='BAS-EVT-0008', publication_date='2026-05-11',
    outlet='Los Angeles Times', author='unknown', title=ttl('https://www.latimes.com/california/story/2026-05-11/la-mayoral-forum-canceled-after-leading-candidates-pull-out'),
    url='https://www.latimes.com/california/story/2026-05-11/la-mayoral-forum-canceled-after-leading-candidates-pull-out',
    source_tier='T2', coverage_type='news_report',
    key_framing='Front-runner withdrawal killed the final pre-primary forum.',
    notable_quotes='unknown', framing_of_candidate='Risk-averse incumbent.', mentions_opponent='yes',
    reliability_notes='Metered. Corroborated by L.A. Magazine and the Wikipedia debate list.')
cov(coverage_id='COV-0006', candidate_id='RAMAN', event_id='unknown', publication_date='2026-05-19',
    outlet='Los Angeles Times', author='unknown', title=ttl('https://www.latimes.com/california/story/2026-05-19/city-council-progressives-snub-raman-endorse-bass-in-la-mayors-race'),
    url='https://www.latimes.com/california/story/2026-05-19/city-council-progressives-snub-raman-endorse-bass-in-la-mayors-race',
    source_tier='T2', coverage_type='news_report',
    key_framing='Progressive council colleagues chose the incumbent over the councilmember.',
    notable_quotes='Hernandez, Jurado and Soto-Martínez endorsements were "aimed at denting left-wing support for Nithya Raman"',
    framing_of_candidate='Isolated on her own council.', mentions_opponent='yes',
    reliability_notes='Metered; lede retrievable.')
cov(coverage_id='COV-0007', candidate_id='RAMAN', event_id='unknown', publication_date='2026-09-19',
    outlet='Los Angeles Times', author='unknown', title=ttl('https://www.latimes.com/california/newsletter/2026-09-19/los-angeles-mayoral-ad-blitz-hollywood-ice-homelessness'),
    url='https://www.latimes.com/california/newsletter/2026-09-19/los-angeles-mayoral-ad-blitz-hollywood-ice-homelessness',
    source_tier='T2', coverage_type='newsletter',
    key_framing='The runoff\'s advertising wave: Hollywood parody, ICE footage, encampment imagery.',
    notable_quotes='Raman "touting her new Hollywood-themed ad \'For Your Consideration,\' timed to coincide with the Emmy Awards"',
    framing_of_candidate='Cultural-fluency campaign.', mentions_opponent='yes',
    reliability_notes='Best single description of the ad war; metered but body retrievable.')
cov(coverage_id='COV-0008', candidate_id='BASS', event_id='BAS-EVT-0015', publication_date='2026-10-20',
    outlet='Los Angeles Times', author='unknown', title=ttl('https://www.latimes.com/california/story/2026-10-20/rick-caruso-has-extreme-concern-over-raman-but-declines-to-endorse-in-mayors-race'),
    url='https://www.latimes.com/california/story/2026-10-20/rick-caruso-has-extreme-concern-over-raman-but-declines-to-endorse-in-mayors-race',
    source_tier='T2', coverage_type='news_report',
    key_framing='The 2022 Republican-adjacent runner-up declines to endorse but says he will vote for Bass.',
    notable_quotes='unknown', framing_of_candidate='Reluctant recipient of centrist votes.', mentions_opponent='yes',
    reliability_notes='Metered; ABC7 interview corroborates the vote intention.')
cov(coverage_id='COV-0009', candidate_id='JOINT', event_id='RAM-EVT-0002', publication_date='2026-02-17',
    outlet='LAist', author='unknown', title=ttl('https://laist.com/news/politics/your-quick-guide-to-the-la-mayors-race'),
    url='https://laist.com/news/politics/your-quick-guide-to-the-la-mayors-race', source_tier='T2',
    coverage_type='news_report',
    key_framing='Neutral candidate guide: biographies, records, the shape of the field.',
    notable_quotes='Bass "touts a drop in homelessness and the lowest crime rate in 60 years"',
    framing_of_candidate='Both candidates described through their own records.', mentions_opponent='yes',
    reliability_notes='Non-partisan public-radio guide; the most useful single baseline document in the archive.')
cov(coverage_id='COV-0010', candidate_id='JOINT', event_id='BAS-EVT-0011', publication_date='2026-08-18',
    outlet='LAist', author='unknown', title=ttl('https://laist.com/news/politics/bass-and-raman-face-off-in-first-mayoral-debate-ahead-of-the-general-election'),
    url='https://laist.com/news/politics/bass-and-raman-face-off-in-first-mayoral-debate-ahead-of-the-general-election',
    source_tier='T2', coverage_type='news_report',
    key_framing='Preview: venue, sponsor, timing, stakes of the first runoff debate.',
    notable_quotes='"You want to hear frustrated? I\'m frustrated too" (quoted from a campaign event)',
    framing_of_candidate='Debate as the runoff\'s first real contrast.', mentions_opponent='yes',
    reliability_notes='Live audio hosted on the same article.')
cov(coverage_id='COV-0011', candidate_id='JOINT', event_id='BAS-EVT-0013', publication_date='2026-09-30',
    outlet='LAist', author='unknown', title=ttl('https://laist.com/news/politics/karen-bass-nithya-raman-gaza-jewish-federation-forum'),
    url='https://laist.com/news/politics/karen-bass-nithya-raman-gaza-jewish-federation-forum',
    source_tier='T2', coverage_type='news_report',
    key_framing='The Gaza split, reported through a domestic community forum.',
    notable_quotes='unknown (audio, 1:39:47, was not transcribed in this build)',
    framing_of_candidate='Candidates judged on foreign-policy language.', mentions_opponent='yes',
    reliability_notes='Full audio available; no transcript.')
cov(coverage_id='COV-0012', candidate_id='RAMAN', event_id='unknown', publication_date='2026-09-25',
    outlet='LAist', author='unknown', title=ttl('https://laist.com/news/politics/la-mayor-race-bass-raman-donors-campaign-finance-sosnick-airbnb'),
    url='https://laist.com/news/politics/la-mayor-race-bass-raman-donors-campaign-finance-sosnick-airbnb',
    source_tier='T2', coverage_type='news_report',
    key_framing='Outside money dwarfs candidate committees; two megadonors on the Raman side.',
    notable_quotes='"Aaron Sosnick, a hedge fund founder, and the construction workers union ... each gave $3 million"',
    framing_of_candidate='Insurgent backed by a hedge-fund billionaire.', mentions_opponent='yes',
    reliability_notes='The clearest explanation of the $1,800 direct-donation cap and the IE structure.')
cov(coverage_id='COV-0013', candidate_id='JOINT', event_id='BAS-EVT-0012', publication_date='2026-10-03',
    outlet='LAist', author='unknown', title=ttl('https://laist.com/brief/news/politics/los-angeles-mayor-race-city-council-district-nine-forum-bass-raman-2026-november-election'),
    url='https://laist.com/brief/news/politics/los-angeles-mayor-race-city-council-district-nine-forum-bass-raman-2026-november-election',
    source_tier='T2', coverage_type='news_report',
    key_framing='South L.A. forum: density, policing, immigration enforcement.',
    notable_quotes='Bass: "Black and brown poor folks the most have been central in my administration"',
    framing_of_candidate='Both candidates courting Black and Latino voters separately.', mentions_opponent='yes',
    reliability_notes='Body says Saturday, caption says Sept. 29 — internal date conflict flagged in campaign_events.csv.')
cov(coverage_id='COV-0014', candidate_id='BASS', event_id='unknown', publication_date='2026-02-10',
    outlet='CalMatters', author='unknown', title=ttl('https://calmatters.org/commentary/2026/02/la-mayor-bass-election-challenge/'),
    url='https://calmatters.org/commentary/2026/02/la-mayor-bass-election-challenge/', source_tier='T2',
    coverage_type='op_ed',
    key_framing='An incumbent governing a city with a stack of unresolved crises.',
    notable_quotes='"housing, utilities and other necessities, homelessness, uncertain water supplies ... budget deficits"',
    framing_of_candidate='Vulnerable incumbent.', mentions_opponent='yes',
    reliability_notes='Commentary; the crisis list is the author\'s, useful as framing rather than fact.')
cov(coverage_id='COV-0015', candidate_id='RAMAN', event_id='RAM-EVT-0007', publication_date='2026-08-06',
    outlet='CalMatters', author='Jim Newton', title=ttl('https://calmatters.org/commentary/2026/08/los-angeles-homelessness-raman-bass/'),
    url='https://calmatters.org/commentary/2026/08/los-angeles-homelessness-raman-bass/', source_tier='T2',
    coverage_type='op_ed',
    key_framing='Homelessness as the race\'s moral core; the carpenters endorsement as a coalition rupture.',
    notable_quotes='"registered 45,194 unhoused people in the city of Los Angeles this year, up from 43,695 the year prior"',
    framing_of_candidate='Serious, specific challenger.', mentions_opponent='yes',
    reliability_notes='Named columnist; carries the 2026 LAHSA count used in this archive.')
cov(coverage_id='COV-0016', candidate_id='JOINT', event_id='RAM-EVT-0016', publication_date='2026-10-15',
    outlet='CalMatters', author='unknown', title=ttl('https://calmatters.org/commentary/2026/10/la-mayoral-debate-friends-feud/'),
    url='https://calmatters.org/commentary/2026/10/la-mayoral-debate-friends-feud/', source_tier='T2',
    coverage_type='op_ed',
    key_framing='Two former allies now trading accusations of lying on television.',
    notable_quotes='"Now is not the time to turn the city over to Nithya Raman."',
    framing_of_candidate='Personal rupture over policy difference.', mentions_opponent='yes',
    reliability_notes='Commentary quoting the debate directly; the source for several verbatim lines.')
cov(coverage_id='COV-0017', candidate_id='RAMAN', event_id='RAM-EVT-0018', publication_date='2026-11-05',
    outlet='CalMatters', author='unknown', title=ttl('https://calmatters.org/commentary/2026/11/mayor-nithya-raman-bass-los-angeles/'),
    url='https://calmatters.org/commentary/2026/11/mayor-nithya-raman-bass-los-angeles/', source_tier='T2',
    coverage_type='op_ed',
    key_framing='How a councilmember beat a mayor, and what the coalition looked like.',
    notable_quotes='"Her election night party at the Greek Theater in Griffith Park was an outpouring of exuberant energy"',
    framing_of_candidate='Coalition-builder.', mentions_opponent='yes',
    reliability_notes='Post-election commentary; venue and atmosphere reported, not observed by the archive.')
cov(coverage_id='COV-0018', candidate_id='RAMAN', event_id='unknown', publication_date='2026-06-24',
    outlet='CalMatters', author='unknown', title=ttl('https://calmatters.org/commentary/2026/06/raman-bass-mayor-political-coalitions/'),
    url='https://calmatters.org/commentary/2026/06/raman-bass-mayor-political-coalitions/', source_tier='T2',
    coverage_type='op_ed',
    key_framing='Los Angeles as a national case study in coalition politics.',
    notable_quotes='"Los Angeles, with its extraordinary diversity, is a national case study in coalition politics"',
    framing_of_candidate='Coalition arithmetic rather than ideology.', mentions_opponent='yes',
    reliability_notes='Commentary; also the source of the tenant-event photo caption.')
cov(coverage_id='COV-0019', candidate_id='JOINT', event_id='unknown', publication_date='2026-06-02',
    outlet='NBC News', author='unknown', title=ttl('https://www.nbcnews.com/politics/2026-primary-elections/los-angeles-mayor-results'),
    url='https://www.nbcnews.com/politics/2026-primary-elections/los-angeles-mayor-results',
    source_tier='T2', coverage_type='live_blog',
    key_framing='Vote totals as they accumulated on primary night.',
    notable_quotes='unknown', framing_of_candidate='Data, not framing.', mentions_opponent='yes',
    reliability_notes='The only retrieved page with a complete, arithmetically consistent primary table.')
cov(coverage_id='COV-0020', candidate_id='JOINT', event_id='unknown', publication_date='2026-10-28',
    outlet='NBC Los Angeles', author='Jonathan Lloyd',
    title=ttl('https://www.nbclosangeles.com/elections/karen-bass-nithya-raman-la-mayor-election-poll/3962255/'),
    url='https://www.nbclosangeles.com/elections/karen-bass-nithya-raman-la-mayor-election-poll/3962255/',
    source_tier='T2', coverage_type='news_report',
    key_framing='Final poll shows a dead heat with about one in five voters undecided.',
    notable_quotes='"each candidate received 40% support"',
    framing_of_candidate='Too close to call.', mentions_opponent='yes',
    reliability_notes='Independent confirmation of the final Berkeley IGS numbers.')
cov(coverage_id='COV-0021', candidate_id='BASS', event_id='BAS-EVT-0002', publication_date='2025-12-14',
    outlet='ABC7 Los Angeles', author='Jose Herrera (CNS)',
    title=ttl('https://abc7.com/post/mayor-karen-bass-appear-reelection-campaign-rally-downtown-la-today/18283470/'),
    url='https://abc7.com/post/mayor-karen-bass-appear-reelection-campaign-rally-downtown-la-today/18283470/',
    source_tier='T2', coverage_type='news_report',
    key_framing='Launch rally as a coalition demonstration against the federal government.',
    notable_quotes='"Who would have imagined that we would have to defend ourselves from our very government?"',
    framing_of_candidate='Experienced coalition manager.', mentions_opponent='no',
    reliability_notes='Wire copy; the fullest account of the launch speech retrieved.')
cov(coverage_id='COV-0022', candidate_id='BASS', event_id='BAS-EVT-0010', publication_date='2026-05-28',
    outlet='Los Angeles Daily News', author='unknown',
    title=ttl('https://www.dailynews.com/2026/05/28/gov-newsom-endorses-la-mayor-karen-bass-as-new-poll-gauges-candidates-support/'),
    url='https://www.dailynews.com/2026/05/28/gov-newsom-endorses-la-mayor-karen-bass-as-new-poll-gauges-candidates-support/',
    source_tier='T2', coverage_type='news_report',
    key_framing='Establishment consolidation in the closing week of the primary.',
    notable_quotes='"figures come from a survey of 1,913 registered voters"',
    framing_of_candidate='Consensus choice.', mentions_opponent='yes',
    reliability_notes='SCNG paper; also carries the late-primary Berkeley IGS numbers.')
cov(coverage_id='COV-0023', candidate_id='RAMAN', event_id='RAM-EVT-0011', publication_date='2026-09-11',
    outlet='Our Weekly', author='unknown', title=ttl('https://www.ourweekly.com/2026/09/11/nithya-raman-announces-new-endorsement/'),
    url='https://www.ourweekly.com/2026/09/11/nithya-raman-announces-new-endorsement/', source_tier='T3',
    coverage_type='news_report',
    key_framing='Black-community weekly covering a former controller\'s endorsement and the budget argument.',
    notable_quotes='"no responsible mayor would pursue them through a financing plan that drains essential services for decades"',
    framing_of_candidate='Fiscally serious challenger.', mentions_opponent='yes',
    reliability_notes='Community weekly; endorsement release largely reprinted.')
cov(coverage_id='COV-0024', candidate_id='RAMAN', event_id='RAM-EVT-0006', publication_date='2026-07-16',
    outlet='FOX 11 Los Angeles', author='unknown', title=ttl('https://www.foxla.com/news/kenneth-mejia-endorses-nithya-raman-la-mayor'),
    url='https://www.foxla.com/news/kenneth-mejia-endorses-nithya-raman-la-mayor', source_tier='T2',
    coverage_type='news_report',
    key_framing='The city controller\'s endorsement turns the budget into a campaign issue.',
    notable_quotes='"criticized City Hall\'s spending choices"',
    framing_of_candidate='Fiscal reformer.', mentions_opponent='yes',
    reliability_notes='Local TV station; the "$1 billion LAPD contract" is reported as a characterisation.')
cov(coverage_id='COV-0025', candidate_id='RAMAN', event_id='RAM-EVT-0015', publication_date='2026-10-01',
    outlet='The Hollywood Reporter', author='unknown', title=ttl('https://www.hollywoodreporter.com/news/politics-news/nithya-raman-hollywood-position-karen-bass-polls-1236720525/'),
    url='https://www.hollywoodreporter.com/news/politics-news/nithya-raman-hollywood-position-karen-bass-polls-1236720525/',
    source_tier='T2', coverage_type='interview',
    key_framing='A challenger pitching herself to the industry as better for Hollywood than the mayor.',
    notable_quotes='unknown (video interview not transcribed)', framing_of_candidate='Industry-friendly progressive.',
    mentions_opponent='yes', reliability_notes='Trade paper; embedded video not transcribed in this build.')
cov(coverage_id='COV-0026', candidate_id='JOINT', event_id='unknown', publication_date='2026-02-07',
    outlet='LAist', author='unknown', title=ttl('https://laist.com/news/politics/austin-beutner-drops-out-of-la-mayoral-race-after-daughters-death'),
    url='https://laist.com/news/politics/austin-beutner-drops-out-of-la-mayoral-race-after-daughters-death',
    source_tier='T2', coverage_type='news_report',
    key_framing='A withdrawal that thinned the non-incumbent field.',
    notable_quotes='unknown', framing_of_candidate='Context for the field.', mentions_opponent='no',
    reliability_notes='Used only to explain the field shape.')

write_csv('05_campaign_media/media_coverage.csv', CH, C)
