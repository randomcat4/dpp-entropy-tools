# PR82 C1 FIRST method/localization review

Line references use the public-clean aliases in `frozen_scope.md`.

Overall scoped status: `ACCEPTED_SCOPED` for the local method-obstruction and finite determinant identities; `INCOMPLETE` for the original PR66 arbitrary-center `p>4` theorem; no blocking `NEEDS_FIX`; no necessary `PENDING_C2` computation for this lane.

## Status separation

### ACCEPTED_SCOPED

1. `README.md:L15-L47` correctly preserves the Dobrushin import problem as an applicability gap. A primary-source check of Dobrushin 1974, printed pp. 14--18 and 24--25, supports the A1/A2 split described in `README.md:L21-L25`: the A1 side carries an exponential support-cardinality summability requirement, while the A2 side removes that support-cardinality exponential only with the stronger null-state vanishing condition. This review did not use the old addendum as evidence.
2. `README.md:L104-L184` proves, at source level, a legal half-period-even `A_p` strict-margin center whose inverse Toeplitz kernel has a polynomial lower tail. This excludes a specific uniform exponential inverse-localization mechanism under the bare arbitrary-center `p>4` hypotheses.
3. `README.md:L51-L96` gives a finite determinant-level A2 candidate: for finite positive definite L-ensembles with a spectral contraction domain, Boolean Mobius inversion of the log-determinant trace expansion leaves only closed walks visiting all vertices in the target support.
4. `README.md:L186-L210` correctly lowers the response target from full holomorphic pressure analyticity to a conditional `C^4` physical-parameter response requirement, while leaving the actual theorem as pending source/proof.
5. `README.md:L212-L230` accurately keeps the original PR66 theorem incomplete and states that no entropy counterexample is claimed.

### INCOMPLETE

1. `README.md:L3`, `README.md:L212-L215`: the original PR66 `p>4` theorem is still incomplete.
2. `README.md:L91-L96`, `README.md:L226`: the A2 route lacks the infinite-volume null-state interaction, boundary-term control, complex-neighborhood compatibility, and weighted absolute Dobrushin A2 norm.
3. `README.md:L183-L184`, `README.md:L227`: Lemma 2.1 does not show that the telescoped interaction itself fails A1; additional determinant cancellations remain possible.
4. `README.md:L202-L210`, `README.md:L228`: the finite-response route still lacks an applicable `C^4` response theorem with the needed uniform remainder.

### NEEDS_FIX

No blocking mathematical `NEEDS_FIX` was found in the frozen README under this bounded source review. One editorial caution: `README.md:L21` and `README.md:L47` mention an old internal review/addendum. For a standalone public checkpoint, the direct Dobrushin primary-source page facts should be sufficient without relying on that old review path.

### PENDING_C2

No exact arithmetic or finite enumeration is necessary for the scoped FIRST verdict. If a future finite check is assigned, it should independently instantiate finite positive definite L-ensembles, compute Boolean Mobius coefficients from the finite log-determinant formula, and compare them with the connected closed-walk expression. That would be a sanity check of the finite identity/sign convention only, not a proof of the infinite-volume A2 bridge.

## Per-claim review

### Role, target class, and entropy object

`README.md:L1-L13` labels the branch as a PR66 low-regularity repair checkpoint, states `INCOMPLETE`, fixes the polynomial class

```text
A_p = { u : sum_m (1+|m|)^p |uhat(m)| < infinity }, p > 4,
```

and restricts the intended DPP entropy to true stationary complete-configuration Shannon entropy. This is accepted as a scope statement. It does not certify the PR66 theorem.

### Dobrushin applicability blocker

`README.md:L15-L20` identifies Dobrushin 1974 as the primary source and says the remaining defect is applicability. The direct primary-source check supports the core distinction used at `README.md:L21-L25`: A1 and A2 have different cancellation/summability hypotheses, and A2 is tied to the null-state vanishing condition.

`README.md:L27-L45` then explains why PR66's interval telescope only gives an ordinary first-moment estimate and an endpoint reference-state cancellation. That does not imply the A1 exponential support-cardinality condition, and it does not imply A2's "any coordinate in the null state" vanishing condition. The warning at `README.md:L45` that a generic Boolean Mobius conversion can cost `2^|A|` is a method warning, not a theorem that DPP determinant structure cannot do better.

