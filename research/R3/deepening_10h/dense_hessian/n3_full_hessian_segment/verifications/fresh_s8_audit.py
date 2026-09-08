from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

import numpy as np


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUT = HERE / "fresh_s8_audit.json"

N = 3
COORDS = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
NVAR = len(COORDS)
T_DEG = 4
H_DEG = 3
ZERO = F(0)
ONE = F(1)


def fstr(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def parse_frac(x: str) -> F:
    return F(x)


def dec(x: F, prec: int = 60) -> str:
    with localcontext() as ctx:
        ctx.prec = prec
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def pt_zero() -> list[F]:
    return [ZERO] * T_DEG


def pt_const(c: F) -> list[F]:
    return [c] + [ZERO] * (T_DEG - 1)


def pt_affine(a: F, b: F) -> list[F]:
    return [a, b] + [ZERO] * (T_DEG - 2)


def pt_add(a: list[F], b: list[F]) -> list[F]:
    return [a[i] + b[i] for i in range(T_DEG)]


def pt_sub(a: list[F], b: list[F]) -> list[F]:
    return [a[i] - b[i] for i in range(T_DEG)]


def pt_scale(c: F, a: list[F]) -> list[F]:
    return [c * x for x in a]


def pt_mul(a: list[F], b: list[F]) -> list[F]:
    out = [ZERO] * T_DEG
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj != 0 and i + j < T_DEG:
                out[i + j] += ai * bj
    return out


def ph_zero() -> list[list[F]]:
    return [pt_zero() for _ in range(H_DEG)]


def ph_const(c: F) -> list[list[F]]:
    return [pt_const(c), pt_zero(), pt_zero()]


def ph_affine_t_plus_h(a: F, b: F, h_coeff: F) -> list[list[F]]:
    return [pt_affine(a, b), pt_const(h_coeff), pt_zero()]


def ph_add(*items: list[list[F]]) -> list[list[F]]:
    out = ph_zero()
    for item in items:
        out = [pt_add(out[i], item[i]) for i in range(H_DEG)]
    return out


def ph_sub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [pt_sub(a[i], b[i]) for i in range(H_DEG)]


def ph_scale(c: F, a: list[list[F]]) -> list[list[F]]:
    return [pt_scale(c, a[i]) for i in range(H_DEG)]


def ph_mul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    out = ph_zero()
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            if i + j < H_DEG:
                out[i + j] = pt_add(out[i + j], pt_mul(ai, bj))
    return out


def det_ph(mat: list[list[list[list[F]]]]) -> list[list[F]]:
    n = len(mat)
    if n == 0:
        return ph_const(ONE)
    if n == 1:
        return mat[0][0]
    if n == 2:
        return ph_sub(ph_mul(mat[0][0], mat[1][1]), ph_mul(mat[0][1], mat[1][0]))
    if n == 3:
        a, b, c = mat[0]
        d, e, f = mat[1]
        g, h, i = mat[2]
        return ph_add(
            ph_mul(ph_mul(a, e), i),
            ph_mul(ph_mul(b, f), g),
            ph_mul(ph_mul(c, d), h),
            ph_scale(-ONE, ph_mul(ph_mul(c, e), g)),
            ph_scale(-ONE, ph_mul(ph_mul(b, d), i)),
            ph_scale(-ONE, ph_mul(ph_mul(a, f), h)),
        )
    raise ValueError("n=3 only")


def mat_add(A, B, scale=ONE):
    return [[A[i][j] + scale * B[i][j] for j in range(N)] for i in range(N)]


def mat_scale(c: F, A):
    return [[c * A[i][j] for j in range(N)] for i in range(N)]


def mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(N)) for j in range(N)] for i in range(N)]


def ident():
    return [[ONE if i == j else ZERO for j in range(N)] for i in range(N)]


def projectors():
    U = [[F(1, 3) for _ in range(N)] for __ in range(N)]
    w = [F(1), F(2), F(-3)]
    V = [[w[i] * w[j] / F(14) for j in range(N)] for i in range(N)]
    I = ident()
    W = [[I[i][j] - U[i][j] - V[i][j] for j in range(N)] for i in range(N)]
    return U, V, W


