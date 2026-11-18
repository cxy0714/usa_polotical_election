# -*- coding: utf-8 -*-
"""press coverage, finance, results, polling."""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.dirname(HERE)
SRC = {r['source_id']: r for r in csv.DictReader(open(os.path.join(CASE, '09_sources', 'sources.csv'), encoding='utf-8'))}


def s(i):
    return '%s|%s' % (i, SRC[i]['url'])


def W(rel, header, rows):
    p = os.path.join(CASE, rel)
    with open(p, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(header)
        for r in rows:
            assert len(r) == len(header), (rel, r[0], len(r), len(header))
            w.writerow(r)
    print('%-46s %3d rows' % (rel, len(rows)))


# ---------------- media coverage
CH = ['coverage_id', 'candidate_id', 'event_id', 'publication_date', 'outlet', 'author', 'title', 'url',
      'source_tier', 'coverage_type', 'key_framing', 'notable_quotes', 'framing_of_candidate',
      'mentions_opponent', 'reliability_notes']
COV = [
 ('SRC-0004', 'OSSOFF', 'OSS-EVT-013', 'news_report', 'Result story: Ossoff wins by 18 points and frames it as a national rebuke.',
  '"Tonight, we\'ve struck a necessary and undeniable blow on behalf of justice and progress"', 'victorious; magnanimous',
  'yes', 'Full article readable; quotes verified against the report.'),
 ('SRC-0002', 'OSSOFF', 'unknown', 'news_report', 'Network call: Ossoff defeats Collins and Democrats hold the seat.',
  'unknown', 'winner', 'yes', 'Body readable; CBS video 4:26 embedded but URL not captured.'),
 ('SRC-0003', 'OSSOFF', 'unknown', 'news_report', 'Live results page; county table rendered client-side and unusable.',
  'unknown', 'neutral', 'yes', 'Only statewide totals readable; NBC showed 4,182,642 votes at 99% of expected.'),
 ('SRC-0016', 'OSSOFF', 'OSS-EVT-007', 'news_report', 'Debate one: personal insults dominate as the two trade attacks on wealth and race.',
  '"You\'re not just lying about my record. You\'re lying about a young woman\'s death"', 'combative; on the offensive',
  'yes', 'Long readable report; quotes matched to speaker.'),
 ('SRC-0017', 'OSSOFF', 'OSS-EVT-008', 'news_report', 'Debate two: immigration, Iran and Epstein, plus an ethics-investigation exchange.',
  '"This is a race between Georgia and Georgetown"', 'combative', 'yes', 'Readable; pool photo credited.'),
 ('SRC-0018', 'OSSOFF', 'OSS-EVT-004', 'news_report', 'Savannah rally: staged unity event with teleprompter and coached crowd.',
  '"Toys out the stroller"', 'energetic but scripted', 'yes', 'Reporter-observed staging detail; strongest source on event production.'),
 ('SRC-0019', 'OSSOFF', 'OSS-EVT-002', 'news_report', 'February rally: response to the FBI search, with a campaign crowd estimate.',
  '"the first light of dawn is on the horizon"', 'defiant', 'yes', 'Crowd figure is campaign-supplied.'),
 ('SRC-0020', 'COLLINS', 'COL-EVT-008', 'news_report', 'Runoff night: Collins wins and calls for party unity.',
  '"stand united around one mission ... get rid of that Jon Ossoff"', 'triumphant; conciliatory', 'yes', 'Readable.'),
 ('SRC-0021', 'COLLINS', 'COL-EVT-011', 'news_report', 'Kemp endorses Collins after campaigning against him in the primary.',
  'unknown', 'normalised by the party', 'yes', 'Statement-based story, no event.'),
 ('SRC-0022', 'COLLINS', 'COL-EVT-012', 'news_report', 'Thune visit: national GOP writes off the governor\'s race but not the Senate race.',
  '"I wouldn\'t be here if I didn\'t think that we could win the state of Georgia"', 'underdog with national backing',
  'yes', 'Readable; includes ad-spending figures.'),
 ('SRC-0023', 'COLLINS', 'COL-EVT-016', 'news_report', 'Trump rally in Dalton: base turnout in north Georgia as early voting starts.',
  '"thank you for your leadership, your backbone"', 'loyal lieutenant', 'yes', 'Readable.'),
 ('SRC-0024', 'OSSOFF', 'OSS-EVT-010', 'news_report', 'Harris and Ossoff court HBCU students in the final week.',
  '"have already shattered every turnout record for young voters"', 'coalition-builder', 'yes', 'Readable.'),
 ('SRC-0026', 'COLLINS', 'COL-EVT-004', 'news_report', 'Toccoa coffee-shop stop: front-runner campaigning on Ossoff, not on rivals.',
  'unknown', 'front-runner', 'yes', 'Readable; voters interviewed were undecided.'),
 ('SRC-0028', 'OSSOFF', 'OSS-EVT-005', 'news_report', 'Press call pressing Collins on a white-nationalist influencer in his business.',
  '"Instead of answering for his own record, Ossoff spent today\'s press conference repeating the same tired attacks"', 'aggressive',
  'yes', 'Both sides quoted.'),
 ('SRC-0029', 'COLLINS', 'COL-EVT-010', 'news_report', 'Savannah Q&A: Collins says the government has "a liability" to Jan. 6 defendants.',
  '"That\'s easy, yes sir"', 'unscripted; off-message', 'yes', 'Readable; campaign clarification included.'),
 ('SRC-0033', 'OSSOFF', 'OSS-EVT-012', 'news_report', 'Ossoff raises $33 million for the homestretch and votes early.',
  'unknown', 'flush with cash', 'yes', 'Readable; photo caption documents the early-voting venue.'),
 ('SRC-0035', 'OSSOFF', 'unknown', 'news_report', 'Ossoff and Warnock say they will not support DHS funding after the Minneapolis shooting.',
  'unknown', 'principled; obstructionist (per GOP)', 'yes', 'Readable; NRSC rebuttal included.'),
 ('SRC-0014', 'COLLINS', 'COL-EVT-002', 'news_report', 'Kickoff rally: pastor, state senator and a video endorsement open the campaign.',
  '"the hardworking men and women of this country will not be forgotten anymore"', 'base-first', 'yes', 'Readable.'),
 ('SRC-0013', 'COLLINS', 'COL-EVT-001', 'news_report', 'Riley family endorsement announced ahead of the kickoff.',
  'unknown', 'endorsed by victims\' family', 'yes', 'Announcement story.'),
 ('SRC-0048', 'OSSOFF', 'unknown', 'news_report', 'Three Georgia Republicans endorse Ossoff, citing constituent service and Helene relief.',
  'unknown', 'broad-appeal incumbent', 'yes', 'Readable.'),
 ('SRC-0049', 'OSSOFF', 'unknown', 'news_report', 'Jeff Flake endorses Ossoff; AJC headline-level only.',
  'unknown', 'centrist validation', 'yes', 'AJC body text is scrambled; headline-only use.'),
 ('SRC-0085', 'COLLINS', 'COL-EVT-005', 'analysis', 'Guardian profile: a candidate shaped by talk radio and grievance.',
  'unknown', 'profiled as hard-edged', 'yes', 'Readable long-form.'),
 ('SRC-0086', 'COLLINS', 'unknown', 'analysis', 'Slate investigates a young-right group chat linked to Collins\'s circle.',
  'unknown', 'scrutinised', 'yes', 'Readable; single-outlet investigation.'),
 ('SRC-0087', 'OSSOFF', 'unknown', 'analysis', 'Washington Post analysis of Ossoff\'s national profile and 2026 stakes.',
  'unknown', 'rising national figure', 'yes', 'Metered but readable.'),
 ('SRC-0089', 'COLLINS', 'unknown', 'news_report', 'Politico: Trump privately questioned whether Collins\'s abortion stance can win.',
  'unknown', 'ideologically rigid', 'yes', 'Readable.'),
 ('SRC-0093', 'OSSOFF', 'unknown', 'news_report', 'AJC: the campaign "roars to life"; headline-level only.',
  'unknown', 'energised', 'yes', 'AJC body text scrambled; headline-only use.'),
 ('SRC-0092', 'COLLINS', 'COL-EVT-003', 'news_report', 'Collins campaign releases an AI-generated video of Ossoff.',
  'unknown', 'innovative; risky', 'yes', 'Local outlet, readable.'),
]
rows = []
for i, (sid, cand, ev, ctype, framing, quotes, candframe, opp, rel) in enumerate(COV, 1):
    r = SRC[sid]
    rows.append(['COV-%03d' % i, cand, ev, r['publication_date'], r['publisher'], 'unknown', r['title'],
                 r['url'], r['source_tier'], ctype, framing, quotes, candframe, opp, rel])
W('05_campaign_media/media_coverage.csv', CH, rows)

# ---------------- finance
FH = ['finance_id', 'candidate_id', 'period', 'report_type', 'reporting_deadline', 'receipts',
      'individual_contributions', 'pac_contributions', 'disbursements', 'cash_on_hand', 'debts_owed',
      'source_urls', 'verification_status', 'notes']
FIN = [
 ['FIN-001', 'OSSOFF', '2025-Q4', 'quarterly', '2025-12-31', 'unknown', 'unknown', 'unknown', 'unknown',
  '25000000', 'unknown', s('SRC-0034'), 'verified', 'Entered 2026 with about $25 million in the bank.'],
 ['FIN-002', 'OSSOFF', '2026-Q2', 'quarterly', '2026-06-30', '20000000', 'unknown', 'unknown', 'unknown',
  '42000000', 'unknown', s('SRC-0032'), 'verified',
  'Second-quarter haul; campaign said total raised for the cycle had reached $81 million and the average contribution was about $40.'],
 ['FIN-003', 'OSSOFF', '2026-Q3', 'quarterly', '2026-09-30', '33000000', 'unknown', 'unknown', 'unknown',
  '26000000', 'unknown', s('SRC-0033'), 'verified', 'July-September haul; also transferred $3.6 million to other Democrats.'],
 ['FIN-004', 'OSSOFF', '2026-Q3', 'cumulative', '2026-10-15', '136610982', 'unknown', 'unknown', '125808380',
  '15134336', 'unknown', s('SRC-0001'), 'verified',
  'FEC totals as of the 14 October 2026 filing, as tabulated in the Wikipedia fundraising table.'],
 ['FIN-005', 'COLLINS', '2026-Q2', 'quarterly', '2026-06-30', '2100000', 'unknown', 'unknown', 'unknown',
  '2200000', 'unknown', s('SRC-0032'), 'verified',
  'About 16,000 donations, average $19.05, per the campaign.'],
 ['FIN-006', 'COLLINS', '2026-Q3', 'quarterly', '2026-09-30', '2700000', 'unknown', 'unknown', 'unknown',
  '1100000', 'unknown', s('SRC-0033'), 'verified', 'Described by the outlet as a "comparably feeble" haul.'],
 ['FIN-007', 'COLLINS', '2026-Q3', 'cumulative', '2026-10-15', '10679277', 'unknown', 'unknown', '10178766',
  '1103682', 'unknown', s('SRC-0001'), 'verified', 'FEC totals as of the 14 October 2026 filing.'],
 ['FIN-008', 'COLLINS', '2026-Q3', 'outside_spending', '2026-09-30', '25900000', 'unknown', 'unknown',
  '25900000', 'unknown', 'unknown', s('SRC-0022'), 'verified',
  'Senate Leadership Fund / One Nation spending in Georgia, including a $1.7 million week; $17.3 million more reserved for TV.'],
]
W('06_campaign_finance/campaign_finance.csv', FH, FIN)

# ---------------- results
RH = ['race_id', 'race_name', 'election_date', 'candidate', 'party', 'votes', 'percentage', 'winner',
      'source_urls', 'verification_status', 'notes']
RES = [
 ['GA-SEN-GOP-P', 'Georgia U.S. Senate Republican primary (first round)', '2026-05-19', 'Mike Collins', 'Republican', '369642', '40.5', 'no', s('SRC-0006'), 'verified', 'Advanced to the runoff.'],
 ['GA-SEN-GOP-P', 'Georgia U.S. Senate Republican primary (first round)', '2026-05-19', 'Derek Dooley', 'Republican', '275534', '30.2', 'no', s('SRC-0006'), 'verified', 'Advanced to the runoff.'],
 ['GA-SEN-GOP-P', 'Georgia U.S. Senate Republican primary (first round)', '2026-05-19', 'Buddy Carter', 'Republican', '229223', '25.1', 'no', s('SRC-0006'), 'verified', 'Eliminated.'],
 ['GA-SEN-GOP-P', 'Georgia U.S. Senate Republican primary (first round)', '2026-05-19', 'McColumn', 'Republican', '28447', '3.1', 'no', s('SRC-0006'), 'partially verified', 'First name not carried in the results table.'],
 ['GA-SEN-GOP-P', 'Georgia U.S. Senate Republican primary (first round)', '2026-05-19', 'Coyne', 'Republican', '9850', '1.1', 'no', s('SRC-0006'), 'partially verified', 'First name not carried in the results table.'],
 ['GA-SEN-GOP-R', 'Georgia U.S. Senate Republican primary runoff', '2026-06-16', 'Mike Collins', 'Republican', '390174', '55.5', 'yes', s('SRC-0007'), 'verified', 'Won after Trump endorsed him on 14 June.'],
 ['GA-SEN-GOP-R', 'Georgia U.S. Senate Republican primary runoff', '2026-06-16', 'Derek Dooley', 'Republican', '312339', '44.5', 'no', s('SRC-0007'), 'verified', 'Conceded.'],
 ['GA-SEN-DEM-P', 'Georgia U.S. Senate Democratic primary', '2026-05-19', 'Jon Ossoff', 'Democratic', '1042331', '100.0', 'yes', s('SRC-0008'), 'verified', 'Unopposed; the published total is a formality.'],
 ['GA-SEN-GEN', 'Georgia U.S. Senate general election', '2026-11-03', 'Jon Ossoff', 'Democratic', '2469037', '59.03', 'yes', s('SRC-0001'), 'verified', 'Infobox totals.'],
 ['GA-SEN-GEN', 'Georgia U.S. Senate general election', '2026-11-03', 'Mike Collins', 'Republican', '1713664', '40.97', 'no', s('SRC-0001'), 'verified', 'Conceded on election night.'],
]
W('07_electoral_context/election_results.csv', RH, RES)

# ---------------- county results (header only: no published county table retrievable)
W('07_electoral_context/county_results.csv',
  ['county_id', 'county', 'ossoff_votes', 'collins_votes', 'other_votes', 'ossoff_pct', 'collins_pct',
   'total_votes', 'source_urls', 'verification_status'], [])

# ---------------- polling
PH = ['poll_id', 'pollster', 'sponsor', 'field_start', 'field_end', 'population', 'sample_size',
      'margin_of_error', 'ossoff_pct', 'collins_pct', 'other_pct', 'undecided_pct', 'leader', 'margin',
      'source_urls', 'verification_status', 'notes']
POLL = [
 ['POLL-001', 'Research Co.', 'Research Co.', '2026-10-31', '2026-11-02', 'likely voters', '450', '4.6',
  '55', '45', 'unknown', 'unknown', 'Ossoff', '10.0', s('SRC-0057'), 'verified',
  'Six-state online survey; 450 likely voters per state. The Wikipedia polling table lists 52-42 for the same pollster, which does not match the published release.'],
 ['POLL-002', 'InsiderAdvantage', 'James Magazine', '2026-10-31', '2026-11-02', 'likely voters', '2500', '1.96',
  '53', '46', 'unknown', '1', 'Ossoff', '7.0', s('SRC-0058'), 'verified', 'Final InsiderAdvantage poll of the cycle.'],
 ['POLL-003', 'Echelon Insights', 'NetChoice', '2026-10-16', '2026-10-23', 'likely voters', '508', '5.2',
  '55', '40', '3', '2', 'Ossoff', '15.0', s('SRC-0059'), 'verified', 'Libertarian Buckley at 3%.'],
 ['POLL-004', 'Big Data Poll', 'Big Data Poll', '2026-09-21', '2026-09-23', 'likely voters', '678', 'unknown',
  '52.2', '41.0', 'unknown', 'unknown', 'Ossoff', '11.2', s('SRC-0060'), 'verified',
  'Also reported 51.0-40.1 among registered voters; leaners shrink the lead.'],
 ['POLL-005', 'Wick Research', 'Wick Research', '2026-06-27', '2026-06-30', 'likely voters', '1175', '2.9',
  '46.7', '42.9', 'unknown', '10.4', 'Ossoff', '3.8', s('SRC-0061'), 'verified', 'Text-to-web survey.'],
 ['POLL-006', 'Emerson College Polling', 'Nexstar Media', '2026-02-28', '2026-03-02', 'likely voters', '1000', '3.0',
  '48', '43', 'unknown', '9', 'Ossoff', '5.0', s('SRC-0056'), 'verified',
  'First Emerson/Nexstar Georgia survey of the cycle; Collins was not yet the nominee.'],
]
W('07_electoral_context/polling.csv', PH, POLL)
