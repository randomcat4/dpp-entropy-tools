# Round 18 lowered-margin boundary diagnostic

STATUS: `CORRECT` for copied-data accounting, the strongest-point gate, and
the stated finite boundary comparison; `SCOUT` for the finite 20,000-proposal
run; `INCOMPLETE` for a full seed replay or any continuous/global claim.  A
fresh non-author audit is preserved under `verifications/`.

## Scope and accounting

This run starts from the audited round-17 strongest point but lowers the
configured spectrum-margin floor from `0.01` to `0.002`.  Its purpose is to
separate genuine local mechanism improvement from an artifact caused by
forcing every accepted center against the previous margin floor.

Each of four single-thread shards records one source row with `index=-1` and
5,000 new proposal rows.  The aggregate has 20,004 stored rows and exactly
20,000 new proposals.

## Float scout result

- new proposals: `20000`
- ledger rows including four repeated source copies: `20004`
- non-`NO_HIT` rows: `0`
- positive stored midpoint gaps: `0`
- largest stored midpoint gap: `-3.82980532620536e-06`
- strongest mechanism ratio: `rho=0.5746069386526107`
- strongest row: shard 2, seed `2026090862`, index 4877,
  `one_basis_rotation`
- strongest stored-step gap: `-0.00024511575569174937`
- strongest stored spectrum margin: `0.015371444079016916`

The source had `rho=0.5740468373613397` and a recorded margin at the old
`0.01` floor.  The new strongest point improves the ratio slightly while
moving *farther inside* to margin `0.01537...`, even though this run permits
margin down to `0.002`.  Thus this frozen finite comparison does not support
the hypothesis that the recent ratio gains are merely caused by approaching
the spectral boundary.  It does not rule out other boundary mechanisms or
replace a theorem.

The deterministic `margin_profile.py` split all 20,000 proposals by recorded
margin.  The best ratios in `[0.002,0.005)`, `[0.005,0.01)`, `[0.01,0.02)`,
and `[0.02,0.05)` are respectively `0.5736420`, `0.5743571`, `0.5746069`,
and `0.5735366`.  This non-monotone frozen profile is the finite evidence
behind the boundary statement.

## Author-side strongest-point gate

The author-side 80-decimal-digit exact-event/Mobius calculation gives

```text
Fisher       = 94.677742786438956010505518587502216169626954176266...
acceleration = 54.402487941054958003060539777512663664268921912127...
H''          = -40.275254845383998007444978809989552505358032264139...
rho          = 0.574606938652610420860153274958863675661506723233...
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
  `6a4fb8bd1790fbe17dbb58fac96a5ee3585bf7aac9c8f395608478b58750a978`
- strongest NPZ SHA-256:
  `b923193115a21585351db4350a4da53a622c937f1789d557fbbcd57a1e13b59c`
- producing script SHA-256:
  `28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268`

All 24 copied files matched their source SHA-256 values before the exact
temporary working directory was removed.  `recheck_best_boundary1.py` reuses
the corrected author gate implementation.  A fresh non-author implementation
did not import that gate or the search modules.  It independently checked all
stored rows and files, rebuilt the strongest point from 4,096 exact events at
120 digits, repeated all three chords and Fraction-LDL checks, and recomputed
the 20,000-row margin profile.  Full regeneration of the seed proposals was
not performed.
