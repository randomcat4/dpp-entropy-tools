# PR82 dependency follow-up FIRST frozen scope

## Frozen object

This is a pure-source dependency follow-up for the PR82 successor `p>8` application. It does not re-run the already completed 5e08/e91c analytic review and does not re-review the original `p>4` theorem.

Frozen dependency binding read:

* `source-snapshots/pr82_dependencies/SOURCE_BINDING.json`

Frozen source files read:

* `source-snapshots/pr82_dependencies/research/I05-DPP-25-20260909/frozen_statement.md`
* `source-snapshots/pr82_dependencies/research/I05-DPP-25-20260909/proof.md`
* `source-snapshots/pr82_dependencies/research/I05-DPP-25-20260909/equilibrium_bridge.md`
* `source-snapshots/pr82_dependencies/research/I05-DPP-21-20260909/proof.md`
* `source-snapshots/pr82_dependencies/research/I05-DPP-21-20260909/finite_range_local_theorem.md`
* `source-snapshots/pr82_dependencies/research/I05-DPP-21-20260909/exponential_wiener_extension.md`

The frozen metadata identifies the PR66 sources at commit `af1edaad69c4e1f5e4bbd1239b8463b56bf64075` and the accepted-main PR53 sources at commit `65e59a46b49cd2dbb5c779a4cfae8cef26441984`. No verification logs, old review reports, SECOND reports, C3 opinions, live heads, or later sources are included in this follow-up.

## Review target

The assigned question is whether pure author/proof sources genuinely support the imports used by `source-snapshots/pr82_delta/research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p8.md`, especially:

1. PR66 complex-disk complete-event inverse and non-nullness inputs;
2. PR66/PR53 parity and `H'(0)=0` inputs;
3. PR53 regularity-free matching quartic lower bound;
4. the exact effect of those imports on the 5e08 `p>8` application.

This follow-up preserves the finite-memory boundary/remainder defect at 5e08 lines 323--342, especially formula (6.7), as a separate quantitative finite-memory comparison claim. The dependency source binding itself does not close that bridge. After re-checking 5e08 lines 259--342 and 344--423, (6.7) is not cited by the main Section 7 application as written: Lemma 6.1 ends with its own QED at lines 295--321, and Section 7 proceeds directly from `h=-nu(logG)` and Lemma 6.1 at lines 346--367.

## Method and exclusions

I performed source reading and ordinary analytic reasoning only. I did not run author code, independent checkers, mathematical scripts, finite computations, entropy jobs, interval jobs, or formal tools. I did not construct a new theorem route.

## Scoped outcome

### ACCEPTED_SCOPED main claim

The main qualitative successor claim is **ACCEPTED_SCOPED**:

> Under the PR66/5e08 standing hypotheses with `p>8`, strict margin, half-period-even center `c`, half-period-odd nonzero direction `g`, an odd `k` with `g_hat(k) != 0`, the corrected BFG proof priority from `c4_response_p8_correction.md`, and the Lemma 6.1 `C^2` response mechanism, the corrected local functional
> `t -> h(c+t g)+alpha_k t^4`
> is locally concave on a nonempty symmetric interval around `0` and strictly concave away from the center.

This acceptance is qualitative and local. It does not include an explicit radius, whole-legal-interval concavity, formalization, novelty, arithmetic verification, the separate finite-memory estimate (6.7), or the full original PR66 frozen statement if read to require real analyticity beyond the `C^2` response used by 5e08.

### ACCEPTED imports supporting the main claim

