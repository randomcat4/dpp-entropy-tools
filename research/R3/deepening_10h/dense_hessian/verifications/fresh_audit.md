# D10-HV fresh audit: dense Hessian scout

STATUS: CORRECT

This is a non-author verification of `research/R3/deepening_10h/dense_hessian/`.
`CORRECT` here means the frozen dense-Hessian probe formulas, coordinate
implementation, and scoped float64 smoke/evidence checks are internally correct
for exact-event DPP Shannon entropy.  It does **not** certify a real
counterexample, a positive-curvature candidate, or global concavity/non-concavity.

## Files and line evidence checked

- `README.md:3-13` states that the route computes full-configuration Shannon
  Hessian over real symmetric coordinates using
  `p_S=(-1)^|S^c| det(K-I_{S^c})` and
  `H''=-sum_S [(p'_S)^2/p_S+p''_S log p_S]`.
- `README.md:21-22` correctly labels all results as float64 scouting and says
  finite non-hits are not a theorem.
- `derivation.md:6-24` gives the signed exact-event determinant, the logdet
  derivatives, and the entropy Hessian split.
- `dense_hessian.py:24-30` builds the full symmetric upper-triangle coordinate
  basis; off-diagonal coordinates simultaneously change `K_ij` and `K_ji`.
- `dense_hessian.py:33-54` constructs signed event matrices and checks determinant
  sign plus probability normalization.
- `dense_hessian.py:72-83` implements `score`, mixed logdet Hessian, Fisher term,
  and event-acceleration term.  The index contractions match the formulas below.
- `dense_hessian.py:85-97` symmetrizes the Hessian blocks and records entropy,
  minimum atom, normalization residual, and component spectra.
- `dense_hessian.py:142-152` chooses a symmetric feasible chord step by checking
  both `K±tD` margins.
- `dense_hessian.py:171-182` implements a direct Möbius atom oracle.
- `dense_hessian.py:185-212` self-tests the event determinant against Möbius and
  checks one finite-difference Hessian quadratic form.
- `dense_hessian.py:215-349` logs seed/range/chunk/threads, result rows, best
  finite scout case, mechanism case, and the float64 warning.
- Existing `results_round3/manifest.json:12-17` reports 300 completed scout
  points, best lambda `-4.63636388825741e-05`, best gap
  `-0.00046365004082549177`, exit code `0`, and the float64/non-theorem warning.
- Existing `results_round3/best_case.json:7-20` records min atom
  `0.023820007177552175`, normalization residual `0.0`, negative best curvature
  and gap, and endpoint margin `0.22574298757680167`.

## Independent derivation from exact-event definitions

Let `q_U(K)=det K_U`, with `q_empty=1`.  For exact event `S`,

```text
p_S(K) = sum_{U superset S} (-1)^(|U|-|S|) q_U(K).
```

This is the inclusion/Möbius definition of exact atoms, not a principal-minor
substitution.  For strict `0<K<I`, all principal `K_U` are positive definite,
and all exact atoms are positive, e.g. from the L-ensemble representation
`L=K(I-K)^-1`.

For an affine line `K(t)=K+tD`, and nonempty `U`,

```text
q'_U = q_U tr(K_U^-1 D_U),
q''_U = q_U [(tr(K_U^-1 D_U))^2 - tr((K_U^-1 D_U)^2)].
```

The exact-event derivatives are obtained by the same Möbius aggregation:

```text
p'_S  = sum_{U superset S} (-1)^(|U|-|S|) q'_U,
p''_S = sum_{U superset S} (-1)^(|U|-|S|) q''_U.
```

Since `sum_S p_S=1`, `sum_S p'_S=sum_S p''_S=0`.  Differentiating
`H=-sum_S p_S log p_S` gives

```text
H''[D,D] = -sum_S (p'_S)^2/p_S - sum_S p''_S log p_S.
```

The author's signed event matrix formula
`p_S=(-1)^|S^c| det(K-I_{S^c})` is equivalent to the Möbius formula.  The logdet
derivative in `derivation.md:10-20` is therefore legitimate on the strict
interior; strict positivity of exact atoms keeps these event matrices nonsingular.

## Implementation audit

The key einsum contractions are correct:

- `score = einsum("qij,pji->qp", inverse, basis)` at `dense_hessian.py:75`
  computes `tr(A_S^-1 E_p)`.
- `products = einsum("qij,pjk->qpik", inverse, basis)` and
  `hlog = -einsum("qpij,qrji->qpr", products, products)` at
  `dense_hessian.py:76-77` compute
  `-tr(A_S^-1 E_p A_S^-1 E_r)`.
- `dense_hessian.py:81-83` then forms
  `-sum p score_p score_r - sum p log(p)(score_p score_r+hlog_pr)`, i.e.
  the Fisher plus event-acceleration decomposition above.

The symmetric coordinate basis is intentionally full but not Frobenius
orthonormal: diagonal basis vectors have Frobenius norm `1`, off-diagonal basis
vectors have Frobenius norm `sqrt(2)`.  This does not invalidate sign detection:
the coordinate map from upper-triangle coordinates to real symmetric directions
is invertible, so a positive coordinate quadratic form is a real positive
direction and a negative semidefinite coordinate Hessian is negative semidefinite
as a bilinear form.  It does mean raw coordinate eigenvalue magnitudes should not
be quoted as Frobenius-normalized curvature without an additional Gram-matrix
normalization.

