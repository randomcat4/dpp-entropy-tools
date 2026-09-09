# Complete C1 proof dossier — PARTIAL

The universal B0 claim in frozen_statement.md is not proved. This dossier includes the full arguments for the accepted restricted results and exact identities. Current review bindings are in verification.md. Frozen author texts below retain their historical labels and are not silently edited. Their original relative references to proof.md mean geometry/proof.md where stated.

The first four parts are: (I) complete structural reconstruction and exact tilts; (II) full-support beta-negative collar; (III) sparse exact-zero sharpness; (IV) the distinct rational finite root certificate. Part IV does not instantiate the unit-normalized family in Part III. The exact rational JSON bounds are authoritative; display decimals are summaries.


---

# Part I — original main/reconstruction.md

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


---

# Part II — original geometry/proof.md

# A uniform beta-negative collar at a full-support rank-one face

Author candidate; not independently reviewed. B0 remains OPEN.

## 1. Precisely restricted assertion

Fix a unit vector u in R^3 with u1 u2 u3 nonzero and lambda in (0,1).
Write P=I-uu^T and L=log(1/tau). Let C range over a compact set of real
symmetric matrices for which B=(PCP)|_{u-perp} >= c I for a fixed c>0.
Allow any uniformly bounded symmetric remainder R(tau,C), and set

    K = lambda uu^T + tau C + tau^2 R(tau,C), tau>0.

No differentiability of R in tau is needed: all derivatives defining the
Fisher matrix and beta below are derivatives in the six actual K entries.
For sufficiently small tau, uniformly in these parameters, K is strict,
connected, N>0, and M>0. Put Delta=det(B). Then

    g^T M^-1 eta = -1/(lambda L) + O(L^-2),                 (1)
    beta = -tau sqrt(Delta)/(sqrt(lambda) L) [1+O(L^-1)],    (2)
    d alpha = 1 - 1/(lambda L) + O(L^-2).                   (3)

In particular beta<0 throughout a sufficiently small uniform collar.
The limiting value d alpha=1 does NOT occur along beta=0 in this collar.
Equation (3), for isotropic soft eigenvalues, is an old boundary mechanism;
the intended added object is (1)-(2), especially uniformity in the soft
shape and the affine corollary in Section 8. Novelty is not certified.

Constants may depend on lambda, u, c, the compact C set and the R bound.
No assertion is made when u loses support, lambda approaches 0 or 1,
or the normalized soft block loses positivity. This is not a theorem on
the entire beta-zero set or on all real three-point kernels.

## 2. Rebuild from eight probabilities and affine jets

Use coordinates (x,y,z,a,b,c), with symmetric off-diagonal basis entries
equal to one in BOTH positions. Set

    q12=xy-a^2, q13=xz-b^2, q23=yz-c^2,
    r=xyz+2abc-xc^2-yb^2-za^2.

In event order (0,1,2,3,12,13,23,123), the probability vector is

    (1-x-y-z+q12+q13+q23-r,
     x-q12-q13+r, y-q12-q23+r, z-q13-q23+r,
     q12-r,q13-r,q23-r,r).

This follows by inclusion-exclusion of the principal minors. Differentiating
this displayed polynomial vector gives all first and second affine jets;
no marginal event is discarded. For a symmetric D with entries
(dx,dy,dz,da,db,dc), for example,

    q12'=y dx+x dy-2a da,
    q12''=2(dx dy-da^2),
    grad r=(yz-c^2,xz-b^2,xy-a^2,2bc-2za,2ac-2yb,2ab-2xc),
    r''=2 tr(K adj(D)).

The other two q formulas are obtained by the explicit substitutions
(x,y,a)->(x,z,b) and (x,y,a)->(y,z,c). The linear probability map above
applies identically to these jets. Thus the off-diagonal factor 2 is kept.
The real identities a^2,b^2,c^2 and T=2abc hold identically as polynomials,
including their full affine jets.

Define F(D,E)=sum_S p'[D] p'[E]/p. Let e_S=(-1)^(3-|S|) and
Lambda=sum_S e_S log p_S; Z=sum_S 1/p_S. The probability-space score
q_S=e_S/(p_S sqrt Z) has norm one for the weighted score inner product.
It is perpendicular to constants and to every monomial X_A of degree
at most two because sum_{S superset A} e_S=0. There are seven such
linearly independent monomials, so q spans their orthogonal complement.
Every K score has mean zero. Orthogonal projection onto the six centered
statistics Tstat=(Xi,XiXj) gives

    Fpair=J^T Cov(Tstat)^-1 J,
    F=Fpair+vv^T, v=g/sqrt Z, g=grad Lambda.

Cov is positive definite since a degree-at-most-two polynomial constant
on all eight configurations has zero nonconstant coefficients. All p_S
are positive in the strict domain. The score's coefficient on q is exactly
Lambda'[D]/sqrt Z, proving the decomposition without a conditional or
locked-odds approximation.

