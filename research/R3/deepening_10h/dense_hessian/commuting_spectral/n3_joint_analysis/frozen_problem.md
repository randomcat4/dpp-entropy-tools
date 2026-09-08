# D10-M6 frozen target: n=3 fixed-Q one-sign spectral rates

Author status: **OPEN_TARGET_WITH_SCOUT_EVIDENCE**.

This directory studies the remaining n=3 fixed-eigenvector spectral-rate
problem.  Let

\[
K(t)=Q\operatorname{diag}(\theta_1+t v_1,\theta_2+t v_2,\theta_3+t v_3)Q^\top,
\qquad Q\in O(3),\quad 0<\theta_i<1.
\]

The local strict-feasibility interval is the set of \(t\) for which every
\(\theta_i+t v_i\) lies in \((0,1)\).  Because the Hessian is quadratic in
\(v\), PSD and NSD one-sign spectral-rate directions are equivalent after
replacing \(v\) by \(-v\).  I therefore write \(v_i\ge0\).

The imported, already-checked n=3 reduction is

\[
H(Y_t)=H(|Y_t|)+G_P(r(t))+G_P(s(t)),\qquad P_{ai}=q_{ai}^2,
\]

where

\[
r_i=\theta_i\prod_{j\ne i}(1-\theta_j),
\qquad
s_i=(1-\theta_i)\prod_{j\ne i}\theta_j,
\]

and

\[
G_P(x)=-\sum_a (Px)_a\log\frac{(Px)_a}{\sum_i x_i}.
\]

The D10-M6 question is whether the singleton and pair conditional channel terms
jointly satisfy

\[
\frac{d^2}{dt^2}\{G_P(r(t))+G_P(s(t))\}\le -H(|Y_t|)'',
\]

or at least a strong enough variant to prove \(H(Y_t)''\le0\) for all
\(Q,\theta,v\ge0\).

No positive \(H''\) candidate is frozen in this directory.
