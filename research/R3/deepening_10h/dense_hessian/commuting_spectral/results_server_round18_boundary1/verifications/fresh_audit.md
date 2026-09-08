# D10-H10 / round18_boundary1 fresh non-author audit

STATUS: `CORRECT` for the stored-artifact accounting, strongest-point
exact-event/Möbius gate, Fraction-LDL feasibility certificate, and finite
boundary-comparison statement.

Layered status:

- `CORRECT`: four stored shards, manifests/logs/best JSON/NPZ consistency, no
  positive status/gap, strongest row identity, high-precision exact-event
  directional gate, and strict rational endpoint feasibility.
- `SCOUT`: the 20,000-proposal no-hit result and the margin-profile evidence.
  These are finite stored-run facts only.
- `INCOMPLETE`: full seed regeneration, any continuous/global theorem, and an
  exactly rational commuting-line certificate after entrywise rationalization.

No gap was found.

## Scope and independence

I did not import the author's `recheck_best_boundary1.py`, round14 gate, search
module, or refinement module.  The independent script in this verification
directory imports only standard-library modules plus NumPy for NPZ reading and
basic spectral diagnostics.

Audit artifacts:

- `fresh_h10_audit.py`
- `fresh_h10_audit.json`

Command run locally from the repo root, with BLAS/OpenMP thread limits set to
one:

```text
python research/R3/deepening_10h/dense_hessian/commuting_spectral/results_server_round18_boundary1/verifications/fresh_h10_audit.py
```

The actual Python executable was the bundled workspace runtime.  No server or
private connection information is recorded here.

## Exact-event/Möbius method used for the strongest point

For a K-affine line `K(t)=K+tD`, I recomputed inclusion probabilities

```text
q_A(t) = P(A subset Y) = det(K_A(t))
```

and exact atoms by the superset Möbius inversion

```text
p_S(t) = sum_{A superset S} (-1)^{|A|-|S|} q_A(t).
```

Since the strongest `K` is strictly inside `0<K<I`, all principal `K_A` are
nonsingular.  The independent directional jets used

```text
q'_A = det(K_A) tr(K_A^{-1}D_A),
q''_A = det(K_A) (tr(M_A)^2 - tr(M_A^2)),  M_A=K_A^{-1}D_A,
```

then applied the same Möbius transform to `q`, `q'`, and `q''`.  With natural
log entropy,

```text
H'' = - sum_S (p'_S)^2 / p_S - sum_S p''_S log p_S
    = acceleration - Fisher.
```

The Decimal recomputation used precision `120` and exact `Decimal.from_float`
input for the saved float64 NPZ entries, followed by entrywise symmetrization.

## Stored-data accounting

Each of the four shards contains exactly one source row plus 5,000 proposal
rows.

| shard | ledger rows | source rows | proposal rows | non-`NO_HIT` | positive gaps | log completed |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 5001 | 1 | 5000 | 0 | 0 | 5000 |
| 1 | 5001 | 1 | 5000 | 0 | 0 | 5000 |
| 2 | 5001 | 1 | 5000 | 0 | 0 | 5000 |
| 3 | 5001 | 1 | 5000 | 0 | 0 | 5000 |

Aggregate:

- total stored ledger rows: `20004`
- repeated source rows: `4`
- new proposal rows: `20000`
- non-`NO_HIT` rows: `0`
- positive stored midpoint gaps: `0`
- largest stored midpoint gap: `-0.00000382980532620536`
- each run log reaches `completed=5000` and its final manifest JSON matches the
  corresponding `manifest.json`

The strongest stored row is exactly:

```text
shard = 2
index = 4877
label = one_basis_rotation
rho_psd = 0.5746069386526107
spectrum_margin = 0.015371444079016916
status = NO_HIT
```

The shard-2 `best_case.json` matches the max-`rho_psd` ledger row.

## Strongest NPZ structural checks

Strongest NPZ SHA-256:

```text
b923193115a21585351db4350a4da53a622c937f1789d557fbbcd57a1e13b59c
```

Additional checks:

- kernel max asymmetry: `5.551115123125783e-17`
- direction max asymmetry: `5.551115123125783e-17`
- basis orthogonality Frobenius residual: `5.5671437743919595e-15`
- kernel reconstruction residual from saved `Q diag(lambda) Q^T`:
  `1.319074423272752e-16`
- direction reconstruction residual from saved `Q diag(rate) Q^T`:
  `9.944161421311174e-17`
- commutator Frobenius residual: `2.095937958333009e-15`
- `lambda_min(K)=0.032969924406879327`,
  `lambda_max(K)=0.9846285559209839`
- `lambda_min(D)=0.4406274848401995`,
  `lambda_max(D)=0.9999999999999996`

Thus the saved float point is a near-commuting fixed-Q PSD direction, with
strictly positive rates.

## 120-precision exact-event gate

The independently recomputed strongest-point values are:

```text
Fisher       = 94.67774278643894939338862940216977755283809517512677398591512137877775860676633247557654939...
acceleration = 54.40248794105495415884639025419834170002346332975917870656240784824145157104722852288420073...
H''          = -40.27525484538399523454223914797143585281463184536759527935271353053630703571910395269234865...
rho          = 0.5746069386526104204168297451961998599296798398247543325600160168526636805480150378134158604...
min atom     = 2.02787017961527826580911170704803215990576506979876913485596644475572937493534624e-8
```

