# D10-U frozen claim: the apparent flat ridge at the uniform kernel

Status: `PROVED` by the author, awaiting fresh non-author verification.

Let (D=D^T\in\mathbb R^{n\times n}) and

\[
K(t)=\tfrac12 I+tD,
\]

for (t) in the strict-feasibility interval (0<K(t)<I).  Let (H(K))
denote the natural-log Shannon entropy of the full exact DPP subset law.

The frozen claims are:

1. The Hessian at the uniform kernel is
   \[
   H''(\tfrac12 I)[D,D]=-4\sum_i D_{ii}^2.
   \]
   Hence its nullspace is exactly the set of symmetric directions with zero
   diagonal.
2. If `diag(D)=0`, then
   \[
   H(\tfrac12 I+tD)
   =n\log 2-8t^4\sum_{i<j}D_{ij}^4+O(t^6).
   \]
   Thus every nonzero Hessian-null direction is a strict quartic descent
   direction, not a positive-curvature direction hidden by rounding.
3. Along every fixed nonzero zero-diagonal direction, there is a punctured
   interval around zero on which the radial curvature is strictly negative:
   \[
   \frac{d^2}{dt^2}H(\tfrac12 I+tD)
   =-96t^2\sum_{i<j}D_{ij}^4+O(t^4)<0.
   \]
4. Among strict real DPP kernels, (K=I/2) is the unique kernel attaining the
   ambient maximum (n\log2).

This is a local/radial exclusion theorem.  It does not assert that the full
Hessian remains negative semidefinite at every nearby kernel in every
transverse direction.
