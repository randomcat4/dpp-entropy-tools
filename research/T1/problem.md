# T1: an event-free bridge-direction curvature test

Status: RUNNING; frozen target v1; no certification yet.

For a finite Hermitian strict contraction K, the exact DPP event law is
p_S(K)=(-1)^{|S^c|} det(K-I_{S^c}), and H(K)=-sum_S p_S log p_S
(natural logarithms). The task is a structural sufficient sign test for the
second derivative on the affine path K+tD. The general Hessian identity is
background, not a contribution.

The first bounded target restricts K to real symmetric matrices and D=iA to
the existing bridge edges of the nonzero off-diagonal support graph of K.
The proposed checker uses only K and A: exact symmetry, strict contraction,
and graph bridge membership. No probability enumeration is used by the checker.
The mathematical statement is in frozen_theorem_v1.md; the statement owner
approved these hypotheses before formal proof drafting.

The broader complex/real concavity question and stationary entropy rates
remain outside this run. An unsupported input returns INCONCLUSIVE, not a
counterexample. Finding no numerical counterexample cannot prove any claim.

Useful family: arbitrary real dense strict-contraction blocks linked through
single bridge edges. The concrete tool examples use chains of triangles,
not only the two-site seed. Positive definiteness can be guaranteed uniformly
by diagonal entries 1/2, triangle weights 1/20, and bridge weights 1/40.
Every row's absolute off-diagonal sum is at most 3/20 < 1/2.

Success means a complete independently audited weak theorem, an exact input
checker, a reproducible non-seed application, and explicit failure boundaries.
Novelty and mathematical correctness are separate judgments.
