# Ready batch 02: two separate C3 claims

Frozen input for both units: PR29 commit
`648f1906468e3e548410f98a6b1a53a978f2ea11`, `research/C3/`.

## A. Radial theorem: ACCEPTED_SCOPED

For an interior diagonal finite kernel B and arbitrary fixed Hermitian A,
the complete configuration entropy `H(B+tA)` is concave on its full
feasible interval. Consequently, for `0<p<1` and bounded measurable real
g, the scalar stationary true entropy rate of `p+t g` is concave on its
legal interval. Boundary values, diagonal changes, noncommuting finite
directions, complex Toeplitz compressions and nonzero mean g are included.

[The fresh nonauthor proof review](children/c3/review_radial_theorem.md)
checks the exact product-replacement DPP identification, bidirectional KL
contraction, entrywise mixed derivatives without a PSD inference, gluing
of the two rays, and passage to three pointwise finite-block entropy
limits. It does not certify arbitrary chords, the full entropy conjecture,
or novelty.

## B. Fixed C3-M1 rate certificate: ACCEPTED_SCOPED

The exact certificate establishes only the fixed three-symbol statement
`(h(f_-)+h(f_+))/2-h(f_0)<0` for the displayed C3-M1 object. In particular,
this is not a positive counterexample or a family concavity theorem.

[The separate certificate review](children/c3/review_rate_certificate.md)
checks the operator residual bound, conditional-probability error bound,
extreme-boundary conditioning theorem and actual infinite-past entropy
enclosure. The fixed server replay used `M=64`, `bits=160`, `n=4`, one
numerical thread and no GPU: six boundary cases, 66 residual rows per case,
and 288 exact event determinants. A separately implemented permutation
determinant check reproduced all 288 events.

The pair-gap upper endpoint is the exact negative rational

```
-299855012916397501897282364769067397783
/356811923176489970264571492362373784095686656
```

The author replay scripts and fixed inputs, replay outputs, independent
reviewer checker, complete logs, PIDs, versions and exit records are in
`children/c3/compute_replay/`. The first invocation of the new reviewer
checker had a Python generator-parenthesization syntax error; its failed
log is preserved. After that syntax fix, PID 167561 exited 0 and reported
`REVIEWER_CHECK_PASS`. The author boundary/rate/audit replay steps each
exited 0. No enlarged window, precision search or random scan was used.

## Nonblocking documentation correction

`rate/candidate.json:6` describes the sign conversion as giving a
conjugate-transpose kernel. Direct substitution into the actual declared
script convention instead gives exactly the true Fourier coefficients
at all three parameter values. `rate_analysis.md:130` already says this
correctly. The certificate is unaffected; clarify this sentence when
editing the author artifact. The frozen author sources are retained
without alteration here.

These are independent scoped acceptances. W1 R2 and W4 remain separate
pending units, and C1's own PR30 is excluded. Only the designated
integrator may merge to main.
