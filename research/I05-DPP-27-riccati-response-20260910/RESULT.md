# Final result of the PR91 author unit

Date: 2026-09-10. Base at branch creation: main@65e59a46b49cd2dbb5c779a4cfae8cef26441984. Predecessor PR79; parent issue65; computation issue74. Main and the predecessor branches are not modified by this unit.

## PROVED (AUTHOR PROOF), PENDING_REVIEW

The fixed symbol and interval remain

    f_t(theta)=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8,
    t in [1/2,3/2].

All probabilities below are COMPLETE occupation events. All derivatives are in this genuinely affine correlation-kernel direction, not an affine L kernel or an observation-basis change. Entropy uses natural logarithms and is normalized per original lattice coordinate.

### A. A full contractive probability operator, not just contractive branches

Let q=t/16, alpha=(a,b) in {-1,+1}^2,

    D_alpha=[[a/2,q],[q,b/2]], E=[[1/8,0],[q,1/8]],
    g_alpha(Q)=ab det(D_alpha-Q),
    T_alpha(Q)=E(D_alpha-Q)^(-1)E^T,
    L_t A(Q)=sum_alpha g_alpha(Q) A(T_alpha(Q)).

On the parameter-independent convex state domain B={Q symmetric: ||Q||_2<=1/8}, all four probabilities satisfy g_alpha>=81/1024 and sum g_alpha=1. Complete-event block determinants identify them with the actual conditional cell probabilities. The no-future seed is Q=0.

Each branch contracts in Frobenius distance by k=34/81. Accounting for the changing probabilities, the ENTIRE law contracts in W1 by

    beta_*=4259/6480<2/3.

The strengthened proof uses image Frobenius radius19/160 and TV(g(Q),g(P))<=||Q-P||_F. It does not omit the weight-variation term. The older bound4363/5184 remains valid but is no longer the strongest result.

The unique invariant law eta_t is the actual infinite-future correction-state law, and

    h(f_t)=(1/2)eta_t B_t,
    B_t(Q)=-sum_alpha g_alpha(Q)log g_alpha(Q).

The infinite reachable attractor has four disjoint injective branch images and is homeomorphic to the four-symbol one-sided space. Its invariant law is non-atomic with full support. This rules out replacing this exact state presentation by finitely many of its own states; it does NOT rule out every different finite HMM presentation.

### B. Genuine parameter derivatives and the complete Fisher bridge

The coding state has genuine, uniformly convergent first/second derivatives, with

    ||Q'||_2<=1/5, ||Q''||_2<=3/4,

and explicit geometric-polynomial truncation errors. The finite complete-event score differs from the corresponding infinite-conditional-score sum by a uniformly bounded remainder, so its Fisher information per original coordinate converges to the FULL conditional Fisher rate, including state movement. No branch or rare event is omitted.