Put ell12=log(p0 p12/(p1 p2)), and define the others by relabeling.
The affine entropy identity is

    -H''=F+sum_ij ellij qij''+Lambda r''
        =F-2 tr(N adj(D)),
    N=-diag(ell23,ell13,ell12)-Lambda K.

For invertible positive N, the coefficient-of-t^2 identity in
det(N+tD)=det(N)det(I+t N^-1D) gives

    2 tr(N adj(D))
      =d[(tr(N^-1D))^2-tr(N^-1D N^-1D)].

Thus B_entropy=-Hess H=F+dG-d eta eta^T. We use N>0 only in the collar
where Section 3 proves it, not as an unproved global premise. Since G is
positive definite on symmetric matrices when N>0, M=Fpair+dG>0 there.
The vector h=M^-1 eta and its normalization h/alpha are the actual
six-dimensional optimizers; no arbitrary Lambda tangent is substituted.

## 3. Event scales and logarithmic cofactor matrix

For i<j define

    k_ij(D)=u_i^2 D_jj+u_j^2 D_ii-2u_i u_j D_ij,
    h_ij=k_ij(C)=k_ij(PCP).

These are positive at C because k_ij(D)=z_ij^T D z_ij with
z_ij=u_j e_i-u_i e_j in u-perp and z_ij nonzero. Uniform compactness gives
positive lower and finite upper bounds. In an orthonormal basis starting
with u, a block determinant expansion gives

    p0=1-lambda+O(tau), p_i=lambda u_i^2+O(tau),
    p_ij=tau lambda h_ij+O(tau^2),
    p123=tau^2 lambda Delta+O(tau^3).                      (4)

For pairs this is just the displayed q polynomial, with the triple term
only O(tau^2). For the triple determinant the upper-left entry is
lambda+O(tau), lower block tau B+O(tau^2), and cross block O(tau),
so its leading term is lambda tau^2 det B. The same block Schur complement
proves K>0 for small tau. The top eigenvalue tends to lambda<1 and the
others to zero, proving I-K>0. Since the off-diagonal entries tend to
lambda u_i u_j nonzero, the graph is connected.

From (4), ellij=-L+O(1), Lambda=L+O(1), and hence

    N=L A+O(1), A=I-lambda uu^T>0,
    N^-1=L^-1 A^-1+O(L^-2), d=(1-lambda)L^3[1+O(L^-1)],
    Z=(tau^2 lambda Delta)^-1[1+O(tau)].                  (5)

Here tau L is bounded and tends to zero, so the O(tau L) contribution
from Lambda(K-lambda uu^T) is included in O(1). All statements are
uniform in the stated compact family. In particular N>0 is established.

## 4. Tangent-normal splitting retains all Fisher costs

Let

    T={u w^T+w u^T : w in R^3},
    V={E symmetric : Eu=0}.

These are complementary three-dimensional subspaces. Every k_ij
vanishes on T. Conversely, if all k_ij(D)=0, the nonzero u_i give
D_ij=(u_i^2 D_jj+u_j^2 D_ii)/(2u_i u_j), so D=u w^T+w u^T with
w_i=D_ii/(2u_i). Therefore k:V -> R^3 is an isomorphism. Also

    sum_ij k_ij(E)=tr E-u^T E u=tr E for E in V.           (6)

Differentiating the exact determinant and pair polynomials at K gives,
uniformly for bounded E in V,

    p_ij'[E]=lambda k_ij(E)+O(tau),
    p123'[E]=tau lambda Delta tr(B^-1 E)+O(tau^2).

For D in T, these derivatives have orders O(tau) and O(tau^2),
respectively; the leading normal determinant differential annihilates T.
The singleton and empty derivatives remain bounded. Thus the full Fisher
has blocks

    F_TT=O(1), F_TV=O(1),
    F_VV=(lambda/tau) H_B+O(1),
    H_B(E,Q)=sum_ij k_ij(E) k_ij(Q)/h_ij.                 (7)

H_B is uniformly positive definite on V by the isomorphism and the
compact bounds on h_ij. Similarly

    g_T=O(1),
    g[E]=tau^-1 ell_B(E)+O(1),
    ell_B(E)=tr(B^-1 E)-sum_ij k_ij(E)/h_ij, E in V.      (8)

In (8), the + triple log contributes the trace term and the three negative
pair logs contribute the sum; all four large terms are retained.
By (5), subtracting gg^T/Z changes the VV block only by O(1), the TV block
by O(tau), and the TT block by O(tau^2). Hence (7) also holds for Fpair.

## 5. Solve the true six-dimensional M system

By (5), dG=L Q0+O(1), where

    Q0(D,E)=(1-lambda) tr(A^-1 D A^-1 E).

The leading TV block is zero: A preserves span(u) and u-perp, whereas
T consists of the first row/column and V of the lower 2 by 2 block.
Also eta(D)=L^-1 tr(A^-1 D)+O(L^-2). Consequently

    M_TT=L Q0_TT+O(1), M_TV=O(1),
    M_VV=(lambda/tau) H_B+O(L).                          (9)

