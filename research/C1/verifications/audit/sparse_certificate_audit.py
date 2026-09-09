#!/usr/bin/env python3
"""Non-author audit of the rational sparse finite-epsilon certificate.

This script does not import the mechanism child's evaluator. It parses the
rerun interval certificate and independently rebuilds the eight probabilities,
first derivatives, Fisher pair block, N, M, alpha, beta, D_M, and the entropy
second derivative sign for representative rational q values in the certified
bracket. The interval certificate supplies the rigorous whole-bracket signs;
these high-precision recomputations are cross-checks, not a replacement for the
outward-rounded certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
from fractions import Fraction
from pathlib import Path

import mpmath as mp

COORDS = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
LAMBDA = Fraction(7, 10)
EPS_EXP = 8
EPS_FRAC = Fraction(1, 10**EPS_EXP)
SQRT_EPS_FRAC = Fraction(1, 10 ** (EPS_EXP // 2))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fstr(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def parse_frac(s: str) -> Fraction:
    return Fraction(str(s).replace("\n", "").replace(" ", ""))


def mpf_frac(x: Fraction) -> mp.mpf:
    return mp.mpf(x.numerator) / mp.mpf(x.denominator)


def nstr(x, digits: int = 50) -> str:
    return mp.nstr(x, digits)


def det3(A):
    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


def cofactor(A, i: int, j: int):
    rows = [r for r in range(3) if r != i]
    cols = [c for c in range(3) if c != j]
    minor = A[rows[0]][cols[0]] * A[rows[1]][cols[1]] - A[rows[0]][cols[1]] * A[rows[1]][cols[0]]
    return (-1 if (i + j) % 2 else 1) * minor


def mmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def mp_matrix(A):
    return mp.matrix(A)


def mat_from_mp(M):
    return [[M[i, j] for j in range(M.cols)] for i in range(M.rows)]


def basis_matrices():
    out = []
    for i, j in COORDS:
        E = [[mp.mpf("0") for _ in range(3)] for __ in range(3)]
        E[i][j] = mp.mpf("1")
        E[j][i] = mp.mpf("1")
        out.append(E)
    return out


BASIS = basis_matrices()


def rational_K(q: Fraction):
    raw = [Fraction(3, 5), Fraction(4, 5), q * SQRT_EPS_FRAC]
    return [
        [
            (EPS_FRAC if i == j else Fraction(0)) + LAMBDA * raw[i] * raw[j]
            for j in range(3)
        ]
        for i in range(3)
    ]


def q_to_K(q: Fraction):
    Kq = rational_K(q)
    return [[mpf_frac(x) for x in row] for row in Kq]


def event_data(K):
    p = []
    J = []
    for mask in range(8):
        M = [[K[i][j] for j in range(3)] for i in range(3)]
        for i in range(3):
            if not ((mask >> i) & 1):
                M[i][i] -= 1
        sign = mp.mpf(-1 if (3 - int(mask).bit_count()) % 2 else 1)
        p.append(sign * det3(M))
        row = []
        for i, j in COORDS:
            deriv = cofactor(M, i, j)
            if i != j:
                deriv += cofactor(M, j, i)
            row.append(sign * deriv)
        J.append(row)
    return p, J


def matrix_leading_minors(A):
    return {
        "minor1": A[0][0],
        "minor2": A[0][0] * A[1][1] - A[0][1] * A[1][0],
        "minor3": det3(A),
    }


def independent_eval(q: Fraction):
    K = q_to_K(q)
    p, J = event_data(K)
    Z = sum(1 / x for x in p)
    signs = [mp.mpf(-1 if (3 - int(mask).bit_count()) % 2 else 1) for mask in range(8)]
    g = [sum(signs[k] * J[k][j] / p[k] for k in range(8)) for j in range(6)]
    Fpair = mp.zeros(6)
    for i in range(6):
        for j in range(6):
            Fpair[i, j] = sum(J[k][i] * J[k][j] / p[k] for k in range(8)) - g[i] * g[j] / Z

    ell12 = mp.log(p[0] * p[3] / (p[1] * p[2]))
    ell13 = mp.log(p[0] * p[5] / (p[1] * p[4]))
    ell23 = mp.log(p[0] * p[6] / (p[2] * p[4]))
    Lambda_val = mp.log(p[7] * p[1] * p[2] * p[4] / (p[0] * p[3] * p[5] * p[6]))
    N = [[-Lambda_val * K[i][j] for j in range(3)] for i in range(3)]
    N[0][0] -= ell23
    N[1][1] -= ell13
    N[2][2] -= ell12
    detN = det3(N)
    adjN = [[cofactor(N, j, i) for j in range(3)] for i in range(3)]
    a_vec = [trace(mmul(adjN, E)) for E in BASIS]

    Htilde = [[mp.mpf("0") for _ in range(6)] for __ in range(6)]
    for i, Ei in enumerate(BASIS):
        for j, Ej in enumerate(BASIS):
            Htilde[i][j] = detN * Fpair[i, j] + trace(mmul(mmul(mmul(adjN, Ei), adjN), Ej))
    h_tilde = mp.lu_solve(mp_matrix(Htilde), mp.matrix(a_vec))
    h_tilde_list = [h_tilde[i] for i in range(6)]
    dalpha_tilde = sum(a_vec[i] * h_tilde_list[i] for i in range(6))

    W = mat_from_mp(mp.inverse(mp_matrix(N)))
    eta = [trace(mmul(W, E)) for E in BASIS]
    G = mp.zeros(6)
    for i, Ei in enumerate(BASIS):
        for j, Ej in enumerate(BASIS):
            G[i, j] = trace(mmul(mmul(mmul(W, Ei), W), Ej))
    M = mp.zeros(6)
    for i in range(6):
        for j in range(6):
            M[i, j] = Fpair[i, j] + detN * G[i, j]
    h_M = mp.lu_solve(M, mp.matrix(eta))
    h_M_list = [h_M[i] for i in range(6)]
    alpha = sum(eta[i] * h_M_list[i] for i in range(6))
    dalpha = detN * alpha
    beta_times_sqrtZ = sum(g[i] * h_M_list[i] for i in range(6))
    beta = beta_times_sqrtZ / mp.sqrt(Z)
    D_M = [x / alpha for x in h_M_list]
    eta_D = sum(eta[i] * D_M[i] for i in range(6))
    Lambda_prime_D = sum(g[i] * D_M[i] for i in range(6))
    negative_entropy_quadratic = 1 / alpha + (beta / alpha) ** 2 - detN
    entropy_second_derivative = -negative_entropy_quadratic

    I_minus_K = [[(mp.mpf(1) if i == j else mp.mpf(0)) - K[i][j] for j in range(3)] for i in range(3)]
    h_diff = max(abs(h_M_list[i] - h_tilde_list[i]) for i in range(6))
    return {
        "q": fstr(q),
        "q_decimal": nstr(mpf_frac(q), 40),
        "kappa_decimal": nstr(mpf_frac(q * q), 40),
        "min_probability": nstr(min(p), 50),
        "Z": nstr(Z, 50),
        "Lambda": nstr(Lambda_val, 50),
        "K_leading_minors": {k: nstr(v, 50) for k, v in matrix_leading_minors(K).items()},
        "I_minus_K_leading_minors": {k: nstr(v, 50) for k, v in matrix_leading_minors(I_minus_K).items()},
        "N_leading_minors": {k: nstr(v, 50) for k, v in matrix_leading_minors(N).items()},
        "detN": nstr(detN, 50),
        "dalpha_via_M": nstr(dalpha, 50),
        "dalpha_via_Htilde": nstr(dalpha_tilde, 50),
        "max_abs_h_difference_between_M_and_Htilde": nstr(h_diff, 30),
        "alpha": nstr(alpha, 50),
        "beta_times_sqrtZ": nstr(beta_times_sqrtZ, 50),
        "beta": nstr(beta, 50),
        "D_M_coords": [nstr(x, 45) for x in D_M],
        "eta_D_M_minus_1": nstr(eta_D - 1, 30),
        "Lambda_prime_D_M": nstr(Lambda_prime_D, 50),
        "negative_entropy_quadratic_D_M": nstr(negative_entropy_quadratic, 50),
        "entropy_second_derivative_D_M": nstr(entropy_second_derivative, 50),
    }


def interval_checks(cert):
    c = cert["certificate"]
    strict = c["strict_reason"]
    left_beta = c["endpoint_left_beta_times_sqrtZ"]
    right_beta = c["endpoint_right_beta_times_sqrtZ"]
    dalpha = c["whole_bracket_dalpha"]
    min_p = c["whole_bracket_min_p"]
    detN = c["whole_bracket_detN"]
    N00 = c["whole_bracket_N00"]
    leading2 = c["whole_bracket_leading2_N"]
    qlo, qhi = [parse_frac(x) for x in c["certified_q_bracket"]]
    max_norm2 = Fraction(1) + qhi * qhi * EPS_FRAC
    max_eigen_upper = EPS_FRAC + LAMBDA * max_norm2
    width = qhi - qlo
    exact = {
        "qlo_positive": qlo > 0,
        "width": fstr(width),
        "width_is_2^-62": width == Fraction(1, 2**62),
        "max_norm2_recomputed": fstr(max_norm2),
        "max_eigen_upper_recomputed": fstr(max_eigen_upper),
        "max_eigen_upper_lt_one_recomputed": max_eigen_upper < 1,
        "left_beta_lower_gt_zero": parse_frac(left_beta["lower"]) > 0,
        "right_beta_upper_lt_zero": parse_frac(right_beta["upper"]) < 0,
        "whole_dalpha_upper_lt_one": parse_frac(dalpha["upper"]) < 1,
        "whole_min_p_lower_gt_zero": parse_frac(min_p["lower"]) > 0,
        "whole_detN_lower_gt_zero": parse_frac(detN["lower"]) > 0,
        "whole_N00_lower_gt_zero": parse_frac(N00["lower"]) > 0,
        "whole_leading2_N_lower_gt_zero": parse_frac(leading2["lower"]) > 0,
        "pivots_exclude_zero": bool(c["pivots_exclude_zero"]),
        "residual_contains_zero": bool(c["residual_contains_zero"]),
        "strict_reason_consistent": (
            bool(strict["epsilon_positive"])
            and bool(strict["max_eigen_upper_lt_one"])
            and bool(strict["connected_for_positive_q"])
            and fstr(max_norm2) == strict["max_norm2"]
            and fstr(max_eigen_upper) == strict["max_eigen_upper"]
        ),
    }
    exact["all_interval_core_checks_pass"] = all(
        exact[k]
        for k in [
            "qlo_positive",
            "width_is_2^-62",
            "max_eigen_upper_lt_one_recomputed",
            "left_beta_lower_gt_zero",
            "right_beta_upper_lt_zero",
            "whole_dalpha_upper_lt_one",
            "whole_min_p_lower_gt_zero",
            "whole_detN_lower_gt_zero",
            "whole_N00_lower_gt_zero",
            "whole_leading2_N_lower_gt_zero",
            "pivots_exclude_zero",
            "residual_contains_zero",
            "strict_reason_consistent",
        ]
    )
    exact["interval_approximations"] = {
        "left_beta_times_sqrtZ": [left_beta["approx_lower"], left_beta["approx_upper"]],
        "right_beta_times_sqrtZ": [right_beta["approx_lower"], right_beta["approx_upper"]],
        "whole_dalpha": [dalpha["approx_lower"], dalpha["approx_upper"]],
        "whole_min_p": [min_p["approx_lower"], min_p["approx_upper"]],
        "whole_detN": [detN["approx_lower"], detN["approx_upper"]],
        "whole_N00": [N00["approx_lower"], N00["approx_upper"]],
        "whole_leading2_N": [leading2["approx_lower"], leading2["approx_upper"]],
    }
    return exact, qlo, qhi


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--mechanism-probe", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--dps", type=int, default=120)
    ns = parser.parse_args()
    mp.mp.dps = ns.dps
    cert_path = Path(ns.certificate)
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    checks, qlo, qhi = interval_checks(cert)
    qmid = (qlo + qhi) / 2
    samples = {
        "left_endpoint": independent_eval(qlo),
        "midpoint": independent_eval(qmid),
        "right_endpoint": independent_eval(qhi),
    }
    high_precision_checks = {
        "left_beta_times_sqrtZ_positive": mp.mpf(samples["left_endpoint"]["beta_times_sqrtZ"]) > 0,
        "right_beta_times_sqrtZ_negative": mp.mpf(samples["right_endpoint"]["beta_times_sqrtZ"]) < 0,
        "midpoint_dalpha_lt_one": mp.mpf(samples["midpoint"]["dalpha_via_M"]) < 1,
        "midpoint_eta_D_M_close_to_one": abs(mp.mpf(samples["midpoint"]["eta_D_M_minus_1"])) < mp.mpf("1e-80"),
        "midpoint_M_and_Htilde_h_match": mp.mpf(samples["midpoint"]["max_abs_h_difference_between_M_and_Htilde"]) < mp.mpf("1e-70"),
        "midpoint_entropy_second_derivative_negative": mp.mpf(samples["midpoint"]["entropy_second_derivative_D_M"]) < 0,
    }
    result = {
        "status": "AUDIT_PASS" if checks["all_interval_core_checks_pass"] and all(high_precision_checks.values()) and cert.get("status") == "CERTIFIED_RATIONAL_SPARSE_ROOT_DALPHA_LT_ONE" else "AUDIT_FAIL",
        "pid": os.getpid(),
        "python": sys.version,
        "platform": platform.platform(),
        "mpmath": mp.__version__,
        "thread_env": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "CUDA_VISIBLE_DEVICES"]},
        "certificate_path": str(cert_path),
        "certificate_sha256": sha256(cert_path),
        "source_sha256_local_copy": sha256(Path(ns.source)),
        "mechanism_probe_sha256_local_copy": sha256(Path(ns.mechanism_probe)),
        "certificate_status": cert.get("status"),
        "certificate_source_sha256_recorded": cert.get("source_sha256"),
        "certificate_mechanism_probe_sha256_recorded": cert.get("mechanism_probe_sha256"),
        "certificate_pid_rerun": cert.get("pid"),
        "finite_epsilon_variant_note": cert.get("finite_epsilon_variant_note"),
        "exact_interval_checks": checks,
        "high_precision_samples": samples,
        "high_precision_checks": high_precision_checks,
        "limitations": [
            "The whole-bracket inequalities come from the rerun outward-rounded interval certificate; the high-precision samples are cross-checks only.",
            "This finite-epsilon rational family is not the unit-normalized sparse family used in the main asymptotic proof; only the stated displayed K is certified.",
            "No claim is made about uniqueness of the beta zero or about the global B0 theorem.",
        ],
    }
    Path(ns.output).parent.mkdir(parents=True, exist_ok=True)
    Path(ns.output).write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"status": result["status"], "pid": result["pid"], "certificate_pid_rerun": result["certificate_pid_rerun"]}, sort_keys=True))
    return 0 if result["status"] == "AUDIT_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
