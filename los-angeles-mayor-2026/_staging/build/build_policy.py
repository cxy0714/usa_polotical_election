# -*- coding: utf-8 -*-
"""Policy positions and career timelines."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import cell, write_csv  # noqa: E402

WIKI = 'https://en.wikipedia.org/w/index.php?title=2026_Los_Angeles_mayoral_election&action=raw'
GUIDE = 'https://laist.com/news/politics/your-quick-guide-to-the-la-mayors-race'
B_HOW = 'https://karenbass.com/how-we-changed-la'
B_WHY = 'https://karenbass.com/why-im-running'
B_VIS = 'https://karenbass.com/term-2-vision'
R_HOU = 'https://www.nithyaforthecity.com/housing'
R_HOM = 'https://www.nithyaforthecity.com/homelessness'
R_PS = 'https://www.nithyaforthecity.com/publicsafety'
R_RENT = 'https://www.nithyaforthecity.com/renters'
R_PAL = 'https://www.nithyaforthecity.com/palisadesrecovery'
R_TRANS = 'https://www.nithyaforthecity.com/transportation'
R_WHY = 'https://www.nithyaforthecity.com/why-im-running'
R_ABOUT = 'https://www.nithyaforthecity.com/about-nithya'
ABC7RALLY = 'https://abc7.com/post/mayor-karen-bass-appear-reelection-campaign-rally-downtown-la-today/18283470/'
CMDEB = 'https://calmatters.org/commentary/2026/10/la-mayoral-debate-friends-feud/'
CMHOMELESS = 'https://calmatters.org/commentary/2026/08/los-angeles-homelessness-raman-bass/'
CMCOAL = 'https://calmatters.org/commentary/2026/06/raman-bass-mayor-political-coalitions/'
LTAFF = 'https://www.latimes.com/california/newsletter/2026-09-19/los-angeles-mayoral-ad-blitz-hollywood-ice-homelessness'
OURW = 'https://www.ourweekly.com/2026/09/11/nithya-raman-announces-new-endorsement/'
FOX = 'https://www.foxla.com/news/kenneth-mejia-endorses-nithya-raman-la-mayor'
LAISTJEW = 'https://laist.com/news/politics/karen-bass-nithya-raman-gaza-jewish-federation-forum'
LAISTSL = 'https://laist.com/brief/news/politics/los-angeles-mayor-race-city-council-district-nine-forum-bass-raman-2026-november-election'
WSC = 'https://www.westsidecurrent.com/elections/column-the-649-000-reasons-traci-park-is-treating-the-2026-election-seriously-and-other/article_2acab222-2301-473a-aa44-333e44906eaf.html'
LT24 = 'https://www.latimes.com/california/story/2024-07-01/mayor-karen-bass-files-paperwork-to-run-for-reelection'
LTCANCEL = 'https://www.latimes.com/california/story/2026-05-11/la-mayoral-forum-canceled-after-leading-candidates-pull-out'

H = ['position_id', 'candidate_id', 'issue', 'subissue', 'position_summary', 'candidate_statement',
     'statement_date', 'context', 'source_urls', 'legislative_record', 'position_changed',
     'change_notes', 'opponent_criticism', 'fact_check', 'verification_status']

P = []


def pos(**k):
    P.append([k.get(h, 'unknown') for h in H])


# ------------------------------------------------------------------ BASS
pos(position_id='BAS-POL-0001', candidate_id='BASS', issue='Other', subissue='Housing supply',
    position_summary='Claims her zoning and permitting changes are already accelerating nearly 40,000 housing units, framing production as the route to affordability.',
    candidate_statement='"Her new policies are already accelerating nearly 40,000 units of housing."',
    statement_date='unknown', context='Campaign record page "How We Changed LA"',
    source_urls=cell(B_HOW), legislative_record='Campaign credits Executive Order No. 1, codified by the City Council in December 2025, with permanently streamlining affordable-housing approvals.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman argues the city still permits too slowly and that production has stalled; she wants to triple annual output.',
    fact_check='The 40,000 figure is the campaign\'s own; no independent count of units produced versus permitted was retrieved.',
    verification_status='partially verified')
pos(position_id='BAS-POL-0002', candidate_id='BASS', issue='Other', subissue='Rent control and tenant protection',
    position_summary='Claims the first meaningful improvements to the Rent Stabilization Ordinance in four decades.',
    candidate_statement='"Mayor Bass changed the status quo by signing into the law the first improvements to the City\'s Rent Stabilization Ordinance in 40 years to limit rent increases and protect tenants."',
    statement_date='unknown', context='Campaign record page',
    source_urls=cell(B_HOW), legislative_record='Signature of the 2024 RSO amendments (ordinance number not stated on the campaign page).',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman\'s campaign claims the same RSO accomplishment for Raman\'s own council work — a direct credit-claiming collision between the two campaigns.',
    fact_check='Both campaigns claim the same 40-year-first RSO change. The archive records both claims without adjudicating authorship.',
    verification_status='conflicting sources')
pos(position_id='BAS-POL-0003', candidate_id='BASS', issue='Other', subissue='Street homelessness',
    position_summary='Claims street homelessness fell 17.5% and that the city recorded its first back-to-back annual decreases.',
    candidate_statement='"Street Homelessness Is Down 17.5 percent. ... LA has achieved its first-ever back-to-back decreases in homelessness."',
    statement_date='unknown', context='Campaign record page',
    source_urls=cell(B_HOW), legislative_record='Inside Safe and the citywide encampment strategy described on the same page.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman calls City Hall\'s homelessness spending unaccountable and says 40% of people housed through the mayor\'s program returned to the streets.',
    fact_check='The 17.5% is a campaign figure. The 2026 LAHSA count reported 45,194 people unhoused in the city, up from 43,695 — a citywide increase that is compatible with a street-count decrease but is not reconciled by either campaign.',
    verification_status='partially verified')
pos(position_id='BAS-POL-0004', candidate_id='BASS', issue='Other', subissue='Encampments and Inside Safe',
    position_summary='Presents Inside Safe as the city\'s first comprehensive encampment-to-interim-housing strategy.',
    candidate_statement='"Mayor Bass led the change by launching the city\'s first comprehensive strategy to move people inside from encampments."',
    statement_date='unknown', context='Campaign record page',
    source_urls=cell(B_HOW),
    legislative_record='Inside Safe launched by executive action in December 2022; funding renewed annually through the budget.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman cites an average cost of about $85,000 per motel room per year, with some rooms near $100,000, and argues vouchers would house three households for the same money.',
    fact_check='The $85,000 figure appears on Raman\'s campaign site; no city audit of per-room Inside Safe costs was retrieved.',
    verification_status='partially verified')
pos(position_id='BAS-POL-0005', candidate_id='BASS', issue='Other', subissue='Police hiring',
    position_summary='Took executive action to expand LAPD hiring after years of shrinkage; opposes reductions to the police budget.',
    candidate_statement='"After years of a shrinking LAPD, Mayor Bass took executive action to get more police officers hired."',
    statement_date='unknown', context='Campaign record page',
    source_urls=cell(B_HOW), legislative_record='Executive directives on hiring and academy classes; budget requests supporting LAPD growth.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman says the city cannot spend its way to safety, points to $152 million in LAPD liability payouts in FY2025, and wants the chief replaced.',
    fact_check='LAPD sworn staffing levels were not independently verified from a retrieved city document.',
    verification_status='partially verified')
pos(position_id='BAS-POL-0006', candidate_id='BASS', issue='Other', subissue='Community safety and alternatives to policing',
    position_summary='Created the first Office of Community Safety to expand civilian crisis response and violence intervention.',
    candidate_statement='"She created the first-ever Office of Community Safety to increase civilian crisis response and community violence intervention."',
    statement_date='unknown', context='Campaign record page', source_urls=cell(B_HOW),
    legislative_record='Office of Community Safety established during the first term.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman argues too many calls for service are still routed to armed officers and that response times vary by neighborhood.',
    fact_check='Program scale and budget were not independently verified.',
    verification_status='partially verified')
pos(position_id='BAS-POL-0007', candidate_id='BASS', issue='Other', subissue='Crime',
    position_summary='Claims homicides fell to their lowest level since the 1960s.',
    candidate_statement='"her comprehensive approach drove homicide to the lowest levels since the 1960s."',
    statement_date='unknown', context='Campaign record page and "Why I\'m Running"',
    source_urls=cell(B_WHY),
    legislative_record='Not applicable — outcome claim, not legislation.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman concedes violent crime is down but says residents do not feel safe because 911 response is slow and streetlights are out.',
    fact_check='Homicide counts were not independently verified from a retrieved LAPD or city dataset.',
    verification_status='partially verified')
pos(position_id='BAS-POL-0008', candidate_id='BASS', issue='Other', subissue='Infrastructure',
    position_summary='Created the city\'s first Comprehensive Infrastructure Plan.',
    candidate_statement='"Mayor Bass took executive action to create LA\'s first-ever CIP, which will create a real roadmap to fix our infrastructure."',
    statement_date='unknown', context='Campaign record page', source_urls=cell(B_HOW),
    legislative_record='Executive action creating the CIP; the plan itself is a roadmap, not funded construction.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman describes broken sidewalks and dark streetlights as evidence that planning has not translated into maintenance.',
    fact_check='No CIP funding table was retrieved.',
    verification_status='partially verified')
pos(position_id='BAS-POL-0009', candidate_id='BASS', issue='Immigration', subissue='Federal immigration enforcement',
    position_summary='Positions herself as the mayor who confronted ICE on the streets and organized mayors against deployments.',
    candidate_statement='"Mayor Bass has been in ICE\'s face on the streets, and she has organized Angelenos, dozens of local mayors and mayors nationally to stand against ICE and troop deployments."',
    statement_date='unknown', context='Campaign record page', source_urls=cell(B_HOW),
    legislative_record='City policies limiting local cooperation with federal immigration enforcement (Sanctuary City ordinance).',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman says residents still feel unprotected and that the city\'s response has been reactive; she pledges an "Immigrants In, ICE Out" agenda.',
    fact_check='The claim of organising "dozens" of mayors was not independently verified.',
    verification_status='partially verified')
pos(position_id='BAS-POL-0010', candidate_id='BASS', issue='Other', subissue='Palisades fire recovery',
    position_summary='Frames recovery from the January 2025 Palisades fire as unfinished work she intends to complete in a second term.',
    candidate_statement='"the recovery from January\'s Palisades Fire" (named as one of the continuing challenges of her term)',
    statement_date='2025-12-13', context='Launch rally speech as reported by CNS/ABC7',
    source_urls=cell(ABC7RALLY),
    legislative_record='Executive orders on debris removal and permitting after the fire (as described in campaign material).',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman says there is still no rebuilding plan and no one in charge, and that the chief recovery officer left after 90 days.',
    fact_check='No rebuilding-permit count was retrieved; the L.A. Times permit-relief newsletter is metered.',
    verification_status='partially verified')
pos(position_id='BAS-POL-0011', candidate_id='BASS', issue='Other', subissue='City budget and fiscal management',
    position_summary='Lists "Budgeting & Fiscal Responsibility" as a second-term priority but published no retrievable detail.',
    candidate_statement='"Budgeting & Fiscal Responsibility" (section heading on the second-term agenda page)',
    statement_date='unknown', context='"Term 2 Vision" agenda page',
    source_urls=cell(B_VIS),
    legislative_record='Not stated on the page.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman says City Hall made fiscal decisions that weakened the budget and that the city spent money it did not have.',
    fact_check='The agenda page\'s issue sections are JavaScript tabs; only headings were retrievable, so no policy content can be quoted.',
    verification_status='partially verified')
pos(position_id='BAS-POL-0012', candidate_id='BASS', issue='Economy', subissue='Film and entertainment jobs',
    position_summary='Appointed a Film Czar, cut city film fees and pressed for an expanded film and TV tax credit.',
    candidate_statement='"She appointed a Film Czar, cut city fees and successfully urged an expanded film & TV tax credit."',
    statement_date='unknown', context='Campaign record page', source_urls=cell(B_HOW),
    legislative_record='Film-permit fee reductions and the city\'s entertainment-industry liaison.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman told The Hollywood Reporter she would do more for Hollywood than Bass.',
    fact_check='Tax-credit expansion is a state action; the campaign attributes advocacy, not enactment, to the mayor.',
    verification_status='partially verified')
pos(position_id='BAS-POL-0013', candidate_id='BASS', issue='Economy', subissue='Downtown and small business',
    position_summary='Points to a permanent al fresco programme and a new Convention Center as downtown revival measures.',
    candidate_statement='"bringing back business to the downtown area via a permanent al fresco initiative and boosting union jobs"',
    statement_date='2025-12-13', context='Launch rally, as reported by CNS/ABC7',
    source_urls=cell(ABC7RALLY),
    legislative_record='Permanent al fresco ordinance; Convention Center authorization and groundbreaking.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman voted against the Convention Center expansion financing and says it drains essential services for decades.',
    fact_check='Raman\'s vote against the financing plan is reported by Our Weekly.',
    verification_status='verified')
pos(position_id='BAS-POL-0014', candidate_id='BASS', issue='Other', subissue='Affordability frame',
    position_summary='Defines the second term as a city "where hardworking people can afford to live" and "our kids no longer dodge tents on their walk to school".',
    candidate_statement='"a city where our kids no longer dodge tents on their walk to school. Where hardworking people can afford to live."',
    statement_date='unknown', context='"Why I\'m Running" page', source_urls=cell(B_WHY),
    legislative_record='Not applicable — message framing.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman frames affordability around rent burden and eviction filings rather than encampments.',
    fact_check='Not a factual claim.',
    verification_status='verified')
pos(position_id='BAS-POL-0015', candidate_id='BASS', issue='Other', subissue='Climate and environment',
    position_summary='Lists "Climate Change & Environmental Justice" among second-term priorities; the campaign also cites progress toward the city\'s zero-emissions goal.',
    candidate_statement='"Climate Change & Environmental Justice" (section heading); "working toward its zero-emissions goal"',
    statement_date='2025-12-13', context='Term 2 agenda page and launch rally',
    source_urls=cell(B_VIS),
    legislative_record='Not stated on the retrieved page text.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman ties environmental policy to transit delivery and street safety.',
    fact_check='Only the heading is retrievable; no target or metric published in the retrieved text.',
    verification_status='partially verified')
pos(position_id='BAS-POL-0016', candidate_id='BASS', issue='Democracy', subissue='Second-term commitment',
    position_summary='Rules out seeking another office, presenting the second term as her final one.',
    candidate_statement='"I\'m not running for another office after this. I\'m running to change Los Angeles."',
    statement_date='unknown', context='"Why I\'m Running" page', source_urls=cell(B_WHY),
    legislative_record='Not applicable.', position_changed='unknown', change_notes='unknown',
    opponent_criticism='Raman\'s campaign frames the same statement as an admission that the first term fell short.',
    fact_check='Not a factual claim.',
    verification_status='verified')

# ------------------------------------------------------------------ RAMAN
pos(position_id='RAM-POL-0001', candidate_id='RAMAN', issue='Other', subissue='Housing supply',
    position_summary='Pledges to triple annual housing construction across all income levels, including market-rate and social housing.',
    candidate_statement='"Our plan will triple annual housing construction and allow Los Angeles to remain a city of opportunity."',
    statement_date='unknown', context='Campaign issue page "Housing For All"', source_urls=cell(R_HOU),
    legislative_record='As a councilmember she passed zoning and planning reforms and permitting overhauls aimed at accelerating production.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass argues the city is already accelerating nearly 40,000 units and that Raman\'s approach would override neighborhood input.',
    fact_check='The tripling target has no published baseline or timeline in the retrieved text.',
    verification_status='partially verified')
pos(position_id='RAM-POL-0002', candidate_id='RAMAN', issue='Other', subissue='Permitting and red tape',
    position_summary='Wants permitting measured in weeks rather than months and a mayoral office dedicated to expediting housing.',
    candidate_statement='"a city where it takes weeks, not months" / "Raman promised to create an office devoted to expediting housing."',
    statement_date='2026-08-19', context='Aug. 19 runoff debate, as reported by CalMatters',
    source_urls=cell(CMDEB),
    legislative_record='Council work on permitting reform cited on her campaign biography page.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass says Raman has given the issue "lip service" and that the mayor\'s office had to absorb constituent service in Raman\'s district.',
    fact_check='The 18-month average permitting timeline cited by the campaign was not independently verified.',
    verification_status='verified')
pos(position_id='RAM-POL-0003', candidate_id='RAMAN', issue='Other', subissue='Renters and eviction',
    position_summary='Centres renters, citing 245,599 eviction notices filed 2023-2025, 93% for non-payment, with an average arrears balance under $4,000.',
    candidate_statement='"From 2023 through 2025, the Housing Department received 245,599 eviction notices. Ninety-three percent were for non-payment of rent. The average amount owed: less than $4,000."',
    statement_date='unknown', context='Campaign issue page "Protecting Renters"', source_urls=cell(R_RENT),
    legislative_record='Universal just-cause protections, a right-to-counsel programme and anti-displacement measures, per her biography page.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass points to the RSO amendments she signed as the substantive rent protection of the term.',
    fact_check='The eviction-notice figures are the campaign\'s; no LAHD dataset was retrieved to check them.',
    verification_status='partially verified')
pos(position_id='RAM-POL-0004', candidate_id='RAMAN', issue='Other', subissue='Rent Stabilization Ordinance credit',
    position_summary='Claims credit for revising the RSO to reduce rental increases for the first time in 40 years.',
    candidate_statement='"revising the Rent Stabilization Ordinance to reduce rental increases for the first time in 40 years"',
    statement_date='unknown', context='Campaign biography page', source_urls=cell(R_ABOUT),
    legislative_record='Council-side work on the RSO amendments.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass claims the same 40-year-first RSO improvement as her own signature achievement.',
    fact_check='Direct collision with BAS-POL-0002. Neither campaign\'s attribution could be checked against the ordinance file in this environment.',
    verification_status='conflicting sources')
pos(position_id='RAM-POL-0005', candidate_id='RAMAN', issue='Other', subissue='Homelessness target',
    position_summary='Pledges to cut the number of people sleeping in tents and encampments by at least 50% by the 2028 Olympics.',
    candidate_statement='"When I\'m mayor, we\'ll reduce the number of people sleeping in tents and encampments by at least 50% by the 2028 Olympics."',
    statement_date='unknown', context='Campaign issue page "Ending Homelessness"', source_urls=cell(R_HOM),
    legislative_record='Council votes on homelessness funding and encampment policy.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass says street homelessness is already down 17.5% and warns that Raman would reverse the encampment strategy.',
    fact_check='The target is a pledge; no baseline count for tent sleeping is published.',
    verification_status='partially verified')
pos(position_id='RAM-POL-0006', candidate_id='RAMAN', issue='Other', subissue='Inside Safe costs and outcomes',
    position_summary='Calls Inside Safe the most expensive interim-housing programme in the city and says 40% of people moved indoors through it returned to the streets.',
    candidate_statement='"40% of people moved indoors through the Mayor\'s signature program have returned to the streets." / average cost "an average of $85,000 a year for a motel room and services"',
    statement_date='unknown', context='Campaign issue page "Ending Homelessness"', source_urls=cell(R_HOM),
    legislative_record='Council efforts to reduce Inside Safe per-unit costs, cited on the same page.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass presents Inside Safe as the city\'s first comprehensive encampment strategy and a success.',
    fact_check='Both the 40% return rate and the $85,000 average are campaign figures; no city audit was retrieved.',
    verification_status='partially verified')
pos(position_id='RAM-POL-0007', candidate_id='RAMAN', issue='Other', subissue='Public safety philosophy',
    position_summary='Rejects both defunding and "business as usual", proposing a redesigned system with more civilian response and accountability.',
    candidate_statement='"We will not achieve the public safety Angelenos need through the binary choice of defunding the police or defending business as usual."',
    statement_date='unknown', context='Campaign issue page "Public Safety"', source_urls=cell(R_PS),
    legislative_record='Council work on crisis response and police accountability, per her biography page.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass tells voters Raman would leave LAPD in "disarray" ahead of the Olympics.',
    fact_check='Not a factual claim.',
    verification_status='verified')
pos(position_id='RAM-POL-0008', candidate_id='RAMAN', issue='Other', subissue='LAPD liability and accountability',
    position_summary='Argues LAPD liability payouts are the single largest source of city liability, at $152 million in FY2025.',
    candidate_statement='"LAPD is the single largest source of liability payouts in the City budget, accounting for $152 million in fiscal year 2025"',
    statement_date='unknown', context='Campaign issue page "Public Safety"', source_urls=cell(R_PS),
    legislative_record='Council oversight of liability claims.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass frames Raman\'s critique of the department as undermining public safety.',
    fact_check='The $152 million figure is the campaign\'s; no city claims report was retrieved.',
    verification_status='partially verified')
pos(position_id='RAM-POL-0009', candidate_id='RAMAN', issue='Other', subissue='Police leadership',
    position_summary='Says LAPD Chief Jim McDonnell has "lost the confidence" of the city.',
    candidate_statement='"Raman says McDonnell has "lost the confidence" of the city"',
    statement_date='2026-09-16', context='CalMatters commentary on the public-safety argument',
    source_urls=cell(CMDEB),
    legislative_record='Not applicable — appointment would be a mayoral power.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass accuses Raman of wanting to destabilise the department before the 2028 Olympics.',
    fact_check='The quote is the commentator\'s paraphrase of Raman\'s position, not a verbatim transcript.',
    verification_status='partially verified')
pos(position_id='RAM-POL-0010', candidate_id='RAMAN', issue='Other', subissue='Palisades rebuilding',
    position_summary='Proposes a single accountable "Recovery District" because rebuilding is spread across more than twelve agencies.',
    candidate_statement='"The Palisades recovery is currently spread across more than twelve agencies, with no single accountable entity responsible for getting families home."',
    statement_date='unknown', context='Campaign issue page "Palisades Recovery"', source_urls=cell(R_PAL),
    legislative_record='State law cited on the page as allowing Los Angeles to create such a district.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass says recovery is under way and that the city streamlined permits after the fire.',
    fact_check='The "twelve agencies" and "17 months, no plan" claims are the campaign\'s.',
    verification_status='partially verified')
pos(position_id='RAM-POL-0011', candidate_id='RAMAN', issue='Other', subissue='Fire response accountability',
    position_summary='Criticises the mayor\'s absence during the January 2025 fires and alleges the after-action report was altered to shift responsibility.',
    candidate_statement='"A Mayor who was out of the country while the fire raged. ... the city tried to cover up responsibility by altering the after-action report."',
    statement_date='unknown', context='Campaign issue page "Palisades Recovery"', source_urls=cell(R_PAL),
    legislative_record='Not applicable — accusation about executive conduct.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass has not addressed the alteration allegation in any retrieved statement.',
    fact_check='UNVERIFIED allegation published by the challenger; no independent reporting on the after-action report was retrieved.',
    verification_status='unverified')
pos(position_id='RAM-POL-0012', candidate_id='RAMAN', issue='Other', subissue='Transit delivery',
    position_summary='Argues Metro\'s voter-approved corridors must be accelerated and that the city\'s bureaucracy is the obstacle.',
    candidate_statement='"Measure R (2008) and Measure M (2016) committed $120B to the expansion of rail and transit across the county, and Measure HLA (2024) mandated that street safety improvements happen when streets get repaved"',
    statement_date='unknown', context='Campaign issue page "Transportation & Street Safety"', source_urls=cell(R_TRANS),
    legislative_record='Council advocacy on the Sepulveda, Vermont and K Line Northern Extension corridors.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass points to her infrastructure plan as the delivery vehicle.',
    fact_check='The $120 billion Measure R/M figure is the campaign\'s characterisation of the two sales-tax measures.',
    verification_status='partially verified')
pos(position_id='RAM-POL-0013', candidate_id='RAMAN', issue='Other', subissue='City budget',
    position_summary='Blames incumbent fiscal decisions for weakening the budget just as needs peaked.',
    candidate_statement='"City Hall made fiscal decisions that weakened our budget and our ability to function, just as needs have reached their highest point."',
    statement_date='unknown', context='"Why I\'m Running" page', source_urls=cell(R_WHY),
    legislative_record='Council budget votes, including opposition to the Convention Center financing plan.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass presents her budgeting as disciplined and accuses Raman of voting against investment.',
    fact_check='A $1 billion structural deficit is reported by a local column (Westside Current) and echoed by the city controller\'s endorsement coverage.',
    verification_status='verified')
pos(position_id='RAM-POL-0014', candidate_id='RAMAN', issue='Other', subissue='Convention Center financing',
    position_summary='Opposes financing the Convention Center expansion in a way that commits essential-service revenue for decades.',
    candidate_statement='"no responsible mayor would pursue them through a financing plan that drains essential services for decades"',
    statement_date='2026-09-11', context='Endorsement announcement covered by Our Weekly', source_urls=cell(OURW),
    legislative_record='Voted against the Convention Center expansion financing, alongside Councilmember Yaroslavsky.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass broke ground on the project and counts it as an economic-development achievement.',
    fact_check='The vote is reported; the financing structure itself was not independently reviewed.',
    verification_status='verified')
pos(position_id='RAM-POL-0015', candidate_id='RAMAN', issue='Immigration', subissue='Federal enforcement response',
    position_summary='Argues an adversarial federal government is sending ICE agents into the city and that residents feel unprotected.',
    candidate_statement='"an adversarial federal government is sending ICE agents into our communities, and too many residents feel unprotected."',
    statement_date='unknown', context='"Why I\'m Running" page; issue menu lists "Immigrants In, ICE Out"',
    source_urls=cell(R_WHY),
    legislative_record='Council work on immigrant legal services and sanctuary policy.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass presents herself as the mayor who stood "in ICE\'s face" and organised other mayors.',
    fact_check='Not a factual claim.',
    verification_status='verified')
pos(position_id='RAM-POL-0016', candidate_id='RAMAN', issue='Foreign policy', subissue='Gaza language at the Jewish-community forum',
    position_summary='Used different language from Bass on the Gaza war at the Sept. 29 Jewish Federation forum.',
    candidate_statement='"gave different descriptions of the Gaza war" (LAist report on the forum)',
    statement_date='2026-09-29', context='Jewish Federation of Los Angeles forum, Skirball Cultural Center',
    source_urls=cell(LAISTJEW),
    legislative_record='Not applicable — municipal race.',
    position_changed='unknown', change_notes='unknown',
    opponent_criticism='Bass used her own Gaza framing to draw a contrast.',
    fact_check='LAist describes the difference but the archive could not retrieve verbatim quotes from the audio within this build.',
    verification_status='partially verified')

write_csv('01_candidates/policy_positions.csv', H, P)

# ------------------------------------------------------------------ career timelines
CH = ['entry_id', 'candidate_id', 'start_date', 'end_date', 'role_or_event', 'organization',
      'location', 'description', 'source_urls', 'verification_status']
C = []


def car(**k):
    C.append([k.get(h, 'unknown') for h in CH])


car(entry_id='BAS-CAR-0001', candidate_id='BASS', start_date='2004-12-01', end_date='2010-11-30',
    role_or_event='State Assemblymember, 47th District', organization='California State Assembly',
    location='Los Angeles', description='Tenure began with the December 2004 swearing-in for the 2005-06 session; month-only date recorded as the 1st by convention.',
    source_urls=cell(WIKI), verification_status='partially verified')
car(entry_id='BAS-CAR-0002', candidate_id='BASS', start_date='2008-05-01', end_date='2010-11-30',
    role_or_event='Speaker of the California State Assembly', organization='California State Assembly',
    location='Sacramento', description='First Black woman to serve as Assembly Speaker.',
    source_urls=cell(WIKI), verification_status='partially verified')
car(entry_id='BAS-CAR-0003', candidate_id='BASS', start_date='2011-01-03', end_date='2022-12-09',
    role_or_event='Member of the U.S. House of Representatives', organization='U.S. Congress',
    location='Los Angeles and Washington, D.C.', description='Represented a Los Angeles district for six terms.',
    source_urls=cell(WIKI), verification_status='partially verified')
car(entry_id='BAS-CAR-0004', candidate_id='BASS', start_date='2019-01-03', end_date='2021-01-03',
    role_or_event='Chair, Congressional Black Caucus', organization='Congressional Black Caucus',
    location='Washington, D.C.', description='Chaired the caucus during the 116th Congress.',
    source_urls=cell(WIKI), verification_status='partially verified')
car(entry_id='BAS-CAR-0005', candidate_id='BASS', start_date='2022-12-12', end_date='unknown',
    role_or_event='Mayor of Los Angeles', organization='City of Los Angeles', location='Los Angeles',
    description='Sworn in as the 43rd mayor. The launch-rally wire copy calls Dec. 13, 2025 "two days after the third anniversary of her swearing-in", which implies Dec. 11; the official date is recorded here and the discrepancy flagged.',
    source_urls=cell(ABC7RALLY), verification_status='verified')
car(entry_id='BAS-CAR-0006', candidate_id='BASS', start_date='2024-07-01', end_date='unknown',
    role_or_event='Files paperwork for reelection', organization='Re-Elect Karen Bass for Mayor 2026',
    location='Los Angeles', description='Opened a 2026 reelection committee 23 months before the runoff.',
    source_urls=cell(LT24), verification_status='partially verified')
car(entry_id='BAS-CAR-0007', candidate_id='BASS', start_date='2025-01-07', end_date='unknown',
    role_or_event='Palisades and Eaton fire emergency response', organization='City of Los Angeles',
    location='Pacific Palisades and Altadena', description='The fires began on Jan. 7, 2025; recovery becomes the central incumbency vulnerability in the campaign.',
    source_urls=cell(R_PAL), verification_status='verified')
car(entry_id='BAS-CAR-0008', candidate_id='BASS', start_date='2025-12-13', end_date='unknown',
    role_or_event='Reelection campaign launch', organization='Re-Elect Karen Bass for Mayor 2026',
    location='Los Angeles', description='Launch rally at Los Angeles Trade-Technical College.',
    source_urls=cell(ABC7RALLY), verification_status='verified')
car(entry_id='BAS-CAR-0009', candidate_id='BASS', start_date='2026-06-02', end_date='unknown',
    role_or_event='First place in the nonpartisan primary', organization='City of Los Angeles',
    location='Los Angeles', description='292,593 votes (34.3%), advancing to the runoff against Raman.',
    source_urls=cell('https://www.nbcnews.com/politics/2026-primary-elections/los-angeles-mayor-results'),
    verification_status='verified')
car(entry_id='BAS-CAR-0010', candidate_id='BASS', start_date='2026-11-03', end_date='unknown',
    role_or_event='Defeated in the runoff', organization='City of Los Angeles', location='Los Angeles',
    description='504,959 votes (45.1%) to Raman\'s 615,264 (54.9%).',
    source_urls=cell(WIKI), verification_status='partially verified')

car(entry_id='RAM-CAR-0001', candidate_id='RAMAN', start_date='2017-01-01', end_date='2020-11-30',
    role_or_event='Co-founder, SELAH Neighborhood Homeless Coalition',
    organization='SELAH Neighborhood Homeless Coalition', location='Los Angeles',
    description='Neighbour-led mutual aid for unhoused residents; the founding year is given as 2017 on the campaign biography page\'s narrative and is recorded at year precision only.',
    source_urls=cell(R_ABOUT), verification_status='partially verified')
car(entry_id='RAM-CAR-0002', candidate_id='RAMAN', start_date='2020-12-01', end_date='unknown',
    role_or_event='Los Angeles City Councilmember, District 4', organization='City of Los Angeles',
    location='Los Angeles', description='Elected in November 2020; the campaign says 2,000 volunteers knocked on more than 80,000 doors and that she was the first to defeat a sitting councilmember in 17 years.',
    source_urls=cell(R_ABOUT), verification_status='verified')
car(entry_id='RAM-CAR-0003', candidate_id='RAMAN', start_date='2022-06-07', end_date='unknown',
    role_or_event='Re-elected to the City Council', organization='City of Los Angeles',
    location='Los Angeles', description='Won re-election in the 2022 cycle; LAist\'s candidate guide is the corroborating source.',
    source_urls=cell(GUIDE), verification_status='partially verified')
car(entry_id='RAM-CAR-0004', candidate_id='RAMAN', start_date='2025-11-15', end_date='unknown',
    role_or_event='First public signals of a mayoral challenge', organization='unknown',
    location='Los Angeles', description='An L.A. Times newsletter asked whether an activist challenging Bass could be "L.A.\'s Mamdani".',
    source_urls=cell('https://www.latimes.com/california/newsletter/2025-11-15/la-on-the-record-an-activist-is-challenging-bass-from-the-left'),
    verification_status='partially verified')
car(entry_id='RAM-CAR-0005', candidate_id='RAMAN', start_date='2026-02-07', end_date='unknown',
    role_or_event='Announces candidacy for mayor', organization='Nithya Raman for Mayor',
    location='Los Angeles', description='Entered on the last day before the filing deadline, per her own account.',
    source_urls=cell(R_WHY), verification_status='verified')
car(entry_id='RAM-CAR-0006', candidate_id='RAMAN', start_date='2026-06-02', end_date='unknown',
    role_or_event='Second place in the nonpartisan primary', organization='City of Los Angeles',
    location='Los Angeles', description='247,781 votes (29.0%), advancing to the runoff.',
    source_urls=cell('https://www.nbcnews.com/politics/2026-primary-elections/los-angeles-mayor-results'),
    verification_status='verified')
car(entry_id='RAM-CAR-0007', candidate_id='RAMAN', start_date='2026-11-03', end_date='unknown',
    role_or_event='Elected Mayor of Los Angeles', organization='City of Los Angeles',
    location='Los Angeles', description='615,264 votes (54.9%) to Bass\'s 504,959 (45.1%).',
    source_urls=cell(WIKI), verification_status='partially verified')

write_csv('01_candidates/bass/career_timeline.csv', CH, [r for r in C if r[1] == 'BASS'])
write_csv('01_candidates/raman/career_timeline.csv', CH, [r for r in C if r[1] == 'RAMAN'])
