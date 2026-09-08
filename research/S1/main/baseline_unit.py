"""One bounded, actually invoked fixed-symbol diagnostic; all numbers are floats."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
from fractions import Fraction

import numpy as np
import scipy
from scipy.linalg import toeplitz


def masses(kernel):
    n = len(kernel)
    if not n:
        return np.ones(1), {"normalization_error": 0.0, "imaginary_error": 0.0}
    bits = ((np.arange(2**n, dtype=np.uint64)[:, None] >>
             np.arange(n, dtype=np.uint64)) & 1).astype(float)
    result = np.empty(2**n)
    imag = 0.0
    for start in range(0, 2**n, 256):
        chunk = bits[start:start+256]
        q = np.broadcast_to(kernel, (len(chunk), n, n)).copy()
        q[:, np.arange(n), np.arange(n)] -= 1-chunk
        sign = (-1.0)**np.sum(1-chunk, axis=1)
        z = sign*np.linalg.det(q)
        imag = max(imag, float(np.max(np.abs(z.imag))))
        result[start:start+len(chunk)] = z.real
    if np.min(result) <= 0 or abs(result.sum()-1) > 1e-10 or imag > 1e-10:
        raise RuntimeError("invalid event mass diagnostics")
    return result, {"normalization_error": float(abs(result.sum()-1)),
                    "imaginary_error": imag, "minimum_probability": float(result.min())}


def entropy(probs):
    return float(-np.dot(probs, np.log(probs)))


def kernel(candidate, t, n):
    a = [float(Fraction(x)) for x in candidate["a"]]
    b = [float(Fraction(x)) for x in candidate["b"]]
    col = np.zeros(n, dtype=complex)
    if n:
        col[0] = float(Fraction(candidate["p"]))
    for k in range(1, min(n, len(a)+1)):
        col[k] = (a[k-1]-1j*t*b[k-1])/2
    return toeplitz(col, col.conj())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-n", type=int, default=12)
    args = parser.parse_args()
    if not 1 <= args.max_n <= 14:
        raise ValueError("this unit is bounded at n<=14")
    started = time.time()
    candidate_path = Path(args.candidate)
    candidate = json.loads(candidate_path.read_text())
    tau = float(Fraction(candidate["tau"]))
    m = len(candidate["a"])
    eps = float(Fraction(candidate["uniform_margin"]))
    rows = []
    for t in [-tau, 0.0, tau]:
        previous = 0.0
        for n in range(1, args.max_n+1):
            K = kernel(candidate, t, n)
            p, diag = masses(K)
            H = entropy(p)
            # m-dependence lower bound: separated n-blocks with m-site gaps.
            lower_dependence = H/(n+m)
            # Finite T2 inequality applied to arbitrarily many n-blocks.
            # Boundary Frobenius energy per cut <=2 sum k |c_k|^2.
            energy = sum(2*k*abs((float(Fraction(a))-1j*t*float(Fraction(b)))/2)**2
                         for k, (a, b) in enumerate(zip(candidate["a"], candidate["b"]), 1))
            lower_t2 = H/n-energy/(n*eps*(1-eps))
            row = {"t": t, "n": n, "H_n": H, "H_n_over_n": H/n,
                   "conditional_upper": H-previous,
                   "rate_lower_m_dependence_float": lower_dependence,
                   "rate_lower_T2_float": lower_t2,
                   "rate_lower_float": max(lower_dependence, lower_t2, 0.0),
                   "probability_count": len(p), **diag}
            rows.append(row)
            previous = H
    checks = []
    for n in [2, 3, 4, 6]:
        pm, _ = masses(kernel(candidate, -tau, n))
        pp, _ = masses(kernel(candidate, tau, n))
        checks.append({"n": n, "endpoint_event_equality_error": float(np.max(abs(pp-pm)))})
    gaps = []
    for n in range(1, args.max_n+1):
        values = [next(r for r in rows if r["t"] == t and r["n"] == n)
                  for t in [-tau, 0.0, tau]]
        rm, r0, rp = values
        gaps.append({"n": n,
                     "finite_gap": (rm["H_n"]+rp["H_n"])/2-r0["H_n"],
                     "increment_gap": (rm["conditional_upper"]+rp["conditional_upper"])/2-r0["conditional_upper"],
                     "rate_gap_lower_float": (rm["rate_lower_float"]+rp["rate_lower_float"])/2-r0["conditional_upper"],
                     "rate_gap_upper_float": (rm["conditional_upper"]+rp["conditional_upper"])/2-r0["rate_lower_float"]})
    record = {
        "status": "COMPLETED_FLOAT_DIAGNOSTIC_NOT_CERTIFICATE", "exit_status": 0,
        "pid": os.getpid(), "seed": None, "randomness": "none",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "candidate_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
        "argv": sys.argv, "threads": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"]},
        "seconds": time.time()-started, "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "candidate": candidate, "rows": rows, "gaps": gaps, "checks": checks,
        "actual_event_evaluations": sum(r["probability_count"] for r in rows)+sum(2*(2**n) for n in [2,3,4,6])
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps({k: record[k] for k in ["status", "pid", "seconds", "peak_rss_kib", "actual_event_evaluations"]}))
    print(json.dumps(gaps[-1]))


if __name__ == "__main__":
    main()
