# D10-H8 round16_refine4 fresh non-author audit

STATUS: CORRECT

Scope of this status: copied-data accounting, hashes, ledger/manifests/logs, best JSON/NPZ consistency, and the strongest stored point's high-precision negative gate.  The finite search implication remains SCOUT.  Full seed regeneration was not executed and is INCOMPLETE.

I did not modify author data or gate files.  I added only:

- `verifications/fresh_round16_refine4_audit.py`
- `verifications/fresh_round16_refine4_audit.json`
- `verifications/fresh_audit.md`

No server was used.  No `C:\canglan\` path was accessed.

## Author-side inputs checked

The README states the intended layered status and scope:

- copied-data accounting and strongest gate await independent review, finite run is `SCOUT`, full replay/global claims are `INCOMPLETE`: `README.md:3-5`;
- four single-thread shards, each with one `index=-1` source row and 5,000 proposals: `README.md:9-13`;
- fixed-Q-at-center float construction and outer spectrum/basis perturbation: `README.md:15-18`;
- finite scout summary: 20,000 proposals, 0 positive gaps, largest stored gap `-4.517140952842169e-05`: `README.md:21-25`;
- strongest row: shard 2, seed `2026090854`, index 4889, `one_basis_rotation`, `rho=0.5735840441822098`: `README.md:26-28`;
- sign-change threshold remains `rho>1`: `README.md:32`;
- author high-precision gate: \(H''<0\), `rho<1`: `README.md:41-42`;
- three high-precision chord gaps and Fraction LDL feasibility: `README.md:45-48`;
- rationalized certificate is near-commuting, not exactly commuting: `README.md:50-53`;
- expected hashes: `README.md:57-62`.

The author JSON repeats the finite scope at `recheck_best_refine4.json:2-3`, the strongest row at `recheck_best_refine4.json:12-31`, and the strongest shard/index at `recheck_best_refine4.json:159-160`.

## Command run

From repo root:

```powershell
$env:OMP_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'; & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'research\R3\deepening_10h\dense_hessian\commuting_spectral\results_server_round16_refine4\verifications\fresh_round16_refine4_audit.py'
```

Exit code: `0`.

Denominators:

- four shards;
- each shard: `5001` CSV data rows = one source row plus `5000` proposal rows;
- aggregate: `20004` CSV data rows = four source rows plus `20000` proposal rows;
- strongest exact-event recomputation: `4096` atoms.

## Hash checks

Expected hashes matched:

- `source.npz`: `21bcb4d8867b2f7d32ee398432dfaa6f2d91976a4a959191d2da4d112153eb71`
- `results_2/best_case.npz`: `b078c507558faa74b2a583581bfc5b51859009dafd12e6c2b95e6e25cad0b5a2`
- `spectral_basis_refine.py`: `28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268`

Additional hashes recorded:

- `commuting_spectral_search.py`: `dd55e9f05afd128a4e64e06ab705ba031fb0f32f0ea4a44a0169b625b9050a37`
- `recheck_best_refine4.py`: `2e80e96c7ba03be312e78480e7efe7b32ea4f64f2c556a33178d56de701e791e`
- `recheck_best_refine4.json`: `fa9d51986d64747618ebadd8b2c52b1521f6ec0972bdadaeeffa273fb68d3725`

## Ledger/manifests/logs/best files: CORRECT

Per shard:

| shard | seed | accepted proposals | best index | best label | best rho | best gap | max stored gap |
|---:|---:|---:|---:|---|---:|---:|---:|
| 0 | 2026090852 | 3500 | 2856 | `spectrum_local` | 0.5732972493148891 | -0.0002391635391498781 | -7.033810064527302e-05 |
| 1 | 2026090853 | 3506 | 4971 | `source_restart` | 0.5732063525042135 | -0.0002188829160711947 | -4.517140952842169e-05 |
| 2 | 2026090854 | 3528 | 4889 | `one_basis_rotation` | 0.5735840441822098 | -0.00013433371724325127 | -6.930968803953164e-05 |
| 3 | 2026090855 | 3535 | 4985 | `one_basis_rotation` | 0.5730855864646438 | -0.00027308587909313786 | -5.789817396362196e-05 |

Checks passed:

- each CSV has `5002` physical lines including header and `5001` data rows;
- each shard has exactly one source row with `index=-1`, label `source_base`;
- each shard has complete proposal indices `0..4999`;
- all row statuses are `NO_HIT`;
- all midpoint gaps are negative;
- manifest status is `SCOUT_COMPLETE`;
- manifest exit code is `0`;
- manifest thread count is `1`;
- manifest `positive_count` is `0`;
- accepted proposal counts match manifest counts;
- every per-shard `best_case.json` matches the best ledger row by `rho_psd`;
- each run log mentions the manifest seed.

Aggregate:

- data rows: `20004`;
- proposal rows: `20000`;
- source rows: `4`;
- non-`NO_HIT` rows: `0`;
- positive gap rows: `0`;
- largest stored midpoint gap: `-4.517140952842169e-05` from shard 1;
- strongest row by `rho_psd`: shard 2, index 4889, `rho_psd=0.5735840441822098`, stored-step gap `-0.00013433371724325127`.

The max stored gap and strongest-by-rho row are different rows; the copied summary is consistent on both.

## Strongest-point independent gate: CORRECT

I did not import `recheck_best_refine4.py`, the round14 gate, or the search module.  The independent script implements:

- inclusion determinant derivatives for all principal subsets;
- explicit superset Möbius inversion to exact-event atoms;
- entropy, Fisher term, acceleration term, and \(H''=\mathrm{acceleration}-\mathrm{Fisher}\);
- three high-precision midpoint chords along the same `Decimal(repr(float))` rationalized line;
- Fraction LDL checks for direction positive definiteness and endpoint spectral margins.

The stored strongest NPZ was symmetrized before rationalization, matching the author convention.

Float orientation diagnostics:

- `max |K-K^T| = 5.551115123125783e-17`;
- `max |D-D^T| = 7.632783294297951e-17`;
- `min eig(K)=0.03037093064321954`, `max eig(K)=0.9893128292654363`;
- `min eig(D)=0.4235346827808973`, `max eig(D)=0.9999999999999978`;
- `||KD-DK||_F=2.153918899240019e-15`.

90-digit exact-event/Möbius recomputation:

- event count: `4096`;
- `sum p = 0.999999999999999999999999999999999999999999999999999999999999999999999999999999999999999994`;
- `min p = 1.51312039104307246464531164482343323107059139744007691871094241202041030188669020929126965E-8`;
- `sum p' = -5.197502E-89`;
- `sum p'' = 7.20222E-89`;
- Fisher `= 98.9440969940350717251420021199956260236638686748301186946280830279191590790091881595208490`;
- acceleration `= 56.7527553017953564670551738233681768935913743810270099072401355580689304211572710692346065`;
- \(H'' = -42.1913416922397152580868282966274491300724942938031087873879474698502286578519170902862425\);
- `rho = 0.573584044182208708723725374457821643297675469047493436184270336752518235080734586610146366`.

