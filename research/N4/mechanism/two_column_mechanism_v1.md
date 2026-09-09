# Exact diamond coupling and a rational moving family

Author status: `INCOMPLETE` for frozen N4 v1. Identities and feasibility below
are author-derived and await non-author checking. This is a finite-dimensional
mechanism object, not a general concavity proof or counterexample.

## 1. Definitions and exact conditioning

Partition the four observed sites as A={1,2} and R={3,4}, and take

    K = [[A, b3, b4],
         [b3^T, d3, 0],
         [b4^T, 0, d4]],       0<K<I.

Here A is symmetric 2 by 2, 0<d3,d4<1 and the bj are real columns. Consider
only the actual affine chord K+sD with D_A=D_R=0 and D_AR=[e3,e4]. Fixing A
is part of this diagnostic, not an added assumption of the root theorem.

For t=(t3,t4) in {0,1}^2 put

    mj(tj) = dj if tj=1, and dj-1 if tj=0,
    qt = product_j dj^tj (1-dj)^(1-tj),
    Ct = A - sum_j bj bj^T / mj(tj).

The marginal law on R is the product Bernoulli law qt. Block determinant
factorization of the signed exact-event matrix gives, for U subset A,

    p_K(U,t) = qt p_Ct(U).

Consequently Ct is the genuine conditional DPP kernel on A and 0<Ct<I. The
last strict inequalities also follow by Schur complements, applying the
conditional inclusion/exclusion operations one site at a time. There is no
replacement of exact events by inclusion minors.

Since qt is constant along s, the entropy identity is exact:

    H(K+sD) = h(d3)+h(d4) + sum_t qt H2(Ct(s)),
    Ct(s) = A - sum_j (bj+s ej)(bj+s ej)^T / mj.

Define Sj=bj ej^T+ej bj^T. Then

    Ct'(0) = -S3/m3-S4/m4,
    Ct''(0) = -2 e3 e3^T/m3-2 e4 e4^T/m4.                 (1)

The conditional path is quadratic; the physical K path is affine. Keeping
the second derivative in (1) is essential.

## 2. Four-event formulas for H2, with conventions fixed

Write C=[[a,c],[c,b]], X=[[x,z],[z,y]], Y=[[xbar,zbar],[zbar,ybar]].
Use event order (11,10,01,00):

    p = (ab-c^2, a(1-b)+c^2, (1-a)b+c^2, (1-a)(1-b)-c^2),
    l_C(X) = (b x+a y-2c z,
              (1-b)x-a y+2c z,
              -b x+(1-a)y+2c z,
              -(1-b)x-(1-a)y-2c z),
    ell_C = log(p11 p00 / (p10 p01)).

All four probabilities are strictly positive. The exact directional Hessian
bilinear form B_C is

    B_C[X,Y] = -sum_i l_C(X)_i l_C(Y)_i / pi
               -(x ybar+xbar y-2 z zbar) ell_C.           (2)

This is obtained by differentiating -sum p log p twice. The mixed event
acceleration is (x ybar+xbar y-2z zbar)(1,-1,-1,1), and its sum vanishes.
Thus (2) needs no imported entropy theorem.

Let G_C be the symmetric matrix satisfying dH2(C)[X]=tr(G_C X). Its entries
are

    (G_C)11 = -b log(p11/p01)-(1-b)log(p10/p00),
    (G_C)22 = -a log(p11/p10)-(1-a)log(p01/p00),
    (G_C)12 = c ell_C.                                   (3)

The off-diagonal convention is important: the coefficient of z in the
directional differential is 2(G_C)12.

## 3. Exact two-column identity

Substitution of (1) into the chain rule yields

    H''(K)[D,D]
      = sum_t qt B_Ct[S3/m3+S4/m4, S3/m3+S4/m4]
        -2 sum_j ej^T (sum_t qt G_Ct/mj) ej.              (4)

The second line is conditional acceleration. It is a sum of separate
quadratic forms in e3 and e4, so it has NO e3-e4 mixed term. Pairing the
two values of tj rewrites its j-th contribution as

    2 ej^T sum_(t_other) q_other (G_C(tj=0)-G_C(tj=1)) ej. (5)

A1 already establishes that a single expression of this kind can be
positive. That observation by itself is not a new mechanism here.

The entire mixed contribution in (4) is

    2 sum_t qt/(m3 m4) B_Ct[S3,S4]
      = 2 (B_C11-B_C10-B_C01+B_C00)[S3,S4].              (6)

