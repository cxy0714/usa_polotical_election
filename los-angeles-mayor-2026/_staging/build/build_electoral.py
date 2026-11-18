# -*- coding: utf-8 -*-
"""Electoral context: results, polling, finance."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import cell, write_csv  # noqa: E402

WIKI = 'https://en.wikipedia.org/w/index.php?title=2026_Los_Angeles_mayoral_election&action=raw'
NBCR = 'https://www.nbcnews.com/politics/2026-primary-elections/los-angeles-mayor-results'
APR = 'https://apnews.com/projects/elections-2026/california-los-angeles-mayor-results/'
CLERK = 'https://cityclerk.lacity.org/election/2026_Nominating_Petition_Filing_Status.pdf'
ETH = 'https://ethics.lacity.gov/elections'
LAISTD = 'https://laist.com/news/politics/la-mayor-race-bass-raman-donors-campaign-finance-sosnick-airbnb'
NBCPOLL = 'https://www.nbclosangeles.com/elections/karen-bass-nithya-raman-la-mayor-election-poll/3962255/'
NBCOCT = 'https://www.nbclosangeles.com/elections/karen-bass-nithya-raman-la-mayor-election-poll/3962255/'
LATSEP23 = 'https://www.latimes.com/california/story/2026-09-23/raman-takes-big-lead-over-bass-in-latest-poll-for-la-mayors-race'
LATSEP19 = 'https://www.latimes.com/california/newsletter/2026-09-19/los-angeles-mayoral-ad-blitz-hollywood-ice-homelessness'
NYPOST = 'https://nypost.com/2026/10/22/us-news/karen-bass-trails-nithya-raman-in-la-mayoral-poll-with-high-disapproval-rating/'
MANH = 'https://manhattan.institute/article/californias-contradictions-survey-analysis-of-2026-voter-preferences-statewide-and-in-los-angeles'

# ---------------------------------------------------------------- results
PRIMARY = [
    ('Karen Bass', 'Nonpartisan', 292593, '34.3', 'yes', 'verified',
     'Top finisher. NBC News results JSON and the Wikipedia table agree on 292,593.'),
    ('Nithya Raman', 'Nonpartisan', 247781, '29.0', 'yes', 'verified',
     'Second finisher; advanced to the Nov. 3 runoff. NBC News and Wikipedia agree.'),
    ('Spencer Pratt', 'Nonpartisan', 217977, '25.5', 'no', 'verified',
     'Third; eliminated. NBC News and Wikipedia agree.'),
    ('Adam Miller', 'Nonpartisan', 30008, '3.5', 'no', 'verified',
     'Percentage computed from votes/853,894, rounded to 0.1 (not printed in the retrieved results page).'),
    ('Rae Chen Huang', 'Nonpartisan', 25220, '3.0', 'no', 'verified',
     'Percentage computed from votes/total.'),
    ('Juanita Lopez', 'Nonpartisan', 13033, '1.5', 'no', 'conflicting sources',
     'NBC News gives 13,033; the Wikipedia table gives 13,032. One-vote discrepancy recorded, not adjusted.'),
    ('Andrew Kim', 'Nonpartisan', 6988, '0.8', 'no', 'verified',
     'Percentage computed from votes/total.'),
    ('Suzy Kim', 'Nonpartisan', 6051, '0.7', 'no', 'verified',
     'Percentage computed from votes/total.'),
    ('Asaad Alnajjar', 'Nonpartisan', 4063, '0.5', 'no', 'verified',
     'Percentage computed from votes/total.'),
    ('Bryant Acosta', 'Nonpartisan', 3471, '0.4', 'no', 'conflicting sources',
     'NBC News gives 3,471; the Wikipedia table gives 3,470. One-vote discrepancy recorded, not adjusted.'),
    ('John Logsdon', 'Nonpartisan', 3029, '0.4', 'no', 'verified',
     'Percentage computed from votes/total.'),
    ('Tish Hyman', 'Nonpartisan', 1640, '0.2', 'no', 'verified',
     'Percentage computed from votes/total.'),
    ('Andrej Selivra', 'Nonpartisan', 1159, '0.1', 'no', 'verified',
     'Percentage computed from votes/total.'),
    ('Nelson Cheng', 'Nonpartisan', 881, '0.1', 'no', 'verified',
     'Percentage computed from votes/total.'),
]
RUNOFF = [
    ('Nithya Raman', 'Nonpartisan', 615264, '54.9', 'yes', 'partially verified',
     'Winner. Totals available only from the Wikipedia results table in this environment (AP live page served no static figures).'),
    ('Karen Bass', 'Nonpartisan', 504959, '45.1', 'no', 'partially verified',
     'Incumbent defeated. Same single-source caveat as the winner row.'),
]

rows = []
for name, party, votes, pct, win, ver, note in PRIMARY:
    rows.append(['LA-MAYOR-2026-P', 'Los Angeles mayor, primary (top-two)', '2026-06-02',
                 name, party, votes, pct, win, cell(NBCR), ver, note])
for name, party, votes, pct, win, ver, note in RUNOFF:
    rows.append(['LA-MAYOR-2026-R', 'Los Angeles mayor, runoff', '2026-11-03',
                 name, party, votes, pct, win, cell(WIKI), ver, note])

write_csv('07_electoral_context/election_results.csv',
          ['race_id', 'race_name', 'election_date', 'candidate', 'party', 'votes', 'percentage',
           'winner', 'source_urls', 'verification_status', 'notes'], rows)

# ---------------------------------------------------------------- county (header only)
write_csv('07_electoral_context/county_results.csv',
          ['county_id', 'county', 'raman_votes', 'bass_votes', 'other_votes', 'raman_pct',
           'bass_pct', 'total_votes', 'source_urls', 'verification_status'], [])

# ---------------------------------------------------------------- polling
POLLS = [
    ('POLL-0001', 'Berkeley Institute of Governmental Studies (IGS)', 'Los Angeles Times (co-sponsor)',
     '2026-10-19', '2026-10-25', 'LV', 2197, '3.0', 40, 40, 'unknown', 19, 'tie', 0,
     cell(NBCPOLL), 'verified',
     'Final pre-election poll. NBC4 reported "each candidate received 40% support" and about 20% undecided; the Wikipedia table gives 19%. Published figures sum to 99 (rounding).'),
    ('POLL-0002', 'McLaughlin & Associates (R)', 'California Post',
     '2026-10-15', '2026-10-18', 'LV', 400, 'unknown', 47, 39, 'unknown', 14, 'raman', 8,
     cell(NYPOST), 'verified',
     'Republican pollster for the New York Post\'s California Post; reported as "Raman leads Bass 47% to 39%". Sums to 100.'),
    ('POLL-0003', 'Impact Research (D)', 'unknown',
     '2026-10-02', '2026-10-07', 'LV', 773, 'unknown', 43, 33, 'unknown', 23, 'raman', 10,
     cell(WIKI), 'partially verified',
     'Only the Wikipedia polling table carries this survey; no sponsor or margin of error reported. Sums to 99 (rounding).'),
    ('POLL-0004', 'Manhattan Institute', 'Manhattan Institute',
     '2026-09-24', '2026-10-01', 'LV', 449, '4.6', 39, 36, 15, 10, 'raman', 3,
     cell(MANH), 'verified',
     'With leaners pushed. The same report gives an initial trial heat of Raman 38 / Bass 32 (six-point lead); the table here records the leaned result and the notes carry both.'),
    ('POLL-0005', 'Berkeley Institute of Governmental Studies (IGS)', 'Los Angeles Times (co-sponsor)',
     '2026-09-15', '2026-09-20', 'LV', 2150, '3.0', 39, 28, 'unknown', 33, 'raman', 11,
     cell(LATSEP23), 'verified',
     'Reported as "Raman is favored by 39% of likely L.A. voters, compared with 28% for Bass... 33% of voters were undecided". Sums to 100.'),
    ('POLL-0006', 'Hart Research Associates (D)', 'Raman campaign (internal memo)',
     '2026-09-01', '2026-09-09', 'LV', 600, '4.0', 44, 39, 'unknown', 17, 'raman', 5,
     cell(LATSEP19), 'verified',
     'Campaign-released internal poll reported by The Times: "44% supported Raman and 39% backed Bass, with 17% undecided". Sums to 100.'),
    ('POLL-0007', 'Tavern Research (D)', 'unknown',
     '2026-08-20', '2026-08-25', 'LV', 2258, '3.0', 53, 47, 'unknown', 'unknown', 'raman', 6,
     cell(WIKI), 'partially verified',
     'With leaners; no undecided share printed. Wiki table also lists an initial 38/32 line. Two-candidate shares sum to 100.'),
    ('POLL-0008', 'Tulchin Research (D)', 'unknown',
     '2026-08-01', '2026-08-31', 'LV', 1200, '2.8', 35, 41, 'unknown', 24, 'bass', 6,
     cell(WIKI), 'partially verified',
     'Field dates published only as "August 2026"; month bounds recorded with that caveat. Sums to 100.'),
]
prows = []
for (pid, pollster, sponsor, fs, fe, pop, n, moe, raman, bass, other, und, leader, margin, src, ver, note) in POLLS:
    prows.append([pid, pollster, sponsor, fs, fe, pop, n, moe, raman, bass, other, und,
                  leader, margin, src, ver, note])
write_csv('07_electoral_context/polling.csv',
          ['poll_id', 'pollster', 'sponsor', 'field_start', 'field_end', 'population',
           'sample_size', 'margin_of_error', 'raman_pct', 'bass_pct', 'other_pct',
           'undecided_pct', 'leader', 'margin', 'source_urls', 'verification_status', 'notes'],
          prows)

# ---------------------------------------------------------------- finance
FIN = [
    ('FIN-0001', 'BASS', '2026-10-17', 'primary_cycle_reported_through', '2026-10-17',
     3252743, 'unknown', 'unknown', 4509228, 24800, 'unknown', cell(ETH), 'partially verified',
     'City Ethics Commission "totals by seat" table, reported through Oct. 17, 2026; includes $1,257,000 in matching funds. Individual vs PAC split not published at this level.'),
    ('FIN-0002', 'RAMAN', '2026-10-17', 'primary_cycle_reported_through', '2026-10-17',
     1015075, 'unknown', 'unknown', 2355691, 3306, 'unknown', cell(ETH), 'partially verified',
     'Same table; includes $1,257,000 in matching funds.'),
    ('FIN-0003', 'PRATT', '2026-06-30', 'primary_cycle_reported_through', '2026-06-30',
     3996187, 'unknown', 'unknown', 3737543, 98818, 'unknown', cell(ETH), 'partially verified',
     'Reported through June 30, 2026; no matching funds listed.'),
    ('FIN-0004', 'MILLER', '2026-06-30', 'primary_cycle_reported_through', '2026-06-30',
     4285242, 'unknown', 'unknown', 4163870, 175918, 'unknown', cell(ETH), 'partially verified',
     'Reported through June 30, 2026; self-funded in part per LAist candidate guide.'),
    ('FIN-0005', 'HUANG', '2026-06-30', 'primary_cycle_reported_through', '2026-06-30',
     322120, 'unknown', 'unknown', 767778, 24509, 'unknown', cell(ETH), 'partially verified',
     'Reported through June 30, 2026; includes $612,956 in matching funds.'),
    ('FIN-0006', 'BASS', '2026-10-17', 'runoff_cycle_reported_through', '2026-10-17',
     1991461, 'unknown', 'unknown', 2786034, 632333, 'unknown', cell(ETH), 'partially verified',
     'Runoff-period report as of Oct. 17, 2026; includes $1,446,697 in matching funds.'),
    ('FIN-0007', 'RAMAN', '2026-10-17', 'runoff_cycle_reported_through', '2026-10-17',
     1505815, 'unknown', 'unknown', 1692227, 1378319, 'unknown', cell(ETH), 'partially verified',
     'Runoff-period report as of Oct. 17, 2026; includes $1,507,000 in matching funds.'),
    ('FIN-0008', 'RAMAN', '2026-09-24', 'independent_expenditure_committee_receipt', '2026-09-24',
     3000000, 'unknown', 'unknown', 'unknown', 'unknown', 'unknown', cell(LAISTD), 'verified',
     'NOT candidate-committee money. Hedge-fund founder Aaron Sosnick, one of the two largest donors to the committee backing Raman; reported口径 = IE committee contribution.'),
    ('FIN-0009', 'RAMAN', '2026-09-24', 'independent_expenditure_committee_receipt', '2026-09-24',
     3000000, 'unknown', 'unknown', 'unknown', 'unknown', 'unknown', cell(LAISTD), 'verified',
     'NOT candidate-committee money. Western States Regional Council of Carpenters, the other $3m donor to the pro-Raman committee (the pair is reported as $7m total with Sosnick\'s extra $1m).'),
    ('FIN-0010', 'RAMAN', '2026-09-24', 'independent_expenditure_committee_receipt', '2026-09-24',
     1000000, 'unknown', 'unknown', 'unknown', 'unknown', 'unknown', cell(LAISTD), 'verified',
     'NOT candidate-committee money. Additional $1m from Sosnick reported by LAist, taking his total to $4m.'),
    ('FIN-0011', 'BASS', '2026-09-24', 'independent_expenditure_committee_receipt', '2026-09-24',
     4000000, 'unknown', 'unknown', 'unknown', 'unknown', 'unknown', cell(WIKI), 'partially verified',
     'NOT candidate-committee money. Airbnb-linked committee money on the Bass side; the Wikipedia summary reports it as "part of nearly $4 million". Figure rests on the Wikipedia table alone.'),
    ('FIN-0012', 'RAMAN', '2026-09-25', 'independent_expenditure_against_candidate', '2026-09-25',
     3000000, 'unknown', 'unknown', 'unknown', 'unknown', 'unknown', cell(WIKI), 'partially verified',
     'NOT candidate-committee money. Los Angeles Police Protective League money aimed at defeating Raman; row is attached to the targeted candidate, not to a supporter.'),
]
write_csv('06_campaign_finance/campaign_finance.csv',
          ['finance_id', 'candidate_id', 'period', 'report_type', 'reporting_deadline',
           'receipts', 'individual_contributions', 'pac_contributions', 'disbursements',
           'cash_on_hand', 'debts_owed', 'source_urls', 'verification_status', 'notes'], FIN)
