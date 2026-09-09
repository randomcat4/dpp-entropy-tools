# Proof II — global concavity for real two-point DPPs

Let

\[
L=\begin{pmatrix}a&c\\c&b\end{pmatrix},\qquad
V=\begin{pmatrix}u&w\\w&v\end{pmatrix},\qquad 0<L<I.
\]

Put `d=ab-c^2` and `q=uv-w^2`. The four complete-event probabilities are

\[
A_0=1-a-b+d,\quad A_1=a-d,\quad A_2=b-d,\quad A_3=d, \tag{1}
\]

all positive, with

\[
A_1A_2-A_0A_3=c^2=:r\ge0. \tag{2}
\]

Along `L+zV`, let `alpha=bu+av-2cw`. The first and second probability derivatives at zero are

\[
x=(-u-v+\alpha,\ u-\alpha,\ v-\alpha,\ \alpha),
\qquad p''=2q(1,-1,-1,1). \tag{3}
\]

Consequently

\[
H''(L)[V,V]=-F+2q\Lambda, \tag{4}
\]

where

\[
F=\sum_{i=0}^3\frac{x_i^2}{A_i},\qquad
\Lambda=\log\frac{A_1A_2}{A_0A_3}\ge0. \tag{5}
\]

If `c=0`, then `r=0`, `A_1A_2=A_0A_3`, hence `Lambda=0` and (4) is `-F<=0`.

Assume `c!=0`. Use the invertible coordinates `y=(u,v,alpha)^T`; then

\[
w=\frac{bu+av-\alpha}{2c},\qquad F=y^TGy,\qquad q=y^TQy, \tag{6}
\]

with

\[
G=\begin{pmatrix}
A_0^{-1}+A_1^{-1}&A_0^{-1}&-A_0^{-1}-A_1^{-1}\\
A_0^{-1}&A_0^{-1}+A_2^{-1}&-A_0^{-1}-A_2^{-1}\\
-A_0^{-1}-A_1^{-1}&-A_0^{-1}-A_2^{-1}&\sum_iA_i^{-1}
\end{pmatrix}, \tag{7}
\]

\[
Q=\begin{pmatrix}0&1/2&0\\1/2&0&0\\0&0&0\end{pmatrix}
 -\frac1{4r}\begin{pmatrix}b\\a\\-1\end{pmatrix}
                    \begin{pmatrix}b&a&-1\end{pmatrix}. \tag{8}
\]

`G` is positive definite because it is the complete four-event Fisher form on the three-dimensional simplex tangent space. Let

\[
P=A_0A_1A_2A_3,\qquad
E=A_0A_3(A_0+A_3)+A_1A_2(A_1+A_2).
\]

Direct expansion using `sum_i A_i=1` gives the exact matrix-pencil identity

\[
\det(G-\lambda Q)=
\frac{16r+4\lambda E-\lambda^3P}{16rP}. \tag{9}
\]

The quadratic coefficient cancels exactly.

Set `X=A_0A_3`, `Y=A_1A_2`; then `r=Y-X>0`, `P=XY`, and `Lambda=log(Y/X)`. Two elementary inequalities close the sign. First,

\[
\sqrt P\,\Lambda\le r. \tag{10}
\]

Indeed, with `z=sqrt(Y/X)>1`, this is `2z log z<=z^2-1`; its difference has derivative `2(z-1-log z)>=0` and vanishes at one. Thus `P\Lambda^2<=r^2`.

Second,

\[
E>4r^2. \tag{11}
\]

Write `p=sqrt X`, `q_0=sqrt Y`, `theta=A_0+A_3`. AM–GM gives `theta>=2p`, `1-theta>=2q_0`, and `p+q_0<=1/2`; hence

\[
E\ge2(p^3+q_0^3).
\]

With `sigma=p+q_0`,

\[
2(p^3+q_0^3)-4(q_0^2-p^2)^2
=2\sigma[p^2-pq_0+q_0^2-2\sigma(q_0-p)^2]
\ge2\sigma pq_0>0,
\]

which proves (11).

For every `0<=lambda<=2Lambda`, (10) implies

\[
\lambda^3P\le\lambda(2\Lambda)^2P\le4\lambda r^2.
\]

Therefore the numerator in (9) is at least

\[
16r+4\lambda(E-r^2)>0. \tag{12}
\]

So `G-lambda Q` never becomes singular on `[0,2Lambda]`. Since it is positive definite at zero, inertia cannot change; thus `G-2Lambda Q` is positive definite. Using (4) and (6),

\[
H''(L)[V,V]=-y^T(G-2\Lambda Q)y<0
\]

for every nonzero `V` when `c!=0`, and `H''<=0` in all cases. Hence the complete-event Shannon entropy of every strict real `2 x 2` DPP is concave along every true affine kernel line. Continuity extends the chord inequality to legal boundary endpoints.