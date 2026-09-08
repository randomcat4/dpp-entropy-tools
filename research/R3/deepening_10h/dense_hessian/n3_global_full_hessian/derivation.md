# A global rank-one-defect representation of the n=3 entropy Hessian

AUTHOR STATUS: STRUCTURAL_THEOREM_CANDIDATE_PENDING_INDEPENDENT_REVIEW.

The full-domain inequalities G1/G2 remain unproved. The results below are proposed exact structural theorems, not deductions from the finite scout.

## 1. Eight exact atoms and four logarithmic coefficients

Write

K=[[x,a,b],[a,y,c],[b,c,z]],
q12=xy-a^2, q13=xz-b^2, q23=yz-c^2,
r=xyz+2abc-xc^2-yb^2-za^2.

The eight exact event probabilities are

p123=r;
p12=q12-r, p13=q13-r, p23=q23-r;
p1=x-q12-q13+r, p2=y-q12-q23+r, p3=z-q13-q23+r;
p0=1-x-y-z+q12+q13+q23-r.

These are exactly Mobius inversion of the inclusion minors. On 0<K<I all eight atoms are strictly positive: for example the signed determinant identity is equivalent to the strictly positive L-ensemble atom formula with L=K(I-K)^(-1)>0, which follows by determinant factorization. All logarithms below are consequently defined.

For a symmetric direction D define its event Fisher quadratic form

F_K(D,E)=sum_S dp_S[D] dp_S[E]/p_S.

Let

l12=log(p0*p12/(p1*p2)), l13=log(p0*p13/(p1*p3)),
l23=log(p0*p23/(p2*p3)),
Lambda=log(p123*p1*p2*p3/(p0*p12*p13*p23)).

Since the singleton inclusion probabilities are linear, grouping the exact-event Hessian acceleration by q12,q13,q23,r gives

B_K(D,D)=F_K(D,D)+2 sum_{i<j} l_ij det(D_{ij})
                         +2 Lambda tr(K adj D),                 (1)

where B=-Hess H. The factor two in the last term comes from
det(K+tD)=det K+t tr(adj K D)+t^2 tr(K adj D)+t^3 det D.

This is a full Sym(3) identity, not a fixed-eigenvector or PSD-direction identity.

## 2. Conditional odds imply a positive cofactor matrix

For {i,j,k}={1,2,3}, put a=K_ij and b=K_ik*K_jk. Direct expansion of the eight atoms yields

p0*pij-pi*pj = -[(1-Kkk)*a+b]^2,
pk*p123-pik*pjk = -[Kkk*a-b]^2.                                (2)

Equivalently these are the negative covariances conditioned respectively on k being absent or present, with their conditioning masses restored. In particular

l_ij<=0,  l_ij+Lambda<=0.                                     (3)

Define the symmetric matrix

N=-diag(l23,l13,l12)-Lambda K.                                 (4)

If Lambda>0, then -l_ij>=Lambda for each pair, so

N>=Lambda(I-K)>0.

If Lambda<0, then -l_ij>=0, so

N>=(-Lambda)K>0.

The Lambda=0 case must not be inferred by continuity alone. Then N is the diagonal matrix -diag(l23,l13,l12). If l_ij=0, (3) and Lambda=0 imply that BOTH squared expressions in (2) vanish. Adding their unsquared zero equations gives a=0, and then b=0. Thus l_ij=0 occurs exactly when K_ij=0 and K_ik*K_jk=0. In a connected three-vertex support graph, every pair has either its own nonzero edge or a two-edge path. Therefore this simultaneous vanishing is impossible for every pair: all three l_ij<0 and N is strictly positive definite.

Hence N is positive semidefinite for every strict kernel, and positive definite whenever its observation support is connected. A disconnected strict kernel has a factored exact law, Lambda=0 and at least one zero diagonal entry in N, consistently with its flat cross-block Hessian directions.

This proves the claimed strictness at Lambda=0 for arbitrary parameters, including paths and equal diagonal entries; no finite test is used.

## 3. One negative rank-one update, with an explicit scalar threshold

Equation (1) becomes

B_K(D,D)=F_K(D,D)-2 tr(N adj D).                              (5)

Assume henceforth that K is connected, so N>0. Set E=N^(-1/2)D N^(-1/2). The adjugate congruence identity gives

tr(N adj D)=det(N) tr(adj E)
           =det(N)/2 * ((tr E)^2-tr(E^2)).

Consequently

B_K(D,D)=F_K(D,D)+det(N)||E||_F^2-det(N)(tr E)^2.              (6)

For an entirely explicit coordinate formula, let E_i, i=1,...,6 be the observation basis (E11,E22,E33,E12+E21,E13+E31,E23+E32), and define

