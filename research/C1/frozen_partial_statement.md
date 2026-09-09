# Frozen partial statement — sparse exact-zero sharpness

This supplements B0 without changing its assumptions or global conclusion.

Fix lambda=7/10 and s=2/5. For epsilon>0 and kappa in [1,10], define

    u=(sqrt(s(1-kappa epsilon)),
       sqrt((1-s)(1-kappa epsilon)),sqrt(kappa epsilon)),
    K(epsilon,kappa)=epsilon I+lambda uu^T,
    L=log(1/epsilon).

Use the complete eight-event definitions of N, Fpair, M, alpha, beta and the genuine M optimizer in frozen_statement.md. All Hessian derivatives remain derivatives in the six actual symmetric K entries.

Partial assertion: there is epsilon0>0 such that, for every epsilon in (0,epsilon0), at least one kappa_epsilon in (1,10) has beta(K(epsilon,kappa_epsilon))=0. Every such zero in [1,10] satisfies

    kappa_epsilon = (3/7)(exp(40/21)-1)+O(1/L),
    d alpha = 1-10/(7L)+O(L^-2) < 1,

with uniform constants. Consequently d alpha tends to 1 along exact beta zeros and no fixed positive delta bounds the entire connected strict beta-zero set by 1-delta.

No explicit numerical epsilon0, uniqueness, smooth selected branch, violating zero, global B0 proof or novelty claim is included. The proof is geometry/sparse_proof.md, frozen author SHA256 b096a9986d123652849704ed001439b63373591153f4bbd321f8023d9ab98e9f; author text committed at 0ff950c685228a9c76be0aa6dbbed77f077899a1. Acceptance depends on the independently recorded final review scope.
