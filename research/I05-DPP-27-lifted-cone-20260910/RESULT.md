# Result: a continuous true-rate curvature interval and a lifted entropy cone

Date2026-09-10. New branch from main@097c4db1e17c176d8b75e9ad5054f5beff9e0e06. Tracks issue65/74; successors to PR91 (theory) and PR98 (accurately restored inputs). Neither frozen source is overwritten.

## PROVED — author proof and author interval execution; independent review pending

For exactly the original fixed symbol

    f_t(theta)=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8,

and true complete-occupation Shannon entropy rate per original coordinate,

    h''(t)<-1/4000 for every t in [49/40,51/40].

The corresponding negative interval follows by exact diagonal gauge. In each interval h(t)+t^2/8000 is strictly concave, with a Jensen lower margin lambda(1-lambda)(t1-t0)^2/8000 for distinct endpoints and0<lambda<1. There is no assertion on the intervening larger intervals.

This covers a continuous parameter interval, not finitely many positive samples or an unspecified neighborhood from analyticity. The proof uses the original degree10 coefficients as exact rational TRIALS, a single common residual and its first two parameter derivatives, outward-rounded multivariate Taylor coefficients on the full state ball, and exact two-variable analytic tails. No coefficient was refitted. No numerical differentiation of an invariant measure is used.

The full true-response gate retains all four branches, Fisher, acceleration, state motion and both invariant-law response terms. Certified full-domain bounds are

    ||D_Q^2 r0||<87/20000,
    ||D_Q^2 r1||<611/100000,
    |r2|<7/10000.

Combined with the exact candidate c2/2=-6660155061088431/2000000000000000000, they give the rational upper bound

    -510355061088431/2000000000000000000 < -1/4000.

The single guarded AUTHOR-LOCAL production ran66.527318643 seconds, exit0, one CPU and8GiB cap within a900-second ceiling. The original code, literal inputs, complete durable output and actual execution are included. It was not an S2/server run. Separate exact primitive checks compare24 rational compositions and636 low-order interval coefficients with different constructions. Independent acceptance of both the dependency theorem and new arithmetic is still required.

## PROVED — structural entropy theorem throughout the original target parameter range

With q=t/16, s=q^2, lift Q=[[x,z],[z,y]] to Z=(x,y,r=qz,d=detQ). This is auxiliary bookkeeping, not a replacement of the physical affine t path. The exact convex hull of the lifted operator ball has coordinates U=4(x+y), V=4(x-y), W=8r/q, D=64d and inequalities

    2|U|-1 <= D <= 1-2sqrt(V^2+W^2).

The normalized four-branch operator preserves concavity on this convex set by the perspective identity. Its homogeneous five-dimensional matrices are affine in s, and their sum resets all four nonconstant coordinates. Individual matrices have determinant ac/2^30, so the sum's rank-one property is NOT a Black-Hole/HMM finite-memory condition.

The entropy Poisson corrector extends to the cone interior and is strictly state-concave:

    -D_Z^2 U_s >= I_4/8.

Its Hessian is the limit of the FULL initial-state Fisher matrices of the finite complete-word laws. This result holds uniformly for t in [1/2,3/2]. It does not relabel state curvature as physical t curvature.

## DISPROVED — a tempting global METHOD, not entropy concavity

A concave observable A(Z)=-y^2 does not in general give joint concavity of (s,Z) -> L_s A(Z). A fully rational interior witness, its positive second derivative, and a strict positive endpoint-average-minus-midpoint difference are in lifted_cone.md and run01/exact_lift.json. A separate concave observable disproves monotonicity of L_s' on the entire concave cone.

A preliminary local derivation interchanged the occupied-sign labels in g. Direct determinant checks caught it; the original failed source and the invalid first witness are preserved. The corrected formula is g=1/4-a*x/2-c*y/2+ac(d+2r-s). All final cone statements and witnesses use it. The interval certificate used the direct determinant throughout and was unaffected.

## INCOMPLETE — exact remaining physical sign

The entire [1/2,3/2] curve, still less its full legal path, has not been proved concave. In squared-amplitude coordinates the pure terms B_ss and L_ss U_s are nonpositive, but the mixed stationary-law response and the s''(t) acceleration term remain. They are displayed explicitly in lifted_cone.md rather than silently discarded. Failure of the general cone shortcut does not disprove the entropy sign.

S3 mathematical review and S2 arithmetic/input review: REQUESTED/PENDING_REVIEW, not assumed running. Old stopped budgets are not reused. Novelty and priority: UNASSESSED. Primary-source applicability checks, complete execution/failure distinctions, and reproduction commands are in sources_and_attempts.md and README.md.
