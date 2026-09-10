# Entropy-specific C2 finite-memory tail, retaining the complete law response

Status: AUTHOR_PROOF / PENDING_INDEPENDENT_REVIEW. Date: 2026-09-10.

This is a second, same-task continuation after HIGH_ORDER_CLOSURE.md was uploaded. It avoids the literal depth-120 Neumann evaluation. Its dependencies are only the complete-event representation and the explicit finite coding-jet estimates of accepted PR91. It does not differentiate a value inequality or invoke a generic spectral gap.

Let Y_j=(X_(2j),X_(2j+1)) and

    h_r(t)=(1/2) H(Y_0 | Y_1,...,Y_r),
    h(t)=lim_r h_r(t), t in I=[1/2,3/2].

Every entropy is full Shannon entropy with natural logarithms. All derivatives below are in the true affine correlation-kernel parameter t.

## 1. Exact finite increment

For n>=1 put delta_n=2(h_(n-1)-h_n). Conditional relative entropy gives the EXACT identity

    delta_n(t)=sum_(w in {--,-+,+-,++}^n) p_n(w;t) F_w(t),
    F_w=KL(g(Q_n(w;t)) || g(Q_(n-1)(w_1,...,w_(n-1);t))).       (1)

Both probability vectors contain all four current-cell outcomes. The future-word law p_n is the actual complete n-cell DPP law, not a frozen or fitted law. Thus

    delta_n''=sum_w [p_n F_w''+2p_n' F_w'+p_n'' F_w].            (2)

The last two terms are NOT discarded.

## 2. Finite full-word Fisher and acceleration budgets