* **Complex-disk complete-event inverse and non-nullness.** PR66 proof lines 50--205 prove a dimension-free complete-event inverse gap, a weighted Schur inverse bound, and a common complex parameter disk. PR66 proof lines 207--318 derive the one-sided Schur-complement influence estimates, and lines 319--333 derive uniform non-nullness/logarithm control on a smaller disk. These are internal matrix/conditional estimates, not consequences of the later Dobrushin import.
* **True conditional entropy identification `h=-nu(logG)`.** PR66 proof lines 391--404 identify the uniform limit of finite Schur complements with the true future conditional and use the stationary finite-alphabet entropy formula. PR66 equilibrium bridge lines 13--20 and 52--67 record the same identification. Together with non-nullness/log control at PR66 proof lines 319--333, this legitimately gives the source-level `h(t)=-nu_t(log G_t)` input used at 5e08 lines 346--350.
* **Parity/evenness.** PR66 proof lines 469--513 establish the half-period diagonal gauge, evenness in the parameter, the `s=t^2` factorization, and the entropy-rate pressure formula in the source proof. PR53 finite-range source lines 54--87 independently record the same finite parity identity and exact entropy-deficit relation without differentiating finite-window limits.
* **Matching quartic lower bound is regularity-free.** PR53 finite-range source lines 88--143 prove the finite matching KL lower bound using parity, fixed marginals, negative association, and the variational characterization of relative entropy. PR53 exponential extension lines 233--253 explicitly state that the finite parity identity and matching argument do not require finite range. PR66 proof lines 560--589 imports the same bound and identifies the coefficient `A >= C_k`.

### CONDITIONAL imports

* **`H'(0)=0`.** The source support is real but conditional on having a valid differentiable entropy-rate/response representation in the replacement p>8 mechanism. PR66 proof lines 515--558 and equilibrium bridge lines 175--215 show the cancellation once the pressure/response identity is available. PR53 finite-range source lines 343--397 gives the same cancellation through the normalized `G_s` formula. Thus this import is no longer a missing PR66/PR53 dependency. Its condition is the Section 7 chain `h=-nu(logG)` plus Lemma 6.1's `C^2` response, not the optional finite-memory comparison (6.7).

### MISSING / still open

* **5e08 finite-memory boundary/remainder bridge, as a separate claim.** The dependency sources do not prove 5e08 formula (6.7). If retained, that estimate still needs a precise canonical truncation, stationary-law comparison, and uniform constants through two parameter derivatives. However, after line-level dependency clarification, this is not a necessary gate for the main Section 7 application unless the proof chooses to route through finite-memory approximants.
* **External Dobrushin applicability for the original PR66 `p>4` theorem.** PR66 proof lines 457--467 and equilibrium bridge lines 147--159 still rely on the imported Dobrushin finite-first-moment analyticity theorem. This follow-up does not re-audit that external theorem or close the original `p>4` statement. The point here is only that this external gap does not invalidate the independent PR66 internal matrix/conditional estimates used by 5e08.

## Effect on the 5e08 p>8 application

The dependency follow-up removes the prior avoidable uncertainty about inherited PR66/PR53 source support. The complex-disk inverse/non-nullness input, true conditional entropy identification, parity/evenness input, `H'(0)=0` conditional cancellation, and regularity-free matching quartic floor are supported by the frozen author/proof sources at the scoped level described above.

The finite-memory boundary/remainder estimate (6.7) remains unproved, but it should not be described as the load-bearing blocker for Section 7 as written. The actual Section 7 dependency chain is: true one-sided conditional entropy formula at lines 346--350, Lemma 6.1 at lines 261--321 applied with `a=p/2>4` at lines 353--367, the `H'(0)=0` cancellation at lines 369--373, and the regularity-free matching floor at lines 383--389.

The main qualitative p>8 corrected-local-concavity claim is therefore accepted at scoped FIRST level. The accepted scope is narrower than a literal reading of 5e08 line 421 as the full frozen PR66 statement with real analyticity; 5e08 proves the `C^2` local response needed for the corrected concavity argument, not a stronger analytic theorem.

## Status buckets

* `ACCEPTED_SCOPED`: main qualitative p>8 corrected-local-concavity claim under the standing hypotheses and correction priority; PR66 internal inverse/non-nullness; `h=-nu(logG)` source identification; parity/evenness; PR53 regularity-free matching quartic lower bound.
* `CONDITIONAL`: `H'(0)=0`, conditional on the 5e08 true entropy-rate formula and Lemma 6.1 response, not on (6.7).
* `INCOMPLETE_EXTRA`: 5e08 finite-memory boundary/remainder estimate (6.7) as a separate quantitative claim.
* `INCOMPLETE_UNCHANGED`: original PR66 external Dobrushin import and arbitrary-center `p>4` theorem.
* `PENDING_C2`: none.
* `NEEDS_FIX`: no new text/code fix beyond the already recorded correction ordering; if (6.7) remains in the source as a quantitative claim, it should be proved or labeled as an additional unproved comparison rather than used implicitly as a theorem gate.
