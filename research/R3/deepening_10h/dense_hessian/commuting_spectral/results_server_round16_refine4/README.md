# Round 16 fourth corrected joint refinement

STATUS: `CORRECT` for copied-data accounting and the strongest-point gate,
`SCOUT` for the finite 20,000-proposal run, and `INCOMPLETE` for a full seed
replay or any continuous/global claim.  A fresh non-author audit is preserved
under `verifications/`.

## Scope and accounting

This fourth joint basis/spectrum refinement starts from the verified round-15
strongest point.  The already preflighted corrected script records one source
row with `index=-1` followed by 5,000 new proposal rows in each of four
single-thread shards.  The aggregate has 20,004 stored rows and exactly 20,000
new proposals.

At each accepted center the direction is a positive spectral-rate direction
in a fixed numerical eigenbasis.  Between centers the heuristic perturbs the
spectrum and makes small Givens rotations of that basis.

## Float scout result

- new proposals: `20000`
- ledger rows including four repeated source copies: `20004`
- non-`NO_HIT` rows: `0`
- positive stored midpoint gaps: `0`
- largest stored midpoint gap: `-4.517140952842169e-05`
- strongest mechanism ratio: `rho=0.5735840441822098`
- strongest row: shard 2, seed `2026090854`, index 4889,
  `one_basis_rotation`
- strongest stored-step gap: `-0.00013433371724325127`

The diagnostic record moves only from `0.5725909` to `0.5735840`; the sign
change threshold remains `rho>1`.

## Author-side strongest-point gate

The author-side 80-decimal-digit exact-event/Mobius calculation gives

```text
Fisher       = 98.944096994035071725142002119995626023663868674830...
acceleration = 56.752755301795356467055173823368176893591374381027...
H''          = -42.191341692239715258086828296627449130072494293803...
rho          = 0.573584044182208708723725374457821643297675469047...
```

The actual high-precision midpoint gaps are negative at the stored step,
`0.001`, and `0.0001`.  Exact rational LDL on symmetrized decimal entries
proves the direction positive definite and proves both `K(t)` and `I-K(t)`
retain margin `1/2000` throughout `|t|<=1/200`.

The float construction is fixed-Q at each center.  Entrywise decimal
rationalization need not preserve exact commutation, so the strict rational
certificate concerns a near-commuting PSD K-affine line, not an exactly
commuting rational line.

## Integrity

- source NPZ SHA-256:
  `21bcb4d8867b2f7d32ee398432dfaa6f2d91976a4a959191d2da4d112153eb71`
- strongest NPZ SHA-256:
  `b078c507558faa74b2a583581bfc5b51859009dafd12e6c2b95e6e25cad0b5a2`
- producing script SHA-256:
  `28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268`

All copied files matched their remote SHA-256 values before the exact remote
temporary directory was removed.  `recheck_best_refine4.py` reuses the
corrected ledger and high-precision implementation from round 14 against this
new frozen directory.  A fresh non-author implementation did not import the
author gate or search modules.  It independently checked all stored rows and
files, rebuilt the 4,096 exact atoms at 90 digits, reproduced the negative
curvature and three chords, and repeated the Fraction LDL certificate.  Full
regeneration of the 20,000 seed proposals was not performed.
