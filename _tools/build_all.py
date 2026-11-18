#!/usr/bin/env python3
"""Rebuild every batch-2 case site, validate the data, then rebuild the shared portal.

Usage: python _tools/build_all.py [slug ...]

With no arguments it runs over the six batch-2 cases. Each step is a separate
process so a failure in one case does not stop the others; the exit code is the
number of failed steps (capped at 1 by the shell).
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH2 = ["michigan-senate-2026", "alaska-senate-2026", "iowa-senate-2026",
          "ohio-senate-2026", "georgia-senate-2026", "los-angeles-mayor-2026"]


def run(args):
    print("$", " ".join(args))
    return subprocess.call(args, cwd=ROOT)


def main(argv):
    cases = argv[1:] or BATCH2
    failed = 0
    for case in cases:
        failed += run([sys.executable, "_tools/validate_case.py", case]) != 0
        failed += run([sys.executable, "_tools/build_case_site.py", case]) != 0
    failed += run([sys.executable, "_tools/build_portal.py"]) != 0
    print(f"\nsteps failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
