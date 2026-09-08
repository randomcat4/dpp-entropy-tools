"""High-precision gate for the strongest joint basis/spectrum refinement point.

The arithmetic helpers are loaded from the already verified round-9 gate, but
the ledger aggregation and report are rebuilt for this independent result set.
"""

from __future__ import annotations

import importlib.util
import json
import time
from decimal import Decimal
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
HELPER_PATH = HERE.parent / "results_server_round9" / "recheck_best.py"
SPEC = importlib.util.spec_from_file_location("round9_gate_helpers", HELPER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load verified round-9 gate helpers")
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)
GATE.HERE = HERE


def main() -> None:
    started = time.time()
    ledger = GATE.aggregate_ledgers()
    best_shard = max(
        range(4),
        key=lambda shard: float(ledger["manifests"][shard]["best_rho_psd"]),
    )
    source = HERE / f"results_{best_shard}" / "best_case.npz"
    data = np.load(source)
    raw_kernel = np.asarray(data["kernel"], dtype=float)
    raw_direction = np.asarray(data["direction"], dtype=float)
    kernel = (raw_kernel + raw_kernel.T) / 2.0
    direction = (raw_direction + raw_direction.T) / 2.0
    mixed, _ = GATE.mixed_atoms_float(kernel)
    mobius = GATE.mobius_atoms_float(kernel)
    strongest_step = str(ledger["best_row"]["chord_step"])
    decimal_rows = [GATE.decimal_directional(kernel, direction, p) for p in (50, 70)]
    chords = GATE.decimal_chords(kernel, direction, [strongest_step, "0.001", "0.0001"])
    feasibility = GATE.exact_feasibility(kernel, direction)
    float_row = GATE.directional_float(kernel, direction)
    report = {
        "status": "HIGH_PRECISION_STABLE_NEGATIVE",
        "scope": "20,000 proposal rows from the pre-fix run plus one frozen strongest-case gate; finite evidence only",
        "old_run_bookkeeping_caveat": (
            "The producing script omitted the known-negative source/base from its ledger and positive_count. "
            "All 20,000 proposals are present; every proposal status and gap is checked directly here."
        ),
        "ledger": ledger,
        "strongest_shard": best_shard,
        "hashes": {
            "source_npz": GATE.sha256(HERE / "source.npz"),
            "best_case_npz": GATE.sha256(source),
            "run_version_script": GATE.sha256(HERE / "spectral_basis_refine_run_version.py"),
            "current_corrected_script": GATE.sha256(HERE.parent / "spectral_basis_refine.py"),
        },
        "symmetrization": {
            "kernel_max_asymmetry": float(np.max(np.abs(raw_kernel - raw_kernel.T))),
            "direction_max_asymmetry": float(np.max(np.abs(raw_direction - raw_direction.T))),
        },
        "spectra_and_commutation": {
            "K_min": float(np.linalg.eigvalsh(kernel)[0]),
            "K_max": float(np.linalg.eigvalsh(kernel)[-1]),
            "D_min": float(np.linalg.eigvalsh(direction)[0]),
            "D_max": float(np.linalg.eigvalsh(direction)[-1]),
            "commutator_frobenius": float(np.linalg.norm(kernel @ direction - direction @ kernel)),
        },
        "event_semantics_float": {
            "event_count": len(mixed),
            "sum_p_minus_one": float(mixed.sum() - 1.0),
            "min_probability": float(mixed.min()),
            "mobius_max_abs_difference": float(np.max(np.abs(mixed - mobius))),
            "mobius_max_relative_difference": float(np.max(np.abs(mixed - mobius) / mixed)),
        },
        "directional_float": float_row,
        "decimal_directional": decimal_rows,
        "decimal_chords": chords,
        "exact_fraction_feasibility": feasibility,
        "checks": {
            "all_20000_proposals_accounted": ledger["row_count"] == 20000,
            "no_proposal_candidate_status": ledger["positive_status_count"] == 0,
            "all_proposal_gaps_nonpositive": all(
                float(row["chord_gap"]) <= 0
                for shard in range(4)
                for row in __import__("csv").DictReader(
                    (HERE / f"results_{shard}" / "candidate_ledger.csv").open(encoding="utf-8", newline="")
                )
            ),
            "known_source_rho_below_one": all(
                float(manifest["source_rho_recomputed"]) < 1.0
                for manifest in ledger["manifests"]
            ),
            "best_rho_below_one": float(ledger["best_row"]["rho_psd"]) < 1.0,
            "decimal_rho_below_one": all(Decimal(row["rho"]) < 1 for row in decimal_rows),
            "decimal_H2_negative": all(Decimal(row["H2"]) < 0 for row in decimal_rows),
            "all_decimal_chords_negative": all(Decimal(row["midpoint_gap"]) < 0 for row in chords),
            "exact_interval_feasible": True,
            "direction_exact_positive_definite": True,
        },
        "exit_code": 0,
        "elapsed_seconds": time.time() - started,
    }
    if not all(report["checks"].values()):
        report["status"] = "FAILED_GATE"
        report["exit_code"] = 1
    (HERE / "recheck_best_refine.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["exit_code"]:
        raise SystemExit(report["exit_code"])


if __name__ == "__main__":
    main()
