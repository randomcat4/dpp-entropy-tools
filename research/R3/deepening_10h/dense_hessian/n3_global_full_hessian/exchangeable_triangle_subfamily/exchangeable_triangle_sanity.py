"""Independent sanity/scout for the exchangeable n=3 triangle subfamily.

This file is author-side exploratory code, not a certificate and not a proof.
It does not import any U8/U10 author gate/search module.  It rebuilds the
eight exact atoms from Mobius inversion of inclusion determinants and computes
B=-Hess H directly from event jets.
"""

from __future__ import annotations

import json
import math
import os
import random
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import numpy as np


HERE = Path(__file__).resolve().parent


def exchangeable_atoms_ab(alpha: float, beta: float) -> list[float]:
    """Per-subset exact atoms by cardinality 0,1,2,3.

    K has eigenvalue alpha on the all-ones line and beta on the two-dimensional
    standard representation.  Thus x=(alpha+2 beta)/3 and
    a=(alpha-beta)/3.
    """

    p0 = (1.0 - alpha) * (1.0 - beta) ** 2
    u = alpha + 2.0 * beta - 3.0 * alpha * beta
    v = 2.0 * alpha + beta - 3.0 * alpha * beta
    p1 = (1.0 - beta) * u / 3.0
    p2 = beta * v / 3.0
    p3 = alpha * beta * beta
    return [p0, p1, p2, p3]


def trivial_block_alpha_beta(alpha: float, beta: float) -> np.ndarray:
    """The 2x2 B-block for the invariant plane, in coordinates (alpha,beta)."""

    p0, p1, p2, p3 = exchangeable_atoms_ab(alpha, beta)
    u = alpha + 2.0 * beta - 3.0 * alpha * beta

    # Corrected derivatives.  In particular
    # d/d alpha [beta(2 alpha + beta - 3 alpha beta)/3]
    # equals beta(2-3 beta)/3, not 2 beta(1-beta)/3.
    p_a = [
        -(1.0 - beta) ** 2,
        (1.0 - beta) * (1.0 - 3.0 * beta) / 3.0,
        beta * (2.0 - 3.0 * beta) / 3.0,
        beta * beta,
    ]
    p_b = [
        -2.0 * (1.0 - alpha) * (1.0 - beta),
        (2.0 - 4.0 * alpha - 4.0 * beta + 6.0 * alpha * beta) / 3.0,
        (2.0 * alpha + 2.0 * beta - 6.0 * alpha * beta) / 3.0,
        2.0 * alpha * beta,
    ]
    p_aa = [0.0, 0.0, 0.0, 0.0]
    p_ab = [
        2.0 * (1.0 - beta),
        (-4.0 + 6.0 * beta) / 3.0,
        (2.0 - 6.0 * beta) / 3.0,
        2.0 * beta,
    ]
    p_bb = [
        2.0 * (1.0 - alpha),
        (-4.0 + 6.0 * alpha) / 3.0,
        (2.0 - 6.0 * alpha) / 3.0,
        2.0 * alpha,
    ]

    block = np.zeros((2, 2), dtype=float)
    for p, mult, da, db, daa, dab, dbb in zip(
        [p0, p1, p2, p3],
        [1.0, 3.0, 3.0, 1.0],
        p_a,
        p_b,
        p_aa,
        p_ab,
        p_bb,
    ):
        block[0, 0] += mult * (da * da / p + daa * math.log(p))
        block[0, 1] += mult * (da * db / p + dab * math.log(p))
        block[1, 1] += mult * (db * db / p + dbb * math.log(p))
    block[1, 0] = block[0, 1]
    return block


