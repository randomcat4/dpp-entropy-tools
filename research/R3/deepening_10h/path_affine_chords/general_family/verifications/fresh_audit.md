# D10-B2V fresh audit: general fixed-beta path-affine family

STATUS: CORRECT

This is a non-author verification of
`research/R3/deepening_10h/path_affine_chords/general_family/`.  `CORRECT`
means the arbitrary-`n` fixed-beta construction, the nonempty open convex
domain `Omega_beta`, the SPD/connected/heterogeneous conditions, the
perturbation-rank formula, the rational full-rank corollary, and the scoped
path entropy DP semantics check out.  It does **not** certify any positive R3
entropy gap, any global concavity/non-concavity theorem, or any claim beyond
the stated fixed-beta unit-bidiagonal family.

## Inputs and line evidence checked

I did not use the author status lines as evidence; `theorem.md:3-4`,
`derivation.md:3`, and `verdict.md:3-5` all correctly say these are author
notes, not fresh certificates.

- `theorem.md:8-42` defines `n`, nonzero `beta`, the unit lower-bidiagonal
  matrix `R`, `S(tau)`, `Omega_beta`, `P(tau)`, `L(tau)`, and `K(tau)`.
- `theorem.md:46-89` states the nine claimed conclusions, including SPD,
  `K=I-S`, tridiagonal entries, connectedness, heterogeneity condition,
  openness/convexity/nonemptiness, K-affine chords, and exact rank.
- `theorem.md:93-177` proves those claims by invertibility of `R`, linearity of
  `S`, inverse Loewner order, `Phi(L)=I-S`, direct tridiagonal multiplication,
  convexity, and invertible rank preservation.
- `theorem.md:179-260` gives the arbitrary-dimensional rational full-rank
  template with `beta_i=1/2`, `u_i=i+1`, `v_i=2i+1`, row-sum scaling, full-rank
  difference, connectedness, and diagonal heterogeneity.
- `theorem.md:262-271` records rational exactness and the intended exact
  certificate interfaces.
- `theorem.md:273-289` correctly limits the relation to the rank-one blocker:
  one-coordinate tau directions are rank-one K directions; multi-coordinate
  chords are the meaningful remaining search space.
- `derivation.md:7-40` explains the `S=(I+L)^-1` change of variables and why
  fixed `R` makes K-affine chords.
- `derivation.md:44-70` gives the rank-one coordinate directions and the
  support-size rank formula.
- `derivation.md:83-170` uses exact-event Möbius semantics and derives
  atom/entropy first and second derivatives.
- `derivation.md:189-291` gives the `O(n^2)` value/jet DP interface and clearly
  says the jet interface is a next implementation target, not the current
  `search.py` implementation.
- `derivation.md:293-314` and `search_results.json:2-23` record finite search
  evidence only: seed `20260908`, `n=5..30`, `160` trials per dimension,
  no positive scout above `1e-10`, best delta
  `-1.8402479120993576e-05`.
- `search.py:30-51` implements the displayed `L` diagonal/edge formulas for
  float and Fraction.
- `search.py:54-71` checks tridiagonal SPD by float LDL pivots before finite
  entropy evaluation.
- `search.py:74-116` implements the path-run entropy DP value recurrence.
- `search.py:101-112` uses `prefix_len = 0 if start == 0 else start - 1`,
  matching the empty-prefix / forced-gap convention.
- `search.py:198-205` computes
  `Delta=(H_minus+H_plus)/2-H_zero`, the correct R3 sign convention.
- `search.py:236-282` separates rank-one, rank-two, and full-rank displacement
  buckets and records feasible/positive denominators.
- `search.py:296-315` runs an exact-DP reuse smoke with direct Möbius comparison
  through the existing path Schur validator.
- `search.py:318-344` records status, seed, range, trials, sign convention,
  finite-search-only flag, exact smoke, positive scouts, best case, and per-`n`
  results.
- `research/R3/next_structures/sparse_schur/path_schur.py:148-181` computes
  interval determinants and selected-run weights.
- `research/R3/next_structures/sparse_schur/path_schur.py:184-231` implements
  `H=log Z-T/Z` with `state_count=n(n+1)/2`.
- `research/R3/next_structures/sparse_schur/path_schur.py:234-288` implements
  direct Möbius exact atoms and compares them to L-ensemble/path weights for
  `n<=8`.

## Mathematical verification

