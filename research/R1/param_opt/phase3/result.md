# P3-01/P3-03 two-dimensional attack result

Mathematical status: `PROVED_CANDIDATE`, pending commit-bound review.

Numerical status: `FINITE_ATTACK_COMPLETE / NO_COUNTEREXAMPLE FOUND`.

The proof, not the finite search, is the principal result.  Its exact
determinant identity is replayed by `symbolic_check.py`.

## Preregistered finite denominator

- Seed: `20260908301`.
- Cap: 160,000 ordinary calls, 128 high-precision checks, one CPU thread,
  8 GiB, 1,800 seconds; no GPU.
- Actual formal calls: 120,000 boundary/flat/general event-coordinate samples
  plus 2,832 calls across 32 optimization restarts, for 122,832 total.
- All call IDs `1..122832` were unique, contiguous, and `OK`; SQLite
  `quick_check` returned `ok`.
- Exit code: 0; elapsed time: 249.415 seconds; terminal PID no longer existed.
- Robust positive Hessian candidates: zero.
- Two formal 90-digit rechecks succeeded.  Including two 64-call smoke runs,
  the ordinary finite denominator was 122,960.

The sampled spectral margins ranged from about `2.96e-17` to `0.481`, minimum
exact-event probability from `7.92e-23`, and `c^2` from `2.33e-26` to `0.250`.
These are floating coverage diagnostics, not interval certificates.

The largest raw floating Hessian value was `1.46e-11`, below the `1e-8`
promotion threshold.  A 90-digit reconstruction changed it to
`-5.2266e-12`; an independent directional formula agreed and its feasible
midpoint gap was `-1.7942e-18`.  It was therefore not promoted.

Two local high-precision smoke checks failed because the bundled local Python
lacked `mpmath`; the same two checks succeeded remotely at 90 digits.  An
initial symbolic assertion also rejected unsimplified expressions displayed
as `0*sqrt(2)`; explicit simplification fixed the test representation.  Both
failures are retained and neither was a mathematical counterexample.

Finite non-detection supplies no premise to the theorem proof.

