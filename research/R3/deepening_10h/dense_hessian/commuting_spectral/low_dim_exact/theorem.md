# Low-dimensional fixed-eigenvector PSD spectral rates

AUTHOR STATUS: N2_PROVED, N3_BLOCKER_IDENTIFIED, pending non-author verification.

## Theorem: n=2 has no positive PSD spectral-rate curvature

Let \(0<\lambda_1,\lambda_2<1\), let \(Q\in O(2)\), and define

\[
K(t)=Q\operatorname{diag}(\lambda_1+tv_1,\lambda_2+tv_2)Q^T,
\]

where \(v_1,v_2\ge0\), not both zero.  For all sufficiently small \(t\),
\(K(t)\) is a strict DPP kernel.  Let \(H(t)\) be the exact-event Shannon
entropy of this DPP, with natural logarithms.  Then

\[
H''(0)<0.
\]

In particular, in dimension two, a fixed-eigenvector PSD spectral-rate
direction cannot produce a positive local R3 midpoint gap.

## Exact-event atoms

Write \(x=Q_{11}^2\in[0,1]\).  Since changing signs of eigenvectors does not
change principal minors, the four exact atoms are

\[
p_\emptyset=(1-\lambda_1)(1-\lambda_2),
\qquad
p_{12}=\lambda_1\lambda_2,
\]

\[
p_1=x\lambda_1(1-\lambda_2)+(1-x)\lambda_2(1-\lambda_1),
\]

\[
p_2=(1-x)\lambda_1(1-\lambda_2)+x\lambda_2(1-\lambda_1).
\]

These are exact-event probabilities, not inclusion probabilities.  Indeed,
for a two-point DPP,

\[
p_{12}=\det K,\qquad
p_1=K_{11}-\det K,\qquad
p_2=K_{22}-\det K,
\]

\[
p_\emptyset=1-K_{11}-K_{22}+\det K=\det(I-K).
\]

Substituting \(K=Q\operatorname{diag}(\lambda_1,\lambda_2)Q^T\) gives the
displayed formulas.

## Entropy split

Let

\[
r=\lambda_1(1-\lambda_2),\qquad q=\lambda_2(1-\lambda_1),
\qquad s=r+q.
\]

Let \(N=|Y|\).  Then

\[
\mathbb P(N=0)=p_\emptyset,\qquad
\mathbb P(N=1)=s,\qquad
\mathbb P(N=2)=p_{12}.
\]

The full four-atom entropy decomposes as

\[
H(Y)=H(N)+\Phi(p_1,p_2),
\]

where

\[
\Phi(u,w)=-u\log\frac{u}{u+w}-w\log\frac{w}{u+w}.
\]

Thus it is enough to prove that both terms are concave along every
\((v_1,v_2)\ge0\), and that \(H(N)\) is strictly concave for every nonzero such
direction.

## Count entropy is strictly concave

Set \(a=p_\emptyset\), \(b=p_{12}\).  Along
\(\lambda_i(t)=\lambda_i+tv_i\),

\[
a''=2v_1v_2,\qquad b''=2v_1v_2,\qquad s''=-4v_1v_2.
\]

If \(v_1v_2=0\), then the count probabilities are affine and nonconstant, so

\[
H(N)''=-\sum_{k=0}^2\frac{(p_k')^2}{p_k}<0.
\]

Now assume \(v_1v_2>0\).  Direct differentiation gives

\[
H(N)''
=-F_N+2v_1v_2\log\frac{s^2}{ab},
\]

where

\[
F_N=
\frac{\left(v_1(1-\lambda_2)+v_2(1-\lambda_1)\right)^2}{a}
+\frac{\left(v_1(1-2\lambda_2)+v_2(1-2\lambda_1)\right)^2}{s}
+\frac{\left(v_1\lambda_2+v_2\lambda_1\right)^2}{b}.
\]

Discarding the middle nonnegative term and dividing by \(v_1v_2\), AM-GM gives

\[
\frac{F_N}{v_1v_2}
\ge
2X+4,
\qquad
X=\frac{s}{\sqrt{ab}}.
\]

The identity \(ab=rq\) and \(s=r+q\) gives \(X\ge2\).  Since

\[
X+2-2\log X>0\qquad(X>0),
\]

we have

\[
F_N>4v_1v_2\log X
=2v_1v_2\log\frac{s^2}{ab}.
\]

Therefore \(H(N)''<0\).

## Singleton split is concave

For \(\Phi(u,w)\),

\[
\nabla\Phi(u,w)=
\left(\log\frac{u+w}{u},\log\frac{u+w}{w}\right),
\]

which is coordinatewise nonnegative for \(u,w>0\), and

\[
\nabla^2\Phi=
\frac1{u+w}
\begin{pmatrix}
-w/u & 1\\
1 & -u/w
\end{pmatrix}
\preceq0.
\]

Along the spectral-rate line,

\[
p_1''=p_2''=-2v_1v_2\le0.
\]

Hence

\[
\frac{d^2}{dt^2}\Phi(p_1(t),p_2(t))
=
\begin{pmatrix}p_1'&p_2'\end{pmatrix}
\nabla^2\Phi
\begin{pmatrix}p_1'\\p_2'\end{pmatrix}
+\Phi_u p_1''+\Phi_w p_2''
\le0.
\]

Combining this with \(H(N)''<0\) proves \(H''(0)<0\).

## Boundaries

- The result is local in \(t\): endpoints must keep
  \(0<\lambda_i+tv_i<1\).
- The direction is PSD because \(D=Q\operatorname{diag}(v_i)Q^T\succeq0\).
- Rank-one cases \(v_1v_2=0\) are included, but they are already covered by
  the rank-one prior-art blocker recorded elsewhere.
- This theorem is dimension two only.  It does not imply the same statement in
  dimension three or higher.