The inverses in (9) have uniform bounds O(1/L) and O(tau). Schur inversion
then first gives h_T=O(L^-2), h_V=O(tau/L). To identify the coefficients,
on T the equation Q0(uu^T,D)=tr(A^-1D) holds: writing
D=u w^T+w u^T, both sides equal 2(u^T w)/(1-lambda).
On V, eta(E)=tr(E)/L+O(L^-2). Using (6), H_B(B,E)=tr E.
Putting these facts into the two block equations gives

    h_T=uu^T/L^2+O(L^-3),
    h_V=tau B/(lambda L)+O(tau L^-2).                    (10)

For clarity, the second inverse's O(tau^2 L) remainder times an O(1/L)
right side is O(tau^2), absorbed into O(tau/L^2) because tau L^2->0.
The TV feedback O(tau/L), after the TT inverse, is O(tau/L^2),
absorbed into the first remainder. Thus (10) controls the degenerating
system, rather than interchanging a singular inverse with a limit.

Combining (8) and (10), the T contribution to g^T h is O(L^-2), while

    g[h_V]=(1/(lambda L)) ell_B(B)+O(L^-2),
    ell_B(B)=tr(I_2)-sum of three ones=2-3=-1.

This proves (1). Dividing by sqrt Z from (5) proves (2). The universal
negative sign comes from two soft determinant degrees versus three pair
events and specifically uses the normal component of the actual M solve.

## 6. The first correction to d alpha

This part explains the attractive near-critical value, but does not give
a beta-zero sequence. Restrict the exact positive form Q=dG to T and
write a=u^T N^-1u. Directly, for D=u w^T+w u^T,

    Q(uu^T,D)=d a eta(D).

Therefore Q_TT^-1 eta_T=uu^T/(d a), and its exact trace Rayleigh value is
eta_T^T Q_TT^-1 eta_T=1/d. This identity holds for the actual N, including
its bounded logarithmic corrections. A Neumann expansion for
M_TT=Q_TT+Fpair_TT, with Q_TT of order L and Fpair_TT bounded, yields

    d alpha_T=1-Fpair(uu^T,uu^T)/(d a^2)+O(L^-2).         (11)

Along the radial direction uu^T, only the limiting empty and singleton
probabilities contribute to the leading Fisher cost. They give

    Fpair(uu^T,uu^T)=1/[lambda(1-lambda)]+O(tau),
    d a^2=L/(1-lambda)[1+O(L^-1)].

The projected rank-one subtraction here is O(tau^2), since g[uu^T]=O(1).
Finally the exact block inverse gives

    alpha-alpha_T
      =(eta_V-M_VT M_TT^-1 eta_T)^T
       (M_VV-M_VT M_TT^-1 M_TV)^-1
       (eta_V-M_VT M_TT^-1 eta_T)=O(tau/L^2).

Multiplying by d=O(L^3) gives O(tau L), absorbed in O(L^-2). Substitution
into (11) proves (3), with a negative first correction for all small tau.

## 7. Why this is not the requested global theorem

On this collar beta is strictly negative; B0's antecedent never holds.
The result excludes a mechanism for bringing beta zeros to the boundary.
It does not bound d alpha on the rest of the zero set. It cannot be made
uniform by silently allowing u_i=0: the isomorphism k in Section 4 then
fails, and its coercivity constants can tend to zero before the limit.
Similarly, degenerating Delta invalidates the uniform inverse and log
estimates. Those are actual remaining regimes, not removable wording.

## 8. Complement-signed affine corollary: no zero can enter the corner

Let S be any diagonal sign matrix, v=Su, and fix the same lambda,u. Put

    A_epsilon=epsilon I+lambda uu^T,
    K(epsilon,t)=(1-t)A_epsilon+t S(I-A_epsilon)S.

For epsilon,t>=0 and tau=epsilon+t>0, set r=t/tau in [0,1]. Exact algebra
gives

    K=lambda uu^T+tau C_r-2epsilon t I,
    C_r=I-lambda r(uu^T+vv^T).

The last term is O(tau^2) uniformly. On u-perp,

    B_r=I_{u-perp}-lambda r(Pv)(Pv)^T,
    Delta_r=1-lambda r[1-(u^T v)^2]>=1-lambda>0.

Thus C_r is a compact family satisfying Section 1. There exists delta>0
such that every point with 0<epsilon+t<delta has beta<0 and d alpha<1.
In particular no exact beta-zero sequence in this affine family can have
both epsilon->0 and t->0 with fixed full-support u and fixed lambda.
This covers t/epsilon tending to zero, a finite value, or infinity.
It does NOT rule out a root with epsilon->0 and t tending to a positive
value, nor a sequence with u or lambda changing.

## 9. Verification status

