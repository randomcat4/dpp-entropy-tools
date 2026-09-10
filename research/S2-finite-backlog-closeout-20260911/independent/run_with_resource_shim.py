#!/usr/bin/env python3
"""Run a frozen POSIX-oriented Python checker on Windows.

Only unavailable process-memory telemetry is replaced.  Mathematical code,
inputs, assertions, and outputs are left untouched.
"""

from types import ModuleType, SimpleNamespace
import runpy
import sys


if len(sys.argv) != 2:
    raise SystemExit("usage: run_with_resource_shim.py CHECKER.py")

shim = ModuleType("resource")
shim.RUSAGE_SELF = 0
shim.getrusage = lambda _: SimpleNamespace(ru_maxrss=0)
sys.modules["resource"] = shim
runpy.run_path(sys.argv[1], run_name="__main__")
