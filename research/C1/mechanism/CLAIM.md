# I05-C1-20260909 mechanism child claim

Task: C1 mechanism falsification and interval computation for B0.

Frozen target used here: for every connected strict real symmetric 3 by 3 DPP
kernel K in the B0 coordinate system, if beta(K)=0 then det(N) alpha(K) <= 1.
The quantities F, N, M, alpha, beta and the true trace-normalized direction
D_M are reconstructed from the eight event probabilities and the six symmetric
coordinates (11,22,33,12,13,23). Off-diagonal directions use Eij+Eji.

Mechanism attacked: twisted complement affine segments

    K(t; epsilon, u, lambda) = (1-t) A + t S(I-A)S,
    A = epsilon I + lambda u u^T,
    S = diag(-1,1,1),

with lambda fixed at 3/5. The first deterministic table keeps
u proportional to (1,2,3) and tests epsilon=10^-2,10^-3,10^-4,10^-5.
This is a joint boundary/ratio degeneration probe, not a random scan. If beta
changes sign, the root is bracketed and det(N) alpha is evaluated at the true
M-optimizer D_M=M^-1 eta/alpha. A later interval certificate may be produced
for one new root branch if it gives useful evidence.

Key falsifiable assertion for this child: along the above exact K-affine
family, beta-zero roots persist as epsilon decreases and det(N) alpha moves
toward the boundary value 1 without exceeding it in the tested range. A
certified violation would require an exact beta root with det(N) alpha > 1 and
a strict finite K-affine entropy chord. A near-zero floating beta is recorded
only as a scout.

Excluded by assignment: no revival of the failed conditional projection
families or locked-odds dominance bound, no random-point enlargement, no claims
about global B0 from finite tables, and no use of C:/canglan.
