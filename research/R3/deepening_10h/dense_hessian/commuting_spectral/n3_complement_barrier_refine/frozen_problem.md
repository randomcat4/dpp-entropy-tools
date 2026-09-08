# D10-M8 frozen analytic refinement

Status: ANALYTIC_REFINEMENT_CORRECT_AFTER_INDEPENDENT_REVIEW; general problem
INCOMPLETE.

## Objects, information, and intent

Let Q be any real orthogonal 3 by 3 matrix, theta in (0,1)^3, and v >= 0.
Keep Q fixed in K(t)=Q diag(theta+t v) Q^T, on its strict feasible interval.
Set P_ai=q_ai^2, r_i=theta_i product_{j!=i}(1-theta_j),
s_i=(1-theta_i) product_{j!=i}theta_j, R=sum r, T=sum s,
alpha=Pr/R, beta=Ps/T. Beta_a denotes the pair event missing coordinate a.
The entropy is that of all eight exact events. All logarithms are natural.

The delegated objective permits a new sufficient subclass, but does not change
the unresolved global target B=-H'' >= 0 for all Q,theta,v>=0. This author
may not promote finite non-hits to a theorem or certify its own proof.

## Candidate claims, all at a fixed base point

1. The combined conditional-layer acceleration is exactly
   A=2 sum_{j<k}v_j v_k C_i (i the remaining index), where
   C_i=sum_a P_ai log(alpha_a beta_a)
       -(1-theta_i)log(product alpha)-theta_i log(product beta).
2. If mu=min_i C_i > 0, then B>0 for every nonzero v>=0. C_i>=0 for all i
   is equivalent to A>=0 for every v>=0, not equivalent to total B>=0.
3. A simpler sufficient condition is m=min_a alpha_a beta_a > 1/27, giving
   C_i>=log(27m)>0. In particular alpha_a,beta_a>=1/5 suffices.
4. For theta_i in [epsilon,1-epsilon] and m>=m0>1/27,
   B >= 2 log(27m0) epsilon(1-epsilon) ||v||^2 / 9.

## Boundaries and exclusions

All rates of the opposite sign are covered by sign reversal. The zero rate
has B=0. Single nonzero rates are included, using the count Fisher term rather
than a strictly positive cross-product sum. Repeated eigenvalues and zero
entries in Q are allowed; kernels themselves remain strictly between 0 and I.
The direction is commuting PSD/NSD, not arbitrary noncommuting PSD/NSD.
No conclusion is frozen at m=1/27 about strictness. No uniform constant is
claimed without fixed epsilon and a fixed positive margin above 1/27.

The proof and exact rational sanity are separate deliverables. A fresh
non-author exact-event audit under `verifications/` judged the stated analytic
refinement correct. No Lean certification or novelty certification is claimed.
