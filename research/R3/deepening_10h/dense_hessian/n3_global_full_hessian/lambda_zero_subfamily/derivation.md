# Lambda zero: Cauchy kernels, exact field scores, and the remaining Schur gate

AUTHOR THEOREM/IDENTITY CANDIDATES, pending independent review.

## 1. Full parameterization by positive weighted Cauchy L matrices

Write L=K(I-K)^(-1)>0. The exact atom identity is
p_S=det(L_S)/det(I+L). To check its semantics, summing these weights with
formal inclusion variables gives det(I+L diag(1+z))/det(I+L)=det(I+K diag z),
whose coefficient of z_A is det K_A. Möbius uniqueness therefore gives
the exact-event law. This is not an identification of p_S with det K_S.

Normalize L to a correlation matrix with offdiagonals A=R12,B=R13,C=R23.
The condition exp Lambda=1 is exactly

det R=(1-A^2)(1-B^2)(1-C^2),
2ABC=A^2 B^2+A^2 C^2+B^2 C^2-A^2 B^2 C^2.                 (1)

If one of A,B,C is zero, (1) forces at most one to be nonzero; this is a
disconnected matrix. K and L have the same block-disconnection partitions,
since each is an invertible rational function of the other. In the connected
case all three are nonzero, and the right side of (1) is positive (rewrite
it as A^2 B^2(1-C^2)+C^2(A^2+B^2)). Thus ABC>0. A diagonal sign conjugation
makes all three positive. All are strictly below one.

Solving the quadratic in B gives

B=AC/[1 +/- sqrt((1-A^2)(1-C^2))].                           (2)

Put A=sech alpha,C=sech gamma with alpha,gamma>0. Formula (2) gives
B=sech(alpha+gamma) or sech(alpha-gamma); the second branch with alpha=gamma
is excluded because B=1. Hence there are pairwise distinct real t_i with
Rij=sech(t_i-t_j). Setting z_i=exp(2t_i)>0 and absorbing the diagonal scales
gives the complete, not necessarily unique, parameterization

Lij=w_i w_j/(z_i+z_j),  w_i>0, z_i>0 pairwise distinct,      (3)

up to diagonal sign conjugation. Conversely (3) is positive definite:
1/(z_i+z_j) is the Gram matrix of the linearly independent functions
exp(-z_i s) on (0,infinity). The normalized Cauchy determinant is
det R=product_(i<j)((z_i-z_j)/(z_i+z_j))^2, and each factor equals
1-Rij^2, proving (1). Thus it gives strict connected Lambda-zero
K=L(I+L)^(-1). Connectedness follows also because L has every edge nonzero.
No uniqueness or classification of K's individual zero entries is asserted.

External fields preserve this submanifold exactly:
L_h=diag(exp(h_i/2)) L diag(exp(h_i/2)). Their atom log density differs by
sum_i h_i 1_{i in S} and a normalizer, so Lambda is unchanged.

## 2. Fisher inverse in the weighted-trace direction is explicit

Use coordinates (11,22,33,12,13,23), with offdiagonal basis entries BOTH one.
Let F=sum_S j_S j_S^T/p_S. On a connected three-vertex kernel F>0: vanishing
all atom derivatives forces all Dii=0 via singleton marginals, then
Kij Dij=0 via pair inclusions. A missing edge of a connected three-vertex
graph is completed by a two-edge path, and the full determinant derivative
then forces its Dij=0 as well.

At Lambda=0 write N=diag(n1,n2,n3)=-diag(ell23,ell13,ell12)>0,
delta=n1 n2 n3, f_i=1/n_i. Strictness of N follows from the reviewed
conditional-square identities, not from continuity: ell_ij=0 and Lambda=0
would force Kij=0 and Kik Kjk=0, contradicting connectedness.

For a real vector h, differentiating the external-field curve gives

D_h=(diag(h)K+K diag(h))/2-K diag(h)K.                       (4)

Its event score is h dot (1_S-diag K). Differentiating expectations in any
direction E, with h and the base point held fixed, proves

