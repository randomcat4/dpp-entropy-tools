#!/usr/bin/env python3
"""Independent formula audit for the C1 beta-zero slice.

The checks here are deliberately bounded. They rebuild the three-point DPP
objects from the eight atom probabilities and compare equivalent formula
paths. They are not a proof of the universal B0 implication.
"""

from __future__ import annotations

import json
import math
import os
import platform
import sys
from fractions import Fraction

import numpy as np


EVENTS = [
    (0, 0, 0),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
    (1, 1, 1),
]
NAMES = ["0", "1", "2", "3", "12", "13", "23", "123"]
SIGMA = np.array([-1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, 1.0])
COORDS = ["x", "y", "z", "a", "b", "c"]


def K_from_coords(v):
    x, y, z, a, b, c = v
    return np.array([[x, a, b], [a, y, c], [b, c, z]], dtype=float)


def det_minor(K, subset):
    if not subset:
        return 1.0
    M = K[np.ix_(subset, subset)]
    return float(np.linalg.det(M))


def explicit_probs(v):
    x, y, z, a, b, c = v
    q12 = x * y - a * a
    q13 = x * z - b * b
    q23 = y * z - c * c
    r = x * y * z + 2 * a * b * c - x * c * c - y * b * b - z * a * a
    return np.array(
        [
            1 - x - y - z + q12 + q13 + q23 - r,
            x - q12 - q13 + r,
            y - q12 - q23 + r,
            z - q13 - q23 + r,
            q12 - r,
            q13 - r,
            q23 - r,
            r,
        ],
        dtype=float,
    )


def mobius_probs(v):
    K = K_from_coords(v)
    out = []
    all_idx = range(3)
    for event in EVENTS:
        S = [i for i, bit in enumerate(event) if bit]
        rest = [i for i in all_idx if i not in S]
        total = 0.0
        for mask in range(1 << len(rest)):
            T = list(S)
            parity = 0
            for bit, item in enumerate(rest):
                if (mask >> bit) & 1:
                    T.append(item)
                    parity += 1
            total += ((-1.0) ** parity) * det_minor(K, sorted(T))
        out.append(total)
    return np.array(out, dtype=float)


def qr_grad_hess(v):
    x, y, z, a, b, c = v
    grad = {}
    hess = {}

    def zero():
        return np.zeros((6, 6), dtype=float)

    grad["q12"] = np.array([y, x, 0, -2 * a, 0, 0], dtype=float)
    hess["q12"] = zero()
    hess["q12"][0, 1] = hess["q12"][1, 0] = 1
    hess["q12"][3, 3] = -2

    grad["q13"] = np.array([z, 0, x, 0, -2 * b, 0], dtype=float)
    hess["q13"] = zero()
    hess["q13"][0, 2] = hess["q13"][2, 0] = 1
    hess["q13"][4, 4] = -2

    grad["q23"] = np.array([0, z, y, 0, 0, -2 * c], dtype=float)
    hess["q23"] = zero()
    hess["q23"][1, 2] = hess["q23"][2, 1] = 1
    hess["q23"][5, 5] = -2

    grad["r"] = np.array(
        [
            y * z - c * c,
            x * z - b * b,
            x * y - a * a,
            2 * b * c - 2 * z * a,
            2 * a * c - 2 * y * b,
            2 * a * b - 2 * x * c,
        ],
        dtype=float,
    )
    hess["r"] = zero()
    hess["r"][0, 1] = hess["r"][1, 0] = z
    hess["r"][0, 2] = hess["r"][2, 0] = y
    hess["r"][1, 2] = hess["r"][2, 1] = x
    hess["r"][0, 5] = hess["r"][5, 0] = -2 * c
    hess["r"][1, 4] = hess["r"][4, 1] = -2 * b
    hess["r"][2, 3] = hess["r"][3, 2] = -2 * a
    hess["r"][3, 3] = -2 * z
    hess["r"][4, 4] = -2 * y
    hess["r"][5, 5] = -2 * x
    hess["r"][3, 4] = hess["r"][4, 3] = 2 * c
    hess["r"][3, 5] = hess["r"][5, 3] = 2 * b
    hess["r"][4, 5] = hess["r"][5, 4] = 2 * a
    return grad, hess


