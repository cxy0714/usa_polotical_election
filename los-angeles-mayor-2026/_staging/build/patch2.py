# -*- coding: utf-8 -*-
import io, os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sources_data.py')
s = io.open(p, encoding='utf-8').read()
REPL = [
    ('"Spencer Pratt responds to Los Angeles mayoral race loss in new video"',
     '"Spencer Pratt responded to his loss in the Los Angeles mayoral race in a video posted Friday"'),
    ('"City Council progressives snub Raman, endorse Bass for L.A. mayor"',
     '"City Council progressives snub Raman, endorse Bass in L.A. mayor\'s race"'),
    ('"Jane Fonda Endorses Karen Bass for Los Angeles Mayor"',
     '"Jane Fonda Endorses LA Mayor Karen Bass for Reelection"'),
    ('"Four of five LA County supervisors endorse Karen Bass for mayor"',
     '"Four of the five LA County supervisors endorsed Karen Bass for mayor"'),
]
for a, b in REPL:
    if a not in s:
        print('MISS', a[:70])
    s = s.replace(a, b)
io.open(p, 'w', encoding='utf-8').write(s)
print('ok')
