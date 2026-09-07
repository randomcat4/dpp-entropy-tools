# Paired frames: the full ordinary second-order coefficient

Author status: PROVED for the fixed family stated here, pending independent verification. No formal gate is requested. The m=3 case and the general m case follow from the same event calculation; no numerical scan is used.

## 1. Statement and exact feasible scope

Let m>=2 and n=2m. Pair coordinate i with coordinate m+i, and fix

    U=(1/sqrt(2))*[I_m; I_m],
    V=(1/sqrt(2))*[I_m; -I_m],
    A=diag(a_1,...,a_m), C=diag(c_1,...,c_m), a_i,c_i>0.

Let X=(x_ij) and Y=(y_ij) be fixed real symmetric matrices with zero diagonal. Assume the complete feasibility conditions

    A-X>=0, A+X>=0, C-Y>=0, C+Y>=0.                    (1)

For sigma in {+1,-1}, put H_sigma=A-sigma X, L_sigma=C+sigma Y, and

    K_(e,sigma)=[U V]diag(I_m-eH_sigma,eL_sigma)[U V]^T.

The center M_e uses A,C. For all sufficiently small e>0 these are real positive contractions. Singular H_sigma or L_sigma are allowed. Condition (1) is necessary and sufficient for eventual feasibility of this fixed B=0 family; a fixed upper bound on all four operator norms gives an explicit small-e interval. The pairwise inequalities x_ij^2<=a_i a_j and y_ij^2<=c_i c_j follow from (1), but are not substituted for full matrix feasibility when m>=3.

For D>0 and 0<=z<=D define

    G_D(z)=z+(D-z)log(1-z/D),
    G_D(D)=D,

with the continuous convention 0 log 0=0. For the exact-event Shannon entropy chord gap,

    Delta_e=(H(K_(e,+))+H(K_(e,-)))/2-H(M_e),

the result is

    Delta_e=C2 e^2+O(e^3 |log e|),
    C2=-sum_(1<=i<j<=m)
          [G_(a_i a_j)(x_ij^2)+G_(c_i c_j)(y_ij^2)].   (2)

There are no omitted multiplicative constants or X/Y cross terms. Both e log(1/e), e, and e^2 log(1/e) coefficients vanish.

Since G_D(z)>0 for z>0 and G_D(0)=0, C2<=0, with equality exactly when X=Y=0. Every nonzero fixed feasible direction in this paired-frame family has Delta_e<0 for all sufficiently small e. If X=Y=0, the kernels agree and Delta_e=0 identically. The m=1 case is this latter trivial case.

## 2. Full exact-event law and tomography kernels

All probabilities below are exact events. Expanding

    det(I+K(diag(z)-I))
       =sum_T det(K_T) product_(i in T)(z_i-1)

shows that its z_S coefficient is the inclusion-exclusion sum defining p_K(S). Diagonalizing K with orthonormal eigenvectors T and eigenvalues lambda gives the equivalent full law

    p_K(S)=sum_(J:|J|=|S|)
       [product_(j in J)lambda_j product_(j notin J)(1-lambda_j)]
       det(T_(S,J))^2.                                 (3)

Formula (3) follows by row expansion and Cauchy-Binet. It permits counting holes among the m high modes and particles among the m low modes. Terms with k eigenmode flips carry O(e^k).

The projection P=UU^T puts probability 2^(-m) on every configuration that occupies exactly one coordinate from each pair. All other configurations have zero projection probability. An r-1 cofactor vector is nonzero only when the event omits one pair i and selects one coordinate from every other pair; then it equals +/-2^(-(m-1)/2)e_i. The addition cofactor vector is nonzero only when one pair i is doubly occupied and all other pairs singly occupied; it has the same form. Thus both first-event measurement maps observe precisely diagonal matrix entries, and their kernels are exactly the zero-diagonal symmetric matrices. Each kernel has dimension m(m-1)/2; when m=3 each has dimension 3.

## 3. Complete event expansion through degree two

Write kappa_d=2^(-(m-d)) for d=0,1,2, and T=tr A+tr C. Say a pair is empty, single, or double according to whether 0,1,2 of its coordinates lie in the event. In single pairs write zeta_i=+1 for choosing i and zeta_i=-1 for choosing m+i.