The proof is analytic and does not use numeric signs as premises.
The author independently reconstructed the eight-probability derivatives
in probe.py and ran nine fixed high-precision checks on a server, with
one thread and no GPU. probe_output.json records the actual PID, versions,
inputs, values and normalized asymptotic ratios. These are finite author
diagnostics, not interval certificates, not a review and not a proof of
an explicit numerical collar radius. Independent nonauthor review is
pending. The global frozen B0 statement is unchanged.


---

# Part III — original geometry/sparse_proof.md

# Exact beta zeros approaching a sparse rank-one boundary

Author candidate, independent review pending. Frozen B0 is unchanged.
This is a PARTIAL result relevant to its zero set, not a proof of B0.
The shared definitions and eight-event/Fpair/cofactor reconstruction are
given in Sections 1-2 of the accompanying proof.md; this file uses those
exact definitions throughout.

## 1. Statement and consequences

Fix lambda=7/10 and s=2/5. For epsilon>0 and kappa in [1,10], put

    u=(sqrt(s(1-kappa epsilon)),
       sqrt((1-s)(1-kappa epsilon)),sqrt(kappa epsilon)),
    K(epsilon,kappa)=epsilon I+lambda uu^T,
    L=log(1/epsilon).

For all sufficiently small epsilon there is at least one exact
kappa_epsilon in (1,10) with beta(K(epsilon,kappa_epsilon))=0. Every such
zero in [1,10] satisfies

    kappa_epsilon = kappa_* + O(1/L),
    kappa_*=(3/7)(exp(40/21)-1),
    d alpha(K(epsilon,kappa_epsilon))
       =1-10/(7L)+O(L^-2) < 1.                            (S1)

In particular d alpha tends to 1 along exact beta zeros. No constant
delta>0 can satisfy d alpha<=1-delta on the entire connected strict
beta-zero set. We do not assert uniqueness of the actual zero, a specified
numeric epsilon threshold, a violating zero, or the global bound d alpha<=1.
If B0 is eventually proved, this result shows its constant 1 is sharp.

We prove the uniform asymptotic underlying the assertion for any fixed
lambda in (0,1), fixed s in (0,1), and compact positive kappa interval.
Set

    a=1-lambda, A=a+lambda kappa, R=1+lambda kappa,
    m=log(A/a), D=a+lambda^2 kappa,
    J=2lambda kappa+mD,
    C(kappa)=kappa[(2lambda-1)-lambda a m]/(a J).

Uniformly on that interval,

    L g^T M^-1 eta = C(kappa)+O(L^-1),                    (S2)
    beta = epsilon sqrt(lambda)/L [C(kappa)+O(L^-1)],     (S3)
    d alpha = 1-1/(lambda L)+O(L^-2).                    (S4)

This support-loss regime is expressly excluded from proof.md's uniform
negative collar; there is no contradiction between the two results.

## 2. Exact probabilities and limiting log data

For a unit u, w_i=u_i^2, the matrix determinant lemma applied to
K(I-K)^-1, or direct substitution into all eight polynomials, gives exactly

    p0=(1-epsilon)^2(1-epsilon-lambda),
    p123=epsilon^2(epsilon+lambda),
    p_i=(1-epsilon)[epsilon(1-epsilon-lambda)+lambda w_i],
    p_ij=epsilon[epsilon(1-epsilon-lambda)+lambda(w_i+w_j)]. (S5)

These formulas are only used to expand values on the family. Their
epsilon/kappa derivatives are NOT used as substitutes for the six
K-coordinate derivatives. Those derivatives come from the polynomial
event map in proof.md Section 2.

Let w=(sqrt(s),sqrt(1-s),0), n=(sqrt(1-s),-sqrt(s),0), and e=e3.
In the orthonormal basis (w,n,e), the central K is exactly

    [[epsilon+lambda(1-kappa epsilon),0,
       lambda sqrt(kappa epsilon(1-kappa epsilon))],
     [0,epsilon,0],
     [lambda sqrt(kappa epsilon(1-kappa epsilon)),0,
       epsilon(1+lambda kappa)]].

Its eigenvalues are epsilon,epsilon,epsilon+lambda, so strictness holds
for 0<epsilon<a. Connectivity follows from all u_i nonzero when
epsilon<1/max(kappa). From (S5),

    p0=a+O(epsilon), p1=lambda s+O(epsilon),
    p2=lambda(1-s)+O(epsilon), p3=epsilon A+O(epsilon^2),
    p12=lambda epsilon+O(epsilon^2),
    p13=lambda s epsilon+O(epsilon^2),
    p23=lambda(1-s)epsilon+O(epsilon^2),
    p123=lambda epsilon^2[1+O(epsilon)].

Consequently ell13,ell23=-m+O(epsilon), Lambda=m+O(epsilon), and
ell12=-L+c12+O(epsilon), c12=log(a/(lambda s(1-s))). In the (w,n,e)
basis this gives

    Nww=ma+O(epsilon), Nnn=m+O(epsilon), Nwn=O(epsilon),
    Nwe=-m lambda sqrt(kappa epsilon)+O(epsilon^(3/2)),
    Nne=0,
    Nee=L-c12+O(epsilon),
    d=m^2 a L[1+O(L^-1)], Z=(lambda epsilon^2)^-1[1+O(epsilon)]. (S6)

