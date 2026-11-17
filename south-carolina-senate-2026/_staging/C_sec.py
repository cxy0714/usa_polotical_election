from C_fetch import get
for n in (51,58):
    u = f"https://en.wikipedia.org/w/index.php?title=2026_United_States_Senate_election_in_South_Carolina&action=raw&section={n}"
    try:
        t = get(u).decode("utf-8")
        print("=== section", n, len(t))
        print(t[:2500])
        print("...")
    except Exception as e:
        print("ERR", n, e)
