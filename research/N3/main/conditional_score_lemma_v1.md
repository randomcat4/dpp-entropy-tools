# Conditional determinant scores: exact lower bound and obstruction

Author status: PROOF_CANDIDATE_PENDING_NONAUTHOR_REVIEW.
The global entropy statement remains INCOMPLETE.

## 1. A lower bound using two conditional covariance squares

Fix any positive differentiable probability law on three binary variables.
For a conditioning coordinate k, split its eight atoms into two tables
`(a,b,c,d)`, ordered `(00,10,01,11)` on the other coordinates. In each table
write

    m=a+b+c+d, delta=ad-bc,
    V=ad(a+d)+bc(b+c)-4 delta^2/m,
    u=delta' - 2 delta m'/m.

All derivatives are evaluated at one point. Let s be the event score p'/p.
On this table define h=(d,-c,-b,a), and h0=h-2delta/m.
Then

    sum_table p h=2delta,  sum_table p h0=0,
    sum_table p h0^2=V,
    sum_table p h0(s-m'/m)=u.

The first identity is direct multiplication. The second follows by centering;
expanding its square proves the third. The last follows by differentiating
ad-bc. Since h has positive and negative coordinates and all atoms are
positive, h is not constant and V>0. Weighted Cauchy therefore gives

    sum_table p (s-m'/m)^2 >= u^2/V.

The Fisher chain rule, obtained by expanding the centered squares, yields

    F >= Q_k := (m_1')^2/(m_0 m_1) + sum_two_tables u^2/V.       (L1)

No DPP property is required for this inequality. It is an elementary score
projection, not a novel general information inequality.

For the actual DPP path K+tD, m_1=K_kk and m_1'=D_kk. The DPP identities add
the essential specialization delta=-w^2, where

    w_0=(1-K_kk)K_ij+K_ik K_jk,
    w_1=K_kk K_ij-K_ik K_jk.

Consequently u=-2w(w'-w m'/m), including w=0 without division by w.
Thus Q_k is an explicit nonnegative quadratic form in the six entries of D,
built from the actual conditional covariance squares and their derivatives.

The omitted information is explicit. With gamma=u/V,

    F-Q_k = sum_two_tables sum_table p
             (s-m'/m-gamma h0)^2.                              (L2)

This identity follows by completing the square. Its four residual conditional
score dimensions cannot be discarded merely because they are nonnegative.

## 2. A tempting sufficient inequality is false

Put C(D)=2 tr(N adj D); the inherited target is B(D)=F(D)-C(D)>=0.
The all-direction shortcut

    max_k Q_k(D) >= C(D)                                      (FALSE)

would imply the target by L1. It fails at the simple actual DPP point

    K=(1/100) [[30,29,15],[29,33,10],[15,10,16]],
    D=diag(1,1,1/3).

The exact atoms in bitmask order 0,1,2,12,3,13,23,123 are
`(292541,260259,272959,14241,92359,24841,42141,659)/1000000`.
The rational LDL checks certify 0<K<I, and also 0<K+-D/100000<I.
The certificate computes the following outward bounds using rational
arithmetic and a logarithm series with a proved remainder:

    max Q_k - C in [-1.911698525970, -1.911698525969],
    B=F-C       in [30.995287355311, 30.995287355312].

Every convex combination of the three Q_k fails at this same direction.
The true entropy curvature is strictly negative. This is a counterexample to
the proposed lower-bound shortcut, not to entropy concavity.

The checker uses log x=log y+j log 2 with 1<=y<=2. For z=(y-1)/(y+1),
the positive 70-term series 2 sum_{r=0}^{69} z^(2r+1)/(2r+1) is a lower bound;
adding 2 z^141/[141(1-z^2)] is an upper bound. Sign-aware rational interval
arithmetic evaluates C=-sum p'' log p. Rounded displayed bounds are outward.

## 3. What the optimizer can still add

Let A,eta be the inherited six-coordinate positive operator and weighted
trace. The unique minimizer under eta^T d=1 is

    d_* = A^-1 eta/(eta^T A^-1 eta).

For every weighted-trace-zero E it satisfies

    F(D_*,E)+det(N) tr(N^-1 D_* N^-1 E)=0.                    (S)

The all-direction witness above makes no claim about this stationary
direction. One may still test Q_k(D_*) or exploit (S) to control the residual
in L2. Simply postulating max Q_k(D_*)>=C(D_*) is a stronger sufficient
condition, not a proved lemma and not an equivalent reformulation.
The exact remaining obligation is to bound the score components retained
in L2 using (S), or replace this projection by one retaining enough of them.
No bound on those residual components has been proved here.

## 4. Executed evidence and scope

U1 evaluated 12 deterministic asymmetric rational centers using the true
trace optimizer; the projected bound sufficed at those 12 directions.
U2 evaluated full averaged quadratic forms at 36 deterministic asymmetric
centers: 20 yielded a negative averaged-bound direction, and 14 of those
also violated all three individual bounds. These are finite scouts only.
U3 simplified and certified the single displayed rational obstruction.
All three server jobs used one thread, recorded PIDs and exited 0.
The inherited event polynomials and rank-one reduction are reused with
recorded source hashes; the independent reviewer must reconstruct the
new formulas rather than treating author assertions as an audit.
