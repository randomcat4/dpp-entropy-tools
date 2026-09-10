# A continuous true-entropy-rate interval, not sampled points

Status: PROVED (AUTHOR PROOF WITH EXECUTED AUTHOR CERTIFICATE), PENDING_REVIEW.
Date: 2026-09-10. The full interval [1/2,3/2] is NOT claimed.

## 1. Exact statement and unchanged physical path

For the complete occupation Shannon entropy rate per original lattice coordinate, with natural logarithms, let

    f_t(theta)=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8.

Then

    h''(t)<-1/4000 for EVERY t in J=[49/40,51/40].                 (1)

In particular h(t)+t^2/8000 is strictly concave on J. For distinct t0,t1 in J and 0<lambda<1,

    h((1-lambda)t0+lambda*t1)
       -(1-lambda)h(t0)-lambda*h(t1)
    > lambda*(1-lambda)*(t1-t0)^2/8000.                           (2)

The same statements hold on -J by the explicit gauge at the end. There is no assertion on the convex hull of J and -J. This unit uses no fixed point sign from PR77, no entropy extrapolation, no finite-difference derivative of an invariant law, and no positive-curvature entropy counterexample.

The original K_t has diagonal1/2, distance-one entry t/16 and distance-two entry1/8. Thus t remains the genuine affine correlation-kernel parameter. The polynomial approximations introduced below are only test observables, not replacement symbols or kernels.

## 2. Exact response gate being used

Write q=t/16, b=1/8, alpha=(a,c) in {-1,+1}^2,

    D_alpha=[[a/2,q],[q,c/2]], E=[[b,0],[q,b]],
    F_alpha(Q)=D_alpha-Q,
    g_alpha(Q)=ac det F_alpha(Q),
    T_alpha(Q)=E F_alpha(Q)^(-1) E^T,
    L_t A(Q)=sum_alpha g_alpha(Q) A(T_alpha(Q)),
    B_t(Q)=-sum_alpha g_alpha(Q) log g_alpha(Q).

The state domain is the parameter-independent ball B={Q symmetric: ||Q||_2<=1/8}. All four weights, including rare branches, are included. The signed complete-event Schur chain identifies these weights as actual conditionals, with no-future seed0; h=(1/2)eta_t B_t. The factor1/2 is per original site, not per cell.

The exact response machinery and its detailed proofs are preserved byte-for-byte from PR91@c7a072ec4eea0c5b0f445bca5796873a9e234948 under dependencies/pr91/. They are dependencies, not newly claimed discoveries or inherited independent numerical acceptance. The relevant gate, rechecked below at the level of all finite rational constants, is:

    r0=B-c0-(I-L)u,
    r1=B_t+L_t u-c1-(I-L)v,
    A=B_tt+L_tt u+2 L_t v,
    r2=A-c2-(I-L)w,

    |h''-c2/2| <= e02/2+(9/100)e12+e20/2,                        (3)

where e02 bounds ||D_Q^2 r0||, e12 bounds ||D_Q^2 r1||, and e20 bounds |r2| on the ENTIRE state ball. In these equations B_t denotes a parameter derivative, and L_t in derivative positions denotes the parameter derivative of L while holding its test observable fixed. No derivative of polynomial coefficients is silently included in those operator derivatives.

For clarity, the exact error behind (3), before inequalities, is

    2h''-eta A = eta L_tt R r0
                  +2 eta L_t R r1
                  +2 eta L_t R L_t R r0.                        (4)

The last term is the nested stationary-law response, not a Fisher fragment. The dependency proof keeps state motion, prediction acceleration and full invariant-law response. It identifies the full Fisher rate separately; fixed-Q partial scores are never renamed full conditional scores.

The constants used from that proof are k=34/81, r=32/9, M=19/160,

    beta=k+2M=4259/6480<2/3,
    gamma=k^2+4kM+2krM+2M^2=63677321/83980800<19/25.

Thus the centered resolvent has first-derivative bound3 and state-Hessian bound25/6. Put

    CtH=(7/64)M^2/2+M/6,
    CttH=M^2/64+2(7/64)M/6+1/36+M/8,
    CgradH=(3/8)M^2/2+(7/64)kM+M/3+k/6+M/2.