For any matrix pair H,L with the present diagonal entries, the exact-event expansion is as follows.

### All pairs single

There are 2^m such supported configurations. Each has p_0=kappa_0 and first coefficient -kappa_0 T. Its second coefficient is

    b_zeta(H,L)=kappa_0[e2(H)+e2(L)+tr H tr L
                                    +tr(H Zeta L Zeta)],
    Zeta=diag(zeta_1,...,zeta_m).                        (4)

Here e2(H)=((tr H)^2-tr(H^2))/2. To derive (4), the no-flip weight is det(I-eH)det(I-eL), multiplied by kappa_0. The other degree-two contributions are one high hole and one low particle. For a supported event its replacement-amplitude matrix is +/-2^(-m/2)Zeta, so their full coefficient is kappa_0 tr(H Zeta L Zeta). Higher flip counts contribute O(e^3) or smaller.

At either endpoint the second-coefficient difference from the center is

    delta b_zeta=-kappa_0 sum_(i<j)
                    [x_ij^2+y_ij^2+2x_ij y_ij zeta_i zeta_j].  (5)

This uses e2(H_sigma)-e2(A)=-sum_(i<j)x_ij^2, and similarly for L; their traces stay fixed. Both endpoints have the same coefficient (5), although their complete probability laws need not agree at higher orders.

### One empty pair i, all other pairs single

There are 2^(m-1) configurations for each i. Their common first coefficient is kappa_1 a_i. Through second order,

    p(H,L)=kappa_1[e H_ii+e^2((H^2)_ii-(tr H+tr L)H_ii)]
                   +O(e^3).

Indeed the one-hole eigenmode sum has matrix coefficient H-e(tr H H-H^2), and survival of the low modes contributes the additional -e tr L H. The cofactor vector from section 2 extracts its i-th diagonal entry. Therefore their endpoint-minus-center second-coefficient difference is

    delta b_i^-=kappa_1 sum_(j!=i)x_ij^2.               (6)

### One double pair i, all other pairs single

Again there are 2^(m-1) events for each i. The first coefficient is kappa_1 c_i, and the analogous addition expansion gives

    delta b_i^+=kappa_1 sum_(j!=i)y_ij^2.               (7)

### Two empty pairs i,j, all others single

For each unordered pair {i,j} there are 2^(m-2) events. Two high holes give the exact leading coefficient

    b_ij^--(H)=kappa_2 det(H_({i,j}))
                =kappa_2(a_i a_j-x_ij^2).             (8)

This is the squared-minor two-hole law (the second exterior power of H) restricted to the missing coordinate indices i,j. At the center it is kappa_2 a_i a_j. Zero determinants are permitted.

### Two double pairs i,j, all others single

The corresponding coefficient is

    b_ij^++(L)=kappa_2(c_i c_j-y_ij^2),                 (9)

and at the center it is kappa_2 c_i c_j. There are again 2^(m-2) events per unordered pair.

### One empty pair i and one double pair j, i!=j

For each ordered pair i,j there are 2^(m-2) events. The only nonzero replacement-amplitude entry is (i,j), with square kappa_2. Thus the exact second-order coefficient is

    b_ij^-+(H,L)=kappa_2 H_ii L_jj=kappa_2 a_i c_j,     (10)

identical at both endpoints and at the center. In particular there is no hidden x_ij y_ij contribution in these zero projection events.

### Every remaining event

It has at least three empty/double pairs in total, so it requires at least three flips and has probability O(e^3). For completeness, if there are k_0 empty pairs and k_2 double pairs, a nonzero determinant in (3) with h high holes and l low particles must have h>=k_0: the selected high columns otherwise exceed the rank of the restricted U frame. The cardinality identity l-h=k_2-k_0 then gives l>=k_2. Hence h+l>=k_0+k_2. This proves the claimed bound and exhausts the entire 2^(2m)-event law.

## 4. Logarithmic coefficients vanish

The endpoint and center constant and first coefficients agree for every event. This eliminates the e and e log(1/e) gap terms.

