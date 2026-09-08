# Round 17 fifth corrected joint refinement

STATUS: `CORRECT` for copied-data accounting and the strongest-point gate,
`SCOUT` for the finite 20,000-proposal run, and `INCOMPLETE` for a full seed
replay or any continuous/global claim.  A fresh non-author audit is preserved
under `verifications/`.

## Scope and accounting

The fifth joint basis/spectrum refinement starts from the audited round-16
strongest point.  Each of four single-thread shards records one source row
with `index=-1` and 5,000 new proposal rows.  The aggregate has 20,004 stored
rows and exactly 20,000 new proposals.

At each accepted center the direction is a positive spectral-rate direction
in a fixed numerical eigenbasis.  The outer heuristic perturbs the spectrum
and makes small Givens rotations of that basis.

## Float scout result

- new proposals: `20000`
- ledger rows including four repeated source copies: `20004`
- non-`NO_HIT` rows: `0`
- positive stored midpoint gaps: `0`
- largest stored midpoint gap: `-4.784058084528198e-05`
- strongest mechanism ratio: `rho=0.5740468373613397`
- strongest row: shard 1, seed `2026090857`, index 4910,
  `three_basis_rotations`
- strongest stored-step gap: `-0.00011880571419009556`

The change from `0.5735840` to `0.5740468` is small, and the strongest point
has reached the configured spectrum-margin floor (`0.01` to float precision).
The sign-change threshold remains `rho>1`.

## Author-side strongest-point gate

The author-side 80-decimal-digit exact-event/Mobius calculation gives

```text
Fisher       = 92.475543357579610884391186838951338228649988385009...
acceleration = 53.085293197689981244584356006329512209098307171112...
H''          = -39.390250159889629639806830832621826019551681213897...
rho          = 0.574046837361339273363350413246429601594117915921...
```

The high-precision midpoint gaps are negative at the stored step, `0.001`,
and `0.0001`.  Exact rational LDL on symmetrized decimal entries proves the
direction positive definite and proves `K(t)` and `I-K(t)` retain margin
`1/2000` throughout `|t|<=1/200`.

The float construction is fixed-Q at each center.  Entrywise rationalization
does not preserve exact commutation, so the strict rational certificate is for
a near-commuting PSD K-affine line, not an exactly commuting rational line.

## Integrity

- source NPZ SHA-256:
  `b078c507558faa74b2a583581bfc5b51859009dafd12e6c2b95e6e25cad0b5a2`
- strongest NPZ SHA-256:
  `6a4fb8bd1790fbe17dbb58fac96a5ee3585bf7aac9c8f395608478b58750a978`
- producing script SHA-256:
  `28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268`

All copied files matched their remote SHA-256 values before the exact remote
temporary directory was removed.  `recheck_best_refine5.py` reuses the
corrected ledger/high-precision implementation from round 14.  A fresh
non-author implementation did not import the author gate or search modules.
It independently checked all stored rows and files, rebuilt all 4,096 exact
atoms at 95 decimal digits, reproduced the negative curvature and three
chords, and repeated the Fraction LDL certificate.  Full regeneration of the
20,000 seed proposals was not performed.  The audit also confirmed that the
configured `0.01` spectrum-margin floor is active for the strongest stored
point, while the point itself remains strictly feasible.
