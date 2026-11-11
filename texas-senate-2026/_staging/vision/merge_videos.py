import json
import subprocess
from pathlib import Path

VISION = Path("texas-senate-2026/_staging/vision")
RAW = VISION / "raw"
cfg = json.loads((VISION / "videos.json").read_text(encoding="utf-8"))
have = {v["slug"] for v in cfg}

NEW = [
    dict(slug="TAL_plano_cbs", video_id="vW1QJCc0_Hw", candidate_source="TALARICO", kind="rally",
         title="James Talarico holds Plano rally ahead of Texas senate election",
         channel="CBS TEXAS", upload_date="2026-10-19", file="TAL_plano_cbs_vW1QJCc0_Hw.mp4"),
    dict(slug="TAL_sanantonio_kens", video_id="PWow10eQp-o", candidate_source="TALARICO", kind="rally",
         title="James Talarico visits San Antonio on 'Clear Eyes, Full Hearts' campaign tour",
         channel="KENS 5", upload_date="2026-10-25", file="TAL_sanantonio_kens_PWow10eQp-o.mp4"),
    dict(slug="TAL_rally_angie", video_id="0nXJYOIZ4Fk", candidate_source="TALARICO", kind="rally_speech",
         title="James Talarico for Texas Rally: Clear Eyes, Full Hearts",
         channel="Angie A (third-party upload)", upload_date="2026-10-30", file="TAL_rally_angie_0nXJYOIZ4Fk.mp4"),
    dict(slug="TAL_watchparty_cbs", video_id="qbQzb0sz2OI", candidate_source="TALARICO", kind="watch_party",
         title="James Talarico supporters erupt in celebration at Austin watch party",
         channel="CBS TEXAS", upload_date="2026-11-04", file="TAL_watchparty_cbs_qbQzb0sz2OI.mp4"),
    dict(slug="TAL_projection_kxan", video_id="63Eb4VlhxSE", candidate_source="TALARICO", kind="news_clip",
         title="Crowds cheer as AP projects James Talarico wins the U.S. Senate race in Texas",
         channel="KXAN", upload_date="2026-11-04", file="TAL_projection_kxan_63Eb4VlhxSE.mp4"),
    dict(slug="PAX_allen_cbs", video_id="7oqcGDWT4Os", candidate_source="PAXTON", kind="final_rally",
         title="Ken Paxton holds final campaign rally in Allen ahead of midterm elections",
         channel="CBS TEXAS", upload_date="2026-11-03", file="PAX_allen_cbs_7oqcGDWT4Os.mp4"),
    dict(slug="PAX_abbott_cbs", video_id="YE4pIbpZhAE", candidate_source="PAXTON", kind="rally",
         title="Paxton, Abbott rally North Texas Republicans as Texas Senate race heats up",
         channel="CBS TEXAS", upload_date="2026-07-28", file="PAX_abbott_cbs_YE4pIbpZhAE.mp4"),
    dict(slug="PAX_concession_nbc", video_id="O7TIsfy4PEQ", candidate_source="PAXTON", kind="concession_speech",
         title="Full speech: Ken Paxton concedes U.S. Senate race to James Talarico",
         channel="NBC DFW", upload_date="2026-11-04", file="PAX_concession_nbc_O7TIsfy4PEQ.mp4"),
    dict(slug="PAX_concession_usa", video_id="7c8BeNjXyks", candidate_source="PAXTON", kind="concession_speech",
         title="Ken Paxton concession speech on midterm election loss to James Talarico",
         channel="USA TODAY", upload_date="2026-11-04", file="PAX_concession_usa_7c8BeNjXyks.mp4"),
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
        print("added", v["slug"], v["duration"], "s")

(VISION / "videos.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("total configured:", len(cfg), "| downloaded:", sum(1 for v in cfg if (RAW / v["file"]).exists()))
