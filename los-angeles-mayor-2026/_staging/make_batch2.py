import json

items = [
    # CalMatters coverage (T2 established nonprofit newsroom)
    ("https://calmatters.org/commentary/2026/02/la-mayor-bass-election-challenge/", "cm_bass_challenge"),
    ("https://calmatters.org/commentary/2026/03/labor-los-angeles-mayor-race/", "cm_labor"),
    ("https://calmatters.org/commentary/2026/04/top-two-race-la-mayor/", "cm_top_two"),
    ("https://calmatters.org/commentary/2026/06/raman-bass-mayor-political-coalitions/", "cm_coalitions"),
    ("https://calmatters.org/commentary/2026/08/los-angeles-homelessness-raman-bass/", "cm_homelessness"),
    ("https://calmatters.org/commentary/2026/09/la-mayoral-rivals-public-safety/", "cm_public_safety"),
    ("https://calmatters.org/commentary/2026/10/la-mayoral-debate-friends-feud/", "cm_debate"),
    ("https://calmatters.org/commentary/2026/10/los-angeles-mayor-race-affordability/", "cm_affordability"),
    ("https://calmatters.org/commentary/2026/10/bass-raman-mayor-identity-politics/", "cm_identity"),
    ("https://calmatters.org/commentary/2026/11/mayor-nithya-raman-bass-los-angeles/", "cm_raman_wins"),
    ("https://calmatters.org/housing/2026/01/measure-ula-raman-dead/", "cm_ula_raman"),
    ("https://calmatters.org/commentary/2026/06/raman-pratt-los-angeles-mayor/", "cm_raman_pratt"),
    # Crosstown (data newsroom)
    ("https://xtown.la/", "xtown_home"),
    ("https://xtown.la/?s=mayor", "xtown_search_mayor"),
    # official
    ("https://ethics.lacity.gov/elections", "ethics_elections"),
    ("https://results.lavote.gov/", "lavote_results"),
    ("https://www.lavote.gov/home/elections/election-results", "lavote_home_results"),
    # campaign sites (may 403)
    ("https://karenbass.com/", "karenbass_home"),
    ("https://www.nithyaforthecity.com/", "nithya_home"),
]
json.dump([{"url": u, "tag": t} for u, t in items],
          open(r"C:\Users\12257\Documents\usa_polotical_election\los-angeles-mayor-2026\_staging\batch2.json", "w"), indent=1)
print(len(items))
