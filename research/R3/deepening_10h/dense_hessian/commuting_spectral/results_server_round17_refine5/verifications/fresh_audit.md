STATUS: CORRECT

Scope of this status: CORRECT only for copied-data accounting/hash consistency and for the frozen strongest-point high-precision gate.  The 20,000-proposal round remains SCOUT evidence, and full seed regeneration remains INCOMPLETE.

## Inputs audited

Read-only audited directory:

`research/R3/deepening_10h/dense_hessian/commuting_spectral/results_server_round17_refine5/`

Author-facing scope markers checked:

- `README.md:3-4` states pending independent review for copied-data accounting and strongest-point gate, and SCOUT for the finite proposal run.
- `README.md:10-12` states four single-thread shards, one `index=-1` source row plus 5,000 proposal rows per shard, for 20,004 stored rows and 20,000 new proposals.
- `README.md:25-28` identifies the strongest row as shard 1, seed 2026090857, index 4910, with rho `0.5740468373613397` and stored-step gap `-0.00011880571419009556`.
- `README.md:41` records the author-side high-precision `H''` as negative.
- `README.md:52` correctly limits the rationalized certificate to a near-commuting PSD K-affine line, not an exactly commuting rational commuting line.
- `recheck_best_refine5.json:2-11`, `:159-164`, `:171-178`, `:211-212`, `:219`, `:242`, and `:293` contain the frozen ledger, strongest index/hash, spectra, 4096-event gate, chord, Fraction LDL, and check summaries.

I did not import `recheck_best_refine5.py`, the round14 gate, or the search module.  The independent script imports only standard-library modules plus NumPy for reading arrays/eigenvalue sanity checks.

## Commands run

Working directory:

`C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo`

Command:

```text
$env:OMP_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'; $py='C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'; & $py 'C:\game\gameproject\showa100\math\i05-real-20260908\R3\repo\research\R3\deepening_10h\dense_hessian\commuting_spectral\results_server_round17_refine5\verifications\fresh_round17_refine5_audit.py'; exit $LASTEXITCODE
```

Exit code: `0`.

Independent JSON output:

`research/R3/deepening_10h/dense_hessian/commuting_spectral/results_server_round17_refine5/verifications/fresh_round17_refine5_audit.json`

Script-reported elapsed time: `6.178741455078125` seconds.

## Denominators

- Shards checked: `4`.
- CSV data rows checked: `20004` = `4` source rows + `20000` proposal rows.  Each CSV has `5001` data rows plus header.
- Per-shard proposal indices checked: exactly `0..4999`; one source row has `index=-1`.
- Exact-event atoms rebuilt for strongest point: `4096`.
- Decimal chord steps checked: `3`.
- Fraction LDL matrices checked: `5` (`D`, plus `K(t)-I/2000` and `I-K(t)-I/2000` at `t=±1/200`).
- Full seed regeneration from random seeds: not run; status INCOMPLETE.

## Ledger/hash results

All ledger checks passed.

| shard | data rows | proposal rows | accepted proposals | best index | best rho | max proposal gap |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 5001 | 5000 | 3499 | 1411 | 0.5738509928981583 | -5.9401486740107146e-05 |
| 1 | 5001 | 5000 | 3531 | 4910 | 0.5740468373613397 | -5.620395474359441e-05 |
| 2 | 5001 | 5000 | 3491 | 1966 | 0.5740092484670168 | -4.784058084528198e-05 |
| 3 | 5001 | 5000 | 3502 | 4977 | 0.5738608752579064 | -5.78912481721261e-05 |

Aggregate checks:

- Stored rows: `20004`, proposals: `20000`, source rows: `4`, matching `recheck_best_refine5.json:5-7`.
- Non-`NO_HIT` rows: `0`; positive gap rows: `0`, matching `recheck_best_refine5.json:10`.
- Aggregate maximum proposal gap: `-4.784058084528198e-05`, matching `recheck_best_refine5.json:11`.
- Each final `run_i.log` JSON manifest equals the corresponding `results_i/manifest.json`.
- Shard 1 manifest records seed/proposal/best/positive/accepted/exit-code data at `results_1/manifest.json:2-19`.
- Shard 1 best JSON records index/rho/gap/spectrum margin/status at `results_1/best_case.json:2`, `:7`, `:17-20`.

Hash checks:

| object | SHA-256 | result |
|---|---|---|
| `source.npz` | `b078c507558faa74b2a583581bfc5b51859009dafd12e6c2b95e6e25cad0b5a2` | matches |
| strongest `results_1/best_case.npz` | `6a4fb8bd1790fbe17dbb58fac96a5ee3585bf7aac9c8f395608478b58750a978` | matches |
| producing script `spectral_basis_refine.py` | `28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268` | matches |

