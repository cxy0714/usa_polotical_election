import csv, sys, os, collections

base = r"south-carolina-senate-2026"
files = {
    "speech_archive": os.path.join(base, "03_speeches", "speech_archive.csv"),
    "speech_video_index": os.path.join(base, "03_speeches", "speech_video_index.csv"),
    "D_sources": os.path.join(base, "_staging", "D_sources.csv"),
}
expected = {
    "speech_archive": "speech_id,candidate_id,event_id,date,speech_title,speech_url,transcript_url,duration,main_topics,major_quotes,rhetorical_devices,opponent_references,personal_story_elements,policy_claims,source_urls,source,verification_status".split(","),
    "speech_video_index": "video_id,candidate_id,video_url,date,duration,event_type,main_topics,relevant_timestamps,transcript_available,visual_observations,completeness,source_urls,verification_status".split(","),
    "D_sources": "source_id,url,title,publisher,publication_date,event_date,access_date,source_tier,source_type,relevant_quote_or_info,reliability_notes,used_by".split(","),
}
for key, path in files.items():
    raw = open(path, "rb").read()
    print(key, "BOM" if raw.startswith(b"\xef\xbb\xbf") else "no-BOM",
          "CRLF" if b"\r\n" in raw else "LF", len(raw), "bytes")
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    hdr = rows[0]
    if hdr != expected[key]:
        print("  HEADER MISMATCH:")
        for a, b in zip(hdr, expected[key]):
            if a != b:
                print("   got:", repr(a), "want:", repr(b))
        print("   len", len(hdr), len(expected[key]))
    bad = 0
    for i, r in enumerate(rows[1:], start=2):
        if len(r) != len(hdr):
            print("  BAD FIELD COUNT line", i, len(r))
            bad += 1
        elif any(c.strip() == "" for c in r):
            print("  BLANK CELL line", i, [hdr[j] for j, c in enumerate(r) if c.strip() == ""])
            bad += 1
    print("  data rows:", len(rows) - 1, "problems:", bad)

# candidate balance
with open(files["speech_archive"], newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))
c = collections.Counter(r["candidate_id"] for r in rows)
print("speech_archive by candidate:", dict(c))
print("ids:", [r["speech_id"] for r in rows])
with open(files["speech_video_index"], newline="", encoding="utf-8") as fh:
    v = list(csv.DictReader(fh))
print("video rows:", len(v), dict(collections.Counter(r["candidate_id"] for r in v)))
with open(files["D_sources"], newline="", encoding="utf-8") as fh:
    s = list(csv.DictReader(fh))
ids = [r["source_id"] for r in s]
print("sources:", len(s), "unique:", len(set(ids)), "dupes:", [k for k, n in collections.Counter(ids).items() if n > 1])
out = [i for i in ids if not (800 <= int(i.split("-")[1]) <= 1099)]
print("out-of-block:", out)
print("source field spot:", s[43]["source_id"], "|", s[43]["url"])
