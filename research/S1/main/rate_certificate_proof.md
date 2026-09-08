# Negative entropy-rate gap for the frozen baseline

Status: complete author candidate with executed exact/interval arithmetic; independent review pending. This excludes one fixed pair as a counterexample. It does not prove the conjecture or a universal negative-curvature statement.

## Fixed claim

For the rational symbol in ../baseline_candidate.json, t=+-1/4 and t=0, with natural-log entropy rate,

    -0.00002621 < (h(f_(-1/4))+h(f_(1/4)))/2-h(f_0) < -0.00002605.

The displayed decimal endpoints are deliberately wider than the rational enclosure in rational_rate_n8.json. The uniform symbol margin is epsilon=3/50. Reflection/conjugation gives equality of endpoint laws, so only t=0 and t=1/4 require separate calculations.

## 1. Extreme-past enclosures

Use the construction and proof in boundary_residual_proof.md, with M=64. Its rational dyadic proposals, exact full half-line residual bounds and approximate future corner matrices are in boundary_residual_M64.json. Applying the construction to f gives the all-one past conditioned future kernel. Applying it to 1-f and complementing gives the all-zero past conditioned future kernel. Both true kernels lie between epsilon I and (1-epsilon)I. Their approximate kernels A differ in operator norm by at most the recorded rational delta, supported in their first three coordinates.

The numerical solve is not trusted: the proof only uses the exact residual of its dyadic rational output. The script must and does check all M+m rows of that residual. Its entries vanish identically outside this range by bandwidth.

## 2. Uniform error of a conditioned one-site probability

For a Hermitian kernel Q with a strict spectral margin a>0, conditioning on a finite pattern gamma on sites P gives

    q(Q,gamma)=Q_(vv)-Q_(vP) [Q_(PP)-diag(1_(gamma=0))]^(-1) Q_(Pv).

To bound the inverse, set E=Q_(PP)-diag(1_(gamma=0)) and J=diag(2 gamma-1). The Hermitian part of JE is the block diagonal matrix with blocks Q_(ones,ones) and I-Q_(zeros,zeros), each >=a I. Thus

    a||z||^2 <= Re <z,JEz> <= ||z|| ||Ez||,

and ||E^(-1)||<=1/a, despite E being indefinite.

Interpolate between the true extreme kernel and A. Every interpolated kernel has margin at least epsilon-delta and operator norm at most 1+delta. Differentiating the displayed Schur complement in a Hermitian direction V gives w*Vw, where w has P-coordinates -E^(-1)Q_(Pv) and target coordinate 1. Therefore

    |q(A,gamma)-q(true,gamma)|
      <= delta [1+((1+delta)/(epsilon-delta))^2] =: e.

All constants are rational. No lower bound on the probability of the conditioning pattern is required beyond strict positivity. This estimate is uniform over its length and pattern. The derivative here is a finite-matrix identity on a uniformly interior segment, not an entropy-rate derivative.

## 3. Genuine entropy-rate inequalities

Let gamma be the observed last n bits before the target and w_gamma its ordinary stationary probability. Let q_1(gamma),q_0(gamma) be the target probabilities when every earlier bit is respectively one or zero, defined by the infinite-past limits above. Conditional negative association makes the target probability nonincreasing in each additionally specified past bit. Passing to the extreme limits and to the usual conditional-probability martingale yields, almost surely conditional on gamma,

    q_1(gamma) <= P(X_target=1 | entire past) <= q_0(gamma).

This is the extreme conditioning argument of Lyons–Steif Section 6 (Proposition 2.6 and the method of Proposition 6.10); it concerns conditional probabilities of a single fixed stationary process.

Compute exact rational Schur probabilities qtilde_1,qtilde_0 from the approximate kernels, and their rational error bounds e_1,e_0 from Section 2. Set

    l_gamma=max(epsilon,qtilde_1-e_1),
    u_gamma=min(1-epsilon,qtilde_0+e_0).

The true entire-past probability lies in this interval. With b(s)=-s log s-(1-s)log(1-s), concavity of binary entropy and the stationary conditional-entropy formula give

    L=sum_gamma w_gamma min(b(l_gamma),b(u_gamma)) <= h(f),
    h(f) <= U=sum_gamma w_gamma b(P(X_target=1 | gamma)).

Only a finite conditioning partition is summed. No derivative, asymptotic fit, or numerical window limit is used. Thus a positive value of L_endpoint-U_center would be a counterexample; here U_endpoint-L_center is strictly negative.

## 4. Exact arithmetic and outward log evaluation

For n=8, rational_rate_certificate.py enumerates all 512 exact configurations of nine sites for each of three kernels (ordinary, approximate all-one, approximate all-zero) and for both parameters t=0,1/4: 3,072 integer Bareiss determinants in total. After a common-denominator scaling, every complex Bareiss division is checked for exact integer divisibility. Hermitian determinants are required to have imaginary part exactly zero. Every event probability is a positive Fraction and normalization is checked as exact equality to one for each distribution.

The resulting probabilities, conditional ratios, weights, l_gamma and u_gamma are rational. Binary entropies are evaluated with mpmath interval logarithms at 45 decimal digits. Rational inputs are converted through interval numerator/denominator division. The dyadic endpoints of every interval are read back as Fractions; the minimum of endpoint-entropy intervals is enclosed by the minimum of lower endpoints and the minimum of upper endpoints. Summation and multiplication use interval arithmetic. The final gap subtracts the outward upper centre bound from the outward lower endpoint bound, and vice versa.

The computation produced

    gap_lower = -299206482628470082967984166428661599036439
                /11417981541647679048466287755595961091061972992,
    gap_upper = -148727663748433704622488410027642662541253
                /5708990770823839524233143877797980545530986496.

Both rational endpoints are strictly negative. These are bounds for the true entropy-rate difference, conditional on the mathematical and implementation audit of the chain above. The only pre-existing theorem used for this certificate is the standard DPP conditioning/negative-association framework and stationary entropy formula; the coarse T2 bound is not used in this certificate.

## Limits

The result treats one fixed, uniformly interior, degree-three affine symbol pair. It says nothing about another coefficient choice, all odd perturbations, rational symbols of unbounded degree, boundary symbols or the conjecture's full measurable class. No novelty or formal-kernel verification is claimed. The failed positive-mechanism batches remain in phase/ and are not promoted to a family theorem.
