# D10-S5 frozen problem and candidate outcome

Status: **CORRECT_AFTER_FRESH_REVIEW_AND_REVISION_RECHECK**.

This work starts from the M7 equation (19) rational base

\[
K_*=
\begin{pmatrix}
151/280&-6/35&-47/280\\
-6/35&94/175&-29/175\\
-47/280&-29/175&747/1400
\end{pmatrix}.
\]

It is the strict real DPP kernel with spectral data

\[
\theta=(1/5,7/10,71/100)
\]

in the rational projector frame \(U=J/3\), \(V=ww^\top/14\),
\(w=(1,2,-3)\), \(W=I-U-V\).  Thus \(K_*\) has three distinct eigenvalues,
heterogeneous coordinate diagonal, and all off-diagonal entries nonzero.

The original D10-S5 question asks what happens when the direction is enlarged
from M7's fixed-\(Q\) one-sign spectral directions to arbitrary real symmetric
PSD/NSD directions in observation coordinates, including noncommuting
directions.

Use the coordinate vector

\[
x(D)=
(D_{11},D_{22},D_{33},D_{12},D_{13},D_{23}).
\]

For exact-event Shannon entropy \(H\), define the Hessian quadratic form

\[
\mathcal H_{K_*}(D)=H''_{K_*}[D,D].
\]

The candidate outcome proved here is stronger than PSD-cone exclusion:

\[
\mathcal H_{K_*}(D)<0
\quad\text{for every nonzero real symmetric }D.
\]

Equivalently, the \(6\times6\) matrix of \(-\mathcal H_{K_*}\) in the above
coordinates is positive definite.  The proof certificate is a rational
log-interval Gershgorin strict diagonal-dominance certificate with minimum
row margin approximately

\[
1.7200075505038613.
\]

Consequently,

\[
\mathcal H_{K_*}(D)
\le
-m\|x(D)\|_2^2
\le
-\frac{m}{2}\|D\|_F^2
\]

with the exact rational interval lower bound \(m>0\) recorded in
`hessian_scout.json`.

This proves a local Hessian exclusion for arbitrary PSD and NSD directions,
indeed for arbitrary symmetric directions, at \(K_*\).  By continuity, it also
gives an existential open neighborhood of \(K_*\) on which the full Hessian
remains negative definite.  No numerical neighborhood radius is claimed.

The exact optimizer of \(\mathcal H_{K_*}\) over the Frobenius-unit PSD cone is
not solved symbolically here.  The included numerical attack log found no
positive direction and suggests a rank-one PSD maximum near \(-2.2851\), but
that value is scout evidence only.
