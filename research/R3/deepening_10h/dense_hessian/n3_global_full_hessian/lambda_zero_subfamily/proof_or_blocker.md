# Explicit strict neighborhood at the proxy blocker

AUTHOR PROOF CANDIDATE, pending independent review. Global Lambda-zero sign
remains INCOMPLETE. The result below controls ALL Sym(3) directions.

## 1. A quantitative bound at Kstar

Let Kstar=[[1/2,3/10,0],[3/10,1/2,3/10],[0,3/10,1/2]].
Its smallest event is q=7/200 and its spectral boundary distance is
1/2-3sqrt(2)/10>1/20, using sqrt(2)<3/2. Its L matrix is

Lstar=(1/7)[[25,30,18],[30,43,30],[18,30,25]].

It has Lambda=0 exactly. It is the earlier Fisher/coarse proxy blocker,
not a positive entropy-curvature example.

We extract the quantitative bound Bstar(D)>=(1/3)||D||_F^2 from the reviewed
centered-path proof. In its notation r=18/25, u=r^2, l=1-u, v=2-u.
The odd block has B>=min(n,m)||D||_F^2, and the h-only block has B>=n||D||_F^2.
Here n=log((1+r)/(1-r))>2r, m=-log(1-u)>u>1/3.

The remaining three-coordinate core is B=(2/l)C_core. The reviewed Schur
identity gives det C_core=l^2 Num with Num>4m+12u>12u.
Moreover tr C_core=6-u-2u^2<=6-u. For a positive three-by-three matrix,
lambda_min>=4 det/(tr)^2, because the product of its other two eigenvalues
is at most (tr/2)^2. For repeated coordinates (d,e,k),
||D||_F^2=2d^2+e^2+2k^2<=2||(d,e,k)||_2^2. Therefore

B_core(D)>[48(1-u)u/(6-u)^2] ||D||_F^2 > (1/3)||D||_F^2.     (12)

The final comparison is exact rational arithmetic at u=324/625. The symmetry
blocks are Frobenius orthogonal, so this proves the full bound claimed.

## 2. Explicit Hessian continuity constant

For a strict three-by-three kernel, each exact atom has the signed mixed
determinant representation p_S=(-1)^{|S^c|}det(K-I_{S^c}). This also follows
from the exact inclusion expansion. The symmetric matrix M=K-I_{S^c}
lies strictly between -I and I, so every column norm is at most one.
Column multilinearity and Hadamard's inequality imply for arbitrary
symmetric directions E,D

|dp[E]|<=3||E||_F,
|d^2p[E,D]|<=6||E||_F||D||_F,
|d^3p[E,D,D]|<=6||E||_F||D||_F^2.                           (13)

These deliberately loose constants count ordered distinct column choices.
If all atoms are >=m0=7/400, differentiating H=-sum p log p three times and
using sum p'''=0 gives

H'''[E,D,D]=sum_S {p'_E(p'_D)^2/p^2
 -(p''_DD p'_E+2p''_ED p'_D)/p-log(p)p'''_EDD}.

Thus its absolute value is bounded by L_H||E||_F||D||_F^2, where the rational
choice

L_H=8[27/m0^2+54/m0+30]=35781360/49                       (14)

is valid. Indeed |log p|<=log(400/7)<5, since the first five terms of e^5
already exceed 400/7. No floating-point logarithm certificate is needed.

Choose the explicit Frobenius radius

epsilon=min(1/40,q/6,1/(6L_H))=49/214688160.                (15)

For ||K-Kstar||_F<=epsilon, the whole connecting segment is strictly feasible
with spectral margin >=1/40. By (13), atoms along it are >=q-3epsilon>=q/2.
Integrating (14) along that segment changes B(D,D) by at most
L_H epsilon ||D||_F^2=(1/6)||D||_F^2. Consequently

B_K(D,D)>=(1/6)||D||_F^2 for every D in Sym(3).              (16)

The radius is about 2.2824e-7: it is extremely conservative. This ball result
does not restrict D to PSD, commuting, or tangent directions.

## 3. An explicit continuous family lying in Lambda zero

For arbitrary real h with max_i|h_i|<=epsilon/2, put
L_h=diag(e^{h_i/2})Lstar diag(e^{h_i/2}), K_h=L_h(I+L_h)^(-1).
Strictness and Lambda=0 are automatic. Along the path sh, equation (4) gives

||dK_sh/ds||_F<=||diag h||_F<=sqrt(3)||h||_infinity
                                      <2||h||_infinity.

Here each product is bounded using ||K||op,||I-K||op<1; the two half terms
sum to the displayed bound. Hence ||K_h-Kstar||_F<=epsilon and (16) holds.
Connectedness follows because L_h has all offdiagonal entries nonzero.
This is a genuine three-parameter continuous Lambda-zero family, not just
the old centered path: at h=0 the derivative of K13 in the h2 direction is
-K12 K23=-9/100, so nearby dense K occur.

More generally the intersection of the ball (15) with the complete Cauchy
parameterization is a relatively open neighborhood in the Lambda-zero
submanifold. The displayed closed external-field box is an explicit subset.

## 4. Remaining blocker and review priorities

Outside this neighborhood, the exact unresolved test is derivation (9)>0,
or equivalently (10)<1. Its U^T W U term cannot currently be bounded sharply
enough in terms of the Cauchy parameters to settle the entire submanifold.
The field inverse identity alone cannot close it: the centered boundary
asymptotic (11) makes the Fisher-only capacity unbounded while B stays strict.

Audit priorities: Cauchy classification branches; symmetry-block norm
conversion and the trace upper bound in (12); all ordered-column factors
in (13); the entropy third derivative signs; block-inverse identity (8).
Numerical checks below are SCOUT/sanity only, not the proof of (16).
