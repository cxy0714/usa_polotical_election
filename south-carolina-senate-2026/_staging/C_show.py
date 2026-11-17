import json, re, html
m = json.load(open("C_meta.json",encoding="utf-8"))
def clean(s):
    if not s: return ""
    s = re.sub(r"<[^>]+>"," ",s)
    s = html.unescape(s)
    return re.sub(r"\s+"," ",s).strip()
for t,v in sorted(m.items()):
    print("##", t)
    print("   lic:", v["LicenseShortName"], "| lic2:", v["License"], "| px:", v["width"], "x", v["height"])
    print("   date:", clean(v["DateTimeOriginal"])[:80])
    print("   artist:", clean(v["Artist"])[:120])
    print("   credit:", clean(v["Credit"])[:120])
    print("   desc:", clean(v["ImageDescription"])[:400])
