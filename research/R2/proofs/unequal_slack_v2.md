# Unequal scalar slacks: audited coefficient and full remainder proof

Author verdict: PROVED for the fixed family below, pending independent
verification. The original informal statement that all multiple-flip events
have higher valuation needs replacement: their absolute baseline probabilities
can be larger than the target scale. The proof below controls their entropy
change instead.

## 1. Frozen statement and feasibility

Fix finite n, 0<r<n, real orthonormal frames U,V with [U V] orthogonal, P=UU^T, Q=VV^T, and a real r-by-d matrix B, d=n-r. Put

    D=UBV^T+VB^TU^T, F=||B||_F^2.

Fix alpha,beta>0, tau>=0 with tau||B||_op<1. For e tending to zero through positive values define

    a=e^alpha, b=e^beta, m=max(alpha,beta),
    t=tau e^(m/2), M=(1-a)P+bQ, K_+=M+tD, K_-=M-tD.

Use exact-event inclusion-exclusion probabilities and natural-log entropy, with Delta=(H(K_+)+H(K_-))/2-H(M). For r-sets S define

    psi_S=det(U_S),
    phi_S=(d/dz)det((U+zVB^T)_S)|_(z=0),
    Z=sum_(|S|=r,psi_S=0)phi_S^2.

Then

    Delta=tau^2[mZ-(alpha+beta)F]e^m log(1/e)+O(e^m).  (1)

All constants depend only on the fixed finite data, including alpha,beta,tau. No uniform assertion for varying frames or exponents is made.

Schur complements give the exact feasibility conditions

    t^2||B||_op^2<=b(1-a),
    t^2||B||_op^2<=a(1-b).                             (2)

Because t^2=tau^2 min(a,b), the strict tau condition makes both inequalities strict for all sufficiently small e. The zero case tau B=0 has K_+=K_-=M and Delta=0 identically. Henceforth assume tau B!=0, so t>0.

## 2. Exact spectral resolution and uniformly comparable rare rates

Take a fixed singular-value decomposition of B and rotate the U,V frames within their respective subspaces. Each paired singular value kappa_j>=0 gives the two-by-two block

    [[1-a, t kappa_j],[t kappa_j,b]].

Set g=1-a-b>0. Its high and low eigenvalues are

    1-a+delta_j, b-delta_j,
    delta_j=(sqrt(g^2+4t^2 kappa_j^2)-g)/2
            =t^2 kappa_j^2/g+O(t^4).                  (3)

Unmatched modes have delta=0. Thus the high-hole rates and low-particle rates are

    h_i=a-delta_i, l_j=b-delta_j,
    sum_i delta_i=sum_j delta_j=t^2F/g+O(t^4).         (4)

The paired modes rotate by the angles theta_j=(1/2)arctan(2t kappa_j/g). Reversing t reverses every angle and leaves every eigenvalue unchanged. In physical coordinates their rotation can be written R(z)=exp(z J_e), evaluated at z=+t or -t. The skew matrix J_e is uniformly bounded for small e, and

    J_e U=VB^T/g+O(t^2).                              (5)

Choose rho with tau^2||B||_op^2<rho<1. Formula (3) gives, for all sufficiently small e,

    0<=delta_i,delta_j<=rho min(a,b),
    (1-rho)a<=h_i<=a, (1-rho)b<=l_j<=b.               (6)

The same bounds hold along the straight rate interpolation

    h_i(u)=a-u delta_i, l_j(u)=b-u delta_j,
    0<=u<=1.

These uniform comparisons cover both the side whose correction is of leading order and the side whose correction is smaller. No expansion requiring t^2/a or t^2/b to tend to zero is used.

## 3. Full-law and entropy estimates used below

The coefficient of z_S in det(I+K(diag(z)-I)) is

    p_K(S)=sum_(T superset S)(-1)^(|T|-|S|)det(K_T).

For an orthogonal eigenvector matrix T with eigenvalues lambda, row expansion followed by Cauchy-Binet gives the exact spectral mixture

    p_K(S)=sum_(J:|J|=|S|)w_J det(T_(S,J))^2,
    w_J=product_(j in J)lambda_j product_(j notin J)(1-lambda_j).  (7)

All weights and squared minors are nonnegative. A pattern with h high holes and l low particles has weight comparable to a^h b^l by (6), with constants uniform in u and in the rotation parameter |z|<=t.

