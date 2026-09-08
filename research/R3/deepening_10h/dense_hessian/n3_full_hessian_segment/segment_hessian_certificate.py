#!/usr/bin/env python3
"""D10-S8 exact-event full-Hessian interval certificate.

The base line is the D10-M8 Section 5 rational commuting line

    K(t) = K0 + t R,
    K0 = (1/5)U + (1/2)V + (4/5)W,
    R  = (1/5)U + (1/3)V + (2/3)W,

where U=J/3, V=ww^T/14, w=(1,2,-3), and W=I-U-V.

For each t-interval, the script bounds the complete 6x6 Hessian of exact-event
Shannon entropy in observation-coordinate Sym(3) directions.  All event jets
are derived from p_S=(-1)^|S^c| det(K-I_{S^c}); logs are enclosed by rational
atanh-series intervals.  The proof gate is strict Gershgorin diagonal dominance
of B(t)=-Hess H(K(t)).
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations
import hashlib
import json
from pathlib import Path
import sys
from typing import Iterable

try:
    import numpy as np
except Exception:  # pragma: no cover - optional scout only
    np = None


HERE = Path(__file__).resolve().parent
COORDS = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
NVAR = len(COORDS)
TAU_DEG = 4   # cubic exact atoms along a 3x3 affine line
H_DEG = 3     # h-degree 0,1,2 is enough for second derivatives
ZERO = F(0)
ONE = F(1)

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def fstr(x: F) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def dec(x: F) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def serialize(obj):
    if isinstance(obj, F):
        return fstr(obj)
    if isinstance(obj, Decimal):
        return str(obj)
    if np is not None and isinstance(obj, np.ndarray):
        return serialize(obj.tolist())
    if np is not None and isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, tuple):
        return [serialize(v) for v in obj]
    if isinstance(obj, list):
        return [serialize(v) for v in obj]
    if isinstance(obj, dict):
        return {str(k): serialize(v) for k, v in obj.items()}
    return obj


def pt_zero() -> list[F]:
    return [ZERO] * TAU_DEG


def pt_const(c: F) -> list[F]:
    return [c] + [ZERO] * (TAU_DEG - 1)


def pt_affine(c0: F, c1: F) -> list[F]:
    return [c0, c1] + [ZERO] * (TAU_DEG - 2)


def pt_add(a: list[F], b: list[F]) -> list[F]:
    return [a[i] + b[i] for i in range(TAU_DEG)]


def pt_sub(a: list[F], b: list[F]) -> list[F]:
    return [a[i] - b[i] for i in range(TAU_DEG)]


def pt_scale(c: F, a: list[F]) -> list[F]:
    return [c * x for x in a]


def pt_mul(a: list[F], b: list[F]) -> list[F]:
    out = [ZERO] * TAU_DEG
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj and i + j < TAU_DEG:
                out[i + j] += ai * bj
    return out


def ph_zero() -> list[list[F]]:
    return [pt_zero() for _ in range(H_DEG)]


def ph_from_h0_h1(h0: list[F], h1: F) -> list[list[F]]:
    return [h0, pt_const(h1), pt_zero()]


def ph_const(c: F) -> list[list[F]]:
    return [pt_const(c), pt_zero(), pt_zero()]


def ph_add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [pt_add(a[i], b[i]) for i in range(H_DEG)]


def ph_scale(c: F, a: list[list[F]]) -> list[list[F]]:
    return [pt_scale(c, a[i]) for i in range(H_DEG)]


def ph_mul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    out = ph_zero()
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            if i + j < H_DEG:
                out[i + j] = pt_add(out[i + j], pt_mul(ai, bj))
    return out


def iadd(a: tuple[F, F], b: tuple[F, F]) -> tuple[F, F]:
    return a[0] + b[0], a[1] + b[1]


def isub(a: tuple[F, F], b: tuple[F, F]) -> tuple[F, F]:
    return a[0] - b[1], a[1] - b[0]


def ineg(a: tuple[F, F]) -> tuple[F, F]:
    return -a[1], -a[0]


def iscale(c: F, a: tuple[F, F]) -> tuple[F, F]:
    if c >= 0:
        return c * a[0], c * a[1]
    return c * a[1], c * a[0]


def imul(a: tuple[F, F], b: tuple[F, F]) -> tuple[F, F]:
    vals = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
    return min(vals), max(vals)


def idiv_pos(a: tuple[F, F], b: tuple[F, F]) -> tuple[F, F]:
    assert b[0] > 0
    return imul(a, (ONE / b[1], ONE / b[0]))


def iabs_upper(a: tuple[F, F]) -> F:
    return max(abs(a[0]), abs(a[1]))


def peval_interval(poly: list[F], x: tuple[F, F]) -> tuple[F, F]:
    out = (poly[-1], poly[-1])
    for c in reversed(poly[:-1]):
        out = iadd(imul(out, x), (c, c))
    return out


def peval_point(poly: list[F], x: F) -> F:
    out = ZERO
    for c in reversed(poly):
        out = out * x + c
    return out


def perm_sign(perm: tuple[int, ...]) -> int:
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inv += int(perm[i] > perm[j])
    return -1 if inv % 2 else 1


def det_ph(matrix: list[list[list[list[F]]]]) -> list[list[F]]:
    n = len(matrix)
    total = ph_zero()
    for perm in permutations(range(n)):
        term = ph_const(F(perm_sign(perm)))
        for i, j in enumerate(perm):
            term = ph_mul(term, matrix[i][j])
        total = ph_add(total, term)
    return total


def mat_add(A: list[list[F]], B: list[list[F]]) -> list[list[F]]:
    return [[A[i][j] + B[i][j] for j in range(3)] for i in range(3)]


def mat_scale(c: F, A: list[list[F]]) -> list[list[F]]:
    return [[c * A[i][j] for j in range(3)] for i in range(3)]


def identity() -> list[list[F]]:
    return [[ONE if i == j else ZERO for j in range(3)] for i in range(3)]


def projectors() -> tuple[list[list[F]], list[list[F]], list[list[F]]]:
    U = [[F(1, 3) for _ in range(3)] for _ in range(3)]
    w = [F(1), F(2), F(-3)]
    V = [[w[i] * w[j] / F(14) for j in range(3)] for i in range(3)]
    I = identity()
    W = [[I[i][j] - U[i][j] - V[i][j] for j in range(3)] for i in range(3)]
    return U, V, W


def m8_section5_line() -> tuple[list[list[F]], list[list[F]]]:
    U, V, W = projectors()
    K0 = mat_add(mat_add(mat_scale(F(1, 5), U), mat_scale(F(1, 2), V)), mat_scale(F(4, 5), W))
    R = mat_add(mat_add(mat_scale(F(1, 5), U), mat_scale(F(1, 3), V)), mat_scale(F(2, 3), W))
    return K0, R


def coordinate_basis() -> list[list[list[F]]]:
    basis = []
    for k, (i, j) in enumerate(COORDS):
        M = [[ZERO for _ in range(3)] for _ in range(3)]
        M[i][j] = ONE
        M[j][i] = ONE
        basis.append(M)
    return basis


def atom_direction_h_polys(K0: list[list[F]], R: list[list[F]], E: list[list[F]], S: int) -> tuple[list[F], list[F], list[F]]:
    """Return p0(t), p_E(t), p_EE(t) polynomials for one exact atom."""
    matrix: list[list[list[list[F]]]] = []
    for i in range(3):
        row = []
        for j in range(3):
            subtract = ONE if i == j and not ((S >> i) & 1) else ZERO
            h0 = pt_affine(K0[i][j] - subtract, R[i][j])
            row.append(ph_from_h0_h1(h0, E[i][j]))
        matrix.append(row)
    detp = det_ph(matrix)
    sign = F((-1) ** (3 - S.bit_count()))
    p0 = pt_scale(sign, detp[0])
    p1 = pt_scale(sign, detp[1])
    p2 = pt_scale(2 * sign, detp[2])
    return p0, p1, p2


@dataclass
class AtomJets:
    p0: list[list[F]]
    p1: list[list[list[F]]]
    pij: list[list[list[list[F]]]]


def build_atom_jets(K0: list[list[F]], R: list[list[F]]) -> AtomJets:
    basis = coordinate_basis()
    zero = [[ZERO for _ in range(3)] for _ in range(3)]
    p0 = [atom_direction_h_polys(K0, R, zero, S)[0] for S in range(8)]
    p1: list[list[list[F]]] = [[pt_zero() for _ in range(8)] for _ in range(NVAR)]
    pii: list[list[list[F]]] = [[pt_zero() for _ in range(8)] for _ in range(NVAR)]
    for i, E in enumerate(basis):
        for S in range(8):
            got = atom_direction_h_polys(K0, R, E, S)
            assert got[0] == p0[S]
            p1[i][S] = got[1]
            pii[i][S] = got[2]
    pij = [[[pt_zero() for _ in range(8)] for _ in range(NVAR)] for _ in range(NVAR)]
    for i in range(NVAR):
        for j in range(i, NVAR):
            if i == j:
                for S in range(8):
                    pij[i][j][S] = pii[i][S]
                    pij[j][i][S] = pii[i][S]
            else:
                Esum = mat_add(basis[i], basis[j])
                for S in range(8):
                    _, _, p2sum = atom_direction_h_polys(K0, R, Esum, S)
                    cross = pt_scale(F(1, 2), pt_sub(pt_sub(p2sum, pii[i][S]), pii[j][S]))
                    pij[i][j][S] = cross
                    pij[j][i][S] = cross
    return AtomJets(p0=p0, p1=p1, pij=pij)


def atanh_log_bounds_unit(y: F, terms: int) -> tuple[F, F]:
    """Bounds log(y) for 1 <= y < 2 using the positive atanh series."""
    assert ONE <= y < 2
    if y == 1:
        return ZERO, ZERO
    z = (y - 1) / (y + 1)
    partial = 2 * sum(z ** (2 * k + 1) / F(2 * k + 1) for k in range(terms))
    tail = 2 * z ** (2 * terms + 1) / (F(2 * terms + 1) * (1 - z * z))
    return partial, partial + tail


@lru_cache(maxsize=None)
def log_bounds_cached(x: F, terms: int) -> tuple[F, F]:
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
    lo, hi = atanh_log_bounds_unit(y, terms)
    # Direct atanh formula for log 2 uses z=(2-1)/(2+1)=1/3.
    z = F(1, 3)
    l2 = 2 * sum(z ** (2 * k + 1) / F(2 * k + 1) for k in range(terms))
    t2 = 2 * z ** (2 * terms + 1) / (F(2 * terms + 1) * (1 - z * z))
    lo2, hi2 = l2, l2 + t2
    if exponent >= 0:
        return lo + exponent * lo2, hi + exponent * hi2
    return lo + exponent * hi2, hi + exponent * lo2


def ilog_pos(a: tuple[F, F], terms: int) -> tuple[F, F]:
    assert a[0] > 0
    lo = log_bounds_cached(a[0], terms)[0]
    hi = log_bounds_cached(a[1], terms)[1]
    return lo, hi


def B_interval_matrix(jets: AtomJets, interval: tuple[F, F], log_terms: int) -> tuple[list[list[tuple[F, F]]], list[tuple[F, F]]]:
    p0_ints = [peval_interval(poly, interval) for poly in jets.p0]
    for p in p0_ints:
        if p[0] <= 0:
            raise ValueError(f"atom interval not positive: {p}")
    log_ints = [ilog_pos(p, log_terms) for p in p0_ints]
    B = [[(ZERO, ZERO) for _ in range(NVAR)] for _ in range(NVAR)]
    for i in range(NVAR):
        for j in range(i, NVAR):
            total = (ZERO, ZERO)
            for S in range(8):
                pi = peval_interval(jets.p1[i][S], interval)
                pj = peval_interval(jets.p1[j][S], interval)
                pij = peval_interval(jets.pij[i][j][S], interval)
                term1 = idiv_pos(imul(pi, pj), p0_ints[S])
                term2 = imul(pij, log_ints[S])
                total = iadd(total, iadd(term1, term2))
            B[i][j] = total
            B[j][i] = total
    return B, p0_ints


def gershgorin_for_B(B: list[list[tuple[F, F]]]) -> dict:
    rows = []
    margins = []
    for i in range(NVAR):
        diag_lower = B[i][i][0]
        off_upper = ZERO
        for j in range(NVAR):
            if i != j:
                off_upper += iabs_upper(B[i][j])
        margin = diag_lower - off_upper
        rows.append({
            "row": i,
            "diag_lower": diag_lower,
            "offdiag_abs_upper": off_upper,
            "margin": margin,
        })
        margins.append(margin)
    return {
        "rows": rows,
        "min_margin": min(margins),
        "all_rows_positive": all(m > 0 for m in margins),
    }


def certify_interval(jets: AtomJets, interval: tuple[F, F], log_terms: int) -> dict:
    B, p0_ints = B_interval_matrix(jets, interval, log_terms)
    gersh = gershgorin_for_B(B)
    return {
        "interval": interval,
        "min_atom_lower": min(p[0] for p in p0_ints),
        "max_atom_upper": max(p[1] for p in p0_ints),
        "gershgorin": gersh,
        "pass": gersh["all_rows_positive"],
    }


def certify_radius(jets: AtomJets, radius: F, log_terms: int, max_depth: int) -> dict:
    queue: list[tuple[F, F, int]] = [(-radius, radius, 0)]
    passed = []
    failed = []
    splits = 0
    while queue:
        a, b, depth = queue.pop()
        try:
            cert = certify_interval(jets, (a, b), log_terms)
            if cert["pass"]:
                passed.append(cert)
                continue
            reason = "gershgorin_not_positive"
        except Exception as exc:
            cert = {"interval": (a, b), "error": repr(exc), "pass": False}
            reason = "exception"
        if depth >= max_depth:
            compact = {
                "interval": cert["interval"],
                "reason": reason,
                "depth": depth,
                "error": cert.get("error"),
            }
            if "min_atom_lower" in cert:
                compact["min_atom_lower"] = cert["min_atom_lower"]
            if "max_atom_upper" in cert:
                compact["max_atom_upper"] = cert["max_atom_upper"]
            if "gershgorin" in cert:
                compact["gershgorin_min_margin"] = cert["gershgorin"]["min_margin"]
                compact["row_margins"] = [r["margin"] for r in cert["gershgorin"]["rows"]]
            failed.append(compact)
        else:
            mid = (a + b) / 2
            queue.append((mid, b, depth + 1))
            queue.append((a, mid, depth + 1))
            splits += 1
    min_margin = min((c["gershgorin"]["min_margin"] for c in passed), default=None)
    min_atom = min((c["min_atom_lower"] for c in passed), default=None)
    return {
        "radius": radius,
        "log_terms": log_terms,
        "max_depth": max_depth,
        "passed": len(passed),
        "failed": len(failed),
        "splits": splits,
        "success": len(failed) == 0 and len(passed) > 0,
        "min_gershgorin_margin": min_margin,
        "min_atom_lower": min_atom,
        "passed_intervals": [
            {
                "interval": c["interval"],
                "min_atom_lower": c["min_atom_lower"],
                "gershgorin_min_margin": c["gershgorin"]["min_margin"],
                "row_margins": [r["margin"] for r in c["gershgorin"]["rows"]],
            }
            for c in sorted(passed, key=lambda x: x["interval"][0])
        ],
        "failed_intervals": failed,
    }


def spectral_margin_for_radius(radius: F) -> F:
    theta = [F(1, 5), F(1, 2), F(4, 5)]
    rate = [F(1, 5), F(1, 3), F(2, 3)]
    lows = [theta[i] - radius * rate[i] for i in range(3)]
    uppers = [ONE - theta[i] - radius * rate[i] for i in range(3)]
    return min(lows + uppers)


def atoms_at_point(jets: AtomJets, t: F) -> list[F]:
    return [peval_point(p, t) for p in jets.p0]


def B_decimal_at(jets: AtomJets, t: F, prec: int = 90) -> list[list[Decimal]]:
    with localcontext() as ctx:
        ctx.prec = prec
        p0s = atoms_at_point(jets, t)
        out = [[Decimal(0) for _ in range(NVAR)] for _ in range(NVAR)]
        for i in range(NVAR):
            for j in range(i, NVAR):
                val = Decimal(0)
                for S in range(8):
                    p0 = p0s[S]
                    pi = peval_point(jets.p1[i][S], t)
                    pj = peval_point(jets.p1[j][S], t)
                    pij = peval_point(jets.pij[i][j][S], t)
                    val += dec(pi * pj / p0) + dec(pij) * ctx.ln(dec(p0))
                out[i][j] = val
                out[j][i] = val
        return out


def float_grid_scout(jets: AtomJets, radius: F, points: int = 81) -> dict:
    if np is None:
        return {"available": False}
    worst = None
    best = None
    for k in range(points):
        t = -radius + F(2 * k, points - 1) * radius
        B = B_decimal_at(jets, t, prec=80)
        Bnp = np.array([[float(x) for x in row] for row in B])
        eig = np.linalg.eigvalsh(Bnp)
        item = {
            "t": t,
            "min_eig_B": float(eig[0]),
            "max_eig_H": float(-eig[0]),
            "max_eig_B": float(eig[-1]),
        }
        if worst is None or item["min_eig_B"] < worst["min_eig_B"]:
            worst = item
        if best is None or item["min_eig_B"] > best["min_eig_B"]:
            best = item
    return {"available": True, "points": points, "worst": worst, "best": best}


def line_nontriviality(K0: list[list[F]], R: list[list[F]]) -> dict:
    offdiag_nonzero = all(K0[i][j] != 0 for i in range(3) for j in range(i + 1, 3))
    diag_values = [K0[i][i] for i in range(3)]
    rate_diag_values = [R[i][i] for i in range(3)]
    return {
        "K0": K0,
        "R": R,
        "K0_diagonal": diag_values,
        "R_diagonal": rate_diag_values,
        "K0_heterogeneous_diagonal": len(set(diag_values)) == 3,
        "K0_all_offdiagonal_nonzero": offdiag_nonzero,
        "spectral_theta": [F(1, 5), F(1, 2), F(4, 5)],
        "spectral_rate": [F(1, 5), F(1, 3), F(2, 3)],
        "strict_feasible_open_interval": [F(-1), F(3, 10)],
    }


def compact_attempt(cert: dict, include_passed_intervals: bool = False) -> dict:
    out = {
        "radius": cert.get("radius"),
        "success": cert.get("success"),
        "passed": cert.get("passed"),
        "failed": cert.get("failed"),
        "splits": cert.get("splits"),
        "log_terms": cert.get("log_terms"),
        "max_depth": cert.get("max_depth"),
        "spectral_margin": cert.get("spectral_margin"),
        "min_gershgorin_margin": cert.get("min_gershgorin_margin"),
        "min_atom_lower": cert.get("min_atom_lower"),
    }
    if include_passed_intervals:
        out["passed_intervals"] = cert.get("passed_intervals", [])
    if cert.get("failed"):
        out["failed_intervals"] = cert.get("failed_intervals", [])
    if cert.get("reason"):
        out["reason"] = cert.get("reason")
    return out


def main() -> int:
    K0, R = m8_section5_line()
    jets = build_atom_jets(K0, R)
    # Exact atom sanity: probabilities sum to one and first/second derivative
    # total masses vanish as polynomials in t.
    atom_sum_poly = pt_zero()
    for p in jets.p0:
        atom_sum_poly = pt_add(atom_sum_poly, p)
    p1_sums = []
    pij_sums = []
    for i in range(NVAR):
        s = pt_zero()
        for S in range(8):
            s = pt_add(s, jets.p1[i][S])
        p1_sums.append(s)
    for i in range(NVAR):
        row = []
        for j in range(NVAR):
            s = pt_zero()
            for S in range(8):
                s = pt_add(s, jets.pij[i][j][S])
            row.append(s)
        pij_sums.append(row)

    log_terms = 20
    max_depth = 10
    radii = [F(1, 100), F(1, 50), F(1, 20), F(1, 10), F(1, 5), F(6, 25), F(49, 200), F(1, 4)]
    attempts = []
    for radius in radii:
        if spectral_margin_for_radius(radius) <= 0:
            attempts.append({
                "radius": radius,
                "success": False,
                "failed": 1,
                "reason": "closed symmetric interval not strictly feasible",
                "spectral_margin": spectral_margin_for_radius(radius),
            })
            continue
        cert = certify_radius(jets, radius, log_terms=log_terms, max_depth=max_depth)
        cert["spectral_margin"] = spectral_margin_for_radius(radius)
        attempts.append(cert)

    success_attempts = [a for a in attempts if a.get("success")]
    largest = max(success_attempts, key=lambda x: x["radius"]) if success_attempts else None
    endpoint_report = {}
    endpoint_radius = largest["radius"] if largest else F(1, 100)
    for t in [-endpoint_radius, ZERO, endpoint_radius]:
        B = B_decimal_at(jets, t)
        if np is not None:
            eig = np.linalg.eigvalsh(np.array([[float(x) for x in row] for row in B]))
            endpoint_report[fstr(t)] = {
                "min_atom": min(atoms_at_point(jets, t)),
                "min_eig_B_float": float(eig[0]),
                "max_eig_H_float": float(-eig[0]),
            }
        else:
            endpoint_report[fstr(t)] = {"min_atom": min(atoms_at_point(jets, t))}
    failed_float_scouts = {}
    for a in attempts:
        if not a.get("success") and "radius" in a and spectral_margin_for_radius(a["radius"]) > 0:
            failed_float_scouts[fstr(a["radius"])] = float_grid_scout(jets, a["radius"], points=201)

    report = {
        "status": "PROOF_CANDIDATE_PENDING_FRESH_REVIEW" if largest else "SCOUT_BLOCKED",
        "method": "exact-event polynomial jets, rational log intervals, adaptive rational interval subdivision, Gershgorin positivity of B=-Hess(H)",
        "coordinate_order": COORDS,
        "line": line_nontriviality(K0, R),
        "sanity": {
            "atom_sum_poly_equals_one": atom_sum_poly == [ONE, ZERO, ZERO, ZERO],
            "p1_total_mass_derivatives_zero": all(s == [ZERO, ZERO, ZERO, ZERO] for s in p1_sums),
            "pij_total_mass_derivatives_zero": all(
                pij_sums[i][j] == [ZERO, ZERO, ZERO, ZERO] for i in range(NVAR) for j in range(NVAR)
            ),
        },
        "log_terms": log_terms,
        "max_depth": max_depth,
        "attempted_radii": [
            compact_attempt(a, include_passed_intervals=(largest is not None and a.get("radius") == largest["radius"]))
            for a in attempts
        ],
        "largest_certified_radius": largest["radius"] if largest else None,
        "largest_certified_interval": [-largest["radius"], largest["radius"]] if largest else None,
        "largest_certified_min_margin": largest["min_gershgorin_margin"] if largest else None,
        "largest_certified_min_atom_lower": largest["min_atom_lower"] if largest else None,
        "endpoint_decimal_scout": endpoint_report,
        "failed_radius_float_grid_scouts": failed_float_scouts,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    out = HERE / "segment_certificate.json"
    out.write_text(json.dumps(serialize(report), indent=2), encoding="utf-8")
    summary = {
        "status": report["status"],
        "json": str(out),
        "largest_certified_radius": report["largest_certified_radius"],
        "largest_certified_interval": report["largest_certified_interval"],
        "largest_certified_min_margin_decimal": dec(report["largest_certified_min_margin"]) if largest else None,
        "largest_certified_min_atom_lower": report["largest_certified_min_atom_lower"],
        "attempts": [
            {
                "radius": a.get("radius"),
                "success": a.get("success"),
                "passed_intervals": a.get("passed"),
                "failed_intervals": a.get("failed"),
                "min_margin_decimal": dec(a["min_gershgorin_margin"]) if a.get("success") else None,
                "spectral_margin": a.get("spectral_margin"),
            }
            for a in attempts
        ],
        "sanity": report["sanity"],
    }
    print(json.dumps(serialize(summary), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
