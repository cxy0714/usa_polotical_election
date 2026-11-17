#!/usr/bin/env python3
"""Extract the event rows from the damaged builder into JSON, then let a clean builder own them.

The original builder's Python file was round-tripped through a PowerShell text write that
mojibaked its Chinese literals, so it no longer parses. Its English `ev(...)` calls are intact
literals, and those are the data. This script scans them, evaluates each argument tuple with
`ast.literal_eval`, and writes `events_data.json`. After this runs once, the builder can be
rewritten as pure ASCII plus a UTF-8 JSON bundle.

Run: python _staging/_extract_events.py
"""
import ast
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "_lead_build_events.py")
OUT = os.path.join(HERE, "events_data.json")


def scan_calls(text):
    calls, i = [], 0
    while True:
        j = text.find("ev(", i)
        if j < 0:
            break
        if text[max(0, j - 4):j].strip().endswith("def"):
            i = j + 3
            continue
        start = j + 3
        k, depth, quote = start, 1, None
        while k < len(text):
            ch = text[k]
            if quote:
                if ch == "\\":
                    k += 2
                    continue
                if ch == quote:
                    quote = None
            else:
                if ch in "\"'":
                    quote = ch
                elif ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0:
                        break
            k += 1
        args = text[start:k]
        try:
            tup = ast.literal_eval("(" + args + ")")
        except Exception as exc:  # noqa: BLE001
            print(f"  skip a call at offset {j}: {type(exc).__name__}")
            i = k + 1
            continue
        calls.append(list(tup))
        i = k + 1
    return calls


def main():
    text = open(SRC, encoding="utf-8", errors="replace").read()
    calls = scan_calls(text)
    print(f"found {len(calls)} event calls")
    widths = {len(c) for c in calls}
    print("argument counts:", widths)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(calls, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}")
    for c in calls[:2]:
        print(" ", c[0], c[1], c[2], "|", c[3][:60])
    return 0


if __name__ == "__main__":
    sys.exit(main())