Scoped status: accepted as preservation of an open external applicability gap.

### Route (i): A2 null-state potential and finite connected walks

`README.md:L51-L59` correctly states that for a binary alphabet with null state `0`, a finite-support interaction vanishing whenever any coordinate is zero must be a coefficient times the product of occupied bits. This makes the A2 repair a quantitative Mobius-coefficient problem, not a gauge relabeling.

`README.md:L63-L74` sets a finite positive definite L-ensemble with `mI <= L <= MI`, defines `gamma=(m+M)/2`, `R=I-L/gamma`, and obtains `||R|| < 1`. In that domain, the finite log-determinant trace series for `log det L_S` is valid.

`README.md:L76-L89` applies Boolean Mobius inversion before taking absolute values. For a fixed finite support, each closed-walk monomial contributes to the Mobius coefficient only when its visited set is exactly the full support; proper visited subsets cancel. The formula is therefore accepted as a finite determinant-level identity, up to the sign convention already acknowledged at `README.md:L87`.

The limitations at `README.md:L91-L96` are essential and correctly stated. Finite marginal L-matrices need not be compressions of the global `K(I-K)^{-1}` operator, and operator-norm convergence of the log series does not supply the absolute weighted sum of `|J_A|` required for Dobrushin A2. Taking absolute values over individual walks introduces a growth constant that is not controlled for an arbitrary strict-margin center.

Scoped status: finite identity accepted; infinite-volume A2 theorem incomplete.

### Route (ii): polynomial lower tail and excluded mechanism

`README.md:L104-L122` constructs a half-period-even Fourier series with coefficients at even frequencies decaying like `(1+r)^-(p+2)`. This belongs to `A_p` because the weighted summand decays summably after multiplying by `(1+2r)^p`.

`README.md:L124-L142` chooses a small epsilon so that `c(theta)=1/2-epsilon a(theta)` is real, half-period-even, in `A_p`, and has a strict spectral margin. The argument uses the absolute summability of the Fourier coefficients and does not depend on numerical search.

`README.md:L144-L159` uses the scalar geometric series for `1/c`. Because all Fourier coefficients of `a` are nonnegative, all convolution coefficients in powers of `a` are nonnegative, so the `k=1` term gives the polynomial lower bound at frequencies `2r`. Thus the infinite inverse Toeplitz kernel `T(c)^-1=T(1/c)` has no exponential off-diagonal bound.

`README.md:L161-L180` transfers any hypothetical finite-section uniform exponential inverse bound to the infinite inverse via coercive Galerkin convergence, then contradicts the polynomial lower tail. This is a valid source-level obstruction to a uniform exponential inverse-entry localization theorem for the complete-event inverse family under only `p>4` and strict margin.

`README.md:L182-L184` correctly limits the conclusion: this does not prove that the actual telescoped interaction fails A1, because determinant cancellations may still occur at the interaction level.

Scoped status: accepted as a mechanism/localization obstruction, not as a DPP entropy theorem counterexample.

### Route (iii): finite response instead of full analyticity

`README.md:L186-L200` observes that a local concavity conclusion for the corrected entropy would follow from `C^4` response, evenness, `h''(0)=0`, and a strict negative quartic coefficient. The displayed expansion `h''(t)=1/2 h^(4)(0)t^2+o(t^2)` is the expected consequence of `C^4` regularity under those hypotheses.

`README.md:L202-L210` properly refuses to import available summable-variation or complete-connection sources as a fourth-order response theorem. This route remains pending source/proof and cannot upgrade the original arbitrary-center `p>4` theorem.

Scoped status: accepted as a conditional target refinement only.

### Current verdict and next gaps

`README.md:L212-L230` is consistent with the bounded review:

- Original PR66 theorem: `INCOMPLETE`.
- New accepted scoped item: the A1 inverse-localization upgrade obstruction at `README.md:L218`.
- New accepted scoped item: the finite determinant Mobius connected-walk candidate at `README.md:L219`.
- New accepted scoped item: the `C^4` response observation at `README.md:L220`.
- No entropy counterexample claimed at `README.md:L222`.
- A2, A1, and finite-response gaps remain exact at `README.md:L224-L228`.
- Independent arithmetic/review is not assumed at `README.md:L230`.

This FIRST review does not assess novelty and does not provide formal verification.
