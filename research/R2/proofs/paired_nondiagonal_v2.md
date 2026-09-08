# Paired rotations with arbitrary PSD inward matrices

Author status: PROVED for the fixed family below, pending independent
verification. The coefficient is exactly the sum of two small-kernel
coefficients; there is no additional cross term.

## 1. Statement, including singular inward matrices

Use any fixed paired rotations `U,V` from `paired_rotations_v2.md`, with one
orthonormal column pair supported on each independent pair of physical
coordinates. Let `A,C` be arbitrary fixed real symmetric PSD `m x m`
matrices, not necessarily diagonal. Let `X,Y` be real symmetric and
zero-diagonal; these are exactly the two full one-flip tomography kernels.
Assume

    A-X>=0, A+X>=0, C-Y>=0, C+Y>=0.                   (1)

For H_sigma=A-sigma X, L_sigma=C+sigma Y define the B=0 endpoints

    K_(e,sigma)=[U V]diag(I-eH_sigma,eL_sigma)[U V]^T.

They and their center are positive contractions for all sufficiently small positive e. All finite data and all pair angles are fixed. The exact-event entropy gap satisfies

    Delta_e=C2 e^2+O(e^3|log e|),
    C2=Gamma(A-X,A+X;A)+Gamma(C-Y,C+Y;C).             (2)

Here Gamma is the ordinary second-order small-kernel chord coefficient, defined and computed explicitly below. In particular C2<=0, strictly if X or Y is nonzero. If X=Y=0, the kernels agree identically and Delta_e=0.

## 2. Explicit small-kernel function

For D>0 let

    G_D(z)=z+(D-z)log(1-z/D), 0<=z<=D,
    G_D(D)=D,
    Phi_D(v)=G_D(v^2), -sqrt(D)<=v<=sqrt(D).

For one matrix A and direction X put a_i=A_ii, D_ij=a_i a_j, u_ij=A_ij, x_ij=X_ij. For D_ij>0 define

    gamma_ij(A,X)
       =Phi_(D_ij)(u_ij)
           -[Phi_(D_ij)(u_ij+x_ij)
                         +Phi_(D_ij)(u_ij-x_ij)]/2.   (3)

Condition (1) gives |u_ij+/-x_ij|<=sqrt(D_ij), so every argument is in the stated domain. If D_ij=0, define gamma_ij=0. This case is forced rather than an arbitrary extension: a zero diagonal entry of a PSD matrix annihilates its entire row and column. Applying this to A and A+/-X shows that a_i=0 forces A_ij=X_ij=0 for every j. Thus no nonzero direction entry occurs in a D=0 pair.

The coefficient in (2) is

    Gamma(A-X,A+X;A)=sum_(i<j)gamma_ij(A,X),
    C2=sum_(i<j)[gamma_ij(A,X)+gamma_ij(C,Y)].          (4)

When A is diagonal, u_ij=0, (3) reduces to -G_(a_i a_j)(x_ij^2), exactly recovering the previous paired theorem.

## 3. Why this is precisely the small-kernel Gamma

Consider the exact-event DPP kernels e(A-X), e(A+X), and eA on m coordinates. For a fixed PSD matrix H, inclusion-exclusion or the full spectral mixture gives, through degree two,

    p_H(empty)=1-e tr H+e^2 e2(H)+O(e^3),
    p_H({i})=e H_ii-e^2 sum_(j!=i)det(H_({i,j}))+O(e^3),
    p_H({i,j})=e^2 det(H_({i,j}))+O(e^3),

and events of size at least three have probability O(e^3). Here e2(H)=sum_(i<j)det(H_({i,j})). These are exact-event coefficients, not the use of a principal minor as a full probability beyond its indicated leading order.

Fix one unordered pair, abbreviate D=a_i a_j, u=A_ij, x=X_ij, and let

    d_0=D-u^2,
    d_+=D-(u+x)^2,
    d_-=D-(u-x)^2,
    f(z)=-z log z, f(0)=0.

Their determinant average differs from the center by -x^2. The empty-event entropy contributes +x^2 to the ordinary second-order chord coefficient. The two singleton finite parts contribute -[log D+2]x^2. The pair entropy contributes [f(d_+)+f(d_-)]/2-f(d_0). Its second-order logarithmic term cancels the singleton second-order logarithmic term. The complete contribution is therefore

    [f(d_+)+f(d_-)]/2-f(d_0)-(1+log D)x^2.             (5)

Using

    f(D-v^2)-(1+log D)v^2=-D log D-Phi_D(v),

reduces (5) exactly to (3). Zero diagonal entries can first be removed, since the corresponding row of H and direction is zero and those coordinates are never selected. Endpoint determinants d_+ or d_- may be zero; the formulas and entropy remainder hold with f(0)=0. Thus (4) is indeed the small-kernel coefficient

    [H(e(A-X))+H(e(A+X))]/2-H(eA)
       =e^2 Gamma(A-X,A+X;A)+O(e^3|log e|).            (6)

No sign assertion is imported into this identification; the sign is proved in section 5.

## 4. Why the paired coefficient splits with no cross term

For a single choice in pair i let p_i(z_i)=u_i(z_i)^2, and let h_i be its binary entropy. Write H_P=sum_i h_i. For positive projection-support configurations put P_z=product_i p_i(z_i) and rho_i=v_i(z_i)/u_i(z_i). The exact-event expansion is the same weighted expansion derived in `paired_rotations_v2.md`; the effect of non-diagonal A,C is as follows.