def p_derivatives(v):
    grad, hess = qr_grad_hess(v)
    dp = np.zeros((8, 6), dtype=float)
    ddp = np.zeros((8, 6, 6), dtype=float)

    dp[0] = np.array([-1, -1, -1, 0, 0, 0], dtype=float) + grad["q12"] + grad["q13"] + grad["q23"] - grad["r"]
    ddp[0] = hess["q12"] + hess["q13"] + hess["q23"] - hess["r"]
    dp[1] = np.array([1, 0, 0, 0, 0, 0], dtype=float) - grad["q12"] - grad["q13"] + grad["r"]
    ddp[1] = -hess["q12"] - hess["q13"] + hess["r"]
    dp[2] = np.array([0, 1, 0, 0, 0, 0], dtype=float) - grad["q12"] - grad["q23"] + grad["r"]
    ddp[2] = -hess["q12"] - hess["q23"] + hess["r"]
    dp[3] = np.array([0, 0, 1, 0, 0, 0], dtype=float) - grad["q13"] - grad["q23"] + grad["r"]
    ddp[3] = -hess["q13"] - hess["q23"] + hess["r"]
    dp[4] = grad["q12"] - grad["r"]
    ddp[4] = hess["q12"] - hess["r"]
    dp[5] = grad["q13"] - grad["r"]
    ddp[5] = hess["q13"] - hess["r"]
    dp[6] = grad["q23"] - grad["r"]
    ddp[6] = hess["q23"] - hess["r"]
    dp[7] = grad["r"]
    ddp[7] = hess["r"]
    return dp, ddp


def finite_diff_dp(v, eps=1e-6):
    out = np.zeros((8, 6), dtype=float)
    for j in range(6):
        e = np.zeros(6)
        e[j] = eps
        out[:, j] = (explicit_probs(v + e) - explicit_probs(v - e)) / (2 * eps)
    return out


def pair_features():
    rows = []
    for e in EVENTS:
        x1, x2, x3 = e
        rows.append([x1, x2, x3, x1 * x2, x1 * x3, x2 * x3])
    return np.array(rows, dtype=float)


def explicit_J_pair(v):
    x, y, z, a, b, c = v
    return np.array(
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [y, x, 0, -2 * a, 0, 0],
            [z, 0, x, 0, -2 * b, 0],
            [0, z, y, 0, 0, -2 * c],
        ],
        dtype=float,
    )


def N_matrix(v, p):
    x, y, z, a, b, c = v
    ell12 = math.log(p[0] * p[4] / (p[1] * p[2]))
    ell13 = math.log(p[0] * p[5] / (p[1] * p[3]))
    ell23 = math.log(p[0] * p[6] / (p[2] * p[3]))
    Lambda = math.log(p[7] * p[1] * p[2] * p[3] / (p[0] * p[4] * p[5] * p[6]))
    K = K_from_coords(v)
    N = -Lambda * K
    N[0, 0] -= ell23
    N[1, 1] -= ell13
    N[2, 2] -= ell12
    return ell12, ell13, ell23, Lambda, N


def basis_matrices():
    mats = []
    for idx in range(6):
        E = np.zeros((3, 3), dtype=float)
        if idx < 3:
            E[idx, idx] = 1.0
        elif idx == 3:
            E[0, 1] = E[1, 0] = 1.0
        elif idx == 4:
            E[0, 2] = E[2, 0] = 1.0
        else:
            E[1, 2] = E[2, 1] = 1.0
        mats.append(E)
    return mats


def matrix_from_coord_vector(v):
    return np.array(
        [
            [v[0], v[3], v[4]],
            [v[3], v[1], v[5]],
            [v[4], v[5], v[2]],
        ],
        dtype=float,
    )


def coord_vector_from_matrix(M):
    return np.array([M[0, 0], M[1, 1], M[2, 2], M[0, 1], M[0, 2], M[1, 2]], dtype=float)


