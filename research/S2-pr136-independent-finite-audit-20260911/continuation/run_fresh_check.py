#!/usr/bin/env python3
"""Run the frozen author checker on the new Windows production output.

The frozen checker is copied byte-for-byte into ``fresh-author-check``.  This
wrapper supplies only the unavailable Windows process-telemetry module; it
does not alter any certificate arithmetic or predicate.
"""

from pathlib import Path
from types import ModuleType, SimpleNamespace
import runpy
import sys


ROOT = Path(__file__).parent
CHECK_ROOT = ROOT / "fresh-author-check"

shim = ModuleType("resource")
shim.RUSAGE_SELF = 0
shim.getrusage = lambda _: SimpleNamespace(ru_maxrss=0)
sys.modules["resource"] = shim

runpy.run_path(str(CHECK_ROOT / "check_certificate.py"), run_name="__main__")
