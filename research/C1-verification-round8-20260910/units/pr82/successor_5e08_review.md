# PR82 5e08 successor delta FIRST review

Line references use:

- `source-snapshots/pr82_delta/research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p8.md`
- `source-snapshots/pr82_delta/research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p8_correction.md`

Overall status: `ACCEPTED_SCOPED` for the corrected BFG relaxation step, the conditional derivative-memory lemma, the two-power Poisson-loss mechanism, and the `p>8` threshold calculation; `INCOMPLETE_BRIDGE` for the full closed theorem and the finite-memory boundary error; `NEEDS_FIX` for the stale unsuperseded proof paragraph in the main file; no `PENDING_C2`.

## Correction priority

`c4_response_p8_correction.md:L3-L5` explicitly says it supersedes the proof paragraph of Lemma 4.1 in `c4_response_p8.md`. This priority must be honored. The original proof at `c4_response_p8.md:L146-L156` is too compressed because BFG's Theorem 1 controls observables in a variation norm tied to the chosen continuity modulus; it cannot simply be applied to an arbitrary `B_b` observable.

The correction fixes the specific issue:

- `c4_response_p8_correction.md:L18-L30` chooses a decreasing polynomial majorant satisfying the BFG chain condition.
- `c4_response_p8_correction.md:L33-L39` explains how to dominate the canonical continuity sequence while keeping the initial entries below one.
- `c4_response_p8_correction.md:L41-L45` applies BFG Proposition 2(iv) to that polynomial majorant.
- `c4_response_p8_correction.md:L48-L67` uses the first-return probabilities to compare `var_k(F)` with the renewal mass.
- `c4_response_p8_correction.md:L70-L86` obtains Lemma 4.1's relaxation estimate.
- `c4_response_p8_correction.md:L88-L96` correctly says the second Poisson step reruns the coupling with the enlarged majorant for the weaker exponent.

Primary BFG check: BFG states the chain condition with an arbitrary decreasing sequence `gamma_m` and `gamma_0<1`, defines the dominating Markov chain, and proves polynomial return when `gamma_m` is polynomial. Its Theorem 1 proof uses an observable variation term and first-return probabilities. The correction's majorant argument is consistent with those hypotheses.

Scoped status: accepted as a repair of Lemma 4.1, conditional on the stated uniform non-nullness and variation bounds.

## DPP derivative-memory lemma

`c4_response_p8.md:L34-L50` claims that parameter derivatives through order four retain the two-leg exponent. The proof at `c4_response_p8.md:L55-L78` is plausible and source-consistent under its inherited inputs:

- uniform complex-disk `S_q` inverse bounds;
- `S_q` Banach algebra closure;
- affine dependence of `u_t`, `v_t`, and `M_t`;
- strict non-nullness so that `log` stays analytic on a common compact set away from zero.

The resolvent derivative formula at `c4_response_p8.md:L63-L68` and the two-leg propagation argument at `c4_response_p8.md:L70-L78` support the conclusion that no extra memory exponent is lost by differentiating in `t` through order four.

Scoped status: accepted as a conditional lemma. It does not independently reprove the inherited PR66 complex-disk inverse/non-nullness facts.

## Polynomial variation and BFG relaxation

`c4_response_p8.md:L82-L109` defines the `B_b` variation scale and the normalized one-sided transfer operator. This is a suitable framework for the response argument.

`c4_response_p8.md:L111-L132` quotes BFG as the external mixing input. Read alone, the main file's proof of Lemma 4.1 is insufficient for arbitrary `B_b`; with `c4_response_p8_correction.md` applied, the claim is acceptable. The correction avoids importing BFG beyond its primary hypotheses.

Scoped status: accepted only with correction priority.

## Poisson loss and response algebra

`c4_response_p8.md:L158-L217` proves `R:B_b -> B_{b-2}` for `2<b<=a`. The split at `n=m`, the use of the centered relaxation estimate, and the two-power loss are consistent once Lemma 4.1 is repaired.

`c4_response_p8.md:L259-L321` then uses two Poisson losses for a second derivative in `s=t^2`. The exponent bookkeeping at `c4_response_p8.md:L297-L313` is correct: choose `4<b<a`, use

```text
R:B_b -> B_{b-2},  R:B_{b-2} -> B_{b-4},
```

and let the derivative operators preserve the relevant spaces. The response formulas at `c4_response_p8.md:L277-L293` have the standard invariant-measure structure for a normalized transfer operator, with moving-observable terms noted.

The proof at `c4_response_p8.md:L315-L321` remains compressed, but it identifies the needed operator Taylor expansion and uniform remainder domination. For a FIRST source review, this is acceptable as a conditional response lemma because the spaces, losses, and correction priority are explicit.

Scoped status: accepted for the conditional `C^2` response lemma in `s`, not for every inherited DPP input.

