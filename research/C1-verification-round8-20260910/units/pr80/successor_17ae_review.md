# Successor 17ae mathematical review

Scoped verdict: the 17ae delta is coherent at the analytic-source level, but its interval-family and neighborhood existence conclusions are conditional on finite-symbolic ingredients that remain SOURCE_ONLY / PENDING_C2. It gives a direct analytic negative-fiber obstruction from formula (2.1) and log positivity, while proposing a complete-interval compensation theorem for an explicit 2+2 family and a coefficient-space correlated neighborhood around the `r=1/8` member. The proof implications have the right strictness, endpoint, and entropy-scope boundaries, but the quantitative constants, event enumerations, pair counts, Gram/log identities, base positive margin, old `s=9/10` recheck, and explicit rational membership remain pending.

## Cross-fiber obstruction

`ADDENDUM_CROSS_FIBER_OBSTRUCTION.md` lines 9-13 correctly define the complete curvature as the complete-law expectation of the square-completed integrand and distinguish a fixed-fiber contribution `C_S` from the second derivative of conditional Shannon entropy alone.

The strictness discussion in lines 15-35 is consistent with the repaired PR80 theorem. The diagonal-pair argument is valid in a finite strict DPP: if a positive-mass atom has nonzero `u` or `y`, then `J(T,T)=4(u(T)^2+y(T)^2)/q(T)>0`, while the cone hypothesis gives nonnegativity for all other pairs. The equality claim under the cone hypothesis is also source-level sound for `s>0`: if equality forces `u=y=0` on all complete events, then `q=1` gives product independence, and the two-coordinate DPP determinant comparison forces every real `B_ij` to vanish. The endpoint statement `H''(0)=0` is properly separated from division by `t^2`.

The negative-fiber family in lines 39-73 is a genuine method obstruction, not an entropy counterexample. The Schur-complement legality argument, the conditional kernel formula for the selected mask, and the exact negative-fiber expression are analytically coherent. The correlated-family variant in lines 91-107 shows that the obstruction is not tied to diagonal marginal blocks. The numerical enclosures and rational-member signs in lines 75-89 and 107 remain author finite evidence pending independent reconstruction.

## Complete-interval compensation theorem

The theorem in `ADDENDUM_CROSS_FIBER_OBSTRUCTION.md` lines 111-180 has a valid analytic shape: it proves a lower bound on `C_tot=t^2 I''`, divides by `t^2=s` only for `t!=0`, and uses the analytic endpoint argument at `t=0`. Since the resulting bound is strictly negative for `H''` away from the single point `t=0`, strict concavity on `[-1,1]` follows once the displayed ingredients are verified.

The inequality chain from lines 154-178 is internally consistent: the window bound for `lambda`, the global Gram relations, and the estimate on `E|z|` combine to produce a positive full-curvature lower bound. This is real cross-fiber compensation because the proof uses complete signed expectations and explicitly does not require every fiber to be positive.

What remains pending is the finite symbolic substrate: the sixteen grouped event probabilities in lines 121-128, the likelihood window in lines 130-140, the Gram relations in lines 142-150, and the log-constant comparisons in lines 164-168. Those are source-only author assertions until independently reconstructed.

## Correlated neighborhood

`ADDENDUM_CORRELATED_NEIGHBORHOOD.md` lines 7-23 correctly remove the apparent endpoint singularity by normalizing `C_tot` as `Gamma(s)=C_tot/s^2` for `s>0` and giving the continuous endpoint value `Gamma(0)=6E_mu a^2`.

The coefficient-neighborhood theorem in lines 25-113 is a legitimate perturbative theorem in coefficient space, not matrix-entry norm. Conditional on the displayed reference bounds and Lipschitz estimates, the proof gives `Gamma>=1/2`, hence `H''(t)<=-t^2/2` for `t!=0`, and uses the analytic endpoint at zero. The selected bad fiber at `s=1/2` is kept negative by a separate one-fiber perturbation bound.

The explicit correlated rational kernel in lines 115-139 is properly framed as a membership application of the coefficient theorem, not a time-grid proof. Its exact coefficient differences, strict Schur check, and direct finite enclosures remain SOURCE_ONLY / PENDING_C2.

The arbitrary-dimensional extension in lines 141-149 is appropriately existential outside the 2+2 quantitative radius. The direct-sum entropy additivity argument and continuity/open-neighborhood argument are sound as an analytic implication: if the base complete-interval positive margin and selected negative fiber are independently certified, then the stated open-class persistence follows by compactness and continuity. The actual existence conclusion therefore remains conditional on the same pending base-margin gate. The source explicitly avoids claiming a uniform dimension-free radius, coverage of all rank-two kernels, or the original 3+3 whole chord.

## README and scope consistency

The updated README is consistent with the earlier source/evidence boundaries:

- Lines 7-13 preserve the old disclosure that the original `s=9/10` outputs are edited summaries, withdraw the old `hi` column as an upper-enclosure claim, and pin the intended PR58 fixture while leaving fixture equality and finite signs pending.
- Lines 15-23 introduce the new cross-fiber and correlated-neighborhood notes while keeping their script outputs as author evidence rather than independent certificates.
- Lines 21-23 state that the new window expression avoids the earlier invalid upper-endpoint convention and that the new outputs are literal saved stdout from author executions. This closes only a documentation/packaging issue; it does not certify the outputs.
- Lines 25-29 keep strictness, historical ratio-test wording, PR70/77 budget, formal status, whole-chord scope, and novelty properly delimited.

References in the source to earlier C1 review text are not used as mathematical evidence in this FIRST delta.

## Still pending

The following are not independently accepted in this review:

- All old `s=9/10` recheck counts, signs, and window bounds reported in `ADDENDUM_CROSS_FIBER_OBSTRUCTION.md` lines 182-191.
- All finite dyadic enclosures in the new output files.
- The claimed final author runtime and final-run status in lines 193-198.
- The exact grouped-event enumeration, Gram sums, log comparisons, and rational constants used in the complete-interval theorem.
- The explicit correlated kernel membership and its direct bad-fiber/full-curvature enclosures.
- Equality between any embedded finite fixture and the cited PR58 source.
- Literature novelty, formal verification, and general dense correlated rank-two whole-chord concavity.

## Final 17ae status

- Strictness and endpoint consistency: source-level PASS.
- Cross-fiber obstruction to universal conditional-fiber positivity: analytic-source PASS, finite examples pending.
- Complete-interval 2+2 compensation theorem: source-level conditional PASS, finite symbolic ingredients pending.
- Correlated 1/40000 coefficient neighborhood: conditional analytic implication accepted; base positive margin and membership constants pending.
- Arbitrary fixed-dimension open classes: conditional direct-sum/compactness/continuity implication accepted; actual existence depends on the same pending base-margin certificate and is not quantitative uniformly in dimension.
- Original 3+3 `s=9/10` whole chord: not newly certified.
- All author scripts/output: SOURCE_ONLY / PENDING_C2.
