# EW primary-source and inheritance map

This is C1's source mapping for the assigned first review, not a second
review. It records how the new EW argument must connect to the unchanged
FR author proof. Acceptance is recorded separately in review_report.md.

## New infinite-range obligations

The A_beta assumption supplies exponential Fourier tails. The new proof
must obtain one weighted Schur-norm inverse bound uniformly over all finite
complete-event matrices, followed by one common complex perturbation disk.
For the band approximation, its inverse bound grows at most linearly in
the chosen bandwidth, whereas the weighted truncation error decays
exponentially. This is the mechanism that replaces a small-Wiener-norm
assumption without requiring the mean to equal one-half.

Remote-condition estimates must include both the near/far Schur correction
and the nonzero direct Fourier tails. In the block identity used there,
the inverse far Schur complement is exactly the far/far block of the full
inverse. Uniform scalar convergence is followed by convergence in a fixed
weaker Hölder norm: choose an exponent below the available variation decay
and interpolate the truncation error with that variation bound. Cauchy
estimates alone on scalar suprema would not establish this Banach-space
step. These are proof obligations checked by the first reviewer.

## RPF spectral gap and analytic perturbation

Cioletti and Silva,
[Spectral Properties of the Ruelle Operator on the Walters Class over Compact Spaces](https://arxiv.org/pdf/1511.01579)
(v2), Theorem 2.1, p. 4, supplies a simple maximal eigenvalue and a strict
spectral gap for Hölder potentials with exponent between zero and one.
Lemma 2.4 and Proposition 2.6 / Corollary 2.7, p. 5, give analytic operator
dependence on the indicated Banach spaces. The paper also exhibits the
failure of a gap for some broader Walters-class potentials; that broader
class alone is not the hypothesis used here.

For this binary shift, take the alphabet prior uniform on {0,1} and the
potential log(2G), where G is the positive normalized one-sided conditional
function. Its integral transfer operator is then the sum operator in FR.
A weaker exponential tail metric provides a fixed admissible Hölder
exponent. Positivity, normalization and operator-norm holomorphy must be
proved for this G before applying the theorem and a contour projection.

An alternative direct gap source is Kloeckner, Lopes and Stadlbauer,
[Contraction in the Wasserstein metric for some Markov chains, and applications to the dynamics of expanding maps](https://arxiv.org/pdf/1412.0848)
(v3), Theorem 1.1, pp. 3-4, and Corollary 1.2, p. 4. Prepending either
binary symbol contracts the exponential tail metric; log G is Lipschitz in
that metric. The corollary states a norm gap on mean-zero observables, not
merely weak convergence of probabilities.

## Inherited author derivations

The unchanged finite_range_local_theorem.md has blob
`c65a4e22ed6ee5c69d1b084cfd04d8e77e8d6263`. Its chain-rule entropy and
relative-entropy rate formulas, parity normalization, cancellation of the
s-linear coefficient, disjoint-edge negative-association tilt, and quartic
curvature conversion must be checked to use only the hypotheses recovered
by EW. Its first-review report is not a premise for this new reviewer.
The exponentially summable conditional error is what controls the O(1)
finite-volume boundary contribution; no volume derivative interchange is
being substituted for it.

For the inherited matching input, C1 directly checked Lyons,
[Determinantal Probability Measures](https://arxiv.org/pdf/math/0204325)
(v4): Theorem 8.1, p. 34, states conditional negative association for the
law of a positive contraction. Equations (6.6)-(6.7), p. 20, describe the
disjoint-coordinate product inequality and explicitly allow decreasing
functions. The nonnegative decreasing edge tilts in FR therefore match
the primary theorem's scope. This supplements the reviewer's separately
reported source-page check without changing that provenance account.

The seven-file companion scope contains the new exact Rudin-Shapiro
checker and its stored output. C1 inspected their source consistency but
did not execute the checker. Their evidentiary scope is the displayed
finite polynomial constants, not entropy-rate analyticity or concavity.
No broader novelty, global-interval result or new formal proof is certified.
