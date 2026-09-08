# General tomography kernel: the second logarithmic term vanishes

Author status: PROVED for the statements below, pending independent
verification. This supplements `mixed_boundary_v2.md` and does not claim a
global sign for the final ordinary second-order coefficient.

## Result

The proposed formula is correct under the fixed B=0 feasible-family assumptions:

    L2=-2 sum_(|S|=r, det U_S=0) q_S(X,Y),
    q_S(X,Y)=tr(X T_S Y T_S^T).                         (1)

However, its right-hand side is zero, event by event, on the tomography kernel. More strongly,

    M_U(X)=0 and det U_S=0
          imply T_S^T X T_S=0,

for every real symmetric Y, even without M_V(Y)=0. Thus the restricted bilinear form suggested in the task is identically zero and reversing Y cannot create a positive epsilon^2 log coefficient. The general ordinary epsilon^2 coefficient remains unsigned here.

## 1. Exact assumptions and the maps

Fix orthonormal U in R^(n by r), V in R^(n by m), m=n-r, with [U V] orthogonal. Let A,C,X,Y be fixed real symmetric matrices of the corresponding dimensions. Assume

    H_sigma=A-sigma X>=0,
    L_sigma=C+sigma Y>=0, sigma=+1,-1.

For every sufficiently small positive epsilon the block-diagonal endpoint

    K_sigma=[U V] diag(I-epsilon H_sigma,epsilon L_sigma)[U V]^T

is a positive contraction. Its center uses H_0=A,L_0=C. No strict positivity is required. All event probabilities are the full exact DPP law, obtained by inclusion-exclusion, or equivalently by its spectral mixture.

For |R|=r-1 let w_R be the cofactor vector of U_R, with

    (w_R)_i=(-1)^(r+i)det(U_(R,{1,...,r}\{i})),

and for |T|=r+1 let (z_T)_j=det([U,v_j]_T). Define

    (M_U(X))_R=w_R^T X w_R,
    (M_V(Y))_T=z_T^T Y z_T.

Assume the full rate invisibility conditions M_U(X)=M_V(Y)=0. Cauchy-Binet, or orthonormality of the exterior coordinate frames, gives

    sum_(|R|=r-1) w_R w_R^T=I_r,
    sum_(|T|=r+1) z_T z_T^T=I_m.

Taking traces against X,Y proves tr X=tr Y=0. These are consequences of the complete maps, not replacements for them.

The first exact-event probabilities of cardinality r-1 and r+1 have rates w_R^T H_sigma w_R and z_T^T L_sigma z_T. The assumptions make these rates identical at the two endpoints and the center, coordinate by coordinate. The first variation of supported r-events also agrees because it is -[tr H_sigma+tr L_sigma]det(U_S)^2. Thus every event has the same constant and linear coefficient in epsilon at all three kernels.

## 2. A zero one-flip rate cannot hide an extra second-order log mode

This point is essential when A or C is singular. Diagonalize a fixed endpoint's H and L, with eigenvalues h_i,l_j>=0. For |R|=r-1, the full spectral mixture has a one-hole contribution

    sum_i epsilon h_i product_(k!=i)(1-epsilon h_k)
                       product_j(1-epsilon l_j)
                       d_(R,i)^2,

where d_(R,i) is the minor of the remaining r-1 high eigenvectors. Its first coefficient is the nonnegative sum sum_i h_i d_(R,i)^2. If that sum is zero, every h_i d_(R,i)^2 is zero and the entire displayed one-hole contribution is identically zero, not merely first-order zero. All other eigenmode selections of cardinality r-1 require at least two holes and one particle, hence at least three flips. Their total probability is O(epsilon^3).

The same argument applies to cardinality r+1. Since rate invisibility makes a zero center rate zero at both endpoints, such events have no second-order probability at any of the three kernels. Consequently all epsilon^2 log terms from the one-flip cardinalities can be counted using their total second coefficients; no zero first-rate events need an extra factor of two.

