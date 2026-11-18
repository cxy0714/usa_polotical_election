import csv
import re

rows = list(csv.DictReader(open("_staging/discovery/ocj_hits.csv", encoding="utf-8")))
by_link = {}
for r in rows:
    by_link.setdefault(r["link"], r)

WANT = [
    "us senate race is center stage",
    "senator-elect sherrod brown could get an early start",
    "democrat sherrod brown defeats republican jon husted",
    "leads ohio republican u.s. sen. jon husted in quarterly",
    "sherrod brown comfortably outraises jon husted",
    "sherrod brown wins ohio democratic u.s. senate primary",
    "sherrod brown reportedly will run for ohio",
    "sherrod brown talks affordability at columbus roundtable",
    "sherrod brown launches dignity of work institute",
    "candidates offer contrasting visions for data centers",
    "leaked memo about data centers shows gop worried",
    "outside groups pour hundreds of millions into ohio races",
    "record-breaking spending",
    "dem strategist expects brown",
    "national democrats target us senate gop incumbents on health",
    "governor respond to calls from brown to extend protections",
    "jon husted wants to",
    "speaks against abortion pill during senate hearing",
    "how to fix social security",
    "senate balance of power falls to ohio",
    "elon musk donates $7 million",
    "family asks national republican senatorial committee",
    "woman accusing sherrod brown of forcing trans surgeries",
    "ohio lt. gov. jon husted to replace jd vance",
    "campaign is trying to portray sherrod brown as the incumbent",
    "new u.s. senator jon husted has a history of connections",
    "ohio u.s. senators husted and moreno",
    "husted took gifts from jobsohio",
    "husted political committee got nearly $500k",
    "top jon husted senate aide kept working",
    "met with man accused of bribery",
    "husted calls on gop us rep. miller",
    "intel plant has been stalled for years",
    "strong candidates in alaska, ohio seen as moving",
    "jon husted distanced himself from executives",
    "in person in corruption trial",
    "vote-early events, ohio capitol rally slated",
    "husted takes down post of him laughing",
    "no ohio u.s. senate candidate gives his unqualified support",
    "deeper look at who",
    "testify in firstenergy corruption trial",
    "ohio republicans launch debate on save act",
]
picked = {}
for want in WANT:
    for link, r in by_link.items():
        if want in r["title"].lower():
            picked[link] = r
            break
    else:
        print("MISS:", want)

lines = []
items = sorted(picked.items(), key=lambda kv: kv[1]["pubDate"][5:16])
for i, (link, r) in enumerate(items, 1):
    tail = re.sub(r"[^a-z0-9]+", "_", link.rstrip("/").rsplit("/", 1)[-1])[:55].strip("_")
    lines.append(f"ocj{i:02d}_{tail},{link}")
open("_staging/urls_ocj.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("picked", len(lines))
