# Analytic Hessian used by the parameter search

Status: INCOMPLETE. This is a numerical exploration implementation, not a concavity theorem.

The parent-frozen target is a real symmetric strict contraction K of order 3 through 10 and a real symmetric Frobenius-unit direction V with positive Shannon entropy Hessian, followed by a rational feasible chord with Delta = (H(K-tV)+H(K+tV))/2-H(K)>0. No premise is changed here.

For each subset S of [n], put D_S=diag(1_{i not in S}) and A_S=K-D_S. The exact event probability is p_S=(-1)^{n-|S|}det A_S. This equals the coefficient in det(I-K+diag(z)K), hence equals inclusion-probability Mobius inversion. Principal minors alone are not exact events.

For strict contractions every event has positive probability. Differentiating det A_S along V gives g_S=tr(A_S^{-1}V), p'_S=p_S g_S, and p''_S=p_S(g_S^2-tr(A_S^{-1}VA_S^{-1}V)). Since sum p'_S=sum p''_S=0, the entropy Hessian is

H''(K)[V,V] = -sum_S p_S[(1+log p_S)g_S^2-log(p_S)tr(A_S^{-1}VA_S^{-1}V)].

Use the Frobenius-orthonormal symmetric basis E_ii and (E_ij+E_ji)/sqrt(2), compute its full Hessian, and take its largest eigenpair. This direction calculation has no restriction to a patterned matrix family.

Kernel parameterization: symmetrize an arbitrary dense raw matrix B; diagonalize B=Q diag(w)Q^T; set K=Q diag(epsilon+(1-2epsilon)sigmoid(w))Q^T. For each selected positive epsilon this parametrizes all symmetric kernels with epsilon I<K<(1-epsilon)I. The finite runs sample epsilon in {0.02,0.005,0.001}; they do not exhaust this open set.

Every numerical hit above 1e-6 must be independently checked and converted to an exact rational object. Tiny positive floating values do not qualify. A negative finite-search result cannot exclude any continuous structural family.

Self-checks compare signed-determinant events with inclusion-probability Mobius inversion and analytic directional Hessians with centered entropy differences. Those author checks validate implementation consistency but do not constitute independent mathematical certification.
