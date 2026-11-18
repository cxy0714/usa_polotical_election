import urllib.request, os
pages = {
 "michigan": "2026_United_States_Senate_election_in_Michigan",
 "alaska": "2026_United_States_Senate_election_in_Alaska",
 "iowa": "2026_United_States_Senate_election_in_Iowa",
 "ohio": "2026_United_States_Senate_election_in_Ohio",
 "georgia": "2026_United_States_Senate_election_in_Georgia",
 "los-angeles": "2026_Los_Angeles_mayoral_election",
}
here = os.path.dirname(os.path.abspath(__file__))
for k, p in pages.items():
    url = f"https://en.wikipedia.org/w/index.php?title={p}&action=raw"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research archive)"})
        t = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
        with open(os.path.join(here, f"{k}.wikitext"), "w", encoding="utf-8") as f:
            f.write(t)
        print(k, len(t), "OK")
    except Exception as e:
        print(k, "ERR", e)
