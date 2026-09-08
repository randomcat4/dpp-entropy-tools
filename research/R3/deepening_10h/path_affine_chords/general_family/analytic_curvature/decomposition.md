# One-dimensional recurrence and curvature decomposition

AUTHOR STATUS: DERIVED_REVISED_BOUNDARIES, pending independent re-verification.

This note records what the path structure proves analytically, and where a
global sign proof can still fail.

## 1. Selected-run factorization

Let \(L=L_\beta(\tau)\succ0\) be tridiagonal.  For an interval
\([a,b]\subseteq\{1,\ldots,n\}\), define

\[
\kappa(a,b)=\det L_{\{a,\ldots,b\}},\qquad \kappa(a,a-1)=1.
\]

If a selected set \(S\) decomposes into maximal consecutive runs

\[
S=[a_1,b_1]\sqcup\cdots\sqcup[a_m,b_m],
\qquad b_j+1<a_{j+1},
\]

then \(L_S\) is block diagonal, hence

\[
\det L_S=\prod_{j=1}^m \kappa(a_j,b_j).
\]

The interval determinants are continuants:

\[
\kappa(a,b)
=d_b\kappa(a,b-1)-e_{b-1}^2\kappa(a,b-2),
\]

where \(d_i=L_{ii}\) and \(e_i=L_{i,i+1}\).

## 2. Tilted partition recurrence

For real \(\alpha\) near \(1\), define the tilted path partition function

\[
Z_m(\alpha,t)
=\sum_{S\subseteq\{1,\ldots,m\}}\det L(t)_S^\alpha .
\]

Here \(L(t)=L_\beta(\tau+t\delta)\), and the power means
\(\exp(\alpha\log\det L(t)_S)\).  All principal minors are positive because
\(L(t)\succ0\) for sufficiently small \(|t|\).

The last vertex \(m\) is either absent, or belongs to a final selected run
\([a,m]\).  Therefore

\[
Z_m(\alpha,t)
=Z_{m-1}(\alpha,t)
+\sum_{a=1}^m
Z_{a-2}(\alpha,t)\kappa(a,m;t)^\alpha ,
\]

with \(Z_0=Z_{-1}=1\).  This is a one-dimensional renewal/Markov-style
recurrence: a zero after a selected run regenerates the prefix.

Let

\[
F(\alpha,t)=\log Z_n(\alpha,t).
\]

The \(L\)-ensemble exact-event law is

\[
p_t(S)=\frac{w_S(t)}{Z_n(1,t)},
\qquad w_S(t)=\det L(t)_S.
\]

Since

\[
\partial_\alpha F(1,t)
=\sum_S p_t(S)\log w_S(t),
\]

the Shannon entropy is

\[
H(t)=F(1,t)-\partial_\alpha F(1,t).
\]

Thus all directional entropy derivatives can be obtained by differentiating a
one-dimensional recurrence instead of enumerating \(2^n\) exact atoms.

## 3. Curvature identity under the tilted law

For a fixed direction \(\delta\), put

\[
\ell_S(t)=\log w_S(t),\qquad
A_S(t)=\ell_S'(t),\qquad
B_S(t)=\ell_S''(t),
\]

and let \(\mathbb E_t\) denote expectation under \(p_t(S)\).  For any
time-dependent statistic \(f_S(t)\),

\[
\frac{d}{dt}\mathbb E_t[f]
=\mathbb E_t[f']+\operatorname{Cov}_t(f,A).
\]

Since \(H=F-\mathbb E[\ell]\) and \(F'=\mathbb E[A]\),

\[
H'=-\operatorname{Cov}(\ell,A).
\]

Differentiating the covariance gives

\[
\boxed{
H''
=-\operatorname{Var}(A)
-\operatorname{Cov}(\ell,B)
-\mathbb E\left[(\ell-\mathbb E\ell)(A-\mathbb EA)^2\right].
}
\]

The first term is always non-positive.  The remaining block

\[
\mathcal R
=-\operatorname{Cov}(\ell,B)
-\mathbb E\left[(\ell-\mathbb E\ell)(A-\mathbb EA)^2\right]
\]

is the only possible source of a positive curvature sign:

\[
H''=-\operatorname{Var}(A)+\mathcal R.
\]

Therefore a checkable sufficient condition for strict negative curvature in a
direction is

\[
\mathcal R<\operatorname{Var}(A).
\]

A crude but computable certificate interface is

\[
\mathcal R
\le
\left|\operatorname{Cov}(\ell,B)\right|
+\mathbb E\left[|\ell-\mathbb E\ell|(A-\mathbb EA)^2\right],
\]

so any rigorous upper bound on the right-hand side below
\(\operatorname{Var}(A)\) proves \(H''<0\) for that direction.

## 4. Relation to the O(n^2) jet DP

The implemented D10-B3 jet DP computes the same objects in \(O(n^2)\) arithmetic
for a fixed direction:

1. interval determinant jets \((\kappa,\kappa',\kappa'')\);
2. selected-run partition jets \(Z,Z',Z''\);
3. selected-run log-weight moment jets
   \(T=\sum_S w_S\log w_S\);
4. \(H=\log Z-T/Z\), using the stable quotient recurrence.

The tilted recurrence above gives an equivalent route:

\[
H''=\partial_t^2F(1,t)-\partial_\alpha\partial_t^2F(1,t).
\]

Both viewpoints avoid exact-event enumeration.  The covariance identity is more
useful for proof search because it separates the always-negative Fisher term
\(-\operatorname{Var}(A)\) from the sign-indefinite residual \(\mathcal R\).

## 5. What is still open

The small-coupling theorem proves strict negative curvature in a continuous
family whose tridiagonal \(L\)-graph is connected.  It does not assert that the
whole parameter domain is topologically connected: the heterogeneity set
\(T_{a,b,\eta}\) usually has two \(\tau\)-branches, and the nonzero \(\beta\)
condition has separate sign chambers.  Nor does it settle the global fixed-beta
path family.
For a global proof, one must control \(\mathcal R\) uniformly.  Equivalently,
one must rule out a regime where

\[
-\operatorname{Cov}(\ell,B)
-\mathbb E\left[(\ell-\mathbb E\ell)(A-\mathbb EA)^2\right]
>
\operatorname{Var}(A).
\]

No such rigorously verified regime is known in this route.  The corrected
D10-B3 search found no positive finite signal up to \(n=100\), but that remains
finite evidence rather than a theorem.