The identity follows because dj/dj=1 and (1-dj)/(dj-1)=-1.
There are no hidden qt weights in the last line. For example, C10 means
leaf 3 is present and leaf 4 is absent, regardless of the entropy-event
ordering used in (2).

Equation (6) is the new inspectable object: a discrete mixed Hessian
difference at four rank-one-shifted 2 by 2 kernels. It measures whether two
moving connection columns can reduce each other's conditional curvature
cost. It is not a proof that the reduction wins.

## 4. The exact matrix gate and its scope

For each j define the symmetric 2 by 2 matrix Lj by its quadratic form

    ej^T Lj ej =
      -sum_t qt/mj^2 B_Ct[Sj,Sj]
      +2 ej^T (sum_t qt G_Ct/mj) ej.                      (7)

Since Sj depends linearly on ej, this defines Lj uniquely. Define the
2 by 2 cross matrix M through

    e3^T M e4 = (B_C11-B_C10-B_C01+B_C00)[S3,S4].        (8)

Thus the Hessian restricted to these four direction coordinates is

    H'' = -e3^T L3 e3 -e4^T L4 e4 +2 e3^T M e4.         (9)

These Lj are full single-column curvature costs, not the Fisher terms
alone. They include conditional acceleration. In particular they must not
be assumed positive merely because each conditional H2 Hessian is negative.

If L3 and L4 are positive definite, all two-column directions have
nonpositive curvature if and only if

    || L3^(-1/2) M L4^(-1/2) ||_op <= 1.                (10)

Proof: the negative of (9) is the quadratic form of
[[L3,-M],[-M^T,L4]]. Conjugating by the block diagonal square roots reduces
positive semidefiniteness to [[I,-T],[-T^T,I]]>=0, which is equivalent to
the singular values of T being at most one. A singular value greater than
one supplies an explicit positive-curvature direction by the associated
left and right singular vectors and inverse square roots.

If either Lj is not positive semidefinite, the corresponding single-column
direction already violates this restricted curvature condition. If the Lj
are only semidefinite, one must first check

    ker(L3) subset ker(M^T),    ker(L4) subset ker(M).

Failure of either condition produces an indefinite block quadratic form.
If both hold, replace inverse square roots by Moore-Penrose inverse square
roots in (10). This includes zero-rank blocks.

The remaining obligation is to prove (10), with its singular boundary
conditions, for the coupled DPP data, or to find a strict failure and then
certify an affine entropy chord. It is stronger than checking either Lj
alone. It does not cover directions changing A or the leaf diagonal/block.

## 5. A strictly feasible rational moving family

For rational 0<r<=1/2 set

    A = [[1/2,1/10],[1/10,1/3]],
    u = (1/5,1/6)^T,       v = (1/7,-1/8)^T,
    d3=r^2, d4=r^4,       b3=r u, b4=r^2 v.

Let e=(1/8,-1/9)^T, f=(1/10,1/11)^T, and choose the affine direction with
columns e3=r e and e4=r^2 f. Then K_r+sD_r replaces u,v by
u_s=u+s e, v_s=v+s f. This supplies a concrete chord for every rational
|s|<=1/4. Both triangles are present and have opposite invariant signs:

    K12 K13 K23 > 0,       K12 K14 K24 < 0.

No diagonal sign gauge can remove the conflict. Diagonals are unequal.
The covariance support graph is a diamond, with two independent cycles.

Here is an explicit feasibility proof for the full interval, rather than
just the center. The componentwise bounds for |s|<=1/4 are

    |u_s| <= (1/4,1/5),    |v_s| <= (1/5,3/20).

The absolute row sums of u_s u_s^T+v_s v_s^T are therefore bounded by
73/400 and 57/400. The diagonal-dominance margins of A are 2/5 and 7/30.
Since both margins exceed 73/400 and 57/400 respectively,

    A-u_s u_s^T-v_s v_s^T > 0.

The Schur complement of diag(r^2,r^4) in K_r+sD_r is exactly that matrix,
so K_r+sD_r>0. For its complement the Schur complement is

    I-A-[r^2/(1-r^2)] u_s u_s^T
        -[r^4/(1-r^4)] v_s v_s^T.

Both bracketed coefficients are <=1 (in fact <=1/3 and <=1/15). The
diagonal-dominance margins of I-A are 2/5 and 17/30, exceeding the same
absolute-row-sum bounds. Therefore K_r+sD_r<I.