Along any finite coding trajectory, PR91 gives Frobenius bounds |Q'|<=3/10, |Q''|<=9/8. The total conditional probability derivatives are

    gamma=g_t+Dg[Q'],
    gamma2=g_tt+2Dg_t[Q']+D2g[Q',Q']+Dg[Q''].

Use epsilon=81/1024, sum|Dg|<=2, sum|D2g|<=4, sum|g_t|<=7/64, sum|Dg_t|<=3/8, sum|g_tt|<=1/32, and the individual bounds |Dg|,|D2g|<=1, |g_t|<=7/256, |Dg_t|<=3/32. They imply

    max |gamma| <=3/10+7/256 <1/3,
    sum |gamma| <=7/64+2*(3/10),
    sum gamma^2/g <= [(3/10+7/256)(7/64+2*(3/10))]/epsilon <3,
    sum |gamma2| <=1/32+2*(3/8)*(3/10)+4*(3/10)^2+2*(9/8)<3,
    max |gamma2| <=1/128+2*(3/32)*(3/10)+(3/10)^2+9/8<4/3.     (3)

The complete-word score is the sum of its finite future-conditional scores. These are orthogonal reverse martingale differences under p_n. Therefore

    sum_w (p_n')^2/p_n <=3n,
    sum_w |p_n'| <=sqrt(3n),
    sum_w |p_n''| <=9n.                                    (4)

For the last inequality write p_n''/p_n=S_n^2+sum_j(log g_j)''. Its L1 norm is at most one complete Fisher budget plus the sum of the conditional absolute gamma2/g and conditional Fisher budgets: 3n+3n+3n. This explicitly includes the full acceleration, not just Fisher.

## 3. Sharper finite initial discrepancies

The two states in (1) share m=n-1 near-cell maps. Their terminal data are T_(w_n)(0) versus 0, including both t jets. Let

    k=34/81, M0=33/400, J0=285/2704, H0=1077/17576.

At Q=0 the inverse bound is 32/13 (rather than 32/9). With e=3/16, e2=17/512, c=1/16 this gives

    ||T(0)||_F^2<=1169/416^2 < M0^2,
    ||partial_t T(0)||_F <= (3/2)[2ce*(32/13)+e2*c*(32/13)^2]=J0,
    ||partial_t^2 T(0)||_F
       <=(3/2)[2c^2*(32/13)+4c^2e*(32/13)^2
                +2e2*c^2*(32/13)^3]=H0.                    (5)

PR91's complete finite-jet difference recurrence is

    dQ_new<=k dQ,
    dJ_new<=k dJ+(3/2)dQ,
    dH_new<=k dH+3dJ+10dQ.

Solving it from (5) yields

    dQ_m<=M0 k^m,
    dJ_m<=[J0+(3M0/(2k))m] k^m,
    dH_m<=[H0+((3J0+10M0)/k)m
                +(9M0/(4k^2))m(m-1)] k^m.                 (6)

No limiting coding derivative is needed here; these are finite words.

## 4. Quadratic KL controls its own two derivatives

Let a=g(Q_n), b=g(Q_(n-1)), d=a-b. Normalization gives sum d=0. The Bregman formula is

    KL(a||b)=sum_i d_i^2 int_0^1 (1-v)/(b_i+v d_i) dv.       (7)

Every denominator is >=epsilon. By (3), its first and second total t derivatives are bounded by u=1/3 and v2=4/3. Therefore, with A>=||d||_2, B>=||d'||_2, C>=||d''||_2,

    |F| <= A^2/(2epsilon),
    |F'| <= AB/epsilon+u A^2/(2epsilon^2),
    |F''| <=(B^2+AC)/epsilon+2u AB/epsilon^2
               +(u^2/epsilon^3+v2/(2epsilon^2))A^2.         (8)

These are obtained by differentiating the identity (7), NOT a KL value bound.

The quadratic formula for g gives componentwise

    |d_i|<=dQ_m,
    |d_i'|<=dJ_m+(63/160)dQ_m,
    |d_i''|<=dH_m+(63/80)dJ_m+(9/8)dQ_m.                   (9)

For the last line use g_tt state-independent, and g_tQ and g_QQ constant. In particular no third derivative has been silently assumed. Four components give the following Euclidean bounds after factoring k^m:

    A=2M0,
    B(m)=2[J0+(3M0/(2k))m+(63/160)M0],
    C(m)=2[H0+((3J0+10M0)/k)m+(9M0/(4k^2))m(m-1)
              +(63/80)(J0+(3M0/(2k))m)+(9/8)M0].            (10)

Write F0,F1(m),F2(m) for the right sides of (8) using (10), without their common factor k^(2m).

## 5. Explicit complete second-response tail theorem

Combine (2), (4), (8)-(10), and 2sqrt(3n)<=n+3. For m=n-1,

    |delta_n''(t)| <= k^(2m) P(m),
    P(m)=F2(m)+(m+4)F1(m)+9(m+1)F0
        =a2 m^2+a1 m+a0,                                  (11)

where exact rational coefficients are

    a2=1809918/180625,
    a1=154889893499/5135349375,
    a0=342449808326286961/15178486401000000.

All coefficients are positive. The same argument gives uniformly summable first derivatives, using |delta_n'|<=k^(2m)[F1(m)+sqrt(3n)F0]; values are also uniformly summable. Hence the elementary uniform derivative-series theorem applied to (1) proves an actual C2 limit, and

    |h_r''(t)-h''(t)| <= E_r=(1/2)sum_(m=r)^infinity k^(2m)P(m). (12)

This holds uniformly for every t in [1/2,3/2]. Put lambda=k^2. The tail is the explicit rational number

    E_r=(lambda^r/2)*{
      a2[r^2/(1-lambda)+2r lambda/(1-lambda)^2
                     +lambda(1+lambda)/(1-lambda)^3]
      +a1[r/(1-lambda)+lambda/(1-lambda)^2]
      +a0/(1-lambda)}.                                    (13)

In particular

    E_9 <115/10^6,
    E_10 <25/10^6,
    E_11 <51/10^7.                                        (14)

This is the entropy-specific improvement: the decay is the square of the state contraction, with both differentiated-law terms retained and bounded by complete Fisher/acceleration budgets. It is not another finite-window sign scan. One chosen finite conditional entropy curvature, together with (13), now controls the true rate uniformly.

## 6. A small finite analytic interpolation gate for the entire macroscopic interval

For r=9, h_9=(H_20-H_18)/2. Cover [1/2,3/2] by four intervals of half-width 1/8 and centers 5/8,7/8,9/8,11/8. On each scaled Bernstein ellipse of parameter rho=3 the complex parameter satisfies |z-t0|<=5/24.

For every complete N-site event its signed matrix is M_N(t)=K_N(t)-I_vacant. At the real center t0, diagonal dominance in operator norm gives sigma_min M_N(t0)>=(2-t0)/8>=5/64, and ||K_N'||<=1/8. Consequently ||(z-t0)M_N(t0)^(-1)K_N'||<=1/3. All complete event probabilities are zero-free on the disk and their logarithms continue from their real positive values. Uniformly there,

    sum_X |p_X(z)| <=(4/3)^N,
    |log p_X(z)| <=3N,
    |partial_z log p_X(z)| <=(12/5)N,
    |partial_z^2 log p_X(z)| <=(12/5)^2 N.

The first inequality uses |det(I+A)|<=(1+||A||)^N and sum p_X(t0)=1. The logarithm bound uses p_X(t0)>=(5/64)^N and the convergent trace-log series. It is not spectral entropy.

Differentiating the complete entropy, retaining both terms, gives

    |H_N''(z)| <=(4/3)^N*(144/25)*(3N^3+4N^2).

Thus |h_9''(z)| is at most

    M=(1/2)[(4/3)^20*(144/25)*(3*20^3+4*20^2)
             +(4/3)^18*(144/25)*(3*18^3+4*18^2)]
     =318159082659774464/9685512225 <40000000.               (15)

For the degree-31 interpolant at the 32 first-kind Chebyshev roots, the standard coefficient/aliasing proof gives

    ||h_9''-P_31||_infinity <=6*(40000000)/3^32.             (16)

For completeness: analytic Chebyshev coefficients have magnitude <=2M rho^(-k); at root nodes, each high-degree Chebyshev polynomial aliases to a signed polynomial of sup norm <=1. Summing the tail gives 2*sum_(k>=32)2M rho^(-k), which is (16).

If certified DCT coefficient enclosures are c_0,...,c_31, a directly checkable sufficient gate on each interval is

    upper(c_0)+sum_(j=1)^31 max(|lower(c_j)|,|upper(c_j)|)
       +6*(40000000)/3^32+E_9 <0.                          (17)

No grid maximum is promoted to a continuum statement: (15)-(17) provide the missing analytic cover. Actual computation of the 128 node enclosures has not yet been claimed at this checkpoint. All new results remain AUTHOR_PROOF / PENDING_INDEPENDENT_REVIEW.
