# -*- coding: utf-8 -*-
pairs = [
 ('README.md', '12 archived images (5 local)', '13 archived images (5 local)'),
 ('README.md', '12 images, 5 downloaded under open licences', '13 images, 5 downloaded under open licences'),
 ('README.md', '`04_visual_archive/` 12 images', '`04_visual_archive/` 13 images'),
 ('09_sources/data_dictionary_bilingual.md', '| 12 | 图像档案，5 张已本地保存 |', '| 13 | 图像档案，5 张已本地保存 |'),
 ('09_sources/data_dictionary_bilingual.md', '12 rows; `local_filename`', '13 rows; `local_filename`'),
]
for p, old, new in pairs:
    t = open(p, encoding='utf-8').read()
    if old in t:
        t = t.replace(old, new)
        open(p, 'w', encoding='utf-8', newline='\n').write(t)
        print('patched', p, old[:44])
    else:
        print('MISS', p, old[:44])