def m8_line():
    U, V, W = projectors()
    K0 = mat_add(mat_add(mat_scale(F(1, 5), U), mat_scale(F(1, 2), V)), mat_scale(F(4, 5), W))
    R = mat_add(mat_add(mat_scale(F(1, 5), U), mat_scale(F(1, 3), V)), mat_scale(F(2, 3), W))
    return K0, R


def coord_basis():
    out = []
    for i, j in COORDS:
        M = [[ZERO for _ in range(N)] for __ in range(N)]
        M[i][j] = ONE
        M[j][i] = ONE
        out.append(M)
    return out


def principal(mat, idx):
    return [[mat[i][j] for j in idx] for i in idx]


def inclusion_det_poly(K0, R, D, mask: int):
    idx = [i for i in range(N) if (mask >> i) & 1]
    mat = [
        [ph_affine_t_plus_h(K0[i][j], R[i][j], D[i][j]) for j in range(N)]
        for i in range(N)
    ]
    return det_ph(principal(mat, idx))


def signed_det_atom_poly(K0, R, D, event_mask: int):
    mat = []
    for i in range(N):
        row = []
        for j in range(N):
            subtract = ONE if i == j and not ((event_mask >> i) & 1) else ZERO
            row.append(ph_affine_t_plus_h(K0[i][j] - subtract, R[i][j], D[i][j]))
        mat.append(row)
    return ph_scale(F((-1) ** (N - event_mask.bit_count())), det_ph(mat))


def exact_atom_poly_from_mobius(K0, R, D, event_mask: int):
    total = ph_zero()
    for sup in range(1 << N):
        if (sup & event_mask) == event_mask:
            total = ph_add(total, ph_scale(F((-1) ** (sup.bit_count() - event_mask.bit_count())), inclusion_det_poly(K0, R, D, sup)))
    return total


def atom_direction_polys(K0, R, D, event_mask: int):
    mob = exact_atom_poly_from_mobius(K0, R, D, event_mask)
    signed = signed_det_atom_poly(K0, R, D, event_mask)
    if mob != signed:
        raise AssertionError(f"Mobius/signed determinant mismatch for event {event_mask}")
    return mob[0], mob[1], pt_scale(F(2), mob[2])


def build_jets(K0, R):
    basis = coord_basis()
    zero = [[ZERO for _ in range(N)] for __ in range(N)]
    p0 = [atom_direction_polys(K0, R, zero, s)[0] for s in range(8)]
    p1 = [[pt_zero() for _ in range(8)] for __ in range(NVAR)]
    pii = [[pt_zero() for _ in range(8)] for __ in range(NVAR)]
    for i, D in enumerate(basis):
        for s in range(8):
            got_p0, got_p1, got_pii = atom_direction_polys(K0, R, D, s)
            assert got_p0 == p0[s]
            p1[i][s] = got_p1
            pii[i][s] = got_pii
    pij = [[[pt_zero() for _ in range(8)] for __ in range(NVAR)] for ___ in range(NVAR)]
    for i in range(NVAR):
        for j in range(i, NVAR):
            if i == j:
                for s in range(8):
                    pij[i][j][s] = pii[i][s]
                    pij[j][i][s] = pii[i][s]
            else:
                Dsum = mat_add(basis[i], basis[j])
                for s in range(8):
                    _, _, p2sum = atom_direction_polys(K0, R, Dsum, s)
                    cross = pt_scale(F(1, 2), pt_sub(pt_sub(p2sum, pii[i][s]), pii[j][s]))
                    pij[i][j][s] = cross
                    pij[j][i][s] = cross
    return {"p0": p0, "p1": p1, "pij": pij}


def iadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def isub(a, b):
    return a[0] - b[1], a[1] - b[0]


def imul(a, b):
    vals = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
    return min(vals), max(vals)


def idiv_pos(a, b):
    assert b[0] > 0
    return imul(a, (ONE / b[1], ONE / b[0]))


def iabs_upper(a) -> F:
    return max(abs(a[0]), abs(a[1]))


def peval(poly: list[F], x: F) -> F:
    y = ZERO
    for c in reversed(poly):
        y = y * x + c
    return y


