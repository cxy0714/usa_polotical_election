import re, collections, sys

p = r"texas-senate-2026/10_video_frames/assets/talarico_logo.svg"
t = open(p, encoding="utf-8").read()
print("paths:", len(re.findall(r"<path", t)))
print("fills:", collections.Counter(re.findall(r'fill="([^"]+)"', t)))
print("strokes:", collections.Counter(re.findall(r'stroke="([^"]+)"', t)))
print("viewBox:", re.findall(r'viewBox="([^"]+)"', t))
print("width/height:", re.findall(r'(?:width|height)="([^"]+)"', t)[:4])
print("style blocks:", len(re.findall(r"<style", t)))
m = re.search(r"<style[^>]*>(.*?)</style>", t, re.S)
if m:
    print(m.group(1)[:800])
print("g transforms:", len(re.findall(r"<g", t)))
