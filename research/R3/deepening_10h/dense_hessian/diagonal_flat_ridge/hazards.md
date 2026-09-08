# D10-U2 hazards

Author status: **HAZARD_LEDGER_PENDING_FRESH_REVIEW**.

1. **Exact events only.**  The proof starts from Möbius inversion of inclusion
   determinants.  Principal minors are inclusion probabilities, not exact
   atoms.

2. **Zero diagonal is a base-direction condition.**  The theorem concerns
   \(K(t)=X+tD\) at a diagonal \(X\) with \(D_{ii}=0\).  It does not say the
   same formula holds at non-diagonal nearby kernels.

3. **Global maximum is fiberwise only.**  The entropy maximum statement fixes
   every diagonal entry \(K_{ii}=x_i\).  It is not a global maximum over all
   kernels with varying one-coordinate marginals.

4. **Strict equality uses DPP pair inclusion.**  Shannon subadditivity gives
   \(H(Y)\le\sum_i h(x_i)\).  Strict equality is ruled out by
   \(\mathbb P(i,j\in Y)=x_ix_j-K_{ij}^2\); if some \(K_{ij}\ne0\), the
   coordinates cannot be independent.

5. **Flat Hessian is not neighborhood Hessian negativity.**  The result proves
   fourth-order radial descent along zero-diagonal rays from diagonal kernels.
   It must not be rewritten as a full-neighborhood concavity or Hessian sign
   theorem.

6. **Heterogeneous diagonal kernels are not generally even in \(t\).**  The old
   uniform \(K=I/2\) proof used complement symmetry to remove odd terms.  For
   general \(X=\operatorname{diag}(x_i)\), the theorem proves \(H'\), \(H''\),
   and \(H'''\) vanish and identifies the negative fourth derivative; it does
   not claim an \(O(t^6)\) remainder.

7. **The \(p''\)-term is not atomwise zero.**  In off-diagonal directions many
   exact atoms have nonzero \(p_S''(0)\).  Logarithmic linear terms cancel only
   after summing against total mass and singleton inclusion marginals.

8. **Strictness uses pair inclusion.**  The fourth derivative is strictly
   negative because any nonzero off-diagonal \(d_{ij}\) forces
   \(\sum_{S\supseteq\{i,j\}}p_S''(0)=-2d_{ij}^2\).  This is a global atom
   statement, not a claim about a single identified atom.

9. **Explicit edge formula depends on centered singleton scores.**  The
   correct constant is
   \[
   H^{(4)}(0)=-12\sum_{i<j}
   D_{ij}^4/[x_i(1-x_i)x_j(1-x_j)].
   \]
   In the uniform \(x_i=1/2\) case, the Taylor \(t^4\) coefficient is therefore
   \(-8\sum_{i<j}D_{ij}^4\), matching U1.

10. **Uniform fourth-order bound needs \(n\ge2\).**  For \(n=1\), the
   zero-diagonal direction space contains only \(D=0\); the normalized slice is
   empty.  The displayed \(n(n-1)\) denominator is stated only for \(n\ge2\).

11. **Uniform small-\(t\) descent needs compactness.**  The descent radius is
   for fixed \(n\) and \(x_i\in[a,b]\subset(0,1)\), with
   \(\|D\|_F=1\).  The radius is existential and may shrink with \(n,a,b\).

12. **Strict feasibility is local for affine rays.**  Arbitrary symmetric zero-diagonal
   directions need not keep \(X+tD\) feasible for large \(t\).  All derivatives
   are local at \(t=0\).

13. **Author-side result only.**  The current directory is an author proof
    candidate and should receive a fresh non-author verification before being
    used as certified infrastructure.
