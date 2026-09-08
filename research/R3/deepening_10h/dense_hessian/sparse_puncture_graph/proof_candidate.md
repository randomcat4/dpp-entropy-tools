# Sparse support: exact sixth jet and diameter-two sufficient theorem

STATUS: PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW.

## 1. Exact likelihood in orthogonal subset characters

At a strict diagonal X=diag(x), put

    a_S=product_{i in S} x_i product_{i not in S}(1-x_i),
    zeta_i(S)=1/x_i if i in S, and -1/(1-x_i) otherwise.

For a zero-diagonal symmetric observation perturbation Z=(z_ij), the signed
exact-event determinant is

    p_S(X+Z)=(-1)^|S^c| det(X+Z-I_{S^c}).

It follows by expanding the selected -1 diagonal entries and comparing with
inclusion Mobius inversion. Expanding this determinant instead in its diagonal
entries d_i=x_i if i in S, d_i=x_i-1 otherwise gives

    p_S(X+Z)/a_S = 1+R_S(Z),
    R_S(Z)=sum_{T subset[n], |T|>=2} det Z_T zeta_T(S),
    zeta_T=product_{i in T}zeta_i.                         (1)

Indeed det(diag d+Z)=sum_T det Z_T product_{i not in T}d_i;
det Z_empty=1 and singleton terms vanish because Z has zero diagonal.
This proves (1) from exact-event semantics, not an assumption about atom laws.

Under a_S, the zeta_i are independent and centered. Let

    w_i=E zeta_i^2 = 1/[x_i(1-x_i)],
    t_i=E zeta_i^3 = (1-2x_i)/[x_i^2(1-x_i)^2].

Distinct subset characters are orthogonal: E[zeta_T zeta_U]=0 for T!=U.
The diagonal marginals remain fixed along X+Z, so sum_S a_S R_S log a_S=0,
and E R=0. Therefore, locally at Z=0,

    F(x,z)-F(x,0)
      =-E[(1+R)log(1+R)]
      =-(1/2)E R^2+(1/6)E R^3-(1/12)E R^4+... .          (2)

These are analytic series near each strict diagonal point. They can be
differentiated in x and z on a smaller common neighborhood.

## 2. The complete fourth, fifth and sixth homogeneous terms

Write R_k=sum_{|T|=k} det Z_T zeta_T. In particular

    R_2=-sum_{i<j}z_ij^2 zeta_i zeta_j,
    R_3=2 sum_{i<j<k}z_ij z_ik z_jk zeta_i zeta_j zeta_k.

The degree-four term is -(1/2)E R_2^2, reproducing U2. The degree-five term
is -E R_2 R_3=0 by orthogonality of subsets of sizes two and three. This
vanishing holds for EVERY strict x; it does not require complement symmetry.

The degree-six term is

    -E R_2 R_4 -(1/2)E R_3^2 +(1/6)E R_2^3.

The first term is zero by subset orthogonality. The second is
-2 sum_{i<j<k} w_i w_j w_k z_ij^2 z_ik^2 z_jk^2. For the third, an ordered
triple of edges has nonzero character expectation only if no vertex has
degree one in its incidence multigraph. There are exactly two possibilities:
all three edges coincide, or the three distinct edges form a triangle.
The former gives -sum z_ij^6 t_i t_j before the factor 1/6. The latter has
six orderings and gives -6 times each triangle monomial with weight w_i w_j w_k.
Thus the full expansion is

    F(x,z)=h(x)
      -(1/2)sum_{i<j}w_i w_j z_ij^4
      -(1/6)sum_{i<j}t_i t_j z_ij^6
      -3 sum_{i<j<k}w_i w_j w_k z_ij^2 z_ik^2 z_jk^2
      +O(||z||^7).                                      (3)

This is a multivariate identity, not a statement about a single ray. The
remainder is analytic in x,z and has z degree at least seven, so its xx, xz,
zz derivatives are respectively O(z^7), O(z^6), O(z^5), locally uniformly in x.
The pure-edge sixth term can have either sign; no sign assumption on t_i t_j
will be made. It is higher order than the quartic term on supported edges.

## 3. Missing-edge curvature and the diameter-two theorem

Let E be the support edges of A and M the missing pairs. Set z=epsilon a,
with a_e=A_ij on E and a_m=0 on M. Use coordinates (x,z_E,z_M) for the full
observation Hessian, with each off-diagonal entry stored once. Let

    C=diag(w_i),
    B_E=6 diag_{ij in E}(w_i w_j A_ij^2),
    B_M=6 diag_{ij in M}
          (w_i w_j sum_{k:ik,jk in E} w_k A_ik^2 A_jk^2). (4)

If M is empty its block is simply omitted. Differentiating (3) yields

    F_xx = -C+O(epsilon^4),
    F_xE = O(epsilon^3),        F_xM=O(epsilon^6),
    F_EE = -epsilon^2 B_E+O(epsilon^4),
    F_EM = O(epsilon^5),
    F_MM = -epsilon^4 B_M+O(|epsilon|^5).                (5)

The absence of lower mixed terms matters. Every missing variable occurs to
an even power in the displayed quartic and sixth-degree polynomials, so its
first derivative vanishes at z_M=0. Two DIFFERENT missing-edge derivatives
also vanish there. The only nonzero leading second missing-edge derivative
is the diagonal derivative of a triangle whose other two edges are present,
giving exactly the common-neighbor sum (4). The xM and EM orders in (5) come
only from the degree-seven remainder or higher terms.

