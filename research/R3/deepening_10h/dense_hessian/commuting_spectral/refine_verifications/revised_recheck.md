# D10-H4 revised recheck: `spectral_basis_refine.py`

STATUS: **CORRECT_FOR_SOURCE_BASE_FIX**

The specific bug from the preflight audit is fixed: the initial source/base
center is now represented in the ledger, in `best_case.json`, in
`positive_count`, and in manifest source fields.

Overall search status remains **SCOUT / INCOMPLETE** as a certificate, because
the positive-orthant optimizer is still heuristic and a separate candidate
freezing boundary remains for chord-gap-only proposal hits.

## Scope

Files read:

- `research/R3/deepening_10h/dense_hessian/commuting_spectral/spectral_basis_refine.py`

Output written:

- `research/R3/deepening_10h/dense_hessian/commuting_spectral/refine_verifications/revised_recheck.md`

No author script was modified.

## 1. Source/base leak is fixed

The revised code now evaluates the source/base center at lines 143--145 and
copies it into `source_metrics` at line 146.  It then computes a source status:

- lines 166--171:
  `source_status = "FLOAT_CANDIDATE"` iff
  `source_metrics["rho_psd"] > 1.0 + threshold` or
  `source_metrics["chord_gap"] > gap_threshold`.

It creates a full source ledger row:

- lines 172--180:
  `index=-1`, `label="source_base"`, zero proposal scales,
  `accepted=True`, all source metrics, and `status=source_status`.

It writes `best_case.json` immediately for the source/base:

- lines 181--183 write `source_row` beside the already-written
  `best_case.npz`.

It initializes the positive counter from source status:

- line 184:
  `positive_count = int(source_status == "FLOAT_CANDIDATE")`.

It writes the source row to `candidate_ledger.csv` before proposal rows:

- lines 186--190:
  header, `writer.writerow(source_row)`, flush.

The manifest now records source and denominator fields directly:

- lines 255--256:
  `proposal_count=args.centers`,
  `ledger_rows_including_source=args.centers + 1`;
- lines 261--263:
  `source_status`, `source_rho`, `source_gap`;
- line 267:
  `positive_count`, now including the source/base candidate if present.

This closes the previous under-reporting bug.  If the source/base is already a
float candidate, it will no longer be invisible to `candidate_ledger.csv`,
`best_case.json`, or `positive_count`.

## 2. Best NPZ / JSON consistency after the fix

For the initial source/base center:

- `best_case.npz` is written at lines 150--157;
- matching `best_case.json` is written at lines 181--183.

For proposal centers that improve `rho_psd`:

- lines 226--240 update `best_metrics`, `best_basis`, `best_spectrum`,
  `best_case.npz`, and `best_case.json` together.

Thus the old “source remains best but `best_case.json` missing” failure mode is
fixed.

## 3. Remaining candidate-freezing boundary

One boundary remains outside the source/base fix.

Proposal status is still defined by either condition:

```python
rho_psd > 1.0 + threshold or chord_gap > gap_threshold
```

but `best_case.npz` is updated only when

```python
metrics["rho_psd"] > best_metrics["rho_psd"]
```

Therefore, a proposal could be counted as `FLOAT_CANDIDATE` solely because its
finite-step `chord_gap` is positive, while not having the largest `rho_psd`.
In that case:

- `positive_count` will correctly increase;
- the CSV row will record the candidate metrics and index;
- but `best_case.npz` may still point to a different, higher-rho center;
- the CSV row does not contain full `basis`, `spectrum`, and `rates`, so the
  exact candidate arrays are not frozen except by deterministic replay.

This is not the previous source/base漏报 bug, and it does not inflate rho.  It is
a reproducibility/freezing risk for gap-positive proposal hits.  If a shard
reports `positive_count>0`, the run owner should inspect the ledger and either
replay the indexed proposal or patch the script to save every
`FLOAT_CANDIDATE` row to a separate NPZ.

## 4. Optimizer coverage boundary remains

The `positive_maximum` routine inherited from `commuting_spectral_search.py`
remains a heuristic positive-orthant search.  It uses a small set of starts and
Adam-style updates in exponential coordinates.  A no-hit run is therefore
SCOUT evidence only, not a certificate that the positive orthant has no
\(\rho>1\) direction.

This boundary is unchanged by the source/base ledger patch and should remain in
any downstream interpretation.

## 5. Revised verdict

Specific patched issue: **CORRECT / RESOLVED**.

Remaining scope:

