# Eight-event reconstruction and a different stationarity mechanism

Author: C1 main. Algebra below is rebuilt here; most structural identities are inherited in substance from the source round. B0 is not solved by this note.

## 1. Event map and full derivatives

Use coordinates (x,y,z,a,b,c). Let q12=xy-a², q13=xz-b², q23=yz-c² and r=xyz+2abc-xc²-yb²-za². The events are p123=r; pij=qij-r; pi=Kii-qij-qik+r; p0=1-x-y-z+q12+q13+q23-r. For any event S, equivalently

    pS=(-1)^(3-|S|) det(K-diag(1_{i not in S})).

The equivalence follows by expanding the determinant in the subtracted diagonal entries and collecting inclusion minors. Positivity follows from L=K(I-K)^-1>0 and pS=det L_S/det(I+L), including p0=1/det(I+L).

Let D have coordinates (X,Y,Z,A,B,C). Then

    q12'=yX+xY-2aA,             q12''=2XY-2A²,
    q13'=zX+xZ-2bB,             q13''=2XZ-2B²,
    q23'=zY+yZ-2cC,             q23''=2YZ-2C²,
    r'=(yz-c²)X+(xz-b²)Y+(xy-a²)Z
        +2(bc-za)A+2(ac-yb)B+2(ab-xc)C,
    r''=2[zXY+yXZ+xYZ-xC²-yB²-zA²]
        +4[cAB+bAC+aBC-cXC-bYB-aZA].

The eight p' and p'' are exactly the same linear combinations of these derivatives as the event formulas (diagonal second derivatives are zero). Bilinear derivatives are obtained by polarization, p''[D,E]=(p''[D+E]-p''[D]-p''[E])/2. This retains all six bases and the off-diagonal factors of two. All formulas are polynomial at zero edges. The implementation independently expands determinant permutations and differentiates each product, without inverses of event matrices.

## 2. Hessian and N

