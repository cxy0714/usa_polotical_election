# -*- coding: utf-8 -*-
"""Speeches, videos, images, advertising, social video and press coverage."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import CASE, cell, write_csv  # noqa: E402

REPORT = {r['url']: r for r in json.load(open(os.path.join(CASE, '_staging', 'mirror_report.json'),
                                               encoding='utf-8'))}


def ttl(url, strip=(' | Los Angeles Times', ' - Los Angeles Times', ' - ABC7 Los Angeles',
                    ' – Daily News', ' | TheWrap', ' - CalMatters', ' | LAist',
                    ' - CBS Los Angeles', ' | Our Weekly', ' | Deadline',
                    ' | The Hollywood Reporter', ' | FOX 11 Los Angeles',
                    ' | New York Post', ' | NBC Los Angeles', ' | NBC News',
                    ' | Manhattan Institute', ' | Westside Current', ' | La Opinión')):
    t = (REPORT.get(url) or {}).get('title') or ''
    for s in strip:
        if t.endswith(s):
            t = t[:-len(s)]
    return t or 'unknown'


WIKI = 'https://en.wikipedia.org/w/index.php?title=2026_Los_Angeles_mayoral_election&action=raw'
NBCR = 'https://www.nbcnews.com/politics/2026-primary-elections/los-angeles-mayor-results'
ABC7RALLY = 'https://abc7.com/post/mayor-karen-bass-appear-reelection-campaign-rally-downtown-la-today/18283470/'
B_HOW = 'https://karenbass.com/how-we-changed-la'
B_WHY = 'https://karenbass.com/why-im-running'
R_HOU = 'https://www.nithyaforthecity.com/housing'
R_HOM = 'https://www.nithyaforthecity.com/homelessness'
R_RENT = 'https://www.nithyaforthecity.com/renters'
R_PAL = 'https://www.nithyaforthecity.com/palisadesrecovery'
R_TRANS = 'https://www.nithyaforthecity.com/transportation'
R_WHY = 'https://www.nithyaforthecity.com/why-im-running'
R_ABOUT = 'https://www.nithyaforthecity.com/about-nithya'
LTAFF = 'https://www.latimes.com/california/newsletter/2026-09-19/los-angeles-mayoral-ad-blitz-hollywood-ice-homelessness'
CMDEB = 'https://calmatters.org/commentary/2026/10/la-mayoral-debate-friends-feud/'
CMHOMELESS = 'https://calmatters.org/commentary/2026/08/los-angeles-homelessness-raman-bass/'
CMWIN = 'https://calmatters.org/commentary/2026/11/mayor-nithya-raman-bass-los-angeles/'
CMCOAL = 'https://calmatters.org/commentary/2026/06/raman-bass-mayor-political-coalitions/'
SOHA_AUG = 'https://www.youtube.com/watch?v=fVzKUvSstY4&ra=m'
LAISTDEB = 'https://laist.com/news/politics/bass-and-raman-face-off-in-first-mayoral-debate-ahead-of-the-general-election'
LAISTSL = 'https://laist.com/brief/news/politics/los-angeles-mayor-race-city-council-district-nine-forum-bass-raman-2026-november-election'
LAISTJEW = 'https://laist.com/news/politics/karen-bass-nithya-raman-gaza-jewish-federation-forum'
LAISTDON = 'https://laist.com/news/politics/la-mayor-race-bass-raman-donors-campaign-finance-sosnick-airbnb'
THR = 'https://www.hollywoodreporter.com/news/politics-news/nithya-raman-hollywood-position-karen-bass-polls-1236720525/'
OURW = 'https://www.ourweekly.com/2026/09/11/nithya-raman-announces-new-endorsement/'
FOX = 'https://www.foxla.com/news/kenneth-mejia-endorses-nithya-raman-la-mayor'

# ------------------------------------------------------------------ speech archive
SH = ['speech_id', 'candidate_id', 'event_id', 'date', 'speech_title', 'speech_url',
      'transcript_url', 'duration', 'main_topics', 'major_quotes', 'rhetorical_devices',
      'opponent_references', 'personal_story_elements', 'policy_claims', 'source_urls',
      'source', 'verification_status']
S = []


def sp(**k):
    S.append([k.get(h, 'unknown') for h in SH])


sp(speech_id='SPE-BAS-0001', candidate_id='BASS', event_id='BAS-EVT-0002', date='2025-12-13',
   speech_title='Reelection launch rally remarks',
   speech_url=ABC7RALLY, transcript_url='unknown', duration='unknown',
   main_topics='Coalition; Trump administration; Palisades recovery; affordability; homelessness; crime; downtown business',
   major_quotes='"This is just overwhelming. I have to tell you my heart is so full." / "They say we can\'t come together. ... But we all come together always." / "Who would have imagined that we would have to defend ourselves from our very government?"',
   rhetorical_devices='Repetition of the "can\'t come together" formula followed by a rebuttal; rhetorical question; first-person testimony about a "hell of a year".',
   opponent_references='None named; the adversary is the federal government rather than a rival candidate.',
   personal_story_elements='Her own emotional response to the crowd and her long residence in the city ("the city I\'ve been in my whole life").',
   policy_claims='Executive Order No. 1 codified by the Council; two-year reductions in street homelessness via Inside Safe; permanent al fresco programme; crime and emissions progress.',
   source_urls=cell(ABC7RALLY), source='ABC7 Los Angeles (CNS wire), quoting the speech',
   verification_status='verified')
sp(speech_id='SPE-BAS-0002', candidate_id='BASS', event_id='unknown', date='unknown',
   speech_title='Remarks on federal immigration enforcement (MacArthur Park period)',
   speech_url=LTAFF, transcript_url='unknown', duration='unknown',
   main_topics='ICE operations; defending Angelenos; family',
   major_quotes='"When someone comes after your family, you don\'t hesitate ... You stand up. You fight."',
   rhetorical_devices='Direct address; short declaratives; family metaphor.',
   opponent_references='None — attack is on federal agents.',
   personal_story_elements='Frames the city as a family under attack.',
   policy_claims='Defence of immigrants against federal enforcement.',
   source_urls=cell(LTAFF), source='L.A. Times newsletter describing the 30-second digital spot that reuses July 2025 footage',
   verification_status='partially verified')
sp(speech_id='SPE-BAS-0003', candidate_id='BASS', event_id='BAS-EVT-0011', date='2026-08-19',
   speech_title='First runoff debate: opening and exchanges',
   speech_url=SOHA_AUG, transcript_url='unknown', duration='unknown',
   main_topics='Affordability; homelessness; record defence',
   major_quotes='"You want to hear frustrated? I\'m frustrated too ... Frustration makes me fight even harder."',
   rhetorical_devices='Concession-then-pivot ("I\'m frustrated too"); triplet of policy deliverables.',
   opponent_references='Raman, by name, on housing delivery.',
   personal_story_elements='Presents herself as a fighter rather than a manager.',
   policy_claims='Street homelessness down; housing permits accelerated; RSO improvements.',
   source_urls=cell(LAISTDEB), source='LAist preview quoting the mayor at a campaign event',
   verification_status='partially verified')
sp(speech_id='SPE-BAS-0004', candidate_id='BASS', event_id='BAS-EVT-0012', date='2026-09-26',
   speech_title='South L.A. forum remarks',
   speech_url=LAISTSL, transcript_url='unknown', duration='unknown',
   main_topics='Black and brown poor residents; homelessness delivery; density; policing',
   major_quotes='"Black and brown poor folks the most have been central in my administration." / homelessness delivery is "completely disfunctional"',
   rhetorical_devices='Self-correction in public ("a lot of people are going to be mad at me"); direct concession.',
   opponent_references='Raman on density and on LAPD conduct.',
   personal_story_elements='Speaks as the mayor who grew up in the city; appeals to lived experience of South L.A. voters.',
   policy_claims='Defends LAPD behaviour during ICE operations; opposes blanket upzoning.',
   source_urls=cell(LAISTSL), source='LAist report and quotes', verification_status='verified')
sp(speech_id='SPE-BAS-0005', candidate_id='BASS', event_id='BAS-EVT-0014', date='2026-10-13',
   speech_title='Final runoff debate: closing argument',
   speech_url=CMDEB, transcript_url='unknown', duration='unknown',
   main_topics='Fitness for office; LAPD; Olympics; record',
   major_quotes='"Now is not the time to turn the city over to Nithya Raman."',
   rhetorical_devices='Closing-frame contrast; repetition of "not the time"; accusation of lying.',
   opponent_references='Sustained, by name.',
   personal_story_elements='Casts herself as the steady hand for the 2028 Olympics.',
   policy_claims='Raman would leave LAPD in disarray; her record claims are false.',
   source_urls=cell(CMDEB), source='CalMatters commentary quoting the debate',
   verification_status='verified')
sp(speech_id='SPE-BAS-0006', candidate_id='BASS', event_id='unknown', date='unknown',
   speech_title='"Know This" campaign video narration',
   speech_url=B_WHY, transcript_url='unknown', duration='unknown',
   main_topics='Record; second-term agenda; city identity',
   major_quotes='unknown', rhetorical_devices='unknown', opponent_references='unknown',
   personal_story_elements='unknown', policy_claims='unknown',
   source_urls=cell(B_WHY), source='Video embedded on the campaign site (YouTube iR5HD6oCjz0, "Mayor Karen Bass – Know This")',
   verification_status='partially verified')
sp(speech_id='SPE-RAM-0001', candidate_id='RAMAN', event_id='RAM-EVT-0002', date='2026-02-07',
   speech_title='Campaign launch statement',
   speech_url=R_WHY, transcript_url='unknown', duration='unknown',
   main_topics='Why she is running; fires; housing production; city dysfunction',
   major_quotes='"On the last day before the deadline, I announced my run for Mayor of Los Angeles. Even for me, the decision felt unexpected - but it also felt necessary."',
   rhetorical_devices='Reluctant-hero framing; anaphora of "the challenges go far beyond the fires".',
   opponent_references='City Hall as an institution rather than Bass personally.',
   personal_story_elements='Admits the decision surprised her.',
   policy_claims='Housing production has stalled; unsheltered homelessness fell but not in proportion to spending; budgets were weakened by fiscal choices.',
   source_urls=cell(R_WHY), source='Campaign "Why I\'m Running" page (written statement, not a transcript)',
   verification_status='verified')
sp(speech_id='SPE-RAM-0002', candidate_id='RAMAN', event_id='RAM-EVT-0007', date='2026-08-10',
   speech_title='Carpenters training-facility remarks',
   speech_url=CMHOMELESS, transcript_url='unknown', duration='unknown',
   main_topics='Housing production; construction jobs; permitting',
   major_quotes='"Mayors don\'t build housing." / "You are the people who build Los Angeles ... And together, we are going to build its future."',
   rhetorical_devices='Audience-as-agent turn (you build the city); bilingual code-switching between English and Spanish; plain declarative sentence as pivot.',
   opponent_references='Notes that the carpenters endorsed Bass in 2022.',
   personal_story_elements='Presents herself as a planner who knows why buildings do not get built.',
   policy_claims='Triple housing production; cut permitting time; build at all income levels.',
   source_urls=cell(CMHOMELESS), source='CalMatters column by Jim Newton quoting the speech',
   verification_status='verified')
sp(speech_id='SPE-RAM-0003', candidate_id='RAMAN', event_id='RAM-EVT-0008', date='2026-08-19',
   speech_title='First runoff debate: opening and exchanges',
   speech_url=SOHA_AUG, transcript_url='unknown', duration='unknown',
   main_topics='Affordability; housing office; red tape',
   major_quotes='Promised an office devoted to expediting housing; accused the mayor of giving red tape "lip service".',
   rhetorical_devices='Institutional proposal as the answer to a moral complaint.',
   opponent_references='Bass, by name.',
   personal_story_elements='unknown',
   policy_claims='A housing-expediting office; faster permits; more production.',
   source_urls=cell(LAISTDEB), source='LAist preview and CalMatters coverage of the debate',
   verification_status='verified')
sp(speech_id='SPE-RAM-0004', candidate_id='RAMAN', event_id='RAM-EVT-0013', date='2026-09-26',
   speech_title='South L.A. forum remarks',
   speech_url=LAISTSL, transcript_url='unknown', duration='unknown',
   main_topics='Density; establishment; displacement',
   major_quotes='"The establishment has taken the people of Los Angeles for granted."',
   rhetorical_devices='Populist anti-establishment framing; geographic fairness argument.',
   opponent_references='Bass on SB 79 and neighbourhood density.',
   personal_story_elements='unknown',
   policy_claims='Housing has been concentrated in poorer districts; density should be spread near transit.',
   source_urls=cell(LAISTSL), source='LAist report', verification_status='verified')
sp(speech_id='SPE-RAM-0005', candidate_id='RAMAN', event_id='RAM-EVT-0014', date='2026-09-29',
   speech_title='Jewish Federation forum remarks',
   speech_url=LAISTJEW, transcript_url='unknown', duration='unknown',
   main_topics='Gaza; antisemitism; city services',
   major_quotes='"A moral outrage" (characterisation of the Gaza war, as reported)',
   rhetorical_devices='Moral-language framing; contrast with the incumbent\'s vocabulary.',
   opponent_references='Implicit contrast with Bass.',
   personal_story_elements='unknown',
   policy_claims='unknown',
   source_urls=cell(LAISTJEW), source='LAist report plus full forum audio',
   verification_status='partially verified')
sp(speech_id='SPE-RAM-0006', candidate_id='RAMAN', event_id='RAM-EVT-0016', date='2026-10-13',
   speech_title='Final runoff debate: opening and exchanges',
   speech_url=CMDEB, transcript_url='unknown', duration='unknown',
   main_topics='Incumbent record; LAPD chief; housing production; fire response',
   major_quotes='"Four years of decline, of mismanagement, of excuses." / the mayor was "MIA" / "lip service"',
   rhetorical_devices='Tricolon of nouns; acronym-like epithet ("MIA"); repetition of "lip service".',
   opponent_references='Sustained, by name.',
   personal_story_elements='unknown',
   policy_claims='Apartment construction is falling; the police chief has lost the city\'s confidence; the mayor was absent during the fire.',
   source_urls=cell(CMDEB), source='CalMatters commentary quoting the debate',
   verification_status='verified')
sp(speech_id='SPE-RAM-0007', candidate_id='RAMAN', event_id='RAM-EVT-0018', date='2026-11-03',
   speech_title='Election-night victory remarks',
   speech_url=CMWIN, transcript_url='unknown', duration='unknown',
   main_topics='Victory; city identity; volunteers',
   major_quotes='"Are you ready for an L.A. that loves you back?"',
   rhetorical_devices='Call-and-response question; second-person address; affective framing of the city as a relationship.',
   opponent_references='None reported.',
   personal_story_elements='Credits the volunteer operation that began in 2020.',
   policy_claims='unknown',
   source_urls=cell(CMWIN), source='CalMatters post-election commentary',
   verification_status='verified')

write_csv('03_speeches/speech_archive.csv', SH, S)

# ------------------------------------------------------------------ video index
VH = ['video_id', 'candidate_id', 'video_url', 'date', 'duration', 'event_type', 'main_topics',
      'relevant_timestamps', 'transcript_available', 'visual_observations', 'completeness',
      'source_urls', 'verification_status']
V = []


def vd(**k):
    V.append([k.get(h, 'unknown') for h in VH])


vd(video_id='VID-0001', candidate_id='JOINT', video_url='https://www.youtube.com/watch?v=AkuJMniInXQ',
   date='2026-05-05', duration='unknown', event_type='debate',
   main_topics='Housing; homelessness; public safety; incumbent record',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — the archive did not view the video; the upload is titled "SOHA May 2026 Mayoral Debate" on the Sherman Oaks HOA channel.',
   completeness='full', source_urls=cell(WIKI), verification_status='verified')
vd(video_id='VID-0002', candidate_id='JOINT', video_url='https://www.youtube.com/watch?v=8rI3A6alVHM',
   date='2026-05-06', duration='unknown', event_type='debate',
   main_topics='Housing; homelessness; public safety',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. NBCLA upload of the three-candidate primary debate.',
   completeness='full', source_urls=cell(WIKI), verification_status='verified')
vd(video_id='VID-0003', candidate_id='JOINT', video_url=SOHA_AUG,
   date='2026-08-19', duration='unknown', event_type='debate',
   main_topics='Affordability; housing; homelessness',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. SOHA upload of the first runoff debate.',
   completeness='full', source_urls=cell(LAISTDEB), verification_status='verified')
vd(video_id='VID-0004', candidate_id='JOINT', video_url='https://www.youtube.com/watch?v=mg8EOrjyMRk&pp=0gcJCY8Co7VqN5tD&ra=m',
   date='2026-10-13', duration='unknown', event_type='debate',
   main_topics='Public safety; housing; fire response; fitness for office',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. NBCLA upload titled "Full debate: Karen Bass vs. Nithya Raman for LA mayor".',
   completeness='full', source_urls=cell(CMDEB), verification_status='verified')
vd(video_id='VID-0005', candidate_id='JOINT', video_url='https://www.youtube.com/watch?v=6I7yezAbueM',
   date='2026-09-29', duration='unknown', event_type='forum',
   main_topics='Gaza; antisemitism; city services',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. Jewish Federation of Los Angeles upload.',
   completeness='full', source_urls=cell(LAISTJEW), verification_status='verified')
vd(video_id='VID-0006', candidate_id='RAMAN', video_url='https://www.youtube.com/watch?v=fkZkM7EH-VY',
   date='unknown', duration='unknown', event_type='campaign_video',
   main_topics='Acceptance and thanks',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. oEmbed title: "I am deeply honored to be your next mayor, LA".',
   completeness='unknown', source_urls=cell(R_WHY), verification_status='partially verified')
vd(video_id='VID-0007', candidate_id='RAMAN', video_url='https://www.youtube.com/watch?v=NH9_bZQ7AyA',
   date='unknown', duration='unknown', event_type='issue_video',
   main_topics='Homelessness causes',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. oEmbed title: "Why did homelessness rise in LA?".',
   completeness='unknown', source_urls=cell(R_HOM), verification_status='partially verified')
vd(video_id='VID-0008', candidate_id='RAMAN', video_url='https://www.youtube.com/watch?v=B-dA-DYMJwQ',
   date='unknown', duration='unknown', event_type='issue_video',
   main_topics='Encampment policy',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. oEmbed title: "Nithya\'s Plan for Addressing Encampments in Los Angeles".',
   completeness='unknown', source_urls=cell(R_HOM), verification_status='partially verified')
vd(video_id='VID-0009', candidate_id='RAMAN', video_url='https://www.youtube.com/watch?v=I41TFtz_ywA',
   date='unknown', duration='unknown', event_type='issue_video',
   main_topics='Rent; housing production; bureaucracy',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. oEmbed title: "Let\'s lower the rent! As Mayor, I\'ll triple housing production and eliminate pointless bureaucracy."',
   completeness='unknown', source_urls=cell(R_HOU), verification_status='partially verified')
vd(video_id='VID-0010', candidate_id='RAMAN', video_url='https://www.youtube.com/watch?v=taKInZXZz5M',
   date='unknown', duration='unknown', event_type='issue_video',
   main_topics='Palisades recovery',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. oEmbed title: "Nithya Raman\'s Palisades Recovery Plan".',
   completeness='unknown', source_urls=cell(R_PAL), verification_status='partially verified')
vd(video_id='VID-0011', candidate_id='RAMAN', video_url='https://www.youtube.com/watch?v=8jN4-CMiv8I',
   date='unknown', duration='unknown', event_type='issue_video',
   main_topics='Tenant story; eviction',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. oEmbed title: "Hayley\'s landlord gave her an impossible ultimatum, but Nithya Raman said NOT TODAY!".',
   completeness='unknown', source_urls=cell(R_RENT), verification_status='partially verified')
vd(video_id='VID-0012', candidate_id='RAMAN', video_url='https://www.youtube.com/watch?v=lNXuCMcvV6Q',
   date='unknown', duration='unknown', event_type='issue_video',
   main_topics='Traffic deaths; street safety',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. oEmbed title: "There were more traffic deaths than homicides in 2025. I\'m running to make LA streets safer for all!".',
   completeness='unknown', source_urls=cell(R_TRANS), verification_status='partially verified')
vd(video_id='VID-0013', candidate_id='BASS', video_url='https://www.youtube.com/watch?v=iR5HD6oCjz0',
   date='unknown', duration='unknown', event_type='campaign_video',
   main_topics='Incumbent record; second term',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. oEmbed title: "Mayor Karen Bass – Know This" on the Re-Elect Karen Bass channel.',
   completeness='unknown', source_urls=cell(B_WHY), verification_status='partially verified')
vd(video_id='VID-0014', candidate_id='RAMAN', video_url='https://www.youtube.com/watch?v=Lrum87XgwWA',
   date='unknown', duration='unknown', event_type='advertisement',
   main_topics='Emmy-themed ad; change; affordability',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. oEmbed title: "For your consideration: Nithya Raman Emmy Awards ad".',
   completeness='unknown', source_urls=cell(LTAFF), verification_status='partially verified')
vd(video_id='VID-0015', candidate_id='RAMAN', video_url=THR,
   date='2026-10-01', duration='unknown', event_type='interview',
   main_topics='Hollywood; production; industry policy',
   relevant_timestamps='unknown', transcript_available='no',
   visual_observations='unknown — not viewed. The trade-paper page carries an embedded video interview; its duration is not machine-readable.',
   completeness='clip', source_urls=cell(THR), verification_status='partially verified')

write_csv('03_speeches/speech_video_index.csv', VH, V)
