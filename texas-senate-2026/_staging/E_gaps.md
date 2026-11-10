# Agent E — Research Gaps, Conflicts and Method Notes

**Scope:** `05_campaign_media/**`, `06_campaign_finance/**`
**Compiled:** 2026-11-10 (access date for all retrievals)
**Status:** complete for what is retrievable; the gaps below are findings, not unfinished work.

---

## 1. Unresolved numerical discrepancies

These are recorded rather than resolved. Do **not** merge any of them silently.

### 1.1 Talarico's Q3 total: $64m (campaign) vs $60.21m (FEC principal committee)
- Campaign announcement, 2026-10-15: "topped $64 million" (`campaign_finance.csv` FIN-TAL-0009; E-S003).
- FEC Form 3 for the principal committee, same quarter: **$60,214,961** in total receipts (`FIN-TAL-0006`; E-S005).
- These are not the same measurement. The campaign total appears to include joint-fundraising-committee money raised on the candidate's behalf; the FEC line covers only C00919084. The gap (~$3.8m) is **not** explained in any source retrieved. The $64m figure is nonetheless corroborated as a *reported* figure by NYT (MC-0029), Dallas Morning News (MC-0030) and NBC News (cited by KPRC, MC-0021) — so the discrepancy is between "what was announced" and "what this committee filed", not evidence that the announcement was wrong.
- **Action needed from Lead/Agent:** if polling/finance integration quotes "$64m", label it a campaign-announced total, not an FEC receipts figure.

### 1.2 Talarico's cumulative total: $134.3m vs $140.3m vs $155m vs $146.3m
Four different cumulative figures circulate, and they are four different things:
- **$134.3m** — campaign claim, donations only, Sept 2025 through the Q3 announcement (E-S003; `FIN-TAL-0008`).
- **$140.3m** — FEC "total contributions" for the principal committee Jan 1 2025–Oct 14 2026 (E-S005; cited as "$140.3 million" by KPRC at E-S001).
- **$146.3m** — FEC "total receipts" for the same committee and period (includes transfers and other receipts, not just contributions).
- **$155m** — Texas Tribune cumulative including joint fundraising committees, as of Oct 14 (E-S002).
- The campaign's own $134.3m is *lower* than the FEC contributions figure, which is counter-intuitive for a total that is supposed to be broader. **Unexplained.** Most likely the campaign excluded transfers/refunds and counted only donations, but no source says so.

### 1.3 Paxton's Q3 total: $18m (campaign) vs $10.25m (FEC principal committee)
- Campaign: $18m "across his principal campaign committee as well as two joint fundraising committees" (E-S004).
- FEC principal committee: **$10,249,117** (`FIN-PAX-0008`; E-S006).
- Difference ~$7.75m is joint-fundraising money. The sources are consistent about the *mechanism*; only the headline number differs by scope. Recorded in `FIN-PAX-0008` notes.

### 1.4 The El Paso Times "$18 million in second-quarter fundraising cash" error
- The El Paso Times (E-S003) describes Paxton's $18m as "second-quarter fundraising cash", announced 2026-10-05.
- KWTX/Texas Tribune (E-S004) is unambiguous: the $18m is **Q3** (July 1–Sept 30), and it "more than doubles his second-quarter haul of **$9 million**".
- Nick Maddux's own quote in *both* articles says the $18m "doubled his second-quarter fundraising record", which only makes sense if $18m is the later (Q3) number.
- **Resolution adopted:** Q3 = $18m, Q2 = $9m. `FIN-PAX-0010` is marked `conflicting sources` and both readings are quoted in its notes.

### 1.5 Musk's total: $158m vs "nearly $190m" vs "more than $190m" vs "over $200m" vs ~$150m
- **$158m** — traceable to FEC filings: $75m (2026-09-09) + $83m (about two weeks later) to Senate Leadership Fund, which passed both sums to Texas PAC (E-S023). Also the figure used by the BBC (E-S025) and KPRC (E-S001).
- **"nearly $190 million"** — Texas Tribune's own characterisation of what Musk "appears to have poured into the U.S. Senate race" (E-S023). This does not equal the $158m traced in the same article; the extra ~$30m is unexplained (possibly Lone Star Liberty PAC money routed via the Axios-reported $10m+$5m+$5m arrangement, plus other vehicles).
- **"more than $190 million from Musk"** — Deadline (E-S014).
- **"over $200 million"** — Talarico's 2026-10-31 statement (Lead-verified) and the framing of the campaign manager's claim (E-S003).
- **~$150m** — a translated Brazilian outlet, per the Lead.
- **Action:** any single figure must carry its attribution and date. `FIN-EXT-0031` is `conflicting sources` for this reason.