For the centered Poisson resolvent Rcal, with u*=Rcal B_t and v*=Rcal(B_t'+L_t'u*), the complete true-rate response is

    h''=(1/2)eta_t[B_t''+L_t''u*+2L_t'v*].

Here operator derivatives keep their trial observable fixed and include the movement of T_alpha. Fixed-Q local Fisher alone is not relabeled as the full Fisher rate. State motion, acceleration and invariant-measure response remain in the formula.

### C. The stronger finite-data TRUE-curvature certificate

The exact identity L_t Q=0 annihilates affine observables under L_t' and L_t''. It also yields direct contraction of the STATE-HESSIAN seminorm:

    |L_t A|_2 <= (63677321/83980800)|A|_2
               <(19/25)|A|_2,
    |Rcal A|_2 <=(25/6)|A|_2.

This is a regularity/resolvent result, NOT a claim that physical h'' is negative.

Choose polynomial Poisson trials u,v,w and constants c0,c1,c2. Define

    r0=B_t-c0-(I-L_t)u,
    r1=B_t'+L_t'u-c1-(I-L_t)v,
    A=B_t''+L_t''u+2L_t'v,
    r2=A-c2-(I-L_t)w.

For verified suprema over the ENTIRE state domain,

    e02>=||D_Q^2 r0||sup,
    e12>=||D_Q^2 r1||sup,
    e20>=||r2||sup,

one has the explicit true-curvature bound

    |h''-c2/2| <= e02/2+(9/100)e12+e20/2.             (*)

The exact coefficients before rounding up are9762629/19660800<1/2 and202141/2359296<9/100. The derivation includes BOTH nested invariant-measure response terms. Constants and affine errors in r0/r1 need not be certified because their responses vanish exactly. No numerical derivative of a discretized invariant measure is needed.

An alternative gate using the earlier residual types is

    |h''-c2/2|<=3e01+e02/15+(11/20)e11+e20/2,

where e01 and e11 bound first state derivatives of r0 and r1. The original coarser gate13e01+e02/8+6e11/5+e20/2 remains correct.

### D. Additional exact consequences

    eta_t Q=0, eta_t det Q=0,
    eta_t g_(a,b)=1/4-ab q^2.

The m-future-cell conditional entropy per original coordinate has actual value error at most(9/16)(34/81)^(2m). This bound is for VALUES ONLY; differentiating it does not prove a curvature bound.

## INCOMPLETE: no full-interval sign has been certified

To finish by (*), each rational parameter cell J needs three outward supremum enclosures on B x J and

    sup_J(c2/2)+e02/2+(9/100)e12+e20/2<0.

The accepted cells must cover every point of[1/2,3/2], including endpoints. This precise finite-data verification is not yet completed. No h'' counterexample was obtained. No author proof or sample is promoted to independent acceptance.

## Actual evidence versus numerical scouts

The bounded exact Fraction checker matched252 complete event values and both genuine t-derivative layers against independent inclusion/Mobius enumeration at t=1/2,5/4,3/2 and lengths2,4,6. Exact normalizations, branch/state/jet bounds, weighted-state identities and rational proof constants passed. These are author computations, not a separate reviewer.

Three degree6/8/10 polynomial scouts at t=5/4 produced c2/2 near-0.00333008. The degree10 diagnostic substitution in the ORIGINAL coarser gate was about9.93e-6, but it uses sampled finite-difference residuals and binary floating arithmetic. It is NOT an error bound for h'' and proves no new point sign. All three full original coefficient/output records are retained, including the weaker trials.

The post-handoff exact constant check at03:32:19UTC verifies the improved beta, state-Hessian contraction and response-error coefficients. It does not run a continuum certificate. Two corrupt text-transcribed coefficient-archive fragments were withdrawn and preserved as failures in Git history. Original coefficient data were successfully transferred to an existing PRIVATE Drive file and are also supplied in the chat raw-execution ZIP; no public raw-coefficient mirror is claimed.

## Review, source and job status at final checkpoint

All new analytic claims here are PROVED (AUTHOR PROOF), PENDING_REVIEW; novelty is UNASSESSED. The preceding PR79 upper-tail B_R is only an upper budget, never a lower bound on the actual tail or a necessary-depth theorem.

During this task main advanced: C3's accepted_pr77.md at c6618e37640c5d019d9bbdc6fbffdc7fe31241f1 now records independent dual acceptance and integration of the FIXED midpoint and three point-curvature certificates. That scope was read. It does not certify the continuous interval, and Section9's true-rate second-order bridge remains incomplete. The new PR91 proofs do not depend on those finite numerical signs.

The explicit original-budget continuum amendment is REQUESTED in issue74 comment5612135254. The optional stronger gate and frozen source are posted in comment5612428413. Maximum7200s total,4CPU,16GiB,noGPU, fixed outward-arithmetic and exact-input requirements, explicit stop/checkpoint/resume conditions. No external continuum execution is asserted without an issue claim; no duplicate budget is created. A currently claimed job must explicitly freeze any changed gate rather than silently replacing its input.

Main proof: proof.md. Strongest refinement: post_handoff_cancellation.md. Complete Fisher/non-atomicity/forgetting: coding_and_fisher.md. General residual derivation and conventions: curvature_certificate.md. Literal source, execution, provenance and failure boundaries: sources_and_attempts.md. This unit continued deriving and checking theory after initial upload and after the compute handoff; it did not terminate at packaging.
