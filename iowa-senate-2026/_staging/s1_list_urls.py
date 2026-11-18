# -*- coding: utf-8 -*-
"""List reference URLs found in the local Wikipedia mirror, grouped by domain."""
import collections
import io
import re
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.join(HERE, "mirrors", "wiki_iowa.wikitext")

text = io.open(WIKI, encoding="utf-8").read()
urls = re.findall(r"https?://[^\s\|\]\}<>\"']+", text)
urls = [u.rstrip(".,;)") for u in urls]
dom = lambda u: re.sub(r"^https?://([^/]+).*", r"\1", u)
c = collections.Counter(dom(u) for u in urls)
for k, v in c.most_common():
    print("%4d  %s" % (v, k))
print("TOTAL occurrences", len(urls), "unique", len(set(urls)))
