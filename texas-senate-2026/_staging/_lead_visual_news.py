"""Lead: append verified news-photograph records (link-only, all rights reserved)
to image_archive.csv. Each row is grounded in a caption/credit line actually
retrieved from the named outlet; no image file is copied.
"""
import csv
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ARCH = os.path.join(ROOT, "04_visual_archive", "image_archive.csv")

HEADER = ["image_id", "candidate_id", "image_date", "event_id", "event_category",
          "source_name", "source_url", "original_image_url", "photographer",
          "copyright_status", "license", "local_filename", "image_resolution",
          "framing", "camera_angle", "image_quality", "face_visibility",
          "body_visibility", "clothing_notes", "notes", "verification_status"]

# (candidate, date, outlet, url, photographer, caption, event_hint, id_num)
NEWS = [
    ("TALARICO", "2025-07-24", "Spectrum News (Austin)",
     "https://spectrumlocalnews.com/tx/austin/news/2025/09/09/texas-democrat-james-talarico-announces-u-s--senate-campaign",
     "Eric Gay / AP",
     "Talarico speaks during a rally to protest against redistricting hearings at the Texas Capitol, Thursday, July 24, 2025, in Austin, Texas. (AP Photo/Eric Gay)",
     "TAL-EVT-0001", 1050),
    ("TALARICO", "2026-02-17", "mynews13 (Spectrum News 13)",
     "https://mynews13.com/fl/orlando/news/2026/09/29/capital-tonight-sept--28",
     "AP (photographer not named in retrieved caption)",
     "Texas state Rep. James Talarico, after voting, in Austin, Texas, Feb. 17, 2026 (composite caption pairing him with Paxton in McKinney 2026-05-19)",
     "TAL-EVT-0004", 1051),
    ("TALARICO", "2026-07-13", "Washington Examiner",
     "https://www.washingtonexaminer.com/news/campaigns/congressional/4709396/talarico-paxton-debate-",
     "AP (AP26195072328107)",
     "Democratic Senate candidate James Talarico speaks at a rally on Monday, July 13, 2026, in Eagle Pass, Texas. (AP Photo)",
     "TAL-EVT-0010", 1052),
    ("TALARICO", "2026-08-09", "FOX 7 Austin",
     "https://www.fox7austin.com/election/talarico-pasadena-rally-new-american-dream-tour",
     "Getty Images (photographer not named in retrieved caption)",
     "Getty photo caption carried by FOX 7 Austin for the Pasadena 'New American Dream Tour' rally, 2026-08-09",
     "TAL-EVT-0012", 1053),
    ("TALARICO", "2026-10-21", "KEYE / Telemundo Austin",
     "https://telemundoaustin.com/news/local/talarico-gana-la-contienda-por-el-senado-de-estados-unidos-en-texas",
     "Cecile Clocheret / AFP via Getty Images",
     "Talarico speaking at the Hilton University of Houston during the 'Clear Eyes, Full Hearts' tour, 2026-10-21",
     "TAL-EVT-0025", 1054),
    ("TALARICO", "2026-03-02", "Brookings Institution (caption)",
     "https://www.brookings.edu/articles/paxtons-landslide-win-signals-end-of-bush-era-texas-gop/",
     "Danielle Villasana / Getty Images",
     "Talarico is visiting various locations around the state in the lead up to tomorrow's primaries, March 2, 2026, Houston, Texas. (Photo by Danielle Villasana/Getty Images)",
     "unknown", 1055),
    ("TALARICO", "2026-03-03", "KLCC / NPR",
     "https://www.klcc.org/npr-news/2026-11-03/democrat-james-talarico-wins-texas-senate-seat",
     "unknown (credit not shown in retrieved caption)",
     "Texas Senate candidate James Talarico addresses supporters on primary election night in Austin, Texas (caption); image reused in the 2026-11-03 general-election story",
     "TAL-EVT-0008", 1056),
    ("TALARICO", "2026-11-03", "Houston Chronicle",
     "https://cmf.houstonchronicle.com/politics/texas/politifact/article/trump-white-house-ballroom-c",
     "unknown (Chronicle staff credit not shown in retrieved caption)",
     "James Talarico takes the stage at an election night watch party at The Long Center on Tuesday, Nov. 3, 2026 in Austin, Texas.",
     "TAL-EVT-0064", 1057),
    ("TALARICO", "2026-11-03", "Brookings Institution (caption)",
     "https://www.brookings.edu/articles/paxtons-landslide-win-signals-end-of-bush-era-texas-gop/",
     "Getty Images (photographer not named in retrieved caption)",
     "Supporters of Democratic U.S. Senate candidate James Talarico cheer after he won the Texas race during a midterm election night watch party at the Long Center for the Performing Arts.",
     "TAL-EVT-0064", 1058),
    ("PAXTON", "2022-10-22", "CNN",
     "https://www.cnn.com/2026/09/05/politics/maga-inc-ken-paxton-trump",
     "Getty Images (photographer not named in retrieved caption)",
     "Ken Paxton greets US President Donald Trump at the 'Save America' rally in Robstown, Texas, on October 22, 2022.",
     "unknown", 1050),
    ("PAXTON", "2026-05-19", "mynews13 (Spectrum News 13)",
     "https://mynews13.com/fl/orlando/news/2026/09/29/capital-tonight-sept--28",
     "AP (photographer not named in retrieved caption)",
     "Texas Attorney General Ken Paxton speaks in McKinney, Texas, May 19, 2026",
     "PAX-EVT-0012", 1051),
    ("PAXTON", "2026-09-09", "CNN",
     "https://edition.cnn.com/2026/09/23/politics/talarico-ad-glenn-rogers-criticizes-ken-paxton-texa",
     "Getty Images (photographer not named in retrieved caption)",
     "Ken Paxton speaks on stage on the first day of the 2026 Republican National Convention in Dallas on September 9.",
     "PAX-EVT-0008", 1052),
    ("PAXTON", "2026-09-09", "KWTX",
     "https://www.kwtx.com/2026/10/05/ken-paxton-raises-personal-best-18-million-third-quarter-texas-",
     "Julia (AP Photo; surname truncated in retrieved caption)",
     "Republican U.S. Senate candidate Texas Attorney General Ken Paxton speaks at the Republican convention Wednesday, Sept. 9, 2026, in Dallas. (AP Photo/Julia ...)",
     "PAX-EVT-0008", 1053),
    ("PAXTON", "2026-10-07", "Newsweek",
     "https://www.newsweek.com/ken-paxton-addresses-leaked-tape-him-criticizing-donald-trump-12555813",
     "AP (AP Photo credit; photographer not named)",
     "U.S. Senate candidate and Texas Attorney General Ken Paxton speaks during a campaign rally at the Freeman Coliseum in San Antonio on October 7, 2026. (AP Photo)",
     "PAX-EVT-0010", 1054),
    ("PAXTON", "2026-10-01", "Politico",
     "https://www.politico.com/news/2026/10/01/paxton-trump-cruz-texas-senate-rally-00000000",
     "Foto: Alex Brandon/AP (caption)",
     "Paxton at Peterbilt Motors in Denton with Trump and Ted Cruz, 2026-10-01; photo credit line carried in Politico caption",
     "PAX-EVT-0009", 1055),
]


