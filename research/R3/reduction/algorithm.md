# Verifiable grouped reduction for exact-event DPP entropy

Status: PROVED for the finite strict grouped low-rank formulas below, as an
author-level mathematical derivation plus executable small-n checks.  Status:
INCOMPLETE for any real-symmetric counterexample search, any claim covering all
real kernels, and any use of T2 as an unexamined black box.  This file is not a
fresh-context verification report.

All logarithms are natural.  The ground set is `E=[n]`.  A finite
marginal-kernel DPP has inclusion probabilities

```text
P(A subset Y) = det K_A,        A subset E,
```

where `K_A` is the principal submatrix indexed by `A` and `det K_empty=1`.
The exact atom probability is `p_K(S)=P(Y=S)`, and the full-subset Shannon
entropy is

```text
H(K) = - sum_{S subset E} p_K(S) log p_K(S),      0 log 0 := 0.
```

The determinant `det K_S` is an inclusion probability.  It is not, except in
special cases, the exact event probability.

## 1. Exact events from inclusion probabilities

For each `A subset E`, define

```text
F(A) = P(A subset Y) = det K_A.
```

Since the event `{A subset Y}` is the disjoint union of exact events
`{Y=S}` over all `S superset A`,

```text
F(A) = sum_{S superset A} p_K(S).
```

Mobius inversion on the Boolean lattice gives, for every `S subset E`,

```text
p_K(S) = sum_{T subset E\S} (-1)^|T| det K_{S union T}.          (1)
```

Proof: substitute the right side into `sum_{S superset A}`.  For a fixed
`R superset A`, the coefficient of `det K_R` becomes

```text
sum_{S: A subset S subset R} (-1)^|R|-|S|
  = (1-1)^|R|-|A|,
```

which is `1` if `R=A` and `0` otherwise.  Hence the inverted values have
exactly the required inclusion sums, so they are the unique atom probabilities.

Formula (1) is valid for every finite marginal kernel for which the DPP exists,
including singular boundary kernels.  Its naive cost is exponential; in the
implementation it is used only as an `n<=8` checker.

## 2. L-ensemble event formula for strict contractions

Assume now that `K` is a strict positive contraction:

```text
0 < K < I.
```

Set

```text
L = K (I-K)^(-1).
```

Then `L` is positive definite and the exact atom probabilities are

```text
p_K(S) = det(I-K) det L_S.                                  (2)
```

Proof.  Define a candidate law by the right side of (2).  Its probability
generating polynomial is

```text
Q(z) = sum_S det(I-K) det L_S prod_{i in S} z_i
     = det(I-K) det(I + Z L),
```

where `Z=diag(z_i)`.  The last equality is the principal-minor expansion:
the principal minor of `ZL` indexed by `S` is
`prod_{i in S} z_i det L_S`.

Right-multiply before taking determinants:

```text
det(I-K) det(I + ZL)
  = det((I + ZL)(I-K))
  = det(I-K + ZK).
```

Put `Z=I+W` with `W=diag(w_i)`.  Then

```text
Q(1+w) = det(I + W K)
       = sum_A det K_A prod_{i in A} w_i.
```

For any exact-event law,

```text
E prod_{i in Y} (1+w_i)
  = sum_A P(A subset Y) prod_{i in A} w_i.
```

Thus the candidate law has inclusion probabilities `det K_A` for every `A`.
By the uniqueness proved in Section 1, it is the DPP atom law.  This also
proves normalization, because `Q(1)=1`.

Boundary note: (2) requires `I-K` invertible and is used here only for
`0<K<I`.  Singular kernels should be handled by Mobius inversion or by a
separately proved limiting argument with explicit error control.

## 3. Grouped low-rank kernel `K=aI+UCU^T`

Let the rows of `U in R^{n x r}` take only `g` values

```text
x_1, ..., x_g in R^r,
```

with multiplicities

```text
N_1, ..., N_g,        sum_g N_g = n.
```

Assume `C=C^T`, `0<a<1`, and the resulting

```text
K = a I_n + U C U^T
```

is a strict positive contraction.  Let

```text
b     = 1-a,
G     = U^T U = sum_g N_g x_g x_g^T,
alpha = a/b.
```

The matrix determinant lemma gives

```text
det(I-K)
  = det(bI_n - U C U^T)
  = b^n det(I_r - b^(-1) C G).                           (3)
```

Woodbury gives a grouped form of `L`:

