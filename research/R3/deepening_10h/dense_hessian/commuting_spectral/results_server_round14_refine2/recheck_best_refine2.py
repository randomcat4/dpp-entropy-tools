"""Author-side high-precision gate for the corrected round-14 refinement run."""

from __future__ import annotations

import csv
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


def aggregate() -> dict[str, object]:
    rows: list[dict[str, str]] = []
    manifests: list[dict[str, object]] = []
    per_shard: list[dict[str, object]] = []
    for shard in range(4):
        directory = HERE / f"results_{shard}"
        with (directory / "candidate_ledger.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            shard_rows = list(csv.DictReader(handle))
        for row in shard_rows:
            row["_shard"] = str(shard)
        manifest = json.loads(
            (directory / "manifest.json").read_text(encoding="utf-8")
        )
        source_rows = [row for row in shard_rows if int(row["index"]) == -1]
        proposal_rows = [row for row in shard_rows if int(row["index"]) >= 0]
        per_shard.append(
            {
                "shard": shard,
                "ledger_rows": len(shard_rows),
                "source_rows": len(source_rows),
                "proposal_rows": len(proposal_rows),
                "float_candidate_rows": sum(
                    row["status"] == "FLOAT_CANDIDATE" for row in shard_rows
                ),
                "positive_gap_rows": sum(
                    float(row["chord_gap"]) > 0.0 for row in shard_rows
                ),
                "maximum_gap": max(float(row["chord_gap"]) for row in shard_rows),
            }
        )
        rows.extend(shard_rows)
        manifests.append(manifest)
    return {
        "ledger_rows_including_four_source_copies": len(rows),
        "proposal_rows": sum(int(row["index"]) >= 0 for row in rows),
        "source_rows": sum(int(row["index"]) == -1 for row in rows),
        "float_candidate_rows": sum(
            row["status"] == "FLOAT_CANDIDATE" for row in rows
        ),
        "non_no_hit_rows": sum(row["status"] != "NO_HIT" for row in rows),
        "positive_gap_rows": sum(float(row["chord_gap"]) > 0.0 for row in rows),
        "maximum_gap": max(float(row["chord_gap"]) for row in rows),
        "best_row": max(rows, key=lambda row: float(row["rho_psd"])),
        "per_shard": per_shard,
        "manifests": manifests,
    }


def main() -> None:
    started = time.time()
    ledger = aggregate()
    best_row = ledger["best_row"]
    best_shard = int(best_row["_shard"])
    best_path = HERE / f"results_{best_shard}" / "best_case.npz"
    best_json = json.loads(
        (HERE / f"results_{best_shard}" / "best_case.json").read_text(
            encoding="utf-8"
        )
    )
    data = np.load(best_path)
    raw_kernel = np.asarray(data["kernel"], dtype=float)
    raw_direction = np.asarray(data["direction"], dtype=float)
    kernel = (raw_kernel + raw_kernel.T) / 2.0
    direction = (raw_direction + raw_direction.T) / 2.0

    mixed, _ = GATE.mixed_atoms_float(kernel)
    mobius = GATE.mobius_atoms_float(kernel)
    decimal_rows = [
        GATE.decimal_directional(kernel, direction, precision)
        for precision in (50, 80)
    ]
    chord_steps = [str(best_row["chord_step"]), "0.001", "0.0001"]
    chords = GATE.decimal_chords(kernel, direction, chord_steps)
    feasibility = GATE.exact_feasibility(kernel, direction)
    float_row = GATE.directional_float(kernel, direction)

    checks = {
        "four_shards": len(ledger["manifests"]) == 4,
        "each_manifest_has_5000_proposals": all(
            int(m["proposal_count"]) == 5000 for m in ledger["manifests"]
        ),
        "each_ledger_has_5001_rows": all(
            int(m["ledger_rows_including_source"]) == 5001
            for m in ledger["manifests"]
        ) and all(s["ledger_rows"] == 5001 for s in ledger["per_shard"]),
        "one_source_row_per_shard": all(
            s["source_rows"] == 1 for s in ledger["per_shard"]
        ),
        "all_20000_proposals_accounted": ledger["proposal_rows"] == 20000,
        "all_sources_accounted": ledger["source_rows"] == 4,
        "no_candidate_status": ledger["non_no_hit_rows"] == 0,
        "no_positive_gap": ledger["positive_gap_rows"] == 0,
        "manifest_positive_counts_zero": all(
            int(m["positive_count"]) == 0 for m in ledger["manifests"]
        ),
        "best_row_matches_json": (
            int(best_row["index"]) == int(best_json["index"])
            and abs(float(best_row["rho_psd"]) - float(best_json["rho_psd"]))
            < 1e-14
        ),
        "best_rho_below_one": float(best_row["rho_psd"]) < 1.0,
        "decimal_rho_below_one": all(
            Decimal(row["rho"]) < 1 for row in decimal_rows
        ),
        "decimal_H2_negative": all(
            Decimal(row["H2"]) < 0 for row in decimal_rows
        ),
        "all_decimal_chords_negative": all(
            Decimal(row["midpoint_gap"]) < 0 for row in chords
        ),
    }

    report = {
        "status": "HIGH_PRECISION_STABLE_NEGATIVE"
        if all(checks.values())
        else "FAILED_GATE",
        "scope": (
            "20,000 new proposal rows plus four explicitly ledgered source copies; "
            "finite evidence and one strongest-point gate only"
        ),
        "ledger": ledger,
        "strongest_shard": best_shard,
        "strongest_index": int(best_row["index"]),
        "hashes": {
            "source_npz": GATE.sha256(HERE / "source.npz"),
            "best_case_npz": GATE.sha256(best_path),
            "producing_script": GATE.sha256(HERE / "spectral_basis_refine.py"),
        },
        "symmetrization": {
            "kernel_max_asymmetry": float(
                np.max(np.abs(raw_kernel - raw_kernel.T))
            ),
            "direction_max_asymmetry": float(
                np.max(np.abs(raw_direction - raw_direction.T))
            ),
        },
        "spectra_and_commutation": {
            "K_min": float(np.linalg.eigvalsh(kernel)[0]),
            "K_max": float(np.linalg.eigvalsh(kernel)[-1]),
            "D_min": float(np.linalg.eigvalsh(direction)[0]),
            "D_max": float(np.linalg.eigvalsh(direction)[-1]),
            "commutator_frobenius": float(
                np.linalg.norm(kernel @ direction - direction @ kernel)
            ),
        },
        "event_semantics_float": {
            "event_count": len(mixed),
            "sum_p_minus_one": float(mixed.sum() - 1.0),
            "min_probability": float(mixed.min()),
            "mobius_max_abs_difference": float(np.max(np.abs(mixed - mobius))),
        },
        "directional_float": float_row,
        "decimal_directional": decimal_rows,
        "decimal_chords": chords,
        "exact_fraction_feasibility": feasibility,
        "checks": checks,
        "exit_code": 0 if all(checks.values()) else 1,
        "elapsed_seconds": time.time() - started,
    }
    (HERE / "recheck_best_refine2.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["exit_code"]:
        raise SystemExit(report["exit_code"])


if __name__ == "__main__":
    main()
