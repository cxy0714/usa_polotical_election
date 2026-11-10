# Agent B - gaps, conflicts, and unverified leads

Compiled by Agent B (bio-policy), 2026-11-10. Scope: biography, career records, policy position matrix.
Companion files: `_staging/B_sources.csv`, `01_candidates/policy_positions.csv`, per-candidate `biography.md`, `political_positions.md`, `career_timeline.csv`.

## 1. Factual conflicts recorded rather than resolved

| # | Conflict | Resolution used in deliverables |
|---|---|---|
| 1 | **Talarico launch date.** Wikipedia dates the Senate announcement to 2025-09-09. TIME and finance reporting describe only "September 2025". A Texas Tribune preview of 2025-09-05 said he "planned to launch". | `career_timeline.csv` records 2025-09-09 with verification_status `conflicting sources` and a note naming the competing dates. |
| 2 | **Talarico's age when first elected.** TIME: won at 28. Wikipedia: 29 at swearing-in. | Both are consistent with a 1989-05-17 birth: 28 at the March 2018 primary, 29 at the November general election and at seating in January 2019. Biography states this explicitly instead of picking one. |
| 3 | **Talarico primary margin.** Wikipedia: 52.4 percent. A widely repeated framing gives 53-45.7. Crockett's own total is not independently captured here. | CSV and biography use "about 52.4 percent" and flag Crockett's share as approximate. |
| 4 | **Paxton runoff margin.** Wikipedia: 63.8 percent, "more than 25 points". | Both figures are used together, since they are consistent; the percentage is the precise one. |
| 5 | **Trump's posture in the GOP primary.** One source says Paxton held Trump's endorsement; TIME says Trump remained atypically neutral, telling allies all three candidates were his friends. | Not resolved. The biography attributes the neutrality claim to TIME's reporting and the endorsement to the election record, and flags the tension in the assessment text. Anyone resolving this should find the actual endorsement statement date. |
| 6 | **"God is non-binary."** The remark is dated to 2021 Texas House floor debate in Fox News' 2026 recap, and TIME records it as a reported line of attack without dating it. | Dated 2021 with a note that the 2026 coverage recirculated it. |
| 7 | **Paxton's IVF posture.** Reporting describes him as opening the door to further IVF restrictions while Cornyn attacked him over IVF. No verbatim Paxton statement was retrieved. | Recorded as `partially verified`, with `position_changed = yes` and an explicit note that the underlying statement was not retrieved. |
| 8 | **Talarico's Equality Act stance.** 2025 statement of support vs. a Washington Post report of October 2026 that his position had become less clear. | Recorded as a reported shift, `partially verified`, sourced to the Wikipedia aggregation of the Post and Statesman pieces. The Post article itself was not retrieved. |

## 2. Top research gaps, by candidate

### Talarico
1. **Pre-2017 employment history.** Nothing beyond "former middle-school teacher" and the Teach For America placement. No employer, role or date range outside teaching is documented in retrieved sources.
2. **Seminary record.** He is described as a seminarian "on academic leave"; course of study, dates of enrolment, and whether he remains enrolled are undocumented.
3. **Campaign infrastructure.** The campaign manager's name (reported by the Lead as Seth Krasne) was not confirmed by any source retrieved here, so it is absent from the timeline.
4. **Capital punishment and vaccine exemptions.** Both positions come from TIME's list of vulnerability points, not from his own statements. Needs a primary statement before use in any comparison row.
5. **Allred "mediocre Black man" episode.** Recorded as disputed; no source retrieved adjudicates what was actually said.
6. **Whether any Republican-leaning endorsements or sheriffs exist.** The immigration page claims a "Republican sheriff" endorsement without naming him; unverified.
7. **Post-election plans.** No source documents when he resigns the House seat or his Senate committee assignments.

