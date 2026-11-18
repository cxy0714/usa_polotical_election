import io
p = "_staging/data_core.py"
lines = io.open(p, encoding="utf-8").read().split("\n")
out = []
changed = 0
for line in lines:
    if 'entry_id="PEL-CAR-06"' in line:
        line = line.replace('start_date="2023-09"', 'start_date="unknown"'); changed += 1
    elif 'entry_id="PEL-CAR-08"' in line:
        line = line.replace('start_date="2025-01", end_date="2026-01"',
                            'start_date="unknown", end_date="unknown"'); changed += 1
    elif 'entry_id="SUL-CAR-02"' in line:
        line = line.replace('start_date="1993", end_date="1997"',
                            'start_date="unknown", end_date="unknown"'); changed += 1
    elif 'entry_id="SUL-CAR-08"' in line:
        line = line.replace('start_date="2024-02"', 'start_date="unknown"'); changed += 1
    out.append(line)
io.open(p, "w", encoding="utf-8").write("\n".join(out))
print("lines changed:", changed)
