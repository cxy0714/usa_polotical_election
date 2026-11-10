# Agent D (speech) — gaps, caveats and handover notes

Compiled 2026-11-10 by Agent D (speech). All retrieval access date: **2026-11-10**.
Write scope: `03_speeches/**`, `_staging/D_sources.csv`, `_staging/D_gaps.md`, `_staging/D_notes.md`.

---

## 1. What was delivered

| Deliverable | Count / status |
|---|---|
| `03_speeches/speech_archive.csv` | **32 rows** — 18 TALARICO, 14 PAXTON |
| `03_speeches/speech_video_index.csv` | **31 rows** — 18 TALARICO, 13 PAXTON |
| `03_speeches/key_speech_analysis/` | **24 files** — 13 TALARICO, 11 PAXTON (each follows the ten-section brief) |
| `03_speeches/communication_analysis_talarico.md` | complete (13 dimensions + message architecture) |
| `03_speeches/communication_analysis_paxton.md` | complete (13 dimensions + message architecture) |
| `03_speeches/transcripts/` | **1 transcript** — TAL-SPC-1109 (MS NOW / Katy Tur, AI-generated, timecoded) |
| `_staging/D_sources.csv` | 55 rows (D-S01…D-S55) |
| Retrieval date | 2026-11-10 |

---

## 2. Quote-verification caveats (read before quoting anything)

**2.1 Nothing was verified against audio or video.** The compiler could not play any video, audio or captions stream. Therefore:
- Every quotation in the 24 analyses comes from **printed text** — a news article's direct quotation, a transcript page, or a campaign statement quoted by an outlet.
- No quotation has been checked against what the speaker's voice actually said. Before publication, each quote should be spot-checked against the linked video (C-SPAN IDs are given where they exist).
- Timestamps are `unknown` in every file except TAL-SPC-1109.

**2.2 The single timecoded transcript is AI-generated.** `transcripts/TAL-SPC-1109_ms_now_katy_tur_interview_2026-10-21.md` is a Whisper AI transcript from a third-party site (ScribeHawk). Word-level accuracy and timecodes are approximate; the video (`https://www.youtube.com/watch?v=g1hOx3MEFuk`) was not playable. Treat timestamps as ±a few seconds and wording as high-but-not-perfect confidence.

**2.3 Partisan-outlet quotes.** The CNN/Jubilee town hall quotations (TAL-SPC-1107) are relayed by **Hannity.com** (a partisan outlet) from CNN audio. They are internally consistent and the exchange is independently confirmed by CNN's own live post and video page, but they should be re-checked against CNN's footage before print use. The 2021 "God is nonbinary" line is a *replay* of an older remark, not a 2026 statement.

