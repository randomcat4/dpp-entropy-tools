# Round 14 corrected joint refinement

STATUS: `CORRECT` for copied-data accounting and the frozen strongest-point
gate, `SCOUT` for the finite 20,000-proposal run, and `INCOMPLETE` for a full
seed replay or any continuous/global concavity claim.  A fresh non-author
audit is preserved under `verifications/`.

## Scope and corrected accounting

This run starts from the verified round-13 strongest point.  Four independent
one-thread shards each made 5,000 new proposals.  Between centers the search
perturbs the spectrum and applies small Givens rotations to the eigenbasis;
at each accepted center it optimizes a positive spectral-rate direction in a
fixed numerical eigenbasis.

The corrected producing script writes the source/base point as `index=-1` and
then all 5,000 proposals.  Thus each CSV has 5,001 rows, while the actual new
proposal denominator is still 5,000 per shard and 20,000 total.  The four
source rows are repeated bookkeeping copies of the same starting point, not
four additional proposals.

## Float scout result

- new proposals: `20000`
- ledger rows including four source copies: `20004`
- non-`NO_HIT` rows: `0`
- positive stored midpoint gaps: `0`
- largest stored midpoint gap: `-6.165970208549254e-05`
- strongest mechanism ratio: `rho=0.5715404864746153`
- strongest row: shard 2, seed `2026090846`, index 4998,
  `three_basis_rotations`
- strongest stored-step gap: `-0.00019844664425683334`

This improves the diagnostic record from about `0.56859` to `0.57154` but
does not approach the sign-change criterion in a theorem-like sense: the
counterexample threshold is still `rho>1`, and the outer center search is
finite and heuristic.

## Author-side strongest-point gate

The author-side 80-decimal-digit exact-event/Mobius calculation gives

```text
Fisher       = 68.111970180326072147483496340076407197405292811844...
acceleration = 38.928748571607984337299345935614395089291059275995...
H''          = -29.183221608718087810184150404462012108114233535849...
rho          = 0.571540486474614276140746429134937786566306363104...
```

The actual high-precision midpoint gaps are negative at the stored step,
`0.001`, and `0.0001`.  Exact rational LDL on the symmetrized decimal entries
proves the direction positive definite and proves both `K(t)` and
`I-K(t)` retain margin `1/2000` throughout `|t|<=1/200`.

As in the preceding rounds, the floating construction uses one numerical
eigenbasis at each frozen center, but entrywise decimal rationalization of the
symmetrized matrices does not preserve exact commutation.  The exact
feasibility and entropy certificate therefore applies to a near-commuting PSD
K-affine line, not an exactly commuting rational line.

A fresh non-author implementation did not import the author gate or search
modules.  It independently recomputed all 4,096 exact atoms at 90 decimal
digits, reproduced the displayed negative `H''` and subunit `rho`, obtained
the same three negative chords, and rebuilt the Fraction LDL certificate.  It
also checked every stored ledger row, the complete proposal indices, all best
JSON/NPZ pairs, accepted counts, manifests and logs.  Full regeneration of the
20,000 proposals from their seeds was not repeated, so that extra replay layer
remains explicitly `INCOMPLETE`.

## Integrity

- source NPZ SHA-256:
  `4bda0a82ca642b5e804bca498107a89a1c81a3a7eb79ce6aca2712e4d594cb72`
- strongest NPZ SHA-256:
  `32741ce56d53b0c3637172d1805b7810990616e6ff90ae0c94509787fdd521ef`
- producing script SHA-256:
  `28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268`

All copied data, manifests, logs and scripts matched the producing hashes
before the exact remote temporary directory was removed.  `recheck_best_refine2.py`
and its JSON are the author-side gate; `verifications/fresh_audit.md` and its
script/JSON are the independent audit.  These certify the stated finite ledger
and strongest point, not the unexplored continuous parameter space.
