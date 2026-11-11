from pathlib import Path

r = Path("README.md")
s = r.read_text(encoding="utf-8")
s = s.replace("10 source videos, 4,947 face detections, 47 face-matched frames",
              "26 source videos, 6,939 face detections, 67 face-matched frames")
r.write_text(s, encoding="utf-8")

m = Path("texas-senate-2026/README.md")
s = m.read_text(encoding="utf-8")
s = s.replace("`10_video_frames/{frame_index,video_sources}.csv`, 4,947 face crops from 10 videos | **47** curated frames",
              "`10_video_frames/{frame_index,video_sources}.csv`, 6,939 face crops from 26 videos | **67** curated frames")
m.write_text(s, encoding="utf-8")
print("ok", "6,939" in r.read_text(encoding="utf-8"), "6,939" in m.read_text(encoding="utf-8"))
