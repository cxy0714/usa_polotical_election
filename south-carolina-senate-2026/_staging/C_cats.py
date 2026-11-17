from C_fetch import get_json, api
import json
cats = ["Category:Annie_Andrews","Category:Darline_Graham",
        "Category:United_States_Senate_election_in_South_Carolina,_2026",
        "Category:Lindsey_Graham"]
out = {}
for c in cats:
    url = api({"action":"query","list":"categorymembers","cmtitle":c,"cmlimit":"200","format":"json","formatversion":"2"})
    try:
        d = get_json(url)
        mem = d.get("query",{}).get("categorymembers",[])
        out[c] = [(m["title"], m.get("ns")) for m in mem]
        print("OK", c, len(mem))
        for t in out[c]:
            print("   ", t)
    except Exception as e:
        out[c] = "ERROR: %r" % e
        print("ERR", c, e)
json.dump(out, open("C_categorydump.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