```text
(I-K)^(-1)
  = b^(-1) I_n + b^(-1) U (bI_r - C G)^(-1) C U^T,

L = K(I-K)^(-1)
  = alpha I_n + U M U^T,

M = b^(-1) (bI_r - C G)^(-1) C.                          (4)
```

To verify the inverse, multiply `(bI-UCU^T)` by the displayed right side.
The only nontrivial bracket is

```text
(I - b^(-1) C G)(bI-CG)^(-1) C - b^(-1) C = 0.
```

Now take an exact event `S`.  Let

```text
c_g = |S intersect group g|,
s   = sum_g c_g,
G_c = U_S^T U_S = sum_g c_g x_g x_g^T.
```

Since `L_S = alpha I_s + U_S M U_S^T`, the matrix determinant lemma gives

```text
det L_S
  = alpha^s det(I_r + alpha^(-1) M G_c).                 (5)
```

Equations (2), (3), and (5) show that `p_K(S)` depends only on the count vector
`c=(c_1,...,c_g)`.  Hence

```text
p(c) = det(I-K) alpha^sum(c)
       det(I_r + alpha^(-1) M sum_g c_g x_g x_g^T).       (6)
```

There are

```text
N(c) = prod_g binom(N_g, c_g)
```

events with this count vector.  Therefore the entropy is

```text
H(K) = - sum_{0<=c_g<=N_g} N(c) p(c) log p(c).            (7)
```

Important entropy bookkeeping: the logarithm in (7) is the logarithm of the
single-event probability `p(c)`, not the logarithm of the whole count-class
mass `N(c)p(c)`.

## 4. Block-exchange specialization

The existing R3 frozen theorem uses a slightly different but compatible
block-exchange model.  Partition `E` into groups `G_g` of sizes `m_g`.  Let
`U` have normalized indicator columns

```text
U_{i,g} = 1/sqrt(m_g) if i in G_g, and 0 otherwise.
```

Let `A` act as `a_g I` on group `g`, with `0<a_g<1`, and let `0<C<I` on the
group-constant subspace.  Define

```text
K = A + U(C - diag(a_g))U^T.
```

Then `K` has eigenvalue `a_g` on the `m_g-1` dimensional within-group
zero-sum subspace, and acts as `C` on the group-constant subspace.  Thus
`0<K<I`.

Let

```text
ell_g = a_g/(1-a_g),
R     = C(I-C)^(-1),
B     = R - diag(ell_g).
```

Then `L=K(I-K)^(-1)` acts as `ell_g I` on the within-group zero-sum
subspace and as `R` on the group-constant subspace, so in coordinates

```text
L = D + U B U^T,
```

where `D` is diagonal with value `ell_g` on group `g`.  For an event count
vector `c`, the diagonal part restricted to `S` has determinant
`prod_g ell_g^{c_g}`, and

```text
U_S^T D_S^(-1) U_S = diag(c_g/(m_g ell_g)).
```

Again by the matrix determinant lemma,

```text
det L_S =
  prod_g ell_g^{c_g}
  det(I_q + B diag(c_g/(m_g ell_g))).                    (8)
```

Combining with (2) gives the exact-event formula in the R3 frozen theorem.
This is a theorem for the stated block-exchange family only; it is not a
coverage result for all real symmetric kernels.

The displayed determinant is often non-symmetric:

```text
det(I_q + B D_c),        D_c=diag(c_g/(m_g ell_g)).
```

Here `B=R-diag(ell_g)` is symmetric, while `B D_c` need not be.  For numerical
sign/logdet work it is better to use the symmetric equivalent

```text
det(I_q + B D_c)
  = det(I_q + sqrt(D_c) B sqrt(D_c)).                    (9)
```

This is exact even when some `c_g=0`.  Let `R_c=sqrt(D_c)`.  Then
`D_c=R_c R_c`, and Sylvester's determinant identity gives

```text
det(I + B R_c R_c) = det(I + R_c B R_c).
```

The right-hand matrix is real symmetric.  Under the strict DPP assumptions the
original principal minor `det L_S` is positive; the symmetric form prevents a
floating implementation from inventing a negative sign only because it applied
`slogdet` to a non-symmetric product.  In exact rational arithmetic one may
still evaluate the non-symmetric form directly because determinant equality is
algebraic.

## 5. Compatible real-symmetric chords

A chord is compatible with the grouped reduction when all points on the chord
share the same group partition and the same feature rows:

```text
K_0 = a_0 I + U C_0 U^T,
K_1 = a_1 I + U C_1 U^T,
K_t = (1-t)K_0 + tK_1
    = a_t I + U C_t U^T,

a_t = (1-t)a_0 + t a_1,
C_t = (1-t)C_0 + t C_1.
```