### 1.6 Outside ad spending by Paxton's side: $214m vs $217m vs $251.7m vs "over $200m"
- **$214m** — Texas Tribune 2026-10-14, "national Republican power brokers (Trump, Senate GOP leadership, Musk) poured over $214 million into Texas in the weeks before the report" (E-S053, Lead-relayed).
- **$217m** — Texas Tribune 2026-10-15, "by the end of the month, a handful of outside groups led by SLF had dropped over $217 million on ads" (E-S023) — i.e. cumulative through 2026-09-30.
- **$251.7m** — AdImpact's total outside ad *support* for Paxton across the general (E-S008).
- **"over $200m"** — Seth Krasne's campaign-statement figure (E-S003, `FIN-EXT-0040`, `unverified`).
- Different denominators (date window; "into Texas" vs "on ads"; "advertising activity" vs "support for the candidate"). Do not average them.

### 1.7 FEC independent-expenditure totals vs AdImpact advertising totals — a factor-of-ten gap
- FEC Schedule E (E-S007) shows, for example, **Texans for a Conservative Majority $24.96m opposing Paxton** and **Lone Star Liberty PAC $7.72m opposing Talarico**.
- AdImpact (E-S008) reports **Texas PAC $182.1m** supporting Paxton and **Lone Star Rising $14.0m**.
- These cannot both describe the same universe. Likely explanations (unverified): (a) the FEC by-candidate pull returned only a subset of reported IEs at the time of access; (b) large parts of the pro-Paxton advertising were booked by **Texas PAC**, an entity whose IEs may not have appeared in the by-candidate aggregation I pulled; (c) AdImpact counts *reserved* airtime, not just aired/reported expenditure.
- **Action:** `campaign_finance.csv` keeps the two layers in separate rows with different `report_type` values (`Independent expenditure` vs `reported_AdImpact`) and explicitly says not to add them. **This is the single most important caution in this agent's output.**
- I attempted to split the FEC IE data into primary vs general by date range and was **blocked by the OpenFEC DEMO_KEY rate limit** (40 calls/hour). So `FIN-EXT-0001..0028` are cycle-wide (primary + general), and the "2026-04-01..2026-10-14" period labels are approximate windows, not verified report periods.

