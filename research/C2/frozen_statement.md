# Frozen statement, version 1 — I05-C2-20260909

The original research question remains: on the fixed real five-point rank-three face below, does any real symmetric A with 0<A<I_3 and real symmetric V have H''(A)[V,V]>0? A successful counterexample must supply a strict positive rational finite chord and a common rational strict-interior lift. No such counterexample is asserted here.

Let

    U = (1/1045) [[615,120,-702],[240,735,246],[-630,30,-71],
                  [480,-620,492],[-170,-390,-540]].

This is exactly the first three columns of the two Householder matrices specified in the task. Write r_i for row i transposed, w_ij=r_i cross r_j. K=UAU^T. The exact event probability is p_A(S)=sum_{T superset S}(-1)^(|T|-|S|) det(K_T). H=-sum p log p, natural logs, 0 log 0=0. Derivatives always mean the affine path A+tV, even when V does not commute with A.

The following explicitly restricted claims are frozen for independent review:

1. **Upper-face compensation cone.** For every real symmetric B with I_3<=B<=2I_3, every 0<e<=1/1971200, and every real symmetric V,

       H''(I_3-eB)[V,V] <= - ||V||_F^2/(352 e).

   In particular it is strictly negative for V nonzero. V may depend arbitrarily on B,e. This is a full-direction local Hessian statement at the specified centers, not global five-point concavity and not a theorem for arbitrary approaching eigenvalue ratios.

2. **Low-event derivative injectivity.** At every 0<A<I_3, if p_empty'=0 and p_ij'=0 for all ten pairs, then V=0. More precisely, all pair derivatives vanish for a nonzero V if and only if tr A=2 and V=s A(I-A) for some nonzero real s.

3. **Residual pair compensation on the exceptional direction.** Under tr A=2 and V=s A(I-A), s nonzero, every pair has p_ij'=0 and p_ij''<0. Consequently its contribution -p_ij'' log p_ij is strictly negative, even though its Fisher contribution vanishes.

These are auxiliary results within the original task, not replacement definitions or a solved global conjecture. Every quantifier in each restricted result is binding. Reviewers must not add hypotheses. The exact frame inequality with constant 1/22 is part of the supporting proof, checked by rational arithmetic; no formal proof assistant verification is claimed.

Boundary convention: the six events of size greater than three vanish identically along these fixed-support paths. All other events are strictly positive. No derivative of log zero is taken. Finite legal steps must keep 0<A+tV<I_3; the precise symmetric-step condition is stated in proof.md.
