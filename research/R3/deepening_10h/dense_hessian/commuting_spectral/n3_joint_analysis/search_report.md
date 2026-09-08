# D10-M6 search report

Status: **SCOUT_NO_POSITIVE_TOTAL_FOUND_AFTER_REPAIR**.

No server, GPU, package installation, or external dependency was used.  BLAS and
OpenMP thread counts were set to one.

## Review-triggered repair note

The first version of `joint_copositive_probe.py` had a simplex optimizer gap:
singular full-support KKT systems were skipped.  A verifier supplied

\[
M=\begin{pmatrix}-2&1&1\\1&-2&1\\1&1&-2\end{pmatrix},
\]

for which the true positive-simplex maximum is \(0\) at
\((1/3,1/3,1/3)\), while the old function returned a negative boundary value.
The old `joint_probe_results.json` is therefore retained only as deprecated
scout evidence.  It must not be cited as an exact simplex maximum certificate.

The same review also noted that \(\Psi''\le0\) is a stronger sufficient
condition, not a weaker one, and is now strictly disproved by certified positive
conditional curvature.  Only the total barrier inequality remains open.

## Run 1c: repaired positive-simplex plus sphere-gate scan

Script:

```text
research/R3/deepening_10h/dense_hessian/commuting_spectral/n3_joint_analysis/joint_copositive_probe.py
```

Command:

```text
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
research\R3\deepening_10h\dense_hessian\commuting_spectral\n3_joint_analysis\joint_copositive_probe.py
```

Exit code: `0`.

Recorded output:
`research/R3/deepening_10h/dense_hessian/commuting_spectral/n3_joint_analysis/joint_probe_results_v3.json`.

Denominators:

- result version: `v3_relative_kkt_scaled_regression`;
- script SHA256:
  `6d275dc10ffa5466f7ead81277fd622c64378f5e020eeb3dd8345aec3a085b9a`;
- seed: `2026090836`;
- strict theta clip: `1e-5`;
- structured base points: `384`;
- random base points requested: `60000`;
- total base points checked: `60384`;
- exact atoms per evaluated direction: `8`;
- directions per reconstructed Hessian: `6`;
- positive-sphere support eigenvector candidates evaluated inside this run:
  `416691`;
- positive total \(H''\) candidates: `0`;
- sphere positive-gate hits: `0`;
- copositivity/simplex sign mismatches: `0`.

Optimizer regression:

```text
singular verifier matrix simplex value = -1.8503717077085963e-17
singular verifier matrix sphere value  = -6.409875621278563e-17
expected value                         = 0

scaled positive matrix simplex value   = 66666666666666.68
scaled positive matrix sphere value    = 200000000000000.0
expected simplex value                 = 66666666666666.664
expected sphere value                  = 200000000000000.0
```

The built-in exact-event sanity check compared the n=3 spectral-channel atoms
against direct Möbius atoms for one rational-angle test point:

- max atom discrepancy: `1.3877787807814457e-16`;
- finite-difference \(H''\): `-0.02619682248905519`;
- formula \(H''\): `-0.026194792217884618`;
- finite-difference absolute error: `2.0302711705721954e-06`.

Best total positive-simplex value was still negative:

\[
\max_{\sum v_i=1,\ v_i\ge0} v^\top Mv=-1.333333333333333.
\]

It occurred at

```text
theta = [0.5, 0.5, 0.5]
v = [0.33333333333333326, 0.33333333333333376, 0.33333333333333287]
```

with total components:

```text
count      = -0.6009251408879267
singleton  = -0.3662040962227032
pair       = -0.3662040962227032
psi        = -0.7324081924454064
total      = -1.3333333333333328
min_atom   = 0.125
```

Important negative-control observation: conditional curvature is strictly not
always nonpositive.  The v3 scan still found

```text
max psi'' over sampled simplex cones = 0.0006515928675194109
```

but at that point the count term was `-4.555005267657262`, so total curvature
remained `-4.554353674789741`.  Individual singleton and pair layers were much
more sign-indefinite:

```text
max singleton-layer value = 1.3512543977138942
max pair-layer value      = 1.5294877418335036
```

These observations keep the singleton/pair joint cancellation question alive
and rule out any proof that simply asserts each conditional layer is concave.

## Run 2: positive-orthant sphere support-eigenvector scan

Script:

```text
research/R3/deepening_10h/dense_hessian/commuting_spectral/n3_joint_analysis/sphere_support_probe.py
```

Command:

```text
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
research\R3\deepening_10h\dense_hessian\commuting_spectral\n3_joint_analysis\sphere_support_probe.py
```

Exit code: `0`.

Recorded output:
`research/R3/deepening_10h/dense_hessian/commuting_spectral/n3_joint_analysis/sphere_probe_results.json`.

Denominators:

- seed: `2026090837`;
- structured base points: `3456`;
- random base points requested: `80000`;
- total base points checked: `83456`;
- support sets per Hessian: `7`;
- support eigenvector candidates evaluated: `574547`;
- exact atoms per evaluated direction: `8`;
- directions per reconstructed Hessian: `6`;
- positive total \(H''\) candidates: `0`.

Best unit-sphere total value was still negative:

\[
\max_{\|v\|_2=1,\ v\ge0}v^\top Mv=-1.3375999999999997.
\]

It occurred at

```text
theta = [0.5, 0.5, 0.5]
v = [0.0, 0.0, 1.0]
support = [2]
```

with

```text
count      = -1.3333333333333333
singleton  = -0.002133333333333237
pair       = -0.002133333333333237
psi        = -0.004266666666666474
total      = -1.3375999999999997
min_atom   = 0.125
```

The largest observed ratio \(\Psi''/(-H(N)'')\) was still negative:

```text
psi_over_count_barrier = -8.541913678890443e-08
```

This occurred very near a strict boundary with min atom about
`1.0633201520854935e-10`, so it is useful only as a scout note, not as a
certificate.

## Interpretation

The new scans remove random sampling over \(v\) at each tested base point.  They
therefore provide stronger finite evidence than the earlier D10-M5 random
\((Q,\theta,v)\) search.  However, both scans are still finite numerical
searches over \((Q,\theta)\).  They do not prove the n=3 one-sign spectral-rate
claim.
