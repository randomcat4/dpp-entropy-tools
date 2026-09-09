# Independent reconstruction audit of I05-W4-20260909

Review date: 2026-09-09.

Frozen source archive SHA-256:

```text
b408d1e8faa8bd99e2df33e03dc00548ff42c4e22ef3e814838049820000c308
```

Base integration branch at the start of review:

```text
research/N3-successor-20260909
e988aa3003484f6368133b8bc0c668331629e369
```

## Verdict

**CORRECT within the frozen subdomain scope** for T1--T3 in
`submission/frozen_statement.md`.

The review accepts the claimed all-direction bound

```text
-H''(K;D) >= (7/10)(S+U+V)
```

for every real symmetric three-by-three `K` satisfying

```text
0 < K_ii < 1,
|K_ij| <= (1/4) sqrt(v_i v_j),  v_i=K_ii(1-K_ii),
```

and every real symmetric direction `D`.  It also accepts the convex-domain
chord conclusion, its continuous extension to the stated closure, and strict
negative definiteness of the entropy Hessian when the nonzero-edge graph is
connected.

The global real three-dimensional theorem is still **not proved**, and no DPP
entropy counterexample is supplied.  Novelty is **not reviewed**.  This is a
fresh reconstruction audit with code independent of the submitted scripts; it
is not external human peer review and not proof-assistant formalization.

## 1. Frozen object and reproducibility

The submission manifest was checked before reading the proof.  Every listed
file matched.  The two submitted programs were rerun from the extracted
archive:

```text
python code/verify_exact.py
python code/replay_explorations.py
```

Their outputs were byte-identical to `submission/outputs/verify_exact.txt` and
`submission/outputs/explorations.json`, respectively.  The exact verifier ended
with `ALL EXACT CHECKS PASSED`.

I then wrote `independent_verify.py` without importing submission code.  It
constructs principal-minor polynomials of `K+tD`, obtains all eight exact-event
probabilities by Mobius inversion, differentiates those polynomials, and forms
`-H''` directly.  Its symbolic stage verifies, state by state, the density,
first derivative, and second derivative formulas used by the proof.

## 2. Domain validity and the density bounds

Write `K_ij=e_ij sqrt(v_i v_j)`, with `|e_ij|<=epsilon=1/4`.  Scaling a quadratic
form by `g_i=sqrt(x_i)f_i` gives

```text
f^T K f >= sum_i g_i^2 - 2 epsilon sum_{i<j}|g_i g_j|
          >= (1-2 epsilon) sum_i g_i^2 > 0.
```

Each vertex occurs in two edges.  Repeating the argument for `I-K`, after
scaling by `sqrt(1-x_i)`, proves `0<K<I` from the displayed hypotheses alone.
No spectral-margin assumption has been inserted.

Relative to the product Bernoulli law with means `x_i`, the exact density is

```text
R = 1 - e12^2 s1 s2 - e13^2 s1 s3 - e23^2 s2 s3
      + 2 e12 e13 e23 s1 s2 s3.
```

Because `|s_i|<=1`, the proof's uniform bounds are correct:

```text
25/32 <= R <= 39/32.
```

The independent symbolic reconstruction verified this identity for all eight
states directly from determinant inclusion probabilities.

## 3. Full Fisher term, including the three-point component

At a fixed center, the independent calculation gives

```text
g = p'/P0
  = sum_i t_i Y_i - 2 sum_{i<j} u_ij Y_iY_j
    + (2C-lambda.t)Y1Y2Y3.
```

The product-Walsh monomials are orthonormal.  Since `R<=M=39/32`, retaining the
entire score yields

```text
F >= M^{-1}[S+4U+(2C-lambda.t)^2].
```

For distinct edge labels `e,f`, with third edge `g`, direct substitution gives

```text
|w_e w_f| = |u_e u_f| e_g^2 sqrt(v_r v_s)
            <= (epsilon^2/4)|u_e u_f|.
```

Thus `C^2 >= V-(epsilon^2/2)U`.  Also each
`lambda_i<=epsilon^2/4`, hence `||lambda||^2<=3epsilon^4/16`.
Using `(2C-L)^2 >= 2C^2-L^2` gives exactly the frozen Fisher bound

```text
F >= M^{-1}[(1-3epsilon^4/16)S+(4-epsilon^2)U+2V].
```

This check is material: the `V` term is the component that controls a missing
edge when the other two center edges are nonzero.

## 4. Real Rayleigh square and logarithmic interactions

For fixed `s_k`, the four conditional density values obey the exact identity

```text
R10 R01 - R00 R11 = (e_ij-e_ik e_jk s_k)^2.
```

The review verified the polynomial identity at the actual Bernoulli endpoints,
without division by an edge.  Together with `R>=m=25/32`, it gives

```text
0 <= -bar(theta_ij)
   <= [e_ij^2+e_ik^2 e_jk^2 v_k]/m^2.
```

The triple finite difference `Lambda` is the integral of
`partial_123 log R` over a box of side length one.  Re-expanding its three
terms confirms the submitted coefficient bounds:

```text
C_P = 81408/15625 < 6,
C_Q = 63488/15625 < 5,
|Lambda| <= 6P+5Q.
```

No differentiation under an improper integral or boundary probability limit
is involved.

## 5. Exact acceleration and the delicate two-edge estimate

