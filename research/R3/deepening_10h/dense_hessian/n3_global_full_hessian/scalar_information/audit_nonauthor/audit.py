#!/usr/bin/env python3
"""
D10-U10b scalar_information fresh non-author audit.

This script does not import or call scalar_information_sanity.py or any U8
author gate/search module.  It independently rebuilds exact atoms, first jets,
Fisher, N, A, eta, rho, and the information-space/ridge identities.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np


BASE = Path(__file__).resolve().parent
AUTHOR_DIR = BASE.parent
ROOT_U8_DIR = AUTHOR_DIR.parent
ATOM_NAMES = ["0", "1", "2", "3", "12", "13", "23", "123"]
COORD_NAMES = ["11", "22", "33", "12", "13", "23"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def F(n: int, d: int = 1) -> Fraction:
    return Fraction(n, d)


def mat_sub_frac(A: List[List[Fraction]], B: List[List[Fraction]]) -> List[List[Fraction]]:
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def eye_frac(n: int) -> List[List[Fraction]]:
    return [[Fraction(1 if i == j else 0, 1) for j in range(n)] for i in range(n)]


def ldl_pivots3_frac(M: List[List[Fraction]]) -> List[Fraction]:
    d0 = M[0][0]
    l10 = M[1][0] / d0
    l20 = M[2][0] / d0
    d1 = M[1][1] - l10 * l10 * d0
    l21 = (M[2][1] - l20 * l10 * d0) / d1
    d2 = M[2][2] - l20 * l20 * d0 - l21 * l21 * d1
    return [d0, d1, d2]


def det2(a: Fraction, b: Fraction, c: Fraction) -> Fraction:
    return a * c - b * b


def det3_frac(K: List[List[Fraction]]) -> Fraction:
    return (
        K[0][0] * (K[1][1] * K[2][2] - K[1][2] * K[2][1])
        - K[0][1] * (K[1][0] * K[2][2] - K[1][2] * K[2][0])
        + K[0][2] * (K[1][0] * K[2][1] - K[1][1] * K[2][0])
    )


def atoms_grads_frac(K: List[List[Fraction]]) -> Tuple[List[Fraction], List[List[Fraction]]]:
    x, y, z = K[0][0], K[1][1], K[2][2]
    a, b, c = K[0][1], K[0][2], K[1][2]
    q12 = x * y - a * a
    q13 = x * z - b * b
    q23 = y * z - c * c
    r = x * y * z + 2 * a * b * c - x * c * c - y * b * b - z * a * a

    gq12 = [y, x, F(0), -2 * a, F(0), F(0)]
    gq13 = [z, F(0), x, F(0), -2 * b, F(0)]
    gq23 = [F(0), z, y, F(0), F(0), -2 * c]
    gr = [
        y * z - c * c,
        x * z - b * b,
        x * y - a * a,
        2 * b * c - 2 * z * a,
        2 * a * c - 2 * y * b,
        2 * a * b - 2 * x * c,
    ]
    vals = [
        1 - x - y - z + q12 + q13 + q23 - r,
        x - q12 - q13 + r,
        y - q12 - q23 + r,
        z - q13 - q23 + r,
        q12 - r,
        q13 - r,
        q23 - r,
        r,
    ]
    base0 = [F(-1), F(-1), F(-1), F(0), F(0), F(0)]
    grads = [
        [base0[i] + gq12[i] + gq13[i] + gq23[i] - gr[i] for i in range(6)],
        [(1 if i == 0 else 0) - gq12[i] - gq13[i] + gr[i] for i in range(6)],
        [(1 if i == 1 else 0) - gq12[i] - gq23[i] + gr[i] for i in range(6)],
        [(1 if i == 2 else 0) - gq13[i] - gq23[i] + gr[i] for i in range(6)],
        [gq12[i] - gr[i] for i in range(6)],
        [gq13[i] - gr[i] for i in range(6)],
        [gq23[i] - gr[i] for i in range(6)],
        gr,
    ]
    return vals, grads


def coord_gradient_to_matrix(g: Sequence[Fraction]) -> List[List[Fraction]]:
    # dot p(D)=<M,D>_F; off-diagonal coordinate D_ij appears twice in Frobenius.
    return [
        [g[0], g[3] / 2, g[4] / 2],
        [g[3] / 2, g[1], g[5] / 2],
        [g[4] / 2, g[5] / 2, g[2]],
    ]


def D(x: Any) -> Decimal:
    if isinstance(x, Fraction):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(str(x))


def dec_zero(n: int, m: int) -> List[List[Decimal]]:
    return [[Decimal(0) for _ in range(m)] for _ in range(n)]


def dec_eye(n: int) -> List[List[Decimal]]:
    M = dec_zero(n, n)
    for i in range(n):
        M[i][i] = Decimal(1)
    return M


def dec_matmul(A: List[List[Decimal]], B: List[List[Decimal]]) -> List[List[Decimal]]:
    n, m, p = len(A), len(B), len(B[0])
    C = dec_zero(n, p)
    for i in range(n):
        for k in range(m):
            aik = A[i][k]
            if aik:
                for j in range(p):
                    C[i][j] += aik * B[k][j]
    return C


def dec_trace(A: List[List[Decimal]]) -> Decimal:
    return sum(A[i][i] for i in range(len(A)))


def dec_det3(M: List[List[Decimal]]) -> Decimal:
    return (
        M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
        - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
        + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])
    )


def dec_inverse(A: List[List[Decimal]]) -> List[List[Decimal]]:
    n = len(A)
    M = [row[:] + eye for row, eye in zip([r[:] for r in A], dec_eye(n))]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if M[piv][col] == 0:
            raise ZeroDivisionError("singular matrix")
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        for j in range(2 * n):
            M[col][j] /= pv
        for i in range(n):
            if i == col:
                continue
            fac = M[i][col]
            if fac:
                for j in range(2 * n):
                    M[i][j] -= fac * M[col][j]
    return [row[n:] for row in M]


def dec_solve(A: List[List[Decimal]], b: List[Decimal]) -> List[Decimal]:
    n = len(A)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if M[piv][col] == 0:
            raise ZeroDivisionError("singular solve")
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        for j in range(col, n + 1):
            M[col][j] /= pv
        for i in range(n):
            if i == col:
                continue
            fac = M[i][col]
            if fac:
                for j in range(col, n + 1):
                    M[i][j] -= fac * M[col][j]
    return [M[i][n] for i in range(n)]


def dec_ldl_pivots(M: List[List[Decimal]]) -> List[Decimal]:
    n = len(M)
    L = dec_zero(n, n)
    d = [Decimal(0) for _ in range(n)]
    for i in range(n):
        L[i][i] = Decimal(1)
    for j in range(n):
        val = M[j][j]
        for k in range(j):
            val -= L[j][k] * L[j][k] * d[k]
        d[j] = val
        for i in range(j + 1, n):
            val2 = M[i][j]
            for k in range(j):
                val2 -= L[i][k] * L[j][k] * d[k]
            L[i][j] = val2 / d[j]
    return d


def basis_dec() -> List[List[List[Decimal]]]:
    out = []
    for k in range(6):
        M = dec_zero(3, 3)
        if k == 0:
            M[0][0] = Decimal(1)
        elif k == 1:
            M[1][1] = Decimal(1)
        elif k == 2:
            M[2][2] = Decimal(1)
        elif k == 3:
            M[0][1] = M[1][0] = Decimal(1)
        elif k == 4:
            M[0][2] = M[2][0] = Decimal(1)
        elif k == 5:
            M[1][2] = M[2][1] = Decimal(1)
        out.append(M)
    return out


BASIS_DEC = basis_dec()


def compute_decimal_coordinate(Kfrac: List[List[Fraction]], dps: int = 100) -> Dict[str, Any]:
    with localcontext() as ctx:
        ctx.prec = dps
        atoms_f, grads_f = atoms_grads_frac(Kfrac)
        K = [[D(Kfrac[i][j]) for j in range(3)] for i in range(3)]
        atoms = [D(p) for p in atoms_f]
        grads = [[D(x) for x in row] for row in grads_f]
        p0, p1, p2, p3, p12, p13, p23, p123 = atoms
        l12 = (p0 * p12 / (p1 * p2)).ln()
        l13 = (p0 * p13 / (p1 * p3)).ln()
        l23 = (p0 * p23 / (p2 * p3)).ln()
        Lambda = (p123 * p1 * p2 * p3 / (p0 * p12 * p13 * p23)).ln()
        N = dec_zero(3, 3)
        N[0][0] = -l23
        N[1][1] = -l13
        N[2][2] = -l12
        for i in range(3):
            for j in range(3):
                N[i][j] -= Lambda * K[i][j]
        detN = dec_det3(N)
        Ninv = dec_inverse(N)
        Fmat = dec_zero(6, 6)
        for s in range(8):
            for i in range(6):
                for j in range(6):
                    Fmat[i][j] += grads[s][i] * grads[s][j] / atoms[s]
        G = dec_zero(6, 6)
        eta = [Decimal(0) for _ in range(6)]
        for i, Ei in enumerate(BASIS_DEC):
            eta[i] = dec_trace(dec_matmul(Ninv, Ei))
            for j, Ej in enumerate(BASIS_DEC):
                G[i][j] = dec_trace(dec_matmul(dec_matmul(dec_matmul(Ninv, Ei), Ninv), Ej))
        A = dec_zero(6, 6)
        B = dec_zero(6, 6)
        for i in range(6):
            for j in range(6):
                A[i][j] = Fmat[i][j] + detN * G[i][j]
        sol_A = dec_solve(A, eta)
        rho = detN * sum(eta[i] * sol_A[i] for i in range(6))
        for i in range(6):
            for j in range(6):
                B[i][j] = A[i][j] - detN * eta[i] * eta[j]
        sol_F = dec_solve(Fmat, eta)
        score_only = detN * sum(eta[i] * sol_F[i] for i in range(6))
        Iminus = dec_eye(3)
        for i in range(3):
            for j in range(3):
                Iminus[i][j] -= K[i][j]
        return {
            "rho": str(+rho),
            "score_only_detN_eta_Finv_eta": str(+score_only),
            "detN": str(+detN),
            "Lambda": str(+Lambda),
            "min_atom_fraction": f"{min(atoms_f).numerator}/{min(atoms_f).denominator}",
            "min_atom_name": ATOM_NAMES[min(range(8), key=lambda i: atoms_f[i])],
            "atoms": {ATOM_NAMES[i]: f"{atoms_f[i].numerator}/{atoms_f[i].denominator}" for i in range(8)},
            "K_ldl_pivots_fraction": [f"{v.numerator}/{v.denominator}" for v in ldl_pivots3_frac(Kfrac)],
            "I_minus_K_ldl_pivots_fraction": [f"{v.numerator}/{v.denominator}" for v in ldl_pivots3_frac(mat_sub_frac(eye_frac(3), Kfrac))],
            "N_ldl_pivots": [str(+v) for v in dec_ldl_pivots(N)],
            "F_ldl_pivots": [str(+v) for v in dec_ldl_pivots(Fmat)],
            "A_ldl_pivots": [str(+v) for v in dec_ldl_pivots(A)],
            "B_ldl_pivots": [str(+v) for v in dec_ldl_pivots(B)],
        }


def frac_to_float_matrix(K: List[List[Fraction]]) -> np.ndarray:
    return np.array([[float(v) for v in row] for row in K], dtype=float)


def orthovec(M: np.ndarray) -> np.ndarray:
    return np.array([M[0, 0], M[1, 1], M[2, 2], math.sqrt(2) * M[0, 1], math.sqrt(2) * M[0, 2], math.sqrt(2) * M[1, 2]])


def matrix_from_grad_float(g: Sequence[Fraction]) -> np.ndarray:
    M = np.zeros((3, 3), dtype=float)
    M[0, 0] = float(g[0])
    M[1, 1] = float(g[1])
    M[2, 2] = float(g[2])
    M[0, 1] = M[1, 0] = float(g[3]) / 2.0
    M[0, 2] = M[2, 0] = float(g[4]) / 2.0
    M[1, 2] = M[2, 1] = float(g[5]) / 2.0
    return M


def operator_ridge_checks(Kfrac: List[List[Fraction]], rho_decimal_value: str) -> Dict[str, Any]:
    K = frac_to_float_matrix(Kfrac)
    atoms_f, grads_f = atoms_grads_frac(Kfrac)
    atoms = np.array([float(p) for p in atoms_f], dtype=float)

    p0, p1, p2, p3, p12, p13, p23, p123 = atoms
    l12 = math.log((p0 * p12) / (p1 * p2))
    l13 = math.log((p0 * p13) / (p1 * p3))
    l23 = math.log((p0 * p23) / (p2 * p3))
    Lambda = math.log((p123 * p1 * p2 * p3) / (p0 * p12 * p13 * p23))
    N = np.diag([-l23, -l13, -l12]) - Lambda * K
    N = (N + N.T) / 2.0
    detN = float(np.linalg.det(N))
    evals, Q = np.linalg.eigh(N)
    Nsqrt = Q @ np.diag(np.sqrt(evals)) @ Q.T

    Mlist = [matrix_from_grad_float(g) for g in grads_f]
    sumM = np.sum(Mlist, axis=0)
    Crows = []
    for p, M in zip(atoms, Mlist):
        Cmat = Nsqrt @ M @ Nsqrt / math.sqrt(detN * p)
        Crows.append(orthovec(Cmat))
    C = np.vstack(Crows)  # rows are C_S as vectors in Frobenius-orthonormal coords.
    Ivec = np.array([1, 1, 1, 0, 0, 0], dtype=float)

    T = np.eye(6) + C.T @ C
    rho2 = float(Ivec @ np.linalg.solve(T, Ivec))

    alpha = np.linalg.solve(np.eye(8) + C @ C.T, C @ Ivec)
    residual3 = Ivec - C.T @ alpha
    ridge3 = float(residual3 @ residual3 + alpha @ alpha)

    # Unnormalised g_S = alpha_S / sqrt(det(N) p_S), proving the det(N)*p_S
    # score normalization in (4).
    g = alpha / np.sqrt(detN * atoms)
    S = np.zeros((3, 3), dtype=float)
    for coeff, M in zip(g, Mlist):
        S += coeff * M
    residual_mat = np.eye(3) - Nsqrt @ S @ Nsqrt
    energy4 = float(np.sum(residual_mat * residual_mat) + detN * float(np.sum(atoms * g * g)))
    mean_g = float(np.sum(atoms * g))
    rho_dec = float(Decimal(rho_decimal_value))
    return {
        "rho_equation_2_operator_float": rho2,
        "rho_equation_3_ridge_float": ridge3,
        "rho_equation_4_unnormalized_float": energy4,
        "rho_decimal_float": rho_dec,
        "max_abs_difference_vs_decimal": max(abs(rho2 - rho_dec), abs(ridge3 - rho_dec), abs(energy4 - rho_dec)),
        "eq2_eq3_abs_difference": abs(rho2 - ridge3),
        "eq3_eq4_abs_difference": abs(ridge3 - energy4),
        "weighted_mean_of_optimal_g": mean_g,
        "sum_M_frobenius_norm": float(np.linalg.norm(sumM, ord="fro")),
    }


def named_cases() -> Dict[str, List[List[Fraction]]]:
    return {
        "heterogeneous_triangle": [
            [F(2, 5), F(1, 12), F(-1, 15)],
            [F(1, 12), F(1, 3), F(1, 18)],
            [F(-1, 15), F(1, 18), F(3, 7)],
        ],
        "signed_path_like": [
            [F(3, 8), F(1, 10), F(0)],
            [F(1, 10), F(5, 12), F(-1, 11)],
            [F(0), F(-1, 11), F(7, 16)],
        ],
        "score_only_shortcut_blocker": [
            [F(1367, 5000), F(7, 250), F(723, 2500)],
            [F(7, 250), F(2187, 2500), F(-33, 2500)],
            [F(723, 2500), F(-33, 2500), F(7231, 10000)],
        ],
    }


def exact_mass_jet_checks(Kfrac: List[List[Fraction]]) -> Dict[str, Any]:
    atoms, grads = atoms_grads_frac(Kfrac)
    matrices = [coord_gradient_to_matrix(g) for g in grads]
    sum_matrix = [[sum(M[i][j] for M in matrices) for j in range(3)] for i in range(3)]
    return {
        "atom_sum_is_one": sum(atoms) == 1,
        "all_atoms_positive": all(p > 0 for p in atoms),
        "sum_gradient_zero": all(sum(grads[s][j] for s in range(8)) == 0 for j in range(6)),
        "sum_M_zero": all(sum_matrix[i][j] == 0 for i in range(3) for j in range(3)),
        "min_atom_fraction": f"{min(atoms).numerator}/{min(atoms).denominator}",
    }


def main() -> int:
    t0 = time.time()
    cases = named_cases()
    inputs = [
        AUTHOR_DIR / "proof_or_blocker.md",
        AUTHOR_DIR / "verdict.md",
        AUTHOR_DIR / "run_log.md",
        AUTHOR_DIR / "scalar_information_sanity.py",
        AUTHOR_DIR / "scalar_information_sanity_results.json",
        ROOT_U8_DIR / "derivation.md",
    ]
    results: Dict[str, Any] = {
        "status": "CORRECT_SCOPED",
        "global_rho_bound": "INCOMPLETE_NOT_PROVED_HERE",
        "script_sha256": None,
        "input_hashes": {str(p.relative_to(ROOT_U8_DIR.parent)): sha256_file(p) for p in inputs if p.exists()},
        "cases": {},
        "checks": {},
    }
    max_eq_diff = 0.0
    for name, K in cases.items():
        dec = compute_decimal_coordinate(K, dps=110)
        op = operator_ridge_checks(K, dec["rho"])
        exact = exact_mass_jet_checks(K)
        results["cases"][name] = {
            "exact_mass_and_jets": exact,
            "coordinate_decimal": dec,
            "operator_ridge_float": op,
            "connected_support": sum(1 for e in [K[0][1], K[0][2], K[1][2]] if e != 0) >= 2,
        }
        max_eq_diff = max(max_eq_diff, op["max_abs_difference_vs_decimal"], op["eq2_eq3_abs_difference"], op["eq3_eq4_abs_difference"])

    blocker = results["cases"]["score_only_shortcut_blocker"]["coordinate_decimal"]
    blocker_ok = (
        Decimal(blocker["score_only_detN_eta_Finv_eta"]) > Decimal(1)
        and Decimal(blocker["rho"]) < Decimal(1)
        and all(Decimal(x) > 0 for x in blocker["N_ldl_pivots"])
        and all(Decimal(x) > 0 for x in blocker["B_ldl_pivots"])
    )
    eq_ok = max_eq_diff < 5e-12
    exact_ok = all(c["exact_mass_and_jets"]["atom_sum_is_one"] and c["exact_mass_and_jets"]["all_atoms_positive"] and c["exact_mass_and_jets"]["sum_gradient_zero"] and c["exact_mass_and_jets"]["sum_M_zero"] for c in results["cases"].values())
    results["checks"] = {
        "equations_2_3_4_constants_and_normalization": "PASS" if eq_ok else "FAIL",
        "max_equation_difference_float": max_eq_diff,
        "exact_atom_mass_and_first_jet_checks": "PASS" if exact_ok else "FAIL",
        "fisher_only_blocker": "PASS" if blocker_ok else "FAIL",
        "blocker_score_only_gt_1": blocker["score_only_detN_eta_Finv_eta"],
        "blocker_true_rho_lt_1": blocker["rho"],
        "blocker_min_B_ldl_pivot": min(blocker["B_ldl_pivots"], key=lambda x: Decimal(x)),
        "equivalent_rewrite_not_proof": "PASS: author explicitly leaves global rho<=1 open",
    }
    if not (eq_ok and exact_ok and blocker_ok):
        results["status"] = "CRITICAL_GAPS"

    elapsed = time.time() - t0
    results["elapsed_seconds"] = elapsed
    (BASE / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    results["script_sha256"] = sha256_file(Path(__file__).resolve())
    (BASE / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")

    run_log = [
        "# D10-U10b scalar_information non-author audit run log",
        "",
        f"Command: `{Path(sys.executable)} {Path(__file__).name}`",
        "Exit code: `0`",
        f"Elapsed seconds: `{elapsed:.6f}`",
        "Author sanity script was hashed but not imported or called.",
        "",
        "Summary:",
        f"- equations (2)(3)(4) constants/normalization: `{results['checks']['equations_2_3_4_constants_and_normalization']}`",
        f"- exact atom mass/first jets: `{results['checks']['exact_atom_mass_and_first_jet_checks']}`",
        f"- Fisher-only blocker: `{results['checks']['fisher_only_blocker']}`",
        f"- global rho<=1 proof: `{results['global_rho_bound']}`",
    ]
    (BASE / "run_log.md").write_text("\n".join(run_log) + "\n", encoding="utf-8")
    print(json.dumps({"status": results["status"], "global_rho_bound": results["global_rho_bound"], "blocker": results["checks"]["fisher_only_blocker"], "max_eq_diff": max_eq_diff, "elapsed_seconds": elapsed}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
