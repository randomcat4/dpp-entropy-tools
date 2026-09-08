# D10-U10c Decimal-jet repair

STATUS: REPAIRED_AND_REGENERATED / FRESH_REVIEWED_SCOUT.

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
authored the scout, so it remains labelled an internal repair audit. A second,
fresh non-author implementation under `fresh_repair_audit/` rebuilt 445
high-precision attempts: 444 strict valid kernels, one exact non-strict
rejection, and zero `rho>1`. It also corrected two prose counters: there are 69
near-threshold records, while 15 top-float rows means 15 attempts and 14 valid
rechecks. The full 38,436-row float trajectories were compact-accounted but not
independently regenerated. The result remains `SCOUT`; no theorem depends on
this ledger.