**2.4 Translation-of-a-translation — not usable as quotation.** Crusoé (Brazilian outlet) renders a victory-speech passage about being "underdogs" and facing "$300 million / more than any Senate campaign in American history" ([D-S48](https://crusoe.com.br/diario/democratas-impoem-derrota-a-republicanos-no-texas-apos-mais-de-30-anos/)). This is Portuguese rendering an English speech. **It is recorded as a lead only and is not quoted anywhere in this archive.** The English originals that *were* verified for the victory speech are: "We just took back Texas", "We just proved that all the money in the world is no match for the people of Texas", the "politics of division / politics of love" line, the "billionaire mega donor… power belongs to the people" line, "We follow a barefoot Rabbi…", "Hate is boring…", and "you were my slingshot and tonight we defeated Goliath". Note that Axios and Al Jazeera print slightly different wordings of the "trillionaire megadonor / corrupt defender" sentence — quote from the outlet you cite.

**2.5 Paraphrases and indirect speech are labelled.** Locations where the archive contains paraphrase rather than verbatim:
- PAX-SPC-1105 — the "most radical Democrat" attack and the Promise Plan detail are the outlet's summary `(paraphrase)`.
- PAX-SPC-1108 — the "transition him out of office" joke is reported in indirect speech; Bob Hall's "Freako Talarico" line is a **warm-up speaker**, not Paxton.
- PAX-SPC-1111 — the "pray for Talarico" passage is indirect speech `(paraphrase)`; "We've had a difficult night" survives only as an outlet headline.
- PAX-SPC-1104 — the three-part ask (prayers, contributions, daily voting encouragement) is `(paraphrase)`.
- PAX-SPC-1110 — the characterisation of Talarico as "the most radical Democrat ever to run for statewide office" in Laredo is the outlet's phrasing.

**2.6 Sourcing asymmetry.** Some quotes rest on a single Tier-2 outlet (e.g. the Lubbock sermon and rally quotes all come from one TIME dispatch, reproduced via a mirror site). Where only one outlet printed a quote, the analysis says so.

**2.7 The Lubbock sermon's date is unknown at day level.** TIME's dispatch (2026-02-27) reports the service but does not print its date. It is recorded as `2026-02` with an explicit note. Do not infer "the Sunday before the primary" without a source.

---

## 3. Video and transcript retrievability

**3.1 Video pages that exist but whose media this compiler could not view or transcribe:**
- TAL-SPC-1113 victory speech — C-SPAN 687403 (page retrieved; body not extractable; no transcript endpoint found).
- PAX-SPC-1111 concession — C-SPAN 687387 (same limitation).
- PAX-SPC-1104 Brownsville — C-SPAN 686858 (listing only).
- TAL-SPC-1107 CNN & Jubilee town hall — CNN video page + Spectrum On Demand listing; Daily Mail video page exists; **no transcript published**.
- TAL-SPC-1104 Colbert — YouTube `oiTJ7Pz_59A` (link supplied by TIME with a cue point near 12:22; not verified).
- TAL-SPC-1109 MS NOW — YouTube `g1hOx3MEFuk` (not playable here; transcript captured separately).

**3.2 Sites that blocked retrieval (recorded, not worked around):** Dallas Morning News, WFAA, KERA, RealClearPolitics, MarketScreener, Daily Mail, NYT (paywall), KUT/KERA pages, Houston Chronicle article bodies only sometimes (the `cmf.` syndication subdomain was readable). Where blocked, the archive uses headline/snippet evidence and marks `partially verified`/`unverified`.

**3.3 Transcript policy.** Only one transcript could be legitimately captured (TAL-SPC-1109). For every other speech the archive records the video/transcript URL and marks availability honestly rather than fabricating text. `transcript_url` is `unknown` wherever none exists.

**3.4 Deleted/unavailable material.** No social post in this archive was found deleted; the launch X post and campaign statements are recorded via outlets' quotations. Several social/video items (Rogan episode July 2025, SNL cold open 2026-11-07, Pasadena rally) survive only as headlines/bylines — see §6.

---

## 4. Conflicts between sources (both recorded; do not silently pick one)

| # | Conflict | Sources | Resolution in archive |
|---|---|---|---|
| C1 | **Paxton tour size:** "more than 30 stops" over 18 days vs "one of 12 on Paxton's Come and Take It Tour" | Dock Line citing Texas Tribune ([D-S22](https://docklinemagazine.com/politics-government/paxton-and-talarico-hit-the-road-on-dueling-bus-tours-as-early-voting-begins)) vs KGNS Laredo ([D-S24](https://www.kgns.tv/2026/10/23/paxton-campaigns-laredo-ahead-midterm-elections/)) | Both noted; archive uses "30+ planned" and flags the "12" count as a local-outlet discrepancy |
| C2 | **Paxton Laredo date:** Fri 2026-10-23 vs 2026-10-24 | KGNS same-day report + Laredo Morning Times photo caption ([D-S23](https://cmf.houstonchronicle.com/local/article/paxton-talarico-laredo-stops-texas-senate-race-22493551.php)) vs Texas Tribune photo caption | 2026-10-23 used (same-day local report); conflict flagged |
| C3 | **Talarico Tyler rally date:** 2026-10-21 (KTRE publication) vs "one day after early voting begins" implying 2026-10-20 | [D-S13](https://www.ktre.com/2026/10/21/us-senate-nominee-james-talarico-holds-rally-tyler/) vs [D-S14](https://www.kltv.com/2026/10/16/james-talarico-planning-rally-tyler-one-day-after-early-voting-begins/) | 2026-10-21 recorded, conflict flagged in TAL-SPC-1108 |
| C4 | **"Drought" length:** "32-year" (HPM/KUT) vs "38-year"/"three-decade" (Axios/NYT) vs "first Dem senator since 1988" | multiple | Different baselines: 1988 = last Democratic **U.S. Senate** win (Bentsen); 1994 = last Democratic **statewide** win. Archive states both, as each source does |
| C5 | **Final margin / precinct count:** ~55% with 5,200 of 5,300 precincts reported at time of speech | Houston Public Media ([D-S03](https://www.houstonpublicmedia.org/articles/news/politics/election-2026/2026/11/03/565938/talarico-paxton-senate-race-texas-results/)) | No final certified margin retrieved → `unknown`; only the in-speech figure is recorded |
| C6 | **Axios vs Al Jazeera wording** of the "trillionaire megadonor" sentence | [D-S51](https://www.axios.com/2026/11/04/texas-senate-results-talarico-paxton), [D-S52](https://www.aljazeera.com/news/2026/11/4/talarico-wins-texas-senate-race-ending-decades-of-republican-dominance) | Both printed; analyst must pick and cite one |
| C7 | **Talarico age:** 36 (TIME, Feb 2026) vs 37 (FOX 7, Aug 2026; Houston Chronicle, Nov 2026) | [D-S07](https://www.yerepouni-news.com/she-cant-win-he-can-inside-james-talaricos-faith-based-bid-to-flip-texas/), [D-S37](https://www.fox7austin.com/news/talarico-pulls-former-cornyn-staff-member-campaign-team.amp) | Consistent with a birthday between February and August 2026; archive quotes each source's own figure |

---

## 5. Missing timestamps / missing durations

- **Durations:** `unknown` for all but TAL-SPC-1109 (≈11 minutes). No source in the corpus publishes run-times for the rallies or speeches.
- **Timestamps:** `unknown` everywhere except TAL-SPC-1109. The brief requires timestamps for key quotations; this archive marks `[unknown]` and, where a transcript exists, gives the AI-derived timecode with a caveat.
- **Relevant-timestamps column** in `speech_video_index.csv` is consequently mostly `unknown`, except the Colbert cue point (~12:22, from TIME's link) and the MS NOW segment range.
- **Recommendation for the Lead:** if any downstream product needs verified timecodes, the C-SPAN IDs (687403, 687387, 686858) are the cheapest route — they have continuous single-camera coverage and closed captions, so timecodes can be extracted by a human/video-capable agent.

---

## 6. Events that could not be verified at content level (recorded as index rows only)

These are in `speech_archive.csv` / `speech_video_index.csv` but have **no analysis file** because no speech text was retrievable. They should not be treated as evidence of content, only of occurrence/messaging:

| speech_id | Event | Evidence level |
|---|---|---|
| TAL-SPC-1114 | "New American Dream Tour" rally, Pasadena, 2026-08-09 | Photo caption in FOX 7 Austin ([D-S37](https://www.fox7austin.com/news/talarico-pulls-former-cornyn-staff-member-campaign-team.amp)) — existence + one descriptive line only |
| TAL-SPC-1115 | Midland, George H.W. and Barbara Bush Convention Center (Feb 2026 swing) | TIME reports the venue and prints two quotes ([D-S07](https://www.yerepouni-news.com/she-cant-win-he-can-inside-james-talaricos-faith-based-bid-to-flip-texas/)) — folded into the Lubbock/rally analysis rather than given its own file |
| TAL-SPC-1116 | Laredo, Golondrina Food Park, 2026-10-25 | Photo caption only ([D-S23](https://cmf.houstonchronicle.com/local/article/paxton-talarico-laredo-stops-texas-senate-race-22493551.php)) |
| TAL-SPC-1117 | SNL cold-open cameo, 2026-11-07 | Headline only ([D-S55](https://www.houstonchronicle.com/news/houston-texas/trending/article/james-talarico-snl-cold-open-22519375.php)); the "That's Senator Talafreako" line came from a Lead-supplied Spectrum News item ([D-S49](https://www.spectrumlocalnews.com/tx/south-texas-el-paso/news/2026/11/10/james-talarico-senate-new-member-orientation)) — not independently retrieved here |
| TAL-SPC-1118 | Joe Rogan Experience, July 2025 | Secondary references only ([D-S16](https://hannity.com/media-room/t-of-little-faith-talarico-pressed-on-god-is-nonbinary-abortion-at-cnn-town-hall-watch/), [D-S03](https://www.houstonpublicmedia.org/articles/news/politics/election-2026/2026/11/03/565938/talarico-paxton-senate-race-texas-results/)); no transcript, no quotes beyond the Torah-"subtle instructions" clip description |
| PAX-SPC-1112 | Conroe GOTV stop, 2026-11-02 | Event listing only ([D-S26](https://www.newsfromthestates.com/article/ken-paxton-appears-cancel-final-rally-his-come-and-take-it-tour-alamo)) |
| PAX-SPC-1113 | Paxton primary-night remarks, 2026-03-03 | Not retrieved; only the runoff result is documented |
| PAX-SPC-1114 | Trump Peterbilt event, Denton, 2026-10-01 | CNN transcript confirms the event and Paxton's presence in coverage; **no Paxton speech text** ([D-S45](https://prod.transcripts.cnn.com/show/cnc/date/2026-10-01/segment/11)) |

Additional documented-but-unanalysed Talarico event: a "Love Thy Neighbor" statewide grocery drive in Dallas on 2026-09-09 (photo caption, Washington Examiner). It is not in the CSVs because no speech content or URL was retrievable — flagging it so Agent A/Lead can decide whether to add it from their event sources.

---

## 7. Coverage asymmetry (a finding, not a failure)

Talarico's retrievable long-form record is materially richer than Paxton's:

| Dimension | Talarico | Paxton |
|---|---|---|
| Full unedited speeches with retrievable video IDs | C-SPAN victory speech; CNN town hall clips; YouTube Colbert/MS NOW | C-SPAN concession + Brownsville only |
| Published transcripts | 1 (AI-generated, timecoded) | 0 |
| Debates | Accepted ≥4 invitations; none held | Accepted none (Texas Tribune, 2026-10-07) |
| Town halls | 1 (CNN & Jubilee) | 0 retrieved |
| In-person delivery descriptions by national correspondents | 1 (TIME at Lubbock sermon) | 0 |
| Local TV articles with direct quotes | ~7 outlets | ~5 outlets |
| Analysed appearances | 13 | 11 |

Reasons: (a) Paxton's campaign held fewer long-form/hostile-press formats (no debate, no town hall); (b) local outlets published shorter print reports of his rallies with fewer direct quotes; (c) his campaign's own video assets were not retrievable via the sources found. This is recorded as an observation about communication strategy and archive availability — **not** an evaluative judgement about either candidate's speaking ability.

---

## 8. Attribution and handover notes for the Lead

1. **SRC reconciliation:** this agent used local ids `D-S01`…`D-S55` in `_staging/D_sources.csv` and inside `source_urls` cells (`D-Snn|https://...`). The Lead should map these to global `SRC-####` at integration. No global SRC ids were invented.
2. **Event ids:** `event_id` is `unknown` in every row because Agent A owns `TAL-EVT-####`/`PAX-EVT-####`. The Lead should join speech rows to campaign_events rows by candidate + date + venue (mapping table below is the intended join key).
3. **Suggested joins (speech → event date/venue):**
   - TAL-SPC-1101 → 2025-09-09 Round Rock launch
   - TAL-SPC-1102/1103 → 2026-02 Lubbock (sermon + rally, same day)
   - TAL-SPC-1105 → 2026-03-03 primary night
   - TAL-SPC-1106 → 2026-09-24 Texas Tribune Festival
   - TAL-SPC-1107 → 2026-10-14 CNN & Jubilee town hall
   - TAL-SPC-1108/1109 → 2026-10-21 Tyler (rally + MS NOW interview)
   - TAL-SPC-1110 → 2026-10-27 Midland, The Loft
   - TAL-SPC-1111 → 2026-10-31 Houston, Bayou Music Center
   - TAL-SPC-1112 → 2026-11-02 Austin, Stubb's
   - TAL-SPC-1113 → 2026-11-03 Austin, The Long Center
   - PAX-SPC-1102 → 2026-10-14 tour announcement
   - PAX-SPC-1103 → 2026-10-17 Rockwall Municipal Airport
   - PAX-SPC-1104 → 2026-10-22 Brownsville/McAllen
   - PAX-SPC-1105 → 2026-10-23 Laredo, Palenque Grill
   - PAX-SPC-1106 → 2026-10-30 Houston, Federal American Grill
   - PAX-SPC-1107 → 2026-11-01 Tyler, Republic Icehouse
   - PAX-SPC-1108 → 2026-11-02 Allen, Matt's Rancho Martinez
   - PAX-SPC-1109 → 2026-05-26 Plano runoff night
   - PAX-SPC-1111 → 2026-11-03 Dallas watch party
4. **Alamo finale:** Paxton's planned 2026-11-02 Alamo rally was scrapped; it is indexed in `speech_video_index.csv` (PAX-VID-1113) with `completeness: unknown` and must be carried as a **cancelled** event in Agent A's event table, with the Texas Tribune/KERA citations ([D-S26](https://www.newsfromthestates.com/article/ken-paxton-appears-cancel-final-rally-his-come-and-take-it-tour-alamo), [D-S27](https://www.kera.org/2026/11/02/ken-paxton-cancels-planned-alamo-campaign-stop-ahead-of-election-day/)).
5. **Copyright:** no photographs were downloaded. All image references are URLs/photo credits only (AP, AFP, Getty, KUT, KLTV, Austin American-Statesman). This complies with conventions §0 rule 7.
6. **Phase labels used in analysis prose:** Talarico `primary` through the runoff period (per conventions §2 note); Paxton `primary` (to 2026-03-03), `runoff` (to 2026-05-26), then `general`/`early_voting`/`gotv`/`election_day`/`post_election`.

---

## 9. Biggest single gaps (ranked by impact on any downstream narrative)

1. **No verified English transcript of either victory or concession speech.** The C-SPAN videos exist; a video-capable pass would settle wording and give real timestamps.
2. **No Paxton long-form unscripted appearance.** The absence of a debate removes the only format that would allow direct stylistic comparison of the two candidates on the same question set.
3. **No verified audio for any Talarico or Paxton appearance**, so the brief's voice/speed/pause/intonation dimensions are largely `⚠ unknown` in both communication analyses. This is an evidence limitation, not an omission.
4. **The CNN & Jubilee town hall has no published transcript**; the most consequential faith exchange of the general election is known only through a partisan outlet's quotations plus CNN clips.
5. **Paxton's earlier primary-phase communication (Feb–May 2026)** is nearly undocumented in retrievable speech material; only the runoff-night line survives.
