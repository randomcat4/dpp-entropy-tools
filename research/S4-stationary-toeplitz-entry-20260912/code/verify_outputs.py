#!/usr/bin/env python3
"""Bounded consistency checks for the committed exploratory outputs."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

from finite_dpp import complete_shannon_hessian, toeplitz_from_coefficients


def rows(path):
    return list(csv.DictReader(path.open(encoding="utf-8")))


def complex_coeffs(pairs):
    return np.array([a + 1j * b for a, b in pairs])


def main():
    p = argparse.ArgumentParser(); p.add_argument("--package", type=Path, required=True); args = p.parse_args()
    out = args.package / "outputs"
    assert len(rows(out / "transition_spectrum.csv")) == 3 * 4 * 17 * 5
    assert len(rows(out / "transition_fit.csv")) == 3 * (4 * 5 - 3)
    assert len(rows(out / "curvature_vs_transition.csv")) == 3 * 4 * 21 * 5
    assert len(rows(out / "extended_curvature.csv")) == 25 + 3 * 23
    assert len(rows(out / "toeplitz_distance.csv")) == 3
    assert len(rows(out / "sr_hessian_landscape.csv")) == 3 * 15 * 15

    fits = rows(out / "transition_fit.csv")
    selected = [r for r in fits if float(r["epsilon"]) == 0.002 and float(r["delta"]) == 0.05]
    assert len(selected) == 3
    for r in selected:
        a = float(r["linear_plus_log_linear_coefficient"])
        measure = float(r["symbol_half_level_measure"])
        assert abs(a - measure) <= 0.1 * measure
        assert float(r["linear_plus_log_max_abs_residual"]) < float(r["max_abs_residual"])

    c2 = json.loads((out / "c2_search_nondegenerate.json").read_text())
    assert len(c2["cases"]) == 4 and c2["positive_hits"] == c2["certified_hits"] == 0
    for case in c2["cases"]:
        assert case["optimizer_success"] is False
        assert "Maximum number of iterations" in case["optimizer_message"]
        assert case["decoded_base_fourier_amplitude_fraction_lower_bound"] == 0.245
        c = complex_coeffs(case["base_symbol"]["coefficients_re_im"])
        d = complex_coeffs(case["direction_symbol"]["coefficients_re_im"])
        K = toeplitz_from_coefficients(case["base_symbol"]["c0"], c, case["n"])
        G = toeplitz_from_coefficients(case["direction_symbol"]["d0"], d, case["n"])
        h = complete_shannon_hessian(K, G)
        assert abs(h.hessian - case["maximum_hessian"]) < 2e-13
        cert = case["base_whole_circle_certificate"]
        assert cert["certified_lower"] > 0 and cert["certified_upper"] < 1
        assert case["certified_local_chord_radius_from_bounds"] > 0
        if case["class"] == "even_f_odd_g":
            assert case["max_complete_event_first_jet"] == 0

    source = args.package / "code" / "upstream_nonsmooth_interval_probe.py"
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest == "f3f49dd0ed382df7dba1d6eb849fac607023b1de5e21f9679c03f52323fc1b30"
    print(json.dumps({"status": "PASS", "checked_c2_cases": 4, "source_sha256": digest}, indent=2))


if __name__ == "__main__": main()
