# R1 certificate verifier

This subdirectory contains the exact rational verifier for real-symmetric DPP
entropy chords.

Run:

```bash
python certify_real_chord.py tests/negative_gap.json --out logs/negative_gap.json
```

Input accepts either matrices of rational strings, or `{K,V}_denominator` plus
`{K,V}_numerators`. Floating-point values are rejected.

The verifier:

- checks K0 and V are real symmetric;
- checks `0 < K0 +- tV < I` using leading principal minors of each endpoint and
  its complement;
- rebuilds all exact event probabilities as `(-1)^|S^c| det(K-I[S^c])`;
- bounds the midpoint entropy gap with rational logarithm intervals.

No positive real-symmetric candidate is certified in this package. The verifier
is ready to evaluate one if supplied as rational JSON.
