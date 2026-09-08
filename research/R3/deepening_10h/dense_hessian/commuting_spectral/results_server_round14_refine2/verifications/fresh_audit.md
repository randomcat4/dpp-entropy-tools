# D10-H6 round14 refine2 fresh non-author audit

STATUS: CORRECT

Scope of this status: the copied ledgers/manifests/hashes and the strongest stored point's high-precision negative gate are correct for the stated finite scout.  The mathematical implication of the 20,000-proposal search remains SCOUT, and a full replay of proposal generation is INCOMPLETE.

I did not modify author data or gate files.  I added only:

- `verifications/fresh_round14_refine2_audit.py`
- `verifications/fresh_round14_refine2_audit.json`
- `verifications/fresh_audit.md`

No server was used.  No `C:\canglan\` path was accessed.

## Inputs checked

Primary author-side claims checked:

- `README.md:3` records `HIGH_PRECISION_STABLE_NEGATIVE`.
- `README.md:14` states the corrected producer writes one source/base row as `index=-1`.
- `README.md:22`-`README.md:30` states 20,000 proposals, no positive midpoint gap, max gap `-6.165970208549254e-05`, strongest `rho=0.5715404864746153`, and strongest row shard 2 / seed `2026090846` / index 4998.
- `README.md:44`-`README.md:51` states high-precision `H''<0`, `rho<1`, negative three-chord gaps, and Fraction LDL margin `1/2000` over `|t|<=1/200`.
- `README.md:56`-`README.md:57` correctly limits the rationalized certificate to a near-commuting PSD K-affine line, not an exactly commuting rational line.
- `recheck_best_refine2.json:2`-`recheck_best_refine2.json:3` records the same finite-scout scope.
- `recheck_best_refine2.json:159`-`recheck_best_refine2.json:212` records the strongest row and high-precision `H''/rho`.
- `recheck_best_refine2.json:224`-`recheck_best_refine2.json:239` records the three negative high-precision chord gaps.
- `recheck_best_refine2.json:248`-`recheck_best_refine2.json:290` records the Fraction LDL feasibility certificate.

## Command run

From repo root:

```powershell
$env:OMP_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'; & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'research\R3\deepening_10h\dense_hessian\commuting_spectral\results_server_round14_refine2\verifications\fresh_round14_refine2_audit.py'
```

Exit code: `0`.

Machine-time denominator: 4 shards, each `5001` CSV data rows (`1` source row plus `5000` proposal rows), for `20004` data rows total.  Exact-event denominator for the strongest-point recomputation: `4096` atoms.

## Hash checks

Matched expected hashes:

- `source.npz`: `4bda0a82ca642b5e804bca498107a89a1c81a3a7eb79ce6aca2712e4d594cb72`
- `results_2/best_case.npz`: `32741ce56d53b0c3637172d1805b7810990616e6ff90ae0c94509787fdd521ef`
- `spectral_basis_refine.py`: `28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268`

Additional local hashes recorded:

- `commuting_spectral_search.py`: `dd55e9f05afd128a4e64e06ab705ba031fb0f32f0ea4a44a0169b625b9050a37`
- `recheck_best_refine2.py`: `e7ab0f1b1a04a6a447241f07ea5938556999f6f50df0d4e606b4a9c0464c1c0e`
- `recheck_best_refine2.json`: `8dad13595ed3a4e51b43837e2f4698d76cec08836de79b870bc90363311f38de`

## Ledger and manifest audit: CORRECT

For each shard `0,1,2,3`:

- physical CSV lines including header: `5002`;
- CSV data rows: `5001`;
- source rows: exactly one, with `index=-1` and label `source_base`;
- proposal rows: exactly `5000`, with unique complete indices `0..4999`;
- manifest status: `SCOUT_COMPLETE`;
- manifest exit code: `0`;
- manifest `positive_count`: `0`;
- all ledger statuses are `NO_HIT`;
- all ledger midpoint gaps are negative;
- accepted proposal counts match each manifest;
- per-shard `best_case.json` matches the best ledger row by `rho_psd`;
- run logs mention the manifest seed.

Per-shard maxima:

| shard | seed | accepted proposals | best index | best label | best rho | max gap |
|---:|---:|---:|---:|---|---:|---:|
| 0 | 2026090844 | 3461 | 3045 | `one_basis_rotation` | 0.569655999211623 | -6.57469482554518e-05 |
| 1 | 2026090845 | 3537 | 1454 | `three_basis_rotations` | 0.5695825133885262 | -7.012567624276045e-05 |
| 2 | 2026090846 | 3478 | 4998 | `three_basis_rotations` | 0.5715404864746153 | -6.165970208549254e-05 |
| 3 | 2026090847 | 3539 | 1195 | `source_restart` | 0.5692654213795351 | -6.193621571171093e-05 |

Aggregate:

- data rows: `20004`;
- proposal rows: `20000`;
- source rows: `4`;
- non-`NO_HIT` rows: `0`;
- positive gap rows: `0`;
- largest stored midpoint gap: `-6.165970208549254e-05`;
- global strongest row: shard `2`, index `4998`, `rho_psd=0.5715404864746153`, stored-step gap `-0.00019844664425683334`.

## Strongest-point independent gate: CORRECT

I did not import the author gate/search modules.  The independent script implements:

- inclusion determinant derivatives for all principal subsets;
- explicit superset Möbius inversion to exact-event atoms;
- entropy, Fisher term, acceleration term, and `H'' = acceleration - Fisher`;
- three high-precision midpoint chords on the same `Decimal(repr(float))` rationalized line;
- Fraction LDL checks for the direction and for endpoint spectral margins.

The strongest stored NPZ was symmetrized before rationalization, matching the author certificate convention.  Raw asymmetry was small:

- `max |K-K^T| = 5.551115123125783e-17`;
- `max |D-D^T| = 5.551115123125783e-17`.

Float orientation checks:

- `min eig(K)=0.0427915872973073`, `max eig(K)=0.9867754718663373`;
- `min eig(D)=0.3586269785490768`, `max eig(D)=0.9999999999999979`;
- `||KD-DK||_F=1.5169241799893413e-15`.

90-digit exact-event/Möbius recomputation over all `4096` atoms:

- `sum p = 1.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000`;
- `min p = 9.763714710141086650834700690023940823658496966703802185406400305506857203416142502424E-9`;
- `sum p' = -2.272598E-89`;
- `sum p'' = -1.128254E-88`;
- Fisher `= 68.1119701803260721474834963400764071974052928118444954768556288417469392274875885696472653`;
- acceleration `= 38.9287485716079843372993459356143950892910592759952848138881129281909784741107374433726352`;
- `H'' = -29.1832216087180878101841504044620121081142335358492106629675159135559607533768511262746301`;
- `rho = 0.571540486474614276140746429134937786566306363104544747825335796071188918475434118474759337`.

