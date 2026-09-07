# Test summary

Run from the repository root with Python 3.12 or later:

```text
python -m unittest discover -s research/R3/reduction/tests -v
```

The suite checks `n<=8` exact atoms by three independent routes:

```text
direct Mobius inversion
full L-ensemble formula
grouped count reduction
```

Covered cases:

* `n=6` random-like grouped low-rank strict contraction.
* `n=8` near-boundary strict contraction with a small atom.
* `n=8` standard-basis block-exchange structure.
* Compatible real-symmetric chord gap against direct Mobius entropy at both
  endpoints and the midpoint.
* Jensen-gap interval sign convention.
* Reduced-only `n=12` probability normalization: 256 count states represent
  4096 events and sum exactly to one.
* Two exact nonconstant-`a_g` frozen-family cases at `n=8`, including a
  near-boundary case. Direct Möbius, full L-ensemble, and reduced atoms agree
  exactly; orbit sizes sum to all 256 subsets.

The probability comparisons are exact rational equalities.  Entropy comparisons
use high-precision Decimal logs and a final-place tolerance, because identical
terms are accumulated in different orders.
