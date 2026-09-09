# Sources and prior-art audit

## Sources actually checked

1. Russell Lyons and Jeffrey E. Steif, *Stationary Determinantal Processes:
   Phase Multiplicity, Bernoullicity, Entropy, and Domination*, arXiv v5,
   23 January 2003. [Original paper](https://arxiv.org/pdf/math/0204324).
   Section 9, Conjecture 9.2, printed p.53 fixes the scalar entropy-rate
   target. Section 6, (6.5), Proposition 6.10 and Theorem 6.12, pp.34–37
   provide the conditioning framework used by the separate numerical-rate
   route. These statements do not assert radial parameter concavity.
   The present theorem uses finite Jensen inequalities and stationarity;
   it does not need outer factors or differentiability of the entropy rate.

2. Andras Meszaros, *Limiting entropy of determinantal processes*, 2020
   version. [Original paper](https://arxiv.org/pdf/1905.11459).
   Sections 2.6–2.7, especially Theorems 2.5 and 2.6, pp.7–9 were checked.
   The random-order conditional entropy representation is adjacent work.
   The projection/tightness requirements of Theorem 2.5 are not silently
   applied to arbitrary varying contractions. It supplies no parameter
   curvature sign used here; it is not a dependency of proof.md.

3. [Source public PR 22](https://github.com/randomcat4/dpp-entropy-tools/pull/22),
   head 60645b4ea9e3f3a79d842b6fe039a33f9daaf7df. Its tree
   5ed568031bb26ef6bbb99382fa5907582f8f1c40 equals the read-only local source.
   The S1 round-two verdict/checkpoint/provenance, rate proof and nonauthor
   audit were read. Its strict certificate is for its own three symbols;
   none of those numeric intervals is transferred to C3's new candidate.

## Novelty search and limits

Original-source searches used combinations of determinantal entropy,
radial concavity, diagonal interpolation, independent replacement,
resampling, product channels, Jeffreys divergence, noise-parameter entropy,
and heat-flow concavity. The accessible results mostly concerned count
entropy under thinning, quantum entropy, or other channel parameterizations.
None of these is a justified substitute for the full-configuration theorem.

The source checkout's prior radial results inspected here are local
fourth-order statements near diagonal kernels; its fixed-block theorem is
entropy maximization at decoupling, not curvature along the whole ray.
This comparison only describes the inspected repository material.

**Novelty is unconfirmed.** Failure to locate the same elementary
product-channel argument is not evidence that it is absent from the
literature. The theorem is not submitted here as a priority claim or as a
paper-core contribution. The finite proof re-establishes all information
inequalities on which it relies.
