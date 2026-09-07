# Frozen theorem v1: finite-block entropy-loss and Jensen-gap enclosure

Frozen by T2 main, 2026-09-07. Status CANDIDATE until fresh independent audit.
Authors and verifiers may not add, weaken or reinterpret assumptions.

## Objects and definitions

For every integer n>=1, let K be an n by n complex Hermitian matrix with 0<=K<=I. In a fixed coordinate basis define the finite DPP P_K by P_K(S subset X)=det K[S,S] for every S subset [n]. Let H(K)=-sum_X P_K(X) log P_K(X), with natural logarithms and 0 log 0=0.

Let Pi be any partition of [n] into nonempty coordinate blocks. Let B=P_Pi(K) be its block diagonal pinching, and E=K-B. Define h(x)=-x log x-(1-x)log(1-x) on [0,1] by continuity. The spectral quantity tr h(K) is NOT H(K). Define

L_Pi(K)=H(B)-H(K), Q_Pi(K)=tr h(B)-tr h(K).

## Claim A: all finite positive contractions

For all objects above, including singular K or B,

0 <= L_Pi(K) <= Q_Pi(K).

H(B)=sum_{A in Pi} H(K[A,A]). No spectral gap is assumed for Claim A.

## Claim B: explicit block buffer only

For every eta in (0,1/2], if eta I<=B<=(1-eta)I, then, with all inverses defined,

Q_Pi(K) <= R_Pi(K):=tr(E^2 [B(I-B)]^{-1})
            <= ||E||_F^2/[eta(1-eta)].

K itself may have eigenvalues zero or one. eta=0 is excluded; no constant uniform in eta is asserted. n is finite; there is no hidden dimension-independent operator-norm claim. Frobenius energy counts every matrix entry.

## Claim C: signed Jensen gap

For every pair of feasible K_0,K_1 of the same dimension, every t in [0,1], and the SAME partition Pi, put K_t=(1-t)K_0+t K_1 and B_r=P_Pi(K_r). Let

J_t=H(K_t)-(1-t)H(K_0)-t H(K_1),
J_t^B=H(B_t)-(1-t)H(B_0)-t H(B_1).

For any independently valid upper bounds C_r>=L_Pi(K_r) for r=0,1,t, Claims A/B permit Q_r, R_r or the corresponding buffered Frobenius bound. Then

J_t^B-C_t <= J_t <= J_t^B+(1-t)C_0+t C_1.

Consequently J_t^B>C_t suffices for J_t>0, while J_t^B< -((1-t)C_0+t C_1) suffices for J_t<0. If neither holds the tool is inconclusive. There is no assertion that a negative seed exists.

## Input, output, and success contract

Input: explicit kernels, a fixed partition, a weight t and (when used) a certified block buffer. The output is an entropy-loss upper bound or Jensen-gap interval. Approximate eigenvalues and ordinary floating arithmetic do not certify exact input conditions or final signs. Rational input can use a sufficient exact row-sum certificate; its rejection does not imply kernel infeasibility.

Success requires a complete finite-dimensional proof plus an application family and a boundary family, and fresh-context verification on a fixed candidate commit. The intended tool reduces full-system subset enumeration to block entropies plus polynomial-size matrix bounds. Its mathematical ingredients may be classical; no novelty claim is included.

## Nonclaims and limits

No entropy-rate theorem, stationary scalarization, complex-to-real transfer, global concavity, Hessian bound, low-rank-only area bound, or moving-scale compactness argument. Fixed finite-dimensional regularization may be used if fully proved; exchanging dimension and perturbation limits is not authorized. Real symmetric kernels are included directly as a subclass, not by realification of a complex process.
