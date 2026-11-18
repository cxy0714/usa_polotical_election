# -*- coding: utf-8 -*-
import io, os, sys

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sources_data.py')
s = io.open(p, encoding='utf-8').read()

REPL = [
    ('https://www.afm47.org/2026-election-endorsements/', 'https://afm47.org/press/afm-47-endorses-karen-bass-for-mayor-of-los-angeles/'),
    ('https://www.emersoncollegepolling.com/california-2026-poll-becerra-continues-to-surge-in-democratic-primary-for-governor/',
     'https://emersoncollegepolling.com/california-2026-poll-becerra-continues-to-surge-steyer-and-hilton-compete-for-second-spot/'),
    ('https://manhattan.institute/article/californias-contradictions-survey-analysis-of-2026-voter-preferences-statewide-and-los-angeles',
     'https://manhattan.institute/article/californias-contradictions-survey-analysis-of-2026-voter-preferences-statewide-and-in-los-angeles'),
    ('https://www.nypost.com/2026/10/22/us-news/karen-bass-trails-nithya-raman-in-la-mayoral-poll-with-high-disapproval-rating/',
     'https://nypost.com/2026/10/22/us-news/karen-bass-trails-nithya-raman-in-la-mayoral-poll-with-high-disapproval-rating/'),
    ('https://www.cnn.com/2026/06/08/politics/nithya-raman-spencer-pratt-karen-bass-los-angeles-mayor/index.html',
     'https://www.cnn.com/2026/06/08/politics/nithya-raman-spencer-pratt-karen-bass-los-angeles-mayor-election'),
    ('https://abc7.com/post/spencer-pratt-responds-los-angeles-mayoral-race-loss-new-video/19995344/',
     'https://abc7.com/post/spencer-pratt-responds-los-angeles-mayoral-race-loss-video/19283238/'),
    ('https://www.nbcnews.com/politics/2026-election/nithya-raman-advances-spencer-pratt-karen-bass-california-primary',
     'https://www.nbcnews.com/politics/2026-election/nithya-raman-advances-spencer-pratt-face-l-mayor-karen-bass-runoff-rcna347483'),
    ('https://laist.com/brief/news/politics/los-angeles-mayor-race-city-council-district-nine-forum',
     'https://laist.com/brief/news/politics/los-angeles-mayor-race-city-council-district-nine-forum-bass-raman-2026-november-election'),
    ('https://www.latimes.com/california/newsletter/2025-11-15/la-on-the-record-an-activist-is-challenging-bass-could-she-be-l-a-s-mamdani',
     'https://www.latimes.com/california/newsletter/2025-11-15/la-on-the-record-an-activist-is-challenging-bass-from-the-left'),
    ('https://www.latimes.com/california/story/2026-05-19/city-council-progressives-snub-raman-endorse-bass',
     'https://www.latimes.com/california/story/2026-05-19/city-council-progressives-snub-raman-endorse-bass-in-la-mayors-race'),
    ('https://www.latimes.com/california/story/2026-09-23/raman-takes-big-lead-over-bass-in-latest-poll-for-la-mayor',
     'https://www.latimes.com/california/story/2026-09-23/raman-takes-big-lead-over-bass-in-latest-poll-for-la-mayors-race'),
    ('https://www.latimes.com/california/story/2026-09-01/raman-gets-key-labor-endorsement-in-mayors-race-although-many-unions-back-bass',
     'https://www.latimes.com/california/story/2026-09-01/raman-gets-key-labor-endorsement-in-mayors-race-although-most-unions-are-backing-bass'),
    ('https://www.latimes.com/california/story/2026-10-20/supervisor-lindsey-horvath-endorses-nithya-raman-for-mayor',
     'https://www.latimes.com/california/story/2026-10-20/lindsey-horvath-endorses-nithya-raman-for-mayor'),
    ('https://www.latimes.com/california/story/2026-10-20/rick-caruso-has-extreme-concern-over-raman-but-declines-to-endorse',
     'https://www.latimes.com/california/story/2026-10-20/rick-caruso-has-extreme-concern-over-raman-but-declines-to-endorse-in-mayors-race'),
    ('https://www.latimes.com/california/newsletter/2026-01-17/palisades-fire-permit-relief',
     'https://www.latimes.com/california/newsletter/2026-01-17/palisades-fire-victim-rebuilding-permits-la-on-the-record'),
    ('https://www.latimes.com/politics/story/2026-06-04/primary-election-2026-map-mayor-neighborhood-results-precincts"',
     'https://www.latimes.com/politics/story/2026-06-04/primary-election-2026-map-mayor-neighborhood-results-precincts/"'),
    ('https://www.hollywoodreporter.com/news/politics-news/nithya-raman-hollywood-position-karen-bass-polls-12367205/',
     'https://www.hollywoodreporter.com/news/politics-news/nithya-raman-hollywood-position-karen-bass-polls-1236720525/'),
    ('https://deadline.com/2026/05/iatse-endorses-karen-bass-la-mayor-race-1236420118/',
     'https://deadline.com/2026/05/karen-bass-iatse-los-angeles-mayor-race-1236916610/'),
    ('https://www.thewrap.com/jane-fonda-endorses-karen-bass-los-angeles-mayor/',
     'https://www.thewrap.com/media-platforms/politics/jane-fonda-endorses-mayor-karen-bass-reelection-exclusive/'),
    ('https://www.westsidecurrent.com/elections/column-the-649-000-reasons-traci-park-is-treating-the-2026-election-seriously-and-other-campaign-finance-takeaways/article_2acab222-2301-473a-aa44-333e44906eaf.html',
     'https://www.westsidecurrent.com/elections/column-the-649-000-reasons-traci-park-is-treating-the-2026-election-seriously-and-other/article_2acab222-2301-473a-aa44-333e44906eaf.html'),
    ('https://www.dailynews.com/2026/03/20/four-of-five-la-county-supervisors-endorse-karen-bass-for-mayor/',
     'https://www.dailynews.com/2026/03/20/four-of-the-five-la-county-supervisors-endorsed-karen-bass-for-mayor/'),
    ('https://www.theguardian.com/us-news/2026/06/09/spencer-pratt-la-mayor-bid-fell-flat',
     'https://www.theguardian.com/us-news/2026/jun/09/spencer-pratt-la-mayor-election'),
    ('https://www.youtube.com/watch?v=fVzKUvSstY4"', 'https://www.youtube.com/watch?v=fVzKUvSstY4&ra=m"'),
    ('https://www.youtube.com/watch?v=mg8EOrjyMRk"', 'https://www.youtube.com/watch?v=mg8EOrjyMRk&pp=0gcJCY8Co7VqN5tD&ra=m"'),
    ('"Her election night party at the Greek Theater in Griffith Park was an outpouring of exuberant energy"',
     '"Are you ready for an L.A. that loves you back?"'),
    ('"critical of City Hall\'s spending choices"', '"criticized City Hall\'s spending choices"'),
]

for a, b in REPL:
    if a not in s:
        print('MISS:', a[:80])
    s = s.replace(a, b)

# drop the blocked AP article entry entirely
lines = s.split('\n')
out = []
skip = 0
for i, ln in enumerate(lines):
    if 'apnews.com/article/los-angeles-mayor-karen-bass-nithya-raman-8c9a5b5538d90719924c59b324f2fd0' in ln:
        skip = 8  # URL line + 7 following lines (tuple body + closing)
    if skip:
        skip -= 1
        continue
    out.append(ln)
s = '\n'.join(out)

io.open(p, 'w', encoding='utf-8').write(s)
print('patched')
