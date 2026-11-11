# 10_video_frames — 视频帧与人脸识别集

**English** — Frames cut from 145 publicly available videos, with every face detected
and matched against the licensed candidate photographs already in `04_visual_archive/`.
This closes the largest documentary gap in the archive — framing, staging and venue
were `unknown` — without inventing anything: the files below are real frames, the
identity call is a scored nearest-neighbour match, and the limits are listed in §7.

**中文** — 本目录是从 145 段公开视频中截取的帧，画面中的人脸全部经过检测，并与
`04_visual_archive/` 中已有的候选人有授权照片做匹配。它填补了档案中最大的文献缺口
（此前"取景／舞台／场地"均为 `unknown`），且不虚构任何内容：下面是真实帧，身份判定是
带分数的最邻近匹配，局限见第 7 节。

---

## 1. Source videos / 来源视频

145 videos downloaded 2026-11-10/11, published between 20240611 and 20261106. 3 are official
campaign channels; the rest are network/station news packages or wire-service feeds.

**Official campaign channels / 官方竞选频道**

| Video ID | Channel | Upload | Kind | Title |
|---|---|---|---|---|
| `F169Ei20N6g` | James Talarico (official campaign) | 2026-10-19 | tour_launch | James Talarico Kicks Off "Clear Eyes, Full Hearts" Tour |
| `9RUJdj83quk` | Ken Paxton for Senate (official campaign) | 2026-09-23 | rally_speech | WATCH: Ken Paxton Gives Remarks at Cypress Rally |
| `DrD_wR6gEU4` | Ken Paxton for Senate (official campaign) | 2026-09-10 | convention_speech | MUST WATCH: Ken Paxton Delivers Speech at the Republican Midterm Convention |

**News / wire packages / 新闻与通讯社**

