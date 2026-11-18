# -*- coding: utf-8 -*-
"""Wrapper: run the repo validator against this case without touching _tools/."""
import os
import runpy
import sys

ROOT = r"C:\Users\12257\Documents\usa_polotical_election"
sys.argv = ["validate_case.py", "iowa-senate-2026"]
os.chdir(ROOT)
runpy.run_path(os.path.join(ROOT, "_tools", "validate_case.py"), run_name="__main__")
