#!/usr/bin/env python3
"""D10-S8b preconditioned interval expansion.

This is an additive script: it imports the S8 exact-event interval machinery but
does not modify the frozen S8 files.  The new proof gate first tries the old
coordinate Gershgorin test.  If that fails, it computes a rational upper
triangular approximation P to the inverse Cholesky preconditioner at the
subinterval midpoint and certifies P^T B(t) P by rigorous interval Gershgorin.

If P is invertible and P^T B P is positive definite for every t in the interval,
then B is positive definite there.  P is made upper triangular with positive
rational diagonal, so invertibility is certified by its diagonal.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

import segment_hessian_certificate as s8

if s8.np is None:
    raise SystemExit("numpy is required only to propose rational preconditioners")


HERE = Path(__file__).resolve().parent
ZERO = F(0)
ONE = F(1)
NVAR = s8.NVAR


def serialize(obj):
    return s8.serialize(obj)


def interval_matrix_transform(B, P):
    """Rigorous interval enclosure of P^T B P, P rational."""
    out = [[(ZERO, ZERO) for _ in range(NVAR)] for _ in range(NVAR)]
    for a in range(NVAR):
        for b in range(a, NVAR):
            acc = (ZERO, ZERO)
            for i in range(NVAR):
                if P[i][a] == 0:
                    continue
                for j in range(NVAR):
                    if P[j][b] == 0:
                        continue
                    coeff = P[i][a] * P[j][b]
                    acc = s8.iadd(acc, s8.iscale(coeff, B[i][j]))
            out[a][b] = acc
            out[b][a] = acc
    return out


def rational_inverse_cholesky_preconditioner(jets, interval, max_den: int):
    mid = (interval[0] + interval[1]) / 2
    Bdec = s8.B_decimal_at(jets, mid, prec=90)
    Bnp = s8.np.array([[float(x) for x in row] for row in Bdec], dtype=float)
    chol = s8.np.linalg.cholesky(Bnp)
    pinv = s8.np.linalg.inv(chol.T)  # upper triangular ideal preconditioner
    P = [[ZERO for _ in range(NVAR)] for _ in range(NVAR)]
    diag = []
    for i in range(NVAR):
        for j in range(NVAR):
            if i > j:
                P[i][j] = ZERO
            else:
                val = F(float(pinv[i, j])).limit_denominator(max_den)
                P[i][j] = val
        diag.append(P[i][i])
    if not all(d > 0 for d in diag):
        raise ValueError("non-positive rational preconditioner diagonal")
    return P, diag


def compact_rows(g):
    return [row["margin"] for row in g["rows"]]


def certify_leaf(jets, interval, log_terms: int, denominators: list[int]):
    B, p0_ints = s8.B_interval_matrix(jets, interval, log_terms)
    plain = s8.gershgorin_for_B(B)
    if plain["all_rows_positive"]:
        return {
            "pass": True,
            "method": "plain_gershgorin",
            "interval": interval,
            "min_atom_lower": min(p[0] for p in p0_ints),
            "min_margin": plain["min_margin"],
            "row_margins": compact_rows(plain),
        }
    attempts = [{
        "method": "plain_gershgorin",
        "min_margin": plain["min_margin"],
        "row_margins": compact_rows(plain),
    }]
    for den in denominators:
        P, diag = rational_inverse_cholesky_preconditioner(jets, interval, den)
        T = interval_matrix_transform(B, P)
        g = s8.gershgorin_for_B(T)
        item = {
            "method": "preconditioned_gershgorin",
            "max_den": den,
            "preconditioner_diag": diag,
            "min_margin": g["min_margin"],
            "row_margins": compact_rows(g),
        }
        attempts.append(item)
        if g["all_rows_positive"]:
            return {
                "pass": True,
                "method": "preconditioned_gershgorin",
                "max_den": den,
                "interval": interval,
                "min_atom_lower": min(p[0] for p in p0_ints),
                "min_margin": g["min_margin"],
                "row_margins": compact_rows(g),
                "preconditioner_diag": diag,
                "preconditioner_upper_triangular": P,
            }
    return {
        "pass": False,
        "interval": interval,
        "min_atom_lower": min(p[0] for p in p0_ints),
        "attempts": attempts,
    }


def certify_radius_preconditioned(jets, radius: F, log_terms: int, max_depth: int, denominators: list[int]):
    queue = [(-radius, radius, 0)]
    passed = []
    failed = []
    splits = 0
    method_counts = {}
    while queue:
        a, b, depth = queue.pop()
        interval = (a, b)
        try:
            leaf = certify_leaf(jets, interval, log_terms, denominators)
        except Exception as exc:
            leaf = {"pass": False, "interval": interval, "error": repr(exc)}
        if leaf["pass"]:
            passed.append(leaf)
            method_counts[leaf["method"]] = method_counts.get(leaf["method"], 0) + 1
            continue
        if depth < max_depth:
            mid = (a + b) / 2
            queue.append((mid, b, depth + 1))
            queue.append((a, mid, depth + 1))
            splits += 1
        else:
            leaf["depth"] = depth
            failed.append(leaf)
    min_margin = min((p["min_margin"] for p in passed), default=None)
    min_atom = min((p["min_atom_lower"] for p in passed), default=None)
    return {
        "radius": radius,
        "success": bool(passed) and not failed,
        "passed": len(passed),
        "failed": len(failed),
        "splits": splits,
        "log_terms": log_terms,
        "max_depth": max_depth,
        "denominators": denominators,
        "spectral_margin": s8.spectral_margin_for_radius(radius),
        "method_counts": method_counts,
        "min_margin": min_margin,
        "min_atom_lower": min_atom,
        "passed_leaf_ledger": [
            {
                "interval": p["interval"],
                "method": p["method"],
                "max_den": p.get("max_den"),
                "min_atom_lower": p["min_atom_lower"],
                "min_margin": p["min_margin"],
                "preconditioner_diag": p.get("preconditioner_diag"),
                "preconditioner_upper_triangular": p.get("preconditioner_upper_triangular"),
            }
            for p in sorted(passed, key=lambda x: x["interval"][0])
        ],
        "failed_leaf_ledger": [
            {
                "interval": f["interval"],
                "min_atom_lower": f.get("min_atom_lower"),
                "error": f.get("error"),
                "last_attempt_min_margin": f.get("attempts", [{}])[-1].get("min_margin") if f.get("attempts") else None,
                "attempt_methods": [
                    {
                        "method": a.get("method"),
                        "max_den": a.get("max_den"),
                        "min_margin": a.get("min_margin"),
                    }
                    for a in f.get("attempts", [])
                ],
            }
            for f in sorted(failed, key=lambda x: x["interval"][0])
        ],
    }


def decimal_or_none(x):
    return None if x is None else str(s8.dec(x))


def summarize_attempt(a):
    return {
        "radius": a["radius"],
        "success": a["success"],
        "passed": a["passed"],
        "failed": a["failed"],
        "splits": a["splits"],
        "spectral_margin": a["spectral_margin"],
        "method_counts": a["method_counts"],
        "min_margin_decimal": decimal_or_none(a["min_margin"]),
        "min_atom_lower": a["min_atom_lower"],
    }


def main() -> int:
    K0, R = s8.m8_section5_line()
    jets = s8.build_atom_jets(K0, R)
    log_terms = 20
    denominators = [64, 256, 1024, 4096]
    planned = [
        (F(49, 200), 10),
        (F(1, 4), 10),
        (F(7, 25), 10),
        (F(29, 100), 11),
    ]
    attempts = []
    for radius, depth in planned:
        if s8.spectral_margin_for_radius(radius) <= 0:
            attempts.append({
                "radius": radius,
                "success": False,
                "passed": 0,
                "failed": 1,
                "splits": 0,
                "log_terms": log_terms,
                "max_depth": depth,
                "denominators": denominators,
                "spectral_margin": s8.spectral_margin_for_radius(radius),
                "method_counts": {},
                "min_margin": None,
                "min_atom_lower": None,
                "failed_leaf_ledger": [{"reason": "closed interval not strictly feasible"}],
            })
            continue
        attempts.append(certify_radius_preconditioned(jets, radius, log_terms, depth, denominators))

    successes = [a for a in attempts if a["success"]]
    largest = max(successes, key=lambda a: a["radius"]) if successes else None
    scouts = {}
    for radius in [F(29, 100), F(299, 1000)]:
        if s8.spectral_margin_for_radius(radius) > 0:
            scouts[s8.fstr(radius)] = s8.float_grid_scout(jets, radius, points=401)

    report = {
        "status": "PROOF_CANDIDATE_PENDING_FRESH_REVIEW" if largest else "SCOUT_BLOCKED",
        "relationship_to_s8": "additive expansion; original [-6/25,6/25] certificate files are not modified",
        "method": "plain Gershgorin first, then rational inverse-Cholesky preconditioned Gershgorin on failed leaves",
        "line": s8.line_nontriviality(K0, R),
        "log_terms": log_terms,
        "denominators": denominators,
        "attempts_summary": [summarize_attempt(a) for a in attempts],
        "largest_certified_radius": largest["radius"] if largest else None,
        "largest_certified_interval": [-largest["radius"], largest["radius"]] if largest else None,
        "largest_certified_min_margin": largest["min_margin"] if largest else None,
        "largest_certified_min_atom_lower": largest["min_atom_lower"] if largest else None,
        "largest_certified_leaf_ledger": largest["passed_leaf_ledger"] if largest else [],
        "failed_attempt_ledgers": {
            s8.fstr(a["radius"]): a["failed_leaf_ledger"]
            for a in attempts
            if not a["success"]
        },
        "manual_blockers": [
            {
                "radius": "299/1000",
                "spectral_margin": s8.spectral_margin_for_radius(F(299, 1000)),
                "status": "TIMEOUT_INTERRUPTED",
                "details": (
                    "A manual preconditioned run with log_terms=20, max_depth=12, "
                    "denominators=[64,256,1024] produced no result after roughly "
                    "150 seconds and was interrupted.  This is a cost/blocker "
                    "record, not a failed mathematical certificate and not a "
                    "positive-curvature candidate."
                ),
            }
        ],
        "float_grid_scouts": scouts,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    out = HERE / "s8b_preconditioned_certificate.json"
    out.write_text(json.dumps(serialize(report), indent=2), encoding="utf-8")
    summary = {
        "status": report["status"],
        "json": str(out),
        "largest_certified_radius": report["largest_certified_radius"],
        "largest_certified_interval": report["largest_certified_interval"],
        "largest_certified_min_margin_decimal": decimal_or_none(report["largest_certified_min_margin"]),
        "largest_certified_min_atom_lower": report["largest_certified_min_atom_lower"],
        "attempts_summary": report["attempts_summary"],
    }
    print(json.dumps(serialize(summary), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