def peval_interval(poly: list[F], interval: tuple[F, F]) -> tuple[F, F]:
    out = (poly[-1], poly[-1])
    for c in reversed(poly[:-1]):
        out = iadd(imul(out, interval), (c, c))
    return out


def log_bounds_unit_1_2(y: F, terms: int) -> tuple[F, F]:
    assert ONE <= y <= 2
    if y == 1:
        return ZERO, ZERO
    z = (y - 1) / (y + 1)
    partial = 2 * sum(z ** (2 * k + 1) / F(2 * k + 1) for k in range(terms))
    tail = 2 * z ** (2 * terms + 1) / (F(2 * terms + 1) * (1 - z * z))
    return partial, partial + tail


@lru_cache(maxsize=None)
def log_bounds_point(x: F, terms: int) -> tuple[F, F]:
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
    lo_y, hi_y = log_bounds_unit_1_2(y, terms)
    lo_2, hi_2 = log_bounds_unit_1_2(F(2), terms)
    if exponent >= 0:
        return lo_y + exponent * lo_2, hi_y + exponent * hi_2
    n = -exponent
    return lo_y - n * hi_2, hi_y - n * lo_2


def ilog_pos(interval: tuple[F, F], terms: int) -> tuple[F, F]:
    assert interval[0] > 0
    lo = log_bounds_point(interval[0], terms)[0]
    hi = log_bounds_point(interval[1], terms)[1]
    return lo, hi


def B_interval(jets, interval: tuple[F, F], log_terms: int):
    p_intervals = [peval_interval(poly, interval) for poly in jets["p0"]]
    if any(p[0] <= 0 for p in p_intervals):
        raise ArithmeticError("nonpositive atom lower bound")
    logs = [ilog_pos(p, log_terms) for p in p_intervals]
    B = [[(ZERO, ZERO) for _ in range(NVAR)] for __ in range(NVAR)]
    for i in range(NVAR):
        for j in range(i, NVAR):
            total = (ZERO, ZERO)
            for s in range(8):
                pi = peval_interval(jets["p1"][i][s], interval)
                pj = peval_interval(jets["p1"][j][s], interval)
                pij = peval_interval(jets["pij"][i][j][s], interval)
                total = iadd(total, idiv_pos(imul(pi, pj), p_intervals[s]))
                total = iadd(total, imul(pij, logs[s]))
            B[i][j] = total
            B[j][i] = total
    return B, p_intervals


def gershgorin(B):
    margins = []
    row_witnesses = []
    for i in range(NVAR):
        diag_lower = B[i][i][0]
        off_upper = sum(iabs_upper(B[i][j]) for j in range(NVAR) if j != i)
        margin = diag_lower - off_upper
        margins.append(margin)
        row_witnesses.append((i, diag_lower, off_upper, margin))
    return min(margins), row_witnesses


def certify_leaf(jets, interval, log_terms):
    B, p_intervals = B_interval(jets, interval, log_terms)
    margin, rows = gershgorin(B)
    return {
        "interval": interval,
        "min_atom_lower": min(p[0] for p in p_intervals),
        "margin": margin,
        "row_witnesses": rows,
        "pass": margin > 0,
    }


def certify_radius(jets, radius: F, log_terms: int = 20, max_depth: int = 10):
    queue = [(-radius, radius, 0)]
    passed = []
    failed = []
    splits = 0
    while queue:
        a, b, depth = queue.pop()
        try:
            cert = certify_leaf(jets, (a, b), log_terms)
            if cert["pass"]:
                passed.append(cert)
                continue
            reason = "nonpositive_gershgorin_margin"
        except Exception as exc:
            cert = {"interval": (a, b), "error": repr(exc)}
            reason = "exception"
        if depth >= max_depth:
            failed.append({
                "interval": cert["interval"],
                "reason": reason,
                "margin": cert.get("margin"),
                "min_atom_lower": cert.get("min_atom_lower"),
                "error": cert.get("error"),
            })
        else:
            mid = (a + b) / 2
            queue.append((mid, b, depth + 1))
            queue.append((a, mid, depth + 1))
            splits += 1
    min_margin = min((x["margin"] for x in passed), default=None)
    min_atom = min((x["min_atom_lower"] for x in passed), default=None)
    # Stable compact leaf hash verifies the exact interval cover without
    # dumping thousands of digits in the JSON.
    leaf_payload = "|".join(f"{fstr(x['interval'][0])},{fstr(x['interval'][1])},{fstr(x['margin'])}" for x in sorted(passed, key=lambda z: z["interval"]))
    return {
        "radius": radius,
        "success": len(failed) == 0 and len(passed) > 0,
        "passed": len(passed),
        "failed": len(failed),
        "splits": splits,
        "min_margin": min_margin,
        "min_margin_decimal": dec(min_margin) if min_margin is not None else None,
        "min_atom_lower": min_atom,
        "first_failed_intervals": failed[:5],
        "leaf_hash_sha256": hashlib.sha256(leaf_payload.encode("utf-8")).hexdigest(),
    }


