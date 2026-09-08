# D10-S3 verdict

STATUS: **INCOMPLETE_FOR_GENERAL_PSD**

Secondary status: **PROVED_DIAGONAL_SUBCLASS_EXCLUSION**.

No \(\rho>1\) or \(H''>0\) PSD/NSD \(K\)-affine direction was found.  No positive
candidate is frozen by this work unit.

What is rigorous:

- A narrow analytic exclusion for standard-coordinate diagonal kernels and
  diagonal PSD/NSD directions is proved in `diagonal_subclass_exclusion.md`.

What is numerically checked:

- The frozen \(n=12\) dense mechanism center was independently recomputed from
  exact-event signed determinants and compared against Möbius inversion.  Its
  full symmetric generalized maximum is \(\rho=0.5261099452386891<1\), and the
  maximizing direction is positive definite.  Within this double-precision
  fixed-center control, no hidden PSD positive-curvature direction appears.
- PSD-only scouts at the same center and small random \(n\le5\) scouts found
  zero positive candidates.

What is not certified:

- No universal PSD/NSD concavity theorem is proved.
- No exclusion is proved for arbitrary commuting pairs after an orthogonal
  rotation; observation-coordinate entropy is basis-sensitive.
- Finite scout misses are not promoted to a theorem.

Run command:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research/R3/deepening_10h/semidefinite_directions/psd_mechanism_search/psd_mechanism_search.py
```

Exit code: `0`.  Seed: `2026090833`.  Main output: `scout_results.json`.
