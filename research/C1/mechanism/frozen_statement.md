# Frozen Statement Used by Mechanism Child

Proof and computation in this child use the parent B0 statement without
changing its assumptions.

Let K be a real symmetric 3 by 3 matrix with 0<K<I and connected nonzero
off-diagonal graph.  Coordinates are

    (x,y,z,a,b,c)

for

    K = [[x,a,b],[a,y,c],[b,c,z]],

and the six tangent bases are

    E11, E22, E33, E12+E21, E13+E31, E23+E32.

For each S subset of {1,2,3},

    p_S = sum_{T superset S} (-1)^(|T|-|S|) det K_T,

with all eight p_S positive.  The entropy is the full eight-atom Shannon
entropy.  Define F, ell_ij, Lambda, N, d=det(N), eta, G, F_pair, M, alpha and
beta exactly as in the parent frozen statement:

    F_ij = sum_S dp_S[E_i] dp_S[E_j] / p_S,
    ell_12 = log(p_empty p_12/(p_1 p_2)),
    Lambda = log(p_123 p_1 p_2 p_3/(p_empty p_12 p_13 p_23)),
    N = -diag(ell_23, ell_13, ell_12) - Lambda K,
    M = F_pair + d G,
    alpha = eta^T M^-1 eta,
    beta = v_score^T M^-1 eta.

The target B0 is:

    beta(K)=0 implies det(N) alpha(K) <= 1.

The true normalized direction is

    D_M = M^-1 eta / alpha.

No arbitrary Lambda-tangent direction may replace D_M.

## Child Specialization

This child certifies only the following partial object:

    K(epsilon,q)=epsilon I+(7/10)u(q)u(q)^T,
    u(q)=(3/5,4/5,q sqrt(epsilon)),
    epsilon=10^-8.

The certified q bracket is

    [4418854248579277079/2305843009213693952,
     8837708497158554159/4611686018427387904].

This K is strict because its eigenvalues are epsilon, epsilon and

    epsilon + (7/10)(1+q^2 epsilon),

which is <1 throughout the bracket.  It is connected because q>0 and all
three off-diagonal entries are nonzero.  The certificate proves an exact beta
zero in the bracket and `det(N)alpha<1` throughout the bracket.

This specialization is a rational finite-epsilon endpoint variant.  It is not
the unit-normalized finite-epsilon family, though it has the same leading
kappa=q^2 sparse asymptotic cue.
