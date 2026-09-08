# Derivation and curvature structure in tau coordinates

AUTHOR STATUS: DERIVED, pending independent verification.

## 1. Why tau is the right affine coordinate

For \(L\succ0\),

\[
\Phi(L)=L(I+L)^{-1}=I-(I+L)^{-1}.
\]

Write

\[
S=(I+L)^{-1}.
\]

Then a K-space affine chord is the same as an S-space affine chord:

\[
K_0=\frac{K_-+K_+}{2}
\quad\Longleftrightarrow\quad
S_0=\frac{S_-+S_+}{2}.
\]

The fixed-beta construction chooses a path Markov covariance form

\[
S(\tau)=R^{-1}\operatorname{diag}(\tau)R^{-T}.
\]

For fixed \(R\), this is linear in \(\tau\), while

\[
S(\tau)^{-1}=R^T\operatorname{diag}(1/\tau)R
\]

is tridiagonal.  Thus the nonlinear map \(L\mapsto K\) becomes linear after
passing through the inverse covariance \(S\).

## 2. Rank-one coordinate directions

Let \(u_i\) be the \(i\)-th column of \(R^{-1}\).  Then

\[
S(\tau)=\sum_i \tau_i u_i u_i^T,
\qquad
K(\tau)=I-\sum_i \tau_i u_i u_i^T.
\]

Hence

\[
\partial_{\tau_i}K=-u_i u_i^T,
\]

a rank-one negative semidefinite direction.  More generally, for a chord
direction \(v\),

\[
K(\tau+v)-K(\tau)=-R^{-1}\operatorname{diag}(v)R^{-T},
\]

so

\[
\operatorname{rank}(K(\tau+v)-K(\tau))
=\#\{i:v_i\ne0\}.
\]

This cleanly separates two mechanisms:

- support size one is a rank-one K direction and is blocked by the Gu
  rank-one concavity result recorded by the parent task;
- any positive midpoint gap in this family must use support size at least two,
  i.e. mixed \(\tau\)-coordinate curvature.

## 3. Exact atom derivatives from Möbius inversion

This subsection is structural; it is not the scalable evaluator.

For an exact event \(A\subseteq E\),

\[
p_A(\tau)=
\sum_{T\subseteq A^c}(-1)^{|T|}
\det K_{A\cup T}(\tau).
\]

For a principal set \(M\), define

\[
\alpha_i(M)=u_{i,M}^T K_M^{-1}u_{i,M},
\qquad
\gamma_{ij}(M)=u_{i,M}^T K_M^{-1}u_{j,M},
\]

where vectors are restricted to coordinates in \(M\).  Since

\[
\partial_i K_M=-u_{i,M}u_{i,M}^T,
\]

Jacobi's determinant formula gives

\[
\partial_i\det K_M
=-\det K_M\,\alpha_i(M).
\]

For second derivatives,

\[
\partial_{ij}\det K_M
=\det K_M\left(\alpha_i(M)\alpha_j(M)-\gamma_{ij}(M)^2\right).
\]

When \(i=j\), this is zero, reflecting the determinant lemma fact that each
principal determinant is affine in every single \(\tau_i\) coordinate.

Therefore

\[
\partial_i p_A
=-\sum_{T\subseteq A^c}(-1)^{|T|}
\det K_{A\cup T}\,\alpha_i(A\cup T),
\]

and

\[
\partial_{ij}p_A
=\sum_{T\subseteq A^c}(-1)^{|T|}
\det K_{A\cup T}
\left(\alpha_i\alpha_j-\gamma_{ij}^2\right)_{A\cup T}.
\]

The sums of the first and second derivatives over all atoms vanish because
\(\sum_A p_A(\tau)=1\).

## 4. Entropy first and second derivatives

With natural-log Shannon entropy

\[
H(\tau)=-\sum_A p_A(\tau)\log p_A(\tau),
\]

strict feasibility gives \(p_A>0\).  Differentiating and using
\(\sum_A\partial_i p_A=0\),

\[
\partial_i H
=-\sum_A \partial_i p_A\log p_A.
\]

For the Hessian,

\[
\partial_{ij}H
=-\sum_A \partial_{ij}p_A\log p_A
-\sum_A\frac{\partial_i p_A\,\partial_j p_A}{p_A}.
\]

In particular, since \(\partial_{ii}p_A=0\),

