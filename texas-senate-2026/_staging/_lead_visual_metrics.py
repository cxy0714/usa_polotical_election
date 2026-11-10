"""Lead: compute real, documented image measurements for downloaded archive
copies (PIL + numpy only; no face-landmark library is available in this
toolchain). Writes metrics to _staging/_visual_metrics.csv and patches
image_archive.csv quality fields with the measured values.
"""
import csv
import json
import os
import re

import numpy as np
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ARCH = os.path.join(ROOT, "04_visual_archive")
CSV = os.path.join(ARCH, "image_archive.csv")
OUT = os.path.join(ROOT, "_staging", "_visual_metrics.csv")
HEADER = ["image_id", "candidate_id", "local_filename", "measured_width",
          "measured_height", "orig_resolution", "orig_megapixels",
          "aspect_ratio", "orientation", "mean_luma", "luma_std",
          "laplacian_var", "mean_saturation", "resolution_class"]


def laplacian_var(gray):
    k = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
    h, w = gray.shape
    if h < 3 or w < 3:
        return 0.0
    # simple valid convolution via strided slices
    c = gray[1:-1, 1:-1]
    up, dn, lf, rt = gray[:-2, 1:-1], gray[2:, 1:-1], gray[1:-1, :-2], gray[1:-1, 2:]
    lap = up + dn + lf + rt - 4.0 * c
    return float(lap.var())


def quality_class(orig_mp):
    """Resolution class of the ORIGINAL archival file (not the 800px derivative
    measured here). Reported separately from sharpness, which was measured on
    the derivative and is only comparable within the same derivative size."""
    if orig_mp >= 8:
        return "high"
    if orig_mp >= 2:
        return "medium"
    return "low"


def main():
    with open(CSV, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    metrics = []
    by_id = {r["image_id"]: r for r in rows}
    for r in rows:
        lf = r.get("local_filename", "")
        if lf in ("", "unknown"):
            continue
        p = os.path.join(ARCH, lf.replace("/", os.sep))
        if not os.path.exists(p):
            continue
        try:
            im = Image.open(p).convert("RGB")
        except Exception:
            continue
        arr = np.asarray(im, dtype=np.float32)
        gray = arr.mean(axis=2)
        h, w = gray.shape
        mp = round((w * h) / 1_000_000, 2)
        sharp = round(laplacian_var(gray), 1)
        # saturation proxy: mean(max-min per pixel) normalised 0-255
        sat = float(np.mean(arr.max(axis=2) - arr.min(axis=2))) / 255.0
        aspect = round(w / h, 3) if h else 0.0
        orig = (r.get("image_resolution") or "").strip()
        orig_mp = 0.0
        m2 = orig.lower().replace(" ", "").split("x")
        try:
            if len(m2) == 2 and m2[0].isdigit() and m2[1].isdigit():
                orig_mp = round((int(m2[0]) * int(m2[1])) / 1_000_000, 2)
        except Exception:
            orig_mp = 0.0
        qc = quality_class(orig_mp) if orig_mp else "unknown"
        m = {
            "image_id": r["image_id"], "candidate_id": r["candidate_id"],
            "local_filename": lf, "measured_width": w, "measured_height": h,
            "orig_resolution": orig or "unknown", "orig_megapixels": orig_mp,
            "aspect_ratio": aspect,
            "orientation": "landscape" if w > h else ("portrait" if h > w else "square"),
            "mean_luma": round(float(gray.mean()), 1),
            "luma_std": round(float(gray.std()), 1),
            "laplacian_var": sharp,
            "mean_saturation": round(sat, 3),
            "resolution_class": qc,
        }
        metrics.append(m)
        src = by_id[r["image_id"]]
        src["image_quality"] = qc
        note = re.sub(r"\s*\|\s*Measured on (local|800px derivative) copy:.*$", "",
                      src.get("notes", "")).strip()
        src["notes"] = (note + f" | Measured on 800px derivative copy: {w}x{h}px, "
                        f"aspect {aspect}, sharpness(LapVar) {sharp}, "
                        f"mean luma {m['mean_luma']}/255; original file "
                        f"{orig or 'unknown'}.").strip(" |")

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(metrics)

    with open(CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)

    print(f"[metrics] {len(metrics)} images measured -> {os.path.relpath(OUT, ROOT)}")
    for cand in ("TALARICO", "PAXTON"):
        sub = [m for m in metrics if m["candidate_id"] == cand]
        if not sub:
            continue
        q = {}
        for m in sub:
            q[m["resolution_class"]] = q.get(m["resolution_class"], 0) + 1
        orient = {}
        for m in sub:
            orient[m["orientation"]] = orient.get(m["orientation"], 0) + 1
        print(f"  {cand}: n={len(sub)} resolution={q} orientation={orient} "
              f"median_aspect={sorted(m['aspect_ratio'] for m in sub)[len(sub)//2]}")


if __name__ == "__main__":
    main()
