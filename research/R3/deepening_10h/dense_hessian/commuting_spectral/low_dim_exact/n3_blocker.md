# n=3 minimal obstruction after the n=2 proof

AUTHOR STATUS: BLOCKER_IDENTIFIED, not a counterexample.

For fixed eigenvectors in dimension three,

\[
K=Q\operatorname{diag}(\lambda_1,\lambda_2,\lambda_3)Q^T,
\qquad
D=Q\operatorname{diag}(v_1,v_2,v_3)Q^T,\quad v_i\ge0.
\]

The exact-event spectral expansion is

\[
p_Y(\lambda)=
\sum_{\substack{J\subseteq\{1,2,3\}\\ |J|=|Y|}}
\left(\prod_{j\in J}\lambda_j\prod_{j\notin J}(1-\lambda_j)\right)
\det(Q_{Y,J})^2.
\]

For singleton atoms \(Y=\{i\}\), this becomes

\[
p_i=\sum_{a=1}^3 q_{ia}^2\lambda_a
\prod_{b\ne a}(1-\lambda_b).
\]

Along \(\lambda(t)=\lambda+tv\),

\[
p_i''
=2\sum_{a=1}^3 q_{ia}^2
\left[
\lambda_a v_bv_c
-v_av_b(1-\lambda_c)
-v_av_c(1-\lambda_b)
\right],
\]

where \(\{a,b,c\}=\{1,2,3\}\).

Unlike the n=2 singleton split, these second derivatives do not have a fixed
sign even when \(v_i\ge0\).  Thus the n=2 proof cannot be lifted by simply
claiming that every within-layer atom is concave and then applying monotone
perspective entropy.

## Exact rational obstruction example

Take the rational orthogonal Householder matrix

\[
Q=I-\frac{1}{7}
\begin{pmatrix}1\\2\\3\end{pmatrix}
\begin{pmatrix}1&2&3\end{pmatrix}
=
\begin{pmatrix}
6/7&-2/7&-3/7\\
-2/7&3/7&-6/7\\
-3/7&-6/7&-2/7
\end{pmatrix}.
\]

Let

\[
\lambda=(3/4,1/2,1/2),\qquad
v=(1/100,1,1).
\]

The three eigen-column contributions in the bracket above are

\[
\left(37/25,\,-1/2,\,-1/2\right).
\]

For the first singleton atom this gives

\[
p_{\{1\}}''
=\frac{36}{49}\frac{37}{25}
+\frac{4}{49}\left(-\frac12\right)
+\frac{9}{49}\left(-\frac12\right)
=\frac{2339}{2450}>0.
\]

This is not a positive entropy-curvature example.  It is only the smallest
structural blocker found here: the n=2 concavity proof relies on
\(p_1''=p_2''\le0\) inside the singleton split, and that sign property already
fails in n=3.

The next n=3 step should control layer entropy by a different mechanism or
construct a true \(H''>0\) candidate with exact-event and feasibility
certificates.
