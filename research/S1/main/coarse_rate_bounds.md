# Coarse genuine-rate bounds used by the baseline

Scope: fixed degree-m real scalar trigonometric symbol f with epsilon<=f<=1-epsilon. No novelty claim is made. The formulas below are mathematical inequalities; their recorded floating-point evaluations are not outward-rounded certificates.

Let c_k=fhat(k), K_N=(c_(i-j)) and H_n=H(P_(K_n)). The process is m-dependent: restrictions to sets separated by more than m are independent because their joint inclusion determinants factor, and inclusion-exclusion determines their joint laws.

For q blocks of n consecutive sites, separated by m discarded sites, their joint entropy is q H_n. This is at most the entropy of the containing interval, by monotonicity under adding coordinates. Dividing by its length and letting q increase proves

    H_n/(n+m) <= h(f).

Stationarity and the entropy chain rule give the standard decreasing upper bounds

    h(f) <= H_n-H_(n-1) <= H_n/n.

For a second lower bound, partition a length-qn Toeplitz compression into q adjacent n-site blocks and call the block diagonal B. Each compression inherits the uniform spectral margin. The independently reviewed finite [T2 inequality](../../T2/frozen_theorem_v1.md) gives

    0 <= q H_n-H_(qn) <= ||K_(qn)-B||_F^2/[epsilon(1-epsilon)].

There are at most q-1 cuts. For each positive displacement k, at most k edges cross any one cut. Counting a long edge more than once only increases the upper bound. Hence, including both matrix orientations,

    ||K_(qn)-B||_F^2 <= (q-1) C,
    C=2 sum_(k=1)^m k |c_k|^2.

After division by qn and q->infinity,

    h(f) >= H_n/n-C/[n epsilon(1-epsilon)].

The baseline script uses the maximum of these two lower bounds and zero, with H_n-H_(n-1) as upper bound. All limiting operations use finite inequalities for the same fixed symbol. No entropy derivative is passed through a limit.

The n=12 gap enclosure is approximately [-0.0608912,0.0592904]. It is valid as a floating evaluation of the stated formulas but cannot certify either sign. This negative outcome motivates the extreme-past conditional method on the same fixed candidate, rather than a larger copy of this coarse scan.