Differentiation of H=-sum p log p, using sum p'=sum p''=0, gives

    B(D,D)=-H''=sum (p')²/p+sum p'' log p.

Collect coefficients of q12'',q13'',q23'',r'' in the last sum: they are ell12,ell13,ell23,Lambda. Since qij''=2 det D_{ij} and r''=2 tr(K adj D),

    B(D,D)=F(D,D)-2 tr(N adj D).

For pair ij with remaining index k, direct multiplication of the event formulas gives

    p0 pij-pi pj=-((1-Kkk)Kij+Kik Kjk)²,
    pk p123-pik pjk=-(Kkk Kij-Kik Kjk)².

Thus ellij<=0 and ellij+Lambda<=0. If Lambda<0, N=diag(-ell)+(-Lambda)K>0. If Lambda>0, N=diag(-ell-Lambda)+Lambda(I-K)>0. If Lambda=0 and ellij=0, both squares vanish; adding their unsquared zero equations yields Kij=0 and then Kik Kjk=0. This contradicts connectedness on three vertices. Hence all -ellij>0 when Lambda=0. This proves N>0 on the full frozen connected domain, including a single zero edge.

Set W=N^-1 and d=det N. Congruence by N^-1/2 and the identity 2 tr(adj A)=(tr A)²-tr(A²) give

    2 tr(N adj D)=d[(tr WD)²-tr(WDWD)].

Therefore B=F+dG-d eta eta^T. In six entry coordinates eta=(W11,W22,W33,2W12,2W13,2W23).

## 3. Complete Fisher and invertibility

In the p-weighted inner product on the eight atoms, let hS=(-1)^(3-|S|)/pS. It is orthogonal to every multilinear statistic of degree at most two because its pairing is an alternating sum. That polynomial space has dimension seven including constants. Its orthogonal complement is exactly span(h), with squared norm Z=sum 1/p. A score sS=pS'/pS is centered and has pairing with h equal to Lambda'. Orthogonal projection consequently gives

    F=Jmom^T Cov(Tstat)^-1 Jmom+gg^T/Z.

Cov(Tstat)>0: if a linear combination of the six centered monomials has zero variance, positivity on all eight atoms makes it identically zero; independence of distinct multilinear monomials makes every coefficient zero. The pair term is positive semidefinite. It is positive definite iff all three edges are nonzero, since Jmom has diagonal mean block I and edge block diag(-2a,-2b,-2c). At a connected one-zero-edge kernel it has rank five; one must not invert Fpair there. Nevertheless G is positive definite, so M=Fpair+dG>0 everywhere in the frozen domain. Moreover F itself is positive definite in the connected domain: zero event derivatives imply zero singleton derivatives and zero derivatives of all nonzero edges; if one edge is zero, r' in its remaining direction is twice the product of the two nonzero edges, forcing that direction to vanish too.

Write h=M^-1 eta, alpha=eta^T h>0. The unique minimizer of M(D,D) under eta(D)=1 is D_M=h/alpha: writing D=D_M+V gives eta(V)=0 and M(D,D)=1/alpha+M(V,V). Also

    Lambda'[D_M]=sqrt(Z) beta/alpha,
    B(D_M,D_M)=1/alpha-d+beta²/alpha².

At an exact beta zero this is 1/alpha-d. For general K, the full optimum follows by Sherman–Morrison:

    rho=d[alpha-beta²/(1+gamma)], gamma=v^T M^-1 v.

Hence beta=0 is an alignment condition on this unique optimizer. None of these identities proves its sign.

## 4. Exponential tilts give exact mixed stationarity equations

This second mechanism uses the full score, rather than a proposed lower Fisher projection. For any diagonal A=diag(a_i), take L(t)=exp(tA)L exp(tA). Its event weights are multiplied by exp(2t sum_{i in S}a_i), so its score at zero is

    s_A(S)=2 sum_i a_i(1_{i in S}-Kii).

Differentiating K=L(I+L)^-1 gives the tangent matrix

    Q_A=AK+KA-2KAK.

This curved L path is used only to identify its first-order K tangent, not to assert any K-affine curvature sign. From the score formula and alternating sums,

    Lambda'[Q_A]=0,
    F(Q_A,D)=Fpair(Q_A,D)=2 tr(A D).

Indeed E[s_A s_D]=2 sum a_i dE[Xi][D]=2 sum a_i Dii. If Q_A=0, its score vanishes at all eight atoms, forcing A=0; these are three independent directions at every strict K. This is compatible with the item-quality exponential flatness described by Hino–Yano, Corollary 1, but the identities above are directly proved and do not assume all cycle signs can be removed.

Substitute Q_A into the exact stationarity system M(h,D)=eta(D). With R=W h W, cyclicity of trace yields three scalar equations:

    diag(2h+d[KR+RK-2KRK])
      =diag(KW+WK-2KWK).                                (T)

Here h denotes the symmetric matrix with coordinate vector M^-1 eta. This use of h is distinguished from the atom-space vector in section 3 by context. Formula (T) is valid even before beta=0; at beta=0 the additional complete-score condition is g^T h=0. It is an exact reduced stationarity test, not a lower bound and not an assumption on arbitrary Lambda tangents.

## 5. Remaining gap and finite diagnostics

The three tilt equations do not determine the six coordinates of h, and imposing g^T h=0 does not provide the missing sign 1/alpha-d. No implication from exponential flatness to K-affine Hessian negativity was found. The unclosed inequality is still the complete Fisher/cofactor control at the actual stationary direction. This is an equivalent blocker, not a new theorem.

`precheck.py` checks exactly three rational-input kernels (one old-root midpoint used only as calibration, one connected zero-edge kernel, one dense interior kernel); `tilt_probe.py` checks the three tilt identities at one fixed kernel and exactly eight fixed star diagnostics. Both ran on the authorized server with one CPU thread, exit 0. Their floating residuals check implementation only. No finite observation certifies a sign on an infinite domain.
