"""Contract the H10 strongest spectrum toward one half to margin 0.12."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
H10 = ROOT / "results_server_round18_boundary1"
MODULE_PATH = H10 / "spectral_basis_refine.py"
SPEC = importlib.util.spec_from_file_location("round18_refine", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load refinement module")
REFINE = importlib.util.module_from_spec(SPEC)
sys.path.insert(0, str(H10))
SPEC.loader.exec_module(REFINE)


def main() -> None:
    target_margin = 0.12
    source_path = H10 / "results_2" / "best_case.npz"
    source = np.load(source_path)
    basis = np.asarray(source["eigenvectors"], dtype=float)
    spectrum = np.asarray(source["spectrum"], dtype=float)
    max_deviation = float(np.max(np.abs(spectrum - 0.5)))
    scale = (0.5 - target_margin) / max_deviation
    interior_spectrum = 0.5 + scale * (spectrum - 0.5)
    rng = np.random.default_rng(2026090874)
    metrics, kernel, direction, rates = REFINE.evaluate(
        basis, interior_spectrum, rng, chunk=32, step_fraction=0.2
    )
    out_npz = HERE / "interior_source_margin012.npz"
    np.savez_compressed(
        out_npz,
        kernel=kernel,
        direction=direction,
        spectrum=interior_spectrum,
        rates=rates,
        eigenvectors=basis,
    )
    report = {
        "status": "AUTHOR_INTERIOR_SOURCE",
        "construction": "affine spectral contraction toward 1/2",
        "seed": 2026090874,
        "target_margin": target_margin,
        "scale": scale,
        "source_spectrum_margin": float(
            np.min(np.minimum(spectrum, 1.0 - spectrum))
        ),
        "interior_spectrum_margin": float(
            np.min(np.minimum(interior_spectrum, 1.0 - interior_spectrum))
        ),
        "metrics": metrics,
        "output": out_npz.name,
    }
    (HERE / "interior_source_margin012.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
