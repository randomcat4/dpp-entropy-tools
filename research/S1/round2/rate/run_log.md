# Run Log

All executed round-two certificate work used the isolated server checkout for the rate child.  No GPU, no system dependency installation and no parallel numerical jobs were used.

Runtime:

```text
Python 3.12.3
NumPy 2.1.2
mpmath 1.3.0
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
BLIS_NUM_THREADS=1
```

## Boundary Unit

Command shape:

```text
/opt/venv/bin/python research/S1/round2/rate/scripts/r2_variational_boundary.py \
  --candidate research/S1/round2/rate/candidate.json \
  --output research/S1/round2/rate/artifacts/r2_boundary_M64.json \
  --M 64 \
  --bits 160
```

Recorded metadata:

```text
exit status: 0
pid: 161244
seconds: 6.794719219207764
peak_rss_kib: 22580
actual cases: 6
actual residual complex entries: 1206
source sha256: 7174665d976b4e63490696a2dc8b23160c0ad3ab12668ea1b05c02fbd1f9907c
candidate sha256: d92793f7196a4eefaece91b3f37e65dec6744f61711363030cd81259aa1ccf09
artifact sha256: 921b8039baf5464b4c14f07b75cf52ff25a0195cc285a8ff25c7fa20ce26bc47
seed: none
randomness: none
```

Coverage:

```text
t=-1/8, complement=false
t=-1/8, complement=true
t=0,    complement=false
t=0,    complement=true
t=1/8,  complement=false
t=1/8,  complement=true
```

Worst operator-error bound: `4.5184132950619655e-28`.

## Rate Unit

Command shape:

```text
/opt/venv/bin/python research/S1/round2/rate/scripts/r2_rate_certificate.py \
  --candidate research/S1/round2/rate/candidate.json \
  --boundary research/S1/round2/rate/artifacts/r2_boundary_M64.json \
  --output research/S1/round2/rate/artifacts/r2_rate_n4.json \
  --n 4
```

Recorded metadata:

```text
exit status: 0
pid: 161258
seconds: 0.060981035232543945
peak_rss_kib: 22588
actual determinants: 288
classification: NEGATIVE_PAIR_GAP
source sha256: 244dee715d56ea9cabe8873ca140112048a1eda6d0fe07e24e30c0f9123be201
boundary sha256: 921b8039baf5464b4c14f07b75cf52ff25a0195cc285a8ff25c7fa20ce26bc47
candidate sha256: d92793f7196a4eefaece91b3f37e65dec6744f61711363030cd81259aa1ccf09
artifact sha256: 3fe57b224676ea48cd5eaaf772603da2626e921adfc0d13bcc117e30761567d2
seed: none
randomness: none
```

The `n=4` interval separated zero, so `n=8` was not run.

## Independent Floating Cross-Checks

Before the strict run, the existing round-one outer-factor implementation was used as a fixed-B1 floating precheck.  The source functions were `spectral_factor_outer` and `boundary_kernel_from_outer` from `research/S1/rate/scripts/rate_bounds.py`, called from a transient local B1-specific scratch calculation.  This precheck used one object only: the frozen round-two B1 candidate in `candidate.json`, with the three separate symbols `t=-1/8`, `t=0`, and `t=1/8`.  It was not a phase sweep, not one of the phase-19-center / 38-H jobs, and not part of the strict JSON certificate.

The floating precheck covered both gates for the fixed B1 object.  The event scale below counts the same raw and two extreme event-mass blocks that the strict script later materializes exactly: `3` symbols times `3` mass blocks per symbol times `2^(r+1)` binary events.

```text
r=4:  fixed objects 1; symbols 3; past words per symbol 16; event-equivalent count 288
r=6:  fixed objects 1; symbols 3; past words per symbol 64; event-equivalent count 1152
r=8:  fixed objects 1; symbols 3; past words per symbol 256; event-equivalent count 4608
r=10: fixed objects 1; symbols 3; past words per symbol 1024; event-equivalent count 18432
```

The approximate gates were:

```text
r=4:  positive gate -3.034890292497039e-05; negative gate -7.346045680090008e-06
r=6:  positive gate -1.887637041586565e-05; negative gate -1.8266608873052093e-05
r=8:  positive gate -1.8567865813001738e-05; negative gate -1.8549702298753523e-05
r=10: positive gate -1.855849587240055e-05; negative gate -1.8557989347245396e-05
```

The `r=10` line therefore records a real floating precheck on the already frozen B1 object.  The strict certificate stopped at `n=4` because the interval file `r2_rate_n4.json` already separates zero; no strict `n=8` or `n=10` run was needed.

After the strict boundary run, comparing all six variational corners to the outer-factor corners gave maximum difference `1.55431223e-15`.
