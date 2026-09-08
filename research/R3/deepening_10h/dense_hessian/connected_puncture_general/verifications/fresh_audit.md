# D10-U7 fresh non-author audit

STATUS: CORRECT.

Scope of this status: the frozen D10-U7 analytic proof candidate in
`connected_puncture_general/` correctly proves the fixed-parameter small
punctured-ray theorem:

- for every fixed finite `n>=2`, every strict diagonal
  `X=diag(x_i)`, and every real zero-diagonal symmetric `A` whose support graph
  on `[n]` is connected with all supported weights nonzero, the full
  observation-coordinate Shannon entropy Hessian at `X+epsilon A` is strictly
  negative definite on `Sym(n)` for all sufficiently small nonzero real
  `epsilon`;
- if the support graph is disconnected, there is an exact flat cross-component
  Hessian direction at every strictly feasible point on the block ray, so the
  same full negative-definiteness property fails;
- the graph-distance congruence limit and the displayed shortest-path
  coefficients are correct in the stated fixed-parameter sense.

This audit does not certify novelty, global concavity away from the diagonal
puncture, a threshold uniform in `n`, boundary diagonals, zero support weights,
or any claim at `epsilon=0`.  The independent finite calculations below are
sanity checks only; the status rests on the analytic lemmas.

## Frozen inputs

Audited author files and SHA256 hashes:

| file | SHA256 |
| --- | --- |
| `frozen_claim.md` | `FBCD270F26F2BCCAED3C4641AE4531BF89A7C982C36E124D56F4B1F85C5D2DFE` |
| `proof_candidate.md` | `2952FE94A42D135E8092E1F9347257BD5EBC77270E2F825C86D186FCDD9085A2` |
| `hazards.md` | `3D3331E0B5C4A67B3CC147492F46C9816ADF1B8E2BD16A13E1901814E4ADBD5E` |
| `verdict.md` | `5C6CC9F872C6CE6F423CBB12E4021A5CE961AB2B3594F6EEB0B4141FA3E80B91` |
| `run_log.md` | `FDD7DB6D16D7CE0E43EC15479FB9F9395944464976F8FE581CFCA6089D1B709B` |
| `general_sanity.py` | `46E075F8DC25814BBE5AB5571BC671552ECD740F8FB87BC93644B5837E5E0970` |
| `sanity_results.json` | `C288BC03BF9D63EC17E382D4AE61FC2C2CB851D259718407D2B04D7C637BD16D` |

Only this `verifications/` directory was written.  No author file, shared
index, or prior verification file was modified.

## 1. Exact-event semantics and coefficient filtration

The proof starts from exact atoms, not inclusion minors.  For every subset
`S`,

```text
p_S(K)=sum_{T superset S} (-1)^(|T|-|S|) det K_T
      =(-1)^|S^c| det(K-I_{S^c}).
```

At `K=X+Z`, with `X=diag(x)` strict and `Z` symmetric zero-diagonal, the
diagonal entries in `K-I_{S^c}` are `x_i` for `i in S` and `x_i-1` otherwise.
Factoring them gives

```text
p_S(X+Z)/a_S = det(I+diag(zeta(S))Z)
             = 1 + sum_T det(Z_T) prod_{i in T} zeta_i(S),
```

where `a_S=prod_{i in S}x_i prod_{i notin S}(1-x_i)` and
`zeta_i=1/x_i` or `-1/(1-x_i)`.  This is exactly the shifted-determinant
version of Möbius inversion.

Under the product law `a_S`, the `zeta_i` are independent and centered.
Because zero-diagonal perturbations preserve total mass and every singleton
inclusion marginal, the logarithmic base term `log a_S`, which is affine in
singleton indicators, contributes zero to the entropy offset.  Hence

```text
H(X+Z)-H(X)=E_a[-D_S(Z) log D_S(Z)].
```

