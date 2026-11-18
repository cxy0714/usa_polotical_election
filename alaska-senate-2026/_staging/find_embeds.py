import re, glob, os
pats = re.compile(r"https?://(?:www\.)?(?:youtube\.com/(?:embed/|watch\?v=|shorts/)[A-Za-z0-9_\-]+|youtu\.be/[A-Za-z0-9_\-]+|vimeo\.com/\d+)")
for p in sorted(glob.glob("_staging/mirrors/pages/*marypeltola*") +
                glob.glob("_staging/mirrors/pages/*dansullivanforalaska*") +
                glob.glob("_staging/mirrors/pages/*sullivanforsenate*") +
                glob.glob("_staging/mirrors/pages/*politicalemails*")):
    s = open(p, encoding="utf-8", errors="ignore").read()
    urls = sorted(set(pats.findall(s)))
    print(os.path.basename(p)[:60], len(urls))
    for u in urls[:10]:
        print("   ", u[:120])