| Video ID | Channel | Upload | Kind | Title |
|---|---|---|---|---|
| `bGW8aWXKdEc` | NBC DFW | 2026-10-30 | tour_stop | Thousands gather for James Talarico's 'Clear Eyes, Full Hearts' tour in Dallas |
| `N6PubEh2jZg` | World Watch With Yemi | 2026-10-28 | rally_speech | James Talarico Full Campaign Rally Speech - Lubbock, TX - 10/27/2026 |
| `sa1vT9B4Ick` | FOX 4 Dallas-Fort Worth | 2026-10-29 | rally | LIVE: James Talarico holds El Paso, Texas rally |
| `Ab7QjD4dB50` | CNN | 2026-11-04 | victory_speech | 'This is a win the size of Texas': Talarico's full victory speech |
| `t3BVsDWgNGo` | KVUE | 2026-10-19 | news_package | Talarico holds 'Clear Eyes, Full Hearts' rally; Paxton makes 'Come and Take It' tour stops |
| `Br3kA5QQDQw` | CBS TEXAS | 2026-10-18 | tour_launch | Ken Paxton kicks off statewide bus tour ahead of early voting in Texas Senate race |
| `puVR9bfMcls` | KHOU 11 | 2026-10-21 | rally | Texas Senate race: Paxton rallies in Conroe amid tight polls |
| `Qk3xvHejQYU` | Associated Press | 2026-11-03 | final_rally | LIVE: Ken Paxton speaks at a rally in Allen, Texas |
| `35-u_mTo-w8` | NBC DFW | 2026-11-03 | rally | Ken Paxton rallies Collin County Republicans in final push before Texas Senate election |
| `h14iskBaBSI` | PBS NewsHour | 2026-11-04 | concession_speech | WATCH: Republican Ken Paxton speaks after losing Texas Senate race |
| `vW1QJCc0_Hw` | CBS TEXAS | 2026-10-19 | rally | James Talarico holds Plano rally ahead of Texas senate election |
| `PWow10eQp-o` | KENS 5 | 2026-10-25 | rally | James Talarico visits San Antonio on 'Clear Eyes, Full Hearts' campaign tour |
| `0nXJYOIZ4Fk` | Angie A (third-party upload) | 2026-10-30 | rally_speech | James Talarico for Texas Rally: Clear Eyes, Full Hearts |
| `qbQzb0sz2OI` | CBS TEXAS | 2026-11-04 | watch_party | James Talarico supporters erupt in celebration at Austin watch party |
| `63Eb4VlhxSE` | KXAN | 2026-11-04 | news_clip | Crowds cheer as AP projects James Talarico wins the U.S. Senate race in Texas |
| `7oqcGDWT4Os` | CBS TEXAS | 2026-11-03 | final_rally | Ken Paxton holds final campaign rally in Allen ahead of midterm elections |
| `YE4pIbpZhAE` | CBS TEXAS | 2026-07-28 | rally | Paxton, Abbott rally North Texas Republicans as Texas Senate race heats up |
| `O7TIsfy4PEQ` | NBC DFW | 2026-11-04 | concession_speech | Full speech: Ken Paxton concedes U.S. Senate race to James Talarico |
| `7c8BeNjXyks` | USA TODAY | 2026-11-04 | concession_speech | Ken Paxton concession speech on midterm election loss to James Talarico |
| `Ln7A66zGNYo` | CBS19 | 2026-10-21 | rally | Talarico rallies supporters in Tyler as Texas Senate race tightens |
| `ufXizbHdU9c` | CBS19 | 2026-10-20 | news_package | Talarico rallies in Tyler as Paxton tours Texas amid tightening Senate race |
| `M8x0ZGVlBhI` | 25 News KXXV | 2026-09-17 | tour_stop | Democratic Senate candidate James Talarico makes campaign stop at Baylor University |
| `aU8yJGKC3DE` | Good Morning America | 2026-11-04 | news_clip | James Talarico wins Texas Senate race |
| `O6HogoPDp4Y` | KETK NBC | 2026-11-01 | rally_speech | Ken Paxton speaks at tense United States Senate campaign rally in Tyler |
| `dOg1d2XSBoQ` | CBS19 | 2026-11-02 | rally | Ken Paxton rallies supporters in Tyler as Senate race enters final stretch |
| `8B6h7IWjCok` | FOX 4 Dallas-Fort Worth | 2026-09-09 | convention_speech | FULL: Ken Paxton's 2026 RNC Midterm Convention Speech |
| `tBuHy4Wan7E` | James Talarico | 20261006 | rally_speech | James Talarico SHUTS DOWN Ken Paxton LIVE ON AIR |
| `4k88mIFdTK4` | James Talarico | 20260716 | rally_speech | James Talarico delivers PERFECT RESPONSE to Ken Paxton's attacks |
| `EbcVUjFRpxc` | James Talarico | 20260730 | debate_challenge | James Talarico CHALLENGES Ken Paxton to 3 Debates LIVE ON AIR |
| `etkbx4itBUI` | James Talarico | 20261104 | victory_speech | Victory Party LIVE: James Talarico for US Senate |
| `iEB7l5NDQos` | ABC13 Houston | 20260830 | news_package | New poll shows James Talarico leading Ken Paxton by 6 percentage points in Senate race |
| `VfuU7Qy5bW0` | James Talarico | 20260305 | victory_speech | James Talarico delivers Democratic primary victory speech |
| `FUSyVVIpgug` | USA TODAY | 20261104 | news_package | How Talarico and Paxton supporters reacted to Texas election results |
| `ezPKVpfjMGE` | James Talarico | 20261106 | victory_speech | James Talarico Delivers Election Night Victory Speech |
| `1n-pbdJf4B0` | James Talarico | 20260304 | victory_speech | James Talarico full remarks at Democratic primary election night watch party |
| `hZXByZ8c4PU` | CBS News | 20260527 | interview | Full interview: James Talarico on Texas Senate race, Ken Paxton and more |
| `83pOVOCMjH0` | The Dallas Morning News | 20261020 | news_package | 'It feels like I'm taking away part of myself:' North Texas voters on Paxton-Talarico Senate race |
| `ajINMbVvxW0` | CBS News | 20260923 | news_package | Talarico leads Paxton in Texas Senate race, Marist poll shows |
| `AWOtbRQoYhc` | Ken Paxton for Senate | 20260827 | rally_speech | Watch - Ken Paxton Delivers Remarks: James Talarico Sold Us Out To China |
| `uKFhoKvxYzA` | CBS Mornings | 20261102 | news_package | Texas voters explain why they're choosing Talarico or Paxton |
| `6OEGm8DHIoM` | FOX 4 Dallas-Fort Worth | 20261104 | rally_speech | FULL VIDEO: Ken Paxton speaks about loss to James Talarico in US Senate race |
| `aDq1dsAybT0` | CBS19 | 20261009 | debate_challenge | Trump urges Paxton-Talarico debate as Texas Senate race deadlocked |
| `fDKCD7CThLA` | CBS News | 20261104 | news_package | Gina Hinojosa beats Greg Abbott and James Talarico defeats Ken Paxton in Texas, CBS News projects |
| `gj_VARdubh4` | FOX 26 Houston | 20261104 | rally_speech | FULL VIDEO: Ken Paxton speaks about loss to James Talarico in US Senate race |
| `aZqbUmYTMEY` | Fox News Clips | 20260911 | news_package | Texas voters reveal TOP issues in critical Paxton-Talarico US Senate race |
| `WwTXGDB208Q` | CBS News | 20261019 | news_package | Can James Talarico convert Republican voters against Ken Paxton in Texas? |
| `sVgkETyyuPg` | CBS News | 20261030 | news_package | James Talarico leading Ken Paxton in Texas, new poll shows |
| `CrnA_Q7YtiI` | Fox News Clips | 20261012 | rally_speech | 'VERY STRANGE time to disappear': Paxton SLAMS Talarico over campaign absence |
| `PgH7p00Q-6M` | CBS TEXAS | 20261104 | news_package | Paxton supporters react to loss to Talarico in Texas Senate race |
| `CamYITDOLDE` | James Talarico | 20260627 | convention_speech | James Talarico Accepts Texas US Senate Nomination |
| `1dTE48BFV5g` | CBS News | 20261019 | news_package | New poll shows Talarico, Paxton essentially tied in Texas as Democrats, Republicans weigh midterms |
| `RW4Xug6fziI` | Face the Nation | 20261018 | news_package | CBS News poll shows a Texas toss-up with Talarico, Paxton in tight Senate race |
| `x5sJnTD4khQ` | NewsNation | 20260906 | debate | Ken Paxton needs to debate James Talarico, Texas Republican says |
| `vDR5SgTvMOs` | USA TODAY | 20261103 | news_package | Ken Paxton or James Talarico? In Texas election, voters on each side feel hope and fear |
| `2E8jb68eVnY` | Forbes Breaking News | 20260818 | news_package | Is Texas Flippable? Here’s What The Latest Paxton-Talarico Poll Says |
| `0vuqwyCPEGA` | CBS19 | 20261013 | rally_speech | ​Texas Attorney General, U.S. Senate candidate Ken Paxton criticizes James Talarico in speech |
| `MGbyIZ_RS4g` | CBS TEXAS | 20260528 | ad | Paxton, Talarico release attack ads as general election matchup set |
| `Atj03AXtV8U` | James Talarico | 20240611 | convention_speech | James Talarico Condemns Christian Nationalism at the Texas Democratic Convention |
| `uJd1L5Ai2As` | KENS 5: Your San Antonio News Source | 20260530 | convention_speech | James Talarico revs up general election campaign in SA after Paxton secures GOP Senate nomination |
| `hhgYQq9VzSY` | CBS TEXAS | 20261004 | news_package | Republicans, Democrats push to motivate voters in Texas Senate race between Talarico and Paxton |
| `JWAECgb0vXo` | CBS19 | 20261019 | news_package | Talarico holds narrow lead over Paxton in Texas Senate race, UH poll finds |
| `lj1CnjPgnvY` | Forbes Breaking News | 20261023 | news_package | Top Pollster Reveals Who Is Winning Between Paxton And Talarico In Latest Poll In Texas Race |
| `raJtXQmqnTA` | Forbes Breaking News | 20261031 | news_package | BREAKING NEWS: Ken Paxton Savages 'Vegan' James Talarico At Get Out The Vote Rally In Fort Worth |
| `0LFki8aA1lk` | Forbes Breaking News | 20260917 | news_package | Paxton And Talarico Neck-And-Neck In Tight Texas Senate Race: New Poll |
| `PNUUDNuG2us` | KENS 5: Your San Antonio News Source | 20260828 | news_package | New poll shows James Talarico leading Ken Paxton in Texas Senate race |
| `0lD4eJd87_M` | CBS TEXAS | 20261019 | news_package | CBS News poll: Talarico-Paxton Senate race is a Texas toss-up |
| `-kK6UPqlhhI` | CBS19 | 20260923 | debate | Senate debate between Paxton and Talarico appears increasingly unlikely |
| `NjjrhccCg5o` | CBS TEXAS | 20261026 | news_package | Paxton vs. Talarico: Political science expert explains what's at stake in 2026 Texas Senate race |
| `AHN7ftYCqjU` | Ken Paxton for Senate | 20260901 | rally_speech | Watch - President Trump urges Texas to Vote for Ken Paxton |
| `CsuL_N6eR3M` | News 4 (WOAI) San Antonio | 20261102 | news_package | James Talarico, Ken Paxton rally San Antonio voters as midterms approach |
| `D2B_Edu3EIw` | USA TODAY | 20260527 | rally_speech | Ken Paxton speech after Texas election win thanks Donald Trump, labels James Talarico a 'threat' |
| `rZZ6lAUuLGQ` | CBS TEXAS | 20260730 | debate_challenge | Ken Paxton, James Talarico agree to televised Texas U.S. Senate debate |
| `r08AxsHMJ8k` | KWTX News10 | 20261104 | rally_speech | Ken Paxton addresses supporters after losing U.S. Senate race to James Talarico |
| `sIwAf4nEH78` | USA TODAY | 20260909 | convention_speech | Ken Paxton RNC speech contrasts campaign with James Talarico and boasts of Donald Trump endorsement |
| `6_CfM0pDZn4` | KETK NBC | 20260927 | news_package | Talarico leads Paxton in latest Texas Senate race poll |
| `nKDCUz_fwik` | KENS 5: Your San Antonio News Source | 20261024 | rally_speech | Ken Paxton holds rally in Selma; James Talarico casts his vote |
| `ZGg8TYQnI4E` | News24 | 20260529 | ad | Ken Paxton targets James Talarico in scathing new campaign ad as Texas campaign intensifies |
| `qy3GI-728yw` | Ken Paxton for Senate | 20260902 | tour_launch | Watch - Ken Paxton Speaks in Parker County on the Protecting the Texas Promise Tour |
| `OZmlQ4xPF2k` | CBS19 | 20260716 | debate | Paxton agrees to debate with Talarico as Texas Senate race intensifies |
| `MtR4fLsIXP4` | Ken Paxton for Senate | 20260629 | ad | Paxton for Senate new ad “Hypocrite” |
| `Xgkb_EJ0F1Q` | KETK NBC | 20260624 | news_package | New Texas poll shows Paxton ahead of Talarico in tight Senate race |
| `m7BAUXTiJVY` | Associated Press | 20261104 | rally_speech | LIVE: James Talarico speaks after winning the Texas Senate election |
| `ib8W9kBcaJU` | James Talarico | 20260829 | rally_speech | LIVE: James Talarico & Mark Cuban on Policy and Culture |
| `a4gD6UWdo4g` | Brian Tyler Cohen News | 20260912 | ad | James Talarico releases devastating ad against Ken Paxton |
| `AOklW9PYZvY` | MS NOW | 20261028 | rally_speech | James Talarico holds midterm rally following call on Paxton to return taxpayer funds |
| `_4AbnkHuDaU` | PBS NewsHour | 20261104 | rally_speech | WATCH: Democrat James Talarico speaks after winning Texas Senate seat |
| `FQFSgvAq4E4` | CBS19 | 20261016 | tour_launch | Texas Senate candidates Paxton, Talarico bring statewide tours to East Texas |
| `1_KTIl1zJIM` | Ken Paxton for Senate | 20261020 | rally_speech | Ablaze - Radical James Talarico is Anti-Texas |
| `WLDE9LrGpNk` | Jimmy Kimmel Live | 20260911 | interview | Jimmy Kimmel’s Interview with James Talarico That the FCC Doesn’t Want You To See |
| `FpIN6tYC5XM` | The Diary Of A CEO | 20261102 | rally_speech | James Talarico: Here Is How They Designed The System To Keep You Poor! |
| `VnurpLQd4c0` | Jubilee | 20261018 | town_hall | James Talarico Debates Texas Voters: Jubilee x CNN Townhall |
| `8aHhIOBLPwM` | Fox News | 20261104 | victory_speech | BREAKING: Dems FLIP Texas as Talarico wins Senate, Abbott loses governor race |
| `Qm4gcgdbRJ0` | CBS TEXAS | 20261104 | victory_speech | Talarico, Hinojosa celebrate historic Texas wins at Whataburger |
| `X6B2-8rX9Cc` | The Washington Examiner | 20261104 | concession_speech | Ken Paxton delivers his concession speech after losing the Texas Senate race to James Talarico |
| `Vj3hXp6DdoI` | Associated Press | 20261103 | rally_speech | LIVE: James Talarico speaks at a rally in Austin |
| `dtfhGrFHdbo` | CBS Austin | 20261104 | victory_speech | WATCH LIVE: James Talarico speaks to supporters on election night |
| `N7oKRMPMcXk` | CBS News | 20260909 | interview | Full interview: James Talarico on affordability, Paxton's AI ads and more |
| `Uarzvd9iPA8` | MS NOW | 20260902 | interview | MS NOW shifts Talarico, Paxton Texas Senate race to 'TOSS-UP': ‘There is a REAL race here’ |
| `doAzTmVf-FQ` | Forbes Breaking News | 20261104 | concession_speech | NEW: James Talarico Reveals Whether Ken Paxton Has Called Him To Concede |
| `_EorvCbDcR4` | NBC News | 20261104 | victory_speech | Full speech: James Talarico projected winner in Texas Senate race |
| `v08ENYbhdvQ` | Forbes Breaking News | 20261104 | concession_speech | BREAKING: Ken Paxton Delivers Less-Than-2-Minute Concession Speech After Losing Texas Senate Race |
| `8rQHiGHrPes` | Face the Nation | 20260527 | interview | Full interview: James Talarico talks Texas Senate race, Ken Paxton, corruption and more |
| `9ao9d7zxkBQ` | Face the Nation | 20260909 | interview | Full interview: James Talarico discusses agenda if elected to Senate, taking on Ken Paxton and more |
| `_efNEPn-lpI` | CBS19 | 20261021 | tour_launch | WATCH LIVE: U.S. Senate candidate James Talarico makes campaign stop in Tyler during statewide tour |
| `txVoQv_3trw` | KVUE | 20261104 | concession_speech | Ken Paxton concedes to James Talarico in Texas U.S. Senate race |
| `eEwRgv9KkvM` | Associated Press | 20260527 | rally_speech | LIVE: Ken Paxton and John Cornyn speeches after Texas Senate primary runoff (Full) |
| `5iUr-IZFnX4` | Jordan Conradson | 20260528 | ad | Ken Paxton ad SLAMS “Radical Talarico” as “Too Low-T for Texas” |
| `pGA4dcKgv28` | LiveNOW from FOX | 20260521 | rally_speech | WATCH: Ken Paxton holds campaign rally in Katy, TX |
| `dm7It_ox_ZY` | FOX 4 Dallas-Fort Worth | 20261030 | rally_speech | LIVE: Talarico, Hinojosa rally in Dallas as Texas races tighten |
| `pD3jKRdC1nY` | CBS Austin | 20260131 | rally_speech | WATCH: Rep. Talarico STOP ICE Rally |
| `OHhEkaGaqRA` | CBS19 | 20261104 | concession_speech | BREAKING: Gov. Greg Abbott concedes, Talarico wins over Paxton |
| `4cF14ikKgBU` | FOX 4 Dallas-Fort Worth | 20261016 | rally_speech | LIVE: James Talarico holds campaign rally in San Marcos |
| `Y0vXI8jET9s` | MAGNO NEWS | 20261102 | rally_speech | 🇺🇸 Ken Paxton For US Senate Rally in San Antonio, Texas [LIVE] |
| `LRqgkScXOVs` | ABC News 4 | 20261025 | rally_speech | LIVE:  James Talarico holds a rally in San Antonio |
| `XjWyySYJCD8` | WFAA | 20261103 | final_rally | 2026 midterms: Paxton, Talarico make final push ahead of Election Day |
| `ma-2faLUnO0` | KCBD NewsChannel 11 - Lubbock, TX | 20261027 | rally_speech | Live with the crowd for Talarico rally at Fiesta Center (5 p.m.) |
| `8o_atiOPOrc` | Ken Paxton for Senate | 20260831 | rally_speech | Watch - Ken Paxton on Keeping It Real with Jillian Michaels |
| `FtJbp3AxhSQ` | FOX 26 Houston | 20261016 | rally_speech | LIVE: James Talarico holds campaign rally in San Marcos |
| `kag4jbVRGBw` | FOX 7 Austin | 20261016 | rally_speech | LIVE: James Talarico holds campaign rally in San Marcos |
| `7R6cYE9MKPQ` | KVUE | 20261016 | tour_launch | Talarico, Paxton ramp up campaign tours |
| `mky5sersn8E` | FOX 7 Austin | 20261030 | rally_speech | LIVE: Talarico, Hinojosa rally in Dallas as Texas races tighten |
| `mUT71uj4Dg4` | FOX 26 Houston | 20261030 | rally_speech | LIVE: Talarico, Hinojosa rally in Dallas as Texas races tighten |
| `CtNU9j_L3a4` | CBS Austin | 20261030 | rally_speech | WATCH LIVE: Texas AG and U.S. Senate Candidate Ken Paxton holds a campaign rally near Beaumont. |
| `x8UfXvN2nmI` | KPRC 2 Click2Houston | 20261104 | concession_speech | Ken Paxton concedes Texas Senate race to James Talarico |
| `qTvwJaEU_hU` | Oneindia News | 20260805 | rally_speech | WATCH: Protesters DISRUPT Ken Paxton Event, Campaign Rally DESCENDS Into Chaos During Texas Speech |
| `E18YdNGIBIY` | KABB FOX San Antonio | 20260809 | rally_speech | LIVE NOW: AG Ken Paxton in San Antonio Protecting The Texas Promise Rally |
| `E_FZ0C2WSNQ` | ARC El Paso | 20261104 | rally_speech | James Talarico speaks after Texas victory over Ken Paxton in US Senate race |
| `EncpHndwz_o` | CBS19 | 20260916 | rally_speech | WATCH LIVE: U.S. Senate candidate Ken Paxton holds meet and greet rally in Longview |
| `dxvkQOBZkNs` | CNN | 20261016 | rally_speech | Talarico rally in Texas 19 days before Senate election |
| `SgCjayat99A` | MS NOW | 20261031 | rally_speech | James Talarico and Gina Hinojosa deliver remarks at a rally in Houston |
| `XMonsb21rMQ` | CNN | 20261103 | final_rally | Talarico's final rally before midterm election day |
| `CjA0E1FkA6o` | FOX 26 Houston | 20261104 | rally_speech | FULL: James Talarico speech after Texas Senate victory |
| `DFFfim-KOR4` | KTSM 9 NEWS | 20261027 | tour_launch | James Talarico campaign tour stop in El Paso |
| `KWyHDDBXKNE` | NBC News | 20260724 | rally_speech | James Talarico unveils border policy plan for TX Senate bid, saying 'both parties have failed us' |
| `DQDL694frhs` | CBS TEXAS | 20261015 | town_hall | James Talarico addresses campaign absence, abortion debate and immigration at CNN Jubilee town hall |
| `8u-VGOO2srs` | KCENNews | 20261014 | town_hall | James Talarico CNN town hall comes as Texas Senate race tightens |
| `-JBnqzzacoE` | KTSM 9 NEWS | 20261027 | tour_launch | James Talarico "Clear Eyes Full Hears" campaign tour stop in El Paso |
| `B2Yb3GNvbRU` | CBS TEXAS | 20260525 | final_rally | Cornyn targets Paxton’s “baggage” in final push before GOP runoff for Senate |
| `zXhUcjSzJbc` | Rebel HQ | 20260226 | town_hall | Talarico’s Town Hall Answer Has Texas Shook |
| `XOWZbLqBzG4` | CNN | 20261015 | town_hall | John Berman breaks down the CNN & Jubilee Town Hall with James Talarico |
| `2vN6aZJ4K2U` | Megyn Kelly | 20261015 | town_hall | The KEY Moment From James Talarico's CNN Town Hall That Shows Why Paxton Might Be in Trouble |
| `M9DWEo5myD0` | MS NOW | 20261103 | final_rally | Ken Paxton speaks on eve of midterm election |