### Supported r-events

Their second coefficient is

    P_z[e2(H_sigma)+e2(L_sigma)+tr H_sigma tr L_sigma
                      +tr(H_sigma Rho L_sigma Rho)],
    Rho=diag(rho_1,...,rho_m).

Their constant and first coefficients agree at both endpoints and at the center, since diag X=diag Y=0 implies tr X=tr Y=0. Averaging the second coefficient cancels all terms linear in X or Y. Its difference from the center is exactly

    -P_z[sum_(i<j)(x_ij^2+y_ij^2)
                        +2sum_(i<j)x_ij y_ij rho_i rho_j].  (7)

In particular the non-diagonal entries of A and C do not create an additional averaged term. Orthogonality and independence give E[rho_i]=0, E[rho_i rho_j]=0, and E[rho_i rho_j log P_z]=0 for i!=j. Therefore every X/Y cross term in (7) disappears from the ordinary entropy coefficient, even for unequal pair angles. The pure contribution is

    (1-H_P)sum_(i<j)(x_ij^2+y_ij^2).                  (8)

### One-hole and one-particle events

For an empty pair i and other single choices of product weight w, the first rate is w a_i. The second coefficient is

    w[(H_sigma^2)_ii-(tr H_sigma+tr L_sigma)(H_sigma)_ii].

Because the diagonal and total trace are fixed, its averaged difference is w sum_(j!=i)x_ij^2. The analogous double-pair difference is w sum_(j!=i)y_ij^2. The non-diagonal A and C produce linear terms in the separate endpoints, but those cancel in the average; they do not change the displayed squared-direction differences.

### Two-hole and two-particle events

For empty pairs i,j the coefficient is now

    w det((A-sigma X)_({i,j}))=w[D-(u-sigma x)^2],     (9)

instead of the earlier diagonal-center expression w(D-x^2). The two-particle coefficient is its C,Y analogue. These are the only second-order event terms whose endpoint finite entropies retain the non-diagonal center entries.

### Mixed empty/double and newly zero supported events

An empty pair i and a double pair j have second coefficient w(H_sigma)_ii(L_sigma)_jj=w a_i c_j, unchanged. Their replacement amplitude has only its (i,j) entry nonzero. At a degenerate pair angle, an additional zero projection event with exactly one zero-U singleton choice k has a replacement amplitude supported only at (k,k), and its coefficient is again unchanged, proportional to a_k c_k. Events with more such missing high directions have no second-order coefficient. Thus no A/C or X/Y cross term is hidden in projection-zero events.

### Collecting one unordered pair

For the high-side pair i,j, supported and one-hole finite terms combine to

    [H_P-h_i-h_j-1-log D]x^2.

The two-hole finite term in (9), after summing the other-pair product weights, is

    [f(d_+)+f(d_-)]/2-f(d_0)-(H_P-h_i-h_j)x^2.

Their sum is exactly (5). The low-side calculation is independent and identical. Logarithmic terms still cancel because the averaged determinant change remains -x^2 or -y^2. This proves (2)–(4) and the absence of extra cross terms.

### Zero diagonal rates and the remainder

If a_i=0, PSD of A+/-X forces its i-th row and X's i-th row to vanish. Every associated squared-direction contribution is zero; no log a_i is used. Its zero one-hole rate has no second-order probability: in the nonnegative exact spectral mixture, every one-hole term must vanish separately, and the next allowed flip count for that cardinality is at least three. The same argument applies to c_i=0. Pair determinant coefficients can also vanish, but then their probability starts at order at least three and their entropy is O(e^3|log e|). Supported positive projection probabilities are smooth, and all other events are handled by the exact flip count. Since the data and dimension are fixed and the full probabilities are polynomials in e, summing these bounds proves the remainder in (2), including singular A,C and singular endpoints.

## 5. Strict sign of the pair function

Inside the open interval |v|<sqrt(D), direct differentiation gives

    Phi_D'(v)=-2v log(1-v^2/D),
    Phi_D''(v)=-2log(1-v^2/D)+4v^2/(D-v^2)>=0.         (10)

It is strictly positive whenever v!=0. The continuous extension at +/-sqrt(D) is strictly convex on the entire closed interval: on any interval of nonzero length its derivative is strictly increasing, since its second derivative is positive except possibly at the single point zero. Equivalently one may restrict to the open interval and then use continuity at boundary endpoints.

Consequently (3) is nonpositive and is strictly negative whenever x_ij!=0. Such a pair necessarily has D_ij>0 by the zero-row argument. Thus nonzero X or nonzero Y supplies at least one strict term in (4), proving C2<0. No assertion that off-diagonal entries of A or C themselves must vanish is used.

A quantitative strengthening follows because Phi_D(v)-v^4/(2D) is convex: (10) is at least 6v^2/D, using -log(1-z)>=z. Hence

    gamma_ij(A,X)
       <=-[3u_ij^2 x_ij^2/D_ij+x_ij^4/(2D_ij)]        (11)

for D_ij>0, with boundary values obtained by continuity. This is optional for the sign proof but shows that a non-diagonal center can strengthen, not remove, the local loss bound.

## 6. Scope

Arbitrary fixed PSD `A,C` are allowed, and the paired coefficient is exactly
the sum of the high and low small-kernel coefficients. Pair angles may be
arbitrary, including degenerate angles. The proof does not cover non-paired
frames or data varying with `e`; global real DPP entropy concavity remains
unresolved. The result remains author-complete rather than independently
verified.

