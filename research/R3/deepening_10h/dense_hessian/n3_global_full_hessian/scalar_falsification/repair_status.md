# D10-U10c Decimal-jet repair

STATUS: REPAIRED_AND_REGENERATED / FRESH_REVIEW_PENDING.

An internal audit found that the Decimal empty-atom first jet used `-1` in all
six observation coordinates. Only the three diagonal coordinates should
contain that term. The float scout was unaffected, but the original Decimal
candidate values were invalid.

The implementation now uses `(-1,-1,-1,0,0,0)`. A complete deterministic
rerun again accounted for 38,436 float attempts, 22,023 accepted strict
connected kernels, 15 top-float high-precision rechecks, 280 boundary probes,
and 150 near-`Lambda=0` path probes. It found zero corrected `rho>1` values.
The corrected best Decimal value is

```text
rho = 0.99509994460201969229112579538559592802...
```

The audit that exposed the bug was performed by the same agent context that
authored the scout, so it is correctly labelled an internal repair audit. A
fresh non-author recheck remains required before promoting the repaired finite
ledger from `SCOUT` to audited finite evidence. No theorem depends on this
ledger.
