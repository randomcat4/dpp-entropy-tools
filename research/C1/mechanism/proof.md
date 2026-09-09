# Proof and Computation Notes

## Rebuilding the B0 quantities

For a mask M subset of {1,2,3}, form the 3 by 3 matrix `A_M` by starting with
K and subtracting 1 from diagonal entry i when i is absent from M.  Then

    p_M = (-1)^(3-|M|) det(A_M).

This determinant form is the exact eight-event DPP probability formula for
n=3.  It also gives the first derivative in each symmetric coordinate:

    J_{M,(ij)} = (-1)^(3-|M|) (cof_{ij}(A_M)+cof_{ji}(A_M))

for i != j, and the single cofactor for diagonal coordinates.  This keeps the
off-diagonal factor two.

With p and J rebuilt, the script computes

    g_j = partial_j Lambda
        = sum_M (-1)^(3-|M|) J_{M,j}/p_M,
    Z = sum_M 1/p_M,
    F = J^T diag(1/p_M) J,
    F_pair = F - g g^T/Z.

The logarithmic matrix is

    N = -diag(ell_23, ell_13, ell_12) - Lambda K.

Let `adjN=adj(N)`, `d=det(N)`,

    a_j = tr(adjN E_j),
    T_ij = tr(adjN E_i adjN E_j).

Since `N^-1=adjN/d`, the matrix

    Htilde = d F_pair + T

equals `d M`, and `a=d eta`.  Therefore the linear solve

    Htilde h = a

gives `h=M^-1 eta`.  The two scalar tests used by the certificate are then

    beta sqrt(Z) = g^T h,
    d alpha = a^T h.

The actual optimizer direction is reconstructed as

    D_M = h/alpha,  alpha=(a^T h)/d.

The JSON output records `eta(D_M)` and `Lambda'(D_M)` at root midpoints as a
sanity check.  At the certified zero the exact sign change is on
`beta sqrt(Z)`, which is equivalent to beta because `Z>0`.

## Certified sparse-edge root

For epsilon=10^-8 set

    u(q)=(3/5,4/5,q/10000),
    K(q)=10^-8 I + (7/10) u(q)u(q)^T.

All entries are rational for rational q.  On the bracket

    q_L = 4418854248579277079/2305843009213693952,
    q_U = 8837708497158554159/4611686018427387904,

the eigenvalue formula gives strict feasibility:

    spec(K) = {epsilon, epsilon, epsilon+(7/10)(1+q^2 epsilon)}.

The interval certificate uses exact Fractions rounded outward to a dyadic grid
for every arithmetic operation.  Logarithms are enclosed by exact range
reduction to [1,2) followed by the positive-tail atanh series.  The interval
linear solve is Gaussian elimination with every pivot interval excluding zero;
the resulting residual intervals contain zero.

The endpoint beta signs are strictly enclosed:

    beta(q_L) sqrt(Z) > 4.67407989657799e-22,
    beta(q_U) sqrt(Z) < -2.49393515852079e-21.

All event probabilities are positive on the whole bracket:

    min_M p_M > 7.0000003569096650512e-17.

The leading minors of N are positive on the whole bracket; in particular

    det(N) > 27.2394697841539050297.

The same whole-bracket interval solve proves

    det(N) alpha < 0.925806704946127239064572716414179284 < 1.

By continuity of the rebuilt p, logs and nonsingular solve on this bracket,
the intermediate value theorem gives at least one exact q_* in (q_L,q_U) with
beta(K(q_*))=0.  The whole-bracket bound then applies to that exact beta-zero
kernel, so it satisfies B0 with a visible margin.

## What this does not prove

The proof above does not show that every beta-zero kernel satisfies B0, nor
that the sparse-edge root is unique.  It also does not prove the asymptotic
formula for the whole root tube; it only supplies a certified finite point and
a deterministic high-precision trend table.
