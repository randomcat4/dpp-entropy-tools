# Post-publication continuation: nonzero Lambda

This work was done after the first PR60 checkpoint. It does not wait for the r=0 computation or for review of the all-r proof.

Status: **PROVED (author proof, independent review pending)** for the conditional-entropy theorem and the explicitly quantified band below. **DISPROVED (author exact certificate)** for the fixed-diagonal radial-monotonicity sufficient condition in section 3, not for DPP entropy concavity. The general missing-edge Schur inequality remains **INCOMPLETE**. Novelty is separate and unassessed.

## 1. Stronger consequence on the entire Lambda-zero family

Let C(K)=H(X3|X1,X2) for the complete three-point DPP law. At every strict connected missing-edge Lambda-zero center in proof.md, C has strictly negative Hessian in all six nonzero real symmetric directions, including directions creating K12.

**Proof.** C=H3-H12. The leaf marginal kernel is diag(x,y) along the entire u-path. At this diagonal two-point center, the complete-event Hessian is

    -H12''(D)=D11^2/v+D22^2/w.

This includes a possibly nonzero D12: its one-event first scores vanish and the second-event terms cancel under the product log weights. This is also obtained immediately from the four inclusion-exclusion probabilities xy-a^2, x(1-y)+a^2, (1-x)y+a^2, (1-x)(1-y)-a^2 at a=0.

The displayed leaf Hessian is independent of u in the fixed direction coordinates of proof.md (2). Thus the radial derivative of -C'' is exactly the same positive definite M proved there. At u=0 the conditional negative Hessian matrix is diag(0,0,4,0,0,0). Integration of M in those fixed physical coordinates therefore gives -C''>0 for every nonzero direction. No restriction of D to the arrow tangent space has been made. This proves the assertion.

## 2. A quantified, parameter-dependent Lambda-nonzero band

This is a distinct subtheorem, not a replacement of the full general-arrow target.

Fix any connected strict Lambda-zero arrow center K0. Use the notation x,y,A,B of proof.md and put

    q0=(1-A-B)/2>0,
    pstar=min_S p_S(K0)>0.

Let T0 be the six-by-six matrix of -C''(K0) in a Frobenius-orthonormal basis of real symmetric matrices: E11,E22,E33 and (Eij+Eji)/sqrt(2). It is explicitly determined from the eight probabilities and their first/second derivatives by (6), subtracting the displayed leaf marginal Hessian. Define the following positive, finite, center-dependent quantities:

    alpha=det(T0)/(tr(T0))^5,
    m=pstar/2,
    L=8*(10/m+3/m^2+log(1/m)),
    rho=min(q0/2,pstar/2,alpha/(2L)).                     (25)

Then for every real delta with |delta|<=rho and every real symmetric D,

    -C''(K0+delta E33;D) >= (alpha/2)||D||F^2,             (26)
    -H3''(K0+delta E33;D)
       >= (alpha/2)||D||F^2+D11^2/v+D22^2/w.              (27)

The center stays strictly legal. Every nonzero delta in this interval has Lambda != 0, since q becomes q0+delta and Lambda=0 is equivalent to q=q0. Thus (25) is a genuine nonempty nonzero-Lambda band around every center covered by the main theorem, including strongly coupled, unequal-diagonal centers. No uniform width is asserted.

**Proof.** By section 1 all eigenvalues of T0 are positive. If lambda_min is its smallest eigenvalue, det(T0)<=lambda_min*(tr(T0))^5, so T0>=alpha I. The two arrow Schur complements after the delta shift are q0+delta and q0-delta. The condition |delta|<=q0/2 makes both strictly positive.

Here are explicit bounds for differentiating the FULL Hessian. Inclusion-exclusion is equivalently

    p_S(K)=(-1)^(3-|S|) det(K-Pi_(S-complement)),

where Pi is the coordinate diagonal projection. On a strict kernel, the symmetric matrix inside the determinant has operator norm at most one. For ||D||F=1 and E=E33, write

    a=p_D, b=p_DD, c=p_E, f=p_DE, g=p_DDE.

The following bounds hold at every point of the delta segment:

    |a|<=sqrt(3), |b|<=2, |c|<=1, |f|<=2, |g|<=1.        (28)

For a, use p_D=+/-tr(adj(A)D) and ||adj(A)||F<=sqrt(3). For b and f, diagonalize A only to estimate the determinant differential: the diagonal-coordinate block of Hess(det A) has row sums of absolute values at most two, while its Frobenius-normalized off-diagonal block has eigenvalues of absolute value at most one. Hence the bilinear operator norm is at most two. This norm calculation does not replace the observation-basis event law by a spectrally rotated law. For c, the exact event derivative in K33 is plus or minus the corresponding leaf probability, at most one. Finally g=+/-2 det(D_{12}), whose absolute value is bounded by D11^2+D22^2+2D12^2<=1.

