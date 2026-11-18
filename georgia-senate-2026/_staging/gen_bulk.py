import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
refs = json.load(open(os.path.join(HERE, 'refs.json'), encoding='utf-8'))

KEEP = [
    'ajc.com', 'cbsnews.com', 'politico.com', 'apnews.com', 'gpb.org', 'atlantanewsfirst.com',
    'georgiarecorder.com', 'nytimes.com', 'washingtonreporter.news', 'domepolitics.com',
    'newschannel9.com', 'wjcl.com', 'wdef.com', 'accesswdun.com', 'mediaite.com', 'nbcnews.com',
    'npr.org', 'cnn.com', 'thehill.com', 'foxnews.com', 'ms.now', 'newjerseyglobe.com',
    'broadwayworld.com', 'insideradvantage.com', 'emersoncollegepolling.com', 'researchco.ca',
    'activote.net', 'bigdatapoll.com', 'wick.io', 'rasmussenreports.com', 'thetrafalgargroup.org',
    'tippinsights.com', 'quantusinsights.org', 'winwithjmc.com', 'fec.gov', 'results.sos.ga.gov',
    'realclearpolling.com', '270towin.com', 'decisiondeskhq.com', 'fiftyplusone.news',
    'racetothewh.com', 'giffords.org', 'lcv.org', 'splcactionfund.org', 'aipacpac.org', 'nrsc.org',
    'nrapvf.org', 'hrc.org', 'endcitizensunited.org', 'reproductivefreedomforall.org',
    'uawpower.org', 'educationvotes.nea.org', 'jstreetpac.org', 'pup-research.com',
    'netchoice.org', 'aarp.org', 'jamesmagazinega.com', 'fiftyplusone.news', 'ballotpedia.org',
]

seen, out = set(), []
for r in refs:
    host = re.sub(r'^https?://(www\.)?', '', r['url']).split('/')[0].lower()
    if not any(host.endswith(k) for k in KEEP):
        continue
    if r['url'] in seen:
        continue
    seen.add(r['url'])
    key = re.sub(r'[^a-z0-9]+', '_', (r['work'] + '_' + r['title']).lower())[:45].strip('_')
    out.append(dict(key=key or 'ref', url=r['url'], work=r['work'], title=r['title'], date=r['date']))

# additional pages discovered by navigation
extra = [
    ('gr_ossoff_wins', 'https://georgiarecorder.com/2026/11/03/u-s-sen-jon-ossoff-wins-reelection-in-georgia-and-coasts-to-a-second-term/'),
    ('gr_debate1', 'https://georgiarecorder.com/2026/10/08/collins-ossoff-trade-personal-insults-during-georgias-first-u-s-senate-debate/'),
    ('gr_debate2', 'https://georgiarecorder.com/2026/10/13/collins-ossoff-clash-in-a-second-heated-debate-as-early-voting-begins-in-georgia/'),
    ('gr_five_things', 'https://georgiarecorder.com/2026/05/13/five-things-to-know-about-the-upcoming-senate-election-in-georgia/'),
    ('gr_fbi_raid', 'https://georgiarecorder.com/2026/02/07/ossoff-tells-supporters-we-will-overcome-this-together-as-he-blasts-trump-for-fbi-raid/'),
    ('gr_save_voting', 'https://georgiarecorder.com/2026/03/18/repub/us-senate-displays-sharp-divisions-over-save-voting-bill-demanded-by-trump/'),
    ('gr_soninlaw', 'https://georgiarecorder.com/2026/07/23/ossoff-slams-senate-gop-challenger-over-silence-on-reports-of-son-in-laws-antisemitic-comments/'),
    ('gr_black_lawmakers', 'https://georgiarecorder.com/2026/08/11/four-dozen-black-georgia-lawmakers-press-collins-on-alleged-white-nationalist-ties/'),
    ('gr_thune', 'https://georgiarecorder.com/2026/09/25/top-u-s-senate-republican-stumps-with-collins-in-georgia-as-seat-appears-to-slip-out-of-reach/'),
    ('gr_20m', 'https://georgiarecorder.com/2026/07/15/ossoff-rakes-in-another-20m-building-on-fundraising-advantage-in-race-for-georgia-senate-seat/'),
    ('gr_33m', 'https://georgiarecorder.com/2026/10/15/ossoff-reports-raising-another-33-million-for-homestretch-of-u-s-senate-reelection-bid/'),
    ('gr_medicaid', 'https://georgiarecorder.com/2026/11/09/repub/democratic-wins-put-medicaid-expansion-back-in-play-in-holdout-states/'),
    ('gr_latinos', 'https://georgiarecorder.com/2026/11/11/georgias-latinos-shift-toward-democratic-candidates-for-now/'),
    ('gr_black_turnout', 'https://georgiarecorder.com/2026/11/16/rise-in-black-voter-turnout-helps-drive-historic-change-in-georgia-transforming-state-government/'),
    ('gr_blue_wave', 'https://georgiarecorder.com/2026/11/06/georgia-democrats-ride-national-blue-wave-into-power-in-history-making-election/'),
    ('wiki_ossoff_page', 'https://en.wikipedia.org/wiki/Jon_Ossoff'),
    ('wiki_2026_sen_page', 'https://en.wikipedia.org/wiki/2026_United_States_Senate_elections'),
    ('commons_ossoff_portrait', 'https://commons.wikimedia.org/wiki/File:Jon_Ossoff_Senate_Portrait_2021_(cropped).jpg'),
    ('commons_collins_portrait', 'https://commons.wikimedia.org/wiki/File:Rep._Mike_Collins_official_photo,_118th_Congress_(cropped).jpg'),
]
for k, u in extra:
    if u not in seen:
        seen.add(u)
        out.append(dict(key=k, url=u, work='', title='', date=''))

json.dump(out, open(os.path.join(HERE, 'urls_bulk.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'urls to fetch')
