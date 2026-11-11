# American Political Image Lab — Case Study 001

**2026 Texas U.S. Senate general election: James Talarico (D) vs. Ken Paxton (R)**
Research period March 2026 – November 2026. Bilingual (English + 中文) primary-source archive.

## What this repository is / 这是什么

A reconstruction of *the publicly documented campaign process* — every documented event, speech,
image, advertisement, finance filing and press item of both candidates, each line traceable to a
numbered source. It is research material for a human-led analytical blog and documentary-style
video; it does **not** rank the two campaigns and contains no blog or video script.

对两位候选人全部有据可查的竞选过程的档案：事件、演讲、影像、广告、财务申报与媒体报道，每一行都可溯源到编号来源。它是人工分析写作的素材，**不评判两场竞选孰优孰劣**，也不包含博客或视频脚本。

## Start here / 从这里开始

| | |
|---|---|
| **Full documentation** | [`texas-senate-2026/README.md`](texas-senate-2026/README.md) — directory map, data contract, honest limits |
| **Read it as a website** | open `texas-senate-2026/site/index.html` (offline, no server, 70 pages, EN/ZH side-by-side, clickable sources) |
| **Video frames** | [`texas-senate-2026/10_video_frames/`](texas-senate-2026/10_video_frames/README.md) — 26 source videos, 6,939 face detections, 67 face-matched frames |
| **Know the gaps first** | [`texas-senate-2026/research_gaps.md`](texas-senate-2026/research_gaps.md) |
| **Rebuild the site** | `python texas-senate-2026/_staging/_lead_build_site.py` |

## Continue on another machine / 换一台电脑继续

The repository is self-contained for **reading and analysis**: all datasets, the offline
bilingual site, the 67 curated video frames and their per-frame measurements are committed.
Only two bulky binary sets are excluded, and both restore with one command:

```bash
git clone git@github.com:cxy0714/usa_polotical_election.git
cd usa_polotical_election

# 1) Optional: restore the model weights (~47 MB) and source video (~490 MB)
python texas-senate-2026/_staging/vision/fetch_models.py     # YuNet + SFace ONNX
python texas-senate-2026/_staging/vision/download_videos.py  # 26 videos (needs yt-dlp + ffmpeg)

# 2) Read the archive — no setup needed
#    open texas-senate-2026/site/index.html

# 3) Re-run any stage of the video pipeline
python texas-senate-2026/_staging/vision/extract_faces.py
python texas-senate-2026/_staging/vision/recognize_faces.py
python texas-senate-2026/_staging/vision/curate.py
python texas-senate-2026/_staging/vision/gen_readme.py
python texas-senate-2026/_staging/_lead_build_site.py

# 4) Run the dataset validator
python texas-senate-2026/_staging/_lead_validate.py
```

Python side needs `opencv-python`, `numpy`, `pandas`, `yt-dlp`, plus `ffmpeg` on `PATH`.
Frames are cut from campaign/news videos and are **internal research only** — see the
rights note in [`texas-senate-2026/10_video_frames/README.md`](texas-senate-2026/10_video_frames/README.md).

### View a remote build over Tailscale / 通过 Tailscale 查看另一台机器生成的站点

The site is static, so the only requirement is a web root that also contains the folders
the pages link into (`10_video_frames/`, `04_visual_archive/`, `09_sources/`). Serving
`site/` alone gives 404s on every image — serve `texas-senate-2026/` and open
`/site/index.html`.

**On the machine that builds** (recommended — no firewall rule, HTTPS certificate included):

```bash
python texas-senate-2026/_staging/serve_site.py     # binds 127.0.0.1:8000, no-store cache
tailscale serve --bg 8000                           # exposes it on the tailnet over HTTPS
```

Then on this laptop open `https://<remote-machine>.<tailnet>.ts.net/site/index.html`.
The helper answers `/` with a redirect to `/site/index.html`, sends `Cache-Control:
no-store` so a fresh rebuild is visible without a hard refresh, and refuses to serve
`_staging/` (raw video, model weights, per-crop cache).

Direct-IP alternative (no `tailscale serve`): bind the tailnet address and open the port
on the firewall —

```powershell
python texas-senate-2026/_staging/serve_site.py --bind 100.x.y.z    # this node's Tailscale IP
New-NetFirewallRule -DisplayName "dsl-site-8000" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

then `http://100.x.y.z:8000/site/index.html`.

**Keep one builder.** The generated `site/*.html` files are committed, so if both machines
rebuild and push you get conflicts on generated HTML. Either the remote machine runs the
pipeline + build and the laptop only `git pull`s, or run `git pull --rebase` immediately
before any build.

## Three cautionary notes / 三条必读前提

1. **No debate took place.** Five records reconstruct the invitations and refusals; the CNN–Jubilee
   event was a solo town hall that several outlets mislabelled as a debate.
   没有辩论。CNN–Jubilee 那场是单人问答，被多家媒体误标为辩论。
2. **Appearance is still unmeasured, but the imagery is now readable.** 67 de-duplicated
   frames from 26 videos document framing, staging and venue; facial geometry, body
   proportions and clothing remain `unknown`, with a reproducible measurement protocol
   waiting for a human to execute.
   外貌仍未测量，但画面已可读：26 段视频、67 帧记录取景与舞台；面部几何、身体比例与着装仍为未测。
3. **Money measures cannot be summed.** FEC Schedule E and AdImpact differ by ~10×, and four
   different Talarico "totals" exist. See the bilingual data dictionary §6.
   资金口径不可相加，详见双语数据字典第 6 节。

## Data conventions / 数据约定

- 12 CSV datasets stay English for machine-readability: field names, identifier schemes and
  controlled vocabularies are frozen; Chinese glosses live in
  [`09_sources/data_dictionary_bilingual.md`](texas-senate-2026/09_sources/data_dictionary_bilingual.md).
- All 45 Markdown documents are EN+ZH; English always governs where the two renderings diverge,
  and every quotation keeps its verbatim English original next to the `（译：…）` rendering.
- `unknown` is a value, not a placeholder: it means "not established", never "probably X".

## Licensing / 授权

Photographs stored under `04_visual_archive/` are licensed copies (CC BY / CC BY-SA / CC0 /
public domain) with photographer, date and licence recorded per image. Rights-reserved photographs
are **link-only** records — no unlicensed copy is reproduced. Text and datasets are research
material; cite the `SRC-####` ids in `09_sources/sources.csv`.