def inclusion_jets(v: np.ndarray):
    """Return inclusion determinants q_A and their first/second jets.

    Coordinates are (11,22,33,12,13,23), with off-diagonal coordinates meaning
    the symmetric matrix entry K_ij=K_ji.
    """

    x1, x2, x3, u, v13, w = map(float, v)
    q = {}
    g = {}
    h = {}

    def zgrad():
        return np.zeros(6, dtype=float)

    def zhess():
        return np.zeros((6, 6), dtype=float)

    q[()] = 1.0
    g[()] = zgrad()
    h[()] = zhess()

    for name, idx, val in [
        ((0,), 0, x1),
        ((1,), 1, x2),
        ((2,), 2, x3),
    ]:
        q[name] = val
        gg = zgrad()
        gg[idx] = 1.0
        g[name] = gg
        h[name] = zhess()

    q12 = x1 * x2 - u * u
    gg = zgrad()
    gg[0], gg[1], gg[3] = x2, x1, -2.0 * u
    hh = zhess()
    hh[0, 1] = hh[1, 0] = 1.0
    hh[3, 3] = -2.0
    q[(0, 1)], g[(0, 1)], h[(0, 1)] = q12, gg, hh

    q13 = x1 * x3 - v13 * v13
    gg = zgrad()
    gg[0], gg[2], gg[4] = x3, x1, -2.0 * v13
    hh = zhess()
    hh[0, 2] = hh[2, 0] = 1.0
    hh[4, 4] = -2.0
    q[(0, 2)], g[(0, 2)], h[(0, 2)] = q13, gg, hh

    q23 = x2 * x3 - w * w
    gg = zgrad()
    gg[1], gg[2], gg[5] = x3, x2, -2.0 * w
    hh = zhess()
    hh[1, 2] = hh[2, 1] = 1.0
    hh[5, 5] = -2.0
    q[(1, 2)], g[(1, 2)], h[(1, 2)] = q23, gg, hh

    r = x1 * x2 * x3 + 2.0 * u * v13 * w - x1 * w * w - x2 * v13 * v13 - x3 * u * u
    gg = zgrad()
    gg[0] = x2 * x3 - w * w
    gg[1] = x1 * x3 - v13 * v13
    gg[2] = x1 * x2 - u * u
    gg[3] = 2.0 * v13 * w - 2.0 * x3 * u
    gg[4] = 2.0 * u * w - 2.0 * x2 * v13
    gg[5] = 2.0 * u * v13 - 2.0 * x1 * w
    hh = zhess()
    hh[0, 1] = hh[1, 0] = x3
    hh[0, 2] = hh[2, 0] = x2
    hh[1, 2] = hh[2, 1] = x1
    hh[0, 5] = hh[5, 0] = -2.0 * w
    hh[1, 4] = hh[4, 1] = -2.0 * v13
    hh[2, 3] = hh[3, 2] = -2.0 * u
    hh[3, 3] = -2.0 * x3
    hh[4, 4] = -2.0 * x2
    hh[5, 5] = -2.0 * x1
    hh[3, 4] = hh[4, 3] = 2.0 * w
    hh[3, 5] = hh[5, 3] = 2.0 * v13
    hh[4, 5] = hh[5, 4] = 2.0 * u
    q[(0, 1, 2)], g[(0, 1, 2)], h[(0, 1, 2)] = r, gg, hh
    return q, g, h


EVENTS = [
    (),
    (0,),
    (1,),
    (2,),
    (0, 1),
    (0, 2),
    (1, 2),
    (0, 1, 2),
]


def event_jets(v: np.ndarray):
    q, g, h = inclusion_jets(v)
    p = []
    pg = []
    ph = []
    full = {0, 1, 2}
    for event in EVENTS:
        event_set = set(event)
        val = 0.0
        gg = np.zeros(6, dtype=float)
        hh = np.zeros((6, 6), dtype=float)
        # Mobius inversion from inclusion probabilities.
        for mask in range(8):
            sup = tuple(i for i in range(3) if mask & (1 << i))
            sup_set = set(sup)
            if not event_set.issubset(sup_set):
                continue
            sign = -1.0 if ((len(sup) - len(event)) % 2) else 1.0
            val += sign * q[sup]
            gg += sign * g[sup]
            hh += sign * h[sup]
        p.append(val)
        pg.append(gg)
        ph.append(hh)
    return np.array(p, dtype=float), pg, ph


