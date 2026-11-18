import json, os
base = os.path.join(os.path.dirname(os.path.abspath(__file__)))
cases = [
 dict(slug="michigan-senate-2026", race_name="2026 United States Senate election in Michigan",
      race_name_zh="2026 年密歇根州联邦参议员选举", case_number=3,
      candidates=[dict(id="ELSAYED", name="Abdul El-Sayed", party="Democratic", lower="elsayed"),
                  dict(id="ROGERS", name="Mike Rogers", party="Republican", lower="rogers")],
      county_keys=["elsayed","rogers"], poll_keys=["elsayed","rogers"],
      result=dict(winner="ELSAYED", margin_pct=7.08, source="SRC-0001"),
      state_regions=["Southeast","West","Mid","Northern","Thumb","statewide","national","unknown"]),
 dict(slug="alaska-senate-2026", race_name="2026 United States Senate election in Alaska",
      race_name_zh="2026 年阿拉斯加州联邦参议员选举", case_number=4,
      candidates=[dict(id="PELTOLA", name="Mary Peltola", party="Democratic", lower="peltola"),
                  dict(id="SULLIVAN", name="Dan S. Sullivan", party="Republican", lower="sullivan")],
      county_keys=["peltola","sullivan"], poll_keys=["peltola","sullivan"],
      result=dict(winner="PELTOLA", margin_pct=4.3, source="SRC-0001"),
      state_regions=["Anchorage","Matanuska-Susitna","Fairbanks","Southeast","Kenai Peninsula","Northern","Rural","statewide","national","unknown"]),
 dict(slug="iowa-senate-2026", race_name="2026 United States Senate election in Iowa",
      race_name_zh="2026 年艾奥瓦州联邦参议员选举", case_number=5,
      candidates=[dict(id="TUREK", name="Josh Turek", party="Democratic", lower="turek"),
                  dict(id="HINSON", name="Ashley Hinson", party="Republican", lower="hinson")],
      county_keys=["turek","hinson"], poll_keys=["turek","hinson"],
      result=dict(winner="TUREK", margin_pct=4.21, source="SRC-0001"),
      state_regions=["Central","Eastern","Western","Northern","Southern","statewide","national","unknown"]),
 dict(slug="ohio-senate-2026", race_name="2026 United States Senate special election in Ohio",
      race_name_zh="2026 年俄亥俄州联邦参议员特别选举", case_number=6,
      candidates=[dict(id="BROWN", name="Sherrod Brown", party="Democratic", lower="brown"),
                  dict(id="HUSTED", name="Jon Husted", party="Republican", lower="husted")],
      county_keys=["brown","husted"], poll_keys=["brown","husted"],
      result=dict(winner="BROWN", margin_pct=4.84, source="SRC-0001"),
      state_regions=["Northeast","Northwest","Central","Southwest","Southeast","statewide","national","unknown"]),
 dict(slug="georgia-senate-2026", race_name="2026 United States Senate election in Georgia",
      race_name_zh="2026 年佐治亚州联邦参议员选举", case_number=7,
      candidates=[dict(id="OSSOFF", name="Jon Ossoff", party="Democratic", lower="ossoff"),
                  dict(id="COLLINS", name="Mike Collins", party="Republican", lower="collins")],
      county_keys=["ossoff","collins"], poll_keys=["ossoff","collins"],
      result=dict(winner="OSSOFF", margin_pct=18.06, source="SRC-0001"),
      state_regions=["Metro Atlanta","North Georgia","Middle Georgia","South Georgia","Coastal Georgia","statewide","national","unknown"]),
 dict(slug="los-angeles-mayor-2026", race_name="2026 Los Angeles mayoral election",
      race_name_zh="2026 年洛杉矶市长选举", case_number=8,
      candidates=[dict(id="RAMAN", name="Nithya Raman", party="Nonpartisan", lower="raman"),
                  dict(id="BASS", name="Karen Bass", party="Nonpartisan", lower="bass")],
      county_keys=["raman","bass"], poll_keys=["raman","bass"],
      result=dict(winner="RAMAN", margin_pct=9.8, source="SRC-0001"),
      state_regions=["Central LA","San Fernando Valley","Westside","South LA","Harbor","Eastside","statewide","national","unknown"]),
]
for c in cases:
    d = os.path.join(base, c["slug"])
    os.makedirs(os.path.join(d, "_staging", "mirrors"), exist_ok=True)
    with open(os.path.join(d, "_staging", "case_meta.json"), "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("wrote", c["slug"])
