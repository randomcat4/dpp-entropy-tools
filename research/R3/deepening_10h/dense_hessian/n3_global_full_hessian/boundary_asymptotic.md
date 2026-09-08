# Dense rank-one boundary subclass and the Schur scalar near one

AUTHOR STATUS: BOUNDARY_SUBCLASS_PROOF_CANDIDATE_PENDING_REVIEW.

This is an analytic candidate for a specific continuous boundary family, not the global n=3 theorem. Fix theta in (0,1) and a real unit vector u with ALL three coordinates nonzero. Set P=uu^T and

K_epsilon=epsilon I+(theta-epsilon)P,
0<epsilon<min(theta,1/2).

Every such sufficiently small kernel is strict and has complete observation support. The proposed asymptotic is, with L=log(1/epsilon),

rho(K_epsilon)=1-1/(theta L)+O(L^(-2)).                        (1)

Constants may depend on the fixed theta,u. Thus rho<1 and the full Hessian is negative definite for all sufficiently small positive epsilon. The complement family I-K_epsilon obeys the same result. No uniformity as theta approaches 0 or 1, or as any u_i approaches zero, is claimed. Unequal vanishing eigenvalue rates are not covered by this proof.

## 1. Event orders and the stiff Fisher operator

The full event is p123=theta epsilon^2, the empty event is (1-theta)(1-epsilon)^2, and

pij=epsilon theta(ui^2+uj^2)
       +epsilon^2(1-ui^2-uj^2-theta).

Singleton events tend to theta ui^2>0. Thus three pair atoms vanish linearly, the full atom quadratically, and the other four atoms stay positive. The complete event formulas follow from the exact principal minors and Mobius inversion, not a spectral count-entropy replacement.

Let F_epsilon denote the full event Fisher bilinear form. Its rational event formulas give the operator expansion

F_epsilon=epsilon^(-1)F_minus1+F0+O(epsilon),                  (2)

where

F_minus1(D,D)=theta sum_{i<j}
   (ui^2 Djj+uj^2 Dii-2ui uj Dij)^2/(ui^2+uj^2).

There is no stronger pole from the full event: adj K=theta epsilon(I-P)+epsilon^2 P, so (dp123)^2/p123 is bounded. The other four probabilities are nonzero at the limit.

The kernel of F_minus1 is exactly

T={u v^T+v u^T: v in R^3}.                                  (3)

Indeed, since all ui are nonzero, setting all three numerators to zero determines Dij=(ui/uj Djj+uj/ui Dii)/2, which is exactly (3). Thus F_minus1 is positive definite on the three-dimensional Frobenius orthogonal complement of T.

Restricted to T, the finite Fisher limit comes only from the empty and singleton events:

F0(D,D)=(tr D)^2/(1-theta)+sum_i Dii^2/(theta ui^2).

In particular F_epsilon(P,P)=1/[theta(1-theta)]+O(epsilon).   (4)

## 2. The logarithmic cofactor matrix

From the event orders,

l_ij=-L+O(1), Lambda=L+O(1).

More precisely the nonzero leading coefficients of the atoms imply full expansions of their logarithms, so

N_epsilon=L N0+N1+O(epsilon L),
N0=I-theta P>0.                                             (5)

Consequently det N=L^3(1-theta)(1+O(1/L)), and

u^T N^(-1)u=1/[L(1-theta)]+O(L^(-2)).                       (6)

These statements are matrix/operator asymptotics for fixed theta,u, not numerical eigenvalue fits.

## 3. Direct full-Hessian endpoint proof

Write a general tangent element D in T as alpha P+u v^T+v u^T with v perpendicular to u. In an orthonormal basis starting with u, its matrix is [[alpha,v^T],[v,0]]. Its adjugate has support only in the lower 2x2 block and is independent of alpha. Therefore the cofactor term -2tr(N adj D) has no radial P/tangent-mixing cross term, exactly, and by (5) its mixing quadratic term is 2L||v||^2+O(||v||^2).