URLs are in `video_sources.csv`.

## 2. Method / 方法

1. **Sampling** — every 0.5 s for videos ≤ 120 s, every 1.0 s above that
   (**106,295** face crops kept in total).
2. **Detection** — OpenCV YuNet (ONNX, 232 KB), score ≥ 0.55, face side ≥ 64 px,
   up to 3 faces per sampled frame.
3. **Identity** — OpenCV SFace (ONNX, 38.7 MB). Embeddings are L2-normalised and
   compared by cosine against **62 reference embeddings** built from the archive's own
   licensed candidate photographs (`04_visual_archive/talarico/campaign/` 7 files,
   `04_visual_archive/paxton/campaign/` 69 files; 62 usable).
4. **Decision rule** — class-balanced best-per-class cosine; a label is assigned only if
   `best ≥ 0.40` **and** `best − second-best ≥ 0.05`, otherwise `unknown`.
5. **Reference sanity check** — same-class mean cosine **0.499**, cross-class mean
   **0.123**. The two reference pools are cleanly separated.
6. **De-duplication** — each surviving candidate frame gets a 64-bit DCT perceptual hash
   and a torso-region colour signature. Within a video, a frame is dropped when the hash
   is within 12 bits of an accepted frame (near-identical framing) or when the torso colour
   matches within 12 RGB units and the hash within 20 bits. Across videos only a
   near-identical image (≤ 6 bits) counts as a duplicate, so different venues survive.
   At most 3 frames per video per outfit-colour bucket are kept.
