#!/usr/bin/env python3
"""Independent check of the round-two coarse event identity candidate."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

import finite_noncommuting_bsc_cert as base


def fs(x: F) -> str:
    return base.fs(x)


def ps(p):
    return [fs(x) for x in base.poly_trim(p)]


def pm_zero(n, m):
    return [[[F(0)] for _ in range(m)] for _ in range(n)]


def pm_eye(n):
    a = pm_zero(n, n)
    for i in range(n):
        a[i][i] = [F(1)]
    return a


def pm_from_const_dir(a, v):
    return [[[a[i][j], v[i][j]] for j in range(len(a[0]))] for i in range(len(a))]


def pm_add(a, b):
    return [[base.padd(a[i][j], b[i][j]) for j in range(len(a[0]))] for i in range(len(a))]


def pm_sub(a, b):
    return [[base.psub(a[i][j], b[i][j]) for j in range(len(a[0]))] for i in range(len(a))]


def pm_mul(a, b):
    out = pm_zero(len(a), len(b[0]))
    for i in range(len(a)):
        for j in range(len(b[0])):
            s = [F(0)]
            for k in range(len(b)):
                s = base.padd(s, base.pmul(a[i][k], b[k][j]))
            out[i][j] = base.poly_trim(s)
    return out


def pm_scale_poly(c, a):
    return [[base.pmul(c, a[i][j]) for j in range(len(a[0]))] for i in range(len(a))]


def pm_trace(a):
    s = [F(0)]
    for i in range(len(a)):
        s = base.padd(s, a[i][i])
    return s


def pm_minor(a, row, col):
    return [[a[i][j] for j in range(len(a)) if j != col] for i in range(len(a)) if i != row]


def pm_adjugate(a):
    n = len(a)
    out = pm_zero(n, n)
    for i in range(n):
        for j in range(n):
            c = base.det_poly(pm_minor(a, j, i))
            if (i + j) % 2:
                c = base.pneg(c)
            out[i][j] = c
    return out


def row_poly_quad(r, m):
    s = [F(0)]
    for i in range(len(r)):
        for j in range(len(r)):
            s = base.padd(s, base.pscale(r[i] * r[j], m[i][j]))
    return base.poly_trim(s)


def cross(u, v):
    return [
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    ]


def coarse_formula_poly(u, a, v, z, mask):
    bits = sum((mask >> i) & 1 for i in range(4))
    ap = pm_from_const_dir(a, v)
    d = base.det_poly(ap)
    if bits == 0:
        return base.det_poly(pm_sub(pm_eye(3), ap))
    if bits == 1:
        i = next(i for i in range(4) if (mask >> i) & 1)
        a2 = pm_mul(ap, ap)
        one_minus_tr = base.psub([F(1)], pm_trace(ap))
        m = pm_add(pm_add(a2, pm_scale_poly(one_minus_tr, ap)), pm_scale_poly(d, pm_eye(3)))
        return row_poly_quad(u[i], m)
    if bits == 2:
        rows = [i for i in range(4) if (mask >> i) & 1]
        w = cross(u[rows[0]], u[rows[1]])
        m = pm_sub(pm_adjugate(ap), pm_scale_poly(d, pm_eye(3)))
        return row_poly_quad(w, m)
    if bits == 3:
        missing = next(i for i in range(4) if ((mask >> i) & 1) == 0)
        return base.pscale(z[missing] * z[missing], d)
    return [F(0)]


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.DEVNULL).strip()


def main() -> int:
    if len(sys.argv) < 4:
        raise SystemExit("usage: coarse_identity_check.py MAIN_REPO COMMIT OUT_JSON")
    main_repo = Path(sys.argv[1])
    commit = sys.argv[2]
    out = Path(sys.argv[3])
    script = Path(__file__).resolve()
    rel = "research/N4/round2/coarse_event_candidate.md"
    raw = subprocess.check_output(["git", "-C", str(main_repo), "show", f"{commit}:{rel}"], text=True)
    blob = git(main_repo, "rev-parse", f"{commit}:{rel}")

    u, z, a, v = base.householder_fixture()
    ka = base.make_k(u, a)
    kv = base.make_k(u, v)
    determinant = {mask: base.event_poly(ka, kv, mask) for mask in range(16)}
    formula = {mask: coarse_formula_poly(u, a, v, z, mask) for mask in range(16)}
    mismatches = []
    for mask in range(16):
        if base.poly_trim(determinant[mask]) != base.poly_trim(formula[mask]):
            mismatches.append({"mask": mask, "determinant": ps(determinant[mask]), "formula": ps(formula[mask])})

    ap = pm_from_const_dir(a, v)
    d = base.det_poly(ap)
    d0 = base.peval(d, F(0))
    d1 = d[1] if len(d) > 1 else F(0)
    qsum = sum(zi * zi for zi in z)
    original_fisher = sum(-((zi * zi * d1) ** 2) / (zi * zi * d0) for zi in z)
    grouped_fisher = -(d1 * d1) / d0

    result = {
        "pid": os.getpid(),
        "argv": sys.argv,
        "python": sys.version,
        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "exit_status": 0,
        "source_commit": commit,
        "source_blob": blob,
        "source_sha256": hashlib.sha256(raw.encode()).hexdigest(),
        "fixture": "z=(1,2,2,4)/5 Householder U, rational noncommuting A,V",
        "formula_matches_independent_event_polynomials": len(mismatches) == 0,
        "mismatches": mismatches,
        "proper_formula_polynomials": {str(mask): ps(formula[mask]) for mask in range(15)},
        "full_formula_polynomial": ps(formula[15]),
        "detA_polynomial": ps(d),
        "sum_q": fs(qsum),
        "triple_fisher_original": fs(original_fisher),
        "triple_fisher_grouped": fs(grouped_fisher),
        "triple_fisher_preserved": original_fisher == grouped_fisher,
        "verdict": "CORRECT_IDENTITY_ONLY" if not mismatches and original_fisher == grouped_fisher and qsum == 1 else "CRITICAL_GAPS",
        "scope_note": "The twelve-symbol coarse vector is constrained polynomial data in A, not an affine free-simplex chord; this check makes no concavity claim.",
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
