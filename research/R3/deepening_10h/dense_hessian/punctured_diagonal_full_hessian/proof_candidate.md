# Full-Hessian negativity in punctured dense cones near the diagonal ridge

AUTHOR STATUS: PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW.

## 1. Local coordinates and the verified fourth-order input

Write a symmetric kernel near the diagonal as `K(x,z)`, where `x` contains
the diagonal entries and `z=(K_ij)_{i<j}` contains each off-diagonal entry
once.  Let

\[
F(x,z)=H(K(x,z)).
\]

All exact atoms are positive at `(x,0)` and are polynomial in `(x,z)`, so F
is real analytic in a neighborhood of every strict diagonal point.

The verified D10-U2 result says, for every fixed strict x and every
zero-diagonal direction Z,

\[
D_zF(x,0)[Z]=D_z^2F(x,0)[Z,Z]=D_z^3F(x,0)[Z,Z,Z]=0,
\tag{1}
\]

and

\[
D_z^4F(x,0)[Z,Z,Z,Z]
=-12\sum_{i<j}
\frac{Z_{ij}^4}{x_i(1-x_i)x_j(1-x_j)}.
\tag{2}
\]

Polarization of the symmetric derivative tensors implies that all pure z
derivatives of orders one through three vanish.  Since this holds identically
for every x in the strict diagonal domain, every x derivative of those zero
tensors also vanishes.  Thus Taylor expansion in z, with x kept as a smooth
parameter, is

\[
F(x,z)=F(x,0)-\frac12\sum_{i<j}c_{ij}(x)z_{ij}^4+R(x,z),
\qquad
c_{ij}(x)=\frac1{x_i(1-x_i)x_j(1-x_j)},
\tag{3}
\]

where, locally uniformly in x,

\[
R_{xx}=O(\|z\|^5),\qquad
R_{xz}=O(\|z\|^4),\qquad
R_{zz}=O(\|z\|^3).
\tag{4}
\]

The weaker orders `O(z^4),O(z^3),O(z^3)` would already suffice; (4) follows
by differentiating a fifth-order analytic remainder with x as parameter.

## 2. Hessian block asymptotics

At z=0 the diagonal-coordinate entropy is the product-Bernoulli entropy, so

\[
F_{xx}(x,0)=-\operatorname{diag}
\left(\frac1{x_i(1-x_i)}\right)=:-C(x),
\qquad C(x)\succ0.
\tag{5}

Fix a zero-diagonal A with every edge nonzero and substitute z=epsilon a,
where `a=(A_ij)`.  Differentiating (3) gives the block matrix

\[
\nabla^2F(x,\epsilon a)=
\begin{pmatrix}
-C(x)+O(\epsilon^4)&O(\epsilon^3)\\
O(\epsilon^3)&
-6\epsilon^2\operatorname{diag}
\bigl(c_{ij}(x)a_{ij}^2\bigr)+O(|\epsilon|^3)
\end{pmatrix}.
\tag{6}
\]

The lower-right leading matrix is negative definite because every
`a_ij!=0`.  Notice that the mixed block is order epsilon cubed, not order
epsilon: the identities in (1) hold for every x and remove every term with at
most three z factors below the quartic term.

For sufficiently small nonzero epsilon, the upper-left block remains
negative definite.  Its negative Schur complement has lower-right leading
part

\[
-6\epsilon^2\operatorname{diag}(c_{ij}a_{ij}^2)
+O(|\epsilon|^3)+O(\epsilon^6),
\tag{7}
\]

where the last term is the mixed-block correction.  The order-epsilon-squared
strict negative diagonal therefore dominates, proving the whole Hessian is
negative definite.

Because `X` is strictly between zero and I, `X+epsilon A` is also strict for
all sufficiently small epsilon.  This proves the pointwise statement for both
signs of epsilon.

## 3. Open neighborhoods and the uniform compact form

At each fixed nonzero sufficiently small epsilon, the maximum eigenvalue of
the finite Hessian matrix is strictly negative.  Exact atoms and Hessian
entries are continuous on the strict kernel domain, so the maximum eigenvalue
remains negative on an open neighborhood of `K_epsilon`.  This is simultaneous
over all real symmetric directions, not a direction-by-direction radius.

For the uniform version, fix `x_i in [a,b] subset (0,1)`, `||A||_F=1`, and
`min_{i<j}|A_ij|>=eta>0`.  The x/A parameter set is compact.  The matrices
C(x) have a common positive lower bound, and
`c_ij(x)A_ij^2` have a common positive lower bound.  The Taylor remainder
constants in (4) are uniform after restricting to one common analytic
neighborhood.  The same block/Schur argument therefore supplies a single
epsilon_0 depending only on `n,a,b,eta`.

## 4. Exact scope

The proof needs full off-diagonal support.  If an edge A_ij vanishes, the
quartic leading Hessian in that edge coordinate has a zero entry and higher
orders/cycle structure must decide its sign.  No conclusion for such sparse
directions is claimed.

The diagonal point itself remains Hessian-degenerate in every off-diagonal
direction.  The result says that a dense punctured cone on either side is
full-Hessian negative, and each of its points is surrounded by an ordinary
open negative-definite region.  It is a local arbitrary-direction theorem,
not global entropy concavity.