Nne is exactly zero because both the diagonal log term and K have no
n-to-e entry in this basis. Inverting this positive block matrix yields

    eta(ww^T)=1/(ma)+O(epsilon), eta(nn^T)=1/m+O(epsilon),
    eta(we^T+ew^T)=2lambda sqrt(kappa epsilon)/(a L)
                    +O(sqrt(epsilon)/L^2),
    eta(ee^T)=1/L+O(L^-2),
    eta(wn^T+nw^T)=O(epsilon),
    eta(ne^T+en^T)=O(epsilon^(3/2)/L).

All constants are uniform because kappa stays in a compact positive
interval; m and A are bounded away from zero. N>0 and then M>0 follow.

## 3. Six genuine directions and the essential common-event cross term

Use direction bases

    U=ww^T, T=wn^T+nw^T, Q=nn^T,
    V=we^T+ew^T, W=ne^T+en^T, Z0=ee^T.

The coordinate coefficient on an off-diagonal basis is the actual matrix
entry, not twice that entry. Every Fisher and g computation below uses
the full eight-event derivative map.

To display the leading computations economically, let a scaled direction
have entries delta U=t, delta V=sqrt(epsilon) v,
delta Z0=epsilon z. The leading derivatives of (p3,p13,p23)/epsilon are

    U:  (-R, R s, R(1-s)),
    v:  (2lambda sqrt(kappa),-2lambda sqrt(kappa)s,
                                      -2lambda sqrt(kappa)(1-s)),
    z:  (a,lambda s,lambda(1-s)).                         (S7)

The triple probability is of lower order, but its log derivative is NOT
negligible. Direct determinant differentiation gives

    g[U] = -kappa-R/A+1/a+O(epsilon),
    sqrt(epsilon) g[V] = 2sqrt(kappa)R/A+O(epsilon),
    epsilon g[Z0] = -lambda kappa/A+O(epsilon),
    g[Q]=O(1), g[T]=O(1), g[W]=O(epsilon^-1/2).           (S8)

For example, g[V] receives -2sqrt(kappa)/sqrt(epsilon) from p123,
+2lambda sqrt(kappa)/(A sqrt(epsilon)) from p3, and
+4sqrt(kappa)/sqrt(epsilon) from the two negative pair logs. For g[U],
the triple log contributes R/lambda; the singleton logs contribute
2/lambda-R/A; the empty log contributes 1/a; and the three negative pair
logs contribute -1/lambda-2R/lambda. These sum to (S8). For g[Q], the
order 1/epsilon terms of the triple and p12 log derivatives cancel;
all other contributions are bounded. Thus no rare log term is omitted.

Put H=1/A+1/lambda. Squaring the derivatives in (S7) against the true
leading probabilities yields

    Fvv=4lambda^2 kappa H,
    Fvz=2lambda sqrt(kappa)(a/A-1),
    Fzz=a^2/A+lambda,
    Fav_rare=-2lambda sqrt(kappa) R H,
    Faz=R(1-a/A).                                       (S9)

Here F(V,V)->Fvv, sqrt(epsilon)F(V,Z0)->Fvz,
epsilon F(Z0,Z0)->Fzz, F(U,V)/sqrt(epsilon)->Fav, and F(U,Z0)->Faz.
The last two limits require the common events as well. For U the common
event derivatives (p0,p1,p2) tend to (-1,s,1-s). For V their derivatives,
divided by sqrt(epsilon), tend to
(-2lambda sqrt(kappa),2lambda sqrt(kappa)s,
2lambda sqrt(kappa)(1-s)). Therefore

    Fav_common = 2lambda sqrt(kappa)/a+2sqrt(kappa)
               =2sqrt(kappa)/a,
    Fav= -2sqrt(kappa)R^2/A+2sqrt(kappa)/a.               (S10)

For Faz the common contribution is +1-1=0. Common-event V,V and V,Z0
terms have smaller order, but their U,V cross term (S10) is leading.
Omitting it gives an incorrect sign mechanism. A failed derivation which
omitted it is recorded in attempts.md and is not a theorem.

Since Z in (S6) is order epsilon^-2, subtracting gg^T/Z changes none of
the limits (S9)-(S10): e.g. its U,V term is O(epsilon^(3/2)), its V,V
term O(epsilon), and its V,Z0 term O(sqrt(epsilon)). Hence the limits
are the exact Fpair limits too.

## 4. Cofactor blocks and control of the unused directions

Using (S6) in dG gives

    dG(U,U)=L/a+O(1),
    dG(V,V)=2m+O(L^-1),
    dG(U,V)/sqrt(epsilon)=2m lambda sqrt(kappa)/a+O(L^-1),
    dG(U,Z0)=o(1),
    sqrt(epsilon)dG(V,Z0)=o(1), epsilon dG(Z0,Z0)=o(1).

