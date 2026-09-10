# PR79 C1 FIRST proof review

Line references use the public-clean aliases in `frozen_scope.md`.

Overall scoped status: `NEEDS_FIX` for tail notation and several dependent phrasings; `PENDING_C2` for exact rational threshold comparisons; `INCOMPLETE` for the whole-interval true-rate curvature claim.

## Main findings

### F1. `NEEDS_FIX`: PR79 identifies an upper-budget tail as the actual tail

`RESULT.md:L19-L23` defines

```text
T_R = sum_{r>=R} |d_r''(t)|
```

and `RESULT.md:L27-L43` reports exact values and inequalities for `T_R`. The source actually computes the explicit upper bound obtained from PR77 equation (8.14), not the actual tail.

The predecessor source states only an inequality:

- `source-snapshots/pr77/proof.md:L511-L514`: `|d_r''(t)| <= [ ... ] e_r^2`.
- `source-snapshots/pr77/proof.md:L525-L535`: the closed sums apply to the quadratic-polynomial majorant.

The PR79 code follows that majorant:

- `tail_budget.py:L17-L20` builds the prefactor from the RHS of PR77 (8.14).
- `tail_budget.py:L23-L37` sums that polynomial bound exactly.

Therefore the computed object should be named something like `B_R`, `tail_bound(R)`, or "the explicit PR77 tail budget". The statements `B_21 < 1/2500` and `B_22 < 1/10000`, once exactly checked, are sufficient upper-budget certificates for the actual tail. The lower statements `B_20 > 1/2500` and `B_21 > 1/5000` show only that the current published budget is too coarse at those depths; they do not prove lower bounds on the actual `sum |d_r''(t)|`.

This affects `RESULT.md:L17-L45`, `RESULT.md:L94-L96`, `RESULT.md:L108`, and `RESULT.md:L117-L118`. The logical content can be preserved by replacing `T_R` with a clearly named upper budget wherever the exact values are reported.

### F2. `PENDING_C2`: exact threshold signs and displayed decimals are author output in this lane

`tail_budget.py:L40-L55` is an exact `Fraction` author program with exact assertions at `tail_budget.py:L51-L54`. `run_record.txt:L8-L15` records the expected deterministic output and `PASS`, while `run_record.txt:L17` correctly says this is author output, not independent review.

This C1 FIRST review did not run the program, reconstruct the rational values, or compare exact fractions. The threshold signs and decimal values remain `PENDING_C2`. For C2 acceptance, the author script and its `PASS` may only be comparison material; C2 should independently rebuild the PR77 majorant and closed geometric sums from the frozen source equations.

### F3. `NEEDS_FIX` or explicit clarification: positive interval versus `|t|` scope

`RESULT.md:L9-L10` freezes the symbol on `1/2 <= |t| <= 3/2`, and `RESULT.md:L120-L124` states the still-incomplete target with the same absolute-value interval. The tail statement itself is only asserted "uniformly in `t in [1/2,3/2]`" at `RESULT.md:L25`.

The permitted PR77 source also phrases the direct tail identity uniformly on `[1/2,3/2]` at `source-snapshots/pr77/proof.md:L520-L523`, although its legality estimates cover `|t| <= 3/2` at `source-snapshots/pr77/proof.md:L21-L38`.

Because PR79 does not prove the final interval claim, this is not a false theorem certification. Still, the public text should either restrict the PR79 tail budget discussion to the positive interval or add the explicit symmetry/transport statement needed to cover the negative interval. This is a quantifier hygiene fix.

## Per-claim proof review

### Frozen object and entropy interpretation

`RESULT.md:L6-L13` fixes the two-harmonic symbol and states that all entropy is complete-configuration Shannon entropy per original lattice coordinate. This matches PR77's object at `source-snapshots/pr77/proof.md:L9-L13` and its complete-event convention at `source-snapshots/pr77/proof.md:L1-L3`.

Accepted source-only, with the interval clarification in F3.

### Tail-only budget and depth thresholds

`RESULT.md:L17-L45` claims exact tail-only thresholds and draws the depth 20/21/22 implications. The algebraic skeleton is source-consistent:

- PR77 defines `d_r = h_r - h_{r+1}` as conditional mutual information at `source-snapshots/pr77/proof.md:L411-L415`.
- PR77 derives the curvature tail bridge `h''(t)=h_R''(t)-sum_{r>=R}d_r''(t)` at `source-snapshots/pr77/proof.md:L517-L523`.
- PR77 gives the majorant for `|d_r''(t)|` at `source-snapshots/pr77/proof.md:L511-L514`.
- PR77 gives the closed sums at `source-snapshots/pr77/proof.md:L525-L535`.
- PR79 implements those constants and sums at `tail_budget.py:L3-L15` and `tail_budget.py:L17-L37`.

The bridge logic in `RESULT.md:L45` is correct when read as an upper-budget statement: if a finite-depth interval certificate gives `sup_J h_R'' <= -m` and the proven upper budget satisfies `B_R < m`, then `h'' < 0` on that cell follows from the tail bridge. Conversely, if the available upper budget is larger than the finite margin, that particular coarse certificate cannot close the sign. It does not refute the true sign and does not show the actual tail is large.

Required repair: rewrite the exact values and inequalities as values of the PR77 upper budget `B_R`, not values of the actual `T_R`.

### Riccati/filter compression route

