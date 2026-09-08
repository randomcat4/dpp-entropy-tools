# Analytic curvature note for the fixed-beta path-affine family

AUTHOR STATUS: REVISED_SUBCLASS_PROVED, pending independent re-verification.
This is an author-side theorem note, not a `CORRECT` certificate.  It has been
revised after the first non-author audit found an overstrict equality statement
in Theorem 1.

## Setup

Fix \(n\ge 2\).  For \(\beta=(\beta_1,\ldots,\beta_{n-1})\), let
\(R_\beta\) be the unit lower-bidiagonal matrix

\[
(R_\beta)_{ii}=1,\qquad (R_\beta)_{i+1,i}=-\beta_i .
\]

For \(\tau\in(0,\infty)^n\), set

\[
S_\beta(\tau)=R_\beta^{-1}\operatorname{diag}(\tau)R_\beta^{-T},
\qquad
K_\beta(\tau)=I-S_\beta(\tau),
\]

and, when \(S_\beta(\tau)\prec I\),

\[
L_\beta(\tau)=R_\beta^T\operatorname{diag}(1/\tau)R_\beta-I.
\]

Then \(K_\beta(\tau)=L_\beta(\tau)(I+L_\beta(\tau))^{-1}\).  The map
\(\tau\mapsto K_\beta(\tau)\) is affine, and

\[
\frac{d}{dt}K_\beta(\tau+t\delta)
=-R_\beta^{-1}\operatorname{diag}(\delta)R_\beta^{-T}.
\]

