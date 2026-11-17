from C_fetch import get
import re
t = get("https://en.wikipedia.org/w/index.php?title=2026_United_States_Senate_election_in_South_Carolina&action=raw&section=62").decode("utf-8")
print("len", len(t))
urls = re.findall(r"https?://[^\s|}<\]]+", t)
seen=[]
for u in urls:
    if u not in seen: seen.append(u)
print("unique urls", len(seen))
open("C_refs.txt","w",encoding="utf-8").write("\n".join(seen))
for u in seen:
    if any(k in u for k in ("postandcourier","thestate.com","scdailygazette","wltx","wistv","counton2","foxcarolina","wspa","greenville","apnews","cnn.com","cbsnews","npr","politico","axios","reuters")):
        print(u)