All atoms are affine in delta, and |c|<=1 implies p_S>=pstar-|delta|>=m. The full negative entropy Hessian derivative is exactly

    d_delta[-H3''(K;D)]
      =sum_S [2af/p-a^2 c/p^2+g log p+bc/p].              (29)

No summand or rare event is removed. Equations (28), p>=m and p<=1 bound its absolute value by

    8*((4sqrt(3)+2)/m+3/m^2+log(1/m)) <= L.

The leaf Hessian is constant in delta, so the same bound applies to -C''. Integrating (29) and using |delta|<=alpha/(2L) yields (26); adding the exact leaf marginal form gives (27).

All entries in T0, hence all quantities in (25), have explicit finite formulas from the exact atoms. Interval evaluation may be used to obtain numerical certified radii for rational centers, but numerical evaluation is not required for the analytic quantifiers of this theorem. The radius intentionally tends to zero in possible degenerations; this is not the previously disproved uniform safety margin.

## 3. A natural full-arrow radial extension is false

The theorem in proof.md follows a specific Lambda-zero center path whose third diagonal changes with u. A tempting replacement is to keep all three diagonals fixed and scale only the two existing edges. That replacement does NOT make the full negative Hessian Loewner-monotone throughout all legal arrow kernels.

Set

    K*=[[11/100,0,33/500],
        [0,1/200,3/1000],
        [33/500,3/1000,199/200]],

    D*=[[0,-1,0],
        [-1,-1/50,2/25],
        [0,2/25,0]],

    C*=K*-diag(K*), K(s)=diag(K*)+s C*.                  (30)

Both K* and I-K* are strictly positive definite. The complete legal radial interval is

    |s| < sqrt(442775/434223),                            (31)

which contains [999/1000,1001/1000]. This follows from the two scalar Schur complements, taking the smaller of

    z/(b0^2/x+c0^2/y),
    (1-z)/(b0^2/(1-x)+c0^2/(1-y)).

The exact eight-event law at s=1, in mask order (0,1,2,12,3,13,23,123), is

    p=(1069,61006,106,319,11068306,1307119,55519,6556)
       /12500000.

In particular

    exp(Lambda)=65729622186464/3466472577089 > 1.          (32)

Define Mtilde=(d/ds)[-Hess H(K(s))] at s=1, with D* a fixed affine entropy direction. Its value on D* is

    Mtilde(D*,D*) = R - (66/3125) log(65729622186464/3466472577089),

where the exact rational term is

    R=62198092976944951510582016487593946984085346423771060505
      /1445745402739430543847620534728498621094597199216967098368.

The rigorous enclosure is

    [-0.01912227459137764707182987490765265,
     -0.01912227459137764707182987490765264] < 0.          (33)

Thus this fixed-diagonal full-arrow radial sufficient condition is false. This does not contradict Theorem 1, whose center path and Lambda-zero quantifiers are different.

### Complete derivative and certificate derivation

Form ALL eight inclusion-exclusion polynomials

    p_S(epsilon,delta)=p_S(K*+epsilon D*+delta C*).

At epsilon=delta=0 take

    p=p_S, a=p_epsilon, b=p_epsilonepsilon,
    c=p_delta, f=p_epsilondelta, g=p_epsilonepsilondelta.

Then -H''(K*;D*) is sum(a^2/p+b log p), and (29) is exactly Mtilde(D*,D*). This derives (33) from the true K-affine event jets, including the mixed triple derivatives. The coefficient g over all eight atoms pairs with the full cube log (32); it is not obtained by deleting events. The source `continuation_exact.py` reconstructs and emits the entire eight-by-six jet table from (30), without importing the main certificate or an older verifier.

For every positive rational log argument, write q=2^k y with 1<=y<2 and w=(y-1)/(y+1). With N=60,

    0 <= log y - 2 sum_(j=0)^(N-1) w^(2j+1)/(2j+1)
       <= 2w^(2N+1)/[(2N+1)(1-w^2)].                    (34)

The same formula at y=2 bounds log2. Scaling by a negative integer k reverses interval endpoints. All sums and errors in the code are rational, and decimal endpoints are rounded outward. The tail inequality is the positive atanh series with every remaining denominator bounded below by 2N+1.

### Actual entropy and legal three-kernel check

