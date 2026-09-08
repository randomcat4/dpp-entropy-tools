#!/usr/bin/env python3
"""D10-S5 scout/certificate work for the full PSD cone at the M7 K_* point.

The exact-event entropy Hessian is assembled from Fraction atom jets.  Decimal
logs are used for the fixed rational base atoms.  Numpy is used only for
eigen/projection-based scouting over PSD directions; it is not treated as a
proof of cone negativity.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import permutations
import json
from pathlib import Path
import random
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
COORDS = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
NVAR = len(COORDS)
DEG = 4
ZERO = F(0)
ONE = F(1)

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def f(num: int, den: int = 1) -> F:
    return F(num, den)


def fstr(x: F) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def dec(x: F) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def serialize(obj):
    if isinstance(obj, F):
        return fstr(obj)
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, np.ndarray):
        return serialize(obj.tolist())
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, list):
        return [serialize(v) for v in obj]
    if isinstance(obj, tuple):
        return [serialize(v) for v in obj]
    if isinstance(obj, dict):
        return {str(k): serialize(v) for k, v in obj.items()}
    return obj


def padd(a: list[F], b: list[F]) -> list[F]:
    return [a[i] + b[i] for i in range(DEG)]


def pscale(c: F, a: list[F]) -> list[F]:
    return [c * x for x in a]


def pmul(a: list[F], b: list[F]) -> list[F]:
    out = [ZERO] * DEG
    for i, av in enumerate(a):
        for j, bv in enumerate(b):
            if i + j < DEG:
                out[i + j] += av * bv
    return out


def iadd(a: tuple[F, F], b: tuple[F, F]) -> tuple[F, F]:
    return a[0] + b[0], a[1] + b[1]


def isub(a: tuple[F, F], b: tuple[F, F]) -> tuple[F, F]:
    return a[0] - b[1], a[1] - b[0]


def iscale(c: F, a: tuple[F, F]) -> tuple[F, F]:
    if c >= 0:
        return c * a[0], c * a[1]
    return c * a[1], c * a[0]


def log_bounds(x: F, terms: int = 35) -> tuple[F, F]:
    """Rigorous rational interval for natural log(x)."""
    assert x > 0
    if x == 1:
        return ZERO, ZERO
    exponent = 0
    y = x
    while y < 1:
        y *= 2
        exponent -= 1
    while y >= 2:
        y /= 2
        exponent += 1

    def atanh_series(z: F) -> tuple[F, F]:
        partial = 2 * sum(z ** (2 * k + 1) / F(2 * k + 1) for k in range(terms))
        tail = 2 * z ** (2 * terms + 1) / (F(2 * terms + 1) * (1 - z * z))
        return partial, partial + tail

    lo, hi = atanh_series((y - 1) / (y + 1))
    lo2, hi2 = atanh_series(F(1, 3))
    if exponent >= 0:
        return lo + exponent * lo2, hi + exponent * hi2
    return lo + exponent * hi2, hi + exponent * lo2


def perm_sign(perm: tuple[int, ...]) -> int:
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inv += int(perm[i] > perm[j])
    return -1 if inv % 2 else 1


def det_poly(matrix: list[list[list[F]]]) -> list[F]:
    m = len(matrix)
    if m == 0:
        return [ONE, ZERO, ZERO, ZERO]
    total = [ZERO] * DEG
    for perm in permutations(range(m)):
        term = [F(perm_sign(perm)), ZERO, ZERO, ZERO]
        for i, j in enumerate(perm):
            term = pmul(term, matrix[i][j])
        total = padd(total, term)
    return total


def matrix_from_coords(x: list[F]) -> list[list[F]]:
    D = [[ZERO for _ in range(3)] for _ in range(3)]
    for value, (i, j) in zip(x, COORDS):
        D[i][j] = value
        D[j][i] = value
    return D


def coords_from_matrix(D: list[list[F]]) -> list[F]:
    return [D[i][j] for i, j in COORDS]


def k_star() -> list[list[F]]:
    return [
        [f(151, 280), -f(6, 35), -f(47, 280)],
        [-f(6, 35), f(94, 175), -f(29, 175)],
        [-f(47, 280), -f(29, 175), f(747, 1400)],
    ]


def d_star_commuting() -> list[list[F]]:
    return [
        [f(307, 630), -f(64, 315), -f(53, 630)],
        [-f(64, 315), f(131, 315), -f(4, 315)],
        [-f(53, 630), -f(4, 315), f(187, 630)],
    ]


def atom_polys_for_direction(K: list[list[F]], D: list[list[F]]) -> list[list[F]]:
    dets: dict[int, list[F]] = {}
    for mask in range(8):
        idx = [i for i in range(3) if mask & (1 << i)]
        matrix = [
            [[[K[i][j], D[i][j], ZERO, ZERO] for j in idx][col] for col in range(len(idx))]
            for i in idx
        ]
        dets[mask] = det_poly(matrix)
    atoms = []
    full = 7
    for S in range(8):
        total = [ZERO] * DEG
        rest = full ^ S
        sub = rest
        while True:
            A = S | sub
            signed = dets[A] if (A.bit_count() - S.bit_count()) % 2 == 0 else pscale(-ONE, dets[A])
            total = padd(total, signed)
            if sub == 0:
                break
            sub = (sub - 1) & rest
        atoms.append(total)
    return atoms


def entropy_hessian_decimal(K: list[list[F]], D: list[list[F]]) -> Decimal:
    atoms = atom_polys_for_direction(K, D)
    total = Decimal(0)
    for poly in atoms:
        p0 = poly[0]
        p1 = poly[1]
        p2 = 2 * poly[2]
        total += -(dec(p1 * p1 / p0) + dec(p2) * dec(p0).ln())
    return total


def entropy_hessian_interval(K: list[list[F]], D: list[list[F]], log_terms: int = 35) -> tuple[F, F]:
    atoms = atom_polys_for_direction(K, D)
    total = (ZERO, ZERO)
    for poly in atoms:
        p0 = poly[0]
        p1 = poly[1]
        p2 = 2 * poly[2]
        rational_part = -p1 * p1 / p0
        log_part = iscale(-p2, log_bounds(p0, terms=log_terms))
        total = iadd(total, iadd((rational_part, rational_part), log_part))
    return total


def base_atoms(K: list[list[F]]) -> list[F]:
    zero = [[ZERO for _ in range(3)] for _ in range(3)]
    return [row[0] for row in atom_polys_for_direction(K, zero)]


def build_hessian_matrix(K: list[list[F]]) -> list[list[Decimal]]:
    basis = []
    for i in range(NVAR):
        x = [ZERO] * NVAR
        x[i] = ONE
        basis.append(matrix_from_coords(x))
    q_diag = [entropy_hessian_decimal(K, B) for B in basis]
    H = [[Decimal(0) for _ in range(NVAR)] for _ in range(NVAR)]
    for i in range(NVAR):
        H[i][i] = q_diag[i]
    for i in range(NVAR):
        for j in range(i + 1, NVAR):
            Dsum = [[basis[i][r][c] + basis[j][r][c] for c in range(3)] for r in range(3)]
            q = entropy_hessian_decimal(K, Dsum)
            H[i][j] = H[j][i] = (q - q_diag[i] - q_diag[j]) / Decimal(2)
    return H


def build_hessian_interval_matrix(K: list[list[F]], log_terms: int = 35) -> list[list[tuple[F, F]]]:
    basis = []
    for i in range(NVAR):
        x = [ZERO] * NVAR
        x[i] = ONE
        basis.append(matrix_from_coords(x))
    q_diag = [entropy_hessian_interval(K, B, log_terms=log_terms) for B in basis]
    H = [[(ZERO, ZERO) for _ in range(NVAR)] for _ in range(NVAR)]
    for i in range(NVAR):
        H[i][i] = q_diag[i]
    for i in range(NVAR):
        for j in range(i + 1, NVAR):
            Dsum = [[basis[i][r][c] + basis[j][r][c] for c in range(3)] for r in range(3)]
            q = entropy_hessian_interval(K, Dsum, log_terms=log_terms)
            off = iscale(F(1, 2), isub(isub(q, q_diag[i]), q_diag[j]))
            H[i][j] = H[j][i] = off
    return H


def gershgorin_certificate_for_negative_hessian(Hint: list[list[tuple[F, F]]]) -> dict:
    margins = []
    rows = []
    for i in range(NVAR):
        diag_lower = -Hint[i][i][1]
        radius_upper = ZERO
        for j in range(NVAR):
            if i == j:
                continue
            lo, hi = Hint[i][j]
            radius_upper += max(abs(lo), abs(hi))
        margin = diag_lower - radius_upper
        margins.append(margin)
        rows.append({
            "row": i,
            "diag_lower_for_minus_H": diag_lower,
            "offdiag_abs_radius_upper": radius_upper,
            "margin": margin,
        })
    return {
        "method": "rational log intervals plus Gershgorin strict diagonal dominance for -H",
        "row_certificates": rows,
        "min_margin": min(margins),
        "all_rows_positive": all(m > 0 for m in margins),
    }


def coord_vector_from_np(D: np.ndarray) -> np.ndarray:
    return np.array([D[i, j] for i, j in COORDS], dtype=float)


def matrix_from_np_coords(x: np.ndarray) -> np.ndarray:
    D = np.zeros((3, 3), dtype=float)
    for value, (i, j) in zip(x, COORDS):
        D[i, j] = value
        D[j, i] = value
    return D


def h2_float(A: np.ndarray, D: np.ndarray) -> float:
    x = coord_vector_from_np(D)
    return float(x @ A @ x)


def frob_normalize_psd(D: np.ndarray) -> np.ndarray:
    D = (D + D.T) / 2
    w, V = np.linalg.eigh(D)
    w = np.maximum(w, 0.0)
    Dp = (V * w) @ V.T
    norm = np.linalg.norm(Dp, "fro")
    if norm == 0:
        return np.eye(3) / np.sqrt(3)
    return Dp / norm


def random_psd(rng: random.Random) -> np.ndarray:
    M = np.array([[rng.gauss(0, 1) for _ in range(3)] for _ in range(3)], dtype=float)
    D = M @ M.T
    return D / np.linalg.norm(D, "fro")


def rank_one_from_vec(u: np.ndarray) -> np.ndarray:
    u = np.asarray(u, dtype=float)
    norm2 = float(u @ u)
    if norm2 == 0:
        u = np.array([1.0, 0.0, 0.0])
        norm2 = 1.0
    return np.outer(u, u) / norm2


def projected_power_scout(A: np.ndarray, starts: int = 400, steps: int = 300, seed: int = 20260908) -> dict:
    rng = random.Random(seed)
    best_D = None
    best_val = -1e100
    rank1_best_D = None
    rank1_best_val = -1e100

    def update(D):
        nonlocal best_D, best_val
        val = h2_float(A, D)
        if val > best_val:
            best_val = val
            best_D = D.copy()

    # Rank-one random scan.
    for _ in range(starts * 10):
        u = np.array([rng.gauss(0, 1) for _ in range(3)], dtype=float)
        D = rank_one_from_vec(u)
        val = h2_float(A, D)
        if val > rank1_best_val:
            rank1_best_val = val
            rank1_best_D = D.copy()
        update(D)

    # PSD projected ascent.
    for _ in range(starts):
        D = random_psd(rng)
        for step in range(steps):
            x = coord_vector_from_np(D)
            grad_x = 2 * A @ x
            # x stores each symmetric off-diagonal entry once, whereas the
            # Frobenius inner product counts it twice.  Convert the coordinate
            # gradient to the true symmetric-matrix Frobenius gradient.
            grad_matrix_coords = grad_x.copy()
            grad_matrix_coords[3:] *= 0.5
            G = matrix_from_np_coords(grad_matrix_coords)
            eta = 0.35 / (1 + step / 60)
            D = frob_normalize_psd(D + eta * G)
        update(D)

    eig_best = np.linalg.eigvalsh(best_D)
    eig_rank1 = np.linalg.eigvalsh(rank1_best_D)
    return {
        "seed": seed,
        "starts": starts,
        "steps": steps,
        "best_value": best_val,
        "best_D": best_D,
        "best_D_eigenvalues": eig_best,
        "best_rank": int(np.sum(eig_best > 1e-8)),
        "rank1_best_value": rank1_best_val,
        "rank1_best_D": rank1_best_D,
        "rank1_best_eigenvalues": eig_rank1,
    }


def rationalize_direction(D: np.ndarray, max_den: int = 10000) -> list[list[F]]:
    return [[F(float(D[i, j])).limit_denominator(max_den) for j in range(3)] for i in range(3)]


def psd_principal_margins(D: list[list[F]]) -> dict:
    minors = {
        "m00": D[0][0],
        "m11": D[1][1],
        "m22": D[2][2],
        "m01": D[0][0] * D[1][1] - D[0][1] ** 2,
        "m02": D[0][0] * D[2][2] - D[0][2] ** 2,
        "m12": D[1][1] * D[2][2] - D[1][2] ** 2,
        "det": (
            D[0][0] * D[1][1] * D[2][2]
            + 2 * D[0][1] * D[0][2] * D[1][2]
            - D[0][0] * D[1][2] ** 2
            - D[1][1] * D[0][2] ** 2
            - D[2][2] * D[0][1] ** 2
        ),
    }
    return minors


def strict_kernel_interval_margin(K: list[list[F]], D: list[list[F]], h: F) -> dict:
    # Conservative Gershgorin-style rational lower margin for K +/- hD and I-K-/+hD:
    # lambda_min(A) >= min_i (A_ii - sum_{j!=i}|A_ij|).
    margins = {}
    for sign in (-1, 1):
        A = [[K[i][j] + sign * h * D[i][j] for j in range(3)] for i in range(3)]
        B = [[(F(int(i == j)) - K[i][j]) - sign * h * D[i][j] for j in range(3)] for i in range(3)]
        margins[f"K_sign_{sign}"] = min(A[i][i] - sum(abs(A[i][j]) for j in range(3) if j != i) for i in range(3))
        margins[f"IminusK_sign_{sign}"] = min(B[i][i] - sum(abs(B[i][j]) for j in range(3) if j != i) for i in range(3))
    return margins


def main() -> int:
    with localcontext() as ctx:
        ctx.prec = 100
        K = k_star()
        atoms = base_atoms(K)
        assert min(atoms) > 0
        Hdec = build_hessian_matrix(K)
        Hint = build_hessian_interval_matrix(K, log_terms=35)
        gersh = gershgorin_certificate_for_negative_hessian(Hint)
        assert gersh["all_rows_positive"]
        A = np.array([[float(x) for x in row] for row in Hdec], dtype=float)
        eig_unconstrained = np.linalg.eigvalsh(A)
        dstar = d_star_commuting()
        h2_dstar = entropy_hessian_decimal(K, dstar)
        scout = projected_power_scout(A)
        best_rat = rationalize_direction(scout["best_D"], 2000)
        best_rat_margins = psd_principal_margins(best_rat)
        best_rat_h2 = entropy_hessian_decimal(K, best_rat)
        best_rat_frob2 = sum(best_rat[i][j] ** 2 for i in range(3) for j in range(3))
        best_rat_h2_unit = best_rat_h2 / (dec(best_rat_frob2))
        feasibility_probe = strict_kernel_interval_margin(K, best_rat, F(1, 1000))

        report = {
            "status": "PROOF_CANDIDATE_PENDING_FRESH_REVIEW",
            "base": "M7 equation (19) K_*",
            "coordinate_order": COORDS,
            "K_star": K,
            "base_atoms": atoms,
            "min_base_atom": min(atoms),
            "entropy_hessian_matrix_decimal": Hdec,
            "interval_log_terms": 35,
            "gershgorin_negative_definite_certificate": gersh,
            "unconstrained_eigenvalues_float": eig_unconstrained,
            "commuting_D_star_H2": h2_dstar,
            "commuting_D_star_frob2": sum(dstar[i][j] ** 2 for i in range(3) for j in range(3)),
            "projected_psd_scout": scout,
            "rationalized_best_direction_den_le_2000": best_rat,
            "rationalized_best_psd_principal_margins": best_rat_margins,
            "rationalized_best_H2": best_rat_h2,
            "rationalized_best_frob2": best_rat_frob2,
            "rationalized_best_H2_per_frob2": best_rat_h2_unit,
            "feasibility_probe_gershgorin_margins_at_h_1_1000": feasibility_probe,
            "notes": [
                "The interval Gershgorin certificate proves strict negativity on all nonzero symmetric directions at K_*.",
                "The PSD projected search is retained as an attack log, not as the proof.",
                "NSD has the same Hessian value by D -> -D.",
            ],
        }
        out = HERE / "hessian_scout.json"
        out.write_text(json.dumps(serialize(report), indent=2), encoding="utf-8")
        print(json.dumps(serialize({
            "status": report["status"],
            "json": str(out),
            "min_base_atom": min(atoms),
            "gershgorin_min_margin_for_minus_H_decimal": dec(gersh["min_margin"]),
            "unconstrained_max_eigenvalue_float": float(eig_unconstrained[-1]),
            "commuting_D_star_H2": h2_dstar,
            "psd_scout_best_value": scout["best_value"],
            "psd_scout_best_rank": scout["best_rank"],
            "rank1_best_value": scout["rank1_best_value"],
            "rationalized_best_H2_per_frob2": best_rat_h2_unit,
            "rationalized_best_psd_det_margin": best_rat_margins["det"],
        }), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
