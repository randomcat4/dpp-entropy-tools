# D10-H15 / round23_interior5 fresh audit

STATUS: SCOUT_CORRECT.

This is only a finite batch audit.  It does not prove monotonicity, a global
upper bound, or any theorem about all commuting-spectral directions.

No author `recheck`, `search`, or `gate` module was imported or called.  The
strongest point was recomputed from exact-event Möbius semantics and determinant
jets in a separate implementation.

## Ledger audit

The four CSV ledgers are internally consistent:

```text
global rows      = 20004
proposal rows    = 20000
source rows      = 4
per shard rows   = 5001
per shard source = 1
```

All proposal indices are exactly `0..4999` in each shard.  Manifest
`accepted_count`, `proposal_count`, `positive_count`, and `exit_code` match the
CSV-derived counts.

Checks passed:

```text
rho_psd >= 1 rows        = 0
positive chord_gap rows  = 0
non-NO_HIT status rows   = 0
proposal margin floor    >= 0.30
source margin            >= 0.32 up to roundoff
```

The CSV-best row is shard `3`, index `2902`, matching `results_3/best_case.json`:

```text
rho_psd                 = 0.15219460446316677
rho_unrestricted        = 0.15219460446316677
status                  = NO_HIT
label                   = three_basis_rotations
spectrum_margin         = 0.3
chord_gap               = -0.002210298455002757
```

The strongest NPZ hash matches the author recheck JSON:

```text
results_3/best_case.npz = fe3dff3b540eb110677268005b5b919b0b0ea89d30f5c4e65baca528ed1a4ff9
```

The source NPZ hash also matches:

```text
interior_source_margin032.npz = 57f08bf9d9abffe23d98d5dbbdd6e3d22026b402f5a7848a4469b70a8b0efcd7
```

## Strongest NPZ structural checks

For the symmetrized stored strongest point:

```text
K_min                = 0.29999999999999966
K_max                = 0.7000000000000015
K spectral margin    = 0.2999999999999985
D_min                = 0.8357649983491937
D_max                = 0.9999999999999992
commutator Frobenius = 1.2006247884730072e-15
basis residual       = 5.347244700248479e-15
```

Thus the stored point is a fixed-Q/near-commuting spectral-rate scout point in
the intended central spectral box.

## 130-digit exact-event/Möbius recomputation

Using all `4096` exact atoms with Möbius inversion of inclusion determinants
and independent determinant derivative formulas, the audit obtains:

```text
fisher       = 52.13829689246824596440687414564032651961650627323514020145353066540073702077041829457835711061329781944774374209772340569694152788
acceleration = 7.935167472932357511910400508044875854160558074817447559920194036060087896589622754074188323768081134001816333036182075386820188448
H''          = -44.20312941953588845249647363759545066545594819841769264153333662934064912418079554050416878684521668544592740906154133031012133943
rho          = 0.1521946044631666869477540561195882218460031201237051576063299975224730265837585706520416126381912789023459946884652833029537655577
min atom     = 0.0000833772362224885015758662624917328170887888111251616788067776514227888714829661399173300983051450312716105710402748624942358917214
```

Normalization residuals are at Decimal roundoff:

```text
sum p - 1 = 1e-129
sum p'    = 1.490e-129
sum p''   = -1.690e-128
```

The recomputed rho and `H''` match the author high-precision record to the
requested precision scale.

## Chord checks

Three independent high-precision entropy chords are negative:

```text
h=0.01    midpoint gap = -0.0022102984550019877496964109659499349519488945596222505842500106069364751404974351361647787027686242056625789788770403160985
h=0.001   midpoint gap = -0.0000221015789057919092803231979347704503433159684460093043089586767581385820637379238439082859947835154740049696466406811480
h=0.0001  midpoint gap = -2.210156485172794608408416197981969667518509549718770868664667542394083575529668278606589768131824880206889201686940535e-7
```

These chords support the local negative second-derivative diagnosis at the
frozen point; they are not a regional proof.

## Fraction LDL feasibility

Interpreting the symmetrized float entries as exact decimal rationals:

```text
D positive definite: min LDL pivot ~= 0.9238679817529035
```

For `|t|<=1/200`, the endpoint checks with margin `1/2000` pass:

```text
t=-1/200:
  K+tD-1/2000 I       min LDL pivot ~= 0.391046623891519
  I-K-tD-1/2000 I     min LDL pivot ~= 0.41380263156067565

t=1/200:
  K+tD-1/2000 I       min LDL pivot ~= 0.4018496104978604
  I-K-tD-1/2000 I     min LDL pivot ~= 0.40276411200040246
```

So the frozen strongest direction is positive definite and the affine chord is
strictly feasible on the requested interval with the requested margin.

## H10-H15 attenuation profile

Read-only profile extracted from the frozen recheck JSONs:

| batch | margin | best rho |
|---|---:|---:|
| H10 / round18 boundary1 | 0.015371444079016916 | 0.5746069386526107 |
| H11 / round19 interior1 | 0.02171078114876157 | 0.5745947308664667 |
| H12 / round20 interior2 | 0.05 | 0.5729410207438331 |
| H13 / round21 interior3 | 0.09999999999999998 | 0.5313886643536545 |
| H14 / round22 interior4 | 0.19999999999999996 | 0.3337720601402677 |
| H15 / round23 interior5 | 0.3 | 0.15219460446316677 |

This supports the finite attenuation narrative in the central spectral box, but
does not prove monotonicity or exclude unsearched mechanisms.

## Scope verdict

- Ledger accounting: SCOUT_CORRECT.
- Margin floor `.30`: SCOUT_CORRECT.
- No row with `rho>=1` or positive gap: SCOUT_CORRECT for the frozen ledgers.
- Strongest shard/index/rho: SCOUT_CORRECT.
- 130-digit exact-event/Möbius H'', Fisher, acceleration, rho: SCOUT_CORRECT.
- Three entropy chords: SCOUT_CORRECT.
- Fraction LDL feasibility for `D>0` and `|t|<=1/200` with `1/2000` margin:
  SCOUT_CORRECT.
- Global theorem or all-domain exclusion: NOT CLAIMED / INCOMPLETE.