The limits have two interior eigenvalues (those of A) and two zero
eigenvalues. The limit is not a projection. Thus the fixed near-projection
R2 hypotheses and the A2 near-projection compact moving-frame family do
not apply directly. The family also has two separate leaf scales; no
uniform asymptotic claim is made here. The route owner is deriving the
scale analysis independently.

The eigenspaces cannot be jointly fixed: for distinct r,s the (3,4) entry
of the commutator [K_r,K_s] is

    rs(s-r) u^T v,           u^T v = 13/1680 != 0.

Hence the midpoints do not commute. This is an algebraic obstruction to
one simultaneous fixed eigenbasis, not a claim of entropy invariance under
arbitrary rotations.

## 6. Known two-site concavity lifted by conditioning (not a new contribution)

More generally, fix every entry outside a principal 2 by 2 block, including
all cross-block entries, in any dimension. The remaining principal block
need not be diagonal. Conditional on its full event T, the central kernel
is A-R_T with R_T fixed; its weight q_T is also fixed. Hence the already
known two-site entropy concavity, applied to
H(rest)+sum_T q_T H2(A-R_T), directly proves concavity on the entire central
2 by 2 block. This is an immediate conditioning lift of an existing result
and is not counted as a new contribution of this unit. The formula below
merely provides an explicit single-edge diagnostic on our family.

For any strict real kernel of any size, vary only one symmetric edge
K12=K21 while all other entries stay fixed. Condition on every other site.
The conditional marginal weights are fixed and the conditional two-site
kernel varies only in its off-diagonal c, with derivative one. Formula (2)
then gives

    d^2 H2/dc^2 = -4c^2 sum_i 1/pi +2 ell_C <= 0.

Indeed p10 p01-p11 p00=c^2, so ell_C<=0, with equality precisely c=0.
Summing over conditional events proves single-edge concavity, including
every chord remaining strictly feasible. This is a direct elementary
diagnostic exclusion, not a newly claimed general theorem of research value.

For the diamond above, the conditional off-diagonal is

    c_t = 1/10 - (b3)_1(b3)_2/m3 - (b4)_1(b4)_2/m4.

Its change when t3 switches is nonzero, so it cannot vanish in all four
conditional events. Thus the central-edge curvature is strictly negative
throughout this rational family. The result holds uniformly in the sense
of sign at each r; no positive lower bound as r tends to zero is asserted.

## 7. Controlled extension to five and six vertices

The exact mechanism extends to A of size two and k=3 or 4 independent
leaves. Take d_(j+2)=r^(2j), b_(j+2)=r^j u_j, j=1,...,k, with u1=u,
u2=v, u3=(1/11,1/13)^T and u4=(1/17,-1/19)^T. Use only the first k
columns. With 0<r<=1/2 these kernels are strictly feasible: adding the
absolute row sums of u3 u3^T and u4 u4^T to the bounds in Section 5 still
leaves both A and I-A strictly diagonally dominant after subtraction.
The first two columns may follow the same |s|<=1/4 chords, with the new
columns fixed. There are k independent triangles and both triangle signs.

For arbitrary simultaneous leaf-column directions, equations (1)-(5) hold
with a sum over all leaves. Each cross pair (j,l) is exactly

    2 sum_(t_other) q_other
        (B_C11-B_C10-B_C01+B_C00)[Sj,Sl],

where 11,10,01,00 now refer only to leaves j,l and the other events are
held fixed. The full sign test is positivity of the resulting 2k by 2k
block cost matrix. Pairwise two-column tests alone do not imply that full
matrix is positive semidefinite. No n=5 or n=6 search was run in this unit.

## 8. Failed shortcuts and exact remaining gap

1. Positive conditional acceleration is insufficient and already known
   from A1. The total cost in (7) must be kept.
2. Separate concavity in each connection column is insufficient: (8) can
   couple the columns. Its normalized singular value is the actual gate.
3. A conditional quadratic path is not the target path; omitting Ct''
   changes the problem.
4. No sign of (6), (9), or the entropy gap for the displayed moving-column
   direction is asserted without evaluation/proof.
5. A finite failure to find a positive value of (9) would not prove (10)
   for all centers, or the unrestricted frozen N4 statement.

The output of this unit is the exact mixed-Hessian gate, its singular
boundary, a feasible rational two-cycle family, and a single-edge analytic
exclusion. General concavity and research novelty remain unresolved.