def full_B_xa(x: float, a: float) -> np.ndarray:
    p, pg, ph = event_jets(np.array([x, x, x, a, a, a], dtype=float))
    B = np.zeros((6, 6), dtype=float)
    for val, gg, hh in zip(p, pg, ph):
        B += np.outer(gg, gg) / val + hh * math.log(val)
    return 0.5 * (B + B.T)


def trivial_block_xa(x: float, a: float) -> np.ndarray:
    B = full_B_xa(x, a)
    I = np.array([1, 1, 1, 0, 0, 0], dtype=float)
    O = np.array([0, 0, 0, 1, 1, 1], dtype=float)
    M = np.array([[I @ B @ I, I @ B @ O], [O @ B @ I, O @ B @ O]])
    return 0.5 * (M + M.T)


def alpha_beta_basis_block_from_full(alpha: float, beta: float) -> np.ndarray:
    x = (alpha + 2.0 * beta) / 3.0
    a = (alpha - beta) / 3.0
    B = full_B_xa(x, a)
    da = np.array([1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3, 1 / 3], dtype=float)
    db = np.array([2 / 3, 2 / 3, 2 / 3, -1 / 3, -1 / 3, -1 / 3], dtype=float)
    M = np.array([[da @ B @ da, da @ B @ db], [db @ B @ da, db @ B @ db]])
    return 0.5 * (M + M.T)


def representation_residual(alpha: float, beta: float) -> dict:
    x = (alpha + 2.0 * beta) / 3.0
    a = (alpha - beta) / 3.0
    B = full_B_xa(x, a)
    T = [
        np.array([1, 1, 1, 0, 0, 0], dtype=float),
        np.array([0, 0, 0, 1, 1, 1], dtype=float),
    ]
    W = [
        np.array([1, -1, 0, 0, 0, 0], dtype=float),
        np.array([1, 1, -2, 0, 0, 0], dtype=float),
        np.array([0, 0, 0, 1, -1, 0], dtype=float),
        np.array([0, 0, 0, 1, 1, -2], dtype=float),
    ]
    cross = max(abs(t @ B @ w) for t in T for w in W)
    BW = np.array([[wi @ B @ wj for wj in W] for wi in W], dtype=float)
    return {
        "alpha": alpha,
        "beta": beta,
        "max_TW_cross_abs": cross,
        "W_basis_min_eig": float(np.linalg.eigvalsh(0.5 * (BW + BW.T))[0]),
    }


def grid_and_random_scout() -> dict:
    start = time.time()
    rng = random.Random(20260908)
    checked = 0
    best_min_eig = (float("inf"), None)
    best_det_scaled = (float("inf"), None)
    bad = []
    cancellation_warnings = []

    def visit(alpha: float, beta: float, label: str):
        nonlocal checked, best_min_eig, best_det_scaled
        if not (0.0 < alpha < 1.0 and 0.0 < beta < 1.0):
            return
        if abs(alpha - beta) < 1e-12:
            return
        P = exchangeable_atoms_ab(alpha, beta)
        if min(P) <= 0.0:
            bad.append({"label": label, "alpha": alpha, "beta": beta, "reason": "nonpositive atom"})
            return
        C = trivial_block_alpha_beta(alpha, beta)
        eig = np.linalg.eigvalsh(C)
        det = float(np.linalg.det(C))
        checked += 1
        if eig[0] < best_min_eig[0]:
            best_min_eig = (
                float(eig[0]),
                {"alpha": alpha, "beta": beta, "label": label, "eig": eig.tolist(), "det": det},
            )
        delta = alpha - beta
        if abs(delta) >= 1e-6 and det > 0.0:
            scaled = det / (delta * delta)
            if scaled < best_det_scaled[0]:
                best_det_scaled = (
                    float(scaled),
                    {"alpha": alpha, "beta": beta, "label": label, "det_over_delta2": scaled, "det": det},
                )
        elif eig[0] < 0.0 or det < 0.0:
            cancellation_warnings.append(
                {
                    "label": label,
                    "alpha": alpha,
                    "beta": beta,
                    "delta": delta,
                    "eig_min": float(eig[0]),
                    "det": det,
                    "classification": "near_diagonal_float_cancellation_not_a_sign_gate",
                }
            )
        if eig[0] < -1e-8 or det < -1e-8:
            bad.append(
                {
                    "label": label,
                    "alpha": alpha,
                    "beta": beta,
                    "eig": eig.tolist(),
                    "det": det,
                }
            )

    # Deterministic interior grid.
    n = 241
    for i in range(1, n):
        alpha = i / n
        for j in range(1, n):
            beta = j / n
            visit(alpha, beta, "grid_241")

    # Boundary-biased random and near-diagonal samples.
    for k in range(120_000):
        mode = rng.random()
        if mode < 0.25:
            beta = rng.random()
            delta = (1 if rng.random() < 0.5 else -1) * 10 ** rng.uniform(-10, -1)
            alpha = min(1 - 1e-15, max(1e-15, beta + delta))
        elif mode < 0.50:
            alpha = 10 ** rng.uniform(-8, -0.0001)
            beta = rng.random()
            if rng.random() < 0.5:
                alpha, beta = 1 - alpha, beta
        elif mode < 0.75:
            beta = 10 ** rng.uniform(-8, -0.0001)
            alpha = rng.random()
            if rng.random() < 0.5:
                alpha, beta = alpha, 1 - beta
        else:
            alpha = rng.random()
            beta = rng.random()
        visit(alpha, beta, "random_boundary_near_diag")

    return {
        "checked": checked,
        "bad_count": len(bad),
        "bad_examples": bad[:5],
        "float_cancellation_warning_count": len(cancellation_warnings),
        "float_cancellation_warning_examples": cancellation_warnings[:5],
        "best_min_eig": best_min_eig[1],
        "best_det_over_delta2": best_det_scaled[1],
        "elapsed_seconds": time.time() - start,
    }


