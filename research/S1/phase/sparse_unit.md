# Second unit: sparse centers and missing harmonics

Status: **INCOMPLETE** for a positive entropy-rate mechanism. The parity-block identity below is **PROVED** for finite-window entropies; all sign observations remain numerical.

This unit was explicitly assigned after the first unit. Its hypothesis was that a harmonic missing at the center could have a small negative single-edge curvature, allowing mixed new-edge terms to dominate. It tested same-parity missing distances 2 and 4, biased density to break complement symmetry, and small second/third harmonic corrections. It did not extend the first dense-center screen by brute force.

## Exact parity block identity

Let the center have p=1/2 and a_k=0 for every positive even k. Let Q be the finite entropy Hessian in the real coordinates b_k of the imaginary Fourier directions. Then

    Q_kl=0 whenever k and l have opposite parity.

Proof. Put U_jj=(-1)^j on the finite index window and transform any kernel by

    T(K)=U(I-K)U*.

Replacing K by I-K complements all bits and preserves configuration entropy. Diagonal unitary conjugation preserves every inclusion determinant and hence the complete DPP law. Thus H(T(K))=H(K). At this center, diagonal entries remain 1/2, odd-distance entries acquire factor +1 and even-distance entries acquire factor -1. Since all even-distance center entries vanish, T fixes the center. For a distance-k imaginary direction D_k,

    T(K_0+sum t_k D_k)=K_0+sum (-1)^(k+1)t_k D_k.

Strict interiority gives analytic finite entropies. Differentiating the entropy invariance twice at zero shows Q_kl=(-1)^(k+l)Q_kl. This proves the claim. It also applies with nonzero odd center harmonics such as a_3; a nonzero a_2 or p!=1/2 can break it.

The invariant finite entropy identity also passes to the entropy-rate limit as an identity of values. No existence or interchange of entropy-rate Hessians is asserted.

Thus missing b_2 and b_3 cannot mix quadratically at an unbiased nearest-neighbor center. Same-parity missing b_2,b_4 is a more discriminating probe.

## Predeclared finite coverage

The 10 center points were:

- p in {1/2,1/4}, a=(p*s,0,0,0) for s in {1/2,9/10,49/50}: six centers.
- p=1/2, a_1=9/20, exactly one of a_2,a_3 equal to either +1/100 or -1/100, and other a_k=0: four centers.

All have a strict triangle feasibility margin, stored exactly in the output. This is a Hessian probe on a neighborhood of each fixed symbol, not a window-dependent symbol. For example, taking all |t_k|<=margin/8 retains at least margin/2 of the center's triangle bound when four harmonics are used. Parameters and any such chosen perturbation box are independent of n.

The complete 4-by-4 imaginary harmonic Hessian was computed at n=6,8,10 for each center: **30 Hessians, 13440 event determinant/inverse evaluations**. Directions use the sine coefficient normalization D_k entries +/-i/2. No random draws or adaptive unreported points were used.

All 30 computed matrices were negative definite. The largest top eigenvalue among them was about -1.14023143e-6. This number is comfortably larger than the recorded normalization residuals, but it remains an ordinary floating point observation and not an interval proof.

For the three unbiased pure nearest-neighbor centers, the n=10 ratio

    rho_24=|Q_24|/sqrt(Q_22*Q_44)

was:

| a_1 | rho_24 | largest eigenvalue of the (2,4) block |
|---:|---:|---:|
|1/4|0.000954529802|-0.000187289158|
|9/20|0.0553842428|-0.0275598644|
|49/100|0.120505459|-0.0680568389|

For a negative-diagonal 2-by-2 block, rho_24>1 would be necessary and sufficient for a positive eigenvalue. The tested values remain below 1. At a_1=49/100 the block was

    [-1.319456042498, -0.036390715621]
    [-0.036390715621, -0.069115081715].

Opposite-parity entries in the unbiased odd-only centers were of floating point residual size, agreeing with the exact lemma. The density-biased centers had nonzero opposite-parity entries but remained negative definite. Both signs of the small even-center perturbation also remained negative definite. Small a_3 perturbations preserved the exact parity rule, as predicted.

Across this batch, the maximum probability normalization error was 1.99840144e-15, maximum event first-derivative residual 1.31973195e-17 and maximum second-derivative total-mass residual 2.20850543e-15. These are implementation diagnostics, not error certificates for the eigenvalues.

## Why the proposed easy escape fails here

A missing Fourier coefficient does not imply zero conditional correlation after the other sites are observed. The single-edge proof in `proof_or_blocker.md` shows that the relevant real conditional edge is a Schur-complement entry. A nearest-neighbor path can fill this entry even when the unconditioned long edge is zero. Consequently the missing harmonic still incurs negative quadratic cost. The computed same-parity mixed term was too small to overcome that cost in every declared example.

There is no analytic all-parameter bound rho_24<=1 in this report. Nor do the finite negative Hessians exclude a positive entropy-rate chord at another amplitude, at another center, or in another harmonic family. The minimal remaining local obligation is a rigorously controlled mixed-edge coupling inequality or a concrete fixed symbol whose coupling exceeds the negative diagonal losses. None was obtained. No larger window or wider scan is launched after this unit.

Provenance: the sparse-center follow-up was assigned by the main instance. The parity symmetry was independently recognized here and by the main instance before the shared suggestion was received; this report supplies the direct proof. The phase sub-instance wrote and ran the finite diagnostics. Independent review remains outstanding.
