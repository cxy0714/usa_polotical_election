import io
p = "_staging/check.py"
s = io.open(p, encoding="utf-8").read()
a1 = 'if sf and sf != "unknown" and not os.path.exists'
b1 = 'if sf and sf not in ("unknown", "not_saved") and not os.path.exists'
a2 = '        sid = r["source_urls"].split("|")[0]'
b2 = '        if "source_urls" not in r:\n            continue\n        sid = r["source_urls"].split("|")[0]'
print("a1", s.count(a1), "a2", s.count(a2))
s = s.replace(a1, b1).replace(a2, b2)
io.open(p, "w", encoding="utf-8").write(s)
