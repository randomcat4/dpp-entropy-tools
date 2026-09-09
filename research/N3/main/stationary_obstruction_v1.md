# The conditional-score shortcut fails even at the true optimizer

Author status: EXACT_CERTIFICATE_PENDING_NONAUTHOR_REVIEW.
This supersedes the open sufficient candidate in section 3 of the earlier
frozen `conditional_score_lemma_v1.md`; that earlier version is retained.

Let A,eta,N be exactly the frozen six-coordinate DPP quantities. Define
`d=A^-1 eta` and `d_*=d/(eta^T d)`. The second vector is the unique minimizer
of d^T A d subject to eta^T d=1. It is the optimizer of A, not of F alone.

Consider the strict rational kernel

    K=(1/100) [[51,24,-24],[24,48,-24],[-24,-24,52]].

Write C(D)=2tr(N adj D), and Q_k for the conditional determinant-score
quadratic forms in the earlier frozen lemma. The certificate encloses the
exact solution of A d=eta and proves, with energy E=d^T A d>0,

    (Q_1(d)-C(d))/E in [-0.101833309756,-0.101833309755],
    (Q_2(d)-C(d))/E in [-0.101569942472,-0.101569942471],
    (Q_3(d)-C(d))/E in [-0.101967455682,-0.101967455681],
    (F(d)-C(d))/E   in [ 0.547561495186, 0.547561495187].

All these ratios are unchanged upon normalizing d to d_*. The normalizer
eta^T d is strictly positive, and the independent rank-one representation
gives rho in [0.452438504813,0.452438504814]. Thus this is a strict actual
DPP counterexample to the stationary sufficient condition
`max_k Q_k(d_*)>=C(d_*)`. It is not an entropy counterexample. Every convex
combination of the three Q_k fails at the same true optimizer.

## Rigorous enclosure, including stationarity

`certify_stationary_obstruction.py` uses the exact rational atom polynomials
and gradients. Each log probability is enclosed by the positive artanh series
and its rational remainder from the first certificate. Arithmetic on N,
N^-1, A and eta is then performed with outward integer rounding to multiples
of 2^-180. Every division interval excludes zero. Gaussian elimination has
strictly positive enclosed pivots and encloses the exact unique linear solve.
The Q_k coefficients themselves are exact rational numbers.

This certifies the exact stationary vector through interval linear algebra;
it does not infer stationarity from a rounded trial direction. The JSON
records the raw vector enclosure, its trace normalizer, normalized vector,
all three gap intervals, elimination pivots, source hashes, PID and exit code.
Feasibility of K is checked by exact rational LDL for both K and I-K.

## Discovery and limits

The discovery unit minimized the specific normalized stationary projection
gap over six kernel parameters, using four fixed starts and a strict maximum
of 128 objective evaluations per start. All 512 calls executed, with zero
rejections; 164 had negative projected gaps. All four optimization runs hit
their stated call limits, so no global optimization claim is made. Their
purpose was candidate generation. The final certificate uses the separate
small-denominator kernel displayed above.

The earlier 180 boundary centers did not refute this candidate. The targeted
interior search does. This is why neither those non-hits nor the initial 12
directions can support a universal lower-bound claim.

The remaining proof must retain or otherwise control the positive residuals
F-Q_k. The optimizer's stationarity equations alone do not justify deleting
them. The frozen entropy target and all its premises remain unchanged.
