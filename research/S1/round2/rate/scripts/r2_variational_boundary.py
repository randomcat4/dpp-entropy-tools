"""Round-two variational extreme-past kernel enclosures for one fixed candidate."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import time

import mpmath as mp

try:
    import resource
except ImportError:  # pragma: no cover - Windows fallback for syntax checks.
    resource = None


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


def mpc(a):
    return mp.mpc(mp.mpf(a[0].numerator) / a[0].denominator, mp.mpf(a[1].numerator) / a[1].denominator)


def encode(a):
    return [str(a[0]), str(a[1])]


def quantize(a, bits):
    return (F(int(mp.nint(a.real * 2**bits)), 2**bits), F(int(mp.nint(a.imag * 2**bits)), 2**bits))


def coeffs(candidate, t, complement):
    p = F(candidate["p"]) + t * F(candidate["dp"])
    a = [F(x) + t * F(dx) for x, dx in zip(candidate["a"], candidate["da"])]
    b = [F(x) + t * F(dx) for x, dx in zip(candidate["b"], candidate["db"])]
    cs = [(p, F(0))] + [(aa / 2, -bb / 2) for aa, bb in zip(a, b)]
    if complement:
        cs = [(1 - p, F(0))] + [neg(c) for c in cs[1:]]
    return cs


def build_case(candidate, t, complement, M, bits):
    cs = coeffs(candidate, t, complement)
    m = len(cs) - 1
    eps = F(candidate["uniform_margin"])

    def c(k):
        if 0 <= k <= m:
            return cs[k]
        if -m <= k < 0:
            return conj(cs[-k])
        return Z

    bblock = [[c(-r - 1 - j) for j in range(m)] for r in range(M)]
    tmat = mp.matrix([[mpc(c(s - r)) for s in range(M)] for r in range(M)])
    xmat = [[Z for _ in range(m)] for _ in range(M)]
    for j in range(m):
        rhs = mp.matrix([mpc(bblock[r][j]) for r in range(M)])
        sol = mp.lu_solve(tmat, rhs)
        for r in range(M):
            xmat[r][j] = quantize(sol[r], bits)

    # With degree m and M supported rows in X, only rows 0,...,M+m-1 can be nonzero.
    residual = []
    for r in range(M + m):
        row = []
        for j in range(m):
            value = c(-r - j - 1)
            for s in range(max(0, r - m), min(M, r + m + 1)):
                value = sub(value, mul(c(s - r), xmat[s][j]))
            row.append(value)
        residual.append(row)

    r_bound = sum(norm1(x) for row in residual for x in row)
    delta = r_bound * r_bound / eps

    bx = [[Z for _ in range(m)] for _ in range(m)]
    xr = [[Z for _ in range(m)] for _ in range(m)]
    for i in range(m):
        for j in range(m):
            for r in range(M):
                bx[i][j] = add(bx[i][j], mul(conj(bblock[r][i]), xmat[r][j]))
                xr[i][j] = add(xr[i][j], mul(conj(xmat[r][i]), residual[r][j]))

    old = [[sub(c(i - j), scale(add(bx[i][j], conj(bx[j][i])), F(1, 2))) for j in range(m)] for i in range(m)]
    corner = [[sub(old[i][j], scale(add(xr[i][j], conj(xr[j][i])), F(1, 2))) for j in range(m)] for i in range(m)]

    return {
        "t": str(t),
        "complement_symbol": complement,
        "M": M,
        "dyadic_bits": bits,
        "epsilon": str(eps),
        "R_norm_bound": str(r_bound),
        "operator_error_upper_rational": str(delta),
        "operator_error_upper_float": float(delta),
        "enclosure_method": "VARIATIONAL_RESIDUAL_SQUARED",
        "corner_rational": [[encode(x) for x in row] for row in corner],
        "corner_float": [[[float(x[0]), float(x[1])] for x in row] for row in corner],
        "solution_dyadic": [[encode(x) for x in row] for row in xmat],
        "residual_rows_checked": M + m,
    }


def peak_rss_kib():
    if resource is None:
        return None
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--M", type=int, default=64)
    parser.add_argument("--bits", type=int, default=160)
    args = parser.parse_args()
    if not 8 <= args.M <= 64:
        raise ValueError("bounded unit supports 8<=M<=64")
    started = time.time()
    mp.mp.dps = 80
    candidate_path = Path(args.candidate)
    candidate = json.loads(candidate_path.read_text())
    tau = F(candidate["tau"])
    cases = [build_case(candidate, t, comp, args.M, args.bits) for t in (-tau, F(0), tau) for comp in (False, True)]
    out = {
        "status": "R2_VARIATIONAL_KERNEL_ENCLOSURES_COMPUTED_REVIEW_PENDING",
        "exit_status": 0,
        "pid": os.getpid(),
        "seed": None,
        "randomness": "none",
        "python": platform.python_version(),
        "mpmath": mp.__version__,
        "mp_dps": mp.mp.dps,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "candidate_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "command": "python research/S1/round2/rate/scripts/r2_variational_boundary.py --candidate research/S1/round2/rate/candidate.json --output research/S1/round2/rate/artifacts/r2_boundary_M64.json --M 64 --bits 160",
        "threads": {k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "BLIS_NUM_THREADS")},
        "seconds": time.time() - started,
        "peak_rss_kib": peak_rss_kib(),
        "actual_cases": len(cases),
        "actual_residual_complex_entries": sum((c["M"] + len(candidate["a"])) * len(candidate["a"]) for c in cases),
        "cases": cases,
    }
    Path(args.output).write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: out[k] for k in ("status", "pid", "seconds", "peak_rss_kib", "actual_cases")}))
    print(json.dumps([{"t": c["t"], "complement": c["complement_symbol"], "error": c["operator_error_upper_float"]} for c in cases]))


if __name__ == "__main__":
    main()