The coefficients for e02 and e12 in (4), after division by2, are at most

    (25/12)[CttH+2(9/50)*3*CgradH]
       =9762629/19660800<1/2,
    (25/6)CtH=202141/2359296<9/100.

These exact rational comparisons are actually executed in interval_certificate.py. The uniform positivity, coding, resolvent and response arguments remain part of the combined proof obligation for independent review; an author run does not itself review those analytic arguments.

## 3. Three original trials become one residual and its derivatives

The literal degree10 coefficients are the original PR91 scout, now accurately public in PR98@55649309437a78d9e5174386d8d260a4ee9c02a1. The four JSON input objects are included unchanged under input/degree10/. Each finite decimal is interpreted as an exact rational coefficient, not as a claimed approximation enclosure for an unknown solution. No coefficient was refitted for this theorem.

There are285 nonconstant monomials (8Q11)^i(8Q22)^j(8Q12)^k. Let u0,v0,w0 and c0,c1,c2 be the three polynomials and Poisson constants in those files. Let tau=t-5/4 and define

    u_tau=u0+tau*v0+(tau^2/2)*w0,
    v_tau=v0+tau*w0,  w_tau=w0,
    c0(tau)=c0+tau*c1+(tau^2/2)*c2,
    c1(tau)=c1+tau*c2.

Set the single analytic residual

    R(Q,tau)=B_t(Q)-c0(tau)-(I-L_t)u_tau(Q).                    (5)

Ordinary total differentiation of (5), using u_tau'=v_tau and v_tau'=w0, gives EXACTLY

    r0=R, r1=partial_tau R, r2=partial_tau^2 R.                 (6)

This is the useful entropy-specific cancellation in the implemented certificate. It creates a single common analytic series, rather than separately fitted values or numerical derivative estimates. The fixed constant is

    c2/2=-6660155061088431/2000000000000000000.                 (7)

## 4. Exact state domain and monomial supremum

Use coordinates

    U=4(Q11+Q22), V=4(Q11-Q22), W=8Q12,
    Q=[[U+V,W],[W,U-V]]/8.

The state ball is exactly

    |U|+sqrt(V^2+W^2)<=1.                                     (8)

The Frobenius norm of a state displacement is sqrt((dU^2+dV^2+dW^2)/32); hence a Hessian in U,V,W is multiplied by32 to obtain the state-Hessian operator norm in the Frobenius metric.

For nonnegative i,j,k, n=i+j+k and r=j+k, the squared maximum of |U^i V^j W^k| on (8) is

    i^(2i) r^r j^j k^k / n^(2n),                              (9)

with the usual0^0=1 convention and constant monomial bound1. To prove (9), first maximize V^j W^k on its Euclidean circle, then maximize |U|^i (1-|U|)^r. The program bounds the square root by exact integer square-root arithmetic at denominator2^80, rounded upward. This is a complete-domain bound, including the boundary, not a sample or rectangular substitute.

We retain state total degree <=N=42 and tau degree <=M=18 in (5). For each retained term, differentiate exactly as a monomial, apply (9), and multiply by |tau| powers bounded at h=1/40. Absolute upper bounds for all entries of D_Q^2R and D_Q^2R_tau are summed. For their nonnegative symmetric entry matrices C0,C1, the rational positive vectors

    w0=(1,4/5,11/10), w1=(1,3/5,1)

give the norm upper bounds max_i (Cj wj)_i/(wj)_i. This follows from the induced weighted supremum norm and Perron comparison; it is not a numerical eigenvalue estimate. Every matrix entry and final weighted-row fraction is retained in run01/certificate.json. The analogous absolute monomial sum bounds R_tautau directly.

## 5. Coefficients: exact preprocessing and outward recurrences

Let x=(U+V)/8, y=(U-V)/8, z=W/8 and q=5/64+tau/16. All g_alpha coefficients and all coefficients of N_i=8 g_alpha T_alpha,i are dyadic with common denominator4096. They are derived from the DIRECT two-by-two determinant and adjugate:

    u=a/2-x, v=c/2-y, w=q-z,
    g=ac(uv-w^2),
    N1=8ac b^2 v,
    N2=8ac(q^2 v-2bqw+b^2u),
    N3=8ac(bqv-b^2w).                                         (10)