7. **Selection floor** — `identity_sim ≥ 0.62`, `sharpness ≥ 40`, `face width ≥ 80 px`;
   max 8 per video, 2.5 s minimum spacing. Result: **220 candidates → 172 kept frames
   (87 Talarico / 85 Paxton); 48 redundant frames removed**.
8. **Measurements** — shot scale from face-width / frame-width ratio; face box in source
   pixels; Laplacian sharpness; mean grey brightness; mean RGB of the region below the
   face (a crude torso proxy, **not** a clothing classification).
9. **Shot layer** (`extract_keyframes.py`) — a 160×90 / 2 fps proxy is decoded per video,
   cuts are detected on frame-to-frame difference with an adaptive threshold, and up to
   8 scenes keep a full-resolution keyframe measured for brightness, contrast, sharpness,
   colourfulness (Hasler–Süsstrunk), saturation, mean RGB and YuNet face fraction.
10. **Audio layer** (`analyze_speech.py`) — 16 kHz decode, energy VAD, pause/loudness/F0/
   speech-rate measurement and caption parsing; see `../11_speech_audio/README.md`.

Scripts: `../_staging/vision/{extract_faces,recognize_faces,curate}.py`;
config: `../_staging/vision/videos.json`; models cached in `../_staging/vision/models/`.