def spectral_margin(radius: F) -> F:
    theta = [F(1, 5), F(1, 2), F(4, 5)]
    rate = [F(1, 5), F(1, 3), F(2, 3)]
    return min([theta[i] - radius * rate[i] for i in range(3)] + [ONE - theta[i] - radius * rate[i] for i in range(3)])


def roots_for_affine_entry(a: F, b: F):
    if b == 0:
        return None
    return -a / b


def structural_checks(K0, R, radius: F):
    offdiag_roots = {}
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        offdiag_roots[f"{i}{j}"] = roots_for_affine_entry(K0[i][j], R[i][j])
    diag_roots = {}
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        diag_roots[f"{i}{j}"] = roots_for_affine_entry(K0[i][i] - K0[j][j], R[i][i] - R[j][j])
    theta = [F(1, 5), F(1, 2), F(4, 5)]
    rate = [F(1, 5), F(1, 3), F(2, 3)]
    collision_roots = {}
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        collision_roots[f"{i}{j}"] = roots_for_affine_entry(theta[i] - theta[j], rate[i] - rate[j])
    interval = (-radius, radius)
    outside = lambda x: x is not None and not (interval[0] <= x <= interval[1])
    return {
        "spectral_margin": spectral_margin(radius),
        "offdiag_zero_roots": offdiag_roots,
        "diag_equality_roots": diag_roots,
        "spectral_collision_roots": collision_roots,
        "connected_on_closed_interval": all(outside(x) for x in offdiag_roots.values()),
        "heterogeneous_diagonal_on_closed_interval": all(outside(x) for x in diag_roots.values()),
        "distinct_spectrum_on_closed_interval": all(outside(x) for x in collision_roots.values()),
    }


def atom_values(jets, t: F):
    return [peval(poly, t) for poly in jets["p0"]]


def B_point_float(jets, t: F):
    with localcontext() as ctx:
        ctx.prec = 90
        p = atom_values(jets, t)
        B = np.zeros((NVAR, NVAR), dtype=float)
        for i in range(NVAR):
            for j in range(i, NVAR):
                val = Decimal(0)
                for s in range(8):
                    pi = peval(jets["p1"][i][s], t)
                    pj = peval(jets["p1"][j][s], t)
                    pij = peval(jets["pij"][i][j][s], t)
                    val += Decimal(pi.numerator) / Decimal(pi.denominator) * Decimal(pj.numerator) / Decimal(pj.denominator) / (Decimal(p[s].numerator) / Decimal(p[s].denominator))
                    val += Decimal(pij.numerator) / Decimal(pij.denominator) * ctx.ln(Decimal(p[s].numerator) / Decimal(p[s].denominator))
                B[i, j] = B[j, i] = float(val)
        return B


def endpoint_and_failed_float_scouts(jets):
    out = {}
    for radius in [F(6, 25), F(49, 200), F(1, 4)]:
        worst = None
        for k in range(101):
            t = -radius + F(2 * k, 100) * radius
            eigs = np.linalg.eigvalsh(B_point_float(jets, t))
            item = {"t": t, "min_eig_B": float(eigs[0]), "max_eig_B": float(eigs[-1])}
            if worst is None or item["min_eig_B"] < worst["min_eig_B"]:
                worst = item
        out[radius] = worst
    return out