Use a fixed decomposition Sym(3)=span(P) plus the two u-mixing coordinates plus T-perpendicular. Congruence-scale these three pieces by 1, L^(-1/2), and sqrt(epsilon), respectively. Equations (2)-(5) give the limiting B quadratic form

1/[theta(1-theta)] on the radial P coordinate;
2||v||^2 on the two mixing coordinates;
F_minus1 on the three normal coordinates.

All are strictly positive. Radial/mixing cross terms come only from bounded Fisher terms and vanish after L^(-1/2). Normal/tangent Fisher leading poles vanish because T is their exact kernel; the remaining cross terms are bounded. Cofactor cross terms are at most O(L), becoming O(sqrt(epsilon)L) or O(sqrt(epsilon L)), both tending to zero. Normal cofactor terms become O(epsilon L). Thus the whole scaled matrix tends in operator norm to a positive definite block diagonal matrix. The scaling is invertible for positive epsilon, proving full-Hessian negativity on a sufficiently small interval of this family.

This direct proof does not require the sharper scalar expansion (1), providing a separate route to the boundary subclass claim.

## 4. First nonzero deficit of the rank-one Schur scalar

For the sharper coefficient, move to E=N^(-1/2)D N^(-1/2) and divide its positive operator A by det N. Let

Ftilde(E,E)=F_epsilon(N^(1/2)E N^(1/2),N^(1/2)E N^(1/2))/det N.

Then rho=<I,(I+Ftilde)^(-1)I> in Frobenius Sym(3). Define v_epsilon=N^(-1/2)u and let T_epsilon be the three-dimensional tangent space {v_epsilon h^T+h v_epsilon^T}. This is precisely the pullback of the fixed kernel T in (3).

In the orthogonal splitting T_epsilon plus its complement, (2), (5) give

Ftilde_TT=O(1/L), Ftilde_TN=O(1/L),
Ftilde_NN=(epsilon L)^(-1)(C0+O(1/L))+O(1/L),

where C0 is positive definite (after identifying the smoothly converging normal spaces). The pole has EXACT zero mixed/tangent blocks because its kernel is T; this prevents an uncontrolled epsilon^(-1) cross term. Thus the inverse normal block of I+Ftilde is O(epsilon L). Its Schur correction to the tangent block is O(epsilon/L), and standard finite-dimensional inverse expansion gives

rho=||Proj_T I||_F^2
      -<Proj_T I,Ftilde_TT Proj_T I>
      +O(L^(-2))+O(epsilon L).                                (7)

The orthogonal projection of I onto T_epsilon is the rank-one projector

P_epsilon=v_epsilon v_epsilon^T/||v_epsilon||^2,

so its squared Frobenius norm is exactly one. Its corresponding D is

D_epsilon=N^(1/2)P_epsilon N^(1/2)
          =P/(u^T N^(-1)u).

Using (4)-(6),

F_epsilon(D_epsilon,D_epsilon)/det N
   =1/(theta L)+O(L^(-2)).                                   (8)

Substitution into (7), with epsilon L=o(L^(-2)), proves (1). The leading deficit is strictly positive. In particular this boundary family approaches the threshold from BELOW, but arbitrarily closely. No universal rho<=c<1 bound can hold on all connected strict kernels.

The most fragile asymptotic step is the moving tangent/normal Schur estimate in section 4. The direct block-scaling proof in section 3 independently establishes the eventual full-Hessian sign even if a reviewer requires a more formal treatment of the first correction coefficient.

## 5. Finite checks and exclusions

The bounded script checks theta=1/10,1/2,9/10 with u=(1,2,2)/3 and epsilon=10^(-k), k=2,4,8,16,32,64. At theta=1/2 and epsilon=10^(-64), (1-rho)L is approximately 1.99884400141, consistent with the limit 2. At theta=9/10 it is approximately 1.11294735246, consistent with 10/9. These checks are SCOUT, not the proof of the asymptotic.

Twelve additional unequal-rate boundary probes use eigenvalues (epsilon^r,epsilon^s,1/2), (r,s)=(1,2),(1,3),(2,3), at four epsilon values and one fixed rational orthogonal basis. They all remain below one, but the analytic theorem above does not cover those rates. No scope extension is inferred.
