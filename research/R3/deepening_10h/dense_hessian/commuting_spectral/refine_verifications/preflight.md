# D10-H4 preflight audit: `spectral_basis_refine.py`

STATUS: **INCORRECT**

Impact scope: narrow but material reporting/ledger bug.  The evaluated
proposal centers are still legal fixed-\(Q\) spectral-rate \(K\)-affine scouts,
and I found no rho-inflation bug in the Hessian formula.  However the initial
source/base center is evaluated and saved as `best_case.npz` but is not written
to the candidate ledger and is not counted in `positive_count`.  If the source
itself is already a float candidate, the manifest can under-report the positive
status.

I sent an immediate warning during the audit because remote shards were already
running.

## Scope

Files read:

- `research/R3/deepening_10h/dense_hessian/commuting_spectral/spectral_basis_refine.py`
- `research/R3/deepening_10h/dense_hessian/commuting_spectral/commuting_spectral_search.py`

Output written:

- `research/R3/deepening_10h/dense_hessian/commuting_spectral/refine_verifications/preflight.md`

No author script was modified.  The smoke check was run inline and did not
write a script or result file.

## 1. Main bug: source/base center not in ledger or `positive_count`

In `spectral_basis_refine.py`, the source center is evaluated first:

- lines 143--145: `base_metrics, base_kernel, base_direction, base_rates =
  evaluate(...)`;
- lines 146--156: those base objects initialize `best_metrics` and are saved
  to `best_case.npz`.

But the ledger and candidate status are only created inside the proposal loop:

- lines 165--166: `positive_count = 0`, `accepted_count = 0`;
- lines 170--204: only proposal indices `0..centers-1` are written to
  `candidate_ledger.csv`;
- lines 186--193: `FLOAT_CANDIDATE` and `positive_count` are computed only for
  proposal metrics.

Consequences:

1. If the source/base center already satisfies
   `rho_psd > 1.0 + threshold` or `chord_gap > gap_threshold`, it is not counted
   in `positive_count`.
2. If no proposal improves on the source, `best_case.npz` is the source, but
   no `best_case.json` is written, because `best_case.json` is only written in
   the proposal-improvement branch at lines 205--219.
3. The manifest status is always `"SCOUT_COMPLETE"` at line 232, so a positive
   base can be present in `best_case.npz`/`best_rho_psd` while the manifest
   still reports `positive_count: 0`.

This is a false-negative / under-reporting bug for candidate status.  It does
not inflate rho.

Recommended minimal fix for the author, not applied here:

- write a base row before the proposal loop, e.g. `index=-1`, `label="source_base"`;
- initialize `positive_count` from the base status;
- write `best_case.json` for the base immediately after `best_case.npz`;
- optionally set manifest status to indicate `FLOAT_CANDIDATE_FOUND` when
  `positive_count>0`.

Preflight action for existing remote shards: inspect `best_rho_psd`,
`best_case.npz`, and whether `best_case.json` exists.  Do not rely only on
`positive_count`.

## 2. Fixed-\(Q\) spectral-rate legality

For each call to `evaluate(basis, spectrum, ...)`, the center is
\[
K=B\operatorname{diag}(\lambda)B^\top
\]
and the direction is
\[
D=B\operatorname{diag}(v)B^\top .
\]
The projectors are built as
```python
projectors = np.einsum("ij,kj->jik", basis, basis)
```
which means
\[
\text{projectors}[j]=B_{\cdot j}B_{\cdot j}^{\top}.
\]
The indexing is correct for spectral-coordinate derivatives.

The line checked by `entropy(kernel ± step * direction)` is therefore
\[
K(t)=B\operatorname{diag}(\lambda+t v)B^\top
\]
for the current fixed basis \(B\).  Even though the outer scout changes \(B\)
from center to center, every individual candidate is still a valid fixed-\(Q\)
spectral-rate affine line, provided the input/source basis is orthonormal.

`givens_perturb` rotates columns by a \(2\times2\) orthogonal Givens block:

\[
(b_a,b_b)\mapsto (c b_a+s b_b,\,-s b_a+c b_b),
\]
so it preserves orthonormality up to floating error when started from an
orthonormal basis.

One caveat: `spectral_basis_refine.py` records
`basis_orthogonality_residual` but does not gate on it.  If a malformed source
NPZ supplied non-orthonormal `eigenvectors`, the spectral-margin step test based
on `spectrum` would no longer be a proof of \(0<K<I\).  This is an input
precondition risk, not a bug for well-formed upstream eigenbasis NPZ files.