Direct second differentiation of the eight event polynomials confirms

```text
p''/P0 = 2 sum_{i<j}(d_i d_j-h_ij^2)s_i s_j/(v_i v_j)
         + 4W s1s2s3/(v1v2v3),
```

and consequently

```text
A = sum p'' log p
  = 2 sum bar(theta_ij)(d_i d_j-h_ij^2)+4 Lambda W.
```

The diagonal-coupling loss is correctly bounded by `(65/1250)S`.

The proof's tersest point is its equation (21).  Here is the explicit check.
For an unordered pair of edge directions `e,f`, let `g` be the third edge and
let

```text
T_ef = V0 |e_g r_e r_f|.
```

Then

```text
P T_ef <= (epsilon^2/4)|u_eu_f|.
```

Writing `A_h=e_h^2`, the three summands of
`Q=A_eA_f+A_eA_g+A_fA_g` satisfy

```text
A_eA_f T_ef <= (epsilon^2/4)(|u_e w_f|+|u_f w_e|),
A_eA_g T_ef <= (epsilon^2/2)|u_e w_f|,
A_fA_g T_ef <= (epsilon^2/2)|u_f w_e|.
```

The omitted variance square root in each conversion is at most `1/2`.  Hence

```text
Q T_ef <= (3epsilon^2/4)(|u_e w_f|+|u_f w_e|).
```

After summing over pairs, the off-diagonal all-ones matrix has operator norm
`2`, so

```text
sum_{e != f}|u_e w_f| <= 2 sqrt(UV) <= U+V.
```

This yields exactly

```text
P T_* <= (epsilon^2/4)U,
Q T_* <= (3epsilon^2/4)(U+V),
```

and therefore the submitted edge-edge loss
`21epsilon^2 U+15epsilon^2 V`.  The mixed edge-diagonal loss
`(39/1024)(S+U)` also follows from `sqrt(v1v2v3)<=1/8` and Cauchy--Schwarz.

## 6. Final constants

Recomputing with exact rational arithmetic gives

```text
c_S = 3643291/4992000,
c_U = 25029/13312,
c_V = 439/624.
```

Their excesses over `7/10` are

```text
148891/4992000,
78553/66560,
11/3120,
```

all positive.  Thus T1 follows with the stated constant and all six real
symmetric coordinates present.

## 7. Convexity, closure, and strictness

The geometric mean is concave and coordinatewise increasing on the nonnegative
quadrant, while `x(1-x)` is concave.  Therefore

```text
(x,y) -> sqrt(x(1-x)y(1-y))
```

is concave.  Each two-sided edge constraint is convex, so the domain is convex.
Integrating the pointwise Hessian inequality along a segment proves the chord
inequality in the open-diagonal domain.

For closure points, `(1-delta)K+delta I/2` lies in the same convex domain with
strict diagonal coordinates.  Event probabilities are polynomials in `K`, and
`-p log p` is continuous at zero.  Passing `delta` down to zero proves the
closure statement without asserting a finite boundary Hessian.

If the nonzero-edge graph is connected, every nonzero diagonal direction is
seen by `S`; every direction on a present edge is seen by `U`; and the sole
missing edge, when there are exactly two present edges, is seen by `V`.  Hence
`S+U+V` is positive definite and T3 follows.  The submitted descriptions of
the one-edge and zero-edge null directions are consistent with block-product
factorization of the center law.

## 8. Independent all-direction stress test

The fixed-seed run checked 36 deterministic and 3,000 random centers.  At each
center it constructed the complete six-by-six curvature matrix by polarization
of direct eight-event directional curvatures; it did not sample directions.
It then tested the minimum eigenvalue of

```text
Q(K) - 0.7 diag(weights(S+U+V)).
```

There were 159 automatic 90-decimal-digit fallbacks for ill-conditioned
Mobius cancellation.  Four additional 110-digit probes used diagonal distances
as small as `1e-30`.  No violation remained.  The smallest negative residue was
about `2.6e-82` on an exact null direction, below the 90-digit eigensolver's
zero tolerance.

An initial float-only run produced a large apparent failure at

```text
x=(0.9997675225046964, 0.9999514128199806, 0.9983286741372697),
e=(0.0035340391227428047, 0, 0.173080689635704).
```

The rare `000` event suffered about `8e-6` relative cancellation error under
ordinary determinant inclusion-exclusion.  Recomputing the same direct
principal-minor construction at 100 digits changed the suspect normalized gap
from `-3.6865...` to `0.2999999901...`; the candidate was purely numerical.
This failed run is retained in `RUN_LOG.md` rather than silently discarded.

For the displayed noncommuting example, the independent direct evaluator gives

```text
[K,D]_12 = -23/80,
-H''(K;D) = 9.509075601194377,
(7/10)(S+U+V) = 6.554468364197529.
```

These numbers are diagnostics, not the proof.

## 9. Limits of this review

This review does not establish the theorem outside the normalized interaction
domain, does not settle the general real three-dimensional problem, and does
not validate any more-point or stationary entropy-rate claim.  It did not
perform an exhaustive literature search, so it does not certify novelty.  It
did not translate the proof into Lean, Coq, Isabelle, or another proof
assistant.  The analytic verdict rests on the line-by-line elementary audit
above, with symbolic reconstruction used to guard coordinate and sign factors.