eta_i=tr(N^(-1)E_i),
A_ij=F_K(E_i,E_j)+det(N) tr(N^(-1)E_i N^(-1)E_j).

In particular the off-diagonal coordinate entries of eta are TWO times the corresponding entries of N^(-1); they are not the uncorrected Frobenius-gradient entries. A is positive definite, since its second summand is a positive definite quadratic form and its Fisher summand is nonnegative. The exact matrix identity and scalar are

B=A-det(N) eta eta^T,
rho(K)=det(N) eta^T A^(-1) eta.                               (7)

This formula uses only the eight atoms, their first derivatives, the four logs, a 3x3 inverse and a 6x6 positive-definite solve. No square-root choice is needed to evaluate it.

Congruencing by A^(-1/2) makes the update I-vv^T, where ||v||^2=rho. Thus

- rho<1 iff B>0;
- rho=1 iff B has five positive eigenvalues and one zero eigenvalue;
- rho>1 iff B has five positive eigenvalues and one negative eigenvalue.

The remaining global connected-kernel problem is EXACTLY the scalar inequality rho(K)<=1, and strict positivity is exactly rho(K)<1. Since connected strict kernels are dense in the strict domain and H is smooth there, proving the non-strict bound on all connected kernels would also extend B>=0 to disconnected kernels by continuity. The inverse-N formula itself is not used at disconnected points. This is a reduction, not its solution.

If rho>1, a concrete violating direction in observation coordinates is d=A^(-1)eta, because

d^T B d=(eta^T A^(-1)eta)*(1-rho)<0.

This furnishes a deterministic direction to freeze and certify if a scalar search crosses one.

## 4. Global five-dimensional strict subspace and coordinate strictness

The hyperplane

T_K={D in Sym(3): tr(N^(-1)D)=0}

has dimension five. For every nonzero D in it, equation (6) gives

B_K(D,D)>=det(N)||N^(-1/2)D N^(-1/2)||_F^2
         >=det(N)/lambda_max(N)^2 * ||D||_F^2>0.                (8)

Therefore H''<0 on this entire five-dimensional direction subspace at EVERY connected strict K. The full Hessian has at most one nonnegative eigenvalue; equivalently B has at most one nonpositive eigenvalue. The scalar alternatives in section 3 make this statement precise, including nullity.

For each diagonal rank-one coordinate, p_S''=0 for all events, so B(Eii,Eii)=F(Eii,Eii)>0: the singleton marginal derivative is one, preventing a zero Fisher form.

For e={i,j} with complementary vertex k, equation (5) gives

B(Eij+Eji,Eij+Eji)=F(Eij+Eji,Eij+Eji)+2Nkk.                  (9)

At a connected strict kernel this is strictly positive. Thus every individual observation coordinate is globally strictly concave there. This does NOT prove joint concavity; the possible rank-one negative update can still involve a combination of coordinates.

## 5. Complement invariance

The complement kernel I-K has atoms p'_S=p_{S^c}. Hence its triple log coefficient is -Lambda and its absent-conditioned pair log is l_ij+Lambda. Substitution in (4) gives exactly N(I-K)=N(K). Event derivatives change sign and are permuted, so their Fisher forms agree. Thus A, B and rho are complement invariant in the common observation coordinates. This is useful for transferring the specifically proved boundary subclass below, not a claim that arbitrary realification or other transformations preserve entropy gaps.

## 6. Precise remaining obstruction

The inequalities (3) completely prove N>=0, but they do not control the remaining Fisher-versus-trace scalar in (7). Positivity of N and Fisher, or positivity of every coordinate diagonal, is insufficient by itself.

An exact algebraic nonimplication illustrates this: set N=I and let an artificial Fisher form be ||D||_F^2. Then A=2I as an operator on Frobenius Sym(3), rho=3/2 and

B(D,D)=2||D||_F^2-(tr D)^2.

All observation-coordinate diagonal curvatures B(E_i,E_i) are positive, but B(I,I)=-3. This is NOT claimed to be a DPP-realizable (N,Fisher) pair. It only disproves the inference that the established structural inequalities alone settle the remaining scalar bound.

Moreover the boundary theorem candidate in boundary_asymptotic.md gives rho tending to one from below on a connected family. Thus a universal bound rho<=c<1 cannot hold, even if the global rho<=1 conjecture is true. A successful general proof must exploit the exact DPP coupling between N and its Fisher form, without relying on a uniform separation from one.

Review priorities: the Mobius log coefficients and factors of two in (1); the Lambda=0 connected strictness in section 2; the off-diagonal coordinate convention in eta/A; the adjugate congruence identity; and the fact that (7) is an equivalence, not a proof of rho<=1.
