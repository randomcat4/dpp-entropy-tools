"""Exact/interval entropy-rate enclosure for the round-two three-symbol object."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time

import mpmath as mp

try:
    import resource
except ImportError:  # pragma: no cover - Windows fallback for syntax checks.
    resource = None

from r2_variational_boundary import Z, add, sub, neg, conj, mul


def divide_exact(a, b):
    d = b[0] * b[0] + b[1] * b[1]
    re = a[0] * b[0] + a[1] * b[1]
    im = a[1] * b[0] - a[0] * b[1]
    if not d or re % d or im % d:
        raise ArithmeticError("non-exact Bareiss division")
    return (re // d, im // d)


def event_masses(kernel):
    n = len(kernel)
    denominator = 1
    for row in kernel:
        for x in row:
            denominator = math.lcm(denominator, x[0].denominator, x[1].denominator)
    amat = [[(int(x[0] * denominator), int(x[1] * denominator)) for x in row] for row in kernel]
    output = []
    for event in range(2**n):
        qmat = [row.copy() for row in amat]
        zeros = 0
        for i in range(n):
            if not ((event >> i) & 1):
                qmat[i][i] = (qmat[i][i][0] - denominator, qmat[i][i][1])
                zeros += 1
        previous = (1, 0)
        for k in range(n - 1):
            pivot = qmat[k][k]
            if pivot == (0, 0):
                raise ArithmeticError("zero principal event pivot")
            for i in range(k + 1, n):
                for j in range(k + 1, n):
                    qmat[i][j] = divide_exact(sub(mul(qmat[i][j], pivot), mul(qmat[i][k], qmat[k][j])), previous)
            previous = pivot
        det = qmat[-1][-1]
        if det[1]:
            raise ArithmeticError("nonreal Hermitian determinant")
        p = F((-1) ** zeros * det[0], denominator**n)
        if p <= 0:
            raise ArithmeticError("nonpositive strict-interior event")
        output.append(p)
    if sum(output) != 1:
        raise ArithmeticError("exact mass normalization failed")
    return output


def coeffs(candidate, t):
    p = F(candidate["p"]) + t * F(candidate["dp"])
    a = [F(x) + t * F(dx) for x, dx in zip(candidate["a"], candidate["da"])]
    b = [F(x) + t * F(dx) for x, dx in zip(candidate["b"], candidate["db"])]
    return [(p, F(0))] + [(aa / 2, -bb / 2) for aa, bb in zip(a, b)]


def symbol_kernel(candidate, t, n):
    cs = coeffs(candidate, t)
    m = len(cs) - 1

    def c(k):
        if 0 <= k <= m:
            return cs[k]
        if -m <= k < 0:
            return conj(cs[-k])
        return Z

    return [[c(i - j) for j in range(n)] for i in range(n)]


def ivf(x):
    return mp.iv.mpf(x.numerator) / mp.iv.mpf(x.denominator)


def rational_endpoint(x, upper):
    q = x._mpi_[1 if upper else 0]
    sign, man, exponent, _ = q
    return F((-1 if sign else 1) * man) * F(2) ** exponent


def interval_string(x):
    lower = rational_endpoint(x, False)
    upper = rational_endpoint(x, True)
    return {"lower": str(lower), "upper": str(upper), "lower_float": float(lower), "upper_float": float(upper)}


def interval_bounds(lower, upper):
    return mp.iv.mpf([ivf(lower).a, ivf(upper).b])


def binary(x):
    if x in (0, 1):
        return mp.iv.mpf(0)
    z = ivf(x)
    return -z * mp.iv.log(z) - (1 - z) * mp.iv.log(1 - z)


def find_case(boundary, t, complement):
    for case in boundary["cases"]:
        if F(case["t"]) == t and bool(case["complement_symbol"]) == complement:
            return case
    raise KeyError(f"missing boundary case t={t}, complement={complement}")


def case_bound(candidate, boundary, t, n):
    m = len(candidate["a"])
    eps = F(candidate["uniform_margin"])
    kernel = symbol_kernel(candidate, t, n + 1)
    raw = event_masses(kernel)
    extreme = []
    errors = []
    case_summaries = []
    for complement in (False, True):
        case = find_case(boundary, t, complement)
        amat = [row.copy() for row in kernel]
        for i in range(m):
            for j in range(m):
                value = tuple(map(F, case["corner_rational"][i][j]))
                if complement:
                    value = sub((F(int(i == j)), F(0)), value)
                amat[i][j] = value
        probs = event_masses(amat)
        extreme.append(probs)
        delta = F(case["operator_error_upper_rational"])
        if delta >= eps:
            raise ArithmeticError("kernel error exceeds margin")
        error = delta * (1 + ((1 + delta) / (eps - delta)) ** 2)
        errors.append(error)
        case_summaries.append(
            {
                "complement_symbol": complement,
                "boundary_operator_error": str(delta),
                "conditional_error_bound": str(error),
                "boundary_method": case.get("enclosure_method"),
            }
        )

    lower = mp.iv.mpf(0)
    upper = mp.iv.mpf(0)
    width = mp.iv.mpf(0)
    min_interval = F(1)
    max_interval = F(0)
    for event in range(2**n):
        idx1 = event + (1 << n)
        weight = raw[event] + raw[idx1]
        q = raw[idx1] / weight
        q1 = extreme[0][idx1] / (extreme[0][event] + extreme[0][idx1])
        q0 = extreme[1][idx1] / (extreme[1][event] + extreme[1][idx1])
        lo = max(eps, q1 - errors[0])
        hi = min(1 - eps, q0 + errors[1])
        if lo > hi or q < lo or q > hi:
            raise ArithmeticError("extreme-past conditional order failed")
        h_lo = binary(lo)
        h_hi = binary(hi)
        low = min(rational_endpoint(h_lo, False), rational_endpoint(h_hi, False))
        high = min(rational_endpoint(h_lo, True), rational_endpoint(h_hi, True))
        lower += ivf(weight) * interval_bounds(low, high)
        upper += ivf(weight) * binary(q)
        width += ivf(weight) * ivf(hi - lo)
        min_interval = min(min_interval, lo)
        max_interval = max(max_interval, hi)

    return {
        "t": str(t),
        "past_length": n,
        "lower_bound_interval": interval_string(lower),
        "upper_bound_interval": interval_string(upper),
        "weighted_extreme_width": interval_string(width),
        "boundary_cases": case_summaries,
        "exact_determinants": 3 * 2 ** (n + 1),
        "normalization": "EXACT_FRACTION_EQUALITY",
        "conditional_range": [str(min_interval), str(max_interval)],
    }


def peak_rss_kib():
    if resource is None:
        return None
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--boundary", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--n", type=int, default=4)
    args = parser.parse_args()
    if not 3 <= args.n <= 12:
        raise ValueError("bounded unit supports 3<=n<=12")
    started = time.time()
    mp.iv.dps = 45
    candidate_path = Path(args.candidate)
    boundary_path = Path(args.boundary)
    candidate = json.loads(candidate_path.read_text())
    boundary = json.loads(boundary_path.read_text())
    tau = F(candidate["tau"])
    cases = [case_bound(candidate, boundary, t, args.n) for t in (-tau, F(0), tau)]
    minus, center, plus = cases
    gap_lower = (F(minus["lower_bound_interval"]["lower"]) + F(plus["lower_bound_interval"]["lower"])) / 2 - F(center["upper_bound_interval"]["upper"])
    gap_upper = (F(minus["upper_bound_interval"]["upper"]) + F(plus["upper_bound_interval"]["upper"])) / 2 - F(center["lower_bound_interval"]["lower"])
    out = {
        "status": "R2_RATE_ENCLOSURE_COMPUTED_REVIEW_PENDING",
        "pid": os.getpid(),
        "exit_status": 0,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "boundary_source_sha256": boundary.get("source_sha256"),
        "candidate_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        "boundary_sha256": hashlib.sha256(boundary_path.read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "mpmath": mp.__version__,
        "interval_dps": mp.iv.dps,
        "argv": sys.argv,
        "command": f"python research/S1/round2/rate/scripts/r2_rate_certificate.py --candidate research/S1/round2/rate/candidate.json --boundary research/S1/round2/rate/artifacts/r2_boundary_M64.json --output research/S1/round2/rate/artifacts/r2_rate_n{args.n}.json --n {args.n}",
        "seed": None,
        "randomness": "none",
        "threads": {k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "BLIS_NUM_THREADS")},
        "seconds": time.time() - started,
        "peak_rss_kib": peak_rss_kib(),
        "actual_determinants": sum(c["exact_determinants"] for c in cases),
        "cases": cases,
        "gap_enclosure": {"lower": str(gap_lower), "upper": str(gap_upper), "lower_float": float(gap_lower), "upper_float": float(gap_upper)},
        "classification": "NEGATIVE_PAIR_GAP" if gap_upper < 0 else "POSITIVE_COUNTEREXAMPLE_CANDIDATE" if gap_lower > 0 else "INCONCLUSIVE",
    }
    Path(args.output).write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: out[k] for k in ("status", "pid", "seconds", "peak_rss_kib", "actual_determinants", "classification")}))
    print(json.dumps(out["gap_enclosure"]))


if __name__ == "__main__":
    main()