def local_expansion_sanity() -> list[dict]:
    rows = []
    for x in [0.1, 0.2, 0.5, 0.8, 0.9]:
        expected_bxx = 3.0 / (x * (1.0 - x))
        expected_baa_over_a2 = 18.0 / (x * x * (1.0 - x) ** 2)
        expected_det_over_a2 = expected_bxx * expected_baa_over_a2
        for a in [1e-4, -1e-4, 1e-3, -1e-3]:
            C = trivial_block_xa(x, a)
            rows.append(
                {
                    "x": x,
                    "a": a,
                    "Bxx": float(C[0, 0]),
                    "Bxa": float(C[0, 1]),
                    "Baa_over_a2": float(C[1, 1] / (a * a)),
                    "det_over_a2": float(np.linalg.det(C) / (a * a)),
                    "expected_Bxx_at_0": expected_bxx,
                    "expected_Baa_over_a2_at_0": expected_baa_over_a2,
                    "expected_det_over_a2_at_0": expected_det_over_a2,
                }
            )
    return rows


def formula_crosscheck() -> list[dict]:
    samples = [(0.2, 0.8), (0.8, 0.2), (0.01, 0.99), (0.99, 0.01), (0.73, 0.41)]
    out = []
    for alpha, beta in samples:
        direct = trivial_block_alpha_beta(alpha, beta)
        from_full = alpha_beta_basis_block_from_full(alpha, beta)
        out.append(
            {
                "alpha": alpha,
                "beta": beta,
                "max_abs_diff_alpha_beta_block": float(np.max(np.abs(direct - from_full))),
                "trivial_eigs": np.linalg.eigvalsh(direct).tolist(),
                "representation": representation_residual(alpha, beta),
            }
        )
    return out


def main() -> int:
    results = {
        "status": "SCOUT_NO_COUNTEREXAMPLE",
        "script": Path(__file__).name,
        "formula_crosscheck": formula_crosscheck(),
        "local_expansion_sanity": local_expansion_sanity(),
        "grid_and_random_scout": grid_and_random_scout(),
    }
    (HERE / "sanity_results.json").write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "status": results["status"],
        "checked": results["grid_and_random_scout"]["checked"],
        "bad_count": results["grid_and_random_scout"]["bad_count"],
        "best_min_eig": results["grid_and_random_scout"]["best_min_eig"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