For `tau_i>0`, `D_tau=diag(tau_i)` is positive definite.  The unit triangular
`R` is invertible for every real `beta`, so

```text
S(tau)=R^-1 D_tau R^-T
```

is symmetric positive definite.  The dependence on `tau` is linear:

```text
S(tau)=sum_i tau_i u_i u_i^T,
```

where `u_i` is column `i` of `R^-1`.  Therefore

```text
Omega_beta = {tau>0 : S(tau) < I}
```

is an open convex subset of `R^n`, hence also of the positive orthant.  It is
nonempty because `S(epsilon*1)=epsilon R^-1 R^-T < I` for sufficiently small
positive `epsilon`.

For `tau in Omega_beta`, `0<S<I`, hence `P=S^-1>I` by Loewner order reversal
and `L=P-I>0`.  Since `I+L=P`,

```text
Phi(L)=L(I+L)^-1=(P-I)P^-1=I-S.
```

Thus `K(tau)=Phi(L(tau))=I-S(tau)` is a strict real DPP marginal kernel:
`0<K<I`.

The tridiagonal formula is correct.  With `w_i=1/tau_i`,

```text
P=R^T diag(w) R
```

has entries

```text
P_ii = w_i + beta_i^2 w_{i+1}  (i<n),
P_nn = w_n,
P_{i,i+1} = - beta_i w_{i+1}.
```

Subtracting `I` gives the displayed `L` entries.  If every `beta_i != 0`, every
adjacent edge is nonzero, so the path is connected.  The theorem's
heterogeneity statement is conditional, as it should be: if these displayed
diagonal entries are not all equal, then the FT-B diagonal-heterogeneous
condition holds.

For `tau^t=(1-t)tau^-+t tau^+`, convexity gives `tau^t in Omega_beta`, and
linearity gives

```text
K(tau^t)=I-S(tau^t)=(1-t)K(tau^-)+tK(tau^+).
```

The rank formula is exact:

```text
K(tau^+) - K(tau^-)
= -R^-1 diag(tau^+-tau^-) R^-T.
```

Invertible left/right multiplication preserves rank, and the rank of a
diagonal matrix is exactly its number of nonzero diagonal entries.  Therefore
the perturbation rank is the support size of `tau^+-tau^-`; generic chords are
full rank, and one-coordinate chords are rank one.

The rational full-rank corollary is also correct.  For the template
`beta_i=1/2`, `u_i=i+1`, `v_i=2i+1`, all data are rational.  Choosing rational
`epsilon` small enough by the absolute row-sum bound puts
`epsilon*u`, `epsilon*v`, and their midpoint in `Omega_beta`.  Since
`v_i-u_i=i`, every coordinate changes and the rank is `n`.  The first/last
diagonal comparisons in `theorem.md:229-258` prove heterogeneity for all
`n>=2`, and scaling by `1/epsilon` plus subtracting `1` preserves inequality.

## O(n^2) entropy DP semantics

For a path tridiagonal `L`, every selected set decomposes uniquely into
contiguous runs.  The determinant of `L_S` factors as the product of interval
continuants over those runs.  The value DP enumerates whether the last vertex
is absent (`Z_{m-1}`, `T_{m-1}`) or belongs to a final selected run `[a,m]`
preceded by an absent separator.  Therefore the prefix length is `a-2` in
1-based notation, implemented as

```text
prefix_len = 0 if start == 0 else start - 1
```

in 0-based code.  The recurrence

```text
Z_m = Z_{m-1} + sum_a Z_{a-2} kappa(a,m)
T_m = T_{m-1} + sum_a kappa(a,m) T_{a-2}
      + sum_a Z_{a-2} kappa(a,m) log kappa(a,m)
H = log Z - T/Z
```

is semantically correct for L-ensemble exact-event entropy.  The implementation
stores all `n(n+1)/2` interval determinants, so arithmetic count and prototype
memory are both `O(n^2)`.  Direct Möbius comparison remains exponential and is
properly limited to small `n`.

The second-order jet DP in `derivation.md:189-291` is a valid formula-level
extension of the same recurrences, but it is not implemented in current
`search.py`; this is correctly presented as future work and is not needed for
the arbitrary-`n` closure theorem.

## Fresh independent n=6 rational check