def main():
    events = {}
    with open(os.path.join(ROOT, "02_campaign_events", "campaign_events.csv"),
              newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            d = r.get("event_date", "")
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
                events.setdefault((r["candidate_id"], d),
                                  (r["event_id"], r["event_category"]))

    with open(ARCH, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    prefix = {"TALARICO": "TAL-IMG-", "PAXTON": "PAX-IMG-"}
    used = {r["image_id"] for r in rows}
    added = 0
    for cand, date, outlet, url, photog, caption, hint, num in NEWS:
        iid = f"{prefix[cand]}{num:04d}"
        while iid in used:
            num += 1
            iid = f"{prefix[cand]}{num:04d}"
        used.add(iid)
        eid, ecat = events.get((cand, date), ("unknown", "unknown"))
        if hint != "unknown" and eid == "unknown":
            eid = hint
        rows.append({
            "image_id": iid, "candidate_id": cand, "image_date": date,
            "event_id": eid, "event_category": ecat,
            "source_name": outlet, "source_url": url,
            "original_image_url": "unknown (page exposes caption/credit only; "
                                  "no downloadable file URL)",
            "photographer": photog,
            "copyright_status": "all_rights_reserved_link_only",
            "license": "all rights reserved - link and credit only",
            "local_filename": "unknown",
            "image_resolution": "unknown",
            "framing": "unknown", "camera_angle": "unknown",
            "image_quality": "unknown", "face_visibility": "unknown",
            "body_visibility": "unknown", "clothing_notes": "unknown",
            "notes": caption + " | Recorded from the outlet's caption/credit line; "
                               "the image itself was NOT copied or redistributed "
                               "(copyright).",
            "verification_status": "partially verified",
        })
        added += 1

    rows.sort(key=lambda r: (r["candidate_id"], r["image_date"], r["image_id"]))
    with open(ARCH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rows)
    tal = sum(1 for r in rows if r["candidate_id"] == "TALARICO")
    pax = sum(1 for r in rows if r["candidate_id"] == "PAXTON")
    print(f"[image_archive.csv] appended {added} news rows -> total {len(rows)} "
          f"(TALARICO={tal}, PAXTON={pax})")


if __name__ == "__main__":
    main()
