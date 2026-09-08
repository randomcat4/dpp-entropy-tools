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
recorded below.  General strict connected `3 x 3` concavity remains open.

## Commit-bound public review

The public consolidation and exact script were frozen in:

```text
commit 6b73114abc6bc262cc1f5b11413782c69c696627
tree   87676276f50617c83d6b7e427d238b164dcbc9e1

proof blob  4453c18a9ae5904f543ed1efe96024db31742223
script blob 2467b2367d5075f16c44f56c5cd66a43f7ec7ccf
```

Two independent contexts used only `git show` on these fixed objects.  Both
returned `STATUS: CORRECT`, confirmed that the public proof preserved the
complete uniform analytic argument and its scope limitations, and replayed
the script blob with the two `PASS` lines above and exit code `0`.  Neither
read a same-named working-tree file or modified repository contents.