\[
\partial_{ii}H
=-\sum_A\frac{(\partial_i p_A)^2}{p_A}\le0.
\]

This matches the rank-one blocker: every coordinate line in \(\tau\) is a
rank-one K-space direction and is locally concave.  Any local convexity in a
direction \(v\) must come from mixed terms
\(\partial_{ij}H\) with \(i\ne j\).

For a small symmetric chord \(\tau\pm hv\),

\[
\Delta(h)
=\frac{H(\tau-hv)+H(\tau+hv)}2-H(\tau)
=\frac{h^2}{2}v^T\nabla^2 H(\tau)v+O(h^4).
\]

Thus a positive R3-style midpoint gap in this family would require a positive
quadratic form of the Hessian in a multi-coordinate direction.

## 5. O(n^2) directional derivative interface through the path DP

The Möbius formulas above expose mechanism but cost exponential time.  The
path-sparse \(L\)-ensemble representation gives an \(O(n^2)\) route for values
and, with automatic differentiation, for directional derivatives.

Along a line

\[
\tau_i(t)=\tau_i+t v_i,
\qquad
w_i(t)=1/\tau_i(t),
\]

we have at \(t=0\)

\[
w_i'=-v_i/\tau_i^2,
\qquad
w_i''=2v_i^2/\tau_i^3.
\]

The tridiagonal \(L(t)\) entries are

\[
d_i(t)=w_i(t)+\beta_i^2w_{i+1}(t)-1
\quad(i<n),
\qquad
d_n(t)=w_n(t)-1,
\]

\[
e_i(t)=-\beta_i w_{i+1}(t).
\]

Thus \(d_i,d_i'',e_i,e_i''\) are explicit.  For an interval determinant
\(\kappa(a,b;t)\), the continuant recurrence is

\[
\kappa(a,b)=d_b\kappa(a,b-1)-e_{b-1}^2\kappa(a,b-2).
\]

The first derivative obeys

\[
\kappa'
=d_b'\kappa_1+d_b\kappa_1'
-2e_{b-1}e_{b-1}'\kappa_2
-e_{b-1}^2\kappa_2',
\]

and the second derivative obeys

\[
\kappa''
=d_b''\kappa_1+2d_b'\kappa_1'+d_b\kappa_1''
-2\left((e_{b-1}')^2+e_{b-1}e_{b-1}''\right)\kappa_2
-4e_{b-1}e_{b-1}'\kappa_2'
-e_{b-1}^2\kappa_2''.
\]

Here \(\kappa_1=\kappa(a,b-1)\) and
\(\kappa_2=\kappa(a,b-2)\).

The NS-1 entropy DP uses

\[
Z_m=Z_{m-1}+\sum_{a=1}^m Z_{a-2}\kappa(a,m),
\]

\[
T_m=T_{m-1}
+\sum_{a=1}^m \kappa(a,m)T_{a-2}
+\sum_{a=1}^m Z_{a-2}\kappa(a,m)\log\kappa(a,m).
\]

Replacing every scalar in these recurrences by a second-order jet
\((x,x',x'')\), and using

\[
(xy)'=x'y+xy',
\qquad
(xy)''=x''y+2x'y'+xy'',
\]

\[
(x\log x)'=x'(\log x+1),
\qquad
(x\log x)''=x''(\log x+1)+(x')^2/x,
\]

gives \(Z,Z',Z'',T,T',T''\) in \(O(n^2)\) arithmetic.  Finally,

\[
H=\log Z-T/Z
\]

can be differentiated by ordinary one-variable calculus.  This would give a
scalable exact-direction curvature evaluator without enumerating \(2^n\)
events.

The current `search.py` uses the value DP for finite chord optimization; this
jet interface is the next implementation target if the family remains active.

## 6. Finite search evidence

`search.py` performed deterministic finite scout optimization over
\(n=5,\ldots,30\), using three direction buckets:

- rank one: one \(\tau_i\) changes;
- rank two: two \(\tau_i\)'s change;
- full rank: all \(\tau_i\)'s change.

The run used seed `20260908` and `160` trials per n.  All generated endpoints
were checked for positivity of \(L\) by float tridiagonal LDL pivots before
entropy evaluation.

The search found no positive scout gap above `1e-10`.  The best finite value
was still negative:

```text
best overall: n=30, rank2,
Delta = -1.8402479120993576e-05.
```

This is evidence only.  It does not prove concavity of the family.