def compare_author_certificate(own_attempts):
    author = json.loads((BASE / "segment_certificate.json").read_text(encoding="utf-8"))
    compact_author = []
    checks = []
    own_by_radius = {fstr(a["radius"]): a for a in own_attempts}
    for a in author["attempted_radii"]:
        own = own_by_radius[a["radius"]]
        min_margin_author = parse_frac(a["min_gershgorin_margin"]) if a.get("min_gershgorin_margin") else None
        min_atom_author = parse_frac(a["min_atom_lower"]) if a.get("min_atom_lower") else None
        compact_author.append({
            "radius": a["radius"],
            "success": a["success"],
            "passed": a["passed"],
            "failed": a["failed"],
            "splits": a["splits"],
            "spectral_margin": a["spectral_margin"],
            "min_margin_decimal": dec(min_margin_author) if min_margin_author is not None else None,
            "min_atom_lower": a.get("min_atom_lower"),
        })
        checks.append(
            own["success"] == a["success"]
            and own["passed"] == a["passed"]
            and own["failed"] == a["failed"]
            and own["splits"] == a["splits"]
            and own["min_margin"] == min_margin_author
            and own["min_atom_lower"] == min_atom_author
            and spectral_margin(own["radius"]) == parse_frac(a["spectral_margin"])
        )
    run_log = (BASE / "run_log.md").read_text(encoding="utf-8")
    script_hash = sha256_file(BASE / "segment_hessian_certificate.py")
    cert_hash = sha256_file(BASE / "segment_certificate.json")
    return {
        "author_status": author["status"],
        "largest_certified_radius": author["largest_certified_radius"],
        "largest_certified_interval": author["largest_certified_interval"],
        "largest_certified_min_atom_lower": author["largest_certified_min_atom_lower"],
        "largest_certified_min_margin_decimal": dec(parse_frac(author["largest_certified_min_margin"])),
        "attempted_radii": compact_author,
        "attempts_match_independent": all(checks),
        "script_sha256": script_hash,
        "certificate_sha256": cert_hash,
        "script_hash_matches_json": script_hash == author["script_sha256"],
        "script_hash_in_run_log": bool(re.search(re.escape(script_hash), run_log, re.IGNORECASE)),
    }


def serialize(obj):
    if isinstance(obj, F):
        return fstr(obj)
    if isinstance(obj, tuple):
        return [serialize(x) for x in obj]
    if isinstance(obj, list):
        return [serialize(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): serialize(v) for k, v in obj.items()}
    return obj


