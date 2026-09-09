#!/usr/bin/env python3
"""Strict finite-box Hessian certificates for the fixed 5x3 U.

The proof-producing path in this file uses Python integers/Fraction only:
probability polynomials, interval arithmetic, log enclosures, and final
Gershgorin inequalities are all rational. Floating point is used only to choose
preconditioners and to display approximate eigenvalues.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import platform
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

NVAR = 6
COORDS = ["a11", "a22", "a33", "a12", "a13", "a23"]
PAIR_INDEX = [(i, j) for i in range(NVAR) for j in range(i, NVAR)]


def parse_q(value) -> Fraction:
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    raise TypeError(f"cannot parse rational from {value!r}")


def qstr(q: Fraction) -> str:
    if q.denominator == 1:
        return str(q.numerator)
    return f"{q.numerator}/{q.denominator}"


def dec(q: Fraction, digits: int = 18) -> str:
    return f"{float(q):.{digits}g}"


@dataclass(frozen=True)
class Iv:
    lo: Fraction
    hi: Fraction

    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError("empty interval")

    @staticmethod
    def point(x: Fraction) -> "Iv":
        return Iv(x, x)

    def __add__(self, other: "Iv") -> "Iv":
        return Iv(self.lo + other.lo, self.hi + other.hi)

    def __neg__(self) -> "Iv":
        return Iv(-self.hi, -self.lo)

    def __sub__(self, other: "Iv") -> "Iv":
        return self + (-other)

    def __mul__(self, other: "Iv") -> "Iv":
        vals = [
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        ]
        return Iv(min(vals), max(vals))

    def scale(self, c: Fraction) -> "Iv":
        if c >= 0:
            return Iv(c * self.lo, c * self.hi)
        return Iv(c * self.hi, c * self.lo)

    def inv(self) -> "Iv":
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError(f"interval contains zero: {self}")
        vals = [Fraction(1, self.lo), Fraction(1, self.hi)]
        return Iv(min(vals), max(vals))

    def div(self, other: "Iv") -> "Iv":
        return self * other.inv()

    def abs_upper(self) -> Fraction:
        return max(abs(self.lo), abs(self.hi))

    def width(self) -> Fraction:
        return self.hi - self.lo

    def to_json(self) -> Dict[str, str]:
        return {
            "lo": qstr(self.lo),
            "hi": qstr(self.hi),
            "lo_decimal": dec(self.lo),
            "hi_decimal": dec(self.hi),
        }


ZERO_IV = Iv.point(Fraction(0))


class Poly:
    __slots__ = ("terms",)

    def __init__(self, terms: Dict[Tuple[int, ...], Fraction] | None = None):
        out: Dict[Tuple[int, ...], Fraction] = {}
        if terms:
            for mon, coeff in terms.items():
                coeff = Fraction(coeff)
                if coeff:
                    if len(mon) != NVAR:
                        raise ValueError("bad monomial length")
                    out[tuple(mon)] = out.get(tuple(mon), Fraction(0)) + coeff
        self.terms = {m: c for m, c in out.items() if c}

    @staticmethod
    def const(c: Fraction) -> "Poly":
        return Poly({(0,) * NVAR: Fraction(c)}) if c else Poly()

    @staticmethod
    def var(i: int) -> "Poly":
        mon = [0] * NVAR
        mon[i] = 1
        return Poly({tuple(mon): Fraction(1)})

    def __add__(self, other: "Poly") -> "Poly":
        terms = dict(self.terms)
        for mon, coeff in other.terms.items():
            terms[mon] = terms.get(mon, Fraction(0)) + coeff
            if not terms[mon]:
                del terms[mon]
        return Poly(terms)

    def __neg__(self) -> "Poly":
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other: "Poly") -> "Poly":
        return self + (-other)

    def __mul__(self, other: "Poly") -> "Poly":
        terms: Dict[Tuple[int, ...], Fraction] = {}
        for m1, c1 in self.terms.items():
            for m2, c2 in other.terms.items():
                mon = tuple(a + b for a, b in zip(m1, m2))
                terms[mon] = terms.get(mon, Fraction(0)) + c1 * c2
        return Poly(terms)

    def scale(self, c: Fraction) -> "Poly":
        return Poly({m: c * v for m, v in self.terms.items()})

    def diff(self, i: int) -> "Poly":
        terms: Dict[Tuple[int, ...], Fraction] = {}
        for mon, coeff in self.terms.items():
            if mon[i]:
                new_mon = list(mon)
                new_mon[i] -= 1
                terms[tuple(new_mon)] = coeff * mon[i]
        return Poly(terms)

    def eval_point(self, xs: Sequence[Fraction]) -> Fraction:
        total = Fraction(0)
        for mon, coeff in self.terms.items():
            term = coeff
            for x, power in zip(xs, mon):
                if power:
                    term *= x**power
            total += term
        return total

    def eval_iv(self, xs: Sequence[Iv]) -> Iv:
        total = ZERO_IV
        for mon, coeff in self.terms.items():
            term = Iv.point(coeff)
            for x, power in zip(xs, mon):
                for _ in range(power):
                    term = term * x
            total = total + term
        return total

    def is_zero(self) -> bool:
        return not self.terms


def poly_sum(items: Iterable[Poly]) -> Poly:
    total = Poly()
    for item in items:
        total = total + item
    return total


def poly_matrix_mul(A: List[List[Poly]], B: List[List[Poly]]) -> List[List[Poly]]:
    rows = len(A)
    cols = len(B[0])
    mid = len(B)
    return [[poly_sum(A[i][k] * B[k][j] for k in range(mid)) for j in range(cols)] for i in range(rows)]


def dot_poly_matrix(x: Sequence[Fraction], M: List[List[Poly]]) -> Poly:
    total = Poly()
    for i in range(3):
        for j in range(3):
            total = total + M[i][j].scale(x[i] * x[j])
    return total


def cross(a: Sequence[Fraction], b: Sequence[Fraction]) -> List[Fraction]:
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def det3_rows(rows: Sequence[Sequence[Fraction]]) -> Fraction:
    a, b, c = rows
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def build_probability_polys(U: List[List[Fraction]]):
    x = [Poly.var(i) for i in range(NVAR)]
    one = Poly.const(Fraction(1))
    zero = Poly()

    A = [
        [x[0], x[3], x[4]],
        [x[3], x[1], x[5]],
        [x[4], x[5], x[2]],
    ]
    tr = x[0] + x[1] + x[2]
    e2 = x[0] * x[1] + x[0] * x[2] + x[1] * x[2] - x[3] * x[3] - x[4] * x[4] - x[5] * x[5]
    detA = (
        x[0] * x[1] * x[2]
        + (x[3] * x[4] * x[5]).scale(Fraction(2))
        - x[0] * x[5] * x[5]
        - x[1] * x[4] * x[4]
        - x[2] * x[3] * x[3]
    )
    adj = [
        [x[1] * x[2] - x[5] * x[5], x[4] * x[5] - x[3] * x[2], x[3] * x[5] - x[1] * x[4]],
        [x[4] * x[5] - x[3] * x[2], x[0] * x[2] - x[4] * x[4], x[3] * x[4] - x[0] * x[5]],
        [x[3] * x[5] - x[1] * x[4], x[3] * x[4] - x[0] * x[5], x[0] * x[1] - x[3] * x[3]],
    ]
    d_minus_e2 = detA - e2
    D1 = [[A[i][j] + adj[i][j] for j in range(3)] for i in range(3)]
    D2 = [[adj[i][j] for j in range(3)] for i in range(3)]
    for i in range(3):
        D1[i][i] = D1[i][i] + d_minus_e2
        D2[i][i] = D2[i][i] - detA

    p0 = one - tr + e2 - detA
    by_subset: Dict[Tuple[int, ...], Poly] = {(): p0}
    for i, r in enumerate(U):
        by_subset[(i + 1,)] = dot_poly_matrix(r, D1)
    for i, j in itertools.combinations(range(5), 2):
        w = cross(U[i], U[j])
        by_subset[(i + 1, j + 1)] = dot_poly_matrix(w, D2)
    for combo in itertools.combinations(range(5), 3):
        rows = [U[i] for i in combo]
        q = det3_rows(rows) ** 2
        by_subset[tuple(i + 1 for i in combo)] = detA.scale(q)
    for size in (4, 5):
        for combo in itertools.combinations(range(5), size):
            by_subset[tuple(i + 1 for i in combo)] = zero

    events = []
    for mask in range(32):
        subset = tuple(i + 1 for i in range(5) if mask & (1 << i))
        poly = by_subset[subset]
        events.append(
            {
                "mask": mask,
                "subset": subset,
                "name": "empty" if not subset else "".join(map(str, subset)),
                "size": len(subset),
                "poly": poly,
                "identically_zero": poly.is_zero(),
            }
        )

    check = poly_sum(e["poly"] for e in events) - Poly.const(Fraction(1))
    if not check.is_zero():
        raise AssertionError("event probabilities do not sum to 1 as polynomials")
    return events


def enrich_jets(events):
    enriched = []
    for e in events:
        p = e["poly"]
        grad = [p.diff(i) for i in range(NVAR)]
        hess = [[grad[i].diff(j) for j in range(NVAR)] for i in range(NVAR)]
        ee = dict(e)
        ee["grad"] = grad
        ee["hess"] = hess
        enriched.append(ee)
    return enriched


def mat_transpose(A):
    return [list(row) for row in zip(*A)]


def matmul_q(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def build_centers(config):
    rotations = {
        name: [[parse_q(x) for x in row] for row in mat]
        for name, mat in config["rotations"].items()
    }
    I = [[Fraction(int(i == j), 1) for j in range(3)] for i in range(3)]
    for name, R in rotations.items():
        RtR = matmul_q(mat_transpose(R), R)
        if RtR != I:
            raise AssertionError(f"rotation {name} is not exactly orthogonal")

    centers = []
    for item in config["centers"]:
        R = rotations[item["rotation"]]
        eigs = [parse_q(x) for x in item["eigenvalues"]]
        D = [[Fraction(0) for _ in range(3)] for _ in range(3)]
        for i, lam in enumerate(eigs):
            D[i][i] = lam
        A = matmul_q(matmul_q(R, D), mat_transpose(R))
        coords = [A[0][0], A[1][1], A[2][2], A[0][1], A[0][2], A[1][2]]
        centers.append(
            {
                "name": item["name"],
                "eigenvalues": eigs,
                "rotation": item["rotation"],
                "reason": item.get("reason", ""),
                "matrix": A,
                "coords": coords,
            }
        )
    return centers


def atanh_log_bounds_unit_to_two(y: Fraction, n_terms: int) -> Iv:
    if not (Fraction(1) <= y < Fraction(2)):
        raise ValueError("y must be in [1,2)")
    z = (y - 1) / (y + 1)
    total = Fraction(0)
    zpow = z
    z2 = z * z
    for j in range(n_terms):
        total += Fraction(2) * zpow / Fraction(2 * j + 1)
        zpow *= z2
    if z == 0:
        rem = Fraction(0)
    else:
        rem = Fraction(2) * zpow / (Fraction(2 * n_terms + 1) * (1 - z2))
    return Iv(total, total + rem)


_LOG2_CACHE: Dict[int, Iv] = {}
_LOGQ_CACHE: Dict[Tuple[Fraction, int], Iv] = {}


def log2_bounds(n_terms: int) -> Iv:
    cached = _LOG2_CACHE.get(n_terms)
    if cached is None:
        cached = atanh_log_bounds_unit_to_two(Fraction(2), n_terms) if False else None
    if cached is None:
        z = Fraction(1, 3)
        total = Fraction(0)
        zpow = z
        z2 = z * z
        for j in range(n_terms):
            total += Fraction(2) * zpow / Fraction(2 * j + 1)
            zpow *= z2
        rem = Fraction(2) * zpow / (Fraction(2 * n_terms + 1) * (1 - z2))
        cached = Iv(total, total + rem)
        _LOG2_CACHE[n_terms] = cached
    return cached


def log_q_bounds(q: Fraction, n_terms: int) -> Iv:
    if q <= 0:
        raise ValueError("log input must be positive")
    key = (q, n_terms)
    cached = _LOGQ_CACHE.get(key)
    if cached is not None:
        return cached

    y = q
    k = 0
    while y >= 2:
        y /= 2
        k += 1
    while y < 1:
        y *= 2
        k -= 1
    ly = atanh_log_bounds_unit_to_two(y, n_terms)
    l2 = log2_bounds(n_terms)
    if k >= 0:
        out = Iv(ly.lo + k * l2.lo, ly.hi + k * l2.hi)
    else:
        out = Iv(ly.lo + k * l2.hi, ly.hi + k * l2.lo)
    _LOGQ_CACHE[key] = out
    return out


def log_iv_bounds(x: Iv, n_terms: int) -> Iv:
    if x.lo <= 0:
        raise ValueError("log interval must be positive")
    return Iv(log_q_bounds(x.lo, n_terms).lo, log_q_bounds(x.hi, n_terms).hi)


def eval_event_iv(event, box: Sequence[Iv], n_terms: int):
    p = event["poly"].eval_iv(box)
    grad = [g.eval_iv(box) for g in event["grad"]]
    hess = [[event["hess"][i][j].eval_iv(box) for j in range(NVAR)] for i in range(NVAR)]
    logp = None if event["identically_zero"] else log_iv_bounds(p, n_terms)
    return p, grad, hess, logp


def entropy_hessian_iv(events, box: Sequence[Iv], n_terms: int):
    H = [[ZERO_IV for _ in range(NVAR)] for _ in range(NVAR)]
    event_bounds = []
    for event in events:
        if event["identically_zero"]:
            event_bounds.append(
                {
                    "name": event["name"],
                    "subset": list(event["subset"]),
                    "mask": event["mask"],
                    "identically_zero": True,
                    "p": Iv.point(Fraction(0)),
                }
            )
            continue
        p, grad, hess, logp = eval_event_iv(event, box, n_terms)
        if p.lo <= 0:
            raise ValueError(f"non-positive probability lower bound for {event['name']}: {p}")
        event_bounds.append(
            {
                "name": event["name"],
                "subset": list(event["subset"]),
                "mask": event["mask"],
                "identically_zero": False,
                "p": p,
            }
        )
        invp = p.inv()
        for a in range(NVAR):
            for b in range(a, NVAR):
                fisher = (grad[a] * grad[b]) * invp
                accel = hess[a][b] * logp
                term = -(fisher + accel)
                H[a][b] = H[a][b] + term
                if a != b:
                    H[b][a] = H[a][b]
    return H, event_bounds


def point_jets(events, coords: Sequence[Fraction]):
    out = []
    for event in events:
        p = event["poly"].eval_point(coords)
        grad = [g.eval_point(coords) for g in event["grad"]]
        hess = [[event["hess"][i][j].eval_point(coords) for j in range(NVAR)] for i in range(NVAR)]
        out.append(
            {
                "name": event["name"],
                "mask": event["mask"],
                "subset": list(event["subset"]),
                "identically_zero": event["identically_zero"],
                "p": qstr(p),
                "gradient": [qstr(x) for x in grad],
                "hessian_upper_triangle": [qstr(hess[i][j]) for i, j in PAIR_INDEX],
            }
        )
    return out


def entropy_hessian_float(events, coords: Sequence[Fraction]):
    H = np.zeros((NVAR, NVAR), dtype=float)
    for event in events:
        if event["identically_zero"]:
            continue
        p = float(event["poly"].eval_point(coords))
        grad = np.array([float(g.eval_point(coords)) for g in event["grad"]], dtype=float)
        hess = np.array(
            [[float(event["hess"][i][j].eval_point(coords)) for j in range(NVAR)] for i in range(NVAR)],
            dtype=float,
        )
        H += -np.outer(grad, grad) / p - hess * math.log(p)
    return 0.5 * (H + H.T)


def interval_neg(M: List[List[Iv]]) -> List[List[Iv]]:
    return [[-M[i][j] for j in range(NVAR)] for i in range(NVAR)]


def rationalize_matrix(A: np.ndarray, max_den: int = 10**10) -> List[List[Fraction]]:
    return [[Fraction(str(float(A[i, j]))).limit_denominator(max_den) for j in range(A.shape[1])] for i in range(A.shape[0])]


def precondition_interval(M: List[List[Iv]], S: List[List[Fraction]]) -> List[List[Iv]]:
    # P = S^T M S.
    temp = [[ZERO_IV for _ in range(NVAR)] for _ in range(NVAR)]
    for i in range(NVAR):
        for j in range(NVAR):
            acc = ZERO_IV
            for k in range(NVAR):
                acc = acc + M[i][k].scale(S[k][j])
            temp[i][j] = acc
    P = [[ZERO_IV for _ in range(NVAR)] for _ in range(NVAR)]
    for i in range(NVAR):
        for j in range(NVAR):
            acc = ZERO_IV
            for k in range(NVAR):
                acc = acc + temp[k][j].scale(S[k][i])
            P[i][j] = acc
    return P


def gershgorin_pd(P: List[List[Iv]]):
    margins = []
    for i in range(NVAR):
        radius = sum(P[i][j].abs_upper() for j in range(NVAR) if j != i)
        margin = P[i][i].lo - radius
        margins.append(margin)
    return min(margins) > 0, margins


def positive_direction_certificate(H_iv, eigvec_float):
    v = [Fraction(str(float(x))).limit_denominator(10**6) for x in eigvec_float]
    q = ZERO_IV
    for i in range(NVAR):
        for j in range(NVAR):
            q = q + H_iv[i][j].scale(v[i] * v[j])
    return v, q


def matrix_frobenius_radius(coord_radius: Fraction) -> Fraction:
    # For symmetric coordinate perturbations with all six coordinate radii rho:
    # ||E||_F^2 <= 3 rho^2 + 2*3 rho^2 = 9 rho^2.
    return 3 * coord_radius


def attempt_domain_summary(eigs: Sequence[Fraction], radius: Fraction):
    spread = matrix_frobenius_radius(radius)
    lower = min(eigs) - spread
    upper = max(eigs) + spread
    target_lower = Fraction(1, 4)
    target_upper = Fraction(3, 4)
    return {
        "operator_envelope": {"lower": qstr(lower), "upper": qstr(upper)},
        "whole_box_in_0_I": lower > 0 and upper < 1,
        "whole_box_in_target_band": lower >= target_lower and upper <= target_upper,
        "center_in_target_band": min(eigs) >= target_lower and max(eigs) <= target_upper,
        "target_intersection_certified_nonempty": min(eigs) >= target_lower and max(eigs) <= target_upper,
    }


def event_bounds_json(event_bounds):
    return [
        {
            "name": e["name"],
            "mask": e["mask"],
            "subset": e["subset"],
            "identically_zero": e["identically_zero"],
            "p": e["p"].to_json(),
        }
        for e in event_bounds
    ]


def min_probability(event_bounds):
    positives = [e for e in event_bounds if not e["identically_zero"]]
    return min(positives, key=lambda e: e["p"].lo)


def rare_probability_summary(event_bounds, limit=8):
    positives = [e for e in event_bounds if not e["identically_zero"]]
    positives.sort(key=lambda e: e["p"].lo)
    return [
        {
            "name": e["name"],
            "mask": e["mask"],
            "subset": e["subset"],
            "lower": qstr(e["p"].lo),
            "upper": qstr(e["p"].hi),
            "lower_decimal": dec(e["p"].lo),
            "upper_decimal": dec(e["p"].hi),
        }
        for e in positives[:limit]
    ]


def iv_matrix_json(M):
    return [[M[i][j].to_json() for j in range(NVAR)] for i in range(NVAR)]


def iv_matrix_decimal_json(M):
    return [
        [
            {
                "lo_decimal": dec(M[i][j].lo),
                "hi_decimal": dec(M[i][j].hi),
            }
            for j in range(NVAR)
        ]
        for i in range(NVAR)
    ]


def gershgorin_rows_json(P, margins):
    rows = []
    for i in range(NVAR):
        off_sum = sum(P[i][j].abs_upper() for j in range(NVAR) if j != i)
        rows.append(
            {
                "row": i,
                "diagonal_lower": qstr(P[i][i].lo),
                "offdiagonal_abs_sum": qstr(off_sum),
                "margin": qstr(margins[i]),
                "diagonal_lower_decimal": dec(P[i][i].lo),
                "offdiagonal_abs_sum_decimal": dec(off_sum),
                "margin_decimal": dec(margins[i]),
            }
        )
    return rows


def frac_matrix_json(M):
    return [[qstr(x) for x in row] for row in M]


def read_main_comparison(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"read_error": str(exc)}


def flatten_hessian_ut_from_full(hess_full: List[List[str]]):
    return [hess_full[i][j] for i, j in PAIR_INDEX]


def compare_main_jets(our_centers, config, out_dir: Path):
    info = config.get("main_comparison_output")
    if not info:
        return {"status": "not_requested"}
    # The main output lives on the server path; a local mirror may not exist.
    local_candidate = out_dir.parent / "main_output" / "independent_events.json"
    data = read_main_comparison(local_candidate)
    if data is None:
        return {
            "status": "main_output_not_available_locally",
            "local_path_checked": str(local_candidate),
            "expected_relative_server_path": info.get("relative_server_path"),
        }
    return {
        "status": "main_output_available_but_schema_not_assumed",
        "local_path_checked": str(local_candidate),
        "top_level_type": type(data).__name__,
        "note": "Exact jet comparison is reported only if the schema is inspected by a reviewer; our center_event_jets.json uses exact rational p/gradient/Hessian values.",
    }


def planned_radii_for_center(center_name: str, base_radii: Sequence[Fraction], radius_plan: dict | None):
    if not radius_plan:
        return list(base_radii)
    direct = radius_plan.get("direct_first_radius", {})
    if center_name not in direct:
        return list(base_radii)
    first = parse_q(direct[center_name])
    smaller = [r for r in base_radii if r < first]
    return [first] + smaller


def run(
    config_path: Path,
    output_root: Path,
    log_terms: int | None,
    max_attempts: int | None,
    radius_plan_path: Path | None,
):
    started = time.time()
    output_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = output_root / f"run_{stamp}_pid{os.getpid()}"
    out_dir.mkdir(parents=True, exist_ok=False)

    config = json.loads(config_path.read_text(encoding="utf-8"))
    n_terms = int(log_terms or config.get("log_series_terms_initial", 96))
    max_total_attempts = int(max_attempts or config.get("max_total_attempts", 128))
    Uden = Fraction(int(config["u_matrix"]["denominator"]), 1)
    U = [[Fraction(int(x), 1) / Uden for x in row] for row in config["u_matrix"]["numerators"]]
    events = enrich_jets(build_probability_polys(U))
    centers = build_centers(config)
    radii = [parse_q(x) for x in config["radius_schedule"]]
    radius_plan = None
    if radius_plan_path is not None:
        radius_plan = json.loads(radius_plan_path.read_text(encoding="utf-8"))

    metadata = {
        "pid": os.getpid(),
        "started_utc": stamp,
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "config_path": str(config_path),
        "output_dir": str(out_dir),
        "thread_env": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "log_series_terms": n_terms,
        "max_total_attempts": max_total_attempts,
        "radius_plan_path": str(radius_plan_path) if radius_plan_path else None,
        "radius_plan": radius_plan,
    }
    (out_dir / "run_environment.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    center_jets = {
        "coordinate_order": COORDS,
        "pair_index_order": [[i, j] for i, j in PAIR_INDEX],
        "centers": [],
    }
    for center in centers:
        center_jets["centers"].append(
            {
                "name": center["name"],
                "rotation": center["rotation"],
                "eigenvalues": [qstr(x) for x in center["eigenvalues"]],
                "matrix": frac_matrix_json(center["matrix"]),
                "coordinates": [qstr(x) for x in center["coords"]],
                "events": point_jets(events, center["coords"]),
            }
        )
    (out_dir / "center_event_jets.json").write_text(json.dumps(center_jets, indent=2), encoding="utf-8")

    attempts_path = out_dir / "attempts.jsonl"
    accepted = []
    failures = []
    refuted = None
    attempts = 0

    with attempts_path.open("w", encoding="utf-8") as attempts_file:
        for center in centers:
            H0 = entropy_hessian_float(events, center["coords"])
            eigvals, eigvecs = np.linalg.eigh(H0)
            point_summary = {
                "center": center["name"],
                "point_hessian_eigenvalues_float": [float(x) for x in eigvals],
                "point_max_eigenvalue_float": float(eigvals[-1]),
            }
            if eigvals[-1] > 1e-8:
                H_point_iv, point_event_bounds = entropy_hessian_iv(events, [Iv.point(x) for x in center["coords"]], n_terms)
                v, q = positive_direction_certificate(H_point_iv, eigvecs[:, -1])
                if q.lo > 0:
                    refuted = {
                        **point_summary,
                        "direction_coordinates": [qstr(x) for x in v],
                        "direction_quadratic_interval": q.to_json(),
                        "center_coordinates": [qstr(x) for x in center["coords"]],
                        "note": "strict positive Hessian direction at the center; chord radius must be chosen inside 0<A<I",
                    }
                    attempts_file.write(json.dumps({"type": "refuted", **refuted}) + "\n")
                    break

            center_accepted = None
            for radius in planned_radii_for_center(center["name"], radii, radius_plan):
                if attempts >= max_total_attempts:
                    break
                attempts += 1
                domain = attempt_domain_summary(center["eigenvalues"], radius)
                attempt_record = {
                    **point_summary,
                    "attempt": attempts,
                    "radius": qstr(radius),
                    "radius_decimal": dec(radius),
                    "domain": domain,
                }
                if not domain["whole_box_in_0_I"]:
                    attempt_record["status"] = "SKIPPED_DOMAIN"
                    attempts_file.write(json.dumps(attempt_record) + "\n")
                    attempts_file.flush()
                    failures.append(attempt_record)
                    continue
                box = [Iv(c - radius, c + radius) for c in center["coords"]]
                try:
                    H_iv, event_bounds = entropy_hessian_iv(events, box, n_terms)
                    M_iv = interval_neg(H_iv)
                    # Build preconditioner from the point Hessian.
                    M0 = -H0
                    L = np.linalg.cholesky(M0)
                    # numpy returns M0 = L L^T.  Use S = L^{-T}, so
                    # S^T M0 S is the identity at the floating center.
                    S_float = np.linalg.inv(L.T)
                    S = rationalize_matrix(S_float)
                    P = precondition_interval(M_iv, S)
                    ok, margins = gershgorin_pd(P)
                    mp = min_probability(event_bounds)
                    attempt_record.update(
                        {
                            "status": "ACCEPTED" if ok else "FAILED_GERSHGORIN",
                            "min_probability_event": mp["name"],
                            "min_probability_lower_decimal": dec(mp["p"].lo),
                            "min_probability_upper_decimal": dec(mp["p"].hi),
                            "gershgorin_margins_decimal": [dec(m) for m in margins],
                            "min_gershgorin_margin_decimal": dec(min(margins)),
                        }
                    )
                    attempts_file.write(json.dumps(attempt_record) + "\n")
                    attempts_file.flush()
                    if ok:
                        center_accepted = {
                            "center": center["name"],
                            "rotation": center["rotation"],
                            "reason": center["reason"],
                            "center_coordinates": [qstr(x) for x in center["coords"]],
                            "center_matrix": frac_matrix_json(center["matrix"]),
                            "center_eigenvalues": [qstr(x) for x in center["eigenvalues"]],
                            "radius": qstr(radius),
                            "radius_decimal": dec(radius),
                            "domain": domain,
                            "point_hessian_eigenvalues_float": [float(x) for x in eigvals],
                            "event_probability_bounds": event_bounds_json(event_bounds),
                            "rare_events_by_lower_bound": rare_probability_summary(event_bounds),
                            "min_probability": {
                                "event": mp["name"],
                                "subset": mp["subset"],
                                "lower": qstr(mp["p"].lo),
                                "upper": qstr(mp["p"].hi),
                                "lower_decimal": dec(mp["p"].lo),
                                "upper_decimal": dec(mp["p"].hi),
                            },
                            "entropy_hessian_interval_decimal": iv_matrix_decimal_json(H_iv),
                            "negative_hessian_preconditioner_S": frac_matrix_json(S),
                            "preconditioned_negative_hessian_interval_decimal": iv_matrix_decimal_json(P),
                            "preconditioned_gershgorin_rows_exact": gershgorin_rows_json(P, margins),
                            "gershgorin_margins": [qstr(m) for m in margins],
                            "gershgorin_margins_decimal": [dec(m) for m in margins],
                            "min_gershgorin_margin": qstr(min(margins)),
                            "certificate": "For every A in the coordinate box, S^T(-H(A))S is strictly diagonally dominant with positive diagonal by the listed rational intervals; hence H(A) is negative definite for all real symmetric directions.",
                        }
                        accepted.append(center_accepted)
                        break
                    failures.append(attempt_record)
                except Exception as exc:
                    attempt_record["status"] = "FAILED_EXCEPTION"
                    attempt_record["exception"] = repr(exc)
                    attempts_file.write(json.dumps(attempt_record) + "\n")
                    attempts_file.flush()
                    failures.append(attempt_record)
            if refuted is not None:
                break
            if center_accepted is None:
                failures.append(
                    {
                        "center": center["name"],
                        "status": "CENTER_NOT_CERTIFIED",
                        "attempts_used_so_far": attempts,
                    }
                )
            if attempts >= max_total_attempts:
                break

    status = "REFUTED" if refuted else ("ACCEPTED_SCOPED" if len(accepted) == len(centers) else "INCOMPLETE")
    cert = {
        "status": status,
        "coordinate_order": COORDS,
        "input_path": str(config_path),
        "output_dir": str(out_dir),
        "attempts_used": attempts,
        "centers_requested": len(centers),
        "centers_accepted": len(accepted),
        "log_series_terms": n_terms,
        "accepted_boxes": accepted,
        "refutation": refuted,
        "failures": failures,
        "zero_events": [
            {"name": e["name"], "mask": e["mask"], "subset": list(e["subset"])}
            for e in events
            if e["identically_zero"]
        ],
        "nonclaim": "This finite-box certificate does not cover the whole spectral domain 1/4 I <= A <= 3/4 I.",
        "main_comparison": compare_main_jets(center_jets, config, out_dir),
    }
    (out_dir / "certificate.json").write_text(json.dumps(cert, indent=2), encoding="utf-8")

    finished = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    result_lines = [
        status,
        "",
        f"Output directory: {out_dir}",
        f"Attempts used: {attempts}/{max_total_attempts}",
        f"Centers accepted: {len(accepted)}/{len(centers)}",
        f"Log series terms: {n_terms}",
        f"Started UTC: {stamp}",
        f"Finished UTC: {finished}",
        f"Elapsed seconds: {time.time() - started:.3f}",
        "",
        "Finite-box scope only; this is not a proof over the entire matrix spectral domain.",
    ]
    if accepted:
        result_lines.extend(["", "Accepted boxes:"])
        for item in accepted:
            result_lines.append(
                f"- {item['center']}: radius {item['radius']} "
                f"(min event {item['min_probability']['event']} lower {item['min_probability']['lower_decimal']}; "
                f"min Gershgorin margin {min(item['gershgorin_margins_decimal'], key=float)})"
            )
    if failures and status != "ACCEPTED_SCOPED":
        result_lines.extend(["", "Uncertified or failed records are in attempts.jsonl and certificate.json."])
    (out_dir / "RESULT.md").write_text("\n".join(result_lines) + "\n", encoding="utf-8")
    (output_root / "LATEST_RESULT.md").write_text("\n".join(result_lines) + "\n", encoding="utf-8")
    (output_root / "LATEST_OUTPUT_DIR.txt").write_text(str(out_dir) + "\n", encoding="utf-8")
    return status, out_dir


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--log-terms", type=int, default=None)
    parser.add_argument("--max-attempts", type=int, default=None)
    parser.add_argument("--radius-plan", type=Path, default=None)
    args = parser.parse_args(argv)
    status, out_dir = run(args.input, args.output_root, args.log_terms, args.max_attempts, args.radius_plan)
    print(f"STATUS {status}")
    print(f"OUTPUT_DIR {out_dir}")
    return 0 if status in {"ACCEPTED_SCOPED", "REFUTED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