def quantities(v):
    p = explicit_probs(v)
    dp, ddp = p_derivatives(v)
    features = pair_features()
    mean = p @ features
    centered = features - mean
    cov = centered.T @ np.diag(p) @ centered
    J_from_atoms = features.T @ dp
    J_direct = explicit_J_pair(v)

    F = dp.T @ np.diag(1 / p) @ dp
    grad_Lambda = (SIGMA[:, None] * dp / p[:, None]).sum(axis=0)
    Z = float((1 / p).sum())
    vscore = grad_Lambda / math.sqrt(Z)
    Fpair_score = F - np.outer(vscore, vscore)
    Fpair_cov = J_direct.T @ np.linalg.solve(cov, J_direct)

    ell12, ell13, ell23, Lambda, N = N_matrix(v, p)
    Ninv = np.linalg.inv(N)
    detN = float(np.linalg.det(N))
    mats = basis_matrices()
    eta = np.array([np.trace(Ninv @ E) for E in mats])
    G = np.array([[np.trace(Ninv @ Ei @ Ninv @ Ej) for Ej in mats] for Ei in mats])
    C_from_probs = np.tensordot(np.log(p), ddp, axes=(0, 0))
    C_from_N = detN * G - detN * np.outer(eta, eta)
    B_from_probs = F + C_from_probs
    B_from_N = F + C_from_N
    M = Fpair_score + detN * G
    Minv_eta = np.linalg.solve(M, eta)
    Minv_v = np.linalg.solve(M, vscore)
    alpha = float(eta @ Minv_eta)
    beta = float(vscore @ Minv_eta)
    gamma = float(vscore @ Minv_v)
    D_M = Minv_eta / alpha

    return {
        "p": p,
        "dp": dp,
        "ddp": ddp,
        "cov": cov,
        "J_from_atoms": J_from_atoms,
        "J_direct": J_direct,
        "F": F,
        "grad_Lambda": grad_Lambda,
        "Z": Z,
        "vscore": vscore,
        "Fpair_score": Fpair_score,
        "Fpair_cov": Fpair_cov,
        "ells": (ell12, ell13, ell23),
        "Lambda": Lambda,
        "N": N,
        "Ninv": Ninv,
        "detN": detN,
        "eta": eta,
        "G": G,
        "C_from_probs": C_from_probs,
        "C_from_N": C_from_N,
        "B_from_probs": B_from_probs,
        "B_from_N": B_from_N,
        "M": M,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "D_M": D_M,
    }


def strict(v):
    K = K_from_coords(v)
    return bool(float(np.min(np.linalg.eigvalsh(K))) > 0 and float(np.min(np.linalg.eigvalsh(np.eye(3) - K))) > 0)


def connected(v):
    return bool(sum(bool(abs(v[i]) > 1e-14) for i in [3, 4, 5]) >= 2)


def principal_rayleigh(v):
    x, y, z, a, b, c = v
    u = a * a
    vv = b * b
    w = c * c
    T = 2 * a * b * c
    pairs = [
        ("12|3", a, z, b, c),
        ("13|2", b, y, a, c),
        ("23|1", c, x, a, b),
    ]
    squares = []
    for name, kij, kkk, kik, kjk in pairs:
        const = kij * kkk - kik * kjk
        squares.append(
            {
                "pair": name,
                "quadratic_coefficients": [float(kij * kij), float(2 * kij * const), float(const * const)],
                "discriminant": float((2 * kij * const) ** 2 - 4 * (kij * kij) * (const * const)),
                "leading_is_zero": bool(abs(kij) < 1e-14),
            }
        )
    return {
        "T2_minus_4uvw": float(T * T - 4 * u * vv * w),
        "has_zero_edge": bool(abs(a) < 1e-14 or abs(b) < 1e-14 or abs(c) < 1e-14),
        "squares": squares,
    }