The leading M(V,W) and sqrt(epsilon)M(Z0,W) vanish, while
M(W,W)->4lambda kappa+2ma>0. In each leading Fisher cross term this is
the cancellation sum_i w_i n_i=0; in dG it follows from the diagonal
leading (w,n) block. In particular M(U,W)=O(epsilon^(3/2)L), not a
leading sqrt(epsilon) source. One may replace the displayed bound by
any weaker uniform bound with this vanishing leading coefficient.

For completeness the other block orders, obtainable by inserting the
same six direction bases into the polynomial derivatives, are

    M(T,T)=2L+O(1), M(Q,Q)=lambda/epsilon+O(L),
    M(U,T)=O(epsilon L), M(U,Q)=O(1),
    M(T,V)=O(epsilon^(3/2)L), M(T,W)=O(sqrt(epsilon)L),
    M(T,Z0)=O(epsilon L),
    M(Q,V),M(Q,W)=O(sqrt(epsilon)L), M(Q,Z0)=O(1).

M(T,Q)=O(1)+O(epsilon L). These deliberately nonsharp bounds suffice.
All polynomial derivatives are rational in sqrt(epsilon), with
denominators consisting of the positive event probabilities. After the
explicit leading powers in (S5) are removed, coefficients and their
remainders are bounded on compact kappa intervals. The logs only enter
dG through the explicitly inverted matrix (S6). Thus the table is a
uniform finite-dimensional expansion, not an inference from probes.

Eliminate Q and T by Schur complements: their inverse orders are
O(epsilon) and O(1/L), and the remaining V,W,Z0 block, after scaling Z0
by sqrt(epsilon), has a uniformly positive limiting matrix. The V,Z0
part is the matrix in (S11) below, whose positive determinant is displayed
there; W has the separate positive limit above. This gives the bounds
needed to solve the full system, rather than freezing arbitrary tangent
components:

    h_U=1/(mL)+O(L^-2), h_Q=O(epsilon), h_T=O(L^-2)+O(epsilon L),
    h_V=O(sqrt(epsilon)/L), h_Z0=O(epsilon/L),
    h_W=O(sqrt(epsilon)/L^2)+O(epsilon^(3/2)L^2).

Sharper h_T=O(epsilon L) follows from its displayed small source terms;
the weaker version written above is enough for g^T h. The W estimate
uses its vanishing leading U,V,Z0 couplings; even the weaker T bound
then supplies only O(sqrt(epsilon)/L^2) after its actual leading
M(T,W)=O(sqrt(epsilon)) coefficient from (S7) and dG is used.
Equivalently one can first use the sharper h_T bound with the coarser
O(sqrt(epsilon)L) entry; either gives the stated negligible g[W] h_W.

## 5. The exact leading two-dimensional solve and its sign

Write h_V=sqrt(epsilon)(v+O(L^-1))/L and
h_Z0=epsilon(z+O(L^-1))/L. The leading equations of M h=eta are

    [[Fvv+2m,Fvz],[Fvz,Fzz]] [v,z]^T
       =[-Fav/m, 1-Faz/m]^T.                            (S11)

In its first row, the cofactor source from h_U is
2lambda sqrt(kappa)/a, exactly the leading eta[V] source after dividing
by sqrt(epsilon)/L. Their cancellation leaves -Fav/m. Thus (S11) is
the leading equation of the actual optimizer, not a chosen Lambda tangent.

Using D=a+lambda^2 kappa, the determinant of the S11 matrix is

    2(2lambda kappa+mD)/A = 2J/A >0.

It is uniformly bounded below on a compact positive kappa interval.
Ordinary bounded inverse perturbation gives the asserted O(L^-1) errors.
Solving yields

    v=sqrt(kappa) lambda kappa [lambda+(1-2lambda)/(a m)]/J,
    z=[lambda kappa R+mA-2lambda^2 kappa^2/(a m)]/J.       (S12)

Combining (S8), the negligible T,Q,W contributions, and (S12),

    L g^T h = (-kappa-R/A+1/a)/m
                +(2sqrt(kappa)R/A)v-(lambda kappa/A)z+O(L^-1)
            =kappa[(2lambda-1)-lambda a m]/(a J)+O(L^-1).

For checking the final simplification, first solve (S11) with the common
cross term deleted. Its resulting coefficient would be
kappa[2+(2lambda-1)m-lambda a m^2]/(a m J).
The missing common term contributes exactly -2kappa/(a m J), leaving
the expression above. This is also a compact audit of the dangerous
common-event cancellation. Equation (S6) now proves (S3).

## 6. d alpha uniformly approaches one from below

On the one-dimensional direction U, the exact identity G(U,U)=eta(U)^2
holds because U has rank one. In this family

    d eta(U)^2=L/a+O(1),
    Fpair(U,U)=1/(lambda a)+O(epsilon).

