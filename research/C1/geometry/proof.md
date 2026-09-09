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