def main() -> int:
    started = time.time()
    U, V, W = projectors()
    K0, R = m8_line()
    jets = build_jets(K0, R)
    sum_p = pt_zero()
    for p in jets["p0"]:
        sum_p = pt_add(sum_p, p)
    p1_mass = []
    p2_mass = []
    for i in range(NVAR):
        s = pt_zero()
        for ev in range(8):
            s = pt_add(s, jets["p1"][i][ev])
        p1_mass.append(s)
        row = []
        for j in range(NVAR):
            ss = pt_zero()
            for ev in range(8):
                ss = pt_add(ss, jets["pij"][i][j][ev])
            row.append(ss)
        p2_mass.append(row)

    radius = F(6, 25)
    attempts = []
    for r in [F(1, 100), F(1, 50), F(1, 20), F(1, 10), F(1, 5), F(6, 25), F(49, 200), F(1, 4)]:
        a = certify_radius(jets, r, log_terms=20, max_depth=10)
        a["spectral_margin"] = spectral_margin(r)
        attempts.append(a)
    largest = [a for a in attempts if a["radius"] == radius][0]
    structure = structural_checks(K0, R, radius)
    endpoint_atoms = {fstr(t): [fstr(x) for x in atom_values(jets, t)] for t in [-radius, ZERO, radius]}
    float_scouts = endpoint_and_failed_float_scouts(jets)
    author_compare = compare_author_certificate(attempts)
    exact_checks = {
        "projectors_sum_to_I": mat_add(mat_add(U, V), W) == ident(),
        "projectors_idempotent_orthogonal": mat_mul(U, U) == U
        and mat_mul(V, V) == V
        and mat_mul(W, W) == W
        and mat_mul(U, V) == [[ZERO] * N for _ in range(N)]
        and mat_mul(U, W) == [[ZERO] * N for _ in range(N)]
        and mat_mul(V, W) == [[ZERO] * N for _ in range(N)],
        "K0_matches_frozen": K0
        == [
            [F(81, 140), -F(17, 70), -F(19, 140)],
            [-F(17, 70), F(18, 35), -F(1, 14)],
            [-F(19, 140), -F(1, 14), F(57, 140)],
        ],
        "R_matches_frozen": R
        == [
            [F(307, 630), -F(64, 315), -F(53, 630)],
            [-F(64, 315), F(131, 315), -F(4, 315)],
            [-F(53, 630), -F(4, 315), F(187, 630)],
        ],
        "atom_mass_polynomial_one": sum_p == [ONE, ZERO, ZERO, ZERO],
        "p1_mass_zero": all(x == [ZERO, ZERO, ZERO, ZERO] for x in p1_mass),
        "p2_mass_zero": all(x == [ZERO, ZERO, ZERO, ZERO] for row in p2_mass for x in row),
        "structure_conditions": structure["connected_on_closed_interval"]
        and structure["heterogeneous_diagonal_on_closed_interval"]
        and structure["distinct_spectrum_on_closed_interval"]
        and structure["spectral_margin"] == F(1, 25),
        "six_over_25_certified": largest["success"]
        and largest["passed"] == 173
        and largest["failed"] == 0
        and largest["min_atom_lower"] == F(63029, 5000000)
        and largest["min_margin"] > 0,
        "failed_expansion_points_not_certified": not [a for a in attempts if a["radius"] == F(49, 200)][0]["success"]
        and not [a for a in attempts if a["radius"] == F(1, 4)][0]["success"],
        "author_certificate_matches_independent": author_compare["attempts_match_independent"]
        and author_compare["script_hash_matches_json"],
    }
    report = {
        "status": "CORRECT" if all(exact_checks.values()) else "CRITICAL_GAPS",
        "method": "independent exact-event/Mobius atom jets, rational interval logs, adaptive subdivision, Gershgorin",
        "coordinate_order": COORDS,
        "line": {
            "K0": K0,
            "R": R,
            "spectral_theta": [F(1, 5), F(1, 2), F(4, 5)],
            "spectral_rate": [F(1, 5), F(1, 3), F(2, 3)],
        },
        "structure": structure,
        "atom_mass_checks": {
            "sum_p": sum_p,
            "all_p1_mass_zero": exact_checks["p1_mass_zero"],
            "all_p2_mass_zero": exact_checks["p2_mass_zero"],
        },
        "endpoint_atoms": endpoint_atoms,
        "attempts": [
            {
                "radius": a["radius"],
                "success": a["success"],
                "passed": a["passed"],
                "failed": a["failed"],
                "splits": a["splits"],
                "spectral_margin": a["spectral_margin"],
                "min_margin": a["min_margin"],
                "min_margin_decimal": a["min_margin_decimal"],
                "min_atom_lower": a["min_atom_lower"],
                "leaf_hash_sha256": a["leaf_hash_sha256"],
                "first_failed_intervals": a["first_failed_intervals"],
            }
            for a in attempts
        ],
        "failed_radius_float_scouts": float_scouts,
        "author_compare": author_compare,
        "exact_checks": exact_checks,
        "denominators": {
            "events": 8,
            "coordinates": 6,
            "certified_subdivision_leaves_for_6_over_25": largest["passed"],
            "attempted_radii": len(attempts),
            "log_terms": 20,
            "max_depth": 10,
            "float_scout_points_per_failed_or_endpoint_radius": 101,
        },
        "fresh_script_sha256": sha256_file(Path(__file__)),
        "elapsed_seconds": time.time() - started,
        "exit_code": 0 if all(exact_checks.values()) else 1,
    }
    OUT.write_text(json.dumps(serialize(report), indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"exit_code": report["exit_code"], "out": str(OUT), "elapsed_seconds": report["elapsed_seconds"]}, indent=2))
    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