For a degree10 trial A with no constant monomial,

    g A(T) = [sum_ijk A_ijk N1^i N2^j N3^k g^(10-i-j-k)] / g^9. (11)

The numerator is formed with exact Python integers after clearing the common decimal coefficient denominator and4096^10. Thus cancellation in its polynomial numerator occurs before any floating interval operation.

On the lower set of retained exponents e, division by g uses

    (P/g)_e = [P_e-sum_(0<f<=e) g_f (P/g)_(e-f)]/g_0.          (12)

For ell=log g, the Euler identity g E(ell)=E(g) gives, for total degree |e|>0,

    ell_e=g_e/g0
          -sum_(0<f<=e) g_f (|e|-|f|) ell_(e-f)/(g0 |e|).       (13)

The nonconstant terms in (12),(13) only use previously computed coefficients. State-degree-first, then tau-degree ordering is compatible with every nonconstant exponent of g. Terms outside the retained lower set cannot influence a retained coefficient.

There are only two logarithm arguments at the origin:999/4096 and1049/4096. Decimal.ln is evaluated at precision100 using its documented correctly rounded nearest contract, then widened by1e-90. The log magnitudes are below2, so both logarithm rounding and the subsequent Decimal widening arithmetic have absolute errors at most1e-99;1e-90 exceeds their combined effect. The widened rationals are then converted to enclosing binary64 endpoints using exact Fraction comparisons.

Every subsequent floating addition, subtraction, multiplication by a signed scalar and division by the positive exact dyadic g0 is widened with nextafter toward the outer infinity immediately AFTER that elementary operation. The program does not use a BLAS reduction or floating matrix eigenvalue. Under IEEE754 binary64 elementary arithmetic, the adjacent floating neighbors enclose the exact result, including subnormal results. Overflow/invalid/divide-by-zero raise; every final coefficient endpoint is checked finite and ordered. Upward absolute products are accumulated by converting each binary64 value to its exact integer ratio and using a common2^1074 denominator, so the long positive reductions have NO rounding loss.

This is a trusted arithmetic implementation contract, not formal verification of Python, NumPy, libmpdec or the CPU. Independent reconstruction remains requested. A separate executed author checker verifies24 exact composition identities in (11) against direct rational matrix inverses and636 retained inverse/log coefficients against an independent finite geometric-series construction. It does not simply rerun the production loop.

## 6. Analytic control of every omitted term

For complex symmetric Q with ||Q||_2<=1/4 and complex |tau|<=1/4, |q|<=3/32. Singular-value estimates give

    sigma_min(D_alpha-Q)>=5/32,
    ||D_alpha-Q||_2<=27/32,
    ||(D_alpha-Q)^(-1)||_2<=32/5,
    ||E||_2^2<=||E||_F^2<=41/1024,
    ||T_alpha||_2<=41/160.

Consequently

    25/1024<=|g_alpha|<=729/1024<3/4,
    ||D_Q g_alpha||<6/5, ||D_Q^2 g_alpha||<=1,
    ||D_Q T_alpha||<=41/25,
    ||D_Q^2 T_alpha||<=2624/125<21.                            (14)

All derivative operator norms here use Frobenius state directions. The complex extension is used only for analytic bounds, not as a probability distribution.

An analytic logarithm can be chosen as

    log g_alpha=log(1/4-ac q^2)
                  +tr log(I-D_alpha^(-1)Q).

The first term has modulus <3/2. The second has modulus <=2log(13/5)<2, because ||D_alpha^(-1)Q||<=8/13. Thus |log g_alpha|<7/2. In particular

    |B|<=21/2,
    ||D_Q^2 B||<256,                                          (15)

the latter from four times [(6/5)^2/(25/1024)+7/2]; sum D_Q^2g=0 cancels the extra constant in the entropy derivative.

Let a_e=|u0_e|+|v0_e|/4+|w0_e|/32 and, for j=0,1,2, define the EXACT polynomial majorant

    P_j(R)=8^j sum_(|e|>=j) a_e (|e|)_j (8R)^(|e|-j).

