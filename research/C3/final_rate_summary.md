# One fixed nonradial chord: genuine rate exclusion

The coherent two-harmonic object C3-M1 is fixed independently of observation
length, with step 1/4 and uniform margin 1/200. Its exact trigonometric
coefficients are in rate/candidate_true_symbol.json. Three parameters and
six complement/extreme-past kernels were evaluated separately.

The following decimal intervals are rounded outward from the exact rational
endpoints in rate/artifacts/c3_m1_rate_n4.json, in nats:

| Process | Lower bound | Upper bound |
|---|---:|---:|
| f_- | 0.68855439608 | 0.68888363966 |
| f_0 | 0.68878627463 | 0.68915262970 |
| f_+ | 0.68784716972 | 0.68868722887 |

The true midpoint gap satisfies

    -0.000951846792 < (h(f_-)+h(f_+))/2-h(f_0) < -0.0000008403727.

The exact upper gate is

    -299855012916397501897282364769067397783
    /356811923176489970264571492362373784095686656 < 0.

Thus C3-M1 is rigorously excluded as a positive entropy-rate counterexample.
This uses n=4 only, 288 exact event determinants and a rational residual
enclosure, not an extrapolation. The finite n=8 phase diagnostic is separate.
The author's self-audit and the nonauthor audit have separate labels.
The nonauthor verdict is CORRECT_SCOPED; see verifications/fixed_rate.md.

The complete method and assumptions appear in rate/rate_analysis.md and
the certificate-theory supplement. The radial family theorem is independent
of this one-object exclusion.
