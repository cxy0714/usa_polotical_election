import urllib.request, os, re, json
here = os.path.dirname(os.path.abspath(__file__))
url = "https://en.wikipedia.org/w/index.php?title=2026_United_States_Senate_special_election_in_Ohio&action=raw"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research archive)"})
t = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
open(os.path.join(here, "ohio.wikitext"), "w", encoding="utf-8").write(t)
print("ohio", len(t))

for k in ["michigan","alaska","iowa","ohio","georgia","los-angeles"]:
    p = os.path.join(here, f"{k}.wikitext")
    txt = open(p, encoding="utf-8").read()
    body = txt.split("}}", 1)[-1]
    # find first bold sentence paragraph after infobox
    paras = [x.strip() for x in body.split("\n\n") if x.strip() and not x.strip().startswith(("{{","|","[[File","{|"))]
    print("\n=====", k, "=====")
    for para in paras[:3]:
        clean = re.sub(r"<ref[^>]*>.*?</ref>", "", para, flags=re.S)
        clean = re.sub(r"<ref[^>]*/>", "", clean)
        clean = re.sub(r"\[\[([^|\]]*\|)?([^\]]*)\]\]", r"\2", clean)
        print(clean[:900].replace("\n"," "))