For any determinant monomial, every active vertex has graph degree two in the
monomial, while its attached character power is one.  In a product of
determinant monomials contributing edge exponent vector `alpha`, the exponent
of `zeta_i` is therefore exactly `delta_i(alpha)/2`.  Thus a nonzero entropy
coefficient requires every active vertex degree `delta_i` to be even; if
`delta_i=2`, the factor `E zeta_i=0` kills the coefficient.  Consequently every
active vertex in a nonzero entropy monomial has degree at least four, and
`|alpha| >= 2 v(alpha)`.

This argument is coefficientwise and valid on the whole strict diagonal
domain, not at one special `x`; therefore later `x`-differentiations preserve
the stated vanishings.

## 2. Bridge (1): residual-support locality

The cross-block flatness lemma is sound.  If `K` is strictly feasible and
block diagonal over components `C_b`, the exact DPP law factors over the
blocks because inclusion determinants factor and Möbius inversion preserves
the product.  For a direction `D` with only cross-block entries:

- every inclusion determinant has first derivative zero at `K`;
- hence every exact atom has `p'_S=0`;
- the marginal law on each block is unchanged along `K+tD`, so for each block
  event `R`, `sum_{S:S cap C_b=R} p''_S=0`;
- since `log p_S` is a sum of block log atoms, both the Fisher term and the
  acceleration term in `H''` vanish.

Polarization then gives zero bilinear Hessian on the whole cross-block
subspace.  Differentiating the identically zero first derivative in a
cross-block direction along any block-internal direction gives zero
cross/internal Hessian.  Entropy additivity gives zero mixed entries between
internal directions in different blocks.

The residual-support extraction in §3.2 is also valid.  Take a coefficient
`z^beta` of the full-coordinate Hessian entry `H_{ef}` after differentiating
first, then restrict all non-`beta` coordinates to zero.  The base kernel is
block diagonal over the connected components of the residual graph
`F_beta`.  If the endpoints of `e` and `f` are not all in one component, the
restricted Hessian entry is identically zero by the cross-block lemma.  An
analytic function identically zero on that local block-diagonal family has all
Taylor coefficients zero, including the coefficient of `z^beta`.

This step does not require assuming monomialwise non-cancellation in advance:
the identity is imposed on the entire restricted analytic function after the
full-coordinate derivatives have already been taken.  It also supplies the
needed locality for `H_e`: a nonzero residual coefficient in a first derivative
requires the endpoints of `e` to be connected in `F_beta`.

## 3. Bridge (2): graph-distance lower bounds and equality

Let `beta` be a residual monomial in `H_{ef}(X+Z)` that survives after
substituting `Z=epsilon A`, so its support lies in the fixed support graph
`G`.  The source entropy monomial is
`alpha=beta+1_e+1_f`, or `beta+2 1_e` when `e=f`, and has degree `|alpha|=r+2`.

By residual locality, `F_beta` contains a path joining the endpoints of `e`
and a path joining the endpoints of `f`.  Hence the active vertices of
`alpha` include at least `max(d_e,d_f)+1` vertices.  Combining this with
`|alpha|>=2v(alpha)` gives

```text
r >= 2 max(d_e,d_f).
```

If `d_e != d_f`, this is already strictly larger than `d_e+d_f`.  If
`d_e=d_f=d` and a mixed same-scale term with `r<=2d` existed, every inequality
would be equality: `r=2d`, `v(alpha)=d+1`, and all active vertices would have
degree exactly four.

In that equality case, any residual path joining the endpoints of `e` must be
a shortest path of length `d` and must use all active vertices.  No extra edge
of `G` may join nonconsecutive vertices on that path, because such a chord
would shorten the `G`-distance between the endpoints of `e`.  Thus the induced
subgraph on the active vertices is exactly this path.  The endpoints of `f`
must lie among these same vertices and have `G`-distance `d`.  Along a length
`d` path, the only pair of vertices at path distance `d` is the endpoint pair;
all other pairs have a shorter path inside `G`.  Therefore `f=e`.

This checks the fragile cases requested in the task:

- multiple shortest paths do not create same-scale mixed entries.  If two
  shortest paths have different vertex sets, the active vertex count exceeds
  the equality bound; if they had the same vertex set but different edges,
  those extra edges would be chords and would shorten the endpoint distance;