`RESULT.md:L47-L63` correctly refuses to identify the two-site Schur recurrence with a finite-state hidden Markov model. The list of missing obligations is materially complete for a load-bearing Riccati/filter certificate: reachable invariant set, genuine branch probabilities, uniform contraction or spectral gap, parameter-jet and invariant-measure response bounds, and the per-cell to per-coordinate factor.

`RESULT.md:L65-L71` gives the derivative

```text
D_S F[Delta] = E S^{-1} Delta S^{-1} E^T
```

which has the right sign for differentiating `D_alpha - E S^{-1} E^T`. The warning that entrywise inverse decay does not automatically give a sharp operator-norm contraction is appropriate. No Riccati curvature certificate is proved here, and the text does not claim one.

Scoped status: accepted as an incomplete-route ledger, not as a proof of any interval sign.

### RPF / prediction-potential interface

`RESULT.md:L73-L89` cites the normalized one-sided conditional `G_t` formula

```text
h''=-nu(psi^2)+nu((psi^2-xi)v)-2nu(psi R(psi v)).
```

This matches the predecessor derivation at `source-snapshots/pr77/proof.md:L323-L386`. The direct conditional-mutual-information bridge at `RESULT.md:L82-L88` matches PR77's exact tail bridge at `source-snapshots/pr77/proof.md:L517-L538`.

Source-only acceptance is limited to the interface level. If a future proof uses the RPF formula or external linear-response theorem as a load-bearing certificate, the theorem hypotheses must be checked against primary statements. PR79's own `RESULT.md:L98-L104` correctly labels Blackwell, Han--Marcus, and Jurgens--Crutchfield as methodological references rather than DPP-specific bridge proofs.

### Method comparison

`RESULT.md:L90-L97` correctly separates the Riccati/filter route from the prediction-potential plus finite conditional tail route. The statement that a finite stationary-cell curvature without invariant-measure/jet error is insufficient is consistent with the missing obligations at `RESULT.md:L55-L61`.

No defect, except that `RESULT.md:L94-L95` should refer to the current coarse uniform upper budget after F1 is fixed.

### Failure ledger

`RESULT.md:L106-L111` is mostly source-consistent:

- The depth-18 warning at `RESULT.md:L108` is valid as a statement about the PR77 upper budget, not the actual tail.
- The finite-HMM warning at `RESULT.md:L109` follows from the continuous Schur-state discussion at `RESULT.md:L49-L55`.
- The contraction warning at `RESULT.md:L110` follows from `RESULT.md:L65-L71`.
- The Jensen-gap warning at `RESULT.md:L111` matches PR77's statement that the fixed midpoint gap is not a curvature proof at `source-snapshots/pr77/proof.md:L317-L318` and `source-snapshots/pr77/proof.md:L571-L575`.

Required repair: change the first item to say the depth-18 PR77 budget is over `5e-3`.

### Next exact gate and final nonclaim

`RESULT.md:L113-L126` states the correct acceptance gate: either finite-depth outward intervals with enough depth or a Riccati invariant-set/contraction/jet certificate. It also correctly leaves

```text
h''(t)<0 for every 1/2<=|t|<=3/2
```

as `INCOMPLETE`.

The gate must not be read as accepting point certificates or a tail budget alone. A future finite certificate must cover cells whose union is the stated target interval, and must prove `sup_J h_R'' + B_R < 0` on each cell using a proven upper budget `B_R`.

## C2 handoff for exact arithmetic

Frozen input for C2:

- PR79 head `bee0e5b5264ced09feb6403a718e25f835e91d21`.
- `source-snapshots/pr79/research/I05-DPP-27-rate-curvature-20260910/tail_budget.py`, SHA256 `B815A6CFD2F5F4DB3EA122B68EED3D3B23E015E35FC917187F2A249171AD88EE`.
- `source-snapshots/pr79/research/I05-DPP-27-rate-curvature-20260910/run_record.txt`, SHA256 `5DFDE80A909998081E911B3ED60C606306FDAE208245C6A8266976C6678702AF`.
- `source-snapshots/pr77/proof.md`, SHA256 `DBF3A31CC9C9176CCA62C4DBD8ABE3A6B433413390B099EDAE351B6BB1A4DC45`, specifically equations (8.14)--(8.16) at `source-snapshots/pr77/proof.md:L511-L535`.

Acceptance criteria:

1. Independently reconstruct the upper-budget formula from PR77's displayed majorant (8.14), the definitions of `A0`, `A1`, `A2`, `C0`, `rho`, and `q`, and the closed sums (8.16). Do not import the author script as the computational source.
2. Produce exact rational values for the reconstructed budgets `B_R` for `R=18,19,20,21,22,23,24`.
3. Produce exact rational threshold differences for the acceptance-relevant comparisons: `B_20-1/2500`, `1/2500-B_21`, `B_21-1/5000`, and `1/10000-B_22`.
4. Record independent source binding and execution binding for that reconstruction, including the PR77 source hash, PR79 source hash, checker code hash if any checker file is created, command, runtime environment summary, and exit status.
5. Only after the independent reconstruction succeeds, compare its exact values with `tail_budget.py` and `run_record.txt`. The author script's `PASS` is comparison evidence only.
6. Report the accepted quantity as the PR77 upper budget `B_R`, unless PR79 is revised to compute actual `sum |d_r''(t)|`.

This is only a future exact-arithmetic contract suggestion. It does not authorize a new entropy, interval, depth-18--24, or author-script execution job. Until C2 completes an independent reconstruction under those criteria, exact threshold signs and displayed decimal values remain pending.