Thus its restricted Rayleigh value satisfies

    d alpha_U
      =d eta(U)^2/[d eta(U)^2+Fpair(U,U)]
      =1-1/(lambda L)+O(L^-2).

The same Schur estimates from Section 4 show that freeing Q contributes
at most O(epsilon) to alpha, freeing T contributes O(L^-3), and the
remaining V,W,Z0 residual contributes O(epsilon/L^2) plus terms of those
same smaller orders. Indeed the residual sizes after solving U are
O(1), O(1/L)+O(epsilon), O(sqrt(epsilon)/L), and O(1/L)
in Q,T,V,Z0, with inverse orders epsilon,1/L,1,epsilon.
Their bounded cross terms are controlled by the positive Schur matrix.
Multiplying by d=O(L) gives O(epsilon L)+O(L^-2), proving (S4).
No statement about all directions' entropy curvature is inferred here.

## 7. Exact zeros, localization, and absence of a uniform safety margin

For lambda=7/10, the numerator of C(kappa) vanishes exactly when
m=40/21. Its derivative there is negative, and

    C'(kappa_*)=-kappa_* lambda^2/(A(kappa_*) J(kappa_*))<0.

At kappa=1, m=log(10/3)<3/2<40/21: the first inequality follows from
exp(3/2)>1+3/2+(3/2)^2/2=29/8>10/3. At kappa=10,
m=log(73/3)>2>40/21 since exp(2)<9<73/3; exp(1)<3 follows directly
from its convergent factorial series. Therefore C(1)>0 and C(10)<0.

The uniform error in (S3) preserves these strict signs for all sufficiently
small epsilon. Since the eight probabilities, N and M are nonsingular
throughout the compact kappa interval for these epsilon, beta is a
continuous function of kappa. The intermediate value theorem produces
at least one exact beta zero in (1,10) for every sufficiently small
epsilon. This is an analytic existence proof, not a near-zero convention.

The function C has a unique zero on [1,10] and has nonzero derivative
there. At an exact zero of beta, (S3) gives |C(kappa)|=O(1/L) uniformly.
Away from any fixed neighborhood of kappa_*, |C| has a positive minimum;
within a sufficiently small neighborhood the mean value theorem gives
|C(kappa)|>=c|kappa-kappa_*|. This proves the uniform localization in S1
without claiming uniqueness of the finite-epsilon roots. Finally (S4)
is uniform on the entire interval, so it applies to every selected exact
root. Its negative 1/L term dominates its O(L^-2) remainder and proves S1.

## 8. Verification and limits

This candidate requires nonauthor review, especially the six-dimensional
block remainders in Section 4. No finite numeric sign is a premise of
the theorem. Six prescribed diagnostic points, not an expanded scan,
are recorded in sparse_probe.py and sparse_probe_output.json. An additional
single-point coefficient audit identified the initially omitted common
cross term; sparse_detail.py and its output retain the failed predicted
values transparently. The corrected closed-form coefficient and the
event/geometry decomposition are the present proof's basis.

B0 remains unresolved; this theorem supplies neither a violation nor
a bound on the rest of its zero set. Novelty is not certified.


---

# Part IV — original mechanism/proof.md

# Proof and Computation Notes

## Rebuilding the B0 quantities

For a mask M subset of {1,2,3}, form the 3 by 3 matrix `A_M` by starting with
K and subtracting 1 from diagonal entry i when i is absent from M.  Then

    p_M = (-1)^(3-|M|) det(A_M).

This determinant form is the exact eight-event DPP probability formula for
n=3.  It also gives the first derivative in each symmetric coordinate:

    J_{M,(ij)} = (-1)^(3-|M|) (cof_{ij}(A_M)+cof_{ji}(A_M))

for i != j, and the single cofactor for diagonal coordinates.  This keeps the
off-diagonal factor two.

With p and J rebuilt, the script computes

    g_j = partial_j Lambda
        = sum_M (-1)^(3-|M|) J_{M,j}/p_M,
    Z = sum_M 1/p_M,
    F = J^T diag(1/p_M) J,
    F_pair = F - g g^T/Z.

The logarithmic matrix is

    N = -diag(ell_23, ell_13, ell_12) - Lambda K.

Let `adjN=adj(N)`, `d=det(N)`,

    a_j = tr(adjN E_j),
    T_ij = tr(adjN E_i adjN E_j).

Since `N^-1=adjN/d`, the matrix

    Htilde = d F_pair + T

equals `d M`, and `a=d eta`.  Therefore the linear solve

    Htilde h = a

gives `h=M^-1 eta`.  The two scalar tests used by the certificate are then

    beta sqrt(Z) = g^T h,
    d alpha = a^T h.

The actual optimizer direction is reconstructed as

    D_M = h/alpha,  alpha=(a^T h)/d.

