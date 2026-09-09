# The acceleration sign alone fails on a Lambda tangent

AUTHOR STATUS: PROVED_CANDIDATE_PENDING_NONAUTHOR_REVIEW. This is a
counterexample to an auxiliary shortcut, not to the frozen implication B0
or to entropy concavity on the Lambda tangent hyperplane.

Use the frozen six coordinates (11,22,33,12,13,23), and set

    K=(1/100)[[50,4,6],[4,50,8],[6,8,50]],
    D=(1,1,1,-3824639319575184888399/113394806345511264244256,0,0).

The matrix K is strict: both K and I-K are strictly diagonally dominant
with positive diagonal, so their eigenvalues are positive. All three graph
edges are nonzero. The eight probabilities and their derivatives are the
exact principal-minor event polynomials, with symmetric off-coordinate
derivatives. Define g=grad Lambda at K. The fourth coordinate of D was
chosen as -(g_1+g_2+g_3)/g_4, with g_4 nonzero. Exact rational arithmetic
therefore gives g^T D=0, without any tolerance or approximate root.

For this direction, write

    F(D,D)=sum_S p'_S(D)^2/p_S,
    C(D)=2 tr(N adj(D))=-sum_S p''_S(D) log p_S,
    B(D,D)=F(D,D)-C(D).

The identity for C follows from the inherited exact second derivative of
entropy, and is evaluated here from the event Hessians. The rational log
series certificate gives

    0.376241571363 <= C(D) <= 0.376241571364,
    12.007687710971 <= B(D,D) <= 12.007687710972.

Both lower endpoints are strictly positive. The certificate uses the
existing exact rational log-bounds implementation (range reduction and
the bounded artanh tail), with its inputs, source hashes and output saved
alongside this note. Fisher's value is rational and is recorded exactly.

For every affine K+sD, the entire three Rayleigh polynomials obey

    Delta_ij det(diag(z)+K+sD)
      = [(z_k+K_kk+sD_kk)(K_ij+sD_ij)
           -(K_ik+sD_ik)(K_jk+sD_jk)]^2.

The output stores every coefficient in s of the z_k^2, z_k and constant
terms. Thus this direction retains the full square identity and its
affine derivatives. Feasibility persists on a neighborhood of s=0 by
strictness. No endpoint-only relaxation is used.

Consequently the proposed shortcut
`full real square identities + Lambda'[D]=0 => C(D)<=0` is false.
The stronger useful inequality `F(D,D)>=C(D)` on the same tangent
hyperplane is not refuted: this point satisfies it with a large margin.
D is not asserted to equal the optimizing direction H^-1 eta, and beta(K)
is not asserted to vanish. This witness therefore supplies no B0
counterexample and leaves the Fisher-control obligation open.

Execution: one deterministic rational center, no seed, one CPU thread,
server PID 161284, exit 0. The exact files are
`lambda_tangent_certificate.py` and `lambda_tangent_certificate.json`.
