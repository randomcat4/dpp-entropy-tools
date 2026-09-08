# D10-H11 fresh nonauthor audit: `results_server_round19_interior1`

STATUS: CORRECT for the frozen ledger/manifests and the strongest independent gate; INCOMPLETE for full seed regeneration of all proposals; SCOUT only for any global interpretation.

I did not import or call the author gate/search modules.  The independent script in this directory rebuilds the exact-event/Möbius entropy derivatives directly from the stored strongest NPZ, and audits the copied CSV/JSON/log/manifest records as frozen evidence.

## Files written by this audit

- `fresh_audit.py` — SHA256 `4fae5c47e74091e2a68c6c5da0a3def09d6d4e2c92eeca2d05f25072ec6e35e9`
- `fresh_audit.json` — SHA256 `0b8379c43a725faaff3e56d11bc17ab1405b8cdec2552d6f5d69c614c91bf492`

Run command and denominator:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\dense_hessian\commuting_spectral\results_server_round19_interior1\verifications\fresh_audit.py
exit code: 0
ledger denominator: 20004 rows = 4 shards * (1 source row + 5000 proposal rows)
exact-event denominator for strongest: 4096 atoms
Decimal precision: 120 digits
```

## Frozen input hashes

Full hash inventory is in `fresh_audit.json`.  The most load-bearing inputs are:

| input | SHA256 |
|---|---|
| `spectral_basis_refine.py` | `28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268` |
| `commuting_spectral_search.py` | `dd55e9f05afd128a4e64e06ab705ba031fb0f32f0ea4a44a0169b625b9050a37` |
| `recheck_best_interior1.py` | `26b6038648c257360b30ce075dfe56bde96f921e45529d10152f08b399c9c0ee` |
| `recheck_best_interior1.json` | `9c63a9bfc64bc080261b3a1ca11febcd89c4af116530c23851b10a2e2bf7adf0` |
| `interior_source_margin003.npz` | `56e289047bc527697b1511763b8c50809445063ee32ed85d26dd0b8d15719e7d` |
| `results_0/best_case.npz` | `4c316f4515bfc1b8c0284e60bb724080f61d523e91d5d9e3299d24f709babebe` |
| H10 comparison `results_server_round18_boundary1/recheck_best_boundary1.json` | `8c64b57a2f01b2521a02eadf6f802c567985059e55cfd89d75c8c1634a0cd36a` |

## Ledger/manifest audit

CORRECT at the frozen-record level.

| shard | rows | source rows | proposal rows | accepted proposals | manifest positive_count | best index | best rho | status |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 | 5001 | 1 | 5000 | 2927 | 0 | 4853 | 0.5745947308664667 | NO_HIT |
| 1 | 5001 | 1 | 5000 | 2916 | 0 | 4880 | 0.5742048679748724 | NO_HIT |
| 2 | 5001 | 1 | 5000 | 2908 | 0 | 3374 | 0.5744295450381214 | NO_HIT |
| 3 | 5001 | 1 | 5000 | 2976 | 0 | 4994 | 0.5742327351874548 | NO_HIT |

Checks passed:

- each shard has exactly one source row with `index=-1`;
- each shard has proposal indices exactly `0..4999`;
- all 20004 ledger rows have `status=NO_HIT`;
- no ledger row has positive chord gap;
- no ledger row has `rho_psd >= 1`;
- global best by ledger `rho_psd` is shard 0, index 4853;
- best JSON rows match their corresponding CSV rows;
- manifest accepted counts and positive counts match the CSV audit;
- maximum stored gap over all rows is still negative: `-0.00016039858818750474`.

Spectrum-margin note: the CSV-recorded proposal margins have minimum `0.02` in every shard and the source rows have margin about `0.03`.  I recomputed spectra for the source NPZ and all four stored best NPZ files.  The strongest shard-0 best has actual float margin `0.021710781148760128`.  One non-strongest best NPZ recomputes as `0.019999999999998463`, which is a `1.5e-15` float-rounding undershoot of the configured `0.02` floor, not a substantive boundary hit.  I did not regenerate the other 19996 proposal matrices; that layer is marked INCOMPLETE below.

## Strongest exact-event/Möbius gate

CORRECT for shard 0, index 4853.

Stored strongest NPZ:

- SHA256 `4c316f4515bfc1b8c0284e60bb724080f61d523e91d5d9e3299d24f709babebe`
- `K` spectrum min/max: `0.03557494817045733`, `0.9782892188512399`
- spectrum margin: `0.021710781148760128`
- `D` eigenvalue min/max: `0.5057992384738401`, `0.9999999999999979`
- `||KD-DK||_F = 2.3189146003247504e-15`

Independent 120-digit exact-event/Möbius derivative recomputation over all 4096 atoms gives:

| quantity | value |
|---|---:|
| entropy | `7.74101917519702085010619537367378562287363660183481613629476342657090294632615679253923504351775979260623824779934845911` |
| Fisher term | `111.039782402901255305206345608301532283777982466061449505947690259859719107553968735647909481680923041281951478296871060` |
| acceleration term | `63.8028738852661006236125425646264725073639382420288517018525014344368309980487513517238310606193854399462352356709914208` |
| `H''` | `-47.2369085176351546815938030436750597764140442240325978040951888254228881095052173839240784210615376013357162426258796392` |
| `rho` | `0.574594730866466959253898834668613177310983170540497787779334564168201868719667966949403736777980243789014114026206511901` |
| min atom | `2.21641359849752851879940492844814703799872410323582751663406098840173990870175412863645810172019954531009711752304551199e-8` |

Normalization gates are at numerical zero at 120-digit precision:

- `sum(p)-1 = -2.4e-119`
- `sum(p') = -6.039027e-119`
- `sum(p'') = 1.38950e-118`

The independent values match the author 80-digit recheck to the displayed precision; absolute differences recorded in `fresh_audit.json` are about `3.6e-19` for `rho` and `1.1e-15` for `H''`.

## Three chord checks

CORRECT.  The same exact-event entropy oracle gives negative midpoint gaps on all three requested scales.

| step | midpoint gap | central second difference |
|---:|---:|---:|
| `0.00429237126063496` | `-0.00043529766082624591515825668283137234375895491889666157898118196820302833892019409821191917911014469560403003085121096` | `-47.2521715737284497785267863836602477764177489015104755284139694465116753987045143791825805156814949162546016640552636035` |
| `0.001` | `-0.00002361886797130225359347766362078504414431282496800748136824839110614897096171724117474712726371583663343506494625331` | `-47.23773594260450718695532724157008828862564993601496273649678221229794192343448234949425452743167326687012989250662` |
| `0.0001` | `-0.00000023618458395662205906054356721483906094479720519938985497588997166579411401593335322245018922105668428294576598596` | `-47.236916791324411812108713442967812188959441039877970995177994333158822803186670644490037844211336856589153197192` |

## Fraction LDL / affine admissibility

CORRECT for the stored strongest rationalized affine line.

The audit converts the stored float entries to exact decimal Fractions and checks LDL pivots exactly for:

- `D > 0`;
- `K + tD - (1/2000)I > 0`;
- `I - K - tD - (1/2000)I > 0`;
- at both endpoints `t = -1/200` and `t = 1/200`.

Endpoint pivot minima, reported as floats only for readability:

| endpoint | matrix | minimum LDL pivot |
|---:|---|---:|
| `-1/200` | `K+tD-(1/2000)I` | `0.0867761483297497` |
| `-1/200` | `I-K-tD-(1/2000)I` | `0.1032787436284628` |
| `1/200` | `K+tD-(1/2000)I` | `0.09915106069628103` |
| `1/200` | `I-K-tD-(1/2000)I` | `0.08791237317479719` |

Since the relevant matrix pencils are affine in `t`, endpoint positivity certifies the whole interval `|t| <= 1/200` for the same `1/2000` spectral-margin certificate.

## H10 comparison

CORRECT as a numerical comparison of frozen high-precision rechecks.

- H10 round18 boundary1 rho: `0.57460693865261042086015327495886367566150672323285968590897042032811118139654128`
- H11 round19 interior1 rho: `0.574594730866466959253898834668613177310983170540497787779334564168201868719667966949403736777980243789014114026206511901`
- H10 minus H11: `0.000012207786143461606254440290250498350523552692361898129635856159909312676873313050596263222019756210985885973793488099`

Interpretation: H11 supports the finite scout claim that a strict-interior spectrum run can nearly attain the current H10 best value.  It does not prove a global optimum, a theorem about all commuting spectral directions, or any positive-gap mechanism.

## Layered verdict

- Input/hash freeze: CORRECT.
- Frozen 4-shard CSV/manifest/log/best JSON accounting: CORRECT.
- Frozen ledger claim “no positive gap and no `rho >= 1` among 20004 rows”: CORRECT.
- Stored source and best-NPZ spectral recomputation: CORRECT, with only harmless float-floor roundoff noted above.
- Strongest 4096-atom exact-event/Möbius gate: CORRECT.
- Three independent chord checks: CORRECT.
- Fraction LDL admissibility for the strongest rationalized affine line on `|t| <= 1/200`: CORRECT.
- Full seed regeneration / independent reconstruction of all 20000 proposal matrices: INCOMPLETE, not performed.
- Scope: SCOUT.  The float search is fixed-`Q` at each center with joint basis/spectrum perturbations; the stored rational line is near-commuting.  This is finite negative evidence and an interior-near-best scout, not a global result.
