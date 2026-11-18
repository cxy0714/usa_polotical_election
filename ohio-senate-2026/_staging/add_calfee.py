"""Insert the Calfee newsletter into _staging/registry.py once."""
p = "_staging/registry.py"
s = open(p, encoding="utf-8").read()
if "ref195_www_calfee_com_newsletters_830" in s:
    print("already present")
else:
    marker = "\n]\n"
    i = s.index("\n]\n", s.index("REGISTRY = ["))
    entry = (
        '    ("ref195_www_calfee_com_newsletters_830", "T2", "analysis", "2026-11-04",\n'
        '     "Calfee, Halter & Griswold election newsletter: unofficial statewide results with '
        'Brown 50.01% (2,302,669) over Husted 45.15% (2,080,064); Levy 2.05%, Redpath 2.79%; '
        'nearly 4.56 million votes cast; more than 1.7 million early ballots (D 468k, R 432k, '
        'unaffiliated about 807k); governor Russo 50.25% over Sprague 46.80%, Pruss 2.95%; '
        'treasurer Walsh 50.55-49.45; state Senate 54 D-44 R; state House 228 D.",\n'
        '     "Law-firm election newsletter summarising unofficial statewide results. Its '
        'rounded percentages differ from the race article by 0.01-0.02 points, so the difference '
        'is recorded as a source conflict rather than silently resolved.",\n'
        '     "results_notes.md; election_context.md"),\n')
    s = s[:i] + "\n" + entry + s[i + 1:]
    open(p, "w", encoding="utf-8").write(s)
    print("inserted")
