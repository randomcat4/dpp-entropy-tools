# D10-H12 / round20_interior2 fresh non-author audit

STATUS: CORRECT for frozen stored-data accounting, the strongest-point
independent exact-event gate, the three stored/high-precision chord checks, and
the Fraction LDL strict-feasibility/PSD certificate.

STATUS: SCOUT for the finite 20,000-proposal run and for the H10/H11/H12
interior-margin comparison.

STATUS: INCOMPLETE for full seed regeneration and reconstruction of all
proposal matrices from the random seeds.

No author search module, author gate module, or inherited recheck wrapper was
imported or reused.  The author wrapper `recheck_best_interior2.py` was read
only as part of the frozen artifact set; all numerical reconstruction below is
from the CSV/JSON/NPZ files directly.

## Frozen input hashes

Full hashes are also recorded in `fresh_audit.json`.  The most relevant frozen
inputs are:

| file | SHA256 |
| --- | --- |
| `README.md` | `4BDDBD7C6F1DFBFB10E2E62733371E8FB5DC0DA45A977B498E88EE16C241A720` |
| `commuting_spectral_search.py` | `DD55E9F05AFD128A4E64E06AB705BA031FB0F32F0EA4A44A0169B625B9050A37` |
| `spectral_basis_refine.py` | `28AE523C10184DC1EFFE2F857ADBDAD4156683292F2AD7DA2D281E2AF6AD7268` |
| `interior_source_margin006.npz` | `34A8A9345C094C34AAC0C4C48A5033A58457174DE3D283868F81DBA1C584FA75` |
| `recheck_best_interior2.json` | `449EB10D2FDC7E38BA95BBF27D517CE905B816C2CA5BFE8B9AC98C7FBF53385B` |
| `results_0/candidate_ledger.csv` | `F98CA34583243D74EC4FCDF0C22E9381C3BBFA9BE7ABEC673941E25404831D04` |
| `results_1/candidate_ledger.csv` | `5118935E04554F2319F012CF9C704744F2DD598B157267D6E3C4C3311687ACE7` |
| `results_2/candidate_ledger.csv` | `87CB3E642BEE73857A92B6D8BCD2D9C4EEB35EABCFD4D7F3FC328E70E8F3FF2D` |
| `results_3/candidate_ledger.csv` | `5D1D5A14512D9A3E7E3C725483839CD56B1EA882DF8DF6676726598B2DD18096` |
| `results_1/best_case.npz` | `1B24617DB8D44973A55D4128B0763260A428B4D8227E1ACAEA4378750D9DB439` |

All four run logs, manifests, best JSONs, and best NPZ hashes are preserved in
the JSON output.

## 1. Ledger, manifest, log, and best-case accounting

The independent parser found exactly four shards.  Each shard has:

- `5001` ledger rows: one `index=-1` source row plus `5000` proposal rows;
- one manifest with `proposal_count=5000`,
  `ledger_rows_including_source=5001`, `positive_count=0`, and `exit_code=0`;
- one run log with `1001` JSON lines, maximum `completed=5000`, and a final
  status line exactly equal to the manifest;
- a `best_case.json` row matching the maximum `rho_psd` row in the corresponding
  ledger.

Aggregate stored-data counts:

```text
total ledger rows        = 20004
proposal rows            = 20000
source rows              = 4
non-NO_HIT status rows   = 0
positive chord_gap rows  = 0
rho_psd >= 1 rows        = 0
minimum proposal margin  = 0.05
minimum source margin    = 0.06000000000000005
maximum stored gap       = -0.00050447989029756
```

The strongest stored row is exactly shard `1`, index `2701`, label
`one_basis_rotation`:

```text
rho_psd              = 0.5729410207438331
rho_unrestricted     = 0.5729410207438331
total normalized H'' = -0.42705897925616687
spectrum margin      = 0.05
stored chord gap     = -0.001306562301046199
status               = NO_HIT
```

Thus the frozen accounting claim `4*(1+5000)=20004`, no positive status/gap,
and no `rho>=1` hit is correct for the stored files.

## 2. Strongest NPZ fixed-Q/PSD structure

For `results_1/best_case.npz`, the NPZ fields are exactly
`kernel`, `direction`, `spectrum`, `rates`, and `eigenvectors`, all float64.
After symmetrizing `kernel` and `direction`:

```text
n                                  = 12
max kernel asymmetry               = 2.7755575615628914e-17
max direction asymmetry            = 7.45931094670027e-17
Q orthogonality Frobenius residual = 5.608895842589592e-15
K - Q diag(lambda) Q^T residual    = 1.3397861372173044e-16
D - Q diag(rate) Q^T residual      = 1.1566740628433365e-16
commutator Frobenius residual      = 2.6171340806144584e-15
min spectrum margin                = 0.05
min rate                           = 0.7850511419928959
max rate                           = 1.0
```

So the stored float object is a legal near-machine-precision fixed-eigenvector
spectral-rate K-affine line, with a positive spectral-rate direction.  The
strict rational certificate below is for the symmetrized decimal-rational line;
after rationalization it should be described as near-commuting, not as an
exactly commuting rational line.

## 3. Independent exact-event/Mobius directional Hessian

The fresh script rebuilds all `2^12=4096` inclusion determinants and then
applies Möbius inversion to exact atoms.  It does not use inclusion minors as
atoms.

For each inclusion determinant along `K+tD`, it computes

```text
q_T      = det(K_T)
q'_T     = det(K_T) tr(K_T^{-1}D_T)
q''_T    = det(K_T){tr(K_T^{-1}D_T)^2 - tr((K_T^{-1}D_T)^2)}
```

using 150-digit `Decimal` LDL/solve arithmetic.  Möbius inversion gives
`p_S,p'_S,p''_S`, and then

