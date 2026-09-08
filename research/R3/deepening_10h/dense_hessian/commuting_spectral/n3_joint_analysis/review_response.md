# D10-M6 response to initial review

Author status: **REVISED_PENDING_FRESH_REVIEW**.

Initial review found four issues:

1. `copositive_and_sphere_reduction.md` rendered the 3x3 \(\kappa(C)\) formula
   as a product because plus signs were missing.
2. `max_quadratic_on_simplex` skipped singular full-support KKT systems.  The
   verifier matrix

   \[
   \begin{pmatrix}
   -2&1&1\\
   1&-2&1\\
   1&1&-2
   \end{pmatrix}
   \]

   has true positive-simplex maximum \(0\), while the old function returned a
   negative value.
3. `joint_reduction.md` described \(\Psi''\le0\) as a weaker target.  This was
   backwards: it is a stronger sufficient condition than the total barrier
   inequality, and fresh review has strictly disproved it.
4. The simplex optimizer used fixed absolute thresholds, so large rescalings of
   a matrix could hide a positive KKT point.  The supplied regression family was
   \(10^{14}[[-10,6,6],[6,-10,6],[6,6,-10]]\), whose positive-simplex maximum
   is \(2\cdot10^{14}/3>0\).

Repairs made:

- The \(\kappa(C)\) formula now has explicit plus signs.
- `joint_copositive_probe.py` now solves augmented face KKT systems by
  scale-aware least-squares residual and includes regression checks for both
  the verifier matrix and a \(10^{14}\)-scaled positive matrix.
- The same script now also runs a support-eigenvector positive-sphere gate
  inside the repaired scan.
- The repaired run writes `joint_probe_results_v3.json`; the old
  `joint_probe_results.json` remains as deprecated scout output.
- `joint_reduction.md`, `search_report.md`, `hazards.md`, and `verdict.md` now
  state that conditional-layer concavity is false and that only the total
  count-barrier inequality remains open.

Repaired run:

```text
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
research\R3\deepening_10h\dense_hessian\commuting_spectral\n3_joint_analysis\joint_copositive_probe.py
```

Exit code: `0`.

Denominators:

- result version: `v3_relative_kkt_scaled_regression`;
- script SHA256:
  `6d275dc10ffa5466f7ead81277fd622c64378f5e020eeb3dd8345aec3a085b9a`;
- base points checked: `60384`;
- exact atoms per direction: `8`;
- directions per Hessian: `6`;
- support-sphere candidates inside repaired run: `416691`;
- positive total candidates: `0`;
- sphere positive-gate hits: `0`.

Regression:

```text
simplex value on verifier matrix = -1.8503717077085963e-17
sphere value on verifier matrix  = -6.409875621278563e-17
expected value                   = 0

scaled simplex value             = 66666666666666.68
scaled expected simplex value    = 66666666666666.664
scaled sphere value              = 200000000000000.0
scaled expected sphere value     = 200000000000000.0
```

The route remains **INCOMPLETE_SCOUT_NO_HIT_AFTER_REPAIR**.
