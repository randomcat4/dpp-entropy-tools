# Round 15 third corrected joint refinement

STATUS: `CORRECT` for copied-data accounting and the frozen strongest-point
gate, `SCOUT` for the finite 20,000-proposal run, and `INCOMPLETE` for a full
seed replay or any continuous/global conclusion.  A fresh non-author audit is
preserved under `verifications/`.

## Scope and accounting

This is a third joint basis/spectrum refinement, started from the verified
round-14 strongest point.  The producing script is the already preflighted
corrected version: each of four one-thread shards records one source row with
`index=-1` followed by 5,000 new proposal rows.  The aggregate therefore has
20,004 stored rows but exactly 20,000 new proposals.

At each accepted center the direction is a positive spectral-rate direction
in a fixed numerical eigenbasis.  Between centers the outer heuristic perturbs
the spectrum and makes small Givens rotations of the eigenbasis.

## Float scout result

- new proposals: `20000`
- ledger rows including four repeated source copies: `20004`
- non-`NO_HIT` rows: `0`
- positive stored midpoint gaps: `0`
- largest stored midpoint gap: `-6.0892895073827447e-05`
- strongest mechanism ratio: `rho=0.5725909000830567`
- strongest row: shard 0, seed `2026090848`, index 4942,
  `three_basis_rotations`
- strongest stored-step gap: `-0.0002264422099376162`

The diagnostic record moves only slightly from `0.5715405` to `0.5725909`.
The sign-change threshold is still `rho>1`.

## Author-side strongest-point gate

The author-side 80-decimal-digit exact-event/Mobius calculation gives

```text
Fisher       = 106.165006155608855332996241872586988965209147774243...
acceleration = 60.789116431963325540364472731878046802811386939317...
H''          = -45.375889723645529792631769140708942162397760834925...
rho          = 0.572590900083056661856638550203110451067306462560...
```

The actual high-precision midpoint gaps are negative at the stored step,
`0.001`, and `0.0001`.  Exact rational LDL on the symmetrized decimal entries
proves the direction positive definite and proves both `K(t)` and `I-K(t)`
retain margin `1/2000` throughout `|t|<=1/200`.

The producing float construction is fixed-Q at each center.  Entrywise decimal
rationalization does not preserve exact commutation, so the strict rational
certificate concerns a near-commuting PSD K-affine line, not an exactly
commuting rational line.

A fresh non-author implementation did not import the author gate or search
modules.  It independently rebuilt all 4,096 exact atoms at 90 digits,
reproduced the negative `H''`, subunit `rho`, three negative chords and
Fraction LDL certificate, and checked every stored ledger row, manifest,
best JSON/NPZ pair, accepted count, index and log.  Full regeneration of the
20,000 proposals from their seeds was not repeated.

## Integrity

- source NPZ SHA-256:
  `32741ce56d53b0c3637172d1805b7810990616e6ff90ae0c94509787fdd521ef`
- strongest NPZ SHA-256:
  `21bcb4d8867b2f7d32ee398432dfaa6f2d91976a4a959191d2da4d112153eb71`
- producing script SHA-256:
  `28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268`

All copied files matched the producing hashes before the exact remote
temporary directory was removed.  `recheck_best_refine3.py` reuses the
corrected ledger and high-precision gate implementation from round 14 against
this new frozen directory.  The separate non-author implementation is under
`verifications/`; both certify only the stated stored scout and strongest
point, not the continuous parameter space.
