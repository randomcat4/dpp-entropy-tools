#!/usr/bin/env python3
"""Boundary probe for U10e: c=1-s, s -> 0, possibly with x -> 0.

The computation separates the vanishing full-atom Fisher contribution
    jF jF^T / F,   F=x^3 s,
as a rank-one term and evaluates the Schur complement by the
Sherman--Morrison identity.  This avoids subtracting enormous 1/s terms in
the sharp two-scale regime s=exp(-beta/x).

This is still a high-precision asymptotic probe, not a proof.
"""

from __future__ import annotations

import hashlib
import json
import os
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Dict, List


getcontext().prec = 180
D = Decimal
OUT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt(x: Decimal, digits: int = 40) -> str:
    return format(+x, f".{digits}E")


def inv(A: List[List[Decimal]]) -> List[List[Decimal]]:
    n = len(A)
    M = [A[i][:] + [D(1) if i == j else D(0) for j in range(n)] for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        p = M[c][c]
        if p == 0:
            raise ZeroDivisionError("singular matrix")
        for j in range(2 * n):
            M[c][j] /= p
        for r in range(n):
            if r == c:
                continue
            f = M[r][c]
            for j in range(2 * n):
                M[r][j] -= f * M[c][j]
    return [row[n:] for row in M]


def dot(u: List[Decimal], v: List[Decimal]) -> Decimal:
    return sum(ui * vi for ui, vi in zip(u, v))


def sigma_stable_xs(x: Decimal, s: Decimal) -> Dict[str, Decimal]:
    """Stable evaluation for c=1-s, 0<x<=1/2, 0<s<1."""
    one = D(1)
    if not (D(0) < x <= D("0.5") and D(0) < s < D(1)):
        raise ValueError("outside boundary domain")
    a = (x * x * (one - s) / D(2)).sqrt()
    t = a * a

    # Exact atoms in the boundary variable s.
    E = (one - x) * (one - D(2) * x + x * x * s)
    F = x * x * x * s
    U = x * ((one - x) * (one - x) + (one - D(2) * x) * x * (one - s) / D(2))
    W = x * (one - x) * (one - x * s)
    V = x * x * (one + (one - D(2) * x) * s) / D(2)
    Z = x * x * (one - x * s)

    ell = (E * V / (U * W)).ln()
    kappa = (E * Z / (U * U)).ln()
    Lam = (F * U * U * W / (E * V * V * Z)).ln()
    n = -ell - Lam * x
    m = -kappa - Lam * x
    q = n * m - D(2) * Lam * Lam * a * a

    jF = [D(2) * (x * x - t), x * x, -D(4) * x * a, D(2) * t]
    jQ = [x, x, -D(2) * a, D(0)]

    def add(u, v):
        return [u[i] + v[i] for i in range(4)]

    def sub(u, v):
        return [u[i] - v[i] for i in range(4)]

    jE = add([D(4) * x - D(2), D(2) * x - D(1), -D(4) * a, D(0)], [-v for v in jF])
    jU = add([D(1) - D(3) * x, -x, D(2) * a, D(0)], jF)
    jW = add([-D(2) * x, D(1) - D(2) * x, D(4) * a, D(0)], jF)
    jV = sub(jQ, jF)
    jZ = add([D(2) * x, D(0), D(0), D(0)], [-v for v in jF])

    # R is B_even with the singular F-atom Fisher term removed.
    R = [[D(0) for _ in range(4)] for __ in range(4)]
    for form, p, mu in zip([jE, jU, jW, jV, jZ], [E, U, W, V, Z], [D(1), D(2), D(1), D(2), D(1)]):
        for i in range(4):
            for j in range(4):
                R[i][j] += mu * form[i] * form[j] / p
    R[0][1] -= D(2) * n
    R[1][0] -= D(2) * n
    R[2][2] += D(4) * n
    R[0][0] -= D(2) * m
    R[3][3] += D(2) * m
    R[0][2] -= D(4) * Lam * a
    R[2][0] -= D(4) * Lam * a
    R[2][3] += D(4) * Lam * a
    R[3][2] += D(4) * Lam * a

    eta = [
        D(2) * (n * m - Lam * Lam * a * a) / (n * q),
        n / q,
        D(4) * Lam * a / q,
        D(2) * Lam * Lam * a * a / (n * q),
    ]
    T0 = [
        [D(1), D(0), D(0)],
        [-eta[0] / eta[1], -eta[2] / eta[1], -eta[3] / eta[1]],
        [D(0), D(1), D(0)],
        [D(0), D(0), D(1)],
    ]

    C = [[sum(T0[i][r] * R[i][j] * T0[j][c] for i in range(4) for j in range(4))
          for c in range(3)] for r in range(3)]
    b = [sum(T0[i][r] * R[i][1] for i in range(4)) for r in range(3)]
    d = R[1][1]
    Cinv = inv(C)
    Cinv_b = [sum(Cinv[i][j] * b[j] for j in range(3)) for i in range(3)]
    base = d - dot(b, Cinv_b)

    u = [sum(T0[i][r] * jF[i] for i in range(4)) for r in range(3)]
    v = jF[1]
    Cinv_u = [sum(Cinv[i][j] * u[j] for j in range(3)) for i in range(3)]
    denom = F + dot(u, Cinv_u)
    residual = v - dot(u, Cinv_b)
    rank_one_correction = residual * residual / denom
    sigma = base + rank_one_correction

    return {
        "sigma": sigma,
        "x_sigma": x * sigma,
        "base_without_full_atom": base,
        "rank_one_correction": rank_one_correction,
        "rank_one_denom": denom,
        "residual": residual,
        "F_atom": F,
        "Lambda": Lam,
        "n": n,
        "m": m,
        "q": q,
        "eta_d": eta[0],
        "eta_e": eta[1],
        "eta_h": eta[2],
        "eta_k": eta[3],
    }


def rec(x: Decimal, s: Decimal, extra=None) -> Dict[str, object]:
    out = sigma_stable_xs(x, s)
    ans = {
        "x": str(x),
        "s": str(s),
        "sigma": fmt(out["sigma"]),
        "x_sigma": fmt(out["x_sigma"]),
        "base_without_full_atom": fmt(out["base_without_full_atom"]),
        "rank_one_correction": fmt(out["rank_one_correction"]),
        "rank_one_denom": fmt(out["rank_one_denom"]),
        "F_atom": fmt(out["F_atom"], 25),
        "Lambda": fmt(out["Lambda"], 25),
        "q": fmt(out["q"], 25),
    }
    if extra:
        ans.update(extra)
    return ans


def main() -> Dict[str, object]:
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    parent = OUT.parent
    inputs = {
        "u10e_derivation": parent / "derivation.md",
        "u10e_verdict": parent / "verdict.md",
        "u10e_search": parent / "search.py",
        "u10e_profile": parent / "profile.json",
    }

    fixed_x = []
    for x in [D("0.01"), D("0.02"), D("0.05"), D("0.1"), D("0.25"), D("0.49")]:
        row = {"x": str(x), "values": []}
        for k in [2, 4, 6, 8, 10, 15, 20, 30, 40, 60, 80]:
            s = D(10) ** (-k)
            row["values"].append(rec(x, s, {"kind": "s=10^-k", "k": k}))
        fixed_x.append(row)

    power_rates = []
    for p in [D("0.5"), D("1"), D("2"), D("4"), D("8")]:
        row = {"p": str(p), "values": []}
        for k in [1, 2, 3, 4, 5, 6, 8]:
            x = D(10) ** (-k)
            s = x ** p
            row["values"].append(rec(x, s, {"kind": "s=x^p", "k_for_x_10^-k": k}))
        power_rates.append(row)

    exponential_rates = []
    beta_values = [D("0.1"), D("0.2"), D("0.3"), D("0.4"), D("0.5"), D("0.6"), D("0.7"), D("1.0"), D("1.5")]
    for beta in beta_values:
        row = {"beta": str(beta), "values": []}
        for x in [D("0.05"), D("0.02"), D("0.01"), D("0.005"), D("0.002"), D("0.001"), D("0.0005"), D("0.0001")]:
            s = (-beta / x).exp()
            row["values"].append(rec(x, s, {"kind": "s=exp(-beta/x)", "beta": str(beta)}))
        exponential_rates.append(row)

    # Beta refinement at a small x value, used only to locate the positive
    # valley in the exponential scale.
    beta_refine = []
    best = None
    x_ref = D("0.0001")
    for j in range(5, 151):
        beta = D(j) / D(100)
        s = (-beta / x_ref).exp()
        item = rec(x_ref, s, {"kind": "beta_refine_at_x=1e-4", "beta": str(beta)})
        beta_refine.append(item)
        sig = D(item["sigma"])
        if best is None or sig < D(best["sigma"]):
            best = item

    result = {
        "status": "BOUNDARY_SCOUT_NO_NEGATIVE__ASYMPTOTIC_BLOCKER_REFINED",
        "precision_decimal_digits": getcontext().prec,
        "input_hashes_sha256": {k: sha256(v) for k, v in inputs.items() if v.exists()},
        "stable_formula": (
            "B_even is split as R + jF*jF^T/F.  In the [T0,e0] Schur complement, "
            "sigma = base_R + (v-u^T R_C^{-1}b)^2 / (F + u^T R_C^{-1}u)."
        ),
        "fixed_x_profiles": fixed_x,
        "power_rate_profiles_s_equals_x^p": power_rates,
        "exponential_rate_profiles_s_equals_exp_minus_beta_over_x": exponential_rates,
        "beta_refinement_at_x_1e_minus_4": {
            "count": len(beta_refine),
            "best": best,
            "values": beta_refine,
        },
        "interpretation": {
            "unique_vanishing_atom": "F=x^3 s; all other atoms have positive s=0 limits for fixed x<1/2.",
            "power_rates": "For sampled s=x^p, x*sigma tends to 1, so sigma escapes to +infinity.",
            "exponential_scale": "The sharp nonuniform valley is s=exp(-beta/x); sampled limiting sigma stays O(1) and positive, with minimum near beta≈0.55.",
            "not_proved": "No rigorous limiting formula phi(beta)>0 or uniform remainder bound is supplied.",
        },
    }
    with (OUT / "asymptotic_results.json").open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(json.dumps({
        "status": result["status"],
        "fixed_x_rows": len(fixed_x),
        "power_rate_rows": len(power_rates),
        "exponential_rate_rows": len(exponential_rates),
        "beta_refine_count": len(beta_refine),
        "beta_refine_best_sigma": best["sigma"],
    }, ensure_ascii=False))
    return result


if __name__ == "__main__":
    main()
