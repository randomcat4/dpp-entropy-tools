#!/usr/bin/env python3
"""Run the frozen author checker on saved parts with a Windows resource shim.

The shim changes only unavailable process telemetry.  It does not change the
frozen checker, its inputs, constants, arithmetic, or predicates.
"""

from pathlib import Path
from types import ModuleType, SimpleNamespace
import runpy
import shutil
import sys


ROOT = Path(__file__).parent
CERT = ROOT / "certificate"
parts = [CERT / f"node_output.part{i}.tsv" for i in range(4)]
assembled = b"".join(path.read_bytes() for path in parts)
(CERT / "node_output.tsv").write_bytes(assembled)

shim = ModuleType("resource")
shim.RUSAGE_SELF = 0
shim.getrusage = lambda _: SimpleNamespace(ru_maxrss=0)
sys.modules["resource"] = shim

runpy.run_path(str(CERT / "check_certificate.py"), run_name="__main__")
shutil.copyfile(CERT / "certificate_result.json", ROOT / "frozen_saved_certificate_result.json")

