"""Render markdown docs with {{key}} -> SRC-#### substitution.

Usage: python _staging/b_docs1.py   (core docs)
"""
import re
import sys

sys.path.insert(0, "_staging")
from b_common import SRC, _resolve  # noqa: E402

FILL = re.compile(r"\{\{([A-Za-z0-9_]+)\}\}")


def render(text):
    missing = []

    def sub(m):
        k = m.group(1)
        try:
            return SRC[_resolve(k)][0]
        except KeyError:
            missing.append(k)
            return "SRC-????"

    out = FILL.sub(sub, text)
    if missing:
        raise KeyError("unresolved placeholders: " + ", ".join(sorted(set(missing))))
    return out


def write(path, text):
    import os
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    body = render(text)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print("wrote", path, len(body), "chars")
