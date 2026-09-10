#!/usr/bin/env python3
"""Independent exact audit of the fresh PR136 full production output."""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import independent_audit as audit


ROOT = Path(__file__).parent
CERT = ROOT / "certificate"
FRESH = ROOT / "fresh_full_128.tsv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def overlaps(left, right) -> bool:
    return max(left[0], right[0]) <= min(left[1], right[1])


def main() -> None:
    started = time.perf_counter()
    inputs = json.loads((CERT / "certificate_inputs.json").read_text(encoding="utf-8"))
    cosines, pi_interval = audit.verify_inputs(inputs)
    fresh_rows = audit.parse_rows(FRESH.read_bytes())
    saved_bytes = b"".join((CERT / f"node_output.part{i}.tsv").read_bytes() for i in range(4))
    saved_rows = audit.parse_rows(saved_bytes)

    overlap_checks = 0
    for node in range(128):
        assert overlaps(fresh_rows[node]["curvature"], saved_rows[node]["curvature"])
        overlap_checks += 1
        fresh_norm = fresh_rows[node]["normalization"]
        saved_norm = saved_rows[node]["normalization"]
        for index in range(0, len(fresh_norm), 2):
            assert overlaps(fresh_norm[index:index + 2], saved_norm[index:index + 2])
            overlap_checks += 1

    polynomial, tail = audit.reconstruct_tail()
    assert tail < F(115, 1_000_000)
    m_exact, interpolation, cells = audit.dct_gate(fresh_rows, cosines, tail)
    assert all(F(cell["true_upper"]) < -F(1, 3000) for cell in cells)

    record = {
        "schema": "pr136-s2-independent-fresh-finite-audit-v1",
        "status": "FRESH_FULL_FINITE_EVIDENCE_PASS",
        "frozen_head": "39098dac760cea2d27f2955bed31f80c87913810",
        "fresh_output": {
            "path": FRESH.name,
            "sha256": sha256(FRESH),
            "bytes": FRESH.stat().st_size,
            "unique_ids": len(fresh_rows),
            "future_words_each": 4**9,
            "current_future_atoms_each": 4**10,
            "normalization_jets_all_enclose": True,
        },
        "independent_input_verification": {
            "nodes": len(inputs["nodes"]),
            "cosine_enclosures": len(cosines),
            "pi_interval": [str(value) for value in pi_interval],
            "log2_enclosed": True,
            "chebyshev_nodes_enclosed": True,
        },
        "saved_fresh_interval_overlap_checks": overlap_checks,
        "tail": {
            "polynomial_coefficients_a0_a1_a2": [str(value) for value in polynomial],
            "E9": str(tail),
            "E9_decimal": float(tail),
            "E9_lt_115e_minus_6": True,
        },
        "continuum": {
            "M_exact": str(m_exact),
            "M_lt_40000000": m_exact < 40_000_000,
            "interpolation_error": str(interpolation),
            "cells": cells,
        },
        "static_kernel_checks": audit.static_kernel_checks(),
        "elapsed_seconds": time.perf_counter() - started,
    }
    output = ROOT / "independent_fresh_audit.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": record["status"],
        "output": str(output),
        "elapsed_seconds": record["elapsed_seconds"],
        "true_uppers": [cell["true_upper_decimal"] for cell in cells],
        "overlap_checks": overlap_checks,
    }))


if __name__ == "__main__":
    main()
