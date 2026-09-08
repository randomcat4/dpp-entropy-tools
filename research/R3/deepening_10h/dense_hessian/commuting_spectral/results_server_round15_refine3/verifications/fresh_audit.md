# D10-H7 round15 refine3 fresh non-author audit

STATUS: CORRECT

Scope of this status: copied-data accounting, hashes, ledger/manifests, best JSON/NPZ consistency, and the strongest stored point's high-precision negative gate.  The finite search implication remains SCOUT, and full proposal regeneration from seeds is INCOMPLETE.

I did not modify author data or gate files.  I added only:

- `verifications/fresh_round15_refine3_audit.py`
- `verifications/fresh_round15_refine3_audit.json`
- `verifications/fresh_audit.md`

No server was used.  No `C:\canglan\` path was accessed.

## Author-side inputs checked

The README records:

- author status `HIGH_PRECISION_STABLE_NEGATIVE`: `README.md:3`;
- four one-thread shards, each one `index=-1` source row plus 5,000 proposal rows: `README.md:9-12`;
- finite scout summary: 20,000 new proposals, 0 positive gaps, largest stored gap `-6.0892895073827447e-05`: `README.md:20-24`;
- strongest row by mechanism ratio: shard 0, seed `2026090848`, index `4942`, `three_basis_rotations`, `rho=0.5725909000830567`: `README.md:25-27`;
- sign threshold remains `rho>1`: `README.md:31`;
- author high-precision gate: \(H''<0\), `rho<1`: `README.md:40-41`;
- high-precision three chords and Fraction LDL feasibility: `README.md:44-47`;
- rationalized certificate is near-commuting, not exactly commuting: `README.md:49-52`;
- expected source/strongest/producer hashes: `README.md:56-61`.

The author JSON records the same finite scope and strongest row at `recheck_best_refine3.json:2-3` and `recheck_best_refine3.json:159-160`.

## Command run

From repo root:

```powershell
$env:OMP_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'; & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'research\R3\deepening_10h\dense_hessian\commuting_spectral\results_server_round15_refine3\verifications\fresh_round15_refine3_audit.py'
```

Exit code: `0`.

Denominators:

- four shards;
- each shard: `5001` CSV data rows = `1` source row plus `5000` proposal rows;
- aggregate: `20004` CSV data rows = `4` source rows plus `20000` proposal rows;
- strongest exact-event recomputation: `4096` atoms.

## Hash checks

Expected hashes matched:

- `source.npz`: `32741ce56d53b0c3637172d1805b7810990616e6ff90ae0c94509787fdd521ef`
- `results_0/best_case.npz`: `21bcb4d8867b2f7d32ee398432dfaa6f2d91976a4a959191d2da4d112153eb71`
- `spectral_basis_refine.py`: `28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268`

Additional hashes recorded:

- `commuting_spectral_search.py`: `dd55e9f05afd128a4e64e06ab705ba031fb0f32f0ea4a44a0169b625b9050a37`
- `recheck_best_refine3.py`: `888f201e824f0ea5ed2f88e8a1d5aaedc85dad0907779a36081a5d767f7c0bf9`
- `recheck_best_refine3.json`: `e709abd00a1cbfa0a7fdcc4be59629cdcea8c477a7eedc4a5bbf83728b35bf6e`

## Ledger/manifests/best files: CORRECT

Per shard:

| shard | seed | accepted proposals | best index | best label | best rho | best gap | max stored gap |
|---:|---:|---:|---:|---|---:|---:|---:|
| 0 | 2026090848 | 3505 | 4942 | `three_basis_rotations` | 0.5725909000830567 | -0.0002264422099376162 | -6.223585415288113e-05 |
| 1 | 2026090849 | 3474 | 4958 | `three_basis_rotations` | 0.5725278078283833 | -0.0002579896413363869 | -7.42496922869762e-05 |
| 2 | 2026090850 | 3507 | 4928 | `spectrum_local` | 0.5720479245084936 | -0.00020412236633937653 | -6.0892895073827447e-05 |
| 3 | 2026090851 | 3397 | 578 | `three_basis_rotations` | 0.5721705438342415 | -0.00032811032990132105 | -6.645026043639035e-05 |

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
- largest stored midpoint gap: `-6.0892895073827447e-05` from shard 2;
- strongest row by `rho_psd`: shard 0, index 4942, `rho_psd=0.5725909000830567`, stored-step gap `-0.0002264422099376162`.

The max stored gap and strongest-by-rho row are different rows; the copied summary is consistent on both.

## Strongest-point independent gate: CORRECT

I did not import author gate/search modules.  The independent script implements:

- inclusion determinant derivatives for all principal subsets;
- explicit superset Möbius inversion to exact-event atoms;
- entropy, Fisher term, acceleration term, and \(H''=\mathrm{acceleration}-\mathrm{Fisher}\);
- three high-precision midpoint chords along the same `Decimal(repr(float))` rationalized line;
- Fraction LDL checks for direction positive definiteness and endpoint spectral margins.

The stored strongest NPZ was symmetrized before rationalization, matching the author convention.

Float orientation diagnostics:

- `max |K-K^T| = 3.2004292879056484e-17`;
- `max |D-D^T| = 5.551115123125783e-17`;
- `min eig(K)=0.037549122305867266`, `max eig(K)=0.9853605058311824`;
- `min eig(D)=0.4634280466613409`, `max eig(D)=0.9999999999999982`;
- `||KD-DK||_F=1.9581532164097705e-15`.

90-digit exact-event/Möbius recomputation:

- event count: `4096`;
- `sum p = 0.999999999999999999999999999999999999999999999999999999999999999999999999999999999999999995`;
- `min p = 2.10371033527606491650537119612162592656042517597285122642489283492777973543100685133319420E-8`;
- `sum p' = -5.933198E-89`;
- `sum p'' = -8.040E-90`;
- Fisher `= 106.165006155608855332996241872586988965209147774243144689572704077450246959841105130659998`;
- acceleration `= 60.7891164319633255403644727318780468028113869393176605012135535214273968015463278909209915`;
- \(H'' = -45.3758897236455297926317691407089421623977608349254841883591505560228501582947772397390065\);
- `rho = 0.572590900083056661856638550203110451067306462560764684025298587791023626891275545400608518`.

