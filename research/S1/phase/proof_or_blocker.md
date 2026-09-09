# Phase route, first bounded unit

Overall status: **INCOMPLETE** for the frozen scalar stationary entropy-rate conjecture. The exact construction, eventwise symmetry and single-edge exclusion below are **PROVED** on their stated scopes. All numerical results are exploratory floating point results, not certificates. No positive finite-window or entropy-rate example was found in the declared batch.

## Fixed rational candidate and feasibility

With theta=2*pi*x, fix

    f_t(x)=1/2+(3/10)cos(theta)+(3/25)cos(2theta)+(1/25)cos(3theta)
                  +t[(3/25)sin(2theta)-(1/25)sin(3theta)], |t|<=1/8.

All parameters, the degree and the endpoints are independent of the window. The triangle bound gives

    |f_t-1/2| <= 23/50+(1/8)(4/25)=12/25.

Thus 1/50<=f_t<=49/50 everywhere, and every compression K_n(t) satisfies (1/50)I<=K_n(t)<=(49/50)I. The latter follows by integrating f_t times the squared absolute value of the corresponding trigonometric polynomial. This is an affine chord in the correlation kernel itself.

Write c_k(t)=fhat_t(k)=(a_k-i*t*b_k)/2 for k>0. In this candidate

    c_1=3/20, c_2=(3/50)(1-it), c_3=(1/50)(1+it).

## Symmetry is eventwise, not just an entropy pairing

Let omega in {0,1}^n and Z={j:omega_j=0}. Its exact event mass is

    q_omega(t)=(-1)^|Z| det M_omega(t), M_omega(t)=K_n(t)-diag(1_Z).

To see the formula, expand the determinant in the diagonal entries selected from -diag(1_Z). The result is the inclusion-exclusion sum of the inclusion probabilities det K[A,A], over all additional selected sites in Z. This explicitly includes all zero constraints.

At an even real center and an odd real direction, K_n(-t)=conjugate(K_n(t)). The same identity holds for M. Its determinant is real because M is Hermitian. Consequently **q_omega(-t)=q_omega(t) for each individual configuration**. Every odd event derivative at zero vanishes. The positive margin makes every exact mass strictly positive: for example, L=K(I-K)^(-1)>0 and q_omega=det(I-K)det L[omega,omega]>0. Hence entropy is analytic on a neighborhood of this chord and

    H_n''(0)=-sum_omega q_omega''(0) log q_omega(0).

