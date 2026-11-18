"""Download licensed Wikimedia Commons portraits (PD/CC0/CC BY/CC BY-SA), <2 MB each.

Writes into 04_visual_archive/<cand>/, records the Commons file page + upload URL in
_staging/fetch_log.csv, and saves a metadata sidecar for the image_archive build.
"""
import urllib.request, json, os, csv, re, hashlib
from datetime import datetime, timezone, timedelta

CASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(CASE, "_staging", "fetch_log.csv")
UA = "Mozilla/5.0 (research archive; +https://example.org/research)"
TZ = timezone(timedelta(hours=8))
ALLOWED = re.compile(r"(public domain|cc0|cc by|cc-by|pd)", re.I)

# (candidate_lower, image_id, filename_stub, Commons title)
PICKS = [
    ("peltola", "PEL-IMG-0001", "peltola_official_portrait_117th_congress",
     "File:U.S. Representative Mary Peltola, 117th Congress.jpg"),
    ("peltola", "PEL-IMG-0002", "peltola_congressional_member_portrait",
     "File:Mary Peltola Congressional Member Portrait (2) (cropped).jpeg"),
    ("peltola", "PEL-IMG-0003", "peltola_indian_affairs_hearing",
     "File:Mary Peltola Testifying at Indian Affairs Oversight Hearing (cropped).jpg"),
    ("sullivan", "SUL-IMG-0001", "sullivan_official_senate_portrait",
     "File:Senator Dan Sullivan official.jpg"),
    ("sullivan", "SUL-IMG-0002", "sullivan_memorial_day_2024",
     "File:Senator Sullivan Memorial Day 2024 (cropped).jpg"),
    ("sullivan", "SUL-IMG-0003", "sullivan_memorial_day_2022_wasilla",
     "File:Dan Sullivan, Memorial Day 2022, Wasilla, Alaska (cropped).jpg"),
]

meta = {r["title"]: r for r in json.load(open(os.path.join(CASE, "_staging", "commons_candidates.json"),
                                             encoding="utf-8"))}


def fetch(u, dst):
    req = urllib.request.Request(u, headers={"User-Agent": UA})
    r = urllib.request.urlopen(req, timeout=60)
    data = r.read()
    with open(dst, "wb") as f:
        f.write(data)
    return r.status, len(data)


rows, out = [], []
for cand, img_id, stub, title in PICKS:
    m = meta[title]
    assert ALLOWED.search(m["lic"]), (title, m["lic"])
    page = "https://commons.wikimedia.org/wiki/" + title.replace(" ", "_")
    fn = f"{img_id}_{stub}.jpg"
    dst = os.path.join(CASE, "04_visual_archive", cand, fn)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    st, n = fetch(m["thumb"], dst)
    assert n < 2_000_000, (fn, n)
    now = datetime.now(TZ).isoformat(timespec="seconds")
    rows.append([m["thumb"], st, n, now, f"04_visual_archive/{cand}/{fn}"])
    # file page also logged (as html mirror)
    try:
        st2, n2 = fetch(page, os.path.join(CASE, "_staging", "mirrors", "pages",
                                           re.sub(r"[^A-Za-z0-9]+", "_", title) + ".html"))
        rows.append([page, st2, n2, now,
                     "_staging/mirrors/pages/" + re.sub(r"[^A-Za-z0-9]+", "_", title) + ".html"])
    except Exception as e:
        rows.append([page, "ERR", 0, now, "not_saved"])
    out.append(dict(image_id=img_id, candidate=cand, file=fn, commons_title=title,
                    commons_page=page, upload_url=m["thumb"], original_url=m["orig"],
                    width=m["tw"], height=m["th"], orig_width=m["ow"], orig_height=m["oh"],
                    license=m["lic"], usage=m["usage"], artist=m["artist"],
                    credit=m["credit"], description=m["desc"], date=m["date"], bytes=n))
    print("saved", fn, n)

with open(LOG, "a", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    for r in rows:
        w.writerow(r)
json.dump(out, open(os.path.join(CASE, "_staging", "portrait_meta.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("done", len(out))
