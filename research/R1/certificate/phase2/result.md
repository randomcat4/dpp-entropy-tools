# Phase-2 rational certificate stress result

Status: **PASS; no certificate logic bug found**.

The unchanged phase-1 verifier was replayed at logarithm-series term counts
`20,40,80,120,180` on the JSON cases in `tests/`. Final outcomes were:

| case | purpose | final outcome |
| --- | --- | --- |
| `near_spectrum_boundary_event_tiny` | strict endpoints, event mass down to `1e-8` | `CERTIFIED_NEGATIVE_GAP` |
| `ultra_small_event_high_denominator` | larger denominator, event mass down to `1e-12` | `CERTIFIED_NEGATIVE_GAP` |
| `large_denominator_zero_gap` | exact zero-gap control | `GAP_UNCERTAIN` at every term count |
| `unseparated_tiny_gap` | nonzero gap below the bounded interval resolution | `GAP_UNCERTAIN` at every term count |
| `endpoint_on_boundary_not_feasible` | endpoint on the strict boundary | `NOT_FEASIBLE` at every term count |
| `float_input_rejected` | non-rational JSON input | `INPUT_ERROR` |

For all feasible cases the verifier rebuilt complete DPP event probabilities
by determinant inclusion-exclusion, checked positivity and normalization, and
never treated principal minors as exact events. Gap interval widths strictly
decreased whenever a gap interval was produced. At 180 terms, the widths were
about `1.25e-174` to `1.91e-174` across the four feasible gap cases.

Two failed calibration attempts are part of the audit trail. Python's default
large-integer string limit first blocked high-term result serialization; direct
high-term replay therefore uses `-X int_max_str_digits=0`. Also, an initial
`1e-12` off-diagonal perturbation was not genuinely unseparated: the verifier
correctly certified it negative at higher terms. The retained test uses
`1e-50` and remains uncertain through the fixed budget.

Example direct replay from this directory:

```text
python -X int_max_str_digits=0 ../certify_real_chord.py tests/near_spectrum_boundary_event_tiny.json --terms 180 --out near_boundary_180.json
```

No positive-gap candidate was supplied or certified. These cases test the
verifier's strictness and conservative uncertainty behavior; they do not add
to the optimizer denominator.
