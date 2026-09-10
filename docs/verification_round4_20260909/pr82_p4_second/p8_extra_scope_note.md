# Narrow note on old p8-only extras

This note does not amend `review_report.md`. It only clarifies how to read the old p8 extras that were described there as "NOT COVERED BY p4 / p8-only extras".

Inputs used: only the frozen author/source files already read for this SECOND review. No later live material, other reviews, C3 adjudication, computation, or new proof search was used.

## 1. Old p8 finite-memory derivative convergence `(6.7)`

Verdict: **INCOMPLETE as a complete standalone proof; CONDITIONAL as a plausible p>8 consequence if the missing perturbation details are supplied.**

Source evidence:

- `c4_response_p8.md` lines 323--342 state the finite-memory claim. The file defines the canonical memory-`N` truncation `G_s^[N]`, records the input truncation estimate `(6.6)` at lines 325--330, chooses `b=4+eta` at line 333, and asserts that the two Poisson bounds, resolvent identity, and multilinear response formulas "then give" `(6.7)` at lines 333--339.
- The p8 Poisson mechanism itself is p>8 only: `R:B_b -> B_{b-2}` is stated in `c4_response_p8.md` lines 158--180, and the two nested losses used in response are at lines 297--313.
- The BFG relaxation gap in the old p8 proof was repaired by `c4_response_p8_correction.md` lines 1--7 and 18--86; the correction preserves the p>8 threshold at lines 88--96.

Reason for the verdict:

The source gives the correct kind of ingredients for a p>8 finite-memory perturbation estimate, but it does not spell out the full stability proof comparing the infinite and memory-`N` stationary functionals through the two nested resolvents. In particular, the frozen author text does not fully expand the uniform finite-truncation constants, the finite-versus-infinite reduced resolvent comparison, and the multilinear remainder bounds that would make `(6.7)` a complete proof rather than a compressed assertion.

The later p4 boundary correction does not disprove p8 `(6.7)`, because p8 has extra room `a>4`. It does, however, shows exactly why such a statement must not be imported casually: `c4_response_p4_boundary_correction.md` lines 145--156 explicitly refuse to claim frozen-future stationary response convergence and replace it by finite Poisson cutoff only. Thus `(6.7)` remains an old p8 conditional extra, not an independently certified result from this SECOND review.

## 2. Old p8 full analytic framing

Verdict: **INCOMPLETE if read as full analyticity of the stationary entropy response; CORRECT/CONDITIONAL only for the narrower analytic-kernel/even-parameter setup.**

Source evidence:

- The analytic kernel setup in `c4_response_p8.md` is source-supported at the level of complete-event conditionals: parameter derivatives and common complex disks are inherited from PR66, and the p8 file states the even `s=t^2` transfer-operator family at lines 219--243.
- PR66 source gives the common complex complete-event disk and logarithmic conditional construction in `pr66_source/proof.md` lines 181--205 and 319--333, and half-period evenness through complete-event determinant invariance at lines 469--487.
- But the actual p8 response lemma proves only `C^2` in `s`, not a full analytic perturbation theorem: `c4_response_p8.md` lines 259--321 state Lemma 6.1 as a C2 response lemma, and the application at lines 361--367 says `H(s)` is C2 near `s=0`.
- The old frozen PR66 theorem statement includes "real analytic in `t`" at `pr66_source/frozen_statement.md` lines 72--82, but the proof source routes that analytic entropy statement through an imported one-dimensional response theorem/Dobrushin-style input at `pr66_source/proof.md` lines 457--467.
- The current PR82 README rejects that old Dobrushin import for this low-regularity repair: `README.md` lines 42--46 say the ordinary first-moment bound does not satisfy Dobrushin A1/A2 and that this packet bypasses the pressure theorem.
- Tanaka is also not a replacement analytic theorem here: `c4_response_p8.md` lines 425--440 and `c4_response_p4_repair.md` lines 548--562 both state that Tanaka's same-space reduced-resolvent/GL hypotheses are not established for the present polynomial-memory scale.

Reason for the verdict:

The frozen sources support an analytic complete-event kernel and an even parameterization through `s=t^2`, conditional on the PR66 complete-event inverse/non-null input. They do not, in the old p8 file itself, provide a full analytic theorem for the stationary entropy functional. The p8 finite-response unit supplies the finite differentiability needed for the quartic curvature calculation, and it explicitly frames the response theorem as C2. Therefore any phrase like "p8 analytic framing" should be read as an analytic-kernel/background framing, not as an independently verified full analytic entropy response.

## Clarified status table

| p8 extra | Status in this SECOND clarification | Practical reading |
|---|---|---|
| BFG arbitrary `B_b` relaxation correction | **CORRECT** | `c4_response_p8_correction.md` supplies the missing coupling-majorant bridge. |
| Two-power Poisson route for p>8 C2 response | **CORRECT, conditional on PR66 inputs** | Enough for the p8 local curvature route. |
| `(6.7)` finite-memory derivative convergence | **INCOMPLETE / CONDITIONAL** | Plausible p>8 consequence, but not fully expanded or independently certified here. |
| Analytic complete-event kernel/even `s=t^2` setup | **CORRECT, conditional on PR66 inputs** | Source-supported as kernel-level setup. |
| Full analytic stationary entropy response | **INCOMPLETE** | p8 source proves C2 response; old analytic theorem import remains outside this accepted repair. |
