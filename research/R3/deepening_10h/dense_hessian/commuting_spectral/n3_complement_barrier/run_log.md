# Bounded analytic run log

Date: 2026-09-08. No random draws, seed: none. No server or GPU was used.
Only this task's assigned directory was written; no shared author files changed.

The initial script checked 34 rational cases and 3 chords, exit 0. It was then
extended with one explicitly chosen asymmetric interval center and twelve
whole-interval polynomial inequalities. No tested interval bound failed, and
no rejected parameter set is omitted. The final run is the frozen evidence
below; the preliminary output was superseded by the strictly extended output.

Run from the repository root:

```
python research/R3/deepening_10h/dense_hessian/commuting_spectral/n3_complement_barrier/sanity.py
```

The local bundled Python 3.12 executable was used. The script uses only the
standard library. It took 0.13928914070129395 seconds, exit code 0.

Final script SHA256:
`641cd7b8412babb8fc78d628dbdcbe228181ac20181f276de273ab43f17cb683`

Final `sanity_results.json` SHA256:
`54df0f345567a0d1e293f67d57572d9f31d79a8676af0741e14a8e6093f18ffc`

The JSON records all 35 parameter sets as exact fractions, direction ranks,
matrices K/D/P, all event cubic coefficients, decomposition components,
probability margins, all 12 interval constraints with their exact lower bounds,
and all 3 chord enclosures with exact denominators. The interval certificate
uses h=1/20; its smallest polynomial lower bound is 3133489/37800000 > 0.
All eigenvalues on that interval have distance at least 19/100 from {0,1}.

There are 31 uniform-layer cases, 3 identity-only general cases, and one new
asymmetric center. All 280 events match direct Mobius inversion coefficientwise
(1120 scalar coefficients). Fisher SOS and complement jets are checked exactly.
The event and layer curvature expressions match to better than 1e-65 at
80-digit Decimal precision. Paired L1 inequalities are exact rational checks.

The three chord steps are 1/100, 1/1000, 1/10000 at the symmetry-breaking
direction of equation (12), not equation (19). Their gaps are enclosed strictly
below zero using rational logarithm series with explicit tails. Equation (19)
is instead certified on its complete interval by the twelve inequalities and
the analytic subclass theorem candidate. These are separate forms of evidence.

Full denominators in the JSON are part of the evidence: no float-only summary
stands in for parameter data. The positive-total-curvature count is computed
from the 35 case barriers, not hardcoded; it is zero. This finite denominator
does not establish any global concavity statement.
