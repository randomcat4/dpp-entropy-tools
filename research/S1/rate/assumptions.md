# Assumptions and Source Facts

All logarithms are natural.  Entropy is the process entropy rate

```text
h(f) = H(X_0 | X_{-1}, X_{-2}, ...)
```

for the stationary DPP with Fourier kernel `K_f(i,j)=fhat(i-j)`.

The route uses these source facts from Lyons--Steif, *Stationary determinantal processes: phase multiplicity, Bernoullicity, entropy, and domination*, arXiv:math/0204324:

- Section 6 formula (6.5) expresses entropy rate as the integral of the binary entropy of the one-step prediction probability given the whole past.
- Section 6 uses negative association to squeeze prediction probabilities between all-one and all-zero past completions.
- Theorem 6.12 identifies the all-one extreme-past limit `nu_f` as a DPP on `N` whose kernel is built from the outer function `phi_f`.
- Conjecture 9.2 is the scalar entropy concavity target.

The route owner's source update was checked against the errata file hosted by Russell Lyons.  The errata entries mention only Remark 5.12 and Remark 7.16, not Theorem 6.12.

No random-order entropy representation is used here, so the Mészáros random-order hypotheses are not invoked.

For the benchmark, the uniform margin is exact by the triangle inequality:

```text
sum |a_k| = 19/50
tau sum |b_k| = 3/50
1/2 - 19/50 - 3/50 = 3/50.
```

The same margin applies to `1-f_t`.
