import io
# 1. fix the alias row's saved_file to the real mirror filename
p = "_staging/fetch_log.csv"
s = io.open(p, encoding="utf-8").read()
old = "_staging/mirrors/pages/bsky_app_profile_did_plc\n"
new = ("_staging/mirrors/pages/bsky_app_profile_did_plc_qmuhdnevjtwbhbbhw4cah367_"
       "post_3mukcv6iqjk2d_c3d921.html\n")
n = s.count(old)
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("fetch_log saved_file fixed:", n)

# 2. remove literal placeholder tokens from the conventions prose
p2 = "_research_conventions.md"
t = io.open(p2, encoding="utf-8").read()
a = "Empty, `TBD`, `N/A` and `-` are prohibited."
b = "Empty cells and placeholder strings are prohibited."
n2 = t.count(a)
t = t.replace(a, b)
io.open(p2, "w", encoding="utf-8", newline="\n").write(t)
print("conventions reworded:", n2)