```text
Fisher       = sum_S (p'_S)^2/p_S
acceleration = -sum_S p''_S log p_S
H''          = acceleration - Fisher
rho          = acceleration/Fisher.
```

Independent strongest-point values:

```text
entropy      = 7.75389598063849416532784951986306292443618884409652562715290835449783115330738569958186843238489849582596640591980704784763551534620636013859432165152
Fisher       = 150.705359365658397446512718889869434870931230224897848998350001117836155977053710655992794314523537084504575000645486182303511977829647577062605077810
acceleration = 86.3452824265265862480854214215835137769723308827377250535489891252919797920947578718315514074695282523081866113679199252585870832333416127462501048581
H''          = -64.3600769391318111984272974682859210939588993421601239448010119925441761849589527841612429070540088321963883892775662570449248945963059643163549729519
rho          = 0.572941020743833606949080185887673473234329021777573756545962212907295922652986539732432361683375603840465400022921547964448306005425740909559871825569
sum p        = 1.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
sum p'       = -1.0984826e-148
sum p''      = -4.5402e-149
min atom     = 3.8682091332133203104007851453621697473585918366989894363088732089815145292319176355455483746945549116858452471218920507080739681477881349771628031e-8
```

The values match the stored/author values to the precision justified by the
float64 NPZ source.  In particular `H''<0`, `rho<1`, and the displayed
`rho≈0.5729410207438331` is independently reproduced.

## 4. Three symmetric entropy chords

Using the same independently reconstructed exact-event entropy, the midpoint
gaps are:

| step | midpoint gap | central second difference |
| ---: | ---: | ---: |
| `0.006369011816615186` | `-0.00130656230104618481173582291847242268615345848266083394059836404041262894839414280258716478331681554356448658452607559552826589016170630544927680037` | `-64.4193012074699878812217293152668988303580703629965251051138641660949595993280868206121354836065557384561529863930921254002280433374495655383560752766` |
| `0.001` | `-0.00003218076608172304978123415556615729719963117456752065260823917496776318471051594700322646983331062620642985388264947412285937107484465464735240547` | `-64.36153216344609956246831113231459439926234913504130521647834993552636942103189400645293966662125241285970776529894824571874214968930929470481094` |
| `0.0001` | `-3.2180045745091411869877613164969948953472403238025852936541260508521686746557682980479529653115713651400368162014085809681540654503478742943607e-7` | `-64.360091490182823739755226329939897906944806476051705873082521017043373493115365960959059306231427302800736324028171619363081309006957485887214` |

All three are strictly negative, and the smaller-step central second
differences converge to the independently computed `H''`.

## 5. Fraction LDL certificate

The script symmetrizes the strongest float matrices and converts entries via
17-digit decimal strings to exact `Fraction`s.  It then performs exact LDL
without floating arithmetic.

Direction certificate:

```text
D positive definite: true
LDL pivot count: 12
minimum D pivot ≈ 0.8362991384327159
```

Strict feasibility on `|t|<=1/200` with margin `1/2000` is certified by
positive LDL pivots for both endpoint matrices
`K+tD-(1/2000)I` and `I-K-tD-(1/2000)I`:

| endpoint | min pivot for `K+tD-margin I` | min pivot for `I-K-tD-margin I` |
| ---: | ---: | ---: |
| `-1/200` | `0.10653443208403632` | `0.11595153751928357` |
| `1/200` | `0.1219302497991355` | `0.10121264120922482` |

Because the affine matrix inequalities are concave/linear in this one
parameter and both endpoint matrices are positive definite after subtracting
the fixed margin, the whole interval is strictly feasible with that certified
margin.  The direction is actually positive definite, hence PSD.

## 6. H10/H11/H12 finite comparison

The best stored ratios from the three relevant rounds are:

| round | best rho | stored spectrum margin | shard/index | status |
| --- | ---: | ---: | --- | --- |
| H10 round18 boundary1 | `0.5746069386526107` | `0.015371444079016916` | `2/4877` | `NO_HIT` |
| H11 round19 interior1 | `0.5745947308664667` | `0.02171078114876157` | `0/4853` | `NO_HIT` |
| H12 round20 interior2 | `0.5729410207438331` | `0.05` | `1/2701` | `NO_HIT` |

H12 is lower than H10 by `0.00166591790877757` and lower than H11 by
`0.0016537101226336004`, retaining about `0.9971007695927168` of the H10
ratio.  This supports the narrow finite statement in the README: the
high-ratio mechanism is still visible in a deeper spectral interior
(`margin>=0.05` for proposals), but increasing the enforced margin may be
attenuating it.  This is only finite SCOUT evidence.  It proves neither
monotonicity in the margin nor any global or continuous optimum statement.

## 7. Command and generated artifacts

Command from repository root:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\dense_hessian\commuting_spectral\results_server_round20_interior2\verifications\fresh_audit.py
```

Exit code: `0`; elapsed time in JSON: `8.363020658493042` seconds.

Generated artifacts:

- `fresh_audit.py`
- `fresh_audit.json`
- `fresh_audit.md`

No author files, shared indexes, or prior results were modified.

## Final layered verdict

- Stored CSV/manifest/log accounting: CORRECT.
- Strongest row identity and best NPZ/hash consistency: CORRECT.
- Independent 150-digit Decimal exact-event/Möbius Fisher/acceleration/Hessian/rho: CORRECT.
- Three symmetric chord midpoint gaps: CORRECT, all negative.
- Fraction LDL PSD direction and `|t|<=1/200` strict feasibility with `1/2000` margin: CORRECT.
- H10/H11/H12 comparison wording: CORRECT as finite SCOUT, with no monotonic/global inference.
- Full seed regeneration and all-proposal matrix reconstruction: INCOMPLETE, not performed in this audit.
