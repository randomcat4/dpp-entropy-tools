#!/usr/bin/env python3
"""Independent checker for the S1 boundary residual enclosure artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

Z = (F(0), F(0))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def neg(a):
    return (-a[0], -a[1])


def sub(a, b):
    return add(a, neg(b))


def conj(a):
    return (a[0], -a[1])


def mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def scale(a, s):
    return (a[0] * s, a[1] * s)


def norm1(a):
    return abs(a[0]) + abs(a[1])


def encode(a):
    return [str(a[0]), str(a[1])]


def decode(a):
    return (F(a[0]), F(a[1]))


def coeffs(candidate, t, complement):
    p = F(candidate["p"])
    a = [F(x) for x in candidate["a"]]
    b = [F(x) for x in candidate["b"]]
    cs = [(p, F(0))] + [(aa / 2, -t * bb / 2) for aa, bb in zip(a, b)]
    if complement:
        cs = [(F(1) - p, F(0))] + [neg(c) for c in cs[1:]]
    return cs


def coeff(cs, lag):
    m = len(cs) - 1
    if 0 <= lag <= m:
        return cs[lag]
    if -m <= lag < 0:
        return conj(cs[-lag])
    return Z


def recompute_case(candidate, case):
    t = F(case["t"])
    complement = bool(case["complement_symbol"])
    M = int(case["M"])
    m = len(candidate["a"])
    eps = F(case["epsilon"])
    cs = coeffs(candidate, t, complement)
    X = [[decode(x) for x in row] for row in case["solution_dyadic"]]
    if len(X) != M or any(len(row) != m for row in X):
        raise AssertionError("solution_dyadic shape mismatch")

    B = [[coeff(cs, -r - 1 - j) for j in range(m)] for r in range(M)]
    residual = []
    for r in range(M + m):
        row = []
        for j in range(m):
            value = coeff(cs, -r - 1 - j)
            for s in range(max(0, r - m), min(M, r + m + 1)):
                value = sub(value, mul(coeff(cs, s - r), X[s][j]))
            row.append(value)
        residual.append(row)

    b_bound = sum(norm1(x) for row in B for x in row)
    r_bound = sum(norm1(x) for row in residual for x in row)
    delta = b_bound * r_bound / eps

    BX = [[Z for _ in range(m)] for __ in range(m)]
    for i in range(m):
        for j in range(m):
            for r in range(M):
                BX[i][j] = add(BX[i][j], mul(conj(B[r][i]), X[r][j]))
    corner = [
        [sub(coeff(cs, i - j), scale(add(BX[i][j], conj(BX[j][i])), F(1, 2))) for j in range(m)]
        for i in range(m)
    ]

    reported_corner = [[decode(x) for x in row] for row in case["corner_rational"]]
    checks = {
        "t": case["t"],
        "complement_symbol": complement,
        "M": M,
        "residual_rows_checked": case["residual_rows_checked"],
        "reported_error_upper_float": case["operator_error_upper_float"],
        "recomputed_B_norm_bound": str(b_bound),
        "recomputed_R_norm_bound": str(r_bound),
        "recomputed_delta": str(delta),
        "delta_float": float(delta),
        "B_norm_match": str(b_bound) == case["B_norm_bound"],
        "R_norm_match": str(r_bound) == case["R_norm_bound"],
        "delta_match": str(delta) == case["operator_error_upper_rational"],
        "corner_match": corner == reported_corner,
        "corner_hermitian": all(corner[i][j] == conj(corner[j][i]) for i in range(m) for j in range(m)),
        "B_zero_after_first_m_rows": all(B[r][j] == Z for r in range(m, M) for j in range(m)),
        "residual_tail_zero_spotcheck": True,
    }
    for r in range(M + m, M + m + 8):
        for j in range(m):
            value = coeff(cs, -r - 1 - j)
            for s in range(max(0, r - m), min(M, r + m + 1)):
                value = sub(value, mul(coeff(cs, s - r), X[s][j]))
            if value != Z:
                checks["residual_tail_zero_spotcheck"] = False
    checks["case_status"] = (
        "CORRECT"
        if all(
            checks[k]
            for k in [
                "B_norm_match",
                "R_norm_match",
                "delta_match",
                "corner_match",
                "corner_hermitian",
                "B_zero_after_first_m_rows",
                "residual_tail_zero_spotcheck",
            ]
        )
        else "CRITICAL_GAPS"
    )
    return checks


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception as exc:
        return f"UNAVAILABLE: {exc}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--boundary-json", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    boundary = json.loads(args.boundary_json.read_text(encoding="utf-8"))
    cases = [recompute_case(candidate, case) for case in boundary["cases"]]
    status = "CORRECT" if all(case["case_status"] == "CORRECT" for case in cases) else "CRITICAL_GAPS"
    result = {
        "status": status,
        "exit_status": 0,
        "pid": os.getpid(),
        "command": " ".join([sys.executable, *sys.argv]),
        "python": sys.version,
        "platform": platform.platform(),
        "git_head": git_head(),
        "seed": "deterministic-no-random-seed-used",
        "source_sha256": sha256_file(Path(__file__).resolve()),
        "candidate_sha256": sha256_file(args.candidate),
        "boundary_json_sha256": sha256_file(args.boundary_json),
        "cases_checked": len(cases),
        "coverage": {
            "residual_entries": "all reported residual rows and columns for each case",
            "tail": "8 zero rows after the proved finite support cutoff, spot-checked exactly",
            "corner": "all reported m by m corner entries recomputed exactly",
        },
        "max_delta_float": max(case["delta_float"] for case in cases),
        "cases": cases,
    }
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"status": status, "pid": os.getpid(), "exit": 0, "out": str(args.out)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