## 3. What the identity pass found / 身份识别结果

| Source video | Kind | Talarico | Paxton | unknown | no face |
|---|---|---|---|---|---|
| FULL VIDEO: Ken Paxton speaks about loss to James Talarico in US… | rally_speech | 0 | 140 | 0 | 0 |
| FULL VIDEO: Ken Paxton speaks about loss to James Talarico in US… | rally_speech | 0 | 140 | 0 | 0 |
| FULL: Ken Paxton's 2026 RNC Midterm Convention Speech | convention_speech | 0 | 140 | 0 | 0 |
| James Talarico Accepts Texas US Senate Nomination | convention_speech | 140 | 0 | 0 | 0 |
| Ken Paxton concedes Texas Senate race to James Talarico | concession_speech | 0 | 139 | 0 | 1 |
| WATCH: Ken Paxton Gives Remarks at Cypress Rally | rally_speech | 0 | 139 | 0 | 1 |
| Ken Paxton speaks on eve of midterm election | final_rally | 0 | 139 | 1 | 0 |
| LIVE: James Talarico speaks at a rally in Austin | rally_speech | 139 | 0 | 1 | 0 |
| James Talarico campaign tour stop in El Paso | tour_launch | 139 | 0 | 1 | 0 |
| LIVE: Ken Paxton speaks at a rally in Allen, Texas | final_rally | 0 | 137 | 1 | 2 |
| Talarico's final rally before midterm election day | final_rally | 137 | 0 | 3 | 0 |
| BREAKING NEWS: Ken Paxton Savages 'Vegan' James Talarico At Get… | news_package | 0 | 136 | 1 | 3 |
| James Talarico Condemns Christian Nationalism at the Texas… | convention_speech | 134 | 2 | 3 | 1 |
| BREAKING: Ken Paxton Delivers Less-Than-2-Minute Concession… | concession_speech | 0 | 134 | 1 | 5 |
| WATCH: Protesters DISRUPT Ken Paxton Event, Campaign Rally… | rally_speech | 0 | 133 | 2 | 5 |
| Ken Paxton RNC speech contrasts campaign with James Talarico and… | convention_speech | 0 | 131 | 8 | 1 |
| Ken Paxton addresses supporters after losing U.S. Senate race to… | rally_speech | 0 | 131 | 2 | 7 |
| WATCH LIVE: U.S. Senate candidate Ken Paxton holds meet and greet… | rally_speech | 0 | 127 | 10 | 3 |
| New Texas poll shows Paxton ahead of Talarico in tight Senate race | news_package | 61 | 62 | 17 | 0 |
| Talarico leads Paxton in latest Texas Senate race poll | news_package | 59 | 63 | 18 | 0 |
| Ken Paxton concedes to James Talarico in Texas U.S. Senate race | concession_speech | 0 | 120 | 11 | 2 |
| LIVE:  James Talarico holds a rally in San Antonio | rally_speech | 120 | 0 | 9 | 11 |
| Watch - Ken Paxton Delivers Remarks: James Talarico Sold Us Out… | rally_speech | 0 | 118 | 22 | 0 |
| FULL: James Talarico speech after Texas Senate victory | rally_speech | 116 | 1 | 18 | 5 |
| James Talarico wins Texas Senate race | news_clip | 117 | 0 | 23 | 0 |
| WATCH: Ken Paxton holds campaign rally in Katy, TX | rally_speech | 0 | 115 | 21 | 4 |
| James Talarico delivers PERFECT RESPONSE to Ken Paxton's attacks | rally_speech | 103 | 11 | 26 | 0 |
| James Talarico: Here Is How They Designed The System To Keep You… | rally_speech | 109 | 0 | 31 | 0 |
| Texas Senate race: Paxton rallies in Conroe amid tight polls | rally | 52 | 56 | 32 | 0 |
| MUST WATCH: Ken Paxton Delivers Speech at the Republican Midterm… | convention_speech | 0 | 108 | 31 | 1 |
| Talarico rallies supporters in Tyler as Texas Senate race tightens | rally | 54 | 54 | 31 | 1 |
| Ken Paxton delivers his concession speech after losing the Texas… | concession_speech | 0 | 106 | 34 | 0 |
| Full interview: James Talarico on Texas Senate race, Ken Paxton… | interview | 106 | 0 | 34 | 0 |
| Full interview: James Talarico talks Texas Senate race, Ken… | interview | 106 | 0 | 34 | 0 |
| Full speech: Ken Paxton concedes U.S. Senate race to James… | concession_speech | 0 | 106 | 1 | 1 |
| Jimmy Kimmel’s Interview with James Talarico That the FCC Doesn’t… | interview | 101 | 1 | 38 | 0 |
| Ken Paxton, James Talarico agree to televised Texas U.S. Senate… | debate_challenge | 50 | 50 | 5 | 0 |
| Talarico holds 'Clear Eyes, Full Hearts' rally; Paxton makes… | news_package | 59 | 39 | 40 | 2 |
| Full interview: James Talarico on affordability, Paxton's AI ads… | interview | 97 | 1 | 39 | 3 |
| Full interview: James Talarico discusses agenda if elected to… | interview | 97 | 1 | 39 | 3 |
| WATCH: Republican Ken Paxton speaks after losing Texas Senate race | concession_speech | 0 | 97 | 37 | 6 |
| James Talarico CHALLENGES Ken Paxton to 3 Debates LIVE ON AIR | debate_challenge | 97 | 0 | 43 | 0 |
| Republicans, Democrats push to motivate voters in Texas Senate… | news_package | 46 | 50 | 43 | 1 |
| James Talarico and Gina Hinojosa deliver remarks at a rally in… | rally_speech | 96 | 0 | 44 | 0 |
| LIVE: James Talarico & Mark Cuban on Policy and Culture | rally_speech | 93 | 1 | 46 | 0 |
| 'VERY STRANGE time to disappear': Paxton SLAMS Talarico over… | rally_speech | 6 | 87 | 47 | 0 |
| Paxton, Talarico release attack ads as general election matchup… | ad | 55 | 35 | 42 | 8 |
| James Talarico addresses campaign absence, abortion debate and… | town_hall | 56 | 34 | 50 | 0 |
| Ken Paxton speaks at tense United States Senate campaign rally in… | rally_speech | 40 | 49 | 49 | 2 |
| WATCH LIVE: Texas AG and U.S. Senate Candidate Ken Paxton holds a… | rally_speech | 1 | 84 | 48 | 7 |
| LIVE NOW: AG Ken Paxton in San Antonio Protecting The Texas… | rally_speech | 0 | 85 | 54 | 1 |
| Ken Paxton speech after Texas election win thanks Donald Trump,… | rally_speech | 0 | 83 | 57 | 0 |
| Trump urges Paxton-Talarico debate as Texas Senate race deadlocked | debate_challenge | 35 | 47 | 57 | 1 |
| James Talarico holds midterm rally following call on Paxton to… | rally_speech | 81 | 1 | 57 | 1 |
| James Talarico delivers Democratic primary victory speech | victory_speech | 81 | 0 | 59 | 0 |
| James Talarico Debates Texas Voters: Jubilee x CNN Townhall | town_hall | 80 | 0 | 60 | 0 |
| James Talarico Full Campaign Rally Speech - Lubbock, TX -… | rally_speech | 77 | 2 | 61 | 0 |
| James Talarico SHUTS DOWN Ken Paxton LIVE ON AIR | rally_speech | 74 | 1 | 65 | 0 |
| James Talarico holds Plano rally ahead of Texas senate election | rally | 32 | 42 | 26 | 2 |
| Watch - Ken Paxton on Keeping It Real with Jillian Michaels | rally_speech | 1 | 72 | 67 | 0 |
| Talarico rally in Texas 19 days before Senate election | rally_speech | 67 | 6 | 61 | 6 |
| WATCH LIVE: U.S. Senate candidate James Talarico makes campaign… | tour_launch | 71 | 2 | 63 | 4 |
| LIVE: James Talarico speaks after winning the Texas Senate… | rally_speech | 71 | 0 | 69 | 0 |
| James Talarico unveils border policy plan for TX Senate bid,… | rally_speech | 39 | 32 | 68 | 1 |
| Full speech: James Talarico projected winner in Texas Senate race | victory_speech | 70 | 0 | 70 | 0 |
| 'This is a win the size of Texas': Talarico's full victory speech | victory_speech | 70 | 0 | 70 | 0 |
| WATCH: Democrat James Talarico speaks after winning Texas Senate… | rally_speech | 69 | 0 | 71 | 0 |
| James Talarico speaks after Texas victory over Ken Paxton in US… | rally_speech | 65 | 0 | 73 | 2 |
| James Talarico full remarks at Democratic primary election night… | victory_speech | 65 | 0 | 75 | 0 |
| Ken Paxton holds final campaign rally in Allen ahead of midterm… | final_rally | 27 | 37 | 35 | 3 |
| NEW: James Talarico Reveals Whether Ken Paxton Has Called Him To… | concession_speech | 60 | 0 | 80 | 0 |
| CBS News poll: Talarico-Paxton Senate race is a Texas toss-up | news_package | 30 | 30 | 72 | 0 |
| LIVE: Ken Paxton and John Cornyn speeches after Texas Senate… | rally_speech | 0 | 58 | 82 | 0 |
| Ken Paxton rallies Collin County Republicans in final push before… | rally | 0 | 57 | 75 | 8 |
| Ken Paxton ad SLAMS “Radical Talarico” as “Too Low-T for Texas” | ad | 51 | 5 | 41 | 2 |
| 🇺🇸 Ken Paxton For US Senate Rally in San Antonio, Texas [LIVE] | rally_speech | 0 | 53 | 85 | 2 |
| New poll shows James Talarico leading Ken Paxton by 6 percentage… | news_package | 28 | 21 | 90 | 1 |
| Texas voters explain why they're choosing Talarico or Paxton | news_package | 21 | 28 | 83 | 8 |
| Talarico, Hinojosa celebrate historic Texas wins at Whataburger | victory_speech | 34 | 15 | 90 | 1 |
| BREAKING: Dems FLIP Texas as Talarico wins Senate, Abbott loses… | victory_speech | 40 | 8 | 92 | 0 |
| Paxton agrees to debate with Talarico as Texas Senate race… | debate | 18 | 28 | 38 | 1 |
| James Talarico, Ken Paxton rally San Antonio voters as midterms… | news_package | 21 | 24 | 92 | 3 |
| Talarico, Paxton ramp up campaign tours | tour_launch | 27 | 18 | 89 | 6 |
| Ken Paxton concession speech on midterm election loss to James… | concession_speech | 0 | 45 | 4 | 8 |
| James Talarico revs up general election campaign in SA after… | convention_speech | 32 | 12 | 95 | 1 |
| Thousands gather for James Talarico's 'Clear Eyes, Full Hearts'… | tour_stop | 31 | 13 | 93 | 3 |
| LIVE: James Talarico holds campaign rally in San Marcos | rally_speech | 36 | 7 | 90 | 7 |
| New poll shows James Talarico leading Ken Paxton in Texas Senate… | news_package | 21 | 21 | 30 | 0 |
| Ken Paxton needs to debate James Talarico, Texas Republican says | debate | 16 | 26 | 98 | 0 |
| Ken Paxton kicks off statewide bus tour ahead of early voting in… | tour_launch | 31 | 11 | 82 | 4 |
| LIVE: James Talarico holds campaign rally in San Marcos | rally_speech | 35 | 7 | 89 | 9 |
| 2026 midterms: Paxton, Talarico make final push ahead of Election… | final_rally | 17 | 24 | 98 | 1 |
| James Talarico visits San Antonio on 'Clear Eyes, Full Hearts'… | rally | 40 | 1 | 61 | 11 |
| James Talarico CNN town hall comes as Texas Senate race tightens | town_hall | 41 | 0 | 20 | 2 |
| Talarico rallies in Tyler as Paxton tours Texas amid tightening… | news_package | 20 | 19 | 72 | 0 |
| Victory Party LIVE: James Talarico for US Senate | victory_speech | 37 | 2 | 99 | 2 |
| Senate debate between Paxton and Talarico appears increasingly… | debate | 11 | 26 | 102 | 1 |
| LIVE: James Talarico holds campaign rally in San Marcos | rally_speech | 28 | 8 | 95 | 9 |
| Democratic Senate candidate James Talarico makes campaign stop at… | tour_stop | 32 | 3 | 90 | 0 |
| Talarico leads Paxton in Texas Senate race, Marist poll shows | news_package | 14 | 18 | 107 | 1 |
| WATCH LIVE: James Talarico speaks to supporters on election night | victory_speech | 32 | 0 | 108 | 0 |
| Top Pollster Reveals Who Is Winning Between Paxton And Talarico… | news_package | 26 | 4 | 109 | 1 |
| Ablaze - Radical James Talarico is Anti-Texas | rally_speech | 30 | 0 | 10 | 4 |
| New poll shows Talarico, Paxton essentially tied in Texas as… | news_package | 14 | 15 | 102 | 9 |
| Texas voters reveal TOP issues in critical Paxton-Talarico US… | news_package | 14 | 15 | 110 | 1 |
| Paxton for Senate new ad “Hypocrite” | ad | 24 | 5 | 21 | 1 |
| Talarico holds narrow lead over Paxton in Texas Senate race, UH… | news_package | 24 | 2 | 72 | 5 |
| Ken Paxton targets James Talarico in scathing new campaign ad as… | ad | 24 | 1 | 115 | 0 |
| James Talarico Kicks Off "Clear Eyes, Full Hearts" Tour | tour_launch | 23 | 2 | 87 | 2 |
| Can James Talarico convert Republican voters against Ken Paxton… | news_package | 16 | 8 | 107 | 9 |
| James Talarico leading Ken Paxton in Texas, new poll shows | news_package | 11 | 11 | 116 | 2 |
| WATCH: Rep. Talarico STOP ICE Rally | rally_speech | 18 | 3 | 114 | 5 |
| Paxton, Abbott rally North Texas Republicans as Texas Senate race… | rally | 2 | 18 | 28 | 3 |
| Texas Senate candidates Paxton, Talarico bring statewide tours to… | tour_launch | 8 | 11 | 38 | 3 |
| MS NOW shifts Talarico, Paxton Texas Senate race to 'TOSS-UP':… | interview | 12 | 4 | 123 | 1 |
| Ken Paxton holds rally in Selma; James Talarico casts his vote | rally_speech | 0 | 15 | 37 | 5 |
| John Berman breaks down the CNN & Jubilee Town Hall with James… | town_hall | 13 | 1 | 125 | 1 |
| The KEY Moment From James Talarico's CNN Town Hall That Shows Why… | town_hall | 13 | 0 | 127 | 0 |
| Cornyn targets Paxton’s “baggage” in final push before GOP runoff… | final_rally | 1 | 11 | 126 | 2 |
| Gina Hinojosa beats Greg Abbott and James Talarico defeats Ken… | news_package | 10 | 0 | 126 | 4 |
| Paxton supporters react to loss to Talarico in Texas Senate race | news_package | 0 | 9 | 80 | 0 |
| Is Texas Flippable? Here’s What The Latest Paxton-Talarico Poll… | news_package | 4 | 5 | 129 | 2 |
| 'It feels like I'm taking away part of myself:' North Texas… | news_package | 2 | 4 | 134 | 0 |
| How Talarico and Paxton supporters reacted to Texas election… | news_package | 0 | 6 | 134 | 0 |
| Ken Paxton rallies supporters in Tyler as Senate race enters… | rally | 0 | 6 | 131 | 3 |
| James Talarico supporters erupt in celebration at Austin watch… | watch_party | 6 | 0 | 134 | 0 |
| CBS News poll shows a Texas toss-up with Talarico, Paxton in… | news_package | 4 | 1 | 135 | 0 |
| James Talarico releases devastating ad against Ken Paxton | ad | 1 | 3 | 133 | 3 |
| Crowds cheer as AP projects James Talarico wins the U.S. Senate… | news_clip | 0 | 4 | 126 | 6 |
| BREAKING: Gov. Greg Abbott concedes, Talarico wins over Paxton | concession_speech | 0 | 3 | 134 | 3 |
| Paxton And Talarico Neck-And-Neck In Tight Texas Senate Race: New… | news_package | 2 | 1 | 136 | 1 |
| Live with the crowd for Talarico rally at Fiesta Center (5 p.m.) | rally_speech | 0 | 2 | 137 | 1 |
| Ken Paxton or James Talarico? In Texas election, voters on each… | news_package | 0 | 1 | 134 | 5 |
| LIVE: Talarico, Hinojosa rally in Dallas as Texas races tighten | rally_speech | 0 | 1 | 37 | 20 |
| James Talarico for Texas Rally: Clear Eyes, Full Hearts | rally_speech | 0 | 1 | 13 | 4 |
| Paxton vs. Talarico: Political science expert explains what's at… | news_package | 0 | 0 | 140 | 0 |
| ​Texas Attorney General, U.S. Senate candidate Ken Paxton… | rally_speech | 0 | 0 | 2 | 1 |
| Watch - President Trump urges Texas to Vote for Ken Paxton | rally_speech | 0 | 0 | 140 | 0 |
| LIVE: Talarico, Hinojosa rally in Dallas as Texas races tighten | rally_speech | 0 | 0 | 16 | 13 |
| LIVE: James Talarico holds El Paso, Texas rally | rally | 0 | 0 | 5 | 0 |
| LIVE: Talarico, Hinojosa rally in Dallas as Texas races tighten | rally_speech | 0 | 0 | 32 | 15 |
| Talarico’s Town Hall Answer Has Texas Shook | town_hall | 0 | 0 | 139 | 1 |
| James Talarico Delivers Election Night Victory Speech | victory_speech | 0 | 0 | 1 | 1 |