def root_segment_midpoint():
    A = np.array(
        [
            [Fraction(37, 700), Fraction(3, 35), Fraction(9, 70)],
            [Fraction(3, 35), Fraction(127, 700), Fraction(9, 35)],
            [Fraction(9, 70), Fraction(9, 35), Fraction(277, 700)],
        ],
        dtype=object,
    )
    S = np.diag([Fraction(-1), Fraction(1), Fraction(1)]).astype(object)
    B = S @ (np.eye(3, dtype=object) - A) @ S
    L = Fraction(39791754487, 17592186044416)
    U = Fraction(79583508975, 35184372088832)
    t = (L + U) / 2
    K = (1 - t) * A + t * B
    return np.array([float(K[0, 0]), float(K[1, 1]), float(K[2, 2]), float(K[0, 1]), float(K[0, 2]), float(K[1, 2])])


def sample_vectors():
    return [
        ("generic_connected", np.array([0.40, 0.45, 0.52, 0.035, -0.045, 0.055])),
        ("zero_edge_connected", np.array([0.40, 0.45, 0.50, 0.0, 0.080, -0.070])),
        ("near_certified_beta_root_midpoint", root_segment_midpoint()),
    ]


def audit_sample(name, v):
    q = quantities(v)
    p = q["p"]
    fd = finite_diff_dp(v)
    offdiag_eta_expected = np.array([2 * q["Ninv"][0, 1], 2 * q["Ninv"][0, 2], 2 * q["Ninv"][1, 2]])
    offdiag_eta_seen = q["eta"][3:6]
    D_M = q["D_M"]
    alpha = q["alpha"]
    beta = q["beta"]
    M = q["M"]
    eta = q["eta"]
    vscore = q["vscore"]
    K = K_from_coords(v)
    hvec = np.linalg.solve(M, eta)
    hmat = matrix_from_coord_vector(hvec)
    W = q["Ninv"]
    R = W @ hmat @ W
    tilt_left = np.diag(2 * hmat + q["detN"] * (K @ R + R @ K - 2 * K @ R @ K))
    tilt_right = np.diag(K @ W + W @ K - 2 * K @ W @ K)
    tilt_lambda = []
    tilt_mixed = []
    for i in range(3):
        A = np.zeros((3, 3), dtype=float)
        A[i, i] = 1.0
        Q_A = A @ K + K @ A - 2 * K @ A @ K
        qavec = coord_vector_from_matrix(Q_A)
        tilt_lambda.append(float(q["grad_Lambda"] @ qavec))
        tilt_mixed.append(float(qavec @ q["Fpair_score"] @ hvec - 2 * hmat[i, i]))
    return {
        "name": name,
        "strict_0_less_K_less_I": strict(v),
        "connected_graph": connected(v),
        "coords": dict(zip(COORDS, [float(x) for x in v])),
        "min_atom_probability": float(np.min(p)),
        "explicit_vs_mobius_prob_max_abs": float(np.max(np.abs(p - mobius_probs(v)))),
        "analytic_vs_centered_finite_dp_max_abs": float(np.max(np.abs(q["dp"] - fd))),
        "offdiag_eta_factor_two_max_abs": float(np.max(np.abs(offdiag_eta_seen - offdiag_eta_expected))),
        "cov_min_eigenvalue": float(np.min(np.linalg.eigvalsh(q["cov"]))),
        "J_rank": int(np.linalg.matrix_rank(q["J_direct"], tol=1e-10)),
        "J_det": float(np.linalg.det(q["J_direct"])),
        "J_atoms_vs_direct_max_abs": float(np.max(np.abs(q["J_from_atoms"] - q["J_direct"]))),
        "Fpair_score_vs_cov_max_abs": float(np.max(np.abs(q["Fpair_score"] - q["Fpair_cov"]))),
        "B_prob_second_derivative_vs_N_formula_max_abs": float(np.max(np.abs(q["B_from_probs"] - q["B_from_N"]))),
        "N_min_eigenvalue": float(np.min(np.linalg.eigvalsh(q["N"]))),
        "M_min_eigenvalue": float(np.min(np.linalg.eigvalsh(M))),
        "Fpair_min_eigenvalue": float(np.min(np.linalg.eigvalsh(q["Fpair_score"]))),
        "ell12_ell13_ell23": [float(x) for x in q["ells"]],
        "Lambda": float(q["Lambda"]),
        "ell_plus_Lambda": [float(x + q["Lambda"]) for x in q["ells"]],
        "detN": float(q["detN"]),
        "alpha": alpha,
        "beta": beta,
        "gamma": q["gamma"],
        "detN_alpha": float(q["detN"] * alpha),
        "D_M_eta": float(eta @ D_M),
        "D_M_M_quadratic": float(D_M @ M @ D_M),
        "D_M_1_over_alpha": float(1 / alpha),
        "D_M_vscore": float(vscore @ D_M),
        "beta_over_alpha": float(beta / alpha),
        "D_M_lambda_prime": float(q["grad_Lambda"] @ D_M),
        "beta_relation_error": float(abs(vscore @ D_M - beta / alpha)),
        "tilt_T_diag_residual_max_abs": float(np.max(np.abs(tilt_left - tilt_right))),
        "tilt_Lambda_prime_max_abs": float(np.max(np.abs(tilt_lambda))),
        "tilt_Fpair_mixed_identity_max_abs": float(np.max(np.abs(tilt_mixed))),
        "rayleigh": principal_rayleigh(v),
    }


