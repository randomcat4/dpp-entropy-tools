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
