from pathlib import Path

p = Path("texas-senate-2026/10_video_frames/README.md")
t = p.read_text(encoding="utf-8")
repl = [
    ("Frames cut from eleven publicly available videos", "Frames cut from ten publicly available videos"),
    ("本目录是从十一段公开视频中截取的帧", "本目录是从十段公开视频中截取的帧"),
    ("Eleven videos, downloaded 2026-11-10", "Ten videos, downloaded 2026-11-10"),
    ("(The eleventh row in `video_sources.csv` is the KVUE package; URLs are in that file.)",
     "(URLs are in `video_sources.csv`.)"),
    ("Two further videos are configured but not yet downloaded",
     "Three further videos are configured but not yet downloaded"),
    ("1. **Two configured videos are not yet downloaded**: `N6PubEh2jZg` (Lubbock full rally\n   speech, 27 min) and `DrD_wR6gEU4` (Paxton speech at the Republican Midterm\n   Convention).",
     "1. **Three configured videos are not yet downloaded**: `N6PubEh2jZg` (Lubbock full\n   rally speech), `sa1vT9B4Ick` (El Paso rally) and `DrD_wR6gEU4` (Paxton speech at the\n   Republican Midterm Convention)."),
]
for a, b in repl:
    if a not in t:
        print("NOT FOUND:", a[:70])
    t = t.replace(a, b)
p.write_text(t, encoding="utf-8")

r = Path("README.md")
s = r.read_text(encoding="utf-8")
s = s.replace("11 source videos, 4,947 face detections", "10 source videos, 4,947 face detections")
r.write_text(s, encoding="utf-8")

m = Path("texas-senate-2026/README.md")
s = m.read_text(encoding="utf-8")
s = s.replace("4,947 face crops from 11 videos", "4,947 face crops from 10 videos")
m.write_text(s, encoding="utf-8")
print("done")
