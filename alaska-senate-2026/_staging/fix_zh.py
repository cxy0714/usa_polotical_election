import io
p = "_research_conventions.md"
t = io.open(p, encoding="utf-8").read()
a = u"禁止空白、`TBD`、`N/A`、`-`。"
b = u"禁止空白单元格与占位字符串。"
print("occurrences:", t.count(a))
t = t.replace(a, b)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
