#!/usr/bin/env python3
"""Point the three photo-documented events at their real Commons file pages.

The events were first written with placeholder Commons titles; the visual archive already holds the
correct file URLs, so they are read from there rather than retyped. Commons pages share one source
row (SRC-0600), which is why the events must carry the token rather than a bare URL.

Run: python _staging/_lead_patch_event_photos.py
"""
import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG = os.path.join(ROOT, "04_visual_archive", "image_archive.csv")
BUILDER = os.path.join(HERE, "_lead_events_build.py")

WANT = {
    "greenville": "GREENVILLE",
    "gas_grits": "GASGRITS",
    "fort_mill": "FORTMILL",
}


def main():
    rows = list(csv.DictReader(open(IMG, encoding="utf-8")))
    picked = {}
    for r in rows:
        local = (r.get("local_filename") or "")
        src = r.get("source_url") or ""
        for key, const in WANT.items():
            if key in local and const not in picked and src.startswith("SRC-"):
                picked[const] = src
    missing = [c for c in WANT.values() if c not in picked]
    print("resolved:", {k: v.split("|")[1][:60] for k, v in picked.items()})
    if missing:
        print("unresolved constants:", missing)
        return 1

    text = open(BUILDER, encoding="utf-8").read()
    block = ("CM = \"SRC-0600|https://commons.wikimedia.org/wiki/File%3A\"\n"
             + "\n".join(f'{c} = "{picked[c]}"' for c in WANT.values()))
    text = re.sub(r'IMG = "https://commons\.wikimedia\.org/wiki/File%3A"', block, text, count=1)
    text = text.replace('IMG + "Annie_Andrews_at_Greenville_Tech.jpg"', "GREENVILLE")
    text = text.replace('IMG + "Annie_Andrews_Gas_Grits_Groceries.jpg"', "GASGRITS")
    text = text.replace('IMG + "Annie_Andrews_Fort_Mill_2026.jpg"', "FORTMILL")
    open(BUILDER, "w", encoding="utf-8", newline="\n").write(text)
    print("builder patched; leftover IMG refs:", text.count("IMG +"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
