# Near-upper-face compensation, including anisotropic approach

Status: PROVED auxiliary range; the global C2 conjecture remains unresolved.
Author: C2 mechanism child, 2026-09-09. Not yet independently reviewed.
No claim of novelty. No numerical premise is used in the proof.

## 1. Objects, quantifiers and result

Let U be a fixed real n by 3 matrix with U^T U=I, n>=4, and every
three rows independent. Write r_i for the transpose of row i,
w_ij=r_i cross r_j, and q_S=det(U_S)^2 for |S|=3. Define

    ell_i=||r_i||^2, z_ij=||w_ij||^2,
    L=max({-log ell_i}_i union {-log z_ij}_ij union {-log q_S}_S).

These are finite nonnegative numbers. All three geometric weights are at
most one. Define the positive frame constant

    kappa=min_{V=V^T, ||V||_F=1} sum_{i<j}(w_ij^T V w_ij)^2/z_ij.

The proof below establishes kappa>0 under the stated hypotheses.
For every 0<delta<=1/8, every symmetric R with rho I<=R<=I where
0<rho<=1, every symmetric V, set A=I-delta R and K(t)=U(A+tV)U^T.
The complete Shannon entropy obeys

    H''(0) <= [-kappa/(4 delta)+16 L+18 log(1/rho)+4] ||V||_F^2. (1)

Consequently it is strictly negative for every nonzero V whenever

    delta [16 L+18 log(1/rho)+4] < kappa/4.                 (2)

The constants and quantifiers are uniform in R and V. In particular, for
ANY sequence delta_j ->0 and R_j with lambda_max(R_j)<=1 and
delta_j log(1/lambda_min(R_j))->0, (2) eventually holds simultaneously
for all directions V, including directions depending arbitrarily on j.
It also covers rho>=exp(-eta/delta) for any fixed eta<kappa/72 and all
sufficiently small delta, with threshold depending only on U and eta.

For the prompt's A=I-e B, use delta=e lambda_max(B) and
R=B/lambda_max(B). Thus B is permitted to depend on e. This is an
auxiliary theorem on the original fixed rank-three face, not an assertion
for every n-dimensional strict interior kernel.

## 2. Rebuilding all event probabilities

For 0<A<I, put C=I-A. The determinant generating identity follows from
Cauchy--Binet:

    E product_{i in X} z_i
      = det(I-A+ A^(1/2) U^T diag(z) U A^(1/2)).

For example, it follows by first expanding det(I+diag(z-1)UAU^T),
whose coefficient form is the DPP inclusion probability identity, and
then applying det(I+XY)=det(I+YX). Factoring det C and expanding the
remaining rank-three determinant gives

    p(S)=det C det((U A C^(-1) U^T)_S), |S|<=3,
    p(S)=0, |S|>3.

The matrices A and C commute because A=I-C; no commutation with V is
ever imposed. For a symmetric 3 by 3 matrix T,
det([r_i r_j]^T T [r_i r_j])=w_ij^T adj(T) w_ij. Hence

    p_0=det C,
    p_i=r_i^T(adj C-det C I)r_i,
    p_ij=w_ij^T[C+C^2-(tr C)C+det C I]w_ij,
    p_S=q_S det(I-C), |S|=3.                              (3)

The pair formula uses adj(I-C)=I+C-(tr C)I+adj C and
adj C=C^2-(tr C)C+e_2(C)I. These polynomial identities extend to
singular C, although the curvature theorem is applied only at positive C.

Exterior Cauchy--Binet and U^TU=I yield

    sum_i r_i r_i^T=I, sum_ij w_ij w_ij^T=I, sum_S q_S=1.

The probability generating function for cardinality is det(C+zA).
In particular E|X|=tr A and E(3-|X|)=tr C.

## 3. Exact cancellation of every log(delta) acceleration term

