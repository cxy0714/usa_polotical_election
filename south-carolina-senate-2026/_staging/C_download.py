# -*- coding: utf-8 -*-
"""Stream C step 3: download the chosen freely-licensed Commons files into
04_visual_archive/<cand>/campaign/ and record real measured stats."""
from C_fetch import get
import json, os, re, io
from PIL import Image
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
META = json.load(open("C_meta.json", encoding="utf-8"))

# (image_id, commons title, candidate dir)
PLAN = [
 ("AND-IMG-0001","File:Annie Andrews in November 2026.jpg","andrews"),
 ("AND-IMG-0002","File:Annie Andrews Greenville.jpg","andrews"),
 ("AND-IMG-0003","File:Annie Andrews at Gas, Grits and Groceries Tour in Abbeville (2026).jpg","andrews"),
 ("AND-IMG-0004","File:Annie Andrews at Gas, Grits and Groceries Tour in Abbeville (2026) (cropped).jpg","andrews"),
 ("AND-IMG-0005","File:Annie Andrews Fort Mill 2026.png","andrews"),
 ("AND-IMG-0006","File:Annie Andrews York Town.png","andrews"),
 ("AND-IMG-0007","File:Jim Clyburn and Annie Andrews in November 2026.jpg","andrews"),
 ("AND-IMG-0008","File:Tim Scott and Annie Andrews in November 2026.jpg","andrews"),
 ("AND-IMG-0009","File:Democratic senators-elect meet with Chuck Schumer in November 2026.jpg","andrews"),
 ("AND-IMG-0010","File:Annie Andrews Senate Campaign Building.jpg","andrews"),
 ("GRA-IMG-0001","File:Darline Graham official portrait.jpg","graham"),
 ("GRA-IMG-0002","File:Official portrait of Darline Graham, member of the United States Senate from South Carolina (2026).jpg","graham"),
 ("GRA-IMG-0003","File:Sen. Darline Graham (R-SC), Official Portrait, 119th Congress.jpg","graham"),
 ("GRA-IMG-0004","File:Darline Graham swear-in.png","graham"),
 ("GRA-IMG-0005","File:Senator Chuck Grassley Swears In Darline Graham As Senator Of South Carolina.jpg","graham"),
 ("GRA-IMG-0006","File:2026-07-26-TS-Graham-Britt-1024x768.png","graham"),
 ("GRA-IMG-0007","File:Darline Graham Nordone butter cow.jpg","graham"),
 ("GRA-IMG-0008","File:Darline Graham Nordone Okra Strut.jpg","graham"),
 ("GRA-IMG-0009","File:P20260918JB-1105 (55542085664).jpg","graham"),
 ("GRA-IMG-0010","File:Darline Graham, 2026 (cropped).png","graham"),
]

def slug(title):
    s = title[5:] if title.startswith("File:") else title
    s = s.lower().replace("%20","_").replace(" ","_")
    s = re.sub(r"[^a-z0-9._-]+","_",s)
    s = re.sub(r"_+","_",s).strip("_")
    return s

def lapvar(gray):
    g = gray.astype(np.float64)
    k = np.array([[0,1,0],[1,-4,1],[0,1,0]], dtype=np.float64)
    from numpy.lib.stride_tricks import sliding_window_view
    w = sliding_window_view(g, (3,3))
    lap = (w*k).sum(axis=(2,3))
    return float(lap.var())

def stats(path):
    im = Image.open(path)
    W,H = im.size
    g = im.convert("L").resize((min(W,900), max(1,int(min(W,900)*H/W))), Image.LANCZOS)
    a = np.asarray(g, dtype=np.float64)
    return {"w":W,"h":H,"aspect":round(W/H,4),"sharpness":round(lapvar(a),1),
            "mean_luma":round(float(a.mean()),1),"bytes":os.path.getsize(path)}

out = []
for iid, title, cand in PLAN:
    m = META[title]
    url = m["thumburl"] or m["url"]
    ext = os.path.splitext(slug(title))[1] or ".jpg"
    fname = iid + "_" + slug(title)
    if not fname.lower().endswith(ext.lower()):
        fname += ext
    d = os.path.join(ROOT, "04_visual_archive", cand, "campaign")
    os.makedirs(d, exist_ok=True)
    dest = os.path.join(d, fname)
    if not os.path.exists(dest) or os.path.getsize(dest) < 5000:
        raw = get(url)
        open(dest,"wb").write(raw)
        print("downloaded", iid, len(raw), "bytes ->", fname)
    else:
        print("exists", fname)
    st = stats(dest)
    rec = {"image_id":iid,"title":title,"cand":cand,
           "local_filename": f"{cand}/campaign/{fname}",
           "thumb_url": url, "orig_url": m["url"], "thumb_px":[m["width"],m["height"]],
           "stats": st}
    out.append(rec)
    print("   ", st)
json.dump(out, open("C_downloads.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("TOTAL", len(out))