I added
`research/R3/deepening_10h/path_affine_chords/general_family/verifications/fresh_general_family_check.py`.
It does not import or call `general_family/search.py`.  It implements Fraction
matrix arithmetic, the theorem's rational `n=6` template, exact rank reduction,
exact Möbius atoms, L-ensemble run weights, and an independent path entropy DP.

Key script locations:

- Fraction determinant/rank primitives: `fresh_general_family_check.py:69-122`.
- `R`, `R^-1`, `S`, `P`, and `L` construction:
  `fresh_general_family_check.py:128-169`.
- Continuants, selected-run weights, Möbius atoms, and DP entropy:
  `fresh_general_family_check.py:182-293`.
- Point checks for SPD, connectedness, heterogeneity, exact atoms, and DP:
  `fresh_general_family_check.py:311-349`.
- Exact support-rank checks and n=6 rational template:
  `fresh_general_family_check.py:351-425`.

Command:

```text
python.exe research/R3/deepening_10h/path_affine_chords/general_family/verifications/fresh_general_family_check.py
```

Exit code: `0`.

Result denominator and highlights:

- `status=PASS`, `n=6`, `beta_i=1/2`.
- Unscaled row-bound maximum: `14969/512`.
- Chosen rational scaling: `epsilon=256/14969`, so
  `epsilon * row_bound = 1/2 < 1`.
- `K_midpoint_exact=true`.
- Rank support checks: support sizes `1`, `2`, `6` have exact ranks `1`, `2`,
  `6`.
- For each of `tau^-`, `tau^0`, `tau^+`:
  - `S` row-sum bound `<1`, hence strict `S<I`;
  - `S * P = I`, `L=P-I`, and `K=I-S=L*S` exactly;
  - `L` is tridiagonal, connected, heterogeneous, and SPD by exact leading
    continuants;
  - `K` leading principal minors are positive;
  - `64` exact atoms checked by Möbius;
  - Möbius atom sum and L-ensemble atom sum are both exactly `1`;
  - atom mismatch count is `0`;
  - DP state count is `21=n(n+1)/2`;
  - DP entropy and direct exact-atom entropy agree within `1e-80` Decimal
    precision (`1.4e-88`, `2e-89`, `9e-89` absolute differences for
    `tau^-`, `tau^0`, `tau^+`).

This independently verifies an arbitrary-dimensional corollary instance beyond
the original n=3/n=4 explicit FT-B examples, with direct exact-event semantics.

## Author search smoke and existing finite evidence

I also ran a small main-path smoke of the author search code with a new seed,
writing output only under this verification directory:

```text
python.exe research/R3/deepening_10h/path_affine_chords/general_family/search.py --n-min 6 --n-max 6 --trials 11 --seed 2026090832 --out research/R3/deepening_10h/path_affine_chords/general_family/verifications/author_search_n6_seed2026090832.json
```

Exit code: `0`.

`author_search_n6_seed2026090832.json:2-18` reports `SCOUT_COMPLETE`, seed
`2026090832`, `n=6`, `11` trials, correct gap sign convention,
finite-search-only flag, n=5 direct-Möbius smoke with `32` events and mismatch
count `0`.  The run had no positive scouts above `1e-10`; its best finite
delta was still negative, `-0.00011749452660936299`
(`author_search_n6_seed2026090832.json:18-29`).

The existing `search_results.json` was not rerun in full.  I parsed its summary:
it covers `n=5..30`, `160` trials per dimension, three buckets per dimension,
and reports no positive scout above `1e-10`.  For `n=6`, `n=9`, and `n=30`,
each of rank-one/rank-two/full-rank buckets records `160` feasible chords and
`0` positives.

## Boundary notes

No critical gap was found.  The following scope limits must remain attached:

1. The arbitrary-`n` theorem is a closure/existence theorem for this fixed-beta
   innovation family.  It does not assert entropy concavity or non-concavity.
2. Finite search misses, including `search_results.json`, are evidence only and
   cannot be promoted to a theorem.
3. The current `search.py` uses the value DP for finite chord entropy.  The
   `O(n^2)` second-order jet DP is only derived, not implemented.
4. Direct Möbius exact-event validation is exponential and should remain a
   small-`n` semantic gate.  Any future positive gap must receive separate
   strict feasibility and outward-rounded entropy/gap certification.
5. The family is not all real symmetric DPP kernels and not all tridiagonal
   SPD `L`; it is the unit lower-bidiagonal fixed-beta innovation subfamily.

Within those limits, the D10-B2V result is `STATUS: CORRECT`.