At C=delta R, write p_S=delta^(3-|S|) g_S. These equalities only
rescale probabilities at the differentiation center: delta is HELD
FIXED when differentiating the affine path C(t)=delta R-tV. Do not
differentiate R or delta as functions of t. Because the support |S|<=3
is fixed and all its probabilities are positive,

    H''=-sum_S (p'_S)^2/p_S -sum_S p''_S log p_S.

Twice differentiating the affine identity E(3-|X|)=tr C gives
sum_S(3-|S|)p''_S=0. Therefore EXACTLY

    H''=-sum_S (p'_S)^2/p_S -sum_S p''_S log g_S.          (4)

This keeps, rather than neglects, all rare-event p'' log p terms.
No uncancelled log(delta) term is present. Derivatives of logarithms are
already included in the complete Fisher term.

In an eigenbasis of R, with eigenvalues b_1,b_2,b_3 in [rho,1], the
matrix defining g_i has eigenvalues b_j b_k(1-delta b_i), and the matrix
defining g_ij has eigenvalues b_i(1-delta b_j)(1-delta b_k). Thus

    rho^3 <=g_0<=1,
    rho^2(1-delta)ell_i <=g_i<=ell_i,
    rho(1-delta)^2 z_ij <=g_ij<=z_ij,
    (1-delta)^3q_S <=g_S<=q_S.                           (5)

All g's are in (0,1]. Put x=log(1/rho) and y=-log(1-delta). Equation
(5) bounds -log g by 3x, L+2x+y, L+x+2y, and L+3y on the four layers.

## 4. Explicit bound on the logarithmic acceleration

For symmetric T,V in dimension three,

    |D^2 det(T)[V,V]| <=2 ||T||_op ||V||_F^2.             (6)

To prove it, orthogonally diagonalize V with eigenvalues v_i. The second
derivative is 2(T_11 v_2v_3+T_22 v_1v_3+T_33 v_1v_2), whose absolute
value is at most 2||T||_op sum_{i<j}|v_i v_j|. The last sum is at most
sum_i v_i^2 by 2|ab|<=a^2+b^2.
Also ||adj V||_op<=||V||_F^2/2 and |e_2(V)|<=||V||_F^2.
The latter follows from e_2=((tr V)^2-tr V^2)/2, or its eigenvalues.

Twice differentiating (3), with C'=-V, yields the bounds

    |p_0''| <=2 delta ||V||_F^2,
    |p_i''| <=(1+2delta) ell_i ||V||_F^2,
    |p_ij''| <=(3+2delta) z_ij ||V||_F^2,
    |p_S''| <=2q_S ||V||_F^2, |S|=3.                    (7)

For clarity the exact singleton and pair accelerations are

    p_i''=2 r_i^T adj V r_i-delta D^2det(R)[V,V]ell_i,
    p_ij''=2 w_ij^T(V^2-(tr V)V)w_ij
                +delta D^2det(R)[V,V]z_ij.

The pair bound uses V^2-(tr V)V=adj V-e_2(V)I. For the top layer,
||A||_op<=1. Summing (7) times the logarithmic bounds, and using
sum ell_i=sum z_ij=3 and sum q_S=1, proves

    |sum p_S'' log g_S|
      <=[(14+12delta)L+(15+24delta)x+(27+18delta)y]||V||_F^2
      <=[16L+18x+4]||V||_F^2.                           (8)

Indeed delta<=1/8, y<=log(8/7)<0.134 and
(27+18/8)log(8/7)<4. Every layer, including the empty event, is present.

## 5. Uniform pair Fisher lower bound, independently reconstructed

Let Q(C)=C+C^2-(tr C)C+det C I and let Z be the derivative of Q(C(t)).
At C=delta R,

    Z=-V+delta[(tr V)R+(tr R)V-RV-VR]
                      -delta^2 Ddet(R)[V] I.            (9)

We claim ||Z+V||_F<=4delta||V||_F for delta<=1. Diagonalize R. On the
off-diagonal entry V_ij the operator (Z+V)/delta multiplies by b_k,
which is at most one. On diagonal entries its 3 by 3 matrix has row i
diagonal coefficient b_j+b_k-delta b_jb_k and off-diagonal coefficient
in column j equal to b_i(1-delta b_k). All these coefficients are
nonnegative. Each row sum is at most 4. The column i sum is
2(b_j+b_k)-3delta b_jb_k<=4. Its Euclidean operator norm is at most
sqrt(||M||_1||M||_infinity)<=4. The Frobenius norm separates the
diagonal and off-diagonal subspaces, proving the claim.

For delta<=1/8 it follows that ||Z||_F>=||V||_F/2. Since p_ij<=delta
z_ij by (5), and p_ij'=w_ij^TZw_ij,

    F_pair=sum_ij (p_ij')^2/p_ij
          >= kappa||Z||_F^2/delta
          >= kappa||V||_F^2/(4delta).                   (10)

For completeness, kappa>0 is not assumed. If all w_ij^TVw_ij=0,
use the independent r_1,r_2,r_3 as a coordinate basis. Under an
invertible change r_i=S e_i, cross products transform as
Sx cross Sy=det(S) S^(-T)(x cross y); the symmetric quadratic form
therefore changes by invertible congruence. The measurements for
(1,2),(1,3),(2,3) force its three diagonal entries to zero.
Write r_4=S(a,b,c)^T. Every triple of the first four rows is independent,
so abc!=0. The measurements for (1,4),(2,4),(3,4), with normals
(0,-c,b),(c,0,-a),(-b,a,0), respectively force each off-diagonal entry
to zero. Thus V=0. Compactness of the Frobenius unit sphere now makes
the displayed minimum defining kappa strictly positive.

Combining (4), (8), (10), and nonnegativity of the other Fisher terms
proves (1) and all the uniform corollaries in Section 1.

## 6. Full fixed-B asymptotic, with the constant term

Here B>0 is FIXED and e->0. Direction V is arbitrary, without a
commutation assumption. Put s=tr B and define, for each pair,

    b=w^TBw,
    c=w^T(B^2-sB)w,
    f=w^TVw,
    g=w^T[(tr V)B+sV-BV-VB]w,
    h=2w^T[V^2-(tr V)V]w.

For each singleton define a=r^T adj B r, l=r^T Dadj(B)[V]r,
k=2r^T adj V r. Let c_U=-sum q_S log q_S and
v=tr V, k_det=v^2-tr(V^2). The complete curvature has expansion

    H''=-J_B(V)/e+C_B(V)+O(e)||V||_F^2,                 (11)
    J_B(V)=sum_pairs f^2/b,
    C_B(V)=sum_pairs[2fg/b+f^2 c/b^2-h log b]
           -sum_singletons[l^2/a+k log a]-v^2+c_U k_det.

The notation O(e)||V||_F^2 means: for every fixed U and fixed positive
B there are e_0>0 and finite C such that the remainder absolute value
is at most C e ||V||_F^2 for all 0<e<e_0 and all symmetric V. It is
also uniform for B in any compact subset of positive definite matrices.
It does NOT assert uniformity as lambda_min B tends to zero.

To check (11) explicitly, pair probabilities and first derivatives are
p=e b+e^2 c+O(e^3) and p'=-f+e g+O(e^2), so their Fisher contribution
is f^2/(eb)-2fg/b-f^2c/b^2+O(e). Singleton probabilities and derivatives
are e^2a+O(e^3) and -el+O(e^2), contributing l^2/a+O(e). Empty-event
Fisher is O(e). Top-layer Fisher is v^2+O(e). In (4), the limiting
scaled probabilities on pair, singleton, and top layers are b,a,q_S;
the corresponding accelerations are h,k,q_S k_det. Empty acceleration
is O(e). Substitution gives exactly (11). All rescaled probabilities
stay uniformly separated from zero on compact positive-B sets; their
logarithms and rational Fisher remainders are real analytic in e near
zero. This proves the stated remainder and shows why no O(log e) or
e log e term is left in the TOTAL curvature.

The separately recorded layer terms do contain log e terms. At e=0,
sum_pairs h=-2k_det and sum_singletons k=k_det; their logarithmic
contributions -sum_pairs h log e-2sum_singletons k log e cancel.
Equation (4) is the all-orders exact version of this cancellation.

## 7. Affine-path legality and remaining escape scale

For V!=0, a symmetric half-step h is valid at A and C exactly when

    h ||A^(-1/2) V A^(-1/2)||_op <1,
    h ||C^(-1/2) V C^(-1/2)||_op <1.                   (12)

These equivalences follow by congruencing A+-hV>0 and C+-hV>0.
A convenient sufficient condition is
h||V||_op<min(1-delta,delta rho). Thus every V has a nonempty valid
affine interval, but extremely anisotropic R may force its width to be
exponentially small. Rescaling V cannot evade (1), because every term
in that inequality is homogeneous of degree two in V.

This proof does not settle sequences with delta log(1/rho) bounded
below by kappa/72 or diverging. The exact unclosed comparison is

    -sum_S p_S'' log g_S <= sum_S(p_S')^2/p_S

on that residual regime (or at moderate delta). In particular, the
absolute-value bound (8) can discard favorable cancellation among
events whose g's vanish together. No positive example is claimed in
that remaining regime. Finite computations do not close it.

## 8. Provenance and checks

The probability formulas, exact logarithm cancellation, fixed-B constant
term, and anisotropic bounds above were derived independently in this
child unit. The parent communicated its pair-Fisher bound while the
unit was in progress; Section 5 supplies a complete reconstruction of
that bound instead of treating the communication as an external theorem.
The accompanying one-fixture check was actually run remotely with all
BLAS/OpenMP thread counts set to one. It is algebra/implementation
calibration only. Independent mathematical review: pending.
