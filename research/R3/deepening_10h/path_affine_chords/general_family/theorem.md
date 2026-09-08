# General fixed-beta innovation family

AUTHOR STATUS: PROVED, pending independent verification.  This file is an
author/generalizer theorem note, not a fresh `CORRECT` certificate.

## Theorem

Fix an integer \(n\ge 2\) and nonzero real parameters

\[
\beta=(\beta_1,\ldots,\beta_{n-1})\in(\mathbb R\setminus\{0\})^{n-1}.
\]

Let \(R=R_\beta\) be the unit lower-bidiagonal matrix

\[
R_{ii}=1,\qquad R_{i+1,i}=-\beta_i,
\]

with all other off-band entries zero.  For \(\tau\in(0,\infty)^n\), define

\[
S(\tau)=R^{-1}\operatorname{diag}(\tau_1,\ldots,\tau_n)R^{-T}.
\]

Let

\[
\Omega_\beta=\{\tau\in(0,\infty)^n:S(\tau)\prec I\}.
\]

For every \(\tau\in\Omega_\beta\), define

\[
P(\tau)=S(\tau)^{-1}=R^T\operatorname{diag}(\tau_1^{-1},\ldots,\tau_n^{-1})R,
\]

\[
L(\tau)=P(\tau)-I,
\qquad
K(\tau)=\Phi(L(\tau))=L(\tau)(I+L(\tau))^{-1}.
\]

Then:

1. \(S(\tau)\) is symmetric positive definite and \(0\prec S(\tau)\prec I\).
2. \(L(\tau)\) is symmetric positive definite.
3. \(K(\tau)\) is a strict real DPP marginal kernel and
   \[
   K(\tau)=I-S(\tau).
   \]
4. \(L(\tau)\) is tridiagonal, with entries
   \[
   L_{ii}(\tau)=\tau_i^{-1}+\beta_i^2\tau_{i+1}^{-1}-1
   \quad(1\le i<n),
   \]
   \[
   L_{nn}(\tau)=\tau_n^{-1}-1,
   \]
   and
   \[
   L_{i,i+1}(\tau)=L_{i+1,i}(\tau)=-\beta_i\tau_{i+1}^{-1}.
   \]
5. Since every \(\beta_i\ne0\), every adjacent edge of \(L(\tau)\) is nonzero;
   the path is connected.
6. If the displayed diagonal entries are not all equal, then \(L(\tau)\) is
   heterogeneous in the FT-B sense.
7. \(\Omega_\beta\) is an open convex nonempty subset of \((0,\infty)^n\).
8. For any \(\tau^-,\tau^+\in\Omega_\beta\) and \(t\in[0,1]\),
   \[
   \tau^t=(1-t)\tau^-+t\tau^+\in\Omega_\beta
   \]
   and
   \[
   K(\tau^t)=(1-t)K(\tau^-)+tK(\tau^+).
   \]
   In particular, at \(t=1/2\),
   \[
   \Phi(L(\tau^0))=\frac{\Phi(L(\tau^-))+\Phi(L(\tau^+))}{2}
   \]
   with \(\tau^0=(\tau^-+\tau^+)/2\).
9. The perturbation rank is exact:
   \[
   \operatorname{rank}(K(\tau^+)-K(\tau^-))
   =
   \#\{i:\tau_i^+\ne\tau_i^-\}.
   \]
   Hence a generic chord in this family is full-rank; it is rank one exactly
   when only one innovation variance changes.

## Proof

For \(\tau_i>0\), the diagonal matrix \(D_\tau=\operatorname{diag}(\tau_i)\)
is positive definite.  Since \(R\) is unit triangular, it is invertible.
Therefore

\[
S(\tau)=R^{-1}D_\tau R^{-T}
\]

is symmetric positive definite.

The map \(\tau\mapsto S(\tau)\) is linear because

\[
S(\tau)=\sum_{i=1}^n \tau_i u_i u_i^T,
\]

where \(u_i\) is the \(i\)-th column of \(R^{-1}\).  Thus
\(\Omega_\beta\) is the intersection of the positive orthant with the open
Loewner condition \(S(\tau)\prec I\).  It is open and convex.  It is nonempty
because \(S(\varepsilon\mathbf 1)=\varepsilon R^{-1}R^{-T}\prec I\) for every
sufficiently small positive \(\varepsilon\).

For \(\tau\in\Omega_\beta\), \(0\prec S(\tau)\prec I\).  Inverting reverses
the Loewner order, so

\[
P(\tau)=S(\tau)^{-1}\succ I.
\]

Therefore \(L(\tau)=P(\tau)-I\succ0\).  Since

\[
I+L(\tau)=P(\tau),
\]

we have

\[
\Phi(L(\tau))
=L(\tau)(I+L(\tau))^{-1}
=(P(\tau)-I)P(\tau)^{-1}
=I-S(\tau).
\]

