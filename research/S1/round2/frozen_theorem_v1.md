# Round 2 frozen contract: non-even centres and general affine directions

Status: frozen by the route owner under the second-round dispatch. Proof and review tasks must not alter the premises. The round-one theorem and certificates remain unchanged.

## Objects and original goal

For a fixed real measurable scalar f:T=R/Z->[0,1], let c_k=integral f(x) exp(-2 pi i k x) dx, K_f(i,j)=c_(i-j), and H_n(f) be the exact configuration entropy of sites 0,...,n-1, using natural logs. The stationary entropy rate h(f)=lim H_n(f)/n exists. The original target is h((f_-+f_+)/2)>=(h(f_-)+h(f_+))/2 for every fixed pair. Neither window-dependent symbols nor matrix-valued block symbols are permitted.

## New exploratory subfamily

Fix m in {3,4}, rational p,a_k,b_k,d_p,d_a,k,d_b,k, a positive rational tau, and

    f_t(x)=p+t*d_p+sum_k [(a_k+t*d_a,k)cos(2 pi k x)+(b_k+t*d_b,k)sin(2 pi k x)].

Require a rational epsilon>0 proving epsilon<=f_t<=1-epsilon for every |t|<=tau. The three symbols f_-tau,f_0,f_tau are fixed independently of n and of the past truncation. The centre has a nonremovable cycle phase: no single circle translation makes all its active Fourier coefficients real. Thus merely translating an old even centre does not meet the new attack's intent.

The old even-centre/odd-direction restriction is explicitly lifted. Both cosine and sine directions, and a mean direction, may vary simultaneously. Endpoints need not be reflected/conjugate or share mean. All three entropies and all three rate intervals must be evaluated individually.

## Finite diagnostic and certification gates

Exact events are signed determinants of K-diag(zeros), not inclusion minors alone. For an affine direction, retain both terms

    H_n''=-sum p_omega'' log p_omega - sum (p_omega')^2/p_omega.

The second term is the nonnegative Fisher cost with a minus sign. It may vanish in some directions but cannot be assumed zero at a non-even centre.

Define Delta=(h(f_-tau)+h(f_tau))/2-h(f_0). A counterexample requires (L_-+L_+)/2-U_0>0; exclusion of one selected pair requires (U_-+U_+)/2-L_0<0. Finite positive curvature does not settle either rate sign. No derivative-limit interchange, finite-order Markov assertion, or identical-endpoint shortcut is allowed.

## Bounded first units

The entire first centre batch contains at most 24 centres, including the main baseline. Test windows n=6,8. n=10 is reserved for a frozen candidate or a stated mechanism check. Initial CPU calculations use one thread per active numerical job, preferably no more than two jobs simultaneously, within the route's 8 CPU/32 GiB cap; no GPU. Exact counts, seeds, commands, source/input hashes, PID and exit state are saved.

The main instance owns the three-symbol baseline and any final claim. The phase task constructs a predeclared non-even batch; the rate task adapts the existing certificate only as needed for the three fixed symbols; the review task independently checks definitions, feasibility, gauge invariants and exact events, then audits frozen non-authored claims. Children do not delegate. A claimed open-problem solution requires two fresh non-author reviewers; scoped exclusions must not be presented as such a solution.

## Sources and non-claims

Lyons–Steif Conjecture 9.2 and Section 6 remain the semantic and conditional-entropy sources. Fan–Liao–Qiu Theorem 1.2 controls separated-block psi-mixing under a spectral margin and a Fourier-tail condition; it does not by itself control dependence after conditioning on an intervening block. The reviewed round-one infinite-past residual proofs may be reused with their hypotheses checked independently for all three symbols.

Two substantively different units returning to the same unexplained mixed-edge gap, or a clear absence of a mechanism, trigger a new STOPPED_SUBSTANTIVE checkpoint. Do not expand the same finite scan to keep busy. Correctness, finite diagnostic coverage, rate certification and novelty remain separate.
