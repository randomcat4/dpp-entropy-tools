# P2: separated rare-leaf scales suppress a nondegenerate two-column interaction

Status: `PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW`. This is a conditional
local exclusion and not a resolution of real-kernel entropy concavity.
Author: N4 main. Mechanism child supplied the exact conditional cross-term
identity and a rational family; the scaling argument below is main-authored.

## Frozen scope
Let A be a fixed real symmetric 2 by 2 matrix and u,v fixed real vectors.
Assume `0 < A-uu^T-vv^T` and `A < I`. Write h(C) for the full four-event
entropy of a strict 2 by 2 kernel C, and B_C for its Hessian bilinear form.
For 0<r small enough set

`K_r = [[A, r u, r^2 v], [r u^T, r^2, 0], [r^2 v^T, 0, r^4]]`.

Only the four-dimensional direction space
`D_r(e,f) = [[0, r e, r^2 f], [r e^T,0,0], [r^2 f^T,0,0]]`
is under study; central and leaf diagonals are fixed along the chord.
Let Q_r(e,f)=H''(K_r)[D_r(e,f),D_r(e,f)].
Define a scalar function of a vector w by

`J_A(w)=h(A-ww^T)-h(A)+grad h(A):(ww^T)`

on its strict domain. Its vector Hessians at u and v are 2 by 2 matrices
`L_u=Hess J_A(u)` and `L_v=Hess J_A(v)`.
The additional, explicitly conditional premise is that both L_u and L_v
are strictly negative definite. This premise is not asserted for arbitrary
A,u,v; replacing it by general single-leaf concavity would reintroduce a
three-dimensional open problem.

## Candidate conclusion
There exists r0>0 such that Q_r(e,f)<0 for all 0<r<r0 and every nonzero
(e,f). More precisely the single-column blocks are

`Q_r(e,0)=r^2 (e^T L_u e+O(r^2)||e||^2)`,
`Q_r(0,f)=r^4 (f^T L_v f+O(r^2)||f||^2)`.

Their mixed block is order r^6. If the positive diagonal defect matrices
are denoted N3_r and N4_r, and the mixed bilinear matrix is M_r so that
`Q_r=-e^T N3_r e-f^T N4_r f+2e^T M_r f`, then

`||N3_r^(-1/2) M_r N4_r^(-1/2)||op=O(r^3)`.

The constants may depend on fixed A,u,v and on their strict margins.
They are not uniform when A,u,v move to a boundary or L_u,L_v become singular.

## Derivation
The lower leaf kernel is diagonal, so its event weights are
`q_t=r^(2t3)(1-r^2)^(1-t3) r^(4t4)(1-r^4)^(1-t4)`.
Put m3=r^2 for t3=1 and m3=r^2-1 otherwise, and define m4 analogously with r^4.
Conditional on this event, the central kernel is

`C_t=A-r^2 uu^T/m3-r^4 vv^T/m4`.

For fixed u,v its four limits are respectively A, A-uu^T, A-vv^T,
and A-uu^T-vv^T. All are strictly between 0 and I by the frozen assumptions.
The full kernel is strictly feasible for small r: its lower Schur complement
is A-uu^T-vv^T; that of I-K is
`I-A-r^2 uu^T/(1-r^2)-r^4 vv^T/(1-r^4)`, which tends to I-A>0.

The joint entropy is `h_Ber(r^2)+h_Ber(r^4)+sum_t q_t h(C_t)`.
The Bernoulli terms are direction-independent. For nearby vectors w,z define
the remaining conditional sum F_r(w,z). All central event masses are positive
on a fixed neighborhood of these four limiting kernels, so F is analytic
in x=r^2,y=r^4,w,z at x=y=0. Direct first differentiation at x=y=0 gives

`F_r(w,z)=h(A)+x J_A(w)+y J_A(z)+O(x^2+xy+y^2)`.

For the z-Hessian the x-only remainder has no z dependence: when y=0,
F depends only on w. Therefore
`Hess_z F=y Hess J_A(z)+O(xy+y^2)`.
Similarly `Hess_w F=x Hess J_A(w)+O(x^2+xy)`.
Taylor differentiation is uniform on that fixed neighborhood, proving the
two diagonal estimates. This separates a needed derivative statement from
an undifferentiated scalar O-bound.

For the mixed derivative put S_u=ue^T+eu^T and S_v=vf^T+fv^T.
The conditional kernels have no mixed second derivative in w,z. Since
`q_t/(m3 m4)` equals +1 for t=00,11 and -1 for t=10,01 exactly,

`e^T M_r f = r^6 [B_C11-B_C10-B_C01+B_C00][S_u,S_v]`.

All four B_C are bounded on the fixed strict neighborhood. Hence M_r=O(r^6).
From the conditional premise and the diagonal estimates,
`N3_r >= a r^2 I` and `N4_r >= b r^4 I` for some a,b>0 and small r.
Consequently the whitened norm is at most C r^6/(sqrt(ab) r^3)=O(r^3).
For sufficiently small r it is below one; completing the block square (or
using the Schur complement) proves strict negative definiteness of Q_r.

## Research implication and limitation
A two-column positive direction in this separated-scale construction cannot
persist toward r=0 while the fixed strict-kernel margins and both limiting
single-column curvature defects stay bounded away from zero. A surviving
candidate must exploit a degenerating single-column defect, moving central
kernel/frames, or a different scale geometry. This does not exclude any of
those regimes, any direction changing A/leaf entries, or arbitrary finite r.
No novelty claim or full formal verification is made.
