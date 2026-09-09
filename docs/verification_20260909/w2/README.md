# W2 PR34 independent review and execution

**ACCEPTED_SCOPED**, frozen head `838c20b12907d94a9d6e023cc03f48c3f3b36c5c`, merged as `66e807ad5825e96932679669b42d16d4cb93832e`. Two fresh nonauthor GPT-5.5 reviewers examined separate mathematical units. These are two scoped reviews, not two reviews of every claim in the entire document. No CI checks were configured.

- [Cyclic strictness audit](cyclic_audit.md): for any measurable real `0<=f<=1` and integer `q>=2`, `h(A_q f)=h(f)` if and only if `A_q f=f` almost everywhere. Each removed Fourier mode gives `h(A_q f)-h(f)>=|fhat(k)|^4`. The stronger bound is half the maximum of the occupied/vacant Bernoulli KL terms in the proof. The negative-association theorem applies to Hermitian non-strict contraction DPPs; the matching is vertex-disjoint and has density one half.
- [Radial quartic audit](radial_quartic_audit.md): for `p=integral f`, `0<p<1`, `h(p+s(f-p))+(4/3)|fhat(k)|^4 s^4` is concave throughout its feasible interval. Boundary values use finite Jensen limits; no entropy-rate derivative is presumed. Nonconstant mean-preserving radial lines are strictly concave.
- The basic diagonal/product-refresh finite entropy and constant-centered entropy-rate concavity in W2 and C3 PR29 is counted **once**. W2's quantitative quartic estimate is an additional result depending on that common theorem. C3's separate fixed-rate certificate is a different object, not another proof of this quantitative theorem.

The integration main additionally checked the displayed mean-changing estimate `-H''>=4 sum_i D_ii^2`, giving `h(a+s u)+2(integral u)^2 s^2` concavity; its extension to diagonal boundary references is the finite regularization argument in the author proof. These are elementary consequences of the audited curvature formula, not a claim about arbitrary nonconstant-centered lines.

## Independent fixed arithmetic

[Plan frozen before execution](FROZEN_COMPUTE.md), [independently written checker](w2_fixed_checks.py), [complete output](w2_fixed_checks.json).

All 15 deterministic cases passed in a fresh review-owned Linux job, one CPU thread, no GPU. The checker constructs exact symbolic principal minors and full event probabilities by Mobius inversion, differentiates them exactly, then evaluates entropy and dissipation with 100 decimal digits. It covers unequal diagonal references with a noncommuting real direction, a non-real Hermitian direction, and a fixed six-point Toeplitz symbol, at parameters including negative values and values greater than one. It checks the full dissipation formula, the quartic curvature bound, and the parity matching entropy bound. Required packages: SymPy and mpmath; run `python w2_fixed_checks.py` in a disposable output directory.

These calculations are high-precision finite checks, not outward interval certificates, infinite-volume extrapolation, or a substitute for the proofs. Exact entropy-rate claims rest on the linked analytic audits.

## Still open

Arbitrary scalar symbol chords and the nonconstant orbit center `c=A_2 f` remain **INCOMPLETE**. Neither midpoint maximality nor cyclic strict comparison supplies concavity along that whole line. The correlated-coordinate selection identity in section 10 is **REFUTED** by its exact two-point counterexample; that example is not an entropy counterexample. Novelty and formal proof certification remain unreviewed.
