import json, os
d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'refs.json'), encoding='utf-8'))
for i, x in enumerate(d):
    print('%03d|%s|%s|%s|%s' % (i, x['work'][:28], x['date'][:18], x['title'][:100], x['url'][:120]))
