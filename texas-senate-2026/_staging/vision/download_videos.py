"""Re-download every source video that is missing from _staging/vision/raw/.

The Git repository deliberately excludes the ~490 MB of source video (and the ONNX
model weights); this script restores them on a fresh clone.

    python texas-senate-2026/_staging/vision/download_videos.py
    python texas-senate-2026/_staging/vision/fetch_models.py      # detector + recogniser

Requires: yt-dlp (`python -m pip install yt-dlp`), ffmpeg on PATH.
"""
import json
import subprocess
import sys
from pathlib import Path

VISION = Path(__file__).resolve().parent
RAW = VISION / "raw"


def main(only=None):
    cfg = json.loads((VISION / "videos.json").read_text(encoding="utf-8"))
    RAW.mkdir(parents=True, exist_ok=True)
    missing = [v for v in cfg if not (RAW / v["file"]).exists()]
    if only:
        missing = [v for v in missing if v["slug"] in only]
    if not missing:
        print("all configured videos present")
        return 0
    print(f"{len(missing)} missing videos; downloading")
    failed = []
    for v in missing:
        cmd = ["python", "-m", "yt_dlp", "--no-warnings",
               "-f", "bv*+ba/b", "--merge-output-format", "mp4",
               "-o", str(RAW / f"{v['slug']}_%(id)s.%(ext)s"),
               f"https://www.youtube.com/watch?v={v['video_id']}"]
        print("->", v["slug"], v["video_id"], flush=True)
        r = subprocess.run(cmd)
        if r.returncode != 0 or not (RAW / v["file"]).exists():
            failed.append(v["slug"])
            print("   FAILED", v["slug"])
    print("done. failed:", failed or "none")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or None))
