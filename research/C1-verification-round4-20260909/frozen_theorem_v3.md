# Frozen Theorem FR first-review contract v3

This is a separate new PR53 FIRST-review unit. It does not change the
completed original five-file review or the PR54 Section 5 repair closure.

## Immutable source

[New source file](https://github.com/randomcat4/dpp-entropy-tools/blob/abdd660a6c7761c7a8a53cb8671b4d2543530a5c/research/I05-DPP-21-20260909/finite_range_local_theorem.md)
at `abdd660a6c7761c7a8a53cb8671b4d2543530a5c`, parent
`e0688fbb713e55f93acf791b83437ddf2cc06b7f`.
The exact one-commit delta adds only this 473-line file; the original five
files are unchanged. Its downloaded Git blob hash was verified as
`c65a4e22ed6ee5c69d1b084cfd04d8e77e8d6263`.

## The frozen claim

Let c and g be real trigonometric polynomials on R/Z with c half-period
invariant, g half-period anti-invariant and nonzero, and a pointwise strict
margin `0<delta<=c<=1-delta<1`. The mean `mu=integral c` is arbitrary in
(0,1). Choose an odd positive k with nonzero Fourier coefficient of g.
Write `gamma=|g_hat(k)|^2` and
`alpha_k=gamma^2/[8 mu^2(1-mu^2)]`.

Theorem FR asserts that there exists an epsilon>0 on which c+t g is strict
and the true stationary complete-configuration Shannon entropy rate satisfies
concavity of `h(c+t g)+alpha_k t^4` on [-epsilon,epsilon]. This implies
strict local concavity of h. The interval is not claimed explicit or equal
to the whole legal interval. All logarithms are natural.

## Load-bearing audit obligations

- Exact parity mutual information and all-event inverse estimates; no rare
  event deletion, coordinate rotation or entropy surrogate.
- Weighted Schur norm control for complex perturbations, remote-boundary
  resolvent decay, and holomorphy in a fixed Hölder Banach space. Uniform
  convergence of scalar values alone does not establish this holomorphy.
- The precise primary Ruelle-Perron-Frobenius theorem supplying the simple
  isolated eigenvalue, gap and uniqueness on the mixing finite full shift;
  the normalization and positivity hypotheses, and perturbation argument.
- Identification of the stationary DPP with that eigenmeasure and the exact
  entropy/relative-entropy rate formulas, without interchanging volume limits
  and derivatives.
- Zero first derivative in s=t^2, the negative-association matching density
  one-half and exact KL coefficient, and analytic expansion yielding local
  curvature. A quartic deficit alone is insufficient.
- The Rudin-Shapiro example, its strict spectral margin, Wiener norm and
  quartic coefficient, checked against the actual stated PR39 criterion.

Return a separate per-claim CORRECT or CRITICAL_GAPS audit and scoped verdict.
Do not add or weaken assumptions. A precise missing estimate or source
hypothesis is a gap; lack of a finite numerical test is not itself a gap.

## Roles and exclusions

One fresh non-author GPT-5.5/xhigh context owns this first audit and may not
spawn descendants. C3 reserves a fresh second only after its first result.
The original PR53 packet is reported ready after both C3-coordinated reviews,
but PR53 was not merged because this new theorem changed its head.

No duplicate PR54 appendix audit, PR51 review or issue52 computation. The
PR54 Section 5 closure at a1e7f720 is complete and remains recorded; C3's
reported d5c55447 successor changes only two other appendix wordings and
does not change RESULT.md. C1 does not review those appendix changes.

No computation is initially needed or authorized by this freeze. Any
necessary finite load-bearing calculation must first have an exact input,
algorithm/error criterion and bounded plan: one arithmetic thread, at most
8 GiB, initial timeout 600 seconds, explicit stopping condition. C2 owns
large computation. No new formal proof or novelty certification is implied.
