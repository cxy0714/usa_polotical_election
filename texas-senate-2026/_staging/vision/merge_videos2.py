import json
import subprocess
from pathlib import Path

VISION = Path("texas-senate-2026/_staging/vision")
RAW = VISION / "raw"
cfg = json.loads((VISION / "videos.json").read_text(encoding="utf-8"))
have = {v["slug"] for v in cfg}

NEW = [
    dict(slug="TAL_tyler_cbs", video_id="Ln7A66zGNYo", candidate_source="TALARICO", kind="rally",
         title="Talarico rallies supporters in Tyler as Texas Senate race tightens",
         channel="CBS19", upload_date="2026-10-21", file="TAL_tyler_cbs_Ln7A66zGNYo.mp4"),
    dict(slug="BOTH_tyler_cbs", video_id="ufXizbHdU9c", candidate_source="BOTH", kind="news_package",
         title="Talarico rallies in Tyler as Paxton tours Texas amid tightening Senate race",
         channel="CBS19", upload_date="2026-10-20", file="BOTH_tyler_cbs_ufXizbHdU9c.mp4"),
    dict(slug="TAL_waco_kxxv", video_id="M8x0ZGVlBhI", candidate_source="TALARICO", kind="tour_stop",
         title="Democratic Senate candidate James Talarico makes campaign stop at Baylor University",
         channel="25 News KXXV", upload_date="2026-09-17", file="TAL_waco_kxxv_M8x0ZGVlBhI.mp4"),
    dict(slug="TAL_win_gma", video_id="aU8yJGKC3DE", candidate_source="TALARICO", kind="news_clip",
         title="James Talarico wins Texas Senate race",
         channel="Good Morning America", upload_date="2026-11-04", file="TAL_win_gma_aU8yJGKC3DE.mp4"),
    dict(slug="PAX_tyler_ketk", video_id="O6HogoPDp4Y", candidate_source="PAXTON", kind="rally_speech",
         title="Ken Paxton speaks at tense United States Senate campaign rally in Tyler",
         channel="KETK NBC", upload_date="2026-11-01", file="PAX_tyler_ketk_O6HogoPDp4Y.mp4"),
    dict(slug="PAX_tyler_cbs", video_id="dOg1d2XSBoQ", candidate_source="PAXTON", kind="rally",
         title="Ken Paxton rallies supporters in Tyler as Senate race enters final stretch",
         channel="CBS19", upload_date="2026-11-02", file="PAX_tyler_cbs_dOg1d2XSBoQ.mp4"),
    dict(slug="PAX_convention_fox4", video_id="8B6h7IWjCok", candidate_source="PAXTON", kind="convention_speech",
         title="FULL: Ken Paxton's 2026 RNC Midterm Convention Speech",
         channel="FOX 4 Dallas-Fort Worth", upload_date="2026-09-09", file="PAX_convention_fox4_8B6h7IWjCok.mp4"),
]

for v in NEW:
    if not (RAW / v["file"]).exists():
        print("SKIP missing file:", v["file"])
        continue
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", str(RAW / v["file"])],
                         capture_output=True, text=True).stdout.strip()
    v["duration"] = round(float(dur))
    if v["slug"] not in have:
        cfg.append(v)
        have.add(v["slug"])
        print("added", v["slug"], v["duration"], "s")

(VISION / "videos.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("total configured:", len(cfg), "| downloaded:", sum(1 for v in cfg if (RAW / v["file"]).exists()))