Three 90-digit midpoint chords:

| step | midpoint gap | central second difference |
|---:|---:|---:|
| 0.002523328352803181 | -0.00013433371724375954925841030937618115296387345686822917612105855079402824194051624288722 | -42.1956317119784193359534140156134675704129487171633261571089160531814235031346732958510650 |
| 0.001 | -0.00002109600761490317251093651901334670338145105621769777348193448136337459775737546220202 | -42.1920152298063450218730380266934067629021124353955469638689627267491955147509244040 |
| 0.0001 | -2.1095674213593331732232248577703490591082163788255353562848067976497896833704777997E-7 | -42.19134842718666346446449715540698118216432757651070712569613595299579366740955599 |

Fraction LDL certificate:

- `D` is positive definite under exact `Fraction(repr(float))` entries; minimum pivot float `0.617304661926381`.
- At `t=-1/200`, both `K(t)-I/2000` and `I-K(t)-I/2000` have all positive Fraction LDL pivots; minimum pivot floats `0.06302687116203644` and `0.07640569960847966`.
- At `t=1/200`, both `K(t)-I/2000` and `I-K(t)-I/2000` have all positive Fraction LDL pivots; minimum pivot floats `0.07326269973469346` and `0.056861398246729054`.

Thus the strongest stored point is a strictly feasible, PSD-direction, rigorously negative gate.  It is not a positive counterexample.

## Full seed regeneration: INCOMPLETE

I checked seed/accounting/log consistency and all stored rows, but I did not rerun the full 20,000-proposal generation from seeds.  Full regeneration should remain a separate replay layer if required.

## Mathematical interpretation: SCOUT

This directory is finite search evidence only:

- the float scout is fixed-Q at each accepted center;
- the outer heuristic perturbs spectrum and basis between centers;
- entrywise decimal rationalization gives a near-commuting PSD K-affine line with `||KD-DK||_F≈2.15e-15`, not an exactly commuting rational line;
- all stored and high-precision signs remain negative: `rho<1`, \(H''<0\), and all checked midpoint gaps are negative;
- this does not prove any universal claim for all commuting spectral directions, all PSD directions, or the full real domain.

## Final layered verdict

- Ledger/manifests/logs/hashes/best files: CORRECT.
- Strongest 90-digit exact-event/Möbius + three-chord + Fraction LDL gate: CORRECT.
- Full proposal-generation replay from seeds: INCOMPLETE.
- Mathematical search implication: SCOUT.

No critical gap was found inside the stated copied-data accounting or strongest negative-certificate scope.