It follows immediately that \(0\prec K(\tau)\prec I\): equivalently,
\(K(\tau)=I-S(\tau)\succ0\) and \(I-K(\tau)=S(\tau)\succ0\).

The inverse formula

\[
P(\tau)=R^T D_\tau^{-1} R
\]

shows that \(P(\tau)\), hence \(L(\tau)\), is tridiagonal.  Multiplying the
unit lower-bidiagonal factors gives the displayed diagonal and edge formulas.
The edge formula is nonzero exactly because each \(\beta_i\ne0\).

For any \(\tau^-,\tau^+\in\Omega_\beta\), convexity gives
\(\tau^t\in\Omega_\beta\).  By linearity of \(S\),

\[
S(\tau^t)=(1-t)S(\tau^-)+tS(\tau^+).
\]

Using \(K=I-S\),

\[
K(\tau^t)
=I-S(\tau^t)
=(1-t)(I-S(\tau^-))+t(I-S(\tau^+))
=(1-t)K(\tau^-)+tK(\tau^+).
\]

Finally,

\[
K(\tau^+)-K(\tau^-)
=-\left(S(\tau^+)-S(\tau^-)\right)
=-R^{-1}\operatorname{diag}(\tau^+-\tau^-)R^{-T}.
\]

Left and right multiplication by invertible matrices preserves rank, so the
rank is the number of nonzero coordinates of \(\tau^+-\tau^-\).

This proves the theorem.

## Corollary: rational FT-B triples exist in every dimension

For every \(n\ge2\), there are rational data giving an FT-B triple whose
K-perturbation has rank \(n\).

One explicit template is

\[
\beta_i=1/2,\qquad
u_i=i+1,\qquad
v_i=2i+1
\]

for \(1\le i\le n\).  Let

\[
\tau^-=\varepsilon u,\qquad
\tau^+=\varepsilon v,\qquad
\tau^0=\frac{\tau^-+\tau^+}{2}.
\]

For the three unscaled positive templates \(u,v,(u+v)/2\), form

\[
S(w)=R^{-1}\operatorname{diag}(w)R^{-T}.
\]

Let \(M\) be any rational number larger than the maximum absolute row-sum norm
of these three matrices.  Since

\[
\lambda_{\max}(S(w))\le \|S(w)\|_\infty^{\mathrm{abs}}<M,
\]

any rational \(0<\varepsilon<1/M\) gives

\[
S(\varepsilon w)=\varepsilon S(w)\prec I
\]

for all three templates.  Thus all three points lie in \(\Omega_\beta\).

The chord has rank \(n\) because

\[
\tau^+_i-\tau^-_i=\varepsilon i\ne0
\]

for every \(i\).  The path is connected because every \(\beta_i=1/2\ne0\).

The diagonal heterogeneity is also explicit.  Before subtracting \(I\), the
first and last diagonal entries for template \(u\) are

\[
1/u_1+\frac{1}{4u_2}=\frac12+\frac1{12}=\frac7{12},
\qquad
1/u_n=\frac1{n+1},
\]

which are unequal for \(n\ge2\).  The same comparison works for
\(v_i=2i+1\):

\[
1/v_1+\frac{1}{4v_2}=\frac13+\frac1{20}=\frac{23}{60},
\qquad
1/v_n=\frac1{2n+1}.
\]

For the midpoint template \(m_i=(u_i+v_i)/2=(3i+2)/2\), the first and last
entries are

\[
1/m_1+\frac{1}{4m_2}=\frac25+\frac1{16}=\frac{37}{80},
\qquad
1/m_n=\frac{2}{3n+2},
\]

again unequal for \(n\ge2\).  Scaling by \(1/\varepsilon\) and subtracting
one from every diagonal entry preserves inequality.  Hence the three
\(L\)-matrices are heterogeneous.

This gives a completely rational arbitrary-dimensional FT-B existence family.

## Rational exactness

If \(\beta\) and \(\tau\) are rational, then \(R\), \(S(\tau)\), \(P(\tau)\),
\(L(\tau)\), and \(K(\tau)\) have rational entries.  Exact certificates can
therefore be checked with fraction arithmetic:

- \(L(\tau)\succ0\) by tridiagonal leading continuants;
- \(K\)-midpoint equality by exact matrix equality;
- perturbation rank by exact row reduction;
- direct event semantics for \(n\le8\) by Möbius inversion.

## Relation to the rank-one blocker

The parent task records Gu's Theorem 7 / Corollary 6 as a prior-art blocker:
rank-one \(K\)-space directions and chords from \(0\) to \(K\) are concavity
directions.  In this family,

\[
\partial_{\tau_i}K=-u_i u_i^T
\]

is rank one, so single-coordinate \(\tau_i\) searches are blocked by that
result.  Multi-coordinate chords have rank equal to the support size of
\(\tau^+-\tau^-\), and are the only meaningful place to look for a positive
gap inside this family.

The theorem above does not reprove Gu's theorem and does not claim a positive
entropy gap.
