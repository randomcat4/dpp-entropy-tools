# D10-M6 fixed-base cone reductions

Author status: **CERTIFICATE_REDUCTION_CANDIDATE_PENDING_FRESH_REVIEW**.

For fixed strict \(\theta\) and fixed \(Q\), the second derivative

\[
v\mapsto H(Y_t)''
\]

is a homogeneous quadratic form in \(v\).  Write it as

\[
H(Y_t)''=v^\top M(\theta,Q)v.
\]

Consequently, n=3 one-sign spectral concavity at this base point is equivalent
to

\[
v^\top M(\theta,Q)v\le0\qquad\text{for every }v\in\mathbb R_+^3.
\]

Equivalently, \(C=-M\) is copositive on the nonnegative orthant.

## 3x3 copositivity check

For a real symmetric \(3\times3\) matrix \(C\), the classical 3x3 copositivity
criterion gives a finite check:

\[
c_{ii}\ge0,
\]

\[
\bar c_{ij}=c_{ij}+\sqrt{c_{ii}c_{jj}}\ge0\qquad(i<j),
\]

and

\[
\kappa(C)=
\sqrt{c_{11}c_{22}c_{33}}
+c_{12}\sqrt{c_{33}}
+c_{13}\sqrt{c_{22}}
+c_{23}\sqrt{c_{11}}
+\sqrt{2\bar c_{12}\bar c_{13}\bar c_{23}}
\ge0.
\]

Thus, after reconstructing \(M\), this is a pointwise exact algebraic target
for that base point.  The scan in `joint_copositive_probe.py` uses this as a
numerical consistency check, while also directly maximizing the same quadratic
on the positive simplex.

## Positive-simplex maximization

Because the quadratic form is homogeneous, the existence of \(v\ge0\) with
\(v^\top Mv>0\) is equivalent to a positive maximum over

\[
\Delta_2=\{v\ge0:\sum_i v_i=1\}.
\]

In dimension three, a nondegenerate quadratic maximum over \(\Delta_2\) occurs
either at a vertex, on an edge stationary point, or at a full-support
stationary point satisfying

\[
M_Iv_I=\lambda{\bf1},\qquad \sum_{i\in I}v_i=1,
\]

for some nonempty support \(I\).  The first version of
`joint_copositive_probe.py` skipped singular full-support KKT systems, so its
reported simplex maxima are kept only as deprecated scout data.  The repaired
v3 version solves the augmented KKT equations on every face with scale-aware
residual checks and includes regression checks for

\[
M=
\begin{pmatrix}
-2&1&1\\
1&-2&1\\
1&1&-2
\end{pmatrix},
\]

whose positive-simplex maximum is \(0\) at \(v=(1/3,1/3,1/3)\).  Even after
this repair, the simplex routine is still a floating-point scout, not a formal
optimizer for every degenerate symbolic \(3\times3\) matrix.  The v3 regression
also includes the scaled positive matrix
\[
10^{14}
\begin{pmatrix}
-10&6&6\\
6&-10&6\\
6&6&-10
\end{pmatrix},
\]
whose positive-simplex maximum is \(2\cdot10^{14}/3\).

## Positive-sphere support eigenvectors

The parent instance suggested an additional, more geometric candidate generator:
maximize \(v^\top Mv\) over

\[
v\ge0,\qquad \|v\|_2=1.
\]

For each nonempty support \(I\), an interior extremum on that support must be
an eigenvector of \(M_{I,I}\).  The script `sphere_support_probe.py` enumerates
same-sign eigenvectors of every principal submatrix and includes all boundary
supports.  This removes random sampling over \(v\) and gives unit-norm
directions useful for mechanism comparison.

For a full KKT local maximum on the orthant sphere, if \(j\notin I\) is an
omitted coordinate then the omitted-gradient condition is

\[
(Mv)_j\le0.
\]

The script records these omitted gradients for the best observed support
candidate.  For mere sign detection, however, filtering by this condition is
not necessary: any enumerated nonnegative direction with \(v^\top Mv>0\) would
already be a valid one-sign positive-curvature direction.

## What this reduction does and does not prove

The copositivity and support-eigenvector reductions are exact mathematical
targets for a fixed base point once \(M\) is known.  The present implementations
are floating-point scouts.  They do not prove the theorem over the continuous
domain of all strict \(\theta\) and all orthogonal \(Q\).  A theorem would still
need either:

1. symbolic/interval proof that \(C(\theta,Q)=-M(\theta,Q)\) satisfies the 3x3
   copositivity inequalities everywhere on the orthostochastic domain; or
2. a rigorously certified base point with \(v^\top Mv>0\), followed by strict
   feasible-chord and exact-event entropy checks.
