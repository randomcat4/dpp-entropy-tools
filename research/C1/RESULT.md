# I05-C1-20260909 — PARTIAL

The universal B0 implication remains unresolved:

    connected strict real symmetric 3x3 K, beta(K)=0
    => det(N(K)) alpha(K) <= 1.

No violating exact zero and no positive K-affine entropy chord were found.
The completed restricted results below do not certify B0 on its whole domain.
Novelty is NOT_CERTIFIED.

## Main restricted theorem: exact zeros approach the proposed boundary

Fix lambda=7/10 and s=2/5. Write L=log(1/epsilon) and

    u=(sqrt(s(1-kappa epsilon)),
       sqrt((1-s)(1-kappa epsilon)),sqrt(kappa epsilon)),
    K(epsilon,kappa)=epsilon I+lambda uu^T,  kappa in [1,10].

There is epsilon0>0 such that for EVERY 0<epsilon<epsilon0 there is an
exact beta-zero parameter kappa_epsilon in (1,10). Every exact zero in this
interval obeys, with uniform errors,

    kappa_epsilon=(3/7)(exp(40/21)-1)+O(1/L),
    det(N) alpha=1-10/(7L)+O(L^-2)<1.

The calculation uses h=M^-1 eta in all six genuine symmetric K directions.
It retains all eight event probabilities, including the leading common-event
U,V Fisher cross term and rare triple log terms. It is not a calculation on
an arbitrary Lambda-tangent direction or on derivatives of family parameters.

Consequently det(N) alpha tends to 1 along exact beta zeros. There is no
universal delta>0 for which the whole connected strict beta-zero domain has
det(N) alpha<=1-delta. If B0 is true, its constant 1 is sharp. This conclusion
does not assert uniqueness or smooth selection of finite-epsilon roots,
an explicit numeric epsilon0, or any inequality on the remaining zero set.

Proof: geometry/sparse_proof.md, frozen SHA256
b096a9986d123652849704ed001439b63373591153f4bbd321f8023d9ab98e9f.
Two independent nonauthor contexts returned CORRECT for this restricted
theorem; see verification.md and the unedited review reports.

## Supporting restricted results

1. Full-support rank-one collar. For fixed lambda in (0,1), fixed unit
   full-support u, compact symmetric C with (PCP)|u-perp uniformly positive,
   bounded symmetric R, P=I-uu^T, and K=lambda uu^T+tau C+tau^2 R,
   the complete optimizer satisfies uniformly

       beta=-tau sqrt(det((PCP)|u-perp))/(sqrt(lambda) log(1/tau))
            *[1+O(1/log(1/tau))] < 0.

   Thus this collar contains no beta zeros for sufficiently small tau.
   The theorem includes the stated fixed full-support twisted-complement
   affine family for all joint epsilon/t ratios. It does not cover support
   loss, an ill-conditioned soft block, or varying boundary lambda.
   This theorem has one independent nonauthor CORRECT review.

2. Finite exact-zero certificate. For the separate rational family

       K(q)=10^-8 I+(7/10)u(q)u(q)^T,
       u(q)=(3/5,4/5,q/10000),
       qL=4418854248579277079/2305843009213693952,
       qU=8837708497158554159/4611686018427387904,

   an exact Fraction-based outward interval calculation proves opposite
   signs of beta sqrt(Z) at qL and qU, strict feasibility, positive atom
   probabilities, positive N, and a nonsingular full solve throughout.
   Hence at least one exact beta zero lies in (qL,qU). The entire bracket has

       0.9256053240119633
       < det(N) alpha <
       0.9258067049461273 < 1.

   This is a new finite certificate relative to the supplied old 0.661528
   calibration, but it is not a violating zero. This u is not unit-normalized;
   the finite certificate cannot be substituted into the analytic family's
   finite-epsilon formulas. The exact fractions in the certificate JSON,
   rather than rounded display decimals, are authoritative.
   The finite certificate and its error-enclosure explanation both received
   a separate nonauthor CORRECT review, including an independent server
   rerun with the required explicit 60-bisection input.

3. Exact structural reconstruction and diagonal-tilt stationarity. The
   full event Hessian, N positivity including connected zero-edge strata,
   covariance Fisher projection, and the true optimizer are reconstructed.
   Diagonal L tilts give exact mixed stationarity equations for h. A nonauthor
   review accepted these identities. They do not establish the missing sign.

## Substantive stop

The unresolved minimum assertion is still complete Fisher/cofactor control
at the actual optimizer for every exact beta-zero kernel outside the proved
restricted sets. The geometric degeneration and exact exponential-tilt
mechanisms have both been developed; their limits are documented, with no
automatic larger scan. HANDOFF.md contains only two concrete possible next
tasks, including the joint lambda-to-one/sparse regime not covered here.

The archive includes complete proofs, failed and corrected attempts, primary
sources, exact inputs, scripts, outputs, dependencies, reviewer provenance,
and checksums. Independent review is mathematical inspection with separate
computational diagnostics, not a machine-checked Lean proof or a human expert
review. Publication is a Draft PR for coordinator review, with B0 open.