### Paxton
1. **Campaign issue content.** `kenpaxton.com` returned only site-builder JSON/CSS; no issues page could be retrieved. Every campaign position in this file is therefore sourced to reporting or to the attorney general record, not to his own literature.
2. **State Senate tenure (2013-2015).** Essentially undocumented beyond the election results and his abortion authorship.
3. **Law practice detail.** Firm names and rough chronology only; no client or case detail.
4. **Debate refusal reasoning.** The fact of the refusal is documented; his stated reason is not.
5. **Data-center policy.** A county's moratorium opinion request was still pending as of August 2026; the substance of his announced data-center agenda is thin.
6. **Senate campaign staffing and finance detail.** Not retrieved. Musk-linked super PAC totals are documented at the race level only.
7. **Position on NATO, State Department and USAID funding.** No statement located; left as `unverified` in the matrix rather than guessed.

## 3. Leads supplied by the Lead that Agent B did **not** independently verify

These are recorded so the Lead can attribute them correctly. None of them is cited in Agent B's deliverables.

- Politico, 2026-10-06, on Ted Cruz as a Paxton backer: https://www.politico.com/news/2026/10/06/ken-paxton-secret-weapon-ted-cruz-01107868
- Trump and Paxton appearance at Peterbilt Motors, Denton, 2026-10-01.
- Houston Chronicle, "How Latino voters in Texas made James Talarico the Democratic nominee".
- The Root, reporting on a roughly $25 million Talarico Black-voter effort.
- Spectrum News, "corruption crisis" framing; KEYE and Telemundo Austin coverage of Paxton's cost-of-living framing.
- El Paso Times, 2026-08-20, Talarico campaign staffing coverage.

## 4. Sources that could not be retrieved (and what that blocked)

| Source | Failure mode | Consequence |
|---|---|---|
| `texastribune.org` article bodies | JS/paywall; the AMP variant redirected to an unrelated page | Any Tribune-only claim is either sourced through a syndicated copy (Gilmer Mirror) or dropped |
| `apnews.com`, `britannica.com`, `newsfromthestates.com`, `web.archive.org` | HTTP 403 | No wire-service confirmation was possible for election-night figures; results rest on the Wikipedia election article |
| `ballotpedia.org` | 202 with empty body | No structured candidate-profile cross-check |
| `kenpaxton.com` / `www.kenpaxton.com` | cross-origin redirect not followed; then site-builder JSON | No primary-source campaign positions for Paxton |
| `kera.org`, `houstonpublicmedia.org`, `newsweek.com`, `nationalreview.com`, `huffpost.com` | truncation before article body | Position rows derived from these are `partially verified` and quote no body text |
| `dallasobserver.com` fraud-charges article | body was navigation chrome only | Used for headline-level corroboration only |
| `texasattorneygeneral.gov` | not retrieved | No primary-source AG releases are cited anywhere in this file set |
| `foxnews.com` (non-`.print` paths), `nytimes.com`, `washingtonpost.com`, `texasmonthly.com` | paywall or incomplete rendering | Secondary reporting of their findings is used instead, and marked as such |

Retrieval workaround worth recording: Wikipedia section-level raw fetches (`/w/index.php?title=PAGE&action=raw&section=N`) overcame the size ceiling on long articles, and local-TV and local-paper syndication (FOX 7 Austin, FOX 26 Houston, ABC 7 Amarillo, Gilmer Mirror, El Paso Times) rendered article bodies that the originating outlets would not.

## 5. Coverage-parity note

`policy_positions.csv` holds 146 rows: 80 TALARICO and 66 PAXTON. The asymmetry is deliberate in two places and a limitation in one:

- **Talarico has more rows in Economy, Education, Energy, Foreign policy, Immigration and Other** because his campaign publishes thirteen issue pages, giving dense, quotable primary-source material.
- **Paxton has more rows in Economy** because his affordability plan has more discrete line items that are individually documented.
- **Paxton is thinner in Gun policy, Healthcare, Labor and Religion** not from under-research but because he has no retrievable campaign issue literature and his record in those areas is litigation, which yields fewer discrete position statements per topic.

No row was added to either side to force numerical parity. Where Paxton's position on a topic is undocumented, the row exists with `unknown` values and `unverified` status rather than being omitted.
