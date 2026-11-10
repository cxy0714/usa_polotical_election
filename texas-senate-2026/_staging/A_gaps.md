# Agent A (campaign-events) — staging gaps and integration notes

**Agent:** A (campaign-events)
**Access date:** 2026-11-10
**Status:** complete for task-1

Staging files:
- `_staging/A_sources.csv` — 81 sources, headers identical to `09_sources/sources.csv`
- `_staging/A_gaps.md` — this file
- (intermediate, safe to delete after integration: `_A_rows_talarico.tsv`, `_A_rows_paxton.tsv`, `_A_build.py`, `_A_repair1.py`, `_A_repair2.py`, `_A_sources.tsv`)

## 1. Integration instructions for the Lead

1. **Source ids.** Every `source_urls` cell in `02_campaign_events/campaign_events.csv` uses local ids `A-S01` … `A-S81` in the form `A-Sxx|https://…`. Rewrite to global `SRC-####` using `A_sources.csv`. Multiple sources in one cell are separated by a single space.
2. **Row counts.** 93 event rows: 49 `TALARICO`, 44 `PAXTON`. Date range 2025-04-08 → 2026-11-09, plus 19 rows with `event_date = unknown` (schedule-only tour stops and undated debate invitations).
3. **Cross-agent links.** `03_speeches/speech_archive.csv` (Agent D) should link to these `event_id`s, particularly `TAL-EVT-0019` (CNN/Jubilee town hall), `TAL-EVT-0031` (Lubbock), `TAL-EVT-0030` (Midland), `TAL-EVT-0040` (final Austin rally), `TAL-EVT-0042` (victory speech), `PAX-EVT-0011` (Rockwall), `PAX-EVT-0018` (Tyler Nov 1), `PAX-EVT-0027` (concession). `04_visual_archive` (Agent C) can link `TAL-EVT-0031`, `PAX-EVT-0018` (protesters outside) and `PAX-EVT-0008` (Youth Summit).
4. **Phase labelling convention applied (per Lead QA).** Stops 2026-10-19 → 2026-11-01 are `early_voting`; 2026-11-02 → `gotv`. Earlier October tour items are `general`. Final distribution: launch 4 / primary 6 / general 30 / early_voting 16 / gotv 26 / post_election 8 / runoff 3.

## 2. Event-identifier reservations used

- `TAL-EVT-0001` … `TAL-EVT-0049` — allocated sequentially, no gaps except `TAL-EVT-0044`–`0046` post-election items.
- `PAX-EVT-0001` … `PAX-EVT-0045`, with **`PAX-EVT-0014` deliberately deleted** during Laredo deduplication (QA item 4). Do not reuse `PAX-EVT-0014`; the id is retired.
- No `JNT-EVT-*` rows created: no joint/cross-candidate event occurred. The CNN/Jubilee town hall was solo and is logged under `TAL-EVT-0019`.

## 3. Gaps carried forward to `research_gaps.md`

Full detail is in `02_campaign_events/event_coverage_gaps.md`. Summary of what remains unresolved:

1. **Paxton tour stop-by-stop map** — 15 of 19 named cities are schedule-only. Stops were posted on Eventbrite and the listing was removed.
2. **Headquarters opening** — zero rows for either candidate; no source.
3. **Closed-door fundraisers** — zero rows; only aggregate fundraising announcements.
4. **Talarico's two-week flu absence (early October)** — deliberately no rows; documented as an activity gap.
5. **Trump 2026-10-27 itinerary** — announced Lubbock+Waco vs. executed Corpus Christi+Lubbock. `PAX-EVT-0045` logged `disputed`.
6. **"Trump campaigned virtually" vs. four documented in-person Texas trips** — not resolvable from retrieved sources; both dated.
7. **Nacogdoches ~2026-05-27 rally** — attribution ambiguous (Talarico preview vs. Paxton rally); no row created.
8. **Democratic primary field shape** — Allred vs. Crockett; sequence not reconstructed.
9. **Talarico Midland/Lubbock date sequencing** — conflicting; Midland may be 2026-10-26.
10. **Paxton Laredo visit count** — collapsed to one visit; may be two.
11. **No labor, county-party, podcast, press-conference or election-day GOTV events** — searched, none retrieved.
12. **Eight Talarico schedule-only stops** without venue/date confirmation.

## 4. Data-quality notes

- `verification_status` distribution: verified 23 / partially verified 66 / conflicting sources 3 / unverified 1. The high `partially verified` share reflects blocked article bodies (The Hill, KXAN, Valley Central, Houston Chronicle, NYT, CNN article pages), not weak sources.
- `event_status` distribution: held 54 / announced 33 / cancelled 5 / disputed 1. **`announced` is not evidence of occurrence.**
- Three-layer rule enforced: every row has a non-`unknown` `analyst_interpretation` beginning `INTERPRETATION:`; `stated_purpose` is `unknown` where no campaign statement was retrieved (most Paxton tour stops).
- No copyrighted images downloaded. Photo/visual information is caption-level metadata only.
- No strategic conclusions about relative campaign quality are drawn anywhere in these files.

## 5. Files not written by me (out of scope)

`09_sources/sources.csv`, `README.md`, `research_gaps.md`, `07_electoral_context/**`, `08_comparative_analysis/**` — Lead-owned. I wrote only `02_campaign_events/**` and `_staging/A_*`.
