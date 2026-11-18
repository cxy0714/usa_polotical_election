# -*- coding: utf-8 -*-
import io
p = "_staging/fetch_log.csv"
log = io.open(p, encoding="utf-8").read().rstrip("\n").split("\n")
target = "https://bsky.app/profile/alaskasurvey.bsky.social/post/3mukcv6iqjk2d"
if not any(line.startswith(target + ",") for line in log):
    log.append("%s,200,33623,2026-11-18T13:23:44+08:00,"
               "_staging/mirrors/pages/bsky_app_profile_did_plc" % target)
    io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(log) + "\n")
    print("appended alias row")
else:
    print("already present")
print("rows:", len(log) - 1)
