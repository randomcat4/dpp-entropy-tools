# D10-H14 / round22_interior4 non-author audit verdict

STATUS: CORRECT for frozen-data accounting and the strongest-point
independent gate.

STATUS: SCOUT for the 20,000-proposal finite profile.  Nothing here proves a
global theorem, a monotonicity statement, or a universal upper bound.

## Summary

I did not import the author recheck, search, or gate code.  The audit script
rebuilds all exact-event probabilities from inclusion determinants by Mobius
inversion, using standard-library `Decimal` precision 130 for the strongest
point.  `numpy` is used only to read NPZ arrays and for non-certifying float
diagnostics.

## Ledger / manifest / log accounting

- Four shards are present.
- Each shard has one source row and `5000` proposal rows.
- Total ledger rows: `20004 = 4*(1+5000)`.
- Proposal rows: `20000`.
- Source rows: `4`.
- Every stored status is `NO_HIT`.
- Rows with `rho_psd > 1`: `0`.
- Rows with `rho_psd >= 1`: `0`.
- Rows with positive stored chord gap: `0`.
- Largest stored chord gap: `-0.0005372634769749141`.
- All four manifests have `exit_code=0`, `positive_count=0`, and match the
  final JSON line of the corresponding run log.

The `0.20` margin floor is consistent after allowing ordinary binary-float
rounding.  The minimum stored proposal margin is
`0.19999999999999996`; `15637` proposal rows are below literal decimal `0.2`,
but `0` rows are below `0.2 - 1e-14`.

## Strongest row and NPZ consistency

The strongest row is exactly the README row:

```text
shard = 0
index = 2996
label = spectrum_local
rho_psd = 0.3337720601402677
spectrum_margin = 0.19999999999999996
stored chord_gap = -0.0022830056643865504
```

The shard-0 `best_case.json` matches this row.  The strongest NPZ hash matches
the README hash:

```text
8c62a7236a613640f0d76f3cedc1899825d63e60a33ca9c49beba4f8754a822b
```

The source NPZ hash also matches the README hash:

```text
b5972686e06976da1ac5e8dc3dcef2090fdd010e2586520ee69836a25ee684cf
```

For the strongest NPZ:

```text
basis orthogonality Frobenius residual = 5.761509752873713e-15
kernel reconstruction Frobenius residual = 9.83146017049016e-17
direction reconstruction Frobenius residual = 1.2423311334055413e-16
commutator Frobenius residual = 2.242389620371037e-15
spectrum min/max = 0.2 / 0.8
rate min/max = 0.914840902309305 / 1.0
```

Thus the stored strongest point is a fixed-`Q` spectral-rate affine line to
float precision, and the stored direction is PSD.

## Independent exact-event directional gate

For the strongest NPZ, rebuilt from `4096` exact events:

```text
Fisher       = 68.528987144383324921438750917243870808477011022689621833639943...
acceleration = 22.873061218506751590011200240145406140658471976954720643681521...
H''          = -45.655925925876573331427550677098464667818539045734901189958421...
rho          = 0.333772060140267822448344604861706337501459353828357942602040168...
min atom     = 0.000016802845760849606674591057669477430631057197677391869916232...
```

Mass and jet checks are at Decimal roundoff scale:

```text
sum p - 1 = -2e-130
sum p'    = -8.6898e-129
sum p''   = -2.190e-128
```

Four actual midpoint chords are negative, including both the ledger `0.01`
step and the requested `1/200` step:

| step | midpoint gap | central second difference |
| --- | ---: | ---: |
| `1/100` | `-0.0022830056643846498...` | `-45.660113287692996...` |
| `1/200` | `-0.00057071215509361918...` | `-45.656972407489534...` |
| `1/1000` | `-0.000022827983890276199...` | `-45.655967780552398...` |
| `1/10000` | `-0.000000228279631722107...` | `-45.655926344421439...` |

## Fraction LDL feasibility gate

Interpreting the stored float64 matrices as exact binary rationals after exact
symmetrization:

- `D` is positive definite by Fraction LDL; minimum pivot float
  `0.946123235197052`.
- For `t=-1/200`, both `K(t)-I/2000` and `I-K(t)-I/2000` are positive by
  Fraction LDL; minimum pivot floats are `0.30144506026909745` and
  `0.3400056912760936`.
- For `t=+1/200`, both `K(t)-I/2000` and `I-K(t)-I/2000` are positive by
  Fraction LDL; minimum pivot floats are `0.31410057506718897` and
  `0.32681211490995016`.

This certifies the requested strict feasibility margin for the stored strongest
small affine chord.

## H10--H14 profile check

The README profile is consistent as finite evidence:

| batch | best margin | best rho |
| --- | ---: | ---: |
| H10 round18 boundary1 | `0.015371444079016916` | `0.5746069386526107` |
| H11 round19 interior1 | `0.02171078114876157` | `0.5745947308664667` |
| H12 round20 interior2 | `0.05` | `0.5729410207438331` |
| H13 round21 interior3 | `0.09999999999999998` | `0.5313886643536545` |
| H14 round22 interior4 | `0.19999999999999996` | `0.3337720601402677` |

The statement “the best ratio falls from about `0.5314` at margin `0.10` to
about `0.3338` at margin `0.20`” is supported by the frozen H13/H14 READMEs.
The broader H10--H14 wording should remain finite-profile language only.

## Final layered verdict

- Copied-output accounting: CORRECT.
- Strongest-row identity and hashes: CORRECT.
- Fixed-`Q` PSD spectral-rate line semantics: CORRECT to stored float precision.
- Independent 130-precision exact-event/Mobius Fisher/acceleration/H''/rho gate:
  CORRECT.
- Four actual chord checks: CORRECT, all negative.
- Fraction LDL `D>0` and `|t|<=1/200` feasibility with `1/2000` margin:
  CORRECT.
- H10--H14 profile wording: CORRECT as finite SCOUT evidence only.
- Any global or monotonic theorem inferred from this finite batch: NOT PROVED.
