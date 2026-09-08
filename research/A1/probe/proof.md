# Exact conditional-acceleration obstruction

Status: PROVED as an author result for the owner's frozen
`frozen_acceleration_obstruction_v1.md`; pending independent review.
The original full-entropy existential target remains INCOMPLETE.

## Exact object and feasibility

Take

\[
K=\begin{pmatrix}1/4&1/10&1/10\\1/10&3/4&1/1000\\1/10&1/1000&1/2\end{pmatrix},
\quad b=(1/10,1/1000)^T,\quad c=1/2,\quad w=(0,1)^T.
\]

All three edges are nonzero. The leading principal minors of K are
`1/4, 71/400, 325079/4000000`; those of I-K are
`3/4, 71/400, 344917/4000000`. Sylvester's criterion gives 0<K<I.
Writing A for its upper two-by-two block, the exact conditional kernels are

\[
C_0=\begin{pmatrix}27/100&501/5000\\501/5000&375001/500000\end{pmatrix},
\quad
C_1=\begin{pmatrix}23/100&499/5000\\499/5000&374999/500000\end{pmatrix}.
\]

The first leading minors of C0, I-C0, C1, I-C1 are respectively
27/100, 73/100, 23/100, 77/100. Their determinants are respectively
384921/2000000, 344917/2000000, 325079/2000000, 365083/2000000.
Thus both conditional kernels are strict contractions.

## Exact entropy derivative and sign certificate

For a two-point kernel [[u,r],[r,v]], the four full event probabilities in
order empty, {1}, {2}, {1,2} are

    1-u-v+uv-r^2, u-uv+r^2, v-uv+r^2, uv-r^2.

Let f be their Shannon entropy. Differentiating at fixed u,r gives

\[
D f(C)[ww^T]=(1-u)\log(p_{00}/p_{01})+u\log(p_{10}/p_{11}).
\]

For C0 their numerators over 2000000 are
`344917, 155079, 1115083, 384921`; for C1 they are
`365083, 134921, 1174917, 325079`. Therefore

\[
R=2\left[
\frac{73}{100}\log\frac{344917}{1115083}
+\frac{27}{100}\log\frac{155079}{384921}
-\frac{77}{100}\log\frac{365083}{1174917}
-\frac{23}{100}\log\frac{134921}{325079}\right].
\]

The certificate uses only rational arithmetic for the sign. For rational
q>0, write q=2^k r with 1<=r<=2, and put z=(r-1)/(r+1). For N=256,

\[
S_N(r)=2\sum_{j=0}^{N-1}\frac{z^{2j+1}}{2j+1},\qquad
0\le\log r-S_N(r)\le
\frac{2z^{2N+1}}{(2N+1)(1-z^2)}.
\]

This follows by integrating the geometric series for 2/(1-z^2), or
bounding its nonnegative tail termwise. Apply the same bounds to log 2;
multiply interval endpoints in reversed order when k or a coefficient is
negative. The certificate computes exact Fraction endpoints throughout.
The displayed decimal values in JSON are informational and are not the
certificate. A coarser outward rational enclosure is

\[
\frac{229172119980517}{500000000000000000}
\ \le R\le\
\frac{91668847992207}{200000000000000000}.
\]

The left endpoint is strictly positive. This proves the second frozen claim.
`conditional.py` implements the formula and saves these outer rational bounds
in `conditional.json` (certificate index 1).

## Why this is exactly the acceleration term

Along K(t) with b(t)=b+tw and fixed A,c, conditional kernels are

\[
C_1(t)=A-b(t)b(t)^T/c,\qquad
C_0(t)=A+b(t)b(t)^T/(1-c).
\]

These conditional DPP laws follow directly by dividing the joint inclusion
minors by c for inclusion of point 3, and using exclusion for its complement;
equivalently the rank-one determinant identity gives the same conditional
inclusion minors. Their full-event laws follow by finite inclusion-exclusion.
The ordinary entropy chain rule consequently gives

\[
H(K(t))=h(c)+c f(C_1(t))+(1-c)f(C_0(t)).
\]

All derivatives are legitimate near zero by strict feasibility and positive
event probabilities. Let T=bw^T+wb^T. Then

\[
C_1'=-T/c,\quad C_0'=T/(1-c),\quad
C_1''=-2ww^T/c,\quad C_0''=2ww^T/(1-c).
\]

Differentiating twice, the sum of the gradient-times-acceleration terms is

\[
c Df(C_1)[C_1'']+(1-c)Df(C_0)[C_0'']
=2(Df(C_0)[ww^T]-Df(C_1)[ww^T])=R>0.
\]

The remaining terms are
`c D²f(C1)[C1',C1'] + (1-c) D²f(C0)[C0',C0']`.
They are not discarded. In fact, an independent full eight-event derivative
calculation in the same certificate gives the total second derivative in
the rigorous interval

\[
[-32529701732259701/500000000000000000,
 -65059403464519401/1000000000000000000],
\]

which is strictly negative. Thus this exact object refutes the blanket
nonpositivity assertion for the acceleration contribution, not entropy
concavity. The new inequality still needed by a conditioning proof is that
the weighted negative conditional-Hessian terms dominate this positive term;
that remaining inequality is not proved here.

## Scope

No frozen premise was modified. No finite chord counterexample, general
three-point concavity proof, or novelty claim is asserted. The exact proof
above is self-contained apart from elementary entropy differentiation,
Sylvester's criterion, and the finite entropy chain rule.
