# S1 rate bounds via extreme pasts

Status: the independent outer-factor implementation numerically excluded the first benchmark as a positive counterexample.  A later route-owner n=8 rational/interval certificate proves the same benchmark has a strict negative entropy-rate gap; my audit of that certificate is `CORRECT`.

This directory contains the rate subtask for the frozen S1 scalar stationary DPP problem.  The route here is independent of finite-window Hessian extrapolation: it bounds the actual entropy rate from finite suffixes and Lyons--Steif extreme-past kernels.

Main files:

- `proof_or_gap.md`: proof of the finite-suffix upper/lower bounds, the answer to the finite Fejer--Riesz corner question, and the exact remaining certificate gap.
- `scripts/rate_bounds.py`: numerical implementation of the finite-suffix bounds.
- `scripts/compare_boundary.py`: cross-check between the outer-factor boundary kernel and the route owner's rational residual kernel enclosure.
- `artifacts/benchmark_r16.json`: r<=16, n<=12 numerical witness for the supplied benchmark.
- `artifacts/boundary_compare.json`: numerical agreement of the two boundary-kernel constructions.
- `author_certificate_audit.md`: independent audit of the route-owner strict n=8 certificate.

For the supplied benchmark

```text
p = 1/2
a = (9/50, -3/25, 2/25)
b = (1/10, 2/25, -3/50)
tau = 1/4
```

the exact triangle-inequality margin is `3/50`, so both endpoint symbols and their complements are uniformly interior.

At suffix length `r=16`, the numerical rate bounds are:

```text
h(f_+) in [0.69239896730095973, 0.69239896730172723]
h(f_0) in [0.69242509149653586, 0.69242509149717146]
L_+(16) - U_0(16) = -2.6124196211729789e-05
U_+(16) - L_0(16) = -2.612419480862993e-05
```

Thus this benchmark is not a positive entropy-rate counterexample.  The route-owner strict n=8 certificate encloses the rate gap in

```text
[-2.6204849038956574e-05, -2.6051480851662238e-05],
```

so the fixed benchmark is now certified negative, within that separate author artifact and this audit.