F(D_h,E)=sum_i h_i Eii.                                    (5)

Let C be the observation covariance, Cii=Kii(1-Kii), Cij=-Kij^2.
It is positive definite since the eight events have full support.
Equation (5) and F>0 imply the EXACT inverse identity

F^(-1) eta=D_f,  eta(E)=sum_i f_i Eii,
V:=eta^T F^(-1)eta=f^T C f.                                (6)

This is an identity, not merely a Cauchy upper bound on Fisher capacity.

## 3. Retaining offdiagonal conditional scores gives a three-by-three gate

Split coordinates into x=(11,22,33), z=(12,13,23). Define the 3 by 3 matrix

U_(ij),l=(delta_il+delta_jl)Kij/2-Kil Klj.

The coordinate vector of D_h is (Ch,Uh), so (5) says F[C;U]=[I;0].
Writing R=Fzz>0, block algebra gives

Fxz=-C^(-1)U^T R,
Fxx=C^(-1)+C^(-1)U^T R U C^(-1).                           (7)

Let J have zero diagonal and Jij=n_k for the complementary k, and let
Z=2 diag(n3,n2,n1)>0. The reviewed exact entropy identity gives

Bxx=Fxx-J, Bxz=Fxz, Bzz=R+Z.

The offdiagonal factors in Z are essential for the chosen coordinates.
Eliminating Bzz proves B>0 iff

S=C^(-1)-J+C^(-1)U^T W U C^(-1)>0,
W=R-R(R+Z)^(-1)R=(R^(-1)+Z^(-1))^(-1)>0.                  (8)

Equivalently the explicit three-by-three matrix

T=C-CJC+U^T W U                                           (9)

must be positive definite. This is an equivalence, NOT a global proof.
Dropping U^T W U gives only a sufficient condition and loses a necessary
stabilizing contribution near some strict boundaries.

For a scalar gate, put A_x=diag(delta/n_i^2) and
I_eff=C^(-1)+C^(-1)U^T W U C^(-1). Eliminating the same offdiagonal block in
the U8 positive matrix A yields exactly

rho=delta f^T (I_eff+A_x)^(-1) f.                           (10)

Thus the minimum remaining statement is (10)<1 for every weighted Cauchy
parameter (3). The displayed matrices use only eight atom gradients and
three positive conditional-odds logarithms. No field-score positivity alone
has been shown to imply it.

## 4. A tempting Fisher-only shortcut fails even on this submanifold

On the reviewed centered path K(1/2,a), set r=8a^2 in (0,1),
n=log((1+r)/(1-r)), m=-log(1-r^2). Here N=diag(n,m,n), Lambda=0.
Equation (6) gives exactly

delta V=m/2+n^2/(4m)-rn/2.

With h=log(1+r), n=m+2h, this is

delta V=m(3/4-r/2)+h(1-r)+h^2/m ~ m/4 -> infinity.           (11)

In particular both Fisher-only tests delta V<=1 and the optimized
trace-capacity sufficient test (2/3)delta V<=1 eventually fail. Yet the
independently audited centered theorem proves full B>0 for every such r.
This is an analytic obstruction to those proof shortcuts, not an entropy
nonconcavity counterexample. It also shows why retaining W in (8) matters.

There is an explicit strict witness, without a floating logarithm test:
take r=1-2^(-16), a=sqrt(r/8). The exact expression (11) is >m/4, and
m>15 log 2>15/2 (use log 2=integral_1^2 dt/t>1/2). Therefore
delta V>15/8 and (2/3)delta V>5/4>1, while the centered theorem gives B>0.
This witness only refutes the sufficiency of those proxy bounds as universal
claims; it is not a counterexample to rho<1.

## 5. What is and is not settled

Equations (1)--(10) are structural identities/equivalences or their stated
parameterization candidate. Equation (11) refutes only proxy criteria.
The next document gives an explicit continuous Lambda-zero family with full
Hessian strictness near the old proxy blocker. Neither that family nor the
finite sanity points settles the whole connected Lambda-zero submanifold.
