#!/usr/bin/env python3
"""D10-U10e independent sigma attack for the symmetric path family.

Domain:
    0 < x <= 1/2, 0 < a < x/sqrt(2).

The script uses the U10d exact-event reduction but recomputes the even-block
Hessian from the atom formulas and the six event-derivative linear forms.
It does not import author sanity scripts.  The output is a high-precision
profile and a set of boundary probes; it is not an interval proof.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


getcontext().prec = 120
D = Decimal
OUT = Path(__file__).resolve().parent


def dec_frac(num: int, den: int = 1) -> Decimal:
    return D(num) / D(den)


def dstr(x: Decimal, digits: int = 50) -> str:
    return format(+x, f".{digits}E")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def atoms_xc(x: Decimal, c: Decimal) -> Dict[str, Decimal]:
    """Atoms for c=2a^2/x^2 in (0,1)."""
    one = D(1)
    t = c * x * x / D(2)
    E = (one - x) * ((one - x) * (one - x) - D(2) * t)
    F = x * (x * x - D(2) * t)
    U = x * (one - x) * (one - x) + (one - D(2) * x) * t
    W = x * (one - x) * (one - x) + D(2) * (one - x) * t
    V = x * x * (one - x) + (D(2) * x - one) * t
    Z = x * x * (one - x) + D(2) * x * t
    return {"E": E, "U": U, "W": W, "V": V, "Z": Z, "F": F}


def mat_inv(A: List[List[Decimal]]) -> List[List[Decimal]]:
    n = len(A)
    M = [A[i][:] + [D(1) if i == j else D(0) for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        p = M[col][col]
        if not p:
            raise ZeroDivisionError("singular matrix in sigma Schur complement")
        for j in range(2 * n):
            M[col][j] /= p
        for row in range(n):
            if row == col:
                continue
            f = M[row][col]
            for j in range(2 * n):
                M[row][j] -= f * M[col][j]
    return [row[n:] for row in M]


def ldl_pivots(A: List[List[Decimal]]) -> List[Decimal]:
    n = len(A)
    L = [[D(0) for _ in range(n)] for _ in range(n)]
    piv = [D(0) for _ in range(n)]
    for i in range(n):
        for j in range(i):
            s = sum(L[i][k] * L[j][k] * piv[k] for k in range(j))
            L[i][j] = (A[i][j] - s) / piv[j]
        piv[i] = A[i][i] - sum(L[i][k] * L[i][k] * piv[k] for k in range(i))
        L[i][i] = D(1)
    return piv


def det4(A: List[List[Decimal]]) -> Decimal:
    M = [row[:] for row in A]
    det = D(1)
    n = 4
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if M[piv][col] == 0:
            return D(0)
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
            det = -det
        p = M[col][col]
        det *= p
        for row in range(col + 1, n):
            f = M[row][col] / p
            for j in range(col, n):
                M[row][j] -= f * M[col][j]
    return det


def sigma_xc(x: Decimal, c: Decimal) -> Dict[str, Decimal]:
    """Return sigma and diagnostics for c=2a^2/x^2."""
    if not (D(0) < x <= D("0.5") and D(0) < c < D(1)):
        raise ValueError("outside reduced domain")
    atoms = atoms_xc(x, c)
    if min(atoms.values()) <= 0:
        raise ValueError("nonpositive atom")
    a = (x * x * c / D(2)).sqrt()
    t = a * a
    E, U, W, V, Z, F = (atoms[k] for k in ["E", "U", "W", "V", "Z", "F"])
    ell = (E * V / (U * W)).ln()
    kappa = (E * Z / (U * U)).ln()
    Lam = (F * U * U * W / (E * V * V * Z)).ln()
    n = -ell - Lam * x
    m = -kappa - Lam * x
    q = n * m - D(2) * Lam * Lam * a * a

    # Linear forms in even coordinates (d,e,h,k).
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
    forms = [jE, jU, jW, jV, jZ, jF]
    probs = [E, U, W, V, Z, F]
    mult = [D(1), D(2), D(1), D(2), D(1), D(1)]

    B = [[D(0) for _ in range(4)] for _ in range(4)]
    for form, p, mu in zip(forms, probs, mult):
        for i in range(4):
            for j in range(4):
                B[i][j] += mu * form[i] * form[j] / p
    B[0][1] -= D(2) * n
    B[1][0] -= D(2) * n
    B[2][2] += D(4) * n
    B[0][0] -= D(2) * m
    B[3][3] += D(2) * m
    B[0][2] -= D(4) * Lam * a
    B[2][0] -= D(4) * Lam * a
    B[2][3] += D(4) * Lam * a
    B[3][2] += D(4) * Lam * a

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
    C0 = [[sum(T0[i][r] * B[i][j] * T0[j][col] for i in range(4) for j in range(4))
           for col in range(3)] for r in range(3)]
    b0 = [sum(T0[i][r] * B[i][1] for i in range(4)) for r in range(3)]
    invC0 = mat_inv(C0)
    sigma = B[1][1] - sum(b0[i] * invC0[i][j] * b0[j] for i in range(3) for j in range(3))
    return {
        "sigma": sigma,
        "sigma_minus_4": sigma - D(4),
        "x": x,
        "c": c,
        "a": a,
        "min_atom": min(atoms.values()),
        "n": n,
        "m": m,
        "Lambda": Lam,
        "q": q,
        "C0_pivots": ldl_pivots(C0),
        "B_even_det": det4(B),
    }


def sigma_float(x: float, c: float) -> float:
    """Fast scout copy of sigma_xc, double precision only."""
    a = x * math.sqrt(c / 2.0)
    t = a * a
    E = (1 - x) * ((1 - x) ** 2 - 2 * t)
    F = x * (x * x - 2 * t)
    U = x * (1 - x) ** 2 + (1 - 2 * x) * t
    W = x * (1 - x) ** 2 + 2 * (1 - x) * t
    V = x * x * (1 - x) + (2 * x - 1) * t
    Z = x * x * (1 - x) + 2 * x * t
    if min(E, F, U, W, V, Z) <= 0:
        return math.nan
    ell = math.log(E * V / (U * W))
    kappa = math.log(E * Z / (U * U))
    Lam = math.log(F * U * U * W / (E * V * V * Z))
    n = -ell - Lam * x
    m = -kappa - Lam * x
    q = n * m - 2 * Lam * Lam * a * a
    eta = [2 * (n * m - Lam * Lam * a * a) / (n * q), n / q, 4 * Lam * a / q, 2 * Lam * Lam * a * a / (n * q)]
    jF = [2 * (x * x - t), x * x, -4 * x * a, 2 * t]
    jQ = [x, x, -2 * a, 0.0]
    add = lambda u, v: [u[i] + v[i] for i in range(4)]
    sub = lambda u, v: [u[i] - v[i] for i in range(4)]
    jE = add([4 * x - 2, 2 * x - 1, -4 * a, 0], [-v for v in jF])
    jU = add([1 - 3 * x, -x, 2 * a, 0], jF)
    jW = add([-2 * x, 1 - 2 * x, 4 * a, 0], jF)
    jV = sub(jQ, jF)
    jZ = add([2 * x, 0, 0, 0], [-v for v in jF])
    B = [[0.0] * 4 for _ in range(4)]
    for form, p, mu in zip([jE, jU, jW, jV, jZ, jF], [E, U, W, V, Z, F], [1, 2, 1, 2, 1, 1]):
        for i in range(4):
            for j in range(4):
                B[i][j] += mu * form[i] * form[j] / p
    B[0][1] -= 2 * n
    B[1][0] -= 2 * n
    B[2][2] += 4 * n
    B[0][0] -= 2 * m
    B[3][3] += 2 * m
    B[0][2] -= 4 * Lam * a
    B[2][0] -= 4 * Lam * a
    B[2][3] += 4 * Lam * a
    B[3][2] += 4 * Lam * a
    T0 = [[1, 0, 0], [-eta[0] / eta[1], -eta[2] / eta[1], -eta[3] / eta[1]], [0, 1, 0], [0, 0, 1]]
    C0 = [[sum(T0[i][r] * B[i][j] * T0[j][col] for i in range(4) for j in range(4)) for col in range(3)] for r in range(3)]
    b = [sum(T0[i][r] * B[i][1] for i in range(4)) for r in range(3)]
    inv = [[0.0] * 3 for _ in range(3)]
    M = [C0[i][:] + [1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    for col in range(3):
        piv = max(range(col, 3), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        p = M[col][col]
        if abs(p) < 1e-300:
            return math.nan
        for j in range(6):
            M[col][j] /= p
        for row in range(3):
            if row != col:
                f = M[row][col]
                for j in range(6):
                    M[row][j] -= f * M[col][j]
    inv = [row[3:] for row in M]
    return B[1][1] - sum(b[i] * inv[i][j] * b[j] for i in range(3) for j in range(3))


def powers10(kmax: int) -> List[Decimal]:
    return [D(10) ** (-k) for k in range(1, kmax + 1)]


def update_best(best: Dict[str, object] | None, rec: Dict[str, Decimal], tag: str) -> Dict[str, object]:
    item = {
        "tag": tag,
        "x": dstr(rec["x"], 40),
        "c": dstr(rec["c"], 40),
        "a": dstr(rec["a"], 40),
        "sigma": dstr(rec["sigma"], 50),
        "sigma_minus_4": dstr(rec["sigma_minus_4"], 50),
        "min_atom": dstr(rec["min_atom"], 30),
        "q": dstr(rec["q"], 30),
        "C0_pivots": [dstr(v, 30) for v in rec["C0_pivots"]],
        "B_even_det": dstr(rec["B_even_det"], 30),
    }
    if best is None or rec["sigma"] < D(str(best["sigma_decimal_raw"])):
        item["sigma_decimal_raw"] = str(rec["sigma"])
        return item
    return best


def main() -> Dict[str, object]:
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    input_paths = {
        "u10d_audit_verdict": OUT.parent / "symmetric_path_subfamily/audit_nonauthor/verdict.md",
        "u10d_derivation": OUT.parent / "symmetric_path_subfamily/derivation.md",
    }
    hashes = {k: sha256(v) for k, v in input_paths.items() if v.exists()}

    # High-precision two-dimensional profile in reduced coordinates (x,c).
    x_values = {dec_frac(i, 240) for i in range(1, 121)}
    c_values = {dec_frac(j, 160) for j in range(1, 160)}
    for eps in powers10(12):
        x_values.add(eps)
        if eps < D("0.5"):
            x_values.add(D("0.5") - eps)
        c_values.add(eps)
        c_values.add(D(1) - eps)
    x_values = sorted(v for v in x_values if D(0) < v <= D("0.5"))
    c_values = sorted(v for v in c_values if D(0) < v < D(1))

    best = None
    negative_hits = []
    count = 0
    for x in x_values:
        for c in c_values:
            rec = sigma_xc(x, c)
            count += 1
            if rec["sigma"] <= 0:
                negative_hits.append({"x": str(x), "c": str(c), "sigma": str(rec["sigma"])})
            best = update_best(best, rec, "grid")

    # Deterministic float scout with log-biased boundary draws.  Top hits are
    # re-evaluated by Decimal.
    rng = random.Random(20260908)
    scout_count = 120000
    float_best = (float("inf"), None)
    float_negative = []
    for _ in range(scout_count):
        mode = rng.randrange(4)
        if mode == 0:
            x = 0.5 * (10 ** (-8 * rng.random()))
        elif mode == 1:
            x = 0.5 - 0.5 * (10 ** (-8 * rng.random()))
        else:
            x = 0.5 * rng.random()
        if mode == 2:
            c = 10 ** (-8 * rng.random())
        elif mode == 3:
            c = 1 - 10 ** (-8 * rng.random())
        else:
            c = rng.random()
        if not (0 < x <= 0.5 and 0 < c < 1):
            continue
        try:
            s = sigma_float(x, c)
        except (ZeroDivisionError, ValueError, OverflowError):
            continue
        if math.isfinite(s) and s < float_best[0]:
            float_best = (s, (x, c))
        if math.isfinite(s) and s <= 0:
            float_negative.append((s, x, c))
            break
    float_best_decimal = None
    if float_best[1] is not None:
        x, c = float_best[1]
        float_best_decimal = update_best(None, sigma_xc(D(str(x)), D(str(c))), "float_best_recheck")

    # Boundary profiles.
    x_probe = [D("0.000001"), D("0.0001"), D("0.01"), D("0.05"), D("0.1"), D("0.25"), D("0.49"), D("0.5")]
    c_probe = [D("0.000001"), D("0.01"), D("0.25"), D("0.81"), D("0.9801"), D("0.999999")]
    boundary = {
        "a_to_zero_c_10^-k": [],
        "spectral_boundary_c_1_minus_10^-k": [],
        "x_to_zero": [],
        "x_to_half": [],
    }
    for x in [D("0.1"), D("0.25"), D("0.49"), D("0.5")]:
        row = {"x": str(x), "limit_1_over_x1mx": dstr(D(1) / (x * (D(1) - x)), 40), "values": []}
        for c in powers10(8):
            rec = sigma_xc(x, c)
            row["values"].append({"c": str(c), "sigma": dstr(rec["sigma"], 40), "sigma_minus_limit": dstr(rec["sigma"] - D(1) / (x * (D(1) - x)), 30)})
        boundary["a_to_zero_c_10^-k"].append(row)
    for x in [D("0.01"), D("0.05"), D("0.1"), D("0.25"), D("0.49")]:
        row = {"x": str(x), "values": []}
        for eps in powers10(10):
            rec = sigma_xc(x, D(1) - eps)
            row["values"].append({"epsilon": str(eps), "sigma": dstr(rec["sigma"], 40), "min_atom": dstr(rec["min_atom"], 25)})
        boundary["spectral_boundary_c_1_minus_10^-k"].append(row)
    for x in powers10(8):
        row = {"x": str(x), "values": []}
        for c in c_probe:
            rec = sigma_xc(x, c)
            row["values"].append({"c": str(c), "x_times_sigma": dstr(x * rec["sigma"], 35), "sigma": dstr(rec["sigma"], 35)})
        boundary["x_to_zero"].append(row)
    for eps in powers10(8):
        x = D("0.5") - eps
        row = {"half_minus_x": str(eps), "values": []}
        for c in [D("0.01"), D("0.25"), D("0.81"), D("0.999999")]:
            rec = sigma_xc(x, c)
            row["values"].append({"c": str(c), "sigma": dstr(rec["sigma"], 35)})
        boundary["x_to_half"].append(row)

    result = {
        "status": "NO_NEGATIVE_SIGMA_FOUND__GLOBAL_PROOF_INCOMPLETE",
        "precision_decimal_digits": getcontext().prec,
        "reduced_domain": "0<x<=1/2, 0<c=2a^2/x^2<1, a=x*sqrt(c/2)>0",
        "input_hashes_sha256": hashes,
        "grid_denominator": {
            "x_count": len(x_values),
            "c_count": len(c_values),
            "evaluations": count,
            "negative_hits": len(negative_hits),
        },
        "best_grid": best,
        "float_scout": {
            "seed": 20260908,
            "proposals": scout_count,
            "negative_hits": len(float_negative),
            "best_float": None if float_best[1] is None else {"sigma": float_best[0], "x": float_best[1][0], "c": float_best[1][1]},
            "best_decimal_recheck": float_best_decimal,
        },
        "boundary_profiles": boundary,
        "minimal_open_inequality": (
            "With C0>0 from the reviewed weighted-trace-zero theorem, prove "
            "sigma(x,c)>0 for 0<x<=1/2 and 0<c<1.  Equivalently prove "
            "det(B_even(x,c))>0, since det(B_even)=det(C0)*sigma in the "
            "basis [ker eta, e0]."
        ),
        "not_a_proof": "The grid and scout are finite high-precision evidence only; no interval derivative bound is supplied here.",
    }
    with (OUT / "profile.json").open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(json.dumps({
        "status": result["status"],
        "evaluations": count,
        "negative_hits": len(negative_hits),
        "best_sigma": best["sigma"],
        "output": str(OUT / "profile.json"),
    }, ensure_ascii=False))
    return result


if __name__ == "__main__":
    main()
