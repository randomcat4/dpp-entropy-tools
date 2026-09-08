# D10-U6/S10 diagonal boundary geometry fresh non-author audit

STATUS: CORRECT.

Scope of this verdict: the geometric corollary in
`diagonal_boundary_geometry/` follows from the already reviewed U3/S9
punctured full-Hessian theorem and U2 diagonal-ridge Hessian degeneracy, with
the stated local/topological and finite-dimensional measure quantifiers.  I
found no critical gap.

Layered status:

- `CORRECT`: openness of `N_n`; every strict diagonal kernel is a relative
  boundary point of `N_n` in `Omega_n`; the full-edge set is open/dense/full
  spherical measure in the zero-diagonal unit sphere; `G_eta` is nonempty,
  compact, and positive spherical measure for
  `0<eta<1/sqrt(n(n-1))`; the compact-uniform U3/S9 threshold applies; and the
  final ambient positive-measure conclusion is justified via openness of
  `N_n`.
- `INCOMPLETE` only for things not claimed: density of `N_n` in all of
  `Omega_n`, sparse angular classifications, explicit thresholds, or global
  full-domain Hessian negativity.

No author file or shared index was modified.

## Inputs and hash binding

Author files read:

| file | SHA-256 |
|---|---|
| `diagonal_boundary_geometry/frozen_problem.md` | `0F31B44936C76E20EB5A3A8102DC76621BA6E871F191FCD986B32BA7AC77B68C` |
| `diagonal_boundary_geometry/proof_candidate.md` | `29047A495A0EB4549E40355B5D6E0907661C007E6F665D30554AD83D07CA54E3` |
| `diagonal_boundary_geometry/verdict.md` | `1AD4D0CD977B3C43F30AA4BDD06A8A29B85563E4AD05EFEE22A91302D9973433` |

Dependencies checked for quantifier scope:

| dependency | file checked | SHA-256 |
|---|---|---|
| U3/S9 punctured full-Hessian theorem | `punctured_diagonal_full_hessian/verifications/fresh_audit.md` | `74DB60B8D16DB613D26B3F86153A1698D636B66366BFA8B5EF043730AEC7A002` |
| U2 diagonal flat ridge | `diagonal_flat_ridge/verifications/fresh_audit.md` | `FDC44C699CF4AC62246776743634B7A4B84F42B217AE80EB4B5152A5C028FD86` |

The U3/S9 audit states `CORRECT` for the pointwise punctured theorem, its
fixed-dimension compact-uniform version, and pointwise open-neighborhood
consequence.  The U2 audit states `CORRECT` for the zero-diagonal Hessian
degeneracy and fourth-order diagonal-ridge structure.  I use only those
quantified statements below.

## 1. Openness of `N_n`

Let

```text
Omega_n = {K in Sym(n): 0<K<I}
N_n = {K in Omega_n: Hess H(K) is negative definite on Sym(n)}.
```

`Omega_n` is open in the finite-dimensional vector space `Sym(n)` because
strict spectral inequalities are open conditions.

For every `K in Omega_n`, all exact atoms are positive.  One way to see this
is to use the equivalent L-ensemble expression

```text
L = K(I-K)^(-1) > 0,
p(S) = det(I-K) det(L_S),
```

so every principal minor `det(L_S)` is positive and `det(I-K)>0`.  Equally,
near a strict point each exact atom remains positive by continuity.  Therefore
`H(K)=-sum_S p_S(K) log p_S(K)` is analytic on `Omega_n`: each `p_S` is a
polynomial in the entries of `K`, and the logarithm is evaluated only at
positive atoms.

In any fixed linear basis of `Sym(n)`, the Hessian matrix entries are
continuous functions of `K`.  The cone of negative-definite symmetric matrices
is open.  Hence `N_n` is open in `Omega_n`, and since `Omega_n` itself is open,
also open as a subset of the ambient `Sym(n)`.

This verifies Section 2 of the author proof.

## 2. Strict diagonal kernels are relative boundary points

Fix `n>=2` and a strict diagonal kernel

```text
X = diag(x_1,...,x_n),  0<x_i<1.
```

First, `X` is not in `N_n`.  U2 gives that every zero-diagonal symmetric
direction has zero second entropy variation at the diagonal base.  Since
`n>=2`, the zero-diagonal subspace contains a nonzero off-diagonal direction.
Thus the full Hessian at `X` has a nontrivial kernel and cannot be negative
definite.

Second, `X` is in the relative closure of `N_n` inside `Omega_n`.  Choose any
zero-diagonal full-edge `A`, for instance all off-diagonal entries nonzero.
U3/S9 supplies `epsilon_0(X,A)>0` such that

```text
X + epsilon A in N_n
```

for every `0<|epsilon|<epsilon_0(X,A)`.  Letting `epsilon -> 0` gives points
of `N_n` converging to `X`.

Since every relative neighborhood of `X` also contains `X` itself and
`X notin N_n`, `X` lies in the relative closure of both `N_n` and its
complement.  Hence `X` is a relative boundary point of `N_n` in `Omega_n`.

No density statement away from the diagonal stratum is used or implied.

## 3. Full-edge angular set `G`

Let

```text
V_0 = {A in Sym(n): diag A=0},
S_0 = {A in V_0: ||A||_F=1}.
```

For `n>=2`, `S_0` is the unit sphere in a vector space of edge dimension
`m=n(n-1)/2`, with Frobenius convention

```text
||A||_F^2 = 2 sum_{i<j} A_ij^2.
```

