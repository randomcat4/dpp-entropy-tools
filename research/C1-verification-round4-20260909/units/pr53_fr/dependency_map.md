# Primary dependency and comparison map

This is C1's source mapping for the fresh Theorem FR reviewer, not a second
review or an independent acceptance of the new theorem.

## RPF gap and uniqueness

Kloeckner, Lopes and Stadlbauer,
[Contraction in the Wasserstein metric for some Markov chains, and applications to the dynamics of expanding maps](https://arxiv.org/pdf/1412.0848)
(v3): Theorem 1.1, pp. 3-4; Corollary 1.2, p. 4; Definition 2.3.
The hypotheses are a compact metric space, contracting inverse branches in
the stated iterated-contraction sense, and a Lipschitz potential. The
normalized operator has a unique invariant probability and a norm spectral
gap on the complement of constants. Page 4 explains the Hölder version
through a snowflaked metric.

For the binary full shift, the branches prepend 0 or 1 and contract the
tail metric `d_b(x,y)=exp(-b N(x,y))` by `exp(-b)`. Theorem FR therefore
needs a fixed b>0 with its potential `log G_0` Lipschitz in that metric,
as well as positivity and normalization. The fresh review checks that
Section 5 actually establishes these facts; scalar uniform convergence
alone is not being used as a substitute.

## Analytic eigendata

Giulietti, Kloeckner, Lopes and Marcon,
[The calculus of thermodynamical formalism](https://arxiv.org/pdf/1508.01297):
Section 2.1 hypotheses H1-H4 and Corollary 3.7, p. 19, establish analyticity
of the Gibbs map into the dual of the observable Banach space under the
stated assumptions. This paper assumes the RPF gap as H3-H4; it is not an
independent proof that FR satisfies those hypotheses. Theorem FR instead
states a Riesz-projection argument after obtaining a gap. Both approaches
require operator-norm holomorphy on one fixed space and an isolated simple
eigenvalue. The correct object is the eigenmeasure as a functional on
Hölder observables, not differentiability in a probability metric.

## Exact PR39 comparison

The [PR39 frozen statement](https://github.com/randomcat4/dpp-entropy-tools/blob/5558a6b22ef8eb080d198d4af6b1a5cfe2fb164f/research/W2/nonconstant_orbit/frozen_statement.md)
at source head `5558a6b22ef8eb080d198d4af6b1a5cfe2fb164f`, blob
`fda902b95247a9367c60a92c43ae3d0e8119ea49`, explicitly requires mean
one-half and `2||c-1/2||_W<1`. This verifies which hypothesis the FR
Rudin-Shapiro example claims to violate. PR39 is a scope comparator,
not a premise replacing the new FR proof. Broader novelty is unassessed.