Total: **106,295 crops → 4,767 Talarico / 4,388 Paxton / 8,592 unknown / 335 no face**.

Curated-frame similarity: Talarico median **0.788** (n=87), Paxton median **0.767**
(n=85); the weakest accepted frame is **0.630**.

## 4. Files / 文件

| File | Content |
|---|---|
| `frame_index.csv` | 172 curated frames: identity + similarity, video, event kind, timestamp, face px, shot scale, sharpness, brightness, torso-region RGB, paths |
| `video_sources.csv` | the 145 source videos with channel, upload date, duration, URL |
| `curation_stats.json` | candidate pool size, kept count and per-video kept counts |
| `frames/*.jpg` | full frames (clean + `_annot` with the detected face box and score) |
| `faces/*.jpg` | 256×256 face crops behind each identity call |
| `sheet_talarico_frames.jpg` | 87 Talarico frames, contact sheet |
| `sheet_paxton_frames.jpg` | 85 Paxton frames, contact sheet |
| `sheet_duel.jpg` | top 12 per candidate side by side |
| `sheet_context.jpg` (+ `_2`, `_3`…) | evenly spaced staging frames from every video (no identity claim) |
| `context/` | the individual staging stills — **local only**, Git-excluded like `raw/` |
| `shot_index.csv` | 1073 scenes/keyframes: timing, brightness, contrast, sharpness, colourfulness, face fraction |
| `video_visual_metrics.csv` | 145 videos: cut rate, mean shot length, motion, static ratio, face presence |
| `keyframes/<slug>/` | the keyframe stills (≤720 px, Git-excluded working copies) |
| `sheet_shots_*.jpg` | global keyframe contact sheets |