Define

```text
G = {A in S_0: A_ij != 0 for all i<j}.
```

For each edge `e=(i,j)`, the condition `A_ij=0` cuts `S_0` by the intersection
with a coordinate hyperplane.  For `m>=2` this is a closed great subsphere with
empty relative interior and spherical measure zero; for `n=2`, the
intersection is empty because `S_0` consists of the two points with
`|A_12|=1/sqrt(2)`.  In both cases, the finite union over edges is closed,
nowhere dense, and measure zero.  Its complement `G` is therefore open, dense,
and full spherical measure in `S_0`.

Applying U3/S9 to any `A in G` gives the claimed punctured radial entrance into
`N_n`.

This verifies the author's angular genericity statement.

## 4. The sector `G_eta`

For

```text
0 < eta < 1/sqrt(n(n-1)),
G_eta = {A in S_0: min_{i<j}|A_ij| >= eta},
```

the claimed nonemptiness, compactness, and positive spherical measure are
correct.

Nonempty: set every edge magnitude equal to

```text
alpha = 1/sqrt(n(n-1)).
```

There are `m=n(n-1)/2` edges, so

```text
||A||_F^2 = 2 m alpha^2 = n(n-1) alpha^2 = 1.
```

Because `eta<alpha`, this point lies in the strict interior of the displayed
coordinate inequalities.

Compact: each map `A -> |A_ij|` is continuous, so `G_eta` is closed in the
compact sphere `S_0`.

Positive spherical measure: for `n>=3`, a small relative spherical
neighborhood of the equal-magnitude point still satisfies all inequalities
`|A_ij|>eta`, so `G_eta` contains a nonempty relatively open patch of `S_0`.
For `n=2`, `S_0` is a two-point sphere and the strict inequality
`eta<1/sqrt(2)` makes `G_eta=S_0`, which has positive normalized spherical
measure.  Thus the endpoint `eta<1/sqrt(n(n-1))` is the right positive-measure
range.  At equality, the set may be nonempty but loses positive measure in
higher dimensions, so the author's strict inequality is necessary for the
positive-measure conclusion.

No connectedness of `G_eta` is claimed or needed; sign chambers may be
disconnected.

## 5. Compact-uniform use of U3/S9

The U3/S9 frozen theorem and fresh audit include the compact-uniform clause:
for fixed `n`, compact diagonal box `x_i in [a,b] subset (0,1)`, normalized
`||A||_F=1`, and a uniform full-edge lower bound
`min_{i<j}|A_ij|>=eta>0`, one common `epsilon_0(a,b,n,eta)>0` works for all
such `X`, all such `A`, both signs of nonzero `epsilon`, and all full
`Sym(n)` Hessian test directions.

The present `G_eta` is exactly such a compact normalized angular family.
Therefore the author is entitled to conclude:

```text
for every box diagonal X,
every A in G_eta,
and every 0<|epsilon|<epsilon_0(a,b,n,eta),
X+epsilon A in N_n.
```

The quantifiers do not range over changing `n`, `eta` tending to zero,
unnormalized `A`, or sparse directions.  The author proof does not claim those
extensions.

## 6. Angular/radial sector versus ambient measure

This is the most delicate measure point.  The zero-diagonal angular/radial
sector itself lies in the affine subspace

```text
X + V_0,
```

which has codimension `n` inside `Sym(n)`.  Therefore that sector alone has
zero ambient Lebesgue measure in `Sym(n)`.

The author proof does not need, and does not successfully assert, that the
sector alone has positive ambient measure.  The valid route is:

1. Pick any `A` in a positive-measure angular patch of `G_eta`.
2. Pick `0<|r|<epsilon_0` small enough that `K=X+rA` is inside the prescribed
   ambient ball around `X`.
3. U3/S9 gives `K in N_n`.
4. Section 1 gives `N_n` open in ambient `Sym(n)`.
5. Hence there is some ordinary ambient ball `B(K,delta)` contained in `N_n`.
6. Shrinking `delta` if necessary to stay inside the original ball around `X`,
   the intersection of that original ball with `N_n` contains a nonempty
   ambient open set, hence has positive ambient Lebesgue measure.

This proves the author's final “every sufficiently small ball about every box
diagonal X meets `N_n` in a nonempty open set of positive ambient Lebesgue
measure” statement without confusing zero-diagonal spherical measure with
ambient Lebesgue measure.

The statement could even be made for any positive ball radius small enough to
work in the intended local neighborhood; the proof only needs choosing
`|r|` smaller than both the U3 threshold and the ball radius.

## 7. Boundary and non-density scope

The candidate explicitly says it does not assert `N_n` is dense in all of
`Omega_n`.  The proof only gives accumulation of `N_n` at the strict diagonal
stratum through full-edge zero-diagonal punctures, plus open ambient
neighborhoods around those punctured points.  It does not control kernels far
from the diagonal stratum and does not classify sparse angular directions.

This scope matches the U3/S9 and U2 dependency boundaries.

## Final verdict

STATUS: CORRECT.

The proof candidate's topology and measure conclusions follow from the
reviewed U3/S9 and U2 inputs with correct quantifiers.  The only caution needed
is interpretive, not a repair: positive spherical measure is first established
inside the zero-diagonal unit sphere, while positive ambient Lebesgue measure
comes only after passing through a punctured point of `N_n` and using openness
of `N_n`.  The author proof's last paragraph uses exactly that route, so no
critical gap remains.