## Half-period parity and the `s=t^2` reduction

`c4_response_p8.md:L219-L242` uses the half-period symmetry

```text
T(c-tg)=D T(c+tg) D
```

to identify the real complete-configuration laws for `t` and `-t`, then uses the inherited complex analytic continuation to treat the family as analytic in `s=t^2`. This is correct for complete DPP configuration probabilities: diagonal gauge conjugation preserves finite principal minors and complete-event probabilities, and non-nullness makes the chosen one-sided conditionals compatible.

Scoped status: accepted, conditional on the inherited common analytic continuation for `G_t`.

## Boundary and finite-memory error

`c4_response_p8.md:L323-L342` asserts a quantitative finite-memory boundary error. This is not closed at the same standard as the response lemma.

The missing details are:

- `G_s^{[N]}` is called the canonical memory-`N` truncation at `c4_response_p8.md:L325`, but its normalization, non-nullness, and stationary law are not defined.
- The bound at `c4_response_p8.md:L328-L330` is plausible for tail-freezing a `B_a` function, but the proof is not supplied.
- The transition from kernel/log-kernel truncation to differentiated stationary expectations at `c4_response_p8.md:L333-L339` requires stability of the two Poisson-loss response formulas under the truncated kernels, with constants uniform in `N`.
- The notation `nu_s^{[N]}(F_s^{[N]})` at `c4_response_p8.md:L337` has not been connected to the DPP finite-window or memory approximation used elsewhere.

Scoped status: `INCOMPLETE_BRIDGE`. This does not by itself kill the local infinite-volume response lemma, but it cannot be used as an accepted uniform finite-memory remainder certificate.

## Application to DPP entropy and the claimed `p>8` theorem

`c4_response_p8.md:L344-L367` applies Lemma 6.1 with `a=p/2`, giving the threshold `p>8` for the `C^2` response in `s`. This threshold is correct for the two-Poisson-loss mechanism.

`c4_response_p8.md:L369-L417` then derives strict local concavity of the corrected entropy from three additional inputs:

- `H'(0)=0`, imported from PR66 at `c4_response_p8.md:L369-L373`;
- the quartic expansion coefficient notation at `c4_response_p8.md:L376-L380`;
- a strict lower bound on `A`, imported from accepted PR53 at `c4_response_p8.md:L383-L389`.

The calculus from `H(s)=H(0)-A s^2+o(s^2)` to the `t`-second derivative at `c4_response_p8.md:L392-L417` is correct. The strictness conclusion follows if the imported coefficient lower bound is accepted and if `alpha_k>0`.

However, those strictness inputs are not re-bound or rechecked in this two-file successor delta, and this lane was not authorized to read old PR66/PR53 proof material. Therefore the actual `p>8` theorem at `c4_response_p8.md:L419-L423` is not fully certified by this FIRST review. The response-regularity bridge is accepted scoped; the final theorem is conditional on inherited parity/relative-entropy and PR53 coefficient inputs.

Scoped status: `INCOMPLETE_BRIDGE` for the full theorem as a standalone delta claim; `ACCEPTED_SCOPED` for the new response-regularity mechanism and its `p>8` threshold.

## Tanaka mapping and the original `p>4` theorem

`c4_response_p8.md:L425-L440` says Tanaka is not a black-box repair of `p>4`. This is source-consistent. Tanaka's primary text requires the abstract operator mapping conditions and, for Theorem 2.10, a reduced resolvent bounded both from the first stronger space to the base space and on each stronger space itself. Tanaka's GL comparison includes a strong Lasota-Yorke inequality. The PR82 successor instead has a proved loss

```text
R:B_b -> B_{b-2}.
```

So Tanaka does not close `p>4`.

`c4_response_p8.md:L442-L453` correctly distinguishes the original range: for `p>4`, `a=p/2>2`, enough for one Poisson inverse but not for the second inverse required by this `C^2` in `s` route. The file also correctly states that this is not a counterexample for `4<p<=8`.

Scoped status: accepted.

## Delta verdict

`ACCEPTED_SCOPED`:

- corrected BFG relaxation step;
- conditional derivative-memory lemma through order four;
- two-power Poisson-loss mechanism;
- parity reduction from `t` to `s=t^2`;
- threshold `p>8` for this response mechanism;
- Tanaka non-application to `p>4`.

`INCOMPLETE_BRIDGE`:

- full "frozen PR66 statement valid with `p>8`" theorem, unless inherited PR66/PR53 strictness inputs are separately source-bound and accepted;
- finite-memory boundary/remainder estimate (6.7).

`NEEDS_FIX`:

- add an inline note in `c4_response_p8.md` near Lemma 4.1 that its proof paragraph is superseded by `c4_response_p8_correction.md`, or merge the correction into the main file.

`PENDING_C2`: none. No finite computation or arithmetic contract is needed or authorized.