This argument uses nonnegativity of the spectral weights and exact-event squared minors. A vanishing signed sum of inclusion minors alone would not justify it.

## 3. Pure-hole and pure-particle logarithmic terms cancel

Let e2(H)=((tr H)^2-tr(H^2))/2, with e2=0 in dimension one. The eigenmode-selection generating function, expanded to second order, gives the following total probabilities by cardinality:

    Pr_H,L(|S|=r-2)=epsilon^2 e2(H)+O(epsilon^3),
    Pr_H,L(|S|=r-1)=epsilon tr H
        -epsilon^2[2e2(H)+tr H tr L]+O(epsilon^3),
    Pr_H,L(|S|=r+1)=epsilon tr L
        -epsilon^2[2e2(L)+tr H tr L]+O(epsilon^3),
    Pr_H,L(|S|=r+2)=epsilon^2 e2(L)+O(epsilon^3).      (2)

Cardinalities outside [0,n] are absent and contribute zero; the corresponding e2 term is then zero. A two-hole event starts at epsilon^2 and hence contributes twice its leading coefficient to the epsilon^2 log(1/epsilon) entropy coefficient. A positive one-hole rate starts at epsilon, so its second coefficient has logarithmic weight one. Section 2 handles zero one-hole rates. All events at distance at least three from r are O(epsilon^3) and irrelevant at this order.

Let delta denote the average of the plus/minus expression minus its center value. Because tr X=tr Y=0,

    delta e2(H)=e2(X)=-tr(X^2)/2,
    delta e2(L)=e2(Y)=-tr(Y^2)/2,
    delta[tr H tr L]=0.

Therefore the combined r-2 and r-1 logarithmic coefficients are

    2[-tr(X^2)/2]+tr(X^2)=0,

and r+1 together with r+2 gives the analogous zero for Y. This is exact cancellation of all pure-hole/pure-particle contributions. It remains valid with individual zero second-order probabilities, because a zero coefficient contributes zero and its higher-order entropy is O(epsilon^3|log epsilon|).

## 4. The remaining r-event term is the proposed formula

Define, for every r-set S,

    (T_S)_(i,j)=det((U with column i replaced by v_j)_S).

If det U_S=0, the no-flip law gives zero exactly and a one-flip selection has the wrong cardinality. The leading epsilon^2 term comes from one hole and one particle. For diagonal H,L the spectral mixture gives sum_(i,j) h_i l_j (T_S)_(i,j)^2. Orthogonal changes of high/low frames, or multilinearity of the corresponding exterior tensors, give for general symmetric H,L

    p_H,L(S)=epsilon^2 q_S(H,L)+O(epsilon^3),
    q_S(H,L)=tr(H T_S L T_S^T).                         (3)

The replacement-column convention fixes all signs; the trace is invariant under orthogonal diagonalization. Since H,L>=0, q_S(H,L)>=0.

Bilinearity gives

    [q_S(A-X,C+Y)+q_S(A+X,C-Y)]/2-q_S(A,C)
       =-q_S(X,Y).

These zero r-events have logarithmic weight two. Supported r-events have a positive constant probability and their entropy is smooth, so they have no logarithmic term. Combining this with section 3 proves formula (1).

## 5. Adjugate geometry annihilates every summand

Write M=U_S, N=V_S. Expansion in the replacement column gives exactly

    T_S=adj(M) N.                                      (4)

Suppose det M=0.

- If rank M<=r-2, all (r-1)-minors vanish, adj(M)=0, and T_S=0.
- If rank M=r-1, adj(M) has rank one and its columns lie in ker M. Thus T_S=a b^T for a nonzero vector a spanning ker M and some b (possibly zero).

