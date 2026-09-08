# N3 unequal-scale sparse-corner falsification

STATUS: INCOMPLETE. No full-entropy counterexample, proof, interval certificate,
or novelty claim is produced. The frozen target is unchanged.

## Reproducible first unit

All 180 centers have the explicit parameterization

    epsilon = 10^(-d), d in {3,9,18},
    s_i = c_i epsilon^(a_i), c=(0.3,0.7,0.9),
    w_i = v_i epsilon^(b_i), v=(1,1.7,-0.6),
    K = diag(s) + theta ww^T/(w^T w).

The three rate vectors a are (1,2,3), (1,3,5), (3,1,2); b ranges over
(0,1,2), (0,0,1), (0,1,3), (0,2,2); theta is 0.2, 0.7, 0.98,
sqrt(epsilon), or 1-sqrt(epsilon). Thus all entries are rational in this
specific finite parameter set. Strict feasibility follows directly from
min(s)>0 and theta+max(s)<1. All off-diagonal entries are nonzero.
This is not the exchangeable family or the fixed-vector equal-soft-scale family.

Hypothesis attacked: unequal diagonal soft scales, moving sparse rank-one
vectors, and endpoint-moving theta might change the sign of the remaining
full-Hessian Schur scalar. Direct event determinants and their cofactor
derivatives are evaluated with 100+3*d*max(a) decimal digits (127 to 370).
There are 180 accepted calls, zero rejected centers, zero rho>1 candidates,
and zero numerical anomalies. A separate one-center smoke call is retained.

The maximum observed rho is 0.9843215686374396156913414686293814675122060027821,
at d=18, a=(1,3,5), b=(0,1,3), theta=1-sqrt(epsilon). This is below one;
it is not a counterexample or a global bound. Full outputs, including every
center and direction, are in [batch.json](batch.json).

## Directed conditional-score lemma attack

For each conditioning site k and state, arrange the four unnormalized atoms
as a,b,c,d. Put m=a+b+c+d, delta=ad-bc and

    V=ad(a+d)+bc(b+c)-4 delta^2/m,
    Q_k(D)=D_kk^2/[K_kk(1-K_kk)]
           + sum_states (delta'-2 delta m'/m)^2/V.

The parent supplied the rigorously valid lower bound F>=Q_k. The all-direction
claim max_k Q_k>=2 tr(N adj D) is too strong. Before the parent reported its
small rational certificate, a bounded 36-center minimax scout independently
found large negative gaps. Those results remain only numerical shortcut
obstructions in [conditional_q.json](conditional_q.json); they are not DPP
entropy counterexamples and do not need further search.

The actual weaker candidate is evaluated at

    D*=A^(-1)eta/[eta^T A^(-1)eta], A=F+det(N)G_N.

All 180 existing centers satisfy the tested inequality numerically. In 141
of them the cofactor quantity C=2 tr(N adj D*) is positive, so the check is
not uniformly vacuous. The minimum normalized gap (max Q_k-C)/det(N) is

    5.2004289899629087993478790258990827678639772834199e-11.

It occurs at d=18, a=(3,1,2), b=(0,0,1), theta=1-sqrt(epsilon).
Here C/det(N)=2.2396091280789493537e-26 and B(D*,D*)/det(N)=
0.016069595557805111173. The individual Q_k/det(N) are approximately
5.5604e-12, 4.6441e-11, and 5.2004e-11. The gap being small is not a sign
failure. The auxiliary F-only constrained minimizer also passes 180/180,
with 71 positive cofactor cases; it is distinct from the frozen A minimizer.

The second optimal-direction run adds cofactor and Q diagnostics to the same
180 centers. It is explicitly a repeated run, not 180 new centers. The prior
script and output are retained with suffix `_v1` and matching source hash.

## Higher-precision check and remaining obligation

[recheck.json](recheck.json) repeats the smoke center, maximum-rho center,
and minimum-A-gap center at 550 decimal digits. It independently reconstructs
the event masses by inclusion-minor Mobius inversion and checks all 48 event
jet entries per center by differentiating the explicit polynomial formula.
Maximum relative event disagreement is below 3e-533; maximum absolute jet
disagreement is below 2e-551. This is same-author arithmetic checking, not a
fresh mathematical review or a rigorous interval sign certificate.

The minimum unresolved lemma remains: prove max_k Q_k(D*)>=C(D*) for every
strict connected real three-dimensional K, or exhibit a strictly validated
failure at its actual A minimizer. The finite 180-point evidence does not
control all joint rates, cancellation patterns, or general interior centers.
The full entropy theorem remains unproved regardless of this lower-bound
lemma's eventual status. No further scan or background job is active.