Thus a \(\tau\)-affine line is a true \(K\)-space affine line.  Its rank is
\(\#\{i:\delta_i\ne0\}\).

Throughout, Shannon entropy uses natural logarithms and the exact-event DPP law
determined by the inclusion probabilities
\(\mathbb P(A\subseteq Y)=\det K_A\).

## Theorem 1: diagonal endpoint curvature

Let \(\beta=0\) and \(0<\tau_i<1\).  Then \(K_0(\tau)=I-\operatorname{diag}(\tau)\)
is a product Bernoulli DPP with

\[
\mathbb P(Y=S)=
\prod_{i\in S}(1-\tau_i)\prod_{i\notin S}\tau_i .
\]

Consequently

\[
H_0(\tau)=\sum_{i=1}^n h(\tau_i),
\qquad
h(x)=-x\log x-(1-x)\log(1-x),
\]

and for every direction \(\delta\in\mathbb R^n\),

\[
\frac{d^2}{dt^2}H_0(\tau+t\delta)\bigg|_{t=0}
=-\sum_{i=1}^n\frac{\delta_i^2}{\tau_i(1-\tau_i)}.
\]

In particular,

\[
\frac{d^2}{dt^2}H_0(\tau+t\delta)\bigg|_{t=0}
\le -4\|\delta\|_2^2,
\]

with equality exactly when every coordinate in the support of \(\delta\)
satisfies \(\tau_i=1/2\).  Nevertheless, for every nonzero \(\delta\),

\[
\frac{d^2}{dt^2}H_0(\tau+t\delta)\bigg|_{t=0}<0.
\]

### Proof

For \(\beta=0\), \(R=I\), \(S=\operatorname{diag}(\tau)\), and
\(K=I-S=\operatorname{diag}(1-\tau_i)\).  A diagonal DPP has independent atoms:
coordinate \(i\) is selected with probability \(1-\tau_i\) and absent with
probability \(\tau_i\).  Equivalently, from the \(L\)-ensemble formula,

\[
\det(I-K)\det L_S
=\prod_i\tau_i\prod_{i\in S}\left(\frac1{\tau_i}-1\right)
=\prod_{i\in S}(1-\tau_i)\prod_{i\notin S}\tau_i .
\]

The entropy is therefore the sum of the one-coordinate entropies.  Since

\[
h''(x)=-\frac1x-\frac1{1-x}=-\frac1{x(1-x)},
\]

the directional second derivative is the displayed sum.  Finally,
\(x(1-x)\le 1/4\) on \((0,1)\), with equality exactly at \(x=1/2\).  Hence
equality in the \(-4\|\delta\|_2^2\) bound occurs exactly when all nonzero
\(\delta_i\) are supported on coordinates with \(\tau_i=1/2\).  The same
formula is still strictly negative for every nonzero \(\delta\), since every
coefficient \(1/(\tau_i(1-\tau_i))\) is finite and positive.

## Theorem 2: small-coupling negative curvature with connected L path graph

Fix \(n\ge2\) and numbers

\[
0<a<b<1,\qquad 0<\eta<\frac1a-\frac1b.
\]

Let

\[
T_{a,b,\eta}
=\left\{\tau\in[a,b]^n:
\left|\frac1{\tau_1}-\frac1{\tau_n}\right|\ge\eta\right\}.
\]

There exists \(\varepsilon=\varepsilon(n,a,b,\eta)>0\) such that for every sign
pattern \(\sigma\in\{\pm1\}^{n-1}\), every

\[
\beta_i\in\sigma_i(0,\varepsilon)
\]

and every \(\tau\in T_{a,b,\eta}\), the following all hold.

1. \(0\prec K_\beta(\tau)\prec I\); equivalently \(K_\beta(\tau)\) is a strict
   real DPP kernel.
2. \(L_\beta(\tau)\succ0\), is tridiagonal, and its path graph has every
   adjacent edge nonzero, hence is graph-connected.
3. \(L_\beta(\tau)\) is heterogeneous: at least two displayed diagonal entries
   differ.
4. For every nonzero \(\delta\in\mathbb R^n\),

   \[
   \frac{d^2}{dt^2}H(K_\beta(\tau+t\delta))\bigg|_{t=0}<0.
   \]

Equivalently, the Shannon entropy is strictly concave along every sufficiently
short \(\tau\)-affine chord through such a point.  Since \(\tau\mapsto K\) is
affine, these are genuine \(K\)-space affine chords.  This theorem gives a
non-empty, non-degenerate continuous family of kernels whose \(L\)-graphs are
connected and where no positive local R3 gap can occur.

The word "connected" in this theorem refers to the graph of each tridiagonal
\(L_\beta(\tau)\), not to the topology of the full parameter set.  The
\(\tau\)-constraint \(T_{a,b,\eta}\) generally splits into the two branches
\(\tau_1^{-1}-\tau_n^{-1}\ge\eta\) and
\(\tau_1^{-1}-\tau_n^{-1}\le-\eta\).  If parameter-space connectedness is
needed, fix one \(\beta\) sign chamber and one of these two \(\tau\) branches.

### Proof

First choose \(\varepsilon_0>0\) so small that

\[
\|S_\beta(\tau)-\operatorname{diag}(\tau)\|_{\rm op}<\frac{1-b}{2}
\]

for all \(\|\beta\|_\infty\le\varepsilon_0\) and all
\(\tau\in[a,b]^n\).  Such an \(\varepsilon_0\) exists because \(R_\beta^{-1}\)
is a finite triangular matrix whose entries are polynomials in the \(\beta_i\),
hence \(S_\beta(\tau)\to\operatorname{diag}(\tau)\) uniformly on the compact
box \([a,b]^n\).  It follows that

\[
\lambda_{\max}S_\beta(\tau)<b+\frac{1-b}{2}<1.
\]

By the same uniform convergence, after possibly shrinking \(\varepsilon_0\),

\[
\lambda_{\min}S_\beta(\tau)>\frac a2>0.
\]

Thus \(0\prec S_\beta(\tau)\prec I\), so \(0\prec K_\beta(\tau)=I-S_\beta(\tau)\prec I\).
Consequently

\[
I+L_\beta(\tau)=S_\beta(\tau)^{-1}\succ I,
\]

and \(L_\beta(\tau)\succ0\).

The tridiagonal entries are

\[
(L_\beta)_{ii}=\tau_i^{-1}+\beta_i^2\tau_{i+1}^{-1}-1
\quad(1\le i<n),
\]

\[
(L_\beta)_{nn}=\tau_n^{-1}-1,
\qquad
(L_\beta)_{i,i+1}=-(\beta_i/\tau_{i+1}).
\]

Hence every edge is nonzero when each \(\beta_i\ne0\).  To force
heterogeneity, compare the first and last diagonal entries.  If
\(\left|\tau_1^{-1}-\tau_n^{-1}\right|\ge\eta\) and
\(|\beta_1|^2/a\le\eta/2\), then

\[
\left|\left(\tau_1^{-1}+\beta_1^2\tau_2^{-1}-1\right)
-\left(\tau_n^{-1}-1\right)\right|\ge\eta/2.
\]

After shrinking \(\varepsilon_0\) again, this holds on \(T_{a,b,\eta}\).
The assumption \(0<\eta<1/a-1/b\) ensures that \(T_{a,b,\eta}\) is nonempty
with nonempty branch interiors; otherwise the universal statement over
\(T_{a,b,\eta}\) may be vacuous or boundary-only.

It remains to prove the curvature claim.  On the strict DPP domain, exact atom
probabilities are positive and analytic in the entries of \(K\); equivalently,
using \(p(S)=\det(I-K)\det L_S\), they are positive and analytic in
\((\beta,\tau)\) wherever \(0<K<I\).  Therefore the entropy Hessian

\[
M(\beta,\tau)=\nabla_\tau^2 H(K_\beta(\tau))
\]

is continuous on a small closed neighborhood of
\(\{0\}\times[a,b]^n\).

By Theorem 1,

\[
M(0,\tau)=\operatorname{diag}\left(
-\frac1{\tau_1(1-\tau_1)},\ldots,
-\frac1{\tau_n(1-\tau_n)}
\right)
\preceq -4I
\]

for all \(\tau\in[a,b]^n\).  The largest eigenvalue of a symmetric matrix is
continuous, so compactness gives an \(\varepsilon\le\varepsilon_0\) such that

\[
\lambda_{\max}M(\beta,\tau)\le -2
\]

for all \(\|\beta\|_\infty\le\varepsilon\) and
\(\tau\in[a,b]^n\).  Therefore every nonzero \(\delta\) satisfies

\[
\delta^TM(\beta,\tau)\delta\le -2\|\delta\|_2^2<0.
\]

Restricting to the punctured sign chamber
\(\beta_i\in\sigma_i(0,\varepsilon)\) gives the claimed graph-connected,
heterogeneous, strict positive-contraction path subfamily.

## Boundaries

- The theorem is local in coupling size.  It does not prove global concavity
  of the full fixed-beta family.
- The theorem is qualitative: it proves existence of an
  \(\varepsilon(n,a,b,\eta)\), but does not provide a sharp computable value.
- The non-degenerate statement assumes \(0<\eta<1/a-1/b\).  For larger \(\eta\)
  the set \(T_{a,b,\eta}\) may be empty; for equality it is boundary-only.
- "Connected" means each \(L\)-matrix has a connected path graph.  The parameter
  set can have multiple sign and \(\tau\)-branch components unless those are
  fixed.
- Rank-one \(\tau\)-directions are already blocked by the Gu rank-one
  concavity prior art recorded by the parent task.  The theorem above also
  rules out multi-coordinate local positive gaps inside the small-coupling
  sign chambers.
- Finite negative searches up to \(n=100\) are supporting diagnostics only and
  are not used as a premise in the proof.