In the second case choose r-1 linearly independent rows of M and let R be the corresponding subset of S. The cofactor vector w_R is nonzero, satisfies U_R w_R=0, and spans ker U_R. Since U_R and M both have rank r-1 and ker M subset ker U_R, these kernels coincide. Therefore w_R is a nonzero scalar multiple of a. The tomography condition w_R^T X w_R=0 implies a^T X a=0. Consequently

    T_S^T X T_S=b(a^T X a)b^T=0,
    q_S(X,Y)=tr(Y T_S^T X T_S)=0                       (5)

for every symmetric Y. When r=1 the same reasoning includes the empty row subset: its cofactor vector is the scalar 1, and M_U(X)=0 forces X=0. Thus all admissible ranks are covered.

Equations (1) and (5) prove the universal cancellation

    L2=0                                               (6)

for every fixed feasible B=0 tomography-kernel family. The anticipated nonzero restricted bilinear form does not exist.

There is a useful symmetric strengthening. In the rank-r-1 case, write adj(M)=a d^T so that b=N^T d. Since U has full column rank, choose a row k outside S with u_k^T a!=0. The bordered determinant formula, with an irrelevant overall sign from sorting rows, gives

    det([U,v_j]_(S union {k}))
       =+/-[-u_k^T adj(M)N_j]
       =+/-[-(u_k^T a)b_j].

Thus the addition cofactor vector z_(S union {k}) is a nonzero scalar multiple of b, unless b=0, which is already trivial. The condition M_V(Y)=0 implies b^T Y b=0. It follows that not only the mixed term but both linear terms disappear:

    q_S(X,C)=0, q_S(A,Y)=0, q_S(X,Y)=0,
    q_S(A-X,C+Y)=q_S(A+X,C-Y)=q_S(A,C).                (6a)

Therefore every zero r-event has exactly the same second-order probability coefficient at each endpoint and at the center.

## 6. Why the Hadamard sum was zero

For the four-point Hadamard frame, the zero `r`-sets are `{1,3}` and
`{2,4}`. The corresponding right null vectors of `U_S` are proportional to
`(1,-1)` and `(1,1)`. For `X=x diag(1,-1)`, both `a^T X a` equal zero. Thus
each of the two `q_S(X,Y)` terms vanishes separately for arbitrary `Y`, not
only after summing. The observed cancellation is an instance of (5), not a
numerical accident.

## 7. Exact remaining second-order object

The preceding cancellations imply

    Delta_epsilon=C2 epsilon^2+O(epsilon^3|log epsilon|)

for fixed data, with no asserted sign of C2. A directly checkable expression can be given from the exact-event probability coefficients

    p_sigma(S)=p_0(S)+epsilon a_S+epsilon^2 b_(sigma,S)
                     +O(epsilon^3),

where p_0 is the projection law and a_S is common to endpoints and center. Write b_(0,S) for the center and delta b_S=(b_(+,S)+b_(-,S))/2-b_(0,S). With f(z)=-z log z, f(0)=0,

    C2 = sum_(p_0(S)>0) [-(log p_0(S)+1) delta b_S]
       + sum_(p_0(S)=0,a_S>0) [-(log a_S+1) delta b_S]
       + sum_(p_0(S)=0,a_S=0)
           [(f(b_(+,S))+f(b_(-,S)))/2-f(b_(0,S))].     (7)

In the last sum the b coefficients are nonnegative. Vanishing b means the probability starts at order at least three; its entropy is covered by the remainder. The quadratic entropy term involving a_S^2 at supported events cancels because a_S is common. The full logarithmic coefficient in (7)'s expansion is zero by (6).

For zero r-events, the stronger identity (6a) makes each endpoint b equal to the center b, so their individual last-line contributions in (7) are exactly zero. Formula (7) does not by itself sign the remaining pure-cardinality and supported-event terms. This ordinary epsilon^2 expression, rather than a sign flip of Y in (1), is the next unresolved target.

## Scope

The result is analytic. Finite diagnostics are not used as evidence for the
universal cancellation. Independent verification and the global-concavity
question remain pending/unresolved.