The usual nonpositive term -sum(q_omega')^2/q_omega vanishes at the center. Its disappearance does not determine the sign of the remaining acceleration sum.

For a basis of imaginary Hermitian directions D_r, put A_omega=M_omega(0)^(-1). Since A is real symmetric and D is i times a real skew symmetric matrix, tr(A D_r)=0. The exact directional Hessian is

    Q_rs = sum_omega q_omega log(q_omega) tr(A_omega D_r A_omega D_s).

Indeed determinant differentiation gives q_rs=-q tr(A D_r A D_s); summing q_rs gives zero. This is the formula used by the batch. No limit in n or derivative-limit exchange occurs here.

## Two invariant phases and the actual cycle change

Diagonal unitary conjugation preserves products of kernel entries around cycles. Because c_1 is nonzero, a diagonal conjugation that preserves Toeplitz form must have successive vertex phases with constant difference. Therefore its action on c_k is multiplication by exp(i*k*phi), up to the harmless choice of orientation. Translation of the symbol produces precisely this action.

Two independent integer relations between the three harmonic phases are represented by the closed walks with lengths (1,1,-2) and (1,1,1,-3). Their products are

    C_112=c_1^2 conjugate(c_2)=(27/20000)(1+it),
    C_1113=c_1^3 conjugate(c_3)=(27/400000)(1-it).

Their arguments are arctan(t) and -arctan(t), respectively. The corresponding relation vectors (2,-1,0) and (3,0,-1) are linearly independent. Both change at the center, so this is a genuine two-relative-phase path; no diagonal gauge can turn its endpoints into the center. In addition, |c_2| and |c_3| increase, which separately rules out translation equivalence. This does not imply any entropy increase. The endpoints themselves are complex conjugates and have exactly the same DPP law.

The triangle (1,2,-3) has

    C_123=c_1 c_2 conjugate(c_3)=(9/50000)(1-it)^2,
    Re C_123=(9/50000)(1-t^2).

It supplies a genuine negative cycle-product acceleration, while Re C_112 and Re C_1113 stay constant. Pair contributions change in the opposite structural sense because |c_2|^2=(9/2500)(1+t^2) and |c_3|^2=(1/2500)(1+t^2). This was the specific cancellation hypothesis tested. Merely assigning nonzero invariant phases would miss these amplitude changes.

## A single imaginary edge cannot give the positive mechanism

**PROVED, finite-kernel scope.** Let K be any strictly interior real symmetric DPP correlation kernel on a finite vertex set. Change only one unordered edge {a,b}, by replacing its two entries with K_ab+i*t*v and its conjugate. On any interval where the resulting kernel remains strictly interior, the full configuration entropy is nonincreasing as a function of t^2. It is strictly decreasing away from zero when v is nonzero. This statement does not require the edge to be a graph bridge.

Proof. Condition on the exact configuration eta on B=V\{a,b}. Its probability w_eta depends only on K[B,B], so it is independent of t and is positive. The conditional correlation kernel on {a,b} is

    C_eta(t)=K[{a,b},{a,b}](t)
             -K[{a,b},B](K[B,B]-diag(1_{eta=0}))^(-1)K[B,{a,b}].

This follows either by a Schur complement of the exact-event determinant above or by taking its ratio with the event mass on B. The inverted matrix is nonsingular because that event has positive mass. Its entries and the correction are real and independent of t. Therefore C_eta(t) has fixed diagonal r,s and off-diagonal z+i*t*v with z real. All its four exact masses are positive. Put u=z^2+t^2*v^2. The conditional pair distribution, in order 11,10,01,00, is

    A=rs-u, B=r(1-s)+u, C=(1-r)s+u, D=(1-r)(1-s)-u.

Differentiating its entropy J(u) gives

    J'(u)=log(AD/(BC)).

Direct multiplication gives AD-BC=-u. Thus J'(u)<=0, with strict inequality when u>0. Since u=z^2+t^2*v^2, J is strictly smaller at any nonzero t when v!=0, including z=0 (then the initial second derivative is zero but the finite decrease is strict). The chain rule for entropy gives

    H(X_V(t))=H(X_B)+sum_eta w_eta J_eta(z_eta^2+t^2*v^2),

which proves the assertion. There is no assumption about a bridge, a graph distance, or stationarity. Endpoints on the boundary can also be obtained by continuity if needed, but they are not needed in this unit.

In particular, every single-edge diagonal entry of the imaginary-direction Hessian at a real center is nonpositive, with formula

    2*v^2 sum_eta w_eta log(A_eta D_eta/(B_eta C_eta)).

A positive multidirectional Hessian therefore requires mixed contributions from different edges. This is a necessary structural condition, not a sufficient condition.

For the displayed Toeplitz candidate, n<=2 is unchanged. At n=3 only edge {0,2} changes, so **H_3(f_t)<H_3(f_0) for every 0<|t|<=1/8** follows rigorously from this lemma. The conditional diagonals are r=s=91/200 after eta_1=1 and r=s=109/200 after eta_1=0. The two conditional real edges are 3/200 and 21/200; their imaginary magnitude is 3|t|/50. This is a finite-window exclusion only; n>=4 changes several edges, and the lemma does not settle those windows or the rate.

## Actual bounded batch and observations

The script `phase_probe.py` was executed, not merely defined. Eight predefined centers used p in {1/2,1/4}, a=(2p)(3/10,s_2*3/25,s_3*1/25), with all four (s_2,s_3) in {+1,-1}^2. Each center has a full 3-by-3 imaginary harmonic Hessian computed at n=4,6,8. All 24 computed Hessians were negative definite. These are 8 parameter points, not 8 gauge-inequivalent classes; at p=1/2 particle-hole and gauge symmetries cause repetitions, retained in the denominator.

At the all-positive p=1/2 center, the n=8 Hessian was

    [-1.253696664496, -0.165947265011, -0.032363622254]
    [-0.165947265011, -0.302793494772, -0.046655306371]
    [-0.032363622254, -0.046655306371, -0.063559944619]

with eigenvalues approximately (-1.283119399096,-0.282148649756,-0.0547820550354). For the chosen b=(0,3/25,-1/25), the off-diagonal Q_23 term contributes positively to b^T Q b, but does not overcome its negative diagonal terms.

The fixed candidate was separately enumerated at t=-1/8,0,1/8 for each n=1,...,10: 30 exact-configuration distributions, with 6138 total determinant evaluations. The finite chord gaps H_n(endpoint)-H_n(center) were:

| n | gap (nats) |
|---:|---:|
|1|0|
|2|0|
|3|-5.17852011494568e-6|
|4|-1.04534996165917e-5|
|5|-1.57217521197239e-5|
|6|-2.09939157045369e-5|
|7|-2.62663030579091e-5|
|8|-3.15387361409236e-5|
|9|-3.68111772663937e-5|
|10|-4.20836195864638e-5|

The apparent limiting gap of successive entropy increments is about -5.27244232e-6. That is **not** a certified entropy-rate value, and neither a negative pair-rate exclusion nor the general conjecture follows. The complete numerical values, probability checks, event-derivative checks and actual execution metadata are in `phase_probe_results.json`.

## Failure ledger and minimal remaining obligation

1. Fisher cancellation succeeds exactly, but it leaves an indefinite-sign event acceleration sum. Disappearance of the Fisher term is not a positive-curvature proof.
2. Two independent cycle phases are present and a triangle real product decreases, but the tested full Hessians are negative. Phase variation alone is not a counterexample mechanism.
3. A single imaginary edge is analytically excluded even when it is in a cycle. Restricting to such a perturbation cannot supply a finite entropy counterexample.
4. The selected multiharmonic direction has a positive mixed Hessian contribution, but its radial/single-edge losses dominate at all tested sizes.
5. Finite negative gaps do not prove a negative entropy-rate gap. The smallest missing obligation for a counterexample remains a different fixed feasible scalar candidate plus certified rate bounds whose endpoint lower bound exceeds the center upper bound. This unit supplies neither.
6. The first upload failed because the assigned server subdirectory did not exist; it was created, then the upload and computation completed. The remote command's extra shell exit-code echo was misquoted; the Python run itself wrote COMPLETED/exit_status=0 and returned a complete result. A subsequent standalone rerun with no wrapper is logged separately to establish a clean process exit without changing coverage claims.

No broad scan extension is justified by these results. A possible different unit would target a provable mixed-edge coupling inequality or an explicitly selected near-boundary family whose cycle terms can dominate. No such dominance witness has been established here.

## Source and certification limits

Only [Lyons–Steif, original paper](https://arxiv.org/pdf/math/0204324), Conjecture 9.2 and the relevant beginning of Section 6 and conditional-entropy discussion were read as mathematical sources. The source asks for entropy of the stationary scalar-symbol process, and Section 6 distinguishes upper estimates from the harder lower estimates. The present unit invokes no quantitative rate theorem from that section. These source-derived statements do not constitute a current-status or novelty audit.

The single-edge proof and finite symmetry derivation are author-produced and have not yet received independent verification. No Lean check or interval arithmetic certificate is claimed. No theorem about all symbols, all Toeplitz windows, all imaginary directions, or entropy-rate concavity has been proved.
