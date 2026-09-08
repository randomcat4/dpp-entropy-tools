# D10-U10c scalar-rho falsification search

AUTHOR VERDICT: SCOUT_NO_COUNTEREXAMPLE_FOUND.

This unit deliberately searched for a connected strict three-dimensional DPP
kernel with the U8 scalar threshold

```text
rho(K)=det(N) eta^T A^{-1} eta
```

crossing `1`.  No such point was found.  This is only finite/scout evidence:
it does not prove the global inequality `rho(K)<=1`.

## Implementation scope

The search script `rho_scalar_search.py` is an independent implementation of
the U8 scalar formula.  It does not import `global_probe.py`,
`rank_one_recheck.py`, `point_interval_gate.py`,
`symbolic_identity_gate.py`, or any U8 author/search/gate module.

It rebuilds from scratch:

- the eight exact Möbius event atoms
  `p0,p1,p2,p3,p12,p13,p23,p123`;
- their first coordinate derivatives in the observation basis
  `(11,22,33,12,13,23)`;
- the event Fisher form `sum_S dp_S dp_S^T/p_S`;
- the four logarithmic coefficients `l12,l13,l23,Lambda`;
- `N=-diag(l23,l13,l12)-Lambda K`;
- `A=Fisher+det(N)G_N`, `eta_i=tr(N^{-1}E_i)`, and `rho`.

For candidates near or above threshold, the script recomputes rho with Python
`Decimal` logarithms and independent small-matrix elimination.  These Decimal
checks are high-precision numerical checks, not interval certificates.

## Actual command

From repository root:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/scalar_falsification/rho_scalar_search.py
```

Exit code: `0`.

The final run took `27.63113284111023` seconds.

## Denominator

Float-stage attempts: `38436`.
Accepted strict connected cases: `22023`.

| route | attempted | accepted | rejected / reason |
|---|---:|---:|---|
| `L_ensemble_exact_atom_boundaries` | 564 | 429 | 124 nonpositive atom, 9 disconnected, 2 `N_not_PD` |
| `rank_one_unequal_soft_rates` | 5400 | 1960 | 2090 not strict spectrum, 1207 nonpositive atom, 143 `N_not_PD` |
| `near_disconnected_and_sign_mixed_edges` | 3672 | 3552 | 120 `N_not_PD` |
| `spectral_0_1_corners` | 6000 | 5594 | 406 nonpositive atom |
| `biased_interior_random` | 6000 | 6000 | none |
| `targeted_local_hill_from_best` | 16800 | 4488 | 12312 not strict spectrum |

Small-atom coverage at threshold `1e-8` hit all eight exact atom names:

```text
p0: 2869, p1: 306, p2: 231, p3: 214,
p12: 530, p13: 551, p23: 615, p123: 4299.
```

Decimal-stage checks:

- `15` top-float rechecks;
- `280` rational-Q rank-one/eigenvalue-rate boundary probes;
- `150` Decimal-only `Lambda≈0` near-disconnected path probes;
- `0` Decimal `rho>1` results;
- `54` Decimal near-threshold records with `rho>0.95`.

## Best observed values

The largest corrected high-precision rho in the final ledger is

```text
rho = 0.9950999446020196922911257953855959280221718650482929047601670254765438777856486836495129344342754064022369540204228662011672508079690065124625029710581117541577676410148416953535847369834577299038700610576856898811907918798087195422548890519163234525698411419379937038366106458706737164750082
1-rho = 0.0049000553979803077088742046144040719778281349517070952398329745234561222143513163504870655657245935977630459795771337988327491920309934875374970289418882458422323589851583046464152630165422700961299389423143101188092081201912804577451109480836765474301588580620062961633893541293262835249918
```

It occurs on the rational-Q rank-one boundary family with
`theta=0.99`, `epsilon=10^-96`, rates `[1,1]`, no complement.  The
smallest exact atom there is `p123=9.9e-193`.  This is close to the
known rank-one boundary mechanism and remains below one.

The largest unequal-soft-rate Decimal probe is

```text
rho = 0.99325250311940130939025336008385825478...
```

at `theta=0.5`, `epsilon=10^-96`, rates `[2,3]`, no complement, with
minimum atom `p123=5e-481`.

The Decimal-only `Lambda≈0` near-disconnected path family did not come close:
its largest corrected rho was about `0.50005480933937655`.

An internal audit found that the first Decimal implementation used the
diagonal derivative `-1` of the empty atom in all six observation coordinates.
The float scout was unaffected, but the first published Decimal rankings were
invalid.  The implementation now uses `(-1,-1,-1,0,0,0)` and the complete
deterministic run has been regenerated.  The corrected 280 boundary probes,
150 near-`Lambda=0` probes, and 15 top-float rechecks still contain no
`rho>1`; all Decimal values in this verdict are from the repaired run.

## Float hazard found

The float stage produced an apparent near-one value

```text
rho_float = 0.9999999999875521
```

on a near-disconnected path with `Lambda≈6.66e-16` and
`min_eig_N≈1.36e-26`.  Decimal recomputation of the same stored `K` gives

```text
rho = 0.50000000000000000000041666666666666662...
```

with `N` LDL pivots of order `2e-10`, `1e-20`, `2e-10`.  This is a useful
negative result for the search protocol: near `Lambda=0` and almost
disconnected support, the scalar formula is badly conditioned in ordinary
floating point and must not be used as a candidate gate.

## Candidate status

No `rho>1` candidate was frozen.  Therefore no bad direction
`D=A^{-1}eta`, strict chord, rational LDL, or log-interval gate was attempted
for a positive witness.

The files to audit are:

- `rho_scalar_search.py`
- `search_ledger.json`
- `near_threshold_candidates.json`
- `run_log.md`
- `verdict.md`

The result is a targeted finite falsification ledger only.  It supports the
statement “this search did not find a scalar counterexample,” not the theorem
`rho(K)<=1`.