The main run path uses a spectral-norm normalization for the reported chord
direction (`dense_hessian.py:257-262`) and checks endpoint feasibility by
eigenvalue margins (`dense_hessian.py:285-315`).  This is adequate for scouting
finite chord gaps.  The reported `lambda_max_coordinate` is the coordinate
matrix eigenvalue; the reported `lambda_max` is the same eigendirection rescaled
before evaluating the quadratic form, so its sign is meaningful but its magnitude
is a convention-dependent scout statistic.

## Commands run and denominators

All commands were run from
`C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo` with BLAS/thread
environment variables set to `1`.

| Check | Command | Exit | Denominator / result |
|---|---|---:|---|
| Runtime | `python.exe --version` | 0 | Python `3.12.14` |
| NumPy | `python.exe -c "import numpy as np; print(np.__version__)"` | 0 | NumPy `2.3.5` |
| Author self-test | `python.exe research/R3/deepening_10h/dense_hessian/dense_hessian.py --self-test` | 0 | `n=4`, `16` events, `10` symmetric coordinates; event/Möbius max error `5.551115123125783e-17`; Hessian finite-difference error `1.3036745372119185e-07` |
| Author main-path smoke | `python.exe research/R3/deepening_10h/dense_hessian/dense_hessian.py --out research/R3/deepening_10h/dense_hessian/verifications/author_smoke_seed2026090830 --seed 2026090830 --n-min 3 --n-max 3 --trials-per-n 1 --chunk 16` | 0 | `1` kernel, `n=3`, `8` events; manifest lines `12-18` show completed `1`, best lambda `-1.3247381140765029`, best gap `-0.0010589846971424954`, exit code `0`, float64 warning |
| Fresh independent script | `python.exe research/R3/deepening_10h/dense_hessian/verifications/fresh_hessian_check.py` | 0 | Möbius/inclusion determinant implementation; tested `n=3` and `n=5` basepoints |

## Fresh independent check results

The independent script is
`research/R3/deepening_10h/dense_hessian/verifications/fresh_hessian_check.py`.
It computes derivatives from inclusion determinants and Möbius aggregation
(`fresh_hessian_check.py:67-112`), separately checks the signed event determinant
identity (`fresh_hessian_check.py:115-125` and
`fresh_hessian_check.py:148`), computes the entropy Hessian
(`fresh_hessian_check.py:135-150`), and performs finite differences plus
author-Hessian comparison (`fresh_hessian_check.py:187-239`).

| Case | Events / coords | Min atom | Normalization / derivative residuals | Author-H max abs delta | Eigenvalue sign | Finite-difference check |
|---|---:|---:|---:|---:|---|---|
| `n=3`, seed `2026090821` | `8` / `6` | `0.04627958416296278` | norm `0.0`; first `2.7755575615628914e-17`; second `0.0`; event-det error `8.326672684688674e-17` | `5.329070518200751e-15` | max `-1.9634453564916377`, min `-6.046121061418368`, positive count `0` | top-direction best abs error `4.976950718216244e-08`; random-direction best abs error `1.5141330855783508e-08` |
| `n=5`, seed `2026090822` | `32` / `15` | `0.00628771911026127` | norm `0.0`; first `1.3877787807814457e-16`; second `3.608224830031759e-16`; event-det error `7.979727989493313e-17` | `4.773959005888173e-15` | max `-0.6003393268818716`, min `-7.6095094024066565`, positive count `0` | top-direction best abs error `3.6219004240223285e-07`; random-direction best abs error `4.918931262309911e-08` |

Both fresh basepoints are strict (`K` margins `0.17` and `0.09` respectively),
the finite-difference steps kept endpoint margins positive, and no positive
Hessian eigenvalue was observed in these two independent checks.

## Boundary notes and future positive-candidate gate

No critical gap was found in the dense-Hessian scout as a scoped exploratory
tool.  The following limitations remain and must be preserved:

1. These are float64 finite checks.  Existing non-hits, including 300 points in
   `results_round3`, do not prove global concavity.
2. Coordinate eigenvalue magnitudes are basis-convention dependent because the
   upper-triangle symmetric basis is not Frobenius orthonormal.
3. The direct Möbius oracle is present in `self_test`; the main scout loop uses
   signed event determinants plus sign/normalization checks.  For any future
   positive signal, direct Möbius/inclusion aggregation should be run on the
   frozen candidate before certification.
4. Any future positive candidate must be frozen with explicit `K,D`, seed,
   denominator/rounding data, and a rigorous gate:
   - prove `0<K<I` and `0<K±alpha D<I` with spectral/Sylvester margin;
   - compute exact atoms by Möbius inclusion-exclusion, not by principal minors;
   - interval-bound atom positivity, normalization, `p'`, `p''`, and
     `H''` or finite chord gap;
   - report the coordinate basis and any norm normalization used;
   - only then state a certified positive lower bound.

Within that scope, the D10-HV verification result is `STATUS: CORRECT`.