## 5. First measurable observations / 可先说的量化观察

Stated as measurements, not interpretations:

- **Shot scale**: Talarico 47 medium / 37 medium-close / 1 close-up; Paxton 64 medium /
  17 medium-close / 2 close-up. The curation floor is a face ≥ 80 px on ≤720p sources, so
  close-ups are mechanically rare and the difference is partly an artefact of the rule.
- **Face size at selection**: Talarico 73–310 px, Paxton 11–387 px.
- **Torso-region mean RGB** varies far more between videos than between candidates —
  venue lighting dominates any colour comparison.
- **Format split**: official channels publish very differently — Talarico's tour clip is
  640×360 / 75 s (social-first cut), Paxton's Cypress rally is 720p / 20 min (broadcast feed).

- **Shot structure**: 145 videos carry scene data; median shot length **12.7 s**, median
  cut rate **4.4 cuts/min**. Median cut rate is 3.2 for Talarico-sourced videos and
  3.7 for Paxton-sourced videos — a mix of broadcast packages and single-camera rally
  feeds, so this is a production-format reading, not a campaign-style claim.
- **Exposure**: median frame brightness 74 (Talarico) vs 82 (Paxton) on the 0–255
  scale. Venue lighting and camera gain dominate; no colour or tone claim follows.

- **Audio**: 145 of 145 videos measured (94 speech-type, 37.2 h). Speech share, pause
  structure, F0 and caption-derived rate live in `../11_speech_audio/`; delivery is no
  longer an `unknown`, though pitch on rally audio is indicative only.

