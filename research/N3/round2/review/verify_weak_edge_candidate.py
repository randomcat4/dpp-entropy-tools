#!/usr/bin/env python3
"""Non-author checks for the fixed dense weak-edge beta candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np

import verify_round2_definitions as base


TARGET_COMMIT = "3087eb189237ec0a2d60127d0c35128f0cbcd91c"
TARGET_PATH = "research/N3/round2/main/dense_weak_edge_beta_v1.md"


def git_blob(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{TARGET_COMMIT}:{path}"], text=True).strip()


def edge_kernel(xs: list[Q], edges: list[Q], t: Q) -> list[list[Q]]:
    x1, x2, x3 = xs
    a, b, c = edges
    return base.mat_from_coords([x1, x2, x3, t * a, t * b, t * c])


def mu_prob(xs: list[Q], S: tuple[int, ...]) -> Q:
    total = Q(1)
    Sset = set(S)
    for i, x in enumerate(xs):
        total *= x if i in Sset else 1 - x
    return total


def chi(xs: list[Q], S: tuple[int, ...], i: int) -> Q:
    x = xs[i]
    s = x * (1 - x)
    return ((1 if i in S else 0) - x) / s


def density_formula(xs: list[Q], edges: list[Q], t: Q, S: tuple[int, ...]) -> Q:
    a, b, c = edges
    chi1, chi2, chi3 = [chi(xs, S, i) for i in range(3)]
    return 1 - t * t * (a * a * chi1 * chi2 + b * b * chi1 * chi3 + c * c * chi2 * chi3) + 2 * t**3 * a * b * c * chi1 * chi2 * chi3


def density_checks(xs: list[Q], edges: list[Q], t: Q) -> dict[str, object]:
    K = edge_kernel(xs, edges, t)
    p = base.events(K)
    ratios = []
    ok = []
    for S in base.SUBSETS:
        mu = mu_prob(xs, S)
        formula = density_formula(xs, edges, t, S)
        ratios.append(str(p[S] / mu))
        ok.append(p[S] == mu * formula)
    variables = base.principal_variables(K)
    return {
        "t": str(t),
        "all_p_over_mu_identities_exact": all(ok),
        "p_over_mu": ratios,
        "T2_equals_4uvw": variables["T"] * variables["T"] == 4 * variables["u"] * variables["v"] * variables["w"],
        "u_v_w_T": [str(variables[key]) for key in ["u", "v", "w", "T"]],
    }


def matrices_for_K(K: list[list[Q]]) -> dict[str, object]:
    p, F = base.fisher_matrix(K)
    lam_grad, Z_exact, v_score = base.lambda_gradient(K)
    F_pair = F - np.outer(v_score, v_score)
    _, N = base.logs_and_N(K)
    N_inv = np.linalg.inv(N)
    det_N = float(np.linalg.det(N))
    basis = base.basis_matrices_float()
    eta = np.array([float(np.trace(N_inv @ E)) for E in basis], dtype=float)
    G = np.array([[float(np.trace(N_inv @ Ei @ N_inv @ Ej)) for Ej in basis] for Ei in basis], dtype=float)
    H = F_pair + det_N * G
    h = np.linalg.solve(H, eta)
    H_inv_v = np.linalg.solve(H, v_score)
    alpha = float(eta @ h)
    beta = float(v_score @ h)
    gamma = float(v_score @ H_inv_v)
    return {
        "F": F,
        "F_pair": F_pair,
        "v_score": v_score,
        "lambda_grad": lam_grad,
        "Z": float(Z_exact),
        "N": N,
        "N_inv": N_inv,
        "det_N": det_N,
        "eta": eta,
        "G": G,
        "H": H,
        "h": h,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
    }


def block_norms(M: np.ndarray) -> dict[str, float]:
    return {
        "dd": float(np.max(np.abs(M[:3, :3]))),
        "do": float(np.max(np.abs(M[:3, 3:]))),
        "oo": float(np.max(np.abs(M[3:, 3:]))),
    }


def asymptotic_probe(xs: list[Q], edges: list[Q], t: Q) -> dict[str, object]:
    K = edge_kernel(xs, edges, t)
    q = matrices_for_K(K)
    tf = float(t)
    s = [float(x * (1 - x)) for x in xs]
    a, b, c = [float(e) for e in edges]
    S = s[0] * s[1] * s[2]
    Fdd0 = np.diag([1 / s[i] for i in range(3)])
    Foo0 = np.diag([4 * a * a / (s[0] * s[1]), 4 * b * b / (s[0] * s[2]), 4 * c * c / (s[1] * s[2])])
    Hoo0 = np.diag([6 * a * a / (s[0] * s[1]), 6 * b * b / (s[0] * s[2]), 6 * c * c / (s[1] * s[2])])
    grad_o0 = np.array([2 * b * c / S, 2 * a * c / S, 2 * a * b / S], dtype=float)
    eta_o0 = np.array([4 * a * a * s[2] / (b * c), 4 * b * b * s[1] / (a * c), 4 * c * c * s[0] / (a * b)], dtype=float)
    h_o0 = np.array([2 * S / (3 * b * c), 2 * S / (3 * a * c), 2 * S / (3 * a * b)], dtype=float)
    beta0 = 4 * math.sqrt(S)
    det_alpha_coeff = (
        a * a * b * b / (s[0] * c * c)
        + a * a * c * c / (s[1] * b * b)
        + b * b * c * c / (s[2] * a * a)
    )

    F = q["F"]
    F_pair = q["F_pair"]
    H = q["H"]
    eta = q["eta"]
    h = q["h"]
    lam = q["lambda_grad"]
    residual = H @ h - eta

    eta_off_factor_error = max(
        abs(eta[3] - 2 * q["N_inv"][0, 1]),
        abs(eta[4] - 2 * q["N_inv"][0, 2]),
        abs(eta[5] - 2 * q["N_inv"][1, 2]),
    )

    return {
        "t": str(t),
        "strict_K": base.strict_by_leading_minors(K),
        "beta": q["beta"],
        "beta_limit": beta0,
        "beta_minus_limit_over_t": (q["beta"] - beta0) / tf,
        "beta_positive": q["beta"] > 0,
        "detN_alpha": q["det_N"] * q["alpha"],
        "detN_alpha_over_t2": q["det_N"] * q["alpha"] / (tf * tf),
        "detN_alpha_coeff": det_alpha_coeff,
        "detN_alpha_coeff_error_over_t": (q["det_N"] * q["alpha"] / (tf * tf) - det_alpha_coeff) / tf,
        "Fdd_error_over_t2": float(np.max(np.abs(F[:3, :3] - Fdd0))) / (tf * tf),
        "Fdo_norm_over_t3": float(np.max(np.abs(F[:3, 3:]))) / (tf**3),
        "Foo_leading_error_over_t4": float(np.max(np.abs(F[3:, 3:] - tf * tf * Foo0))) / (tf**4),
        "Fpair_do_norm_over_t3": float(np.max(np.abs(F_pair[:3, 3:]))) / (tf**3),
        "Hdo_norm_over_t3": float(np.max(np.abs(H[:3, 3:]))) / (tf**3),
        "Hoo_leading_error_over_t3": float(np.max(np.abs(H[3:, 3:] - tf * tf * Hoo0))) / (tf**3),
        "lambda_grad_o_over_t2": (lam[3:] / (tf * tf)).tolist(),
        "lambda_grad_o_limit": grad_o0.tolist(),
        "lambda_grad_o_error_over_t": (np.max(np.abs(lam[3:] / (tf * tf) - grad_o0)) / tf).item(),
        "eta_off": eta[3:].tolist(),
        "eta_off_limit": eta_o0.tolist(),
        "eta_off_error_over_t": (np.max(np.abs(eta[3:] - eta_o0)) / tf).item(),
        "eta_off_factor2_error": eta_off_factor_error,
        "h_off_t2": (h[3:] * tf * tf).tolist(),
        "h_off_t2_limit": h_o0.tolist(),
        "h_off_t2_error_over_t": (np.max(np.abs(h[3:] * tf * tf - h_o0)) / tf).item(),
        "H_solve_residual_max_abs": float(np.max(np.abs(residual))),
        "blocks": {"F": block_norms(F), "F_pair": block_norms(F_pair), "H": block_norms(H)},
    }


def case_checks() -> list[dict[str, object]]:
    cases = [
        {
            "name": "abc_positive",
            "xs": [Q(2, 5), Q(3, 7), Q(4, 9)],
            "edges": [Q(1, 3), Q(1, 5), Q(2, 7)],
        },
        {
            "name": "abc_negative",
            "xs": [Q(5, 12), Q(7, 15), Q(3, 8)],
            "edges": [Q(1, 4), Q(-2, 9), Q(1, 6)],
        },
    ]
    out = []
    for case in cases:
        xs = case["xs"]
        edges = case["edges"]
        probes = [asymptotic_probe(xs, edges, Q(1, den)) for den in [100, 200, 400]]
        density = density_checks(xs, edges, Q(1, 100))
        out.append(
            {
                "name": case["name"],
                "xs": [str(x) for x in xs],
                "edges": [str(e) for e in edges],
                "abc_sign": "positive" if edges[0] * edges[1] * edges[2] > 0 else "negative",
                "density_check": density,
                "probes": probes,
                "all_beta_positive": all(p["beta_positive"] for p in probes),
                "detN_alpha_smallest_t_less_than_one": probes[-1]["detN_alpha"] < 1.0,
                "Fdo_order_ratio_bounded": max(p["Fdo_norm_over_t3"] for p in probes) < 1e5,
                "Hdo_order_ratio_bounded": max(p["Hdo_norm_over_t3"] for p in probes) < 1e5,
                "eta_off_factor2_ok": max(p["eta_off_factor2_error"] for p in probes) < 1e-12,
                "solve_residual_ok": max(p["H_solve_residual_max_abs"] for p in probes) < 1e-8,
            }
        )
    return out


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def jsonable(value):
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [jsonable(v) for v in value]
    if isinstance(value, tuple):
        return [jsonable(v) for v in value]
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="research/N3/round2/review/weak_edge_audit_results.json")
    ns = parser.parse_args()

    cases = case_checks()
    pass_checks = []
    for case in cases:
        pass_checks.extend(
            [
                case["density_check"]["all_p_over_mu_identities_exact"],
                case["density_check"]["T2_equals_4uvw"],
                case["all_beta_positive"],
                case["detN_alpha_smallest_t_less_than_one"],
                case["Fdo_order_ratio_bounded"],
                case["Hdo_order_ratio_bounded"],
                case["eta_off_factor2_ok"],
                case["solve_residual_ok"],
            ]
        )
        for probe in case["probes"]:
            pass_checks.extend(
                [
                    probe["strict_K"],
                    abs(probe["beta_minus_limit_over_t"]) < 50,
                    abs(probe["detN_alpha_coeff_error_over_t"]) < 1e4,
                    probe["Fdd_error_over_t2"] < 1e4,
                    probe["Foo_leading_error_over_t4"] < 1e7,
                    probe["lambda_grad_o_error_over_t"] < 1e5,
                    probe["eta_off_error_over_t"] < 1e5,
                    probe["h_off_t2_error_over_t"] < 1e5,
                ]
            )

    script_path = Path(__file__).resolve()
    result = {
        "status": "PASS" if all(pass_checks) else "FAIL",
        "purpose": "Non-author bounded audit of fixed dense weak-edge beta asymptotic candidate.",
        "target_commit": TARGET_COMMIT,
        "target_blob": git_blob(TARGET_PATH),
        "script": str(script_path),
        "script_sha256": sha256_file(script_path),
        "base_script": str(Path(base.__file__).resolve()),
        "base_script_sha256": sha256_file(Path(base.__file__).resolve()),
        "argv": sys.argv,
        "pid": os.getpid(),
        "cwd": os.getcwd(),
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "env_threads": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "cases": cases,
        "coverage": {
            "fixed_candidate_objects": 1,
            "sign_branches": 2,
            "exact_density_checks": 2,
            "asymptotic_probe_points": 6,
            "t_values": ["1/100", "1/200", "1/400"],
        },
        "non_coverage": [
            "No uniformity as means or edge constants degenerate.",
            "No zero-edge coverage for the weak-edge candidate, which assumes fixed nonzero a,b,c.",
            "No proof of beta-zero implication B0 or global rho<=1.",
            "No audit of any later beta-zero root certificate.",
        ],
    }

    output = Path(ns.output)
    output.write_text(json.dumps(jsonable(result), indent=2, sort_keys=True), encoding="utf-8")
    print(f"STATUS {result['status']}")
    print(f"wrote {output}")
    print(f"pid {result['pid']}")
    print(f"target {TARGET_COMMIT}")
    print(f"coverage {json.dumps(result['coverage'], sort_keys=True)}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
