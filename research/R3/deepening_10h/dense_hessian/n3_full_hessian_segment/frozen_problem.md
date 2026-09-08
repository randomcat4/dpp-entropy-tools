# D10-S8 frozen problem

AUTHOR STATUS: PROOF_CANDIDATE_PENDING_FRESH_REVIEW.

## Object

Work in observation coordinates for real symmetric `3 x 3` DPP marginal
kernels.  Let

\[
U=\frac13\mathbf 1\mathbf 1^\top,\qquad
w=(1,2,-3)^\top,\qquad V=\frac{ww^\top}{14},\qquad W=I-U-V .
\]

These are rational orthogonal rank-one projectors.  Define the M8 Section 5
line

\[
K(t)=K_0+tR,
\]

where

\[
K_0=\frac15U+\frac12V+\frac45W,\qquad
R=\frac15U+\frac13V+\frac23W .
\]

Equivalently,

\[
K_0=
\begin{pmatrix}
81/140&-17/70&-19/140\\
-17/70&18/35&-1/14\\
-19/140&-1/14&57/140
\end{pmatrix},
\]

\[
R=
\begin{pmatrix}
307/630&-64/315&-53/630\\
-64/315&131/315&-4/315\\
-53/630&-4/315&187/630
\end{pmatrix}.
\]

The spectral coordinates are

\[
\theta(t)=\left(\frac15+\frac t5,\frac12+\frac t3,\frac45+\frac{2t}3\right).
\]

## Candidate theorem

For every

\[
t\in[-6/25,6/25],
\]

the kernel `K(t)` is a strict real DPP kernel with connected observation graph,
heterogeneous diagonal, and distinct spectrum.  Moreover the exact-event
Shannon entropy Hessian in the full observation-coordinate space
`\mathrm{Sym}(3)` is strictly negative definite:

\[
D^2H(K(t))[E,E]<0
\]

for every nonzero real symmetric `E`.

This is stronger than a PSD/NSD-only statement on this line: it covers arbitrary
noncommuting symmetric directions.  It is not a global theorem for all
`3 x 3` kernels, nor a theorem near every point of the M8 product region.

## Success certificate

A valid proof must cover the continuous interval, not a finite grid.  The
accepted certificate route is:

1. derive exact atom jets from
   \[
   p_S(K)=(-1)^{|S^c|}\det(K-I_{S^c});
   \]
2. express the `6 x 6` matrix \(B(t)=-D^2H(K(t))\) in the coordinate order
   `(11,22,33,12,13,23)`;
3. cover the interval by rational subintervals;
4. on each subinterval, use rational interval arithmetic and rigorous natural
   logarithm intervals;
5. certify strict positive definiteness of \(B(t)\) by Gershgorin diagonal
   dominance.

The current script certifies `|t|<=6/25`; attempts at `49/200` and `1/4`
remain certificate failures for this Gershgorin method, not counterexamples.