There is also a uniform logarithm bound for every exact event. Each weight in (7) is at least c a^r b^d, because every rare rate is bounded below by (6) and every survival factor is bounded below by a positive constant. For a fixed S, the sum of det(T_(S,J))^2 over all |J|=|S| is 1 by Cauchy-Binet and orthonormality of the rows. Consequently

    p_K(S)>=c a^r b^d,
    |log p_K(S)|<=C[1+log(1/e)].                       (8)

This holds for every interpolated rate kernel and every rotation used in the proof. In particular no individual event is exactly zero at positive e, although its projection-limit coefficient can vanish.

### Rotation estimate for a cardinality class

Keep the endpoint weights fixed and write p_S(z)=sum_J w_J f_(S,J)(z)^2, where f is a rotated minor. All f and its first two z-derivatives are uniformly bounded, since the dimension is fixed and J_e is bounded. Cauchy-Schwarz gives

    (p'_S(z))^2/p_S(z)<=4sum_J w_J(f'_(S,J)(z))^2.

Together with p''_S=2sum_J w_J[(f')^2+f f''] and (8), this bounds the second derivative of the entropy contribution of any set of cardinalities by

    C W [1+log(1/e)],                                 (9)

where W is the total spectral weight of patterns of those cardinalities. For all cardinalities other than r, at least one flip is needed, so W<=C(a+b). Taylor's integral remainder therefore shows that their symmetric rotation entropy difference is

    O(t^2(a+b)[1+log(1/e)])=o(t^2).                   (10)

This bound includes events whose unrotated first-event rate is zero. It does not divide by that rate.

### Rate-change estimates

For the unrotated fixed eigenframes, differentiate the weights in (7) along u. Each differentiated rare or survival factor contributes O(t^2). If a pattern needs at least two flips, its differentiated product still has at least one rare factor unless a survival factor was differentiated, in which case at least two remain. As there are finitely many patterns,

    sum_(patterns with at least two flips)|w'_J(u)|
         <=C t^2(a+b).                               (11)

For all patterns combined the bound is O(t^2). Using (8), entropy changes confined to cardinalities at distance at least two from r are therefore

    O(t^2(a+b)[1+log(1/e)])=o(t^2).                   (12)

Unlike an absolute probability estimate, (11) remains useful when, for example, a^2 is much larger than t^2.

## 4. High-hole cardinality: its logarithm is alpha log(1/e)

Work first in the unrotated fixed eigenframes while varying u. For |S|=r-1 let q_(S,i)>=0 be the rank-r-1 projection probability when high eigenmode i alone is deleted, and let q_S=sum_i q_(S,i).

If q_S>0, the one-hole part of (7), comparability (6), and the finite mixture imply

    c_S a<=p_S(u)<=C_S a,
    log p_S(u)=log a+O(1),                             (13)

uniformly in u. Every one-hole weight has derivative -delta_i+O(t^2(a+b)); patterns with more flips give smaller derivative terms. Their conditional projection laws sum to one. Therefore

    sum_(|S|=r-1)p'_S(u)
         =-sum_i delta_i+O(t^2(a+b)).                  (14)

If q_S=0, every q_(S,i) is zero by nonnegativity; the entire one-hole contribution is identically absent in the unrotated frames. All remaining selections of cardinality r-1 have at least two holes and one particle, hence at least three flips. Their weight derivatives are O(t^2(a+b)^2), in particular covered by the negligible bound (11). Thus deleting the zero-q events from the sum in (14) changes only its error term. Their entropy derivative is controlled by (8), not by assigning them the incorrect log a scale.

Now differentiate -sum p log p, use (13) on positive-q events, and (8) on the remaining events. The all-pattern derivative variation is O(t^2), so the bounded O(1) errors in (13) contribute O(t^2). Integrating u from 0 to 1 yields

    H_(|S|=r-1)(unrotated endpoint spectrum)
       -H_(|S|=r-1)(M)
       =(sum_i delta_i)log a+O(t^2).                  (15)

Replacing the sum using (4), g=1+O(a+b), log a=-alpha log(1/e), and the fact that every positive power of e times log(1/e) tends to zero, gives

    (15)=-alpha t^2 F log(1/e)+O(t^2).                (16)

Adding the symmetric rotation effect (10) does not change this formula. It holds whether alpha equals the maximum exponent or the smaller exponent.

## 5. Low-particle and farther cardinalities

The identical argument with a single added low mode gives

    averaged endpoint minus center entropy on |S|=r+1
       =-beta t^2 F log(1/e)+O(t^2).                  (17)

When a one-particle projection rate is zero, its entire one-particle contribution vanishes in the fixed frames and the next possible selection requires at least three flips; the same zero-rate audit applies. Equations (10)–(12) show that all cardinalities outside {r-1,r,r+1}, together, contribute o(t^2) to the chord entropy difference.

It is not asserted that their absolute probabilities or absolute entropies are o(t^2). For instance alpha=1,beta=3 gives a two-hole baseline of order e^2, larger than the target t^2 of order e^3. What is small is its change along this chord, established by (11)–(12).

## 6. Supported r-events contribute only O(t^2)

For a fixed r-set with psi_S!=0, the no-flip projection probability is bounded away from zero throughout all sufficiently small rotations and rate interpolations. Therefore its entropy is smooth there. Changing the spectrum from the center rates to (4) changes its probability and entropy by O(t^2). At fixed endpoint weights, the average of the +t and -t rotations cancels its linear term; a bounded second derivative gives another O(t^2). There are finitely many supported sets, so their total contribution is O(t^2).

This step uses fixed positive projection probabilities. It does not claim uniformity if the frame itself varies with e.

## 7. Zero r-events and the m log(1/e) layer

For psi_S=0, the rotated high projection has amplitude, from (5),

    psi_S(+-t)=+-t phi_S/g+O(t^2).

Its no-flip weight is 1+O(a+b). Every other eigenmode selection of cardinality r requires at least one hole and one particle, so its combined weight is O(ab). Hence, separately at either endpoint,

    p_(K_+-)(S)=t^2 phi_S^2
                  +O(t^2(a+b)+t^3+ab).               (18)

At the center the no-flip probability is exactly zero and

    p_M(S)=O(ab).                                     (19)

These formulas do not assume phi_S!=0. If it is positive in square, compare the entropy of (18) with f(t^2 phi_S^2); the logarithms of both arguments are O(log(1/e)) by (8) and the explicit power t^2. If phi_S=0, use (8) directly to bound f(p) by C p[1+log(1/e)]. In either case the accumulated error in this comparison, and the center entropy (19), are bounded by

    C[t^2(a+b)+t^3+ab][1+log(1/e)]=O(t^2).            (20)

The last bound is explicit: ab/t^2=e^(min(alpha,beta))/tau^2, while a,b,t are positive powers of e times fixed constants. Thus each error term divided by t^2 remains bounded and in fact tends to zero after its logarithmic factor.

Finally

    f(t^2 phi_S^2)=m t^2 phi_S^2 log(1/e)+O(t^2),

where the fixed logarithms of tau^2 and of nonzero phi_S^2 belong to the O(t^2) term. Summing zero r-events gives

    m t^2 Z log(1/e)+O(t^2).                          (21)

The exterior derivative eta with coordinates phi_S is a sum of orthonormal one-column replacements with coefficients B_ij. Hence ||eta||^2=F and 0<=Z<=F, independently of the two exponents.

## 8. Combination, strict sign, and audit conclusion

Adding (16), (17), (21), and the remaining O(t^2) terms proves

    Delta=t^2[mZ-(alpha+beta)F]log(1/e)+O(t^2),

which is exactly (1) because t^2=tau^2 e^m and tau is fixed. Since Z<=F,

    mZ-(alpha+beta)F<=-min(alpha,beta)F.

Thus tau B!=0 implies a strictly negative gap for all sufficiently small e. This includes equal exponents as a special case and arbitrary positive real, not necessarily rational, exponents.

Audit outcome: the coefficient and strict-sign conclusion are correct. The
remainder obligation is supplied by (6)–(20). Two cautions are substantive:
multiple-flip baseline mass is not always smaller than `e^m`, and a zero
one-flip projection coefficient must not simply be assigned `log a` or
`log b`. Neither issue changes the final formula after the eventwise and
entropy-change estimates above.

## Scope

This is an analytic fixed-family theorem. It makes no novelty claim and no
global-concavity claim.