The strongest row is exactly shard `1`, index `4910`, matching `recheck_best_refine5.json:159-160`.

## Independent strongest-point gate

I rebuilt the exact-event distribution by Möbius inversion from inclusion determinants over all `4096` events, then computed the directional second derivative

`H'' = acceleration - Fisher`.

Precision: Decimal context `95`.

Results:

- entropy: `7.732139509405617013536075801780687364710193516686559812149770943297799601300983975731115552988`
- Fisher: `92.475543357579610884391186838951338228649988385008924831421641458651239170661397929922760961761`
- acceleration: `53.085293197689981244584356006329512209098307171112294125527279944644080584956993095256285166193`
- `H''`: `-39.390250159889629639806830832621826019551681213896630705894361514007158585704404834666475795568`
- `rho`: `0.57404683736133927336335041324642960159411791592054046449391672280761406097688556849852250247295`
- min atom: `1.527554179874662092000021066613571536649682803021115233548193132154833763595244065274958811542E-8`
- `sum p - 1`, `sum p'`, and `sum p''` were below the script thresholds; all atoms were positive.

These values match the author-side 80-digit gate in `recheck_best_refine5.json:211-212` within the independent threshold.

Three actual chords were independently recomputed from exact-event atoms, all with negative midpoint gap:

| step | midpoint gap | central second difference |
|---:|---:|---:|
| 0.0024559544091088455 | -0.00011880571419037756949272303499191525141079667639967174602716878980918166739351425 | -39.393695526586247503327939350783879186682188192529363649021315759869694375419685 |
| 0.001 | -0.000019695410599522668856995897608625118153890021430691682996179411075286739489014250 | -39.390821199045337713991795217250236307780042861383365992358822150573478978028500 |
| 0.0001 | -1.9695127934973845684431741329175111741386881469823045331351606208930087501424964E-7 | -39.390255869947691368863482658350223482773762939646090662703212417860175002849928 |

So the strongest stored point is a stable negative gate, not a hidden positive candidate.

## Spectrum-margin floor check

The strongest `best_case.json` reports `spectrum_margin = 0.010000000000000009` (`results_1/best_case.json:18`), equal to the configured search floor to float precision.  I checked this as a search-floor saturation, not as a singularity.

Independent float spectral checks on the symmetrized stored `K`:

- `lambda_min(K) = 0.033892448198570034`.
- `lambda_max(K) = 0.9900000000000004`.
- `min(lambda_min(K), 1-lambda_max(K)) = 0.009999999999999565`.
- NPZ stored spectrum gives min `0.03389244819857005`, max `0.99`, margin `0.010000000000000009`.
- `lambda_min(D) = 0.40717368217061306`, `lambda_max(D) = 0.9999999999999971`.
- commutator Frobenius norm `1.9719152934673647e-15`.

Thus the point touches the numerical acceptance floor near `1-lambda_max(K)=0.01`; it is still strictly inside `0<K<I`, and no positive/negative conclusion is being inferred from the floor itself.

Fraction LDL certificate for the decimal-rationalized line:

- `D > 0`: all `12` pivots positive; smallest pivot float proxy `0.6227356672249269`.
- At `t=-1/200`: all pivots positive for `K(t)-I/2000` and `I-K(t)-I/2000`; smallest pivot float proxies `0.08696316278730505` and `0.0709807916992364`.
- At `t=1/200`: all pivots positive for `K(t)-I/2000` and `I-K(t)-I/2000`; smallest pivot float proxies `0.09771527681220817` and `0.051505134873525364`.

This certifies the rationalized line has the requested `1/2000` spectral margin throughout the endpoint-checked interval `|t|<=1/200` by convexity of the PSD cone along the affine line.

## Scope cautions

- The float scout fixes `Q` at each accepted center while the outer heuristic perturbs both basis and spectrum; this remains a finite search layer.
- The Fraction certificate is for the symmetrized decimal-rationalized near-commuting K-affine line.  It is not an exact commuting spectral-family theorem.
- I did not replay the random generation from seeds `2026090856..2026090859`; seed regeneration is therefore INCOMPLETE.
- No positive gap, rho above 1, or strict counterexample candidate was found in the audited frozen data.

## Layered verdict

- Copied data accounting, manifests, logs, best JSON/NPZ/hash consistency: CORRECT.
- Strongest-point 90+ digit exact-event/Möbius gate, three chords, and Fraction LDL feasibility: CORRECT.
- Full seed regeneration: INCOMPLETE.
- Mathematical/global claim beyond this finite near-commuting rational line: SCOUT only.
