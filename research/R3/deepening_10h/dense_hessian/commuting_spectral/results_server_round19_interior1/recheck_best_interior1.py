"""Run the corrected high-precision gate on round-19 interior data."""

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "results_server_round14_refine2" / "recheck_best_refine2.py"
SPEC = importlib.util.spec_from_file_location("corrected_interior_gate", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load corrected refinement gate")
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)
GATE.HERE = HERE
GATE.GATE.HERE = HERE
ORIGINAL_SHA256 = GATE.GATE.sha256


def sha256_with_source_alias(path: Path) -> str:
    """Preserve the copied remote source name while satisfying the old gate."""
    if path.name == "source.npz" and not path.exists():
        path = HERE / "interior_source_margin003.npz"
    return ORIGINAL_SHA256(path)


GATE.GATE.sha256 = sha256_with_source_alias


if __name__ == "__main__":
    GATE.main()
    inherited = HERE / "recheck_best_refine2.json"
    inherited.replace(HERE / "recheck_best_interior1.json")
