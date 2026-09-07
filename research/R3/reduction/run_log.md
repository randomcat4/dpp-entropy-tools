# Reduction run log

Status: `PROVED` for the author-level grouped exact-event reduction;
`INCOMPLETE` for a real counterexample, all-real coverage, or a closed T2
transfer. No fresh-context mathematical certification is claimed.

## Reproduction

The dependency-free implementation was reproduced in the isolated R3 remote
checkout with Python 3.12.3. It uses no NumPy, BLAS, OpenMP, or GPU code.

```text
python -m unittest discover -s research/R3/reduction/tests -v
```

The revised integrated suite has eight tests:

- `n=6`: 64 exact events versus 24 count states;
- near-boundary `n=8`: 256 exact events versus 81 count states;
- block-exchange `n=8`: 256 exact events versus 48 count states;
- compatible real chord gap against direct Möbius entropy;
- Jensen-gap interval sign convention.
- two nonconstant-`a_g` exact frozen-family checks at `n=8`, one near the
  spectral boundary, with direct Möbius, full L-ensemble, and reduced atoms.

All three exact-event implementations agree as rational numbers:

```text
direct Möbius atoms == full L-ensemble atoms == grouped count atoms
```

An additional reduced-only `n=12` smoke test represents 4096 events by 256
count states and has exact probability sum 1. It is a functionality check, not
a gap certificate.

Integrated remote reproduction: 6 tests passed in 0.352 seconds, exit code 0,
with all numerical thread caps set to one.

After the v1 verifier found the group-specific coverage mismatch, the revised
exact suite ran 8 tests in 0.429 seconds and, after adding a strict-positive
minimum-atom assertion, again ran 8 tests in 0.436 seconds. Both runs exited 0.

## Failure ledger

The first author-side entropy test compared high-precision Decimal sums for
literal equality. Exact atom probabilities already matched, but summation order
changed the last Decimal places. The test now retains exact rational equality
for atoms and uses a `1e-80` tolerance only for entropy accumulation.

No counterexample search was performed by this reduction task. The separate
structure search and main smoke run record their own complete denominators.
