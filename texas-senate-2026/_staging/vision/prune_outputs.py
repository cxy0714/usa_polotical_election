import csv
from pathlib import Path

import pandas as pd

VISION = Path("texas-senate-2026/_staging/vision")
OUT = VISION / "out"
man = pd.read_csv(OUT / "manifest.csv")
ids = set(man["frame_id"])
idf = pd.read_csv(OUT / "identity.csv")
keep = idf[idf["frame_id"].isin(ids)]
dropped = len(idf) - len(keep)
keep.to_csv(OUT / "identity.csv", index=False)
print(f"identity rows: {len(idf)} -> {len(keep)} (dropped {dropped} stale)")

removed = 0
for slug_dir in OUT.iterdir():
    faces = slug_dir / "faces"
    if not faces.is_dir():
        continue
    for f in faces.glob("*.jpg"):
        if f.stem not in ids:
            f.unlink()
            removed += 1
print("removed stale crops:", removed)

print(keep.groupby(["slug", "label"]).size().unstack(fill_value=0).to_string())