If strict positive contraction certificates hold for `K_0` and `K_1`, then
`K_t` is feasible for every `t in [0,1]` by convexity.  For numerical
certificates it is still useful to check the point actually used, especially
when interval arithmetic or rational rounding changes the endpoints.

The implementation uses the Jensen concavity-gap convention

```text
J_t(K_0,K_1) = H(K_t) - (1-t)H(K_0) - t H(K_1).           (10)
```

Concavity predicts `J_t>=0`.  A real finite-dimensional concavity violation is
therefore certified by `J_t<0`.

The R3 problem statement also uses the opposite midpoint violation magnitude

```text
Delta = (H(K_-)+H(K_+))/2 - H(M) = -J_{1/2}(K_-,K_+).
```

Thus `Delta>0` is the same as `J_{1/2}<0`.  Every report should name which
sign convention it is using.

## 6. Complexity

Naive atom computation:

```text
2^n events, each requiring a determinant or a Mobius sum.
```

The checker in `reference_implementation.py` intentionally uses the slow
Mobius formula for `n<=8`.

Grouped low-rank computation:

```text
count states = prod_g (N_g+1).
```

For each count state, (6) needs an `r x r` determinant and the rank-`r` Gram
sum `G_c`.  With incremental updates the arithmetic cost is

```text
O( prod_g(N_g+1) * r^3 )
```

and memory can be `O(r^2+g)` for streaming entropy accumulation.  For fixed
`g` and `r`, this is polynomial in `n`; for fixed group sizes but growing `g`,
the count grid can still be exponential in `g`.

Memoized dynamic programming is valid when distinct count vectors collide in
the same reduced state.  Let a reduced state be `(s,G_c)`, where
`s=sum c_g`.  Process groups one at a time and update

```text
D_{h+1}(s+k, G + k x_{h+1}x_{h+1}^T)
 += D_h(s,G) binom(N_{h+1},k),       0<=k<=N_{h+1}.
```

Induction on `h` proves that `D_h` is exactly the total multiplicity of partial
count vectors producing that reduced state.  At the end, evaluate (6) once per
distinct state and multiply by the stored multiplicity.

This DP may be much smaller than the full count grid when many feature
outer-products coincide or have small integer structure.  In the generic case
there may be no collisions, so this is an exact compression opportunity, not a
claimed universal polynomial algorithm in `g`.

Also, the determinant part of (6) is a degree-at-most-`r` polynomial in the
counts, so normalization and some low moments can sometimes be computed through
exterior-power identities.  The entropy has an additional `log det(...)` term;
this file does not claim a general exact entropy formula using only finitely
many polynomial moments.  Further compression of that logarithmic residual is
OPEN.

## 7. Strict positive-contraction certificates

For arbitrary exact rational `K`, one may certify

```text
K > 0 and I-K > 0
```

by exact Sylvester or LDL checks on both matrices.  This costs full `n x n`
linear algebra.

For `K=aI+UCU^T`, a smaller certificate is available when

```text
G = U^T U
```

is nonsingular.  On `ker U^T`, `K` has eigenvalue `a` and `I-K` has eigenvalue
`1-a`.  On `col(U)`, write a vector as `Uy` and set `z=Gy`.  Then

```text
(Uy)^T K (Uy)     = z^T (C + a G^(-1)) z,
(Uy)^T(I-K)(Uy)  = z^T ((1-a)G^(-1) - C) z.
```

Therefore the following exact conditions are sufficient and necessary in this
full-column-rank representation:

```text
0<a<1,
G > 0,
C + a G^(-1) > 0,
(1-a)G^(-1) - C > 0.                                  (11)
```

The implementation reports exact leading principal minors for these small
forms.  If `G` is singular, first delete redundant feature columns or use a
full-space certificate; the current helper reports that case as unsupported,
not as infeasible.

## 8. Numerical stability and gap enclosures

For candidate search, floating `slogdet` on the small `r x r` matrices is
usually adequate.  For certification, use directed arithmetic:

1. Certify strict feasibility of every endpoint, and of any rounded midpoint
   actually used.
2. Compute each atom probability per count class as a rational or interval
   using (6), including the multiplicity separately.
3. Enclose `-p log p` with outward-rounded logarithm intervals.  The previous
   T3-style exact check used range reduction to `[1,2]` and the positive
   `atanh` series with an explicit geometric tail; the same log oracle can be
   plugged into this count reduction.
