import json

items = []
for p in ['/why-im-running', '/term-2-vision', '/how-we-changed-la', '/endorsements']:
    items.append({"url": "https://karenbass.com" + p, "tag": "bass_site" + p.replace('/', '_')})
for p in ['/about-nithya', '/why-im-running', '/housing', '/homelessness', '/publicsafety',
          '/renters', '/palisadesrecovery', '/transportation', '/endorsements']:
    items.append({"url": "https://www.nithyaforthecity.com" + p, "tag": "raman_site" + p.replace('/', '_')})
json.dump(items, open(r"C:\Users\12257\Documents\usa_polotical_election\los-angeles-mayor-2026\_staging\batch3.json", "w"), indent=1)
print(len(items))