The true entropy curvature for the same K*,D* has the concave sign:

    -H''(K*;D*) in
    [0.09085487822146532947682573934164664,
     0.09085487822146532947682573934164665].               (35)

With tau=1/100000, the three exact kernels K*-tau D*, K*, K*+tau D* and their complements pass strict rational Sylvester checks. Convexity of 0<K<I makes the entire segment legal. Their COMPLETE entropy Jensen difference is

    (H(K*-tau D*)+H(K*+tau D*))/2-H(K*) in
    [-0.00000000000454275478584750276044882,
     -0.00000000000454275478584750276044881] < 0.          (36)

Therefore (30) is neither a strict DPP entropy counterexample nor a positive-Jensen candidate for C2. Only the auxiliary monotonicity assertion is disproved. The exact run actually completed and ended `ALL POST-CHECKPOINT EXACT CHECKS PASSED`.

Discovery used a bounded double-precision scout, followed by differential evolution with seed22603, population factor12 and at most160 iterations; it stopped after4020 evaluations. Those floating values are not used in (31)–(36). The rational center and simple direction (30) were reconstructed and checked independently by the exact event formulas and log enclosures above.

## 4. A new one-sided perspective bridge for the remaining problem

The following identities are proved here; the convexity obligation they expose is still INCOMPLETE. This route does not discard the third-bit-zero events.

For a strict kernel let Pij=pij0+pij1 and define

    G1(K)=sum_(i,j) pij1 log(pij1/Pij).

Complementing all three coordinates merely permutes the leaf outcomes, so exactly

    -H(X3|X1,X2)=G1(K)+G1(I-K).                           (37)

Both one-sided terms must be retained. At an arrow center set tij=q+A(1-i)+B(1-j) as before, let Tij be its derivative in an arbitrary physical direction, and put

    ell0=log(t00/t10), k0=log(t00/t01),
    v1=log(t10*t01/(t00*t11))>0.

Differentiating the perspective r log(r/P), using sum pij1''=0, gives

    G1'' = sum Pij Tij^2/tij + sum pij1'' log tij
                               -sum Pij'' tij.

Here Pij''=2 det(D12)(-1)^(i+j), while tij is additive in i,j. The last sum is therefore exactly zero. Collecting the remaining complete jets by q13,q23 and det K yields

    G1''(K;D)=F1(D)-2 tr(N1 adj D),
    F1(D)=sum_(i,j) Pij Tij^2/tij,
    N1=diag(k0,ell0,0)+v1 K > 0.                         (38)

The four terms of F1 include the complete triple event; its complementary four terms enter through (37). N1 positivity does NOT alone prove (38) nonnegative, just as the analogous full-Fisher structural inference was previously insufficient.

There is a useful exact scale reduction. Congruence by S_l=diag(1,1,sqrt(l)) sends each pij1 to l*pij1 and leaves Pij unchanged, so

    G1(S_l K S_l)=l G1(K)+l log(l) K33,
    G1''(S_l K S_l;S_l D S_l)=l G1''(K;D).               (39)

This is a kernel congruence with its correct transformed function and direction, NOT an entropy-invariant spectral rotation. The second term in the first identity is affine in K and hence has zero Hessian. Taking l=1/q normalizes q to one. Thus the stronger one-sided nonnegativity problem can be studied on four shape variables

    0<x,y<1, A/q>0, B/q>0,

without an upper restriction q+A+B<1 on the auxiliary positive masses. At such arrow centers all four pij1 and all four Pij are positive; these formulas define a local perspective function even when it is not itself a normalized DPP law. A proof of its convexity on this auxiliary domain would, through (37)–(39), close the full original arrow conditional-entropy problem. No such proof is asserted here.

This bridge removes one scale and fixes the one-sided three-way-log sign, but the remaining obligation is the actual coupled inequality

    F1(D) >= 2 tr(N1 adj D) for every real symmetric D,

not merely N1>0 or several good rank-one directions. It is an alternative to the general five-parameter logarithmic Schur inequality, not a conclusion from finite non-hits.

## 5. Final remaining scope

The full Lambda-zero M and entropy Hessian theorem is the main completed author result. This continuation additionally proves full-six-direction conditional strictness and the adaptive nonzero-Lambda band (25). It also gives the strict method obstruction (30)–(36) and the exact one-sided scale bridge (37)–(39).

The general Lambda-nonzero Sfull>=0 inequality outside the band, the stronger one-sided inequality in (38), and the general real three-point theorem remain INCOMPLETE. No strict positive entropy Jensen counterexample has been found or certified. No claim in this continuation upgrades itself to independent review or to a novelty result.