Here (n)_j is the falling factorial. On the above complex domain, the program computes exactly

    M0=21/2+|c0|+|c1|/4+|c2|/32+P0(1/4)+3P0(41/160)<16,

    MH=256+P2(1/4)
       +4[P0(41/160)+2(6/5)(41/25)P1(41/160)
            +(3/4)((41/25)^2 P2(41/160)+21P1(41/160))]<4096.    (16)

Therefore |R|<16 and ||D_Q^2R||<4096 throughout that COMPLEX domain. No coefficient sign or scout residual is used to guess either bound; the exact majorant fractions are in the output.

For each real Q in B apply two-variable Cauchy to R(lambda Q,tau) on |lambda|<=2, |tau|<=r=1/4. State-degree j terms have coefficient bound16*2^(-j)*r^(-l). For the state Hessian use4096*2^(-(j-2))*r^(-l), since two state derivatives lower the homogeneous degree by2.

Let a=h/r=1/10 and k=M+1. Put

    T0=a^k/(1-a),
    T1=a^(k-1)[k/(1-a)+a/(1-a)^2],
    T2=a^(k-2)[k(k-1)/(1-a)+2ka/(1-a)^2+2a^2/(1-a)^3].

Summing the two omitted regions (state degree>N or tau degree>M), with harmless double counting at their intersection, gives

    tail02=4096[2^(-(N-2))/(1-a)+2T0],
    tail12=(4096/r)[2^(-(N-2))/(1-a)^2+2T1],
    tail20=(16/r^2)[2^(-N)*2/(1-a)^3+2T2].                    (17)

At N42,M18 these are, respectively,

    6357830174143/1536000000000000000000,
    6358069249471/345600000000000000000,
    6436251076031/39813120000000000000000.

This proves the error for all omitted terms and all |tau|<=1/40. Differentiating a value-only real bound is NOT used.

## 7. Actual terminal arithmetic and strict conclusion

The single production run completed all four branches. After (17), exact comparison with rational thresholds gives

    e02 <87/20000,
    e12 <611/100000,
    e20 <7/10000.                                             (18)

The sharper actual totals are approximately0.004346663899254519,0.006100259364965853,0.0006909819837319293. Those decimals are display only; their full exact upper fractions, entry matrices and tails are retained. The production program's original acceptance threshold was -1/10000. The stronger corollary (18) is separately checked exactly from the SAME completed output, not a rerun, refit or changed input.

Using the rational thresholds (18), rather than the display decimals, (3) yields

    h'' < -6660155061088431/2000000000000000000
             +(87/20000)/2+(9/100)(611/100000)+(7/10000)/2
         = -510355061088431/2000000000000000000
         < -1/4000.                                         (19)

The actual unrounded certified upper endpoint is approximately-0.00026223124620406476. Equation (19), not a rounded decimal or sample, proves (1) on the entire closed interval.

## 8. Symmetry, scope and execution status

For any finite compression, let U_ii=(-1)^i. Then K_-t=U K_t U*, including the unchanged second off-diagonal. Each signed complete-event matrix is conjugated by the same U, so every complete event probability and entropy is unchanged. Passing to the rate gives h(-t)=h(t). The previously justified C2 regularity then transfers (1) to -J. This does not prove a larger interval.

The author-local production was bounded by900 seconds, one CPU thread and8GiB address space, independently of any old Codex budget. Start05:46:27.887874UTC, finish05:47:34.415155UTC, exit0, elapsed66.527318643s, worker reaped. Exact environment, original command, stdout and stderr are public under run01/. There was no production rerun or numerical repair. Later small algebra checks are separately recorded; one unrelated lifted-state label error and its invalid preliminary witness were caught and preserved before that theory was finalized. This interval program always used the direct determinant (10), not the erroneous lifted formula.

Independent mathematical/arithmetic acceptance: PENDING_REVIEW. No server/S2 execution is asserted. Novelty: UNASSESSED. The full [1/2,3/2] sign and general DPP entropy concavity remain INCOMPLETE.
