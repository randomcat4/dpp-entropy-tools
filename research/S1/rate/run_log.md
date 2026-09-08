# Run Log

All local numerical runs used the Codex bundled Python runtime:

```text
Python 3.12.14
Numpy 2.3.5
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
BLIS_NUM_THREADS=1
```

No GPU and no system dependency installation were used.

## rate bounds

Command shape:

```text
python scripts/rate_bounds.py --max-r 16 --block-n 12 --out artifacts/benchmark_r16.json
```

Recorded output:

```text
exit status: 0
pid: 36264
script sha256: 3c28127440d145ea894f5f80fd3b1a7d1c382c9c5420bbd844601405ae09b74b
coverage: r=1..16 for f_-, f_0, f_+; block n=1..12 for f_-, f_0, f_+
random seed: none
```

## boundary cross-check

Command shape:

```text
python scripts/compare_boundary.py --residual-json <route-owner boundary_residual_M64.json> --out artifacts/boundary_compare.json
```

Recorded output:

```text
exit status: 0
residual sha256: 90c313c56ef3a5bf522c7906c1bb782a0ff61b50ed6fe256aba098ac15f4ad6b
max outer-vs-residual corner difference: 8.3266727e-16
random seed: none
```

## author certificate audit

Read-only audit inputs:

```text
commit a98811c6597577f73128aaed3fd7dde6169af350
rate_certificate_proof.md
rational_rate_certificate.py
rational_rate_n8.json
boundary_residual.py
boundary_residual_proof.md
baseline_candidate.json
```

Independent comparison from `artifacts/benchmark_r16.json`, restricted to `r=8`:

```text
mine lower gate:  -2.6204663531426142e-05
mine upper gate:  -2.6051588097764089e-05
author interval: [-2.6204849038956574e-05, -2.6051480851662238e-05]
```