If G has diameter at most two and is connected, every missing pair has at
least one common neighbor. All w_i are positive and all supported A_ij are
nonzero, so C, B_E and B_M are positive definite in their respective spaces.
For epsilon!=0 apply the invertible congruence scaling

    S_epsilon=diag(I_x, |epsilon|^(-1) I_E, |epsilon|^(-2) I_M).

Equations (5) imply

    S_epsilon^T Hess F(x,epsilon a) S_epsilon
        -> -diag(C,B_E,B_M)                              (6)

in matrix operator norm as epsilon tends to zero from either side. For example,
the EM block after scaling is O(epsilon^2), the xM block is O(epsilon^4), and
the MM error is O(|epsilon|). The limit is negative definite. Thus for all
sufficiently small nonzero epsilon the scaled and original Hessians are
negative definite. This proves the diameter-two sufficient theorem on the
entire Sym(n) direction space, not just directions on E.

This congruence argument also checks the potentially dangerous mixed-block
effect: eliminating the supported-edge block would give a correction of order
epsilon^(10)/epsilon^2=epsilon^8 to a missing-edge block whose main order is
epsilon^4, too small to reverse its sign. No sign error in a Schur term is used.

Strict feasibility follows by shrinking epsilon so that
|epsilon| ||A||_op < min_i{x_i,1-x_i}. At each fixed allowed epsilon, continuity
then supplies an open strict-kernel neighborhood with full-Hessian negativity.
The open-neighborhood radius is allowed to shrink as epsilon tends to zero.

For fixed n, a compact strict diagonal box, a fixed diameter-two support graph,
||A||_F=1 and min_{e in E}|A_e|>=eta>0, the proof is uniform. Every supported
coefficient in B_E is at least 96eta^2; every missing coefficient in B_M is
at least 384eta^4. Analytic remainder constants are uniform on a common tube,
so a single epsilon threshold works for that compact family. The nonempty
weight range is eta<=1/sqrt(2|E|). No uniformity as eta tends to zero is claimed.

## 4. Complete n=3 classification

For a path 1--2--3 with weights A_12=a!=0, A_23=b!=0, A_13=0, (4) gives

    F_{z13,z13}(x,epsilon a)
       =-6 w_1 w_2 w_3 a^2 b^2 epsilon^4+O(|epsilon|^5). (7)

The two supported-edge diagonal entries have leading terms
-6w_1w_2 a^2 epsilon^2 and -6w_2w_3 b^2 epsilon^2. The diagonal-coordinate
block is negative at order one. The complete three-scale congruence (6)
proves full-Hessian negativity for every sufficiently small nonzero epsilon.

The three-vertex star is the same graph after relabelling; (7) is its missing
leaf-to-leaf edge formula. A triangle is covered by U3 or the E-only case of
the present proof. Thus every connected support on three vertices succeeds.

If only one edge is present, the third vertex is isolated. The next section
gives a cross-component direction with EXACT zero curvature for every strict
epsilon, so full-Hessian negativity fails, not merely its leading estimate.
The empty graph fails for the same reason. Hence connected support is necessary
and sufficient for the n=3 punctured-ray property.

## 5. Disconnected support is an exact obstruction in every dimension

If K is block diagonal over at least two vertex components, its DPP law
factorizes over these blocks: inclusion determinants factor and so does their
Mobius inversion. Write the exact law as p_S=product_b p_b(S_b).
Choose D=E_ij+E_ji crossing two distinct components.

Every principal inclusion determinant has zero first directional derivative
at the block-diagonal K. Indeed its submatrix is positive definite and block
diagonal, so det'(K_T)[D_T]=det K_T tr(K_T^{-1}D_T)=0. Consequently p'_S=0
for every exact atom. Moreover each block marginal law is unchanged along
K+tD, since its kernel submatrix does not change. Therefore for every block
event S_b, sum_{S:S restricted to b=S_b} p''_S=0.

Since log p_S=sum_b log p_b(S_b), the acceleration entropy term also vanishes:

    H''_K[D,D]=-sum p_S'^2/p_S-sum p_S''log p_S=0.        (8)

D is nonzero and has a small strict feasible affine interval. Thus the full
Hessian cannot be negative definite at any such K. Applied to X+epsilon A,
this proves that connected G is necessary in general.

## 6. Distance at least three: exact blocker, not a counterexample

If some pair ij has graph distance at least three, the common-neighbor sum
in (4) is zero. The order-six entropy expansion cannot establish a negative
leading missing-edge curvature for that coordinate. The weighted congruence
used for (6) then has a singular limit; one must compute higher orders and
their mixed-direction interactions, not merely continue the same assertion.

The accompanying bounded degree-eight calculation for the four-vertex path
1--2--3--4 and missing edge 14 tests the next distance. It is only an exact
SCOUT at a rational diagonal/weights. Even if that single curvature is negative,
it does not prove the full Hessian negative, let alone settle all connected
graphs with competing paths. General connected-support sufficiency remains
INCOMPLETE; no counterexample to it is claimed.

Review priorities: the exact likelihood (1), orthogonality eliminating degree
five and R2*R4, all edge triples contributing to degree six, mixed block orders,
the invertible scaling with three rates, and the exact disconnected obstruction.
The author does not self-certify CORRECT or claim an exhaustive graph theorem.