At order e^2 log(1/e), positive one-hole rates have logarithmic weight one on their second coefficient. Summing (6) over every i and its single-coordinate choices gives 2 sum_(i<j)x_ij^2. Two-hole events start at degree two, so (8) has weight two; its difference sums to -2 sum_(i<j)x_ij^2. The two cancel. Equations (7) and (9) give the identical cancellation for Y. Supported probabilities have no logarithmic terms and (10) does not change. This proves the complete absence of an e^2 log gap.

## 5. Ordinary second-order coefficient, one unordered pair at a time

Let f(p)=-p log p. For supported events the shared first coefficient makes the f'' term cancel in the chord comparison. Since f'(kappa_0)=m log 2-1 and

    sum_zeta zeta_i zeta_j=0 for i!=j,

the cross terms in (5) cancel exactly. The total supported contribution is

    [1-m log 2]sum_(i<j)(x_ij^2+y_ij^2).               (11)

For one-hole events with common first rate kappa_1 a_i, the finite part accompanying a second-coefficient change is -[log(kappa_1 a_i)+1]delta b. Summing over configurations and then over the two ends of one unordered pair, the x_ij^2 coefficient is

    [-log(a_i a_j)+2(m-1)log 2-2]x_ij^2.              (12)

Combine (11) and (12) and set D=a_i a_j, z=x_ij^2. The supported-plus-one-hole term for this pair is

    [(m-2)log 2-1-log D]z.                            (13)

The finite two-hole entropy difference from (8), after summing all 2^(m-2) configurations, is

    f(D-z)-f(D)-(m-2)(log 2)z.                        (14)

Adding (13) and (14) yields

    -z-z log D-(D-z)log(D-z)+D log D
       =-[z+(D-z)log(1-z/D)]
       =-G_D(z).                                     (15)

The calculation for Y is identical with D=c_i c_j and z=y_ij^2. Mixed empty/double events do not change at this order. Equations (11)–(15) prove the exact pair decomposition (2).

No triangle or higher-cycle term can appear at this order: the complete event expansion involves only e2, squared off-diagonal entries, and the X/Y cross terms already canceled in (11).

## 6. Boundary values, remainder, and strict sign

Full feasibility (1) ensures 0<=z<=D for every pair by its 2-by-2 principal minors. Supported probabilities are uniformly positive for fixed m near e=0; all one-hole and one-particle rates are positive because a_i,c_i>0; all mixed rates in (10) are positive. Pure two-hole or two-particle leading coefficients may vanish. When they do, their probability is O(e^3), which contributes O(e^3|log e|) to entropy and is consistent with the continuous convention in (14). The same bound handles every remaining event. All exact probabilities are polynomials in e and there are finitely many events, so ordinary Taylor expansion and the elementary p log p expansion give the stated O(e^3|log e|) remainder for fixed data, including singular endpoints.

For 0<=z<D,

    G_D(0)=0,
    G_D'(z)=-log(1-z/D)>=0.

The derivative is strictly positive for z>0, and the boundary value G_D(D)=D is positive. Thus C2 is strictly negative unless every off-diagonal entry of X and Y is zero. Also -log(1-u)>=u on [0,1) gives the useful quantitative bound

    G_D(z)>=z^2/(2D),
    C2<=-(1/2)sum_(i<j)
          [x_ij^4/(a_i a_j)+y_ij^4/(c_i c_j)].         (16)

Equation (16) includes z=D by continuity. It explains why small invisible directions can give very small negative coefficients without approaching a positive branch.

## 7. The requested m=3 specialization and diagnostic comparison

For m=3, (2) is the sum over exactly {1,2},{1,3},{2,3}. Both tomography kernels have dimension 3, so this covers all six independent invisible direction entries, subject to the complete endpoint feasibility (1), rather than a selected one-dimensional subfamily.

For the unequal-diagonal example `a_1a_3=5`, `c_2c_3=4`,
`x_13=y_23=1/3`, with all other entries zero, the formula is exactly

    C2=-G_5(1/9)-G_4(1/9).

This expression requires no numerical scan. The proof is analytic and does
not use the finite diagnostics as evidence for its universal sign.

## Scope

The proof excludes the complete fixed paired-frame family with positive diagonal A,C and zero-diagonal X,Y. It does not sign general non-paired tomography kernels, non-diagonal A,C, moving frames, or a regime in which the fixed data vary with e. No global real-kernel concavity theorem or novelty claim follows. Author-complete does not mean independently verified.

