# D10-S3 PSD mechanism scout report

Status: **SCOUT_NO_HIT_PLUS_PROVED_DIAGONAL_SUBCLASS**.

General PSD/NSD \(K\)-affine entropy concavity remains **INCOMPLETE**.
No \(\rho>1\) or \(H''>0\) candidate was found or frozen in this work unit.

## Inputs treated as prior evidence, not theorem

- Existing D10-S derivation records the exact-event identity
  \(p_K(S)=(-1)^{n-|S|}\det(K-Q_S)\) and the directional Hessian split
  \(H''=-\sum_Sp_Sv_S^2-\sum_Sp_Sw_S\log p_S\)
  (`../derivation.md`, lines 8-29).
- The same file gives a genuine warning sign: two PSD rank-one directions can
  have positive mixed Hessian, so rank-one concavity cannot be naively summed
  (`../derivation.md`, lines 45-64).
- The dense Hessian round6 analysis reports a stable mechanism ratio
  \(\rho\approx0.5261099452386903\), still below the positive-curvature
  threshold \(\rho>1\) (`../../dense_hessian/server_round6_analysis/analysis.md`,
  lines 9-21).
- Its suggested next structure is fixed observation kernel with fixed
  eigenvectors and heterogeneous positive spectral rates, while warning not to
  replace full configuration entropy by spectral Bernoulli entropy
  (`../../dense_hessian/server_round6_analysis/analysis.md`, lines 124-147).

## Independent implementation

Script:

`psd_mechanism_search.py`

The script is self-contained and does not import the author's Hessian code.  It
uses the signed determinant exact-event formula, independently compares it
against inclusion-probability Möbius inversion on the fixed \(n=12\) center,
builds the exact-event quadratic Fisher and acceleration forms, and then tests
PSD directions through:

1. the frozen positive definite dense direction;
2. the full symmetric generalized control at the frozen center;
3. the \(K\)-commuting positive spectral-rate subspace;
4. the original-coordinate diagonal subspace;
5. identity direction;
6. random PSD rank/factor directions;
7. log-spectrum SPD directions;
8. a local PSD factor walk around the frozen direction;
9. small \(n=2,3,4,5\) random PSD scouts.

Because the full symmetric generalized maximum at the fixed \(n=12\) center is
already below 1 and its maximizing direction is positive definite, this fixed
center shows no numerically visible hidden PSD flip in the recomputed
double-precision quadratic control.  The subsequent PSD-only draws are therefore
diagnostic for nearby mechanisms, not a proof over all centers.

## Run record

Command run from
`C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo`:

```text
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
research/R3/deepening_10h/semidefinite_directions/psd_mechanism_search/psd_mechanism_search.py
```

Exit code: `0`.  Runtime recorded by the script: `2.7080140113830566` seconds.
NumPy version: `2.3.5`.  Seed: `2026090833`.  No GPU or server was used, and no
new external dependency was installed; the script uses NumPy.

Output:

`scout_results.json`

## Main numerical findings

For the frozen \(n=12\) dense mechanism center:

| Direction family | Best \(\rho\) | \(H''\) sign | PSD status |
|---|---:|---:|---|
| full symmetric generalized control | 0.5261099452386891 | negative | maximizing direction PSD, rank 12 |
| frozen dense direction | 0.5261099452386899 | negative | PSD, rank 12 |
| \(K\)-commuting spectral-rate subspace | 0.5133580085580258 | negative | PSD after sign choice, rank 12 |
| original-coordinate diagonal subspace | 0.45712469833003244 | negative | PSD after sign choice, rank 12 |
| identity direction | 0.4344106019978416 | negative | PSD, rank 12 |

The best fixed-center PSD scout was the full generalized direction, with

\[
F_+=1.0000000000000002,\quad
A=0.5261099452386903,\quad
H''=-0.47389005476130996.
\]

The strict feasible chord gate at step \(h=10^{-4}\) gave endpoint margins
`0.0001579592541962568` and `0.0001611704993774521`, and midpoint gap
`-2.3694486372960455e-09`.  The central second difference was
`-0.4738897274592091`.

Exact-event checks at this center:

- all `4096` signed determinant atoms were positive;
- minimum atom was `3.488201486707941e-14`;
- signed determinant sum residual was `0.0`;
- signed determinant versus direct Möbius maximum absolute difference was
  `5.656142040774439e-16`.

PSD-only draw counts at the fixed center:

- deterministic controls: `11`;
- commuting log-uniform positive-rate draws: `6000`;
- random PSD rank/factor draws: `9000`;
- random SPD log-spectrum draws: `5000`;
- local PSD factor walk proposals: `2500`, accepted `2111`.

No fixed-center batch improved over \(\rho=0.52610994523869\).

Small-\(n\) random PSD scout:

| n | centers | PSD directions | event distributions built | event atoms per build | max observed \(\rho\) | positive candidates |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 500 | 10000 | 500 | 4 | 0.2417516532772835 | 0 |
| 3 | 260 | 3120 | 260 | 8 | 0.27074759435535223 | 0 |
| 4 | 120 | 960 | 120 | 16 | 0.25329812105632843 | 0 |
| 5 | 60 | 360 | 60 | 32 | 0.21648316267023057 | 0 |

These finite misses are scouts only.  They are not evidence for a universal
theorem beyond the sampled parameterizations.

## Proved exclusion zone

The file `diagonal_subclass_exclusion.md` proves a narrow but exact PSD/NSD
subclass:

if \(K(t)=\operatorname{diag}(k_i+td_i)\) remains strict, then exact atoms are
the product Bernoulli atoms obtained from Möbius inversion, and

\[
H''(K(t))=-\sum_i\frac{d_i^2}{(k_i+td_i)(1-k_i-td_i)}\le0,
\]

strict unless \(D=0\).  This covers arbitrary-rank diagonal PSD or NSD
directions in the original observation basis, including heterogeneous rates.

Scope warning: this does **not** cover arbitrary commuting \(K,D\) after a
rotation, because DPP configuration entropy is basis-sensitive.

## Verdict

No robust positive semidefinite mechanism candidate was found.  The known
stable \(n=12\) mechanism remains below the true positive-curvature gate, and
the independent fixed-center full symmetric control found no hidden PSD
direction at that specific center.  This fixed-center statement is a numerical
scout/control, not an interval theorem.

The only closed result from this work unit is the diagonal coordinate-product
PSD/NSD exclusion.  The general PSD/NSD direction problem remains open.