- overlapping paths and shared endpoints for `e != f` still fail the equality
  condition, since the second marked pair would have distance strictly less
  than `d` along the same active path unless it is the same unordered pair;
- non-induced chords are not ignored: their existence changes the true
  distance, so the geodesic used in the leading term is the shorter one.

Therefore every distinct off-diagonal coordinate pair satisfies

```text
H_{ef}(X+epsilon A)=O(|epsilon|^(d_e+d_f+1)).
```

For `e=f`, the first possible residual degree is `2d_e`.  Equality forces the
residual support to be exactly a shortest path `P` from one endpoint of `e` to
the other.  If `d_e>=2`, then `e` is not a support edge, so `alpha_e=2`; the
degree-four condition at an endpoint forces the adjacent path-edge exponent
to be two, and propagation along the path forces every path edge to have
exponent two.  If `d_e=1`, the separate one-edge quartic coefficient applies.

Thus the diagonal leading term is a sum over squared products along distinct
shortest paths.  Edge signs cannot cancel, because every path contribution is
`prod A_a^2`, not a signed path amplitude.

## 4. Bridge (3): doubled-cycle coefficient

For a simple cycle of length `m>=3`, with cycle-edge variables `z_i`,
`q=prod z_i`, and `X_i=z_i^2`, the scalar determinant is

```text
det(I+Z_cycle)=M(X)+2(-1)^(m-1)q,
M(X)=sum_{cycle matchings J} (-1)^|J| prod_{i in J}X_i.
```

The determinant permutation classification is complete: permutations are
either fixed points plus disjoint edge transpositions, or one of the two
oriented full cycles.  This includes `m=3`, where the two oriented triangle
cycles are exactly the two non-matching terms.

For `f(u)=-u log u`, the coefficient of `q^2=prod X_i` in
`f(M+cq)` receives:

- `c^2 f''(1)/2 = -2` from the quadratic oriented-cycle term, since `c^2=4`;
- no contribution from the linear `q f'(M)` term, because `f'(M)` is even in
  each `z_i`;
- no contribution from powers `q^k`, `k>=3`, to the `q^2` monomial.

It remains to compute `[X_1...X_m]f(M)`.  In `M^r` for a positive integer
`r`, selecting the squarefree full product assigns each cycle edge to one of
`r` matching factors.  This is a proper `r`-coloring of the line graph of the
cycle, again a cycle.  Therefore

```text
[X_1...X_m]M^r = (-1)^m ((r-1)^m+(-1)^m(r-1)).
```

The coefficient of a fixed squarefree monomial in `(1+(M-1))^r` is a
polynomial in `r` of degree at most `m`, so equality for all positive integers
extends to the formal polynomial identity.  Differentiating at `r=1` gives
`[X_1...X_m]M log M=1`, hence `[X_1...X_m]f(M)=-1`.  The total scalar
coefficient is `-1-2=-3`.

Restoring exact-event entropy uses the coefficient filtration from §1.  In the
doubled simple cycle every active vertex has degree four, so the scalar
coefficient is multiplied by `prod_v E zeta_v^2 = prod_v w_v`.  Two
derivatives in the marked coordinate then give the Hessian factor `-6`.  For a
support edge (`d=1`), the separate scalar coefficient of `z_e^4` in
`-(1-z_e^2)log(1-z_e^2)` is `-1/2`; its second derivative also gives `-6`.

## 5. Remainders, congruence limit, and feasibility

The entropy offset starts at total off-diagonal degree four throughout the
strict diagonal domain, so

```text
H_xx = -diag(1/[x_i(1-x_i)]) + O(|epsilon|^4).
```

For `H_e`, the same residual-locality argument applied to a first derivative
gives a source monomial `alpha=beta+1_e`.  If a residual coefficient has degree
`r`, the endpoints of `e` must be connected in `F_beta`, so
`r+1>=2(d_e+1)` and `r>=2d_e+1`.  Since these lower coefficients vanish
identically as analytic functions of `x`, differentiating in any diagonal
coordinate preserves the order:

```text
H_{x_i,e}=O(|epsilon|^(2d_e+1)).
```

Together with the mixed off-diagonal bound and the diagonal coefficient
formula,