4. Sum entropy intervals over count states with outward rounding.
5. Combine entropy intervals for a chord using the sign-correct interval rule.

If

```text
H_i in [lo_i, hi_i]   for i=0,1,t,
```

then the Jensen gap (10) satisfies

```text
J_t in [
  lo_t - (1-t)hi_0 - t hi_1,
  hi_t - (1-t)lo_0 - t lo_1
].                                                        (12)
```

For the R3 violation magnitude `Delta=-J_{1/2}`, reverse the endpoints.

If only probability intervals are available, apply the continuous function
`phi(p)=-p log p` on each probability interval.  Since `phi'(p)=-log p-1`,
the interval maximum/minimum must check the endpoint values and the critical
point `p=e^(-1)` if it lies inside the interval.  Do not add epsilon to zero
probabilities; use the convention `0 log 0=0` or a proved limiting argument.

## 9. Relationship to T2 finite-block loss bounds

I inspected the R2 fixed commit named by the R3 ledger:

```text
27dda692856da210e23ae74ce267b813d3221822
T2: finite-block entropy gap transfer tool and reproducible evidence
```

The exact frozen T2 v1 statement is:

* For finite Hermitian `0<=K<=I` and a coordinate partition `Pi`, let
  `B=P_Pi(K)` be block pinching.  Define
  `L_Pi(K)=H(B)-H(K)` and
  `Q_Pi(K)=tr h(B)-tr h(K)`.  Claim A states
  `0 <= L_Pi(K) <= Q_Pi(K)`, including singular kernels.
* If `eta I <= B <= (1-eta)I`, Claim B states
  `Q_Pi(K) <= tr(E^2 [B(I-B)]^(-1))
             <= ||E||_F^2/[eta(1-eta)]`,
  where `E=K-B`.
* For the same partition along a chord, with
  `J_t=H(K_t)-(1-t)H(K_0)-tH(K_1)`, Claim C states that any valid upper bounds
  `C_r >= L_Pi(K_r)` imply

```text
J_t^B - C_t <= J_t <= J_t^B + (1-t)C_0 + t C_1.
```

The fresh T2 verifier report at the same fixed local source marked those
claims `CORRECT` within their finite-dimensional scope.  I did not rerun the
T2 artifact or promote it to a new R3 theorem.

Condition check against this R3 reduction:

* Our kernels are finite real symmetric strict contractions, hence lie inside
  T2's finite Hermitian feasible class when a T2 partition is supplied.
* Our formula computes `H(K_r)` directly for compatible grouped low-rank
  points.  It therefore does not require T2 to evaluate the finite chord gap.
* If a later R3 route uses T2 to replace full entropy by block entropy plus a
  loss bound, it must provide the partition, the pinched kernels `B_r`, the
  buffer `eta` when Claim B is used, and the asymmetric coefficients in Claim
  C.  The sign conversion to the R3 `Delta=-J` convention must be explicit.
* OPEN: no integration theorem is proved here showing that a particular
  `n>=11` grouped low-rank family has a T2 loss small enough to transfer a
  negative Jensen gap.  Such a claim needs its own finite-scale inequality
  `error < target_gap`.

Consequently, this reduction is compatible with T2 as an entropy evaluator or
as a source of external loss bounds, but no T2 block-loss conclusion is used as
a black box in the proof above.

## 10. Implementation and verification coverage

The reference implementation provides:

* exact rational Mobius atom probabilities for small `n`;
* exact rational L-ensemble atom probabilities for small strict `K`;
* construction of `K=aI+UCU^T` from repeated feature rows;
* reduced count-state probabilities using (6);
* entropy from count classes with high-precision Decimal logarithms;
* strict positive-contraction certificate (11) for full-rank feature Gram;
* compatible chord Jensen gap computation;
* an interval-combination helper implementing (12).

The tests compare, for `n<=8`, all of the following:

```text
direct Mobius atoms == full L-ensemble atoms == grouped count atoms.
```

They include a random-like grouped case, a near-boundary strict case with very
small atom probabilities, a standard-basis block-exchange case, and a
compatible chord gap comparison.  These tests validate the implementation and
catch sign/multiplicity mistakes; they are not a substitute for the algebraic
proofs above.

Nonclaims:

* No finite numerical check is promoted to a theorem about all real symmetric
  DPP kernels.
* No five-parameter or other small family is called a high-dimensional
  covering family.
* No candidate real counterexample is certified here.
* Ordinary Decimal entropy values are diagnostics.  Strict final signs require
  outward-rounded entropy intervals or exact rational log bounds.