Three 90-digit midpoint chords:

| step | midpoint gap | central second difference |
|---:|---:|---:|
| 0.0031589573126367663 | -0.00022644220993686739706470220496475205048758967469847917053935812906104316470503433477840 | -45.3836964524533270300736446772681802797238749106604585085473155611627209316118104959845627 |
| 0.001 | -0.00002268833579157430324325890134337578618152949008272692045922798808422143209137408250880 | -45.3766715831486064865178026867515723630589801654538409184559761684428641827481650176 |
| 0.0001 | -2.2687948770869472808825199895159553550027547748581965183106834031750731757386242850E-7 | -45.37589754173894561765039979031910710005509549716393036621366806350146351477248570 |

Fraction LDL certificate:

- `D` is positive definite under exact `Fraction(repr(float))` entries; minimum pivot float `0.671321944243324`.
- At `t=-1/200`, both `K(t)-I/2000` and `I-K(t)-I/2000` have all positive Fraction LDL pivots; minimum pivot floats `0.08071429058048336` and `0.09263850034715466`.
- At `t=1/200`, both `K(t)-I/2000` and `I-K(t)-I/2000` have all positive Fraction LDL pivots; minimum pivot floats `0.09161883148969902` and `0.07358077675028875`.

Thus the strongest stored point is a strictly feasible, PSD-direction, rigorously negative gate.  It is not a positive counterexample.

## Proposal seed regeneration: INCOMPLETE

I checked seed/accounting/log consistency and all stored rows, but I did not rerun the full 20,000-proposal generation from seeds.  Given the author logs are roughly 1,070--1,108 seconds per shard, full regeneration should be treated as a separate replay layer if required.

## Mathematical interpretation: SCOUT

This directory is finite search evidence only:

- each accepted center uses a positive spectral-rate direction in a fixed numerical eigenbasis;
- the outer heuristic perturbs both spectrum and basis between centers;
- entrywise decimal rationalization of the strongest point gives a near-commuting PSD K-affine line with `||KD-DK||_F≈1.96e-15`, not an exactly commuting rational line;
- all stored and high-precision signs remain negative: `rho<1`, \(H''<0\), and all checked midpoint gaps are negative;
- the run does not prove a theorem for all commuting spectral directions, all PSD directions, or the full real domain.

## Final layered verdict

- Ledger/manifests/hashes/best files: CORRECT.
- Strongest 90-digit exact-event/Möbius + three-chord + Fraction LDL gate: CORRECT.
- Full proposal-generation replay from seeds: INCOMPLETE.
- Mathematical search implication: SCOUT.

No critical gap was found inside the stated copied-data accounting or strongest negative-certificate scope.
