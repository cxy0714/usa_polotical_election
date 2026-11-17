from C_fetch import get_json, api
import json

andrews = [
 "File:Annie Andrews at Gas, Grits and Groceries Tour in Abbeville (2026) (cropped).jpg",
 "File:Annie Andrews at Gas, Grits and Groceries Tour in Abbeville (2026).jpg",
 "File:Annie Andrews Fort Mill 2026 (cropped 3).png",
 "File:Annie Andrews Fort Mill 2026 (cropped).png",
 "File:Annie Andrews Fort Mill 2026.png",
 "File:Annie Andrews Greenville (cropped 2).jpg",
 "File:Annie Andrews Greenville (cropped).jpg",
 "File:Annie Andrews Greenville.jpg",
 "File:Annie Andrews in November 2026.jpg",
 "File:Annie Andrews York Town (cropped 2).png",
 "File:Annie Andrews York Town (cropped).png",
 "File:Annie Andrews York Town.png",
 "File:Jim Clyburn and Annie Andrews in November 2026.jpg",
 "File:Tim Scott and Annie Andrews in November 2026.jpg",
 "File:Democratic senators-elect meet with Chuck Schumer in November 2026.jpg",
 "File:Annie Andrews Senate Campaign Building.jpg",
]
graham = [
 "File:2026-07-26-TS-Graham-Britt-1024x768.png",
 "File:2026-07-26-TS-Graham-Britt-1024x768 cropped.png",
 "File:2026-07-26-TS-Graham-Britt-1024x768 cropped 2.png",
 "File:Darline Graham Nordone butter cow.jpg",
 "File:Darline Graham Nordone butter cow (cropped).jpg",
 "File:Darline Graham Nordone Okra Strut.jpg",
 "File:Darline Graham Nordone Okra Strut (cropped).jpg",
 "File:Darline Graham official portrait.jpg",
 "File:Darline Graham official portrait (cropped).jpg",
 "File:Darline Graham official portrait (cropped2).jpg",
 "File:Darline Graham official portrait (cropped3).jpg",
 "File:Darline Graham swear-in.png",
 "File:Darline Graham swear-in (cropped).png",
 "File:Darline Graham, 2026 (cropped).png",
 "File:Official portrait of Darline Graham, member of the United States Senate from South Carolina (2026).jpg",
 "File:Official portrait of Darline Graham, member of the United States Senate from South Carolina (2026) (cropped).jpg",
 "File:Official portrait of Darline Graham, member of the United States Senate from South Carolina (2026) (cropped) 2.jpg",
 "File:P20260918JB-1105 (55542085664).jpg",
 "File:P20260918JB-1111 (55542038358).jpg",
 "File:P20260918JB-1120 (55542038343).jpg",
 "File:Sen. Darline Graham (R-SC), Official Portrait, 119th Congress.jpg",
 "File:Sen. Darline Graham Delivers Floor Remarks in support of Russia Sanctions Bill.webm",
 "File:Senator Darline Graham Official Portrait, 119th Congress.jpg",
 "File:Senator Chuck Grassley Swears In Darline Graham As Senator Of South Carolina.jpg",
]
graham = [t for t in graham if not t.endswith(".webm")]

allm = {}
for name, titles in (("andrews", andrews), ("graham", graham)):
    url = api({"action":"query","titles":"|".join(titles),
               "prop":"imageinfo","iiprop":"url|size|extmetadata","iiurlwidth":"900",
               "format":"json","formatversion":"2"})
    d = get_json(url)
    pages = d.get("query",{}).get("pages",[])
    print("==", name, "requested", len(titles), "pages", len(pages))
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata",{}) or {}
        def v(k):
            x = em.get(k,{})
            return x.get("value") if isinstance(x,dict) else x
        allm[p["title"]] = {
            "ns": p.get("ns"),
            "missing": p.get("missing", False),
            "url": ii.get("url"),
            "thumburl": ii.get("thumburl"),
            "width": ii.get("width"), "height": ii.get("height"),
            "size": ii.get("size"),
            "LicenseShortName": v("LicenseShortName"),
            "License": v("License"),
            "Artist": v("Artist"),
            "Credit": v("Credit"),
            "DateTimeOriginal": v("DateTimeOriginal"),
            "ImageDescription": v("ImageDescription"),
            "Categories": v("Categories"),
            "UsageTerms": v("UsageTerms"),
        }
        if p.get("missing"):
            print("  MISSING", p.get("title"))
        else:
            print("  ", p.get("title"), "|", allm[p["title"]]["LicenseShortName"], "|", allm[p["title"]]["width"], "x", allm[p["title"]]["height"], "| thumb:", bool(allm[p["title"]]["thumburl"]))
json.dump(allm, open("C_meta.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