```text
H_{ee}(X+epsilon A)
 = -6 epsilon^(2d_e)
     sum_{P shortest for e} (prod_{v in P}w_v)(prod_{a in P}A_a^2)
   + O(|epsilon|^(2d_e+1)),
```

the distance-scaled congruence with `|epsilon|^-d_e` on each off-diagonal
coordinate has a finite operator-norm limit

```text
-diag(w_i, b_e).
```

Every `w_i` and `b_e` is strictly positive for the fixed assumptions:
`0<x_i<1`, connected `G`, and nonzero support weights.  The scaling matrix is
invertible for every `epsilon != 0`, and congruence preserves inertia.  Hence
the original unscaled Hessian is strictly negative definite once the scaled
matrix is sufficiently close to its strictly negative diagonal limit.

Strict feasibility is obtained independently by shrinking the same punctured
threshold so that

```text
|epsilon| ||A||_op < min_i{x_i,1-x_i}.
```

Then both `K_epsilon` and `I-K_epsilon` are positive definite.  The conclusion
is genuinely full `Sym(n)` curvature at the strict kernel, not just curvature
along the original ray.

For disconnected support, `X+epsilon A` is block diagonal over at least two
components.  Any nonzero direction crossing two components is an exact
cross-block flat direction by §2, so full negative definiteness is impossible.
This proves the stated connected/disconnected iff classification for the
small-puncture property at each fixed strict diagonal and fixed support-weight
matrix.

## 6. Independent finite sanity

I added `fresh_u7_audit.py`, a standard-library-only Fraction script that
imports no author module.  It rebuilds exact atoms using the shifted
determinant formula, expands the normalized exact-event entropy series, and
checks selected edge cases that are especially prone to false proofs.

Command from repository root:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\dense_hessian\connected_puncture_general\verifications\fresh_u7_audit.py
```

Exit code: `0`.

Generated files:

- script SHA256:
  `0C1BB698A37905DE31C122960006DB4028C1FEFC8C8BD0F682BF99DE0F4A5252`
- JSON SHA256:
  `0B9D0FAEB0DD470F7DFB586074491936524CEFF329B8F8CF89860B6D3C586CCB`

Finite denominator/scope accounting:

- one dense `n=4` exact-event gate: all 16 shifted-determinant atoms equal
  direct Möbius atoms, sum to one, and are positive for the chosen rational
  strict kernel;
- six cycle lengths `m=3,...,8`: the matching part gives coefficient `-1`,
  and adding the oriented-cycle quadratic contribution gives the doubled-cycle
  scalar coefficient `-3`;
- `P5` endpoint distance four: all Hessian coefficients below
  `epsilon^8` vanish, and the `epsilon^8` coefficient equals
  `-263671875/20939776`, matching the shortest-path formula;
- `C4` two-shortest-path target: the `epsilon^4` coefficient equals
  `-1269164425/16032016`, matching the positive sum over two geodesics;
- a chorded graph where a nominal longer path is shortened: the leading
  coefficient uses the true distance-two geodesic and equals
  `-390625/9801`;
- two same-distance mixed cases on `P5`, including shared endpoints and
  overlapping geodesics, have no same-scale mixed coefficient in the retained
  exact expansion;
- the `P5` endpoint first-derivative locality check has no coefficient through
  the required `epsilon^8` range.

These finite checks are deliberately not promoted to a theorem.  They only
support the line-by-line proof audit above and guard against transcription
errors in constants and event semantics.

## Final layered verdict

- Exact-event formula and entropy coefficient filtration: CORRECT.
- Bridge (1), residual-support locality after differentiating the full
  Hessian: CORRECT.
- Bridge (2), minimum degree, graph-distance lower bound, equality case,
  multiple-geodesic/shared-endpoint/chord hazards: CORRECT.
- Bridge (3), doubled-cycle coefficient `-3` and Hessian factor `-6`:
  CORRECT.
- Remainder orders, distance-weighted congruence limit, strict feasibility,
  and connected/disconnected iff quantifiers: CORRECT.

No critical gap or counterexample was found.
