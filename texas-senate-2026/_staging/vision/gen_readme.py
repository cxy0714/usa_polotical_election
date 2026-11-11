"""Regenerate 10_video_frames/README.md from the pipeline outputs.

Bilingual (EN + ZH) documentation for the video frame set. Run after curate.py:
    python texas-senate-2026/_staging/vision/gen_readme.py
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VISION = ROOT / "_staging" / "vision"
DEST = ROOT / "10_video_frames"
RAW = VISION / "raw"


def rows(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def clean_title(s, width=66):
    s = s.replace("|", "/")
    if len(s) <= width:
        return s
    return s[:width].rsplit(" ", 1)[0] + "…"


def main():
    cfg = json.loads((VISION / "videos.json").read_text(encoding="utf-8"))
    vsrc = rows(DEST / "video_sources.csv")
    frames = rows(DEST / "frame_index.csv")
    ident = rows(VISION / "out" / "identity.csv")
    manifest = rows(VISION / "out" / "manifest.csv")
    stats = json.loads((DEST / "curation_stats.json").read_text(encoding="utf-8"))
    meta = {v["slug"]: v for v in cfg}

    missing = [v for v in cfg if not (RAW / v["file"]).exists()]
    n_crops = len(manifest)
    counts = Counter(r["label"] for r in ident)
    tal, pax = counts["TALARICO"], counts["PAXTON"]
    unk, nof = counts["unknown"], counts["noface"]

    per_slug = defaultdict(Counter)
    for r in ident:
        per_slug[r["slug"]][r["label"]] += 1

    n_tal = sum(1 for r in frames if r["identity"] == "TALARICO")
    n_pax = sum(1 for r in frames if r["identity"] == "PAXTON")
    n_frames = len(frames)

    def sub(cand):
        sel = [r for r in frames if r["identity"] == cand]
        sc = Counter(r["shot_scale"] for r in sel)
        sims = sorted(float(r["identity_sim"]) for r in sel)
        fw = [int(r["face_w_px"]) for r in sel]
        return sc, sims, fw

    sc_t, sims_t, fw_t = sub("TALARICO")
    sc_p, sims_p, fw_p = sub("PAXTON")

    official = [v for v in vsrc if "official campaign" in v["channel"].lower()]
    news = [v for v in vsrc if v not in official]

    L = []
    A = L.append
    A("# 10_video_frames — 视频帧与人脸识别集")
    A("")
    A("**English** — Frames cut from %d publicly available videos, with every face detected" % len(vsrc))
    A("and matched against the licensed candidate photographs already in `04_visual_archive/`.")
    A("This closes the largest documentary gap in the archive — framing, staging and venue")
    A("were `unknown` — without inventing anything: the files below are real frames, the")
    A("identity call is a scored nearest-neighbour match, and the limits are listed in §7.")
    A("")
    A("**中文** — 本目录是从 %d 段公开视频中截取的帧，画面中的人脸全部经过检测，并与" % len(vsrc))
    A("`04_visual_archive/` 中已有的候选人有授权照片做匹配。它填补了档案中最大的文献缺口")
    A("（此前\"取景／舞台／场地\"均为 `unknown`），且不虚构任何内容：下面是真实帧，身份判定是")
    A("带分数的最邻近匹配，局限见第 7 节。")
    A("")
    A("---")
    A("")
    A("## 1. Source videos / 来源视频")
    A("")
    A("%d videos downloaded 2026-11-10/11, published between %s and %s. %d are official"
      % (len(vsrc), min(v["upload_date"] for v in vsrc), max(v["upload_date"] for v in vsrc), len(official)))
    A("campaign channels; the rest are network/station news packages or wire-service feeds.")
    if missing:
        A("A further %d configured videos could not be downloaded (§7.1)." % len(missing))
    A("")
    A("**Official campaign channels / 官方竞选频道**")
    A("")
    A("| Video ID | Channel | Upload | Kind | Title |")
    A("|---|---|---|---|---|")
    for v in official:
        A("| `%s` | %s | %s | %s | %s |" % (v["video_id"], v["channel"], v["upload_date"], v["event_kind"], v["title"]))
    A("")
    A("**News / wire packages / 新闻与通讯社**")
    A("")
    A("| Video ID | Channel | Upload | Kind | Title |")
    A("|---|---|---|---|---|")
    for v in news:
        A("| `%s` | %s | %s | %s | %s |" % (v["video_id"], v["channel"], v["upload_date"], v["event_kind"], v["title"]))
    A("")
    A("URLs are in `video_sources.csv`.")
    A("")
    A("## 2. Method / 方法")
    A("")
    A("1. **Sampling** — every 0.5 s for videos ≤ 120 s, every 1.0 s above that")
    A("   (**%s** face crops kept in total)." % f"{n_crops:,}")
    A("2. **Detection** — OpenCV YuNet (ONNX, 232 KB), score ≥ 0.55, face side ≥ 64 px,")
    A("   up to 3 faces per sampled frame.")
    A("3. **Identity** — OpenCV SFace (ONNX, 38.7 MB). Embeddings are L2-normalised and")
    A("   compared by cosine against **62 reference embeddings** built from the archive's own")
    A("   licensed candidate photographs (`04_visual_archive/talarico/campaign/` 7 files,")
    A("   `04_visual_archive/paxton/campaign/` 69 files; 62 usable).")
    A("4. **Decision rule** — class-balanced best-per-class cosine; a label is assigned only if")
    A("   `best ≥ 0.40` **and** `best − second-best ≥ 0.05`, otherwise `unknown`.")
    A("5. **Reference sanity check** — same-class mean cosine **0.499**, cross-class mean")
    A("   **0.123**. The two reference pools are cleanly separated.")
    A("6. **De-duplication** — each surviving candidate frame gets a 64-bit DCT perceptual hash")
    A("   and a torso-region colour signature. Within a video, a frame is dropped when the hash")
    A("   is within %d bits of an accepted frame (near-identical framing) or when the torso colour"
      % 12)
    A("   matches within 12 RGB units and the hash within 20 bits. Across videos only a")
    A("   near-identical image (≤ 6 bits) counts as a duplicate, so different venues survive.")
    A("   At most 3 frames per video per outfit-colour bucket are kept.")
    A("7. **Selection floor** — `identity_sim ≥ 0.62`, `sharpness ≥ 40`, `face width ≥ 80 px`;")
    A("   max 8 per video, 2.5 s minimum spacing. Result: **%d candidates → %d kept frames"
      % (stats["candidates"], stats["kept"]))
    A("   (%d Talarico / %d Paxton); %d redundant frames removed**."
      % (stats["kept_tal"], stats["kept_pax"], stats["removed"]))
    A("8. **Measurements** — shot scale from face-width / frame-width ratio; face box in source")
    A("   pixels; Laplacian sharpness; mean grey brightness; mean RGB of the region below the")
    A("   face (a crude torso proxy, **not** a clothing classification).")
    A("")
    A("Scripts: `../_staging/vision/{extract_faces,recognize_faces,curate}.py`;")
    A("config: `../_staging/vision/videos.json`; models cached in `../_staging/vision/models/`.")
    A("")
    A("## 3. What the identity pass found / 身份识别结果")
    A("")
    A("| Source video | Kind | Talarico | Paxton | unknown | no face |")
    A("|---|---|---|---|---|---|")
    order = sorted(per_slug.items(), key=lambda kv: (-(kv[1]["TALARICO"] + kv[1]["PAXTON"]), kv[0]))
    for slug, c in order:
        m = meta.get(slug, {})
        A("| %s | %s | %d | %d | %d | %d |" % (
            clean_title(m.get("title", slug)), m.get("kind", ""), c["TALARICO"], c["PAXTON"], c["unknown"], c["noface"]))
    A("")
    A("Total: **%s crops → %s Talarico / %s Paxton / %s unknown / %s no face**."
      % (f"{n_crops:,}", f"{tal:,}", f"{pax:,}", f"{unk:,}", f"{nof:,}"))
    A("")
    A("Curated-frame similarity: Talarico median **%.3f** (n=%d), Paxton median **%.3f**"
      % (sims_t[len(sims_t) // 2] if sims_t else 0, n_tal,
         sims_p[len(sims_p) // 2] if sims_p else 0))
    A("(n=%d); the weakest accepted frame is **%.3f**."
      % (n_pax, min(sims_t + sims_p) if (sims_t + sims_p) else 0))
    A("")
    A("## 4. Files / 文件")
    A("")
    A("| File | Content |")
    A("|---|---|")
    A("| `frame_index.csv` | %d curated frames: identity + similarity, video, event kind, timestamp, face px, shot scale, sharpness, brightness, torso-region RGB, paths |" % n_frames)
    A("| `video_sources.csv` | the %d source videos with channel, upload date, duration, URL |" % len(vsrc))
    A("| `curation_stats.json` | candidate pool size, kept count and per-video kept counts |")
    A("| `frames/*.jpg` | full frames (clean + `_annot` with the detected face box and score) |")
    A("| `faces/*.jpg` | 256×256 face crops behind each identity call |")
    A("| `sheet_talarico_frames.jpg` | %d Talarico frames, contact sheet |" % n_tal)
    A("| `sheet_paxton_frames.jpg` | %d Paxton frames, contact sheet |" % n_pax)
    A("| `sheet_duel.jpg` | top 12 per candidate side by side |")
    A("| `sheet_context.jpg` | evenly spaced staging frames from every video (no identity claim) |")
    A("")
    A("## 5. First measurable observations / 可先说的量化观察")
    A("")
    A("Stated as measurements, not interpretations:")
    A("")
    A("- **Shot scale**: Talarico %d medium / %d medium-close / %d close-up; Paxton %d medium /"
      % (sc_t["medium"], sc_t["medium-close"], sc_t["close-up"], sc_p["medium"]))
    A("  %d medium-close / %d close-up. The curation floor is a face ≥ 80 px on ≤720p sources, so"
      % (sc_p["medium-close"], sc_p["close-up"]))
    A("  close-ups are mechanically rare and the difference is partly an artefact of the rule.")
    if fw_t:
        A("- **Face size at selection**: Talarico %d–%d px, Paxton %d–%d px."
          % (min(fw_t), max(fw_t), min(fw_p), max(fw_p)))
    A("- **Torso-region mean RGB** varies far more between videos than between candidates —")
    A("  venue lighting dominates any colour comparison.")
    A("- **Format split**: official channels publish very differently — Talarico's tour clip is")
    A("  640×360 / 75 s (social-first cut), Paxton's Cypress rally is 720p / 20 min (broadcast feed).")
    A("")
    A("## 5.1 The official mark / 官方标志")
    A("")
    A("`assets/talarico_logo.svg` is **`File:James Talarico for Senate logo.svg`** from")
    A("Wikimedia Commons, sourced to `jamestalarico.com`. Parsed as vector data:")
    A("")
    A("| Property | Value |")
    A("|---|---|")
    A("| Canvas | 204 × 52 (ratio ≈ 3.9 : 1, a horizontal wordmark) |")
    A("| Paths | 18 (glyph outlines converted to paths; plus one `fill=\"none\"` background) |")
    A("| Colours | `black` × 18, `white` × 1, `none` × 1 — **no hex palette, no gradient, no accent colour** |")
    A("| Strokes | none |")
    A("| Typography | outlined, no live text and no `font-family` declaration |")
    A("")
    A("So the documented mark is a **monochrome black wordmark** with no colour system of its")
    A("own: whatever colour the campaign used came from photography and merchandise, not from")
    A("the logo file. Two small star-shaped paths sit at the lower corners of the canvas.")
    A("")
    A("**Paxton side: no comparable mark was located.** A Commons namespace search for a Paxton")
    A("campaign logo returned nothing usable, and the campaign site served no retrievable")
    A("issue/branding pages. This asymmetry must travel with any \"brand-system\" comparison.")
    A("")
    A("## 6. Reproduction / 复现")
    A("")
    A("```powershell")
    A("# first clone only: restore the video + model binaries excluded from Git (~530 MB)")
    A("python texas-senate-2026/_staging/vision/fetch_models.py        # YuNet + SFace ONNX")
    A("python texas-senate-2026/_staging/vision/download_videos.py     # 26 source videos")
    A("")
    A("python texas-senate-2026/_staging/vision/extract_faces.py     # sampling + detection")
    A("python texas-senate-2026/_staging/vision/recognize_faces.py   # SFace identity pass")
    A("python texas-senate-2026/_staging/vision/curate.py            # de-duplicated curated set")
    A("python texas-senate-2026/_staging/vision/gen_readme.py        # regenerate this file")
    A("```")
    A("")
    A("## 7. Limits — read before using / 使用前必读")
    A("")
    if missing:
        A("1. **%d configured videos could not be downloaded**: %s. They stalled at 0 bytes or"
          % (len(missing), ", ".join("`%s`" % v["video_id"] for v in missing)))
        A("   at ~5 KB/s during section downloads and were dropped rather than left half-processed.")
        A("   They remain registered in `videos.json`, so a retry is one command away.")
    else:
        A("1. **All %d configured videos are present.**" % len(cfg))
    A("2. **No audio was analysed.** Nothing here says anything about delivery, tone or pacing;")
    A("   all prosody fields in the main archive remain `unknown`.")
    A("3. **%d frames from %d videos is still a small sample.** It cannot support frequency"
      % (n_frames, len(vsrc)))
    A("   claims about either campaign's imagery.")
    A("4. **Mixed production contexts.** Official feeds and local-TV packages differ in camera")
    A("   position, lighting and graphics; comparing across them confounds source with candidate.")
    A("5. **The torso RGB column is a crude region mean**, often capturing background. It is not")
    A("   a garment-colour reading.")
    A("6. **No facial geometry measurement was performed** beyond the face bounding box. The")
    A("   interocular/face-width protocol in the two visual analyses is still unexecuted.")
    A("7. **Rights**: these frames are cut from YouTube videos owned by the campaigns and TV")
    A("   stations. They are stored for **internal analysis only** and are **not licensed for")
    A("   republication**. Any public use requires a licensed still or link-only treatment.")
    A("")

    (DEST / "README.md").write_text("\n".join(L), encoding="utf-8")
    print("wrote README:", n_frames, "frames,", len(vsrc), "videos,", len(missing), "missing")


if __name__ == "__main__":
    main()