## 3. PSD rates and step feasibility

`positive_maximum` returns a strictly positive vector from exponential
coordinates, unless the unrestricted generalized eigenvector is already
one-sign, in which case it returns that vector with positive sign.  After
`rates = rates / rates.max()`, the direction remains PSD:
\[
D=B\operatorname{diag}(\text{rates})B^\top\succeq0.
\]

The step
```python
max_step = min_i min(spectrum_i, 1-spectrum_i) / rates_i
step = min(step_fraction * max_step, 0.01)
```
keeps every spectral coordinate \(\lambda_i\pm step\,v_i\) in \((0,1)\) when
`basis` is orthonormal and `step_fraction<1`.

Inline smoke check:

```text
orth_residual = 3.103353719248244e-16
projector_outer_error = 0.0
rate_min = 0.017097319150925484
rate_max = 1.0
direction_eig_min = 0.0170973191509255
direction_eig_max = 1.0000000000000004
step = 0.01
K_minus_eig_min = 0.19088704467587508
I_minus_K_minus_eig_min = 0.2003673314487806
K_plus_eig_min = 0.20911295532412477
I_minus_K_plus_eig_min = 0.1996326685512192
rho_psd = 0.09348779966606319
chord_gap = -0.0003984577606392925
```

This smoke supports the Givens/projector/PSD/step mechanics; it is not a proof
of search coverage.

## 4. Exact-event Hessian and rho

In `commuting_spectral_search.py`, `event_data` constructs exact configuration
atoms using
\[
p(S)=(-1)^{n-|S|}\det(K-I_{S^c}),
\]
checks the expected determinant sign, and checks normalization.  This is the
right exact-event semantics for entropy atoms.

`restricted_components` computes, for each spectral projector \(P_a\),
\[
\partial_a\log p(S)=\operatorname{tr}(M_S^{-1}P_a),
\]
and
\[
\partial_{ab}^2\log p(S)
=-\operatorname{tr}(M_S^{-1}P_aM_S^{-1}P_b).
\]
Thus for a rate vector \(v\),
\[
H''(v)=-v^\top Fv+v^\top Av,
\qquad
\rho(v)=\frac{v^\top Av}{v^\top Fv}.
\]
The status condition `rho_psd > 1 + threshold` is therefore aligned with
positive Fisher-normalized second derivative.

I found no sign error here and no rho-inflation mechanism in these formulas.

## 5. Heuristic optimizer limitation

`positive_maximum` is an Adam-style heuristic over positive exponential
coordinates plus a few starts:

- all-ones;
- unrestricted one-sign eigenvector when available;
- coordinate starts;
- eight random lognormal starts.

This can miss the true positive-orthant maximum, especially if the optimum is
near a boundary face.  Therefore a no-hit run is only SCOUT evidence.  This is
not a false-positive bug, but it is a possible false-negative mechanism inherent
in the scout design.

Because the author scripts already label these runs as float64 scouts, this
does not by itself make the code mathematically invalid.  It does mean remote
non-hits cannot be read as a certificate.

## 6. Acceptance chain and best-case files

The proposal/acceptance chain itself is coherent:

- proposals are generated from the current accepted base or from the source
  restart branch;
- accepted proposals update `base_basis`, `base_spectrum`, and `base_metrics`;
- the global best is updated from every evaluated proposal, not only accepted
  proposals.

For proposals that improve `rho_psd`, `best_case.npz`, `best_case.json`, and
manifest `best_rho_psd` should agree up to normal run-completion timing.

The exception is the base-center bug above: if the initial source remains best,
`best_case.npz` exists but `best_case.json` may not, and the base status is not
represented in the ledger.

## Final verdict

Overall preflight status: **INCORRECT** because candidate reporting can miss a
positive source/base center.

What remains correct:

- individual evaluated candidates are fixed-\(Q\) spectral-rate \(K\)-affine
  lines, assuming the source basis is orthonormal;
- Givens perturbations preserve orthogonality;
- projector indexing is correct;
- PSD rates and spectral step feasibility are correct under the orthonormal
  basis precondition;
- exact-event Hessian/rho signs are correct;
- no rho-inflation bug was found.

What is affected:

- `positive_count`, `candidate_ledger.csv`, `best_case.json`, and manifest
  status can under-report when the source/base center is already a candidate;
- no-hit claims remain heuristic SCOUT only because `positive_maximum` is not a
  certified global positive-orthant solver.