Three high-precision midpoint chords are all negative:

| step | midpoint gap | central second difference |
|---:|---:|---:|
| 0.0036875441404792273 | -0.00019844664425465482217519952929146203449812120131177537651194469870059477610357060834429 | -29.1876614263498291400999049881747198687496220375581191734402731810439611372242604681188600 |
| 0.001 | -0.00001459177395692516356434408838279195230134949133638618631043024016284929491742507628679 | -29.1835479138503271286881767655839046026989826727726208604803256985898348501525736 |
| 0.0001 | -1.4591612435806010685463318854170515610144769963889829368861584010722715893687173409E-7 | -29.18322487161202137092663770834103122028953992777965873772316802144543178737434682 |

Fraction LDL certificate:

- `D` is positive definite under exact `Fraction(repr(float))` entries; minimum LDL pivot float `0.5101187732631215`.
- On `t=-1/200`, both `K(t)-I/2000` and `I-K(t)-I/2000` have all positive Fraction LDL pivots; minimum pivot floats `0.10798184022423032` and `0.05845982825337602`.
- On `t=1/200`, both `K(t)-I/2000` and `I-K(t)-I/2000` have all positive Fraction LDL pivots; minimum pivot floats `0.11792215927131186` and `0.04894849509845937`.

Thus the strongest stored point is a rigorously negative gate, not a positive counterexample.

## Proposal generation replay: INCOMPLETE

I checked seed/accounting consistency and every ledger row, but I did not re-run the full 20,000-proposal generation.  The run logs and manifests are internally consistent, and the stored best JSON/NPZ files match their ledgers, but complete regeneration would be a separate replay layer.

## Mathematical scope: SCOUT

This round is a finite search certificate, not a theorem:

- the float scout optimizes PSD directions in a fixed numerical eigenbasis at each accepted center;
- the outer search still ranges over joint basis/spectrum proposals;
- the rationalized strongest line is a near-commuting PSD K-affine line (`||KD-DK||_F≈1.52e-15`), not an exactly commuting rational line;
- all checked signs are negative (`rho<1`, `H''<0`, and finite midpoint gaps `<0`);
- no statement about all commuting spectral directions, all PSD directions, or the whole real domain follows from these finite misses.

## Final layered verdict

- Ledger/manifests/hashes: CORRECT.
- Strongest 90-digit exact-event/Möbius + three-chord + Fraction LDL gate: CORRECT.
- Proposal generation replay from seed: INCOMPLETE.
- Search-theoretic content: SCOUT only.

No critical gap was found inside the stated copied-data accounting or strongest negative-certificate scope.