Möbius consistency residuals:

```text
sum p - 1 = -3.0e-120
sum p'    = -5.62732e-120
sum p''   =  3.97480e-119
```

These values agree with the author-side gate at the level relevant to the
stored float object and keep the signs stable: `H''<0` and `rho<1`.

## Three actual midpoint chords

For `gap(h) = (H(K+hD)+H(K-hD))/2 - H(K)`, all three independently recomputed
exact-event/Möbius gaps are negative.

| step `h` | midpoint gap | `2 gap / h^2` |
|---:|---:|---:|
| `0.0034885350115169567` | `-2.45115755691343020674916104235810383525025143636508664522302230658866819543593393e-4` | `-40.2823734745374067677627468036626262537914884869610513730783250447353856647402931` |
| `0.001` | `-2.01379197051893835626091127339165158966428322315390433503477038254893993433190187e-5` | `-40.2758394103787671252182254678330317932856644630780867006954076509787986866380373` |
| `0.0001` | `-2.01376303453516138925454394872444280532591757044348711069014688773799886307972765e-7` | `-40.2752606907032277850908789744888561065183514088697422138029377547599772615945530` |

The chord signs match the negative second jet; no positive entropy gap is
detected at these actual steps.

## Fraction-LDL feasibility certificate

Separately from the Decimal entropy gate, I interpreted the symmetrized saved
float entries as exact decimal rationals via `Fraction(repr(float_entry))`.
Using no-pivot exact LDL:

- `D` is positive definite; the smallest LDL pivot is approximately
  `0.6094618773284424`.
- At radius `|t|<=1/200` with strict margin `1/2000`, all four exact rational
  matrices pass positive LDL:
  - `K + (1/200)D - (1/2000)I`, min pivot about `0.08061592992196824`
  - `I - K - (1/200)D - (1/2000)I`, min pivot about `0.06651798118795857`
  - `K - (1/200)D - (1/2000)I`, min pivot about `0.06993471539882132`
  - `I - K + (1/200)D - (1/2000)I`, min pivot about `0.08229098622623375`

This proves strict feasibility for the rationalized near-commuting K-affine
line over `|t|<=1/200`.  It does not certify an exactly commuting rational
line, because entrywise rationalization need not preserve exact simultaneous
diagonalization.

## Margin-profile audit

I did not import `margin_profile.py`.  I recomputed the profile directly from
the four proposal ledgers, excluding the four source rows.

The author profile's denominator is correct:

```text
proposal rows = 20000
```

Threshold counts match:

| minimum margin | eligible proposal rows | best row |
|---:|---:|---|
| `0.002` | 20000 | shard 2, index 4877 |
| `0.005` | 18948 | shard 2, index 4877 |
| `0.01` | 9575 | shard 2, index 4877 |
| `0.015` | 1476 | shard 2, index 4877 |
| `0.02` | 351 | shard 3, index 4492 |
| `0.03` | 25 | shard 0, index 466 |
| `0.05` | 0 | none |

Fixed-bin counts and best ratios also match:

| margin bin | rows | best rho | best row |
|---:|---:|---:|---|
| `[0.002,0.005)` | 1052 | `0.5736419781543403` | shard 2, index 631 |
| `[0.005,0.01)` | 9373 | `0.5743571409699975` | shard 3, index 3746 |
| `[0.01,0.02)` | 9224 | `0.5746069386526107` | shard 2, index 4877 |
| `[0.02,0.05)` | 351 | `0.5735366107089594` | shard 3, index 4492 |

The bin counts sum to `20000`.  The four best-bin ratios are non-monotone
across the displayed margin bins.  README/profile wording correctly keeps this
as finite evidence and says it is not a theorem / does not replace a theorem.

## Boundary-comparison statement

The specific statement “the strongest improvement is not driven by moving
closer to the spectral boundary” is supported as a finite stored-run
comparison:

```text
configured margin floor = 0.002
source margin           = 0.010000000000000009
strongest margin        = 0.015371444079016916
source rho              = 0.5740468373613397
strongest rho           = 0.5746069386526107
rho improvement         = 0.0005601012912710
```

The strongest row improves `rho` while moving farther inside than both the
configured floor and the repeated source row.  This does not rule out other
boundary mechanisms and is not a structural theorem.

## Current corrected script boundary

I checked the current `spectral_basis_refine.py` text without importing it.
The present file has the expected source/candidate freezing safeguards:

- source row is written to the ledger;
- source `FLOAT_CANDIDATE` contributes to `positive_count`;
- source candidate NPZ/JSON can be frozen as `candidate_source_base`;
- every proposal `FLOAT_CANDIDATE` gets its own `candidate_*.npz/json`;
- manifest separates `proposal_count` from `ledger_rows_including_source`.

Current script SHA-256:

```text
28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268
```

This audit verifies the current frozen files and current script state.  It does
not retroactively regenerate every seed or certify any run produced by a
different historical script state.
