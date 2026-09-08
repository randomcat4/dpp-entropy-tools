# Non-author reviews: product-diagonal neighborhood theorem

The detailed private candidate and exact script were reviewed under hashes

```text
candidate A1B958AD88244093AB757628B12653524AA548B31CE6F3A60E17093F19CDA139
script    4CA49010FB6CB96D6D1B4C9D3CE74DE7E5DDEEBDF322BCA4149766DF3D346A39
```

Two independent contexts that did not author the proof returned `CORRECT`.
Both audited the load-bearing analytic argument rather than relying on the
finite exact script.

The first reviewer checked the complete-event density, entropy expansion,
single-edge cross-block cancellation, sign-parity and support classification
of every analytic remainder monomial, anisotropic weights, absolute-convergent
summation, sextic mixed-term absorption, diagonal/off-diagonal Young estimate,
graph-stratum kernels, and strict chord integration.

The second reviewer independently checked the same points, with special
attention to uniformity in the compact diagonal cube and to edge ratios that
approach zero arbitrarily fast.  It confirmed that the weights
`x^2+y^2z^2` and cyclic variants cover both axis and path degeneracies without
division by a vanishing weight.

Both exact-script replays exited `0` with:

```text
PASS: all 8 Mobius full-event polynomials and probability mass
PASS: exact degree 4, 6, 7 entropy coefficients; degree 5 is zero
```

The public proof `proofs/diagonal_perturbation_neighborhood.md` is a
consolidation of the reviewed candidate.  Its fixed commit-bound review is
recorded after the freeze commit.  General strict connected `3 x 3` concavity
remains open.