def positivity_regime_check():
    """Numerical examples for the three algebraic N>0 regimes.

    The proof is written in the report. This only records representative
    reconstructed matrices, including a connected zero-edge sample where J
    drops rank.
    """
    rows = []
    for name, v in sample_vectors():
        q = quantities(v)
        rows.append(
            {
                "name": name,
                "Lambda": float(q["Lambda"]),
                "N_min_eigenvalue": float(np.min(np.linalg.eigvalsh(q["N"]))),
                "diag_minus_ell": [float(-x) for x in q["ells"]],
                "diag_minus_ell_minus_Lambda": [float(-x - q["Lambda"]) for x in q["ells"]],
            }
        )
    return rows


def main():
    np.set_printoptions(precision=17, suppress=False)
    samples = [audit_sample(name, v) for name, v in sample_vectors()]
    tolerances = {
        "explicit_vs_mobius_prob_max_abs": 1e-12,
        "analytic_vs_centered_finite_dp_max_abs": 5e-10,
        "offdiag_eta_factor_two_max_abs": 1e-12,
        "J_atoms_vs_direct_max_abs": 1e-12,
        "Fpair_score_vs_cov_max_abs": 1e-10,
        "B_prob_second_derivative_vs_N_formula_max_abs": 1e-10,
        "beta_relation_error": 1e-12,
        "tilt_T_diag_residual_max_abs": 1e-10,
        "tilt_Lambda_prime_max_abs": 1e-10,
        "tilt_Fpair_mixed_identity_max_abs": 1e-10,
    }
    pass_checks = []
    for sample in samples:
        pass_checks.extend([sample["strict_0_less_K_less_I"], sample["connected_graph"]])
        pass_checks.extend(sample[k] <= tol for k, tol in tolerances.items())
        pass_checks.extend(
            [
                sample["min_atom_probability"] > 0,
                sample["cov_min_eigenvalue"] > 0,
                sample["N_min_eigenvalue"] > 0,
                sample["M_min_eigenvalue"] > 0,
                bool(abs(sample["rayleigh"]["T2_minus_4uvw"]) <= 1e-18),
                bool(all(abs(row["discriminant"]) <= 1e-15 for row in sample["rayleigh"]["squares"])),
            ]
        )
    pass_checks.append(bool(any(sample["rayleigh"]["has_zero_edge"] and sample["J_rank"] < 6 for sample in samples)))

    result = {
        "status": "PASS" if all(pass_checks) else "FAIL",
        "pid": os.getpid(),
        "exit_status_if_printed": 0 if all(pass_checks) else 1,
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "thread_env": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "samples": samples,
        "positivity_regime_numeric_record": positivity_regime_check(),
        "non_coverage": [
            "Bounded deterministic formula audit only.",
            "No universal proof of beta=0 implies det(N)*alpha<=1.",
            "No certified beta-zero violation and no entropy chord certificate.",
            "No Lean or interval global proof.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result["exit_status_if_printed"]


if __name__ == "__main__":
    raise SystemExit(main())
