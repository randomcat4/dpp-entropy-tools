# Arbitrary strict `A_0` centers: local corrected true entropy-rate concavity

Status: **PROVED AS AN AUTHOR THEOREM / PENDING INDEPENDENT REVIEW.**

This file combines the new `C^4` bridge in `arbitrary_A0_C4_proof.md` with the already accepted regularity-free parity matching bound. It is a theorem about the classical stationary DPP complete-configuration Shannon entropy rate along the physical affine kernel path.

## Theorem

Let

\[
\mathcal A_0=\left\{u:\sum_{m\in\mathbb Z}|\widehat u(m)|<\infty\right\}.
\]

Let real `c,g in A_0` satisfy

\[
c(\theta+1/2)=c(\theta),
\qquad
g(\theta+1/2)=-g(\theta),
\qquad g\ne0,
\tag{T.1}
\]

and suppose that for some `delta>0`,

\[
\delta\le c(\theta)\le1-\delta
\quad\text{a.e.}
\tag{T.2}
\]

Put

\[
\mu=\widehat c(0).
\]

For every odd integer `k` with `\widehat g(k)\ne0`, define

\[
\alpha_k=
\frac{|\widehat g(k)|^4}
{8\mu^2(1-\mu^2)}.
\tag{T.3}
\]

Then there exists `epsilon>0` such that `c+t g` is strictly legal for `|t|<=epsilon` and

\[
\boxed{
t\longmapsto h(c+t g)+\alpha_k t^4
\text{ is concave on }[-\epsilon,\epsilon].}
\tag{T.4}
\]

After shrinking `epsilon`, its second derivative is strictly negative for every `0<|t|<=epsilon`.

No small-Wiener-center assumption and no positive Fourier moment is required.

## 1. Exact parity identities

Half-period support gives

\[
\widehat c(j)=0\quad(j\text{ odd}),
\qquad
\widehat g(j)=0\quad(j\text{ even}).
\tag{1.1}
\]

Hence the even-coordinate and odd-coordinate restrictions of `T(c+t g)` do not depend on `t`. At `t=0` the cross-parity block vanishes, so the two parity DPPs are independent.

For every finite interval `Lambda_n`, writing its parity parts as `E_n,O_n`, the complete law satisfies

\[
P_{n,0}=P_{E_n}\otimes P_{O_n}
\]

and therefore

\[
D(P_{n,t}\|P_{n,0})
=H(P_{n,0})-H(P_{n,t}).
\tag{1.2}
\]

Also the diagonal gauge `D_{jj}=(-1)^j` gives

\[
T(c-tg)=D T(c+t g)D,
\]

and the zero-set diagonal of every complete event commutes with `D`. Thus every finite complete-event probability and every finite entropy is even in `t`. Passing to the entropy rate gives

\[
J(t):=h(c)-h(c+t g)
=d(P_t\|P_0)\ge0,
\qquad J(-t)=J(t).
\tag{1.3}
\]

## 2. New arbitrary-`A_0` regularity input

`arbitrary_A0_C4_proof.md` proves, directly from complete-event determinants, that under (T.1)-(T.2)

\[
\boxed{h(c+t g)\in C^4}
\tag{2.1}
\]

on a nonempty real neighborhood of zero.

The mechanism is finite-range preconditioning of the **fixed center**, not a global inverse theorem in the unweighted BGS algebra. A finite-range truncation `c^0` has uniformly gapped complete-event matrices and exponentially local event inverses. The Wiener tail `c-c^0+t g` is made small only in operator norm for the trace-log contraction. The reference inverse is then approximated in operator norm by configuration-local finite-support operators. Complete-event Bell differentiation costs the number of visited/localized coordinates, not their physical diameter, so only the unweighted sums

\[
\sum_j|\widehat c(j)|,
\qquad
\sum_j|\widehat g(j)|
\]

enter. The relative-KL density and fixed-reference cross-entropy density are separately shown `C^4`, and their exact finite identity gives (2.1). Fisher and atom acceleration remain inside the differentiated complete law.

## 3. Accepted regularity-free matching floor

For every odd `k` with `\widehat g(k)\ne0`, the accepted PR53 parity matching/negative-association bound applies without a Fourier regularity assumption beyond legality. It gives, for every sufficiently small legal `t`,

\[
J(t)
\ge\frac12 d_{\rm Ber}
\left(\mu^2-|\widehat g(k)|^2t^2\,\middle\|\,\mu^2\right).
\tag{3.1}
\]

As `t->0`,

\[
J(t)\ge C_k t^4+O(t^6),
\qquad
C_k=
\frac{|\widehat g(k)|^4}
{4\mu^2(1-\mu^2)}
=2\alpha_k.
\tag{3.2}
\]

Only this accepted matching floor is imported; no PR53 analytic-response theorem is used.

## 4. Curvature dichotomy

By (1.3) and (2.1), `J` is even, nonnegative, `C^4`, and has a minimum at zero. Thus

\[
J'(0)=0,
\qquad
J''(0)\ge0.
\]

Set

\[
F(t)=h(c+t g)+\alpha_k t^4
=h(c)-J(t)+\alpha_k t^4.
\]

If `J''(0)>0`, then `F''(0)<0`, so continuity gives `F''<0` on a sufficiently small interval.

If `J''(0)=0`, even `C^4` Taylor expansion gives

\[
J(t)=A t^4+o(t^4),
\qquad
J''(t)=12A t^2+o(t^2).
\tag{4.1}
\]

Comparing with (3.2) yields

\[
A\ge C_k=2\alpha_k.
\]

Therefore

\[
F''(t)
=-12(A-\alpha_k)t^2+o(t^2)
\le-12\alpha_k t^2+o(t^2)<0
\tag{4.2}
\]

for all sufficiently small nonzero `t`, while `F''(0)=0`. Shrink once more to preserve strict legality. This proves (T.4).

## 5. What is genuinely new

PR113 required

\[
\sum_{m\ne0}|\widehat c(m)|<\min(\mu,1-\mu),
\]

which is a small-center condition relative to the product Bernoulli reference. The present theorem allows **every** strict half-period-even `A_0` center, including centers with arbitrarily large off-zero Wiener mass consistent with pointwise strict legality.

PR110 requires the positive Sobolev/Fourier moment

\[
\sum_m(1+|m|)^2|\widehat u(m)|^2<\infty.
\]

The present theorem does not. For example, after choosing a strict finite trigonometric half-period-even base center, one may add a sufficiently small even-frequency tail of size

\[
\widehat r(2n)\asymp\frac1{n(\log(n+2))^2}
\]

with phases chosen to keep the symbol real, and similarly choose an odd-frequency direction with the same type of tail. These sequences are in `ell^1` but fail every positive weighted Wiener moment and can be chosen outside `H^1_F`. The center may simultaneously contain a large finite-range correlated component, so it need not satisfy PR113's small-Wiener inequality.

## 6. Nonclaims and evidence status

- The theorem is an **author proof pending independent review**.
- It does not prove concavity on the whole legal interval.
- It does not cover arbitrary merely measurable symbols outside `A_0`.
- It does not prove general real-kernel finite-dimensional entropy concavity.
- It supplies no entropy counterexample.
- It does not infer a common `ell^1` envelope for arbitrary `A_0` complete-event inverses from inverse-closedness.
- No numerical computation or finite-window sign extrapolation is used.
- Novelty is not assessed.

The physical path remains `K_t=T(c)+tT(g)` throughout, and all statements concern the true complete-configuration Shannon entropy rate.