The JSON output records `eta(D_M)` and `Lambda'(D_M)` at root midpoints as a
sanity check.  At the certified zero the exact sign change is on
`beta sqrt(Z)`, which is equivalent to beta because `Z>0`.

## Certified sparse-edge root

For epsilon=10^-8 set

    u(q)=(3/5,4/5,q/10000),
    K(q)=10^-8 I + (7/10) u(q)u(q)^T.

All entries are rational for rational q.  On the bracket

    q_L = 4418854248579277079/2305843009213693952,
    q_U = 8837708497158554159/4611686018427387904,

the eigenvalue formula gives strict feasibility:

    spec(K) = {epsilon, epsilon, epsilon+(7/10)(1+q^2 epsilon)}.

The interval certificate uses exact Fractions rounded outward to a dyadic grid
for every arithmetic operation.  Logarithms are enclosed by exact range
reduction to [1,2) followed by the positive-tail atanh series.  The interval
linear solve is Gaussian elimination with every pivot interval excluding zero;
the resulting residual intervals contain zero.

The endpoint beta signs are strictly enclosed:

    beta(q_L) sqrt(Z) > 4.67407989657799e-22,
    beta(q_U) sqrt(Z) < -2.49393515852079e-21.

All event probabilities are positive on the whole bracket:

    min_M p_M > 7.0000003569096650512e-17.

The leading minors of N are positive on the whole bracket; in particular

    det(N) > 27.2394697841539050297.

The same whole-bracket interval solve proves

    det(N) alpha < 0.925806704946127239064572716414179284 < 1.

By continuity of the rebuilt p, logs and nonsingular solve on this bracket,
the intermediate value theorem gives at least one exact q_* in (q_L,q_U) with
beta(K(q_*))=0.  The whole-bracket bound then applies to that exact beta-zero
kernel, so it satisfies B0 with a visible margin.

## What this does not prove

The proof above does not show that every beta-zero kernel satisfies B0, nor
that the sparse-edge root is unique.  It also does not prove the asymptotic
formula for the whole root tube; it only supplies a certified finite point and
a deterministic high-precision trend table.


---

# Part V — interval error enclosure (integration note)

# Soundness of the finite certificate arithmetic

This integration note explains the error enclosure in the included
mechanism/scripts/sparse_rational_certificate.py. It does not assert the
global B0 inequality or a new asymptotic theorem.

Every interval endpoint is a Python Fraction, hence an exact rational.
The constructor rounds a rational lower endpoint down and upper endpoint
up to multiples of 2^-620. Addition, negation and multiplication use the
ordinary endpoint enclosure formulas, followed by the same outward rounding.
Division is only performed after excluding zero from the denominator
interval, using the reciprocal interval [1/upper,1/lower]. Induction on
the finite arithmetic expression therefore proves containment of every
exact value, even though repeated uses of a dependent input can widen it.

For logarithms, write x=2^k y with 1<=y<2 and integer k. For
z=(y-1)/(y+1) in [0,1/3], the convergent atanh series gives

    log(y)=2 sum(j>=0) z^(2j+1)/(2j+1).

With n=110 retained terms, its nonnegative remaining tail is at most

    2 z^(2n+1)/[(2n+1)(1-z^2)].

Indeed each remaining denominator is at least 2n+1 and the remaining
powers form a geometric series with ratio z^2. The same formula bounds
log(2), using z=1/3. Thus log(x)=log(y)+k log(2) has rational lower and
upper bounds; the endpoints of k log(2) are reversed for negative k.
Monotonicity of log extends this to positive input intervals by using the
lower input's lower log bound and the upper input's upper log bound.
All these endpoints are then rounded outward. No floating log is used
to decide a certified sign.

The exact p and coordinate Jacobian polynomials are evaluated through
these interval operations. Positive atom bounds make all divisions and
logs valid. Positive leading principal minors prove N>0 on the complete
input q interval by Sylvester's criterion. The formula reconstruction
then gives d>0, Fpair>=0, and M=Fpair+dG>0. Alternatively the actual
Gaussian interval elimination records pivot intervals avoiding zero at
every step; hence for each concrete q, its exact elimination and solution
are enclosed by the computed intervals. A residual interval containing
zero is a consistency check, not a substitute for pivot or positivity
arguments.

The exact identities Htilde=dM, a=d eta reduce the solve to
Htilde h=a, with h=M^-1 eta, beta sqrt(Z)=g^T h, and d alpha=a^T h.
The resulting endpoint sign enclosures and whole-bracket bound therefore
apply to the genuine optimizer. Floating bisection is used only to propose
the rational bracket; strict endpoint signs are recomputed by the exact
interval procedure. Since all quantities are continuous and nonsingular
throughout that bracket, the intermediate value theorem supplies an exact
beta zero. No numerical near-zero is promoted to equality.

The JSON's exact Fraction endpoints are authoritative. Its decimal fields
are also rounded outward explicitly by floor/ceiling on a decimal grid.
The weaker decimal bounds in RESULT.md deliberately preserve that direction.
