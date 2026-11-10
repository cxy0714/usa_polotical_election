import csv, re, sys, io

ROOT = r"C:\Users\thinkbook-cxy\Documents\usa_polotical_election\texas-senate-2026"
STG = ROOT + r"\_staging"

EVENT_COLS = ["event_id","candidate_id","event_date","event_time","event_title","event_category","city","venue","state_region","event_status","campaign_phase","stated_purpose","observable_function","analyst_interpretation","target_audience","main_messages","policy_issues","speech_summary","transcript_url","video_url","photo_urls","media_coverage","opponent_reference","visual_notes","source_urls","verification_status","analyst_notes"]

CAND = {"TALARICO","PAXTON"}
STATUS = {"held","cancelled","postponed","rescheduled","virtual","announced","unverified","disputed"}
PHASE = {"pre_launch","launch","primary","runoff","general","early_voting","gotv","election_day","post_election"}
CATEGORY = {"launch","announcement","rally","town_hall","meet_and_greet","community_visit","small_business_visit","workplace_visit","university_visit","religious_appearance","labor_event","party_event","county_party_meeting","q_and_a","interview_tv","interview_radio","podcast","newspaper_interview","livestream","debate","debate_invitation","press_conference","video_release","tour_stop","tour_launch","tour_finale","fundraiser","endorsement_event","hq_opening","early_voting_event","gotv_event","surrogate_event","election_eve","watch_party","victory_speech","concession_speech","other"}
VERIF = {"verified","partially verified","unverified","conflicting sources"}
REGION = {"East Texas","North Texas","Central Texas","South Texas","West Texas","Gulf Coast","Panhandle","statewide","national","unknown"}
OPP = {"yes","no","unknown"}
TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")
DATE_RE = re.compile(r"^(\d{4}-(\d{2}(-\d{2})?)?|unknown)$")

def load(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            rows.append((i, line.split("\t")))
    return rows

def validate(rows, cols, name):
    errs = []
    for ln, f in rows:
        if len(f) != len(cols):
            errs.append(f"{name} line {ln}: {len(f)} fields, expected {len(cols)}")
            continue
        d = dict(zip(cols, f))
        if d["candidate_id"] not in CAND:
            errs.append(f"{name} line {ln} {d['event_id']}: bad candidate_id {d['candidate_id']!r}")
        if d["event_status"] not in STATUS:
            errs.append(f"{name} line {ln} {d['event_id']}: bad event_status {d['event_status']!r}")
        if d["campaign_phase"] not in PHASE:
            errs.append(f"{name} line {ln} {d['event_id']}: bad campaign_phase {d['campaign_phase']!r}")
        if d["event_category"] not in CATEGORY:
            errs.append(f"{name} line {ln} {d['event_id']}: bad event_category {d['event_category']!r}")
        if d["verification_status"] not in VERIF:
            errs.append(f"{name} line {ln} {d['event_id']}: bad verification_status {d['verification_status']!r}")
        if d["state_region"] not in REGION:
            errs.append(f"{name} line {ln} {d['event_id']}: bad state_region {d['state_region']!r}")
        if d["opponent_reference"] not in OPP:
            errs.append(f"{name} line {ln} {d['event_id']}: bad opponent_reference {d['opponent_reference']!r}")
        if not DATE_RE.match(d["event_date"]):
            errs.append(f"{name} line {ln} {d['event_id']}: bad event_date {d['event_date']!r}")
        if d["event_time"] != "unknown" and not TIME_RE.match(d["event_time"]):
            errs.append(f"{name} line {ln} {d['event_id']}: bad event_time {d['event_time']!r}")
        if not d["source_urls"].strip() or d["source_urls"].strip() == "unknown":
            errs.append(f"{name} line {ln} {d['event_id']}: empty source_urls")
        for c in cols:
            if d[c].strip() == "":
                errs.append(f"{name} line {ln} {d['event_id']}: blank cell {c}")
        if d["analyst_interpretation"].strip().lower().startswith("interpretation:") is False:
            errs.append(f"{name} line {ln} {d['event_id']}: analyst_interpretation missing INTERPRETATION: prefix")
    return errs

def write_csv(path, cols, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        w.writerow(cols)
        for _, f in rows:
            w.writerow(f)

ev = load(STG + r"\_A_rows_talarico.tsv") + load(STG + r"\_A_rows_paxton.tsv")
errs = validate(ev, EVENT_COLS, "events")
src = [(ln, f) for ln, f in load(STG + r"\_A_sources.tsv") if f and f[0] != "source_id"]
SRC_COLS = ["source_id","url","title","publisher","publication_date","event_date","access_date","source_tier","source_type","relevant_quote_or_info","reliability_notes","used_by"]
errs += validate_src if False else []
for ln, f in src:
    if len(f) != len(SRC_COLS):
        errs.append(f"sources line {ln}: {len(f)} fields, expected {len(SRC_COLS)}")
        continue
    d = dict(zip(SRC_COLS, f))
    if d["source_tier"] not in {"T1","T2","T3"}:
        errs.append(f"sources line {ln} {d['source_id']}: bad tier {d['source_tier']!r}")
    for c in SRC_COLS:
        if d[c].strip() == "":
            errs.append(f"sources line {ln}: blank cell {c}")

if errs:
    print("VALIDATION ERRORS (%d):" % len(errs))
    for e in errs:
        print("  " + e)
    sys.exit(1)

write_csv(ROOT + r"\02_campaign_events\campaign_events.csv", EVENT_COLS, ev)
write_csv(STG + r"\A_sources.csv", SRC_COLS, src)

tal = [f for _, f in ev if f[1] == "TALARICO"]
pax = [f for _, f in ev if f[1] == "PAXTON"]
print("campaign_events.csv rows: total %d | TALARICO %d | PAXTON %d" % (len(ev), len(tal), len(pax)))
dates = sorted(f[2] for _, f in ev)
print("earliest date:", dates[0], "latest date:", dates[-1])
print("A_sources.csv rows:", len(src))