## 5.1 The official mark / 官方标志

`assets/talarico_logo.svg` is **`File:James Talarico for Senate logo.svg`** from
Wikimedia Commons, sourced to `jamestalarico.com`. Parsed as vector data:

| Property | Value |
|---|---|
| Canvas | 204 × 52 (ratio ≈ 3.9 : 1, a horizontal wordmark) |
| Paths | 18 (glyph outlines converted to paths; plus one `fill="none"` background) |
| Colours | `black` × 18, `white` × 1, `none` × 1 — **no hex palette, no gradient, no accent colour** |
| Strokes | none |
| Typography | outlined, no live text and no `font-family` declaration |

So the documented mark is a **monochrome black wordmark** with no colour system of its
own: whatever colour the campaign used came from photography and merchandise, not from
the logo file. Two small star-shaped paths sit at the lower corners of the canvas.

**Paxton side: no comparable mark was located.** A Commons namespace search for a Paxton
campaign logo returned nothing usable, and the campaign site served no retrievable
issue/branding pages. This asymmetry must travel with any "brand-system" comparison.

## 6. Reproduction / 复现

```powershell
# first clone only: restore the video + model binaries excluded from Git
python texas-senate-2026/_staging/vision/fetch_models.py        # YuNet + SFace ONNX
python texas-senate-2026/_staging/vision/download_videos.py     # the 145 configured videos

# optional: re-run discovery on YouTube and rebuild the selection
python texas-senate-2026/_staging/vision/discover_videos.py     # ~35 searches
python texas-senate-2026/_staging/vision/select_videos.py       # quotas + budget
python texas-senate-2026/_staging/vision/download_all.py        # video + captions
python texas-senate-2026/_staging/vision/normalize_config.py    # candidate/kind fixes

python texas-senate-2026/_staging/vision/extract_faces.py       # sampling + detection
python texas-senate-2026/_staging/vision/recognize_faces.py     # SFace identity pass
python texas-senate-2026/_staging/vision/curate.py              # de-duplicated curated set
python texas-senate-2026/_staging/vision/extract_keyframes.py   # scene cuts + keyframes
python texas-senate-2026/_staging/vision/gen_readme.py          # regenerate this file

python texas-senate-2026/_staging/vision/analyze_speech.py      # audio + delivery
python texas-senate-2026/_staging/vision/gen_audio_readme.py    # 11_speech_audio/README
```

## 7. Limits — read before using / 使用前必读

1. **All 145 configured videos are present.**
2. **Audio is analysed separately, not here.** `../11_speech_audio/` measures speech share,
   pauses, F0 and caption-based rate. It does not support claims about emotion, sincerity
   or "tone"; rally audio is a mix and pitch there is indicative only.
3. **172 frames from 145 videos is still a small sample.** It cannot support frequency
   claims about either campaign's imagery.
4. **Mixed production contexts.** Official feeds and local-TV packages differ in camera
   position, lighting and graphics; comparing across them confounds source with candidate.
5. **The torso RGB column is a crude region mean**, often capturing background. It is not
   a garment-colour reading.
6. **No facial geometry measurement was performed** beyond the face bounding box. The
   interocular/face-width protocol in the two visual analyses is still unexecuted.
7. **Rights**: these frames are cut from YouTube videos owned by the campaigns and TV
   stations. They are stored for **internal analysis only** and are **not licensed for
   republication**. Any public use requires a licensed still or link-only treatment.