### 1.8 PAC contributions: $518,805 vs $518,000 vs $468,805.64 (Talarico); $435,150 vs $702,000
- KPRC (E-S001): $518,805 (Talarico) and $435,150 (Paxton) "as of 2026-10-20", citing FEC.
- Texas Tribune (E-S002): about $518,000 (Talarico) and about $702,000 (Paxton) "as of Oct. 14" — the Paxton figure includes joint-fundraising-committee money; KPRC's does not.
- FEC principal committee line item (E-S005/E-S006): Talarico $468,805.64 through the pre-general report; Paxton $392,150 by the same measure.
- **Unexplained** for Talarico: $518,805 vs $468,805.64 is a ~$50k gap that the "as of" dates do not explain (Oct 20 is *after* the pre-general close of Oct 14, but the extra two days' receipts would have to be entirely PAC money).
- Because these are third-party renderings of FEC data, all three are recorded as `partially verified`.

### 1.9 "Three debates scheduled" (2026-09-02) — a claim that did not survive
The Washington Examiner stated on 2026-09-02 that debates were "scheduled" for **Sept. 22, Oct. 6 and Oct. 13**, each hosted by a different news station (E-S010). **No debate was held.** By 2026-09-28 Spectrum was reporting "No debate set between Talarico and Paxton" (MC-0051), and the CNN×Jubilee event of 2026-10-14 was a solo voter Q&A (E-S019). The Examiner's sentence is preserved in `media_coverage.csv` MC-0008 with a caution, and must not be carried into any event table as three scheduled debates.

### 1.10 "Debate" used for a solo town hall
CNN's live-post headline says Talarico "debates voters" (MC-0055); the Daily Beast called it "CNN's Talarico Debate" (MC-0058); the Tennessean column treats it as a debate (MC-0057). The Miami Herald preview (MC-0062) correctly describes it as taking "questions". **Convention adopted here:** the 2026-10-14 CNN×Jubilee event is recorded as a town hall / voter Q&A, and any "debate" label in a headline is quoted, not adopted.

---

## 2. Coverage and retrievability gaps

### 2.1 Reuters is absent
**No Reuters item on this race was retrievable** at access. Several searches were run; none returned a Reuters URL. `media_coverage.csv` therefore has no Reuters row. This is a genuine hole in the outlet mix specified by the brief and is recorded rather than filled with a look-alike wire story (AP and AFP are present; AP only at headline/video level).

### 2.2 Paywalled / blocked sources (recorded at headline level only)
| Source | Status at access | Consequence |
|---|---|---|
| NYT (all pieces) | HTTP 403 via fetch | Headline-level only: MC-0028, MC-0029, MC-0046 (`E-S042`); the $64m and "Angela Paxton" stories are corroborated by other outlets. |
| Washington Post (MC-0032, MC-0067) | Headline/snippet only | The "two Texas Republicans voted for Talarico" story is unverified beyond its headline. |
| Dallas Morning News (MC-0030, MC-0045) | JS "Client Challenge" | Headline only; `E-S028` records the block. |
| Politico (E-S031) | CAPTCHA interstitial | $20m ad-buy figure relies on E-S004 corroboration. |
| The Independent (E-S032) | HTTP 403 | Leaked-audio quotes **not verified** — see §3.2. |
| Fox News print URL (E-S033) | 404 | Same story unverified. |
| AFP factcheck (E-S035) | HTTP 403 | Fraud/clerical-error row at headline level only (MC-0042). |
| Houston Chronicle interactive (MC-0049) | JS-only | Only the subhead "$273M+ ad landscape" captured. |
| Community Impact (MC-0031) | Body not rendered | Recorded as an anchor for Q3 report dates only; **no figures taken**. |
| Newsweek (MC-0065) | HTTP 403 | Leaked-tape story headline only. |

### 2.3 Ad creative is under-documented
This is the biggest substantive gap. For most advertisements I have the *existence, sponsor, message and (where reported) verbatim lines* — but **not** video URLs, transcripts, exact lengths, or visual descriptions beyond what a reporter described. Consequences:
- `video_url` and `transcript_url` are `unknown` for nearly every row in `advertisements.csv`.
- `main_visual_elements`, `narration_soundtrack` and `candidate_appearance` are frequently `unknown`.
- Several campaign intro/bio spots are recorded as three thematic rows (TAL-AD-0001..0003) because the Texas Tribune describes three creative themes without naming or dating individual spots. They are **not** three confirmed distinct ad files.
- **Paxton campaign creative is almost entirely undocumented** — I have the buy ($20m, week of 2026-09-28) but no title, script or URL (`PAX-AD-0001`). Agent C (visual) and Agent D (speech/video) may be able to close this; I deliberately left it as `unknown` rather than infer.
- Aggregate/placement rows (`EXT-AD-0011`, `EXT-AD-0012`) are included so outside spending is not understated, but they are **not** individual spots and must not be counted as such.

### 2.4 AdImpact and Adweek figures are vendor/campaign claims
- AdImpact (E-S008) is an industry measurement firm; its $573m includes **reservations**, not just aired spots.
- Adweek's $56.5m broadcast / $8.3m CTV / $8m YouTube / $210,000 radio are **campaign-supplied** (E-S026).
- Neither is an FEC filing. Both are labelled `reported_AdImpact` / `campaign_claim` in `report_type` and `partially verified` in `verification_status`.

### 2.5 Social media is thin and mostly unverifiable
- Candidate X/Twitter posts are known **only as quotes inside news articles** (E-S021, E-S022, E-S023). No permalinks, no timestamps, no engagement data.
- The TikTok account and its "3 billion organic views" claim (E-S026) are recorded as an **aggregate campaign claim**, not post-level data.
- **No post was independently retrievable.** `social_media.csv` marks almost everything `partially verified`, and one row (`PAX-SM-0004`) is `unverified` and explicitly labelled as speech content, not a post.
- The `@Republicans` post (PAX-SM-0002) is a **party account**, not the Paxton campaign. It is recorded under PAXTON only so the attack is traceable, with an explicit warning not to attribute it to the candidate.

### 2.6 Timing precision
- Several `release_date` values are day-level good (`2026-08-29`, `2026-09-23`, `2026-10-02`, `2026-10-17`).
- Some are month-only (`EXT-AD-0003`) or window-based (`TAL-AD-0001..0003`, `2025-09..2026-08`), and these use non-ISO ranges deliberately so nobody mistakes them for verified dates.
- `EXT-AD-0004`'s release date is the date it is *documented airing nationally* (2026-10-04); Chron says the creative had been running "in the past few weeks", so the true first airing is earlier and unknown.

---

## 3. Substantive research gaps

### 3.1 Pre-general/post-general financial picture after 2026-10-14
The last FEC report covered through **2026-10-14** (`FIN-TAL-0007`, `FIN-PAX-0009`). The **post-general report** (covering Oct 15–Nov 30, due in December) was not available at access, and no reliable reporting on final spending was retrieved. So:
- Final spending/cash-on-hand for the closing three weeks of the campaign is **unknown**.
- The "who actually spent more" question cannot be answered from filings here; only AdImpact's tracking estimate exists (E-S008).
- **Known consequence:** $9.92m (Talarico) and $4.78m (Paxton) cash on hand as of 2026-10-14 are the *last verified* balances. Any later figure in integration must not be derived from these by subtraction.

### 3.2 The Paxton leaked audio (campaign-control narrative)
The Lead flagged this as a major media-narrative item, and I agree it belongs in the timeline — but **I could not verify it**. The Independent returned 403 (`E-S032`), the Fox News print URL 404'd (`E-S033`), and Newsweek 403'd (MC-0065). What I have is:
- A headline-level claim that Paxton vented about lacking control of his campaign "as the DC establishment he once battled comes to his aid".
- A Times of India aggregation quoting the fragment "Dragging Us Down" (MC-0066, T3).
- The Lead's verification that the recording is a **2026-09-24 audio leaked to Politico**, reported 2026-10-05.
**What is missing:** the verbatim quotes, the exact reporting date, and confirmation of who published first. The timeline entry is therefore marked ⚠ and the narrative table says "under-verified". **Action:** someone with paywall/proxy access should retrieve the Independent or Politico piece before this is written up.

### 3.3 The TIME / Colbert attribution claim
The Lead relayed: a Colbert interview posted to YouTube drew almost 9 million views and helped raise **$2.5m in 24 hours plus 4,000 new volunteers** (TIME, Feb 2026). I **did not retrieve the TIME article** and have no URL, so I did **not** add a row for it. It is a documented-attribution claim worth having, but per the conventions I will not record a figure I cannot tie to a source. **Action:** Lead to supply the TIME URL, or Agent E to retrieve it in a second pass.

### 3.4 Debate invitations — the full list
Confirmed invitations: **Nexstar/KXAN**, **WFAA/TEGNA**, **Hearst + NBC/Telemundo**, **CNN**, and a **Fox News debate moderated by Bret Baier** that the network agreed to host (E-S021, E-S023). "At least four" acceptances is the best-attested count (Tribune, via Mediaite). Whether Talarico accepted *five* is unresolved: the Baier/Fox invitation may be one of the four or an additional one. **Do not state a count higher than four without a source.**

### 3.5 Opinion coverage is under-collected
I have only a handful of explicit `op_ed` rows (MC-0056, MC-0057, MC-0060, MC-0064) and mostly at headline level. A proper opinion-landscape section (conservative vs liberal columnists on both candidates) would need a dedicated pass; the brief asks for opinion to be distinguished, which is done, but not for it to be exhaustive.

### 3.6 Local Texas TV/newspaper breadth
Present: KPRC (Houston), KWTX (Waco), Chron (Houston), El Paso Times, Dallas Morning News, Fort Worth Star-Telegram, Community Impact, Spectrum News (mynews13), Texas Standard. **Missing:** San Antonio Express-News, Austin American-Statesman as a distinct outlet (it appears only as the Chronicle's co-bylined partner), Rio Grande Valley outlets, Telemundo/Univision Spanish-language coverage (the Spanish *ads* are documented, the Spanish *coverage* is not). Spanish-language media coverage is a real gap for a Texas race with a heavily advertised Spanish-language campaign.

---

## 4. Coverage-parity note (conventions §8)

`media_coverage.csv` row counts: **TALARICO-subject 38**, **PAXTON-subject 28** (66 rows total; as of compilation). This asymmetry is real and has three causes, all recorded rather than padded:

1. **The paid-media story is a Talarico story.** He outspent, out-raised and out-advertised; the record-quarter and record-ad-spending stories centre on him. AdImpact itself puts outside groups at 92% of Paxton's ad support vs 23% of Talarico's (E-S008), so most pro-Paxton advertising is *outside-group* activity with no candidate campaign to report on.
2. **Paxton's campaign creative is undocumented** (§2.3), so Paxton rows are disproportionately about money, scandals, the debate refusal and the leaked audio.
3. **Paxton's own events** (bus tour, Alamo finale) are Agent A's remit and are only touched here where coverage bears on the narrative.

I did **not** inflate Paxton's row count with opinion pieces or headline-only items to force parity. Where a Paxton row is headline-only, it says so.

---

## 5. Method notes for integration

1. **`report_type` values are deliberately heterogeneous** because the brief asked for filings *and* reporting *and* outside-spending estimates in one table. The values used are `Q3 (October Quarterly YYYY)`, `YE`, `12P`, `12R`, `12G`, `Campaign announcement`, `Reporting on ...`, `Independent expenditure ...`, `reported_AdImpact ...`, `FEC filing of outside group ...`, `campaign_claim ...`. **Any of these that is not an FEC report type must not be summed with FEC receipts.** If the Lead prefers a strict vocabulary (`FEC_Q3` / `reported_AdImpact` / `campaign_claim`), the mapping is mechanical: `Q*`/`YE`/`12*` → `FEC_*`; `reported_AdImpact`/`reported (...)`/`Reporting on ...` → `reported`; `Campaign announcement`/`campaign_claim` → `campaign_claim`.
2. **All dollar amounts are rounded to integers** per conventions §3, from FEC cents values. Exact cents are preserved in the notes of the FEC-derived rows where the rounding changes the story (it doesn't for any row here).
3. **`cash_on_hand` is always end-of-period.** Beginning cash is in the notes where useful.
4. **`period` values are explicit date ranges**, not quarter labels, so that irregular FEC periods (pre-primary, pre-runoff, pre-general, partial first report) are unambiguous.
5. **`source_urls` format** is `E-S###|https://...` per conventions §1/§3; the Lead should rewrite these to `SRC-####` at integration. Where the URL is not known, the cell reads `E-S###|url unknown` — that is intentional, not a blank.
6. **Cross-references:** `advertisements.csv.media_coverage` and `media_coverage.csv` use `MC-####` ids defined in `media_coverage.csv`; `campaign_finance.csv` and the timeline use `E-S###` ids defined in `E_sources.csv`. `FIN-####` and `MC-####` are local to this agent and need remapping at integration.
7. **Two source ids are deliberate pointers, not second sources:** `E-S051` resolves to `E-S023` and `E-S052` resolves to `E-S024`. They exist so finance rows can cite a filing-derived figure without implying independent corroboration.

---

## 6. Highest-value things a second pass should chase

1. **The post-general FEC reports** (due December 2026) — this is the only way to close §3.1.
2. **The 2026-09-24 Paxton audio** — verbatim quotes and first-publisher confirmation (§3.2).
3. **Paxton campaign ad titles and video URLs** — the single largest creative gap (§2.3).
4. **Reuters** — at least one wire story to complete the outlet mix (§2.1).
5. **Spanish-language coverage** (Telemundo/Univision) of the Spanish-language ad campaign (§3.6).
6. **The TIME/Colbert attribution** ($2.5m in 24 hours, 4,000 volunteers) with a real URL (§3.3).
7. **The Texas PAC / Senate Leadership Fund IE filings** at transaction level, to test whether the FEC-vs-AdImpact gap in §1.7 is a data-pull artifact or a real reporting difference.
