"""Run the corrected round-14 high-precision gate on round-16 data."""

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "results_server_round14_refine2" / "recheck_best_refine2.py"
SPEC = importlib.util.spec_from_file_location("corrected_refinement_gate", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load corrected refinement gate")
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)
GATE.HERE = HERE
GATE.GATE.HERE = HERE


if __name__ == "__main__":
    GATE.main()
    inherited = HERE / "recheck_best_refine2.json"
    inherited.replace(HERE / "recheck_best_refine4.json")