- source/base status is now counted and ledgered correctly;
- source/base `best_case.npz` and `best_case.json` are now consistent;
- manifest now distinguishes proposal count from ledger rows including source;
- manifest directly records source rho/gap/status;
- no-hit remains heuristic SCOUT;
- gap-positive proposal candidates are counted but not necessarily NPZ-frozen
  unless they also improve best `rho_psd`.

## 6. Addendum: candidate-case freeze patch recheck

STATUS: **PARTIAL**

I rechecked the later local revision that adds per-candidate files under
`candidate_cases/`.

For proposal rows, the previous gap-positive freezing risk is closed.  The code
now does:

- lines 207--212: compute proposal `status` from either
  `rho_psd > 1.0 + threshold` or `chord_gap > gap_threshold`;
- lines 213--214: increment `positive_count` for every proposal
  `FLOAT_CANDIDATE`;
- lines 226--240: for every such proposal, create `candidate_cases/`, then
  write both `candidate_{index:06d}.npz` and `candidate_{index:06d}.json`
  containing `kernel`, `direction`, `spectrum`, `rates`, `eigenvectors`, and
  the row metrics.

Therefore a proposal that is positive only by finite-step `chord_gap`, but does
not set a new best `rho_psd`, is now separately frozen.  The earlier proposal
parameter-freezing risk is resolved for local runs using this revised hash.

One source/base edge remains: `source_status` can itself be `FLOAT_CANDIDATE`,
but the new `candidate_cases/` block is only inside the proposal loop.  The
source/base arrays are initially present in `best_case.npz`; however, if a
later proposal has higher `rho_psd`, `best_case.npz` can be overwritten and the
source/base candidate is then not separately preserved under `candidate_cases/`.
The source row remains in the ledger, but its evaluated `direction/rates` are
not independently frozen except by deterministic replay.

Recommended final small patch, not applied here:

- if `source_status == "FLOAT_CANDIDATE"`, also write
  `candidate_cases/candidate_source_base.{npz,json}` or an equivalent
  `candidate_-000001.{npz,json}` immediately after `source_row` is created.

Remote-batch caveat: the currently running remote shards are on the old hash.
For that batch, if the ledger shows a gap-only candidate that is not the final
best-rho case, the candidate arrays still require deterministic replay; the
local `candidate_cases/` improvement does not retroactively freeze old remote
outputs.

## 7. Final addendum: `candidate_source_base` patch recheck

STATUS: **CORRECT_FOR_LEDGER_AND_CANDIDATE_FREEZE**

I rechecked the current local script after the final source-candidate freezing
patch.

The remaining source/base edge from Section 6 is now closed:

- lines 184--197 execute only when
  `source_status == "FLOAT_CANDIDATE"`;
- the code creates `candidate_cases/`;
- it writes `candidate_source_base.npz` with
  `kernel=base_kernel`, `direction=base_direction`,
  `spectrum=base_spectrum`, `rates=base_rates`, and
  `eigenvectors=base_basis`;
- it writes matching `candidate_source_base.json` from `source_row`;
- this happens before the proposal loop, so later `best_case.npz` overwrites do
  not affect the preserved source candidate file.

Together with the proposal-candidate block at lines 240--254, the current local
hash now freezes every `FLOAT_CANDIDATE` class:

1. source/base candidate: `candidate_source_base.{npz,json}`;
2. proposal candidate by `rho_psd`: `candidate_INDEX.{npz,json}`;
3. proposal candidate by finite-step `chord_gap`: `candidate_INDEX.{npz,json}`;
4. best-by-rho case, independently: `best_case.{npz,json}`.

Final local layered status:

- source/base ledger row and `positive_count`: **CORRECT / RESOLVED**;
- source/base candidate parameter freeze: **CORRECT / RESOLVED**;
- proposal gap-only candidate parameter freeze: **CORRECT / RESOLVED**;
- best-case NPZ/JSON consistency: **CORRECT** for completed local runs;
- fixed-\(Q\), PSD-rate, projector, step-feasibility, and rho semantics:
  unchanged from preflight, no bug found;
- no-hit interpretation: still **SCOUT / INCOMPLETE**, because
  `positive_maximum` is a heuristic optimizer and finite search is not a
  coverage certificate.

Remote-batch caveat remains: any remote shards already running on the old hash
will not have these new `candidate_cases/` files.  If those old runs report a
candidate row not captured by their final `best_case.npz`, deterministic replay
is still required for that batch.
