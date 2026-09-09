# I05 DPP27 — fixed two-harmonic true-rate curvature continuation

Date: 2026-09-10. Base: `main@65e59a46b49cd2dbb5c779a4cfae8cef26441984`.
Parent direction: issue #65 / PR #77. Heavy continuum computation remains issue #74 and is **REQUESTED / PENDING_REVIEW**, not assumed to have run.

Frozen symbol:

```text
f_t(theta)=1/2+(1/4)cos(4*pi*theta)+(t/8)cos(2*pi*theta),
1/2 <= |t| <= 3/2.
```

All entropy is complete-configuration Shannon entropy per original lattice coordinate. No principal-minor probability, von Neumann entropy, L-affine substitute, or finite-window `H_n/n` extrapolation is used.

## Status summary

### PROVED (AUTHOR PROOF; arithmetic identity from PR77 constants, not independent review)

The explicit PR77 conditional-mutual-information curvature tail (its equations (8.14)--(8.16)) implies the following exact tail-only thresholds for

```text
T_R = sum_{r>=R} |d_r''(t)|,
```

uniformly in `t in [1/2,3/2]`:

```text
T_18 = 0.005512904463282267...,
T_20 = 0.0007184877398699024...,
T_21 = 0.00025895742050788696...,
T_22 = 0.00009323703026192439...,
T_23 = 0.000033536439712203354...,
T_24 = 0.0000120512043381899....
```

The exact rational program `tail_budget.py` proves in particular

```text
T_20 > 1/2500,
T_21 < 1/2500,
T_21 > 1/5000,
T_22 < 1/10000.
```

Therefore a continuum certificate based only on the published uniform PR77 tail cannot use the depth-18 point certificates as a whole-interval bridge. If the finite conditional curvature has only a `4e-4` negative upper margin on some parameter cell, depth 20 is analytically insufficient under this coarse common tail, while depth 21 is tail-compatible. For a `1e-4` margin, depth 22 is tail-compatible. These are only necessary/sufficient tail-budget comparisons; they do not assert any finite conditional curvature sign.

### INCOMPLETE_BRIDGE — two-site Riccati / hidden-filter state route

Grouping future coordinates into two-site cells gives the continuous Schur-state update already frozen in issue #74,

```text
F_{alpha,t}(S)=D_alpha(t)-E(t) S^{-1} E(t)^T.
```

This is not, by itself, a finite-state hidden Markov representation. The state `S` ranges over a continuous reachable set. Blackwell's entropy-rate representation for functions of finite-state Markov chains and the Han--Marcus derivative/analyticity theory motivate an invariant-measure/filter approach, but they do not remove the obligation to prove for this DPP:

1. an invariant reachable set for all four branches;
2. positivity/normalization of the four branch weights as the genuine complete two-site conditional probabilities;
3. contraction (or a spectral gap) in one fixed norm/metric on that reachable set, uniformly for `t in [1/2,3/2]`;
4. first and second parameter-jet bounds and the invariant-measure response;
5. the factor `1/2` converting per-cell entropy to entropy per original coordinate.

No finite-state HMM theorem is invoked without those bridges.

A tempting Euclidean derivative bound is

```text
D_S F[Delta] = E S^{-1} Delta S^{-1} E^T.
```

The existing entrywise inverse-decay constant from PR77 controls scalar entries of event-matrix inverses, but it does not by itself give a sharp enough uniform operator norm for every two-site Schur inverse. Hence a global contraction constant below one is **not proved here**. The missing object is an explicit invariant box/cone (or another metric) strong enough to bound `S^{-1}` on the reachable set.

### PROVED INTERFACE — RPF / prediction-potential route already available

PR77's normalized one-sided complete conditional `G_t` has the exact full response

```text
h''=-nu(psi^2)+nu((psi^2-xi)v)-2nu(psi R(psi v)),
v=R log G.
```

This keeps complete Fisher information, acceleration, and invariant-measure response. The direct conditional-mutual-information identity

```text
h''(t)=h_R''(t)-sum_{r>=R} d_r''(t)
```

is a second, structurally different bridge because it needs only a rigorous finite-depth conditional-curvature enclosure plus the explicit tail above; it does not require identifying a finite hidden state.

## Method comparison

**Riccati/filter compression.** Potential advantage: branch-and-bound on a low-dimensional continuous state can replace enumeration of `2^R` words and may yield much sharper local contraction and response constants. Main unclosed step: rigorous reachable-set/contraction/jet certificate for all four branches.

**Prediction-potential / Poisson + finite conditional tail.** Advantage: the true-rate bridge is already explicit and does not assume a hidden finite-state representation. Cost: with the current coarse uniform constants, depth 18 is far too shallow for the weakest observed negative curvature scale; exact tail arithmetic points to depth 21--22 before finite-cell interval margins can plausibly close the theorem.

The methods are complementary rather than interchangeable. A Riccati computation may sharpen the same true-rate error, but a finite value of its stationary-cell curvature without invariant-measure/jet error remains insufficient.

## Primary sources checked

- David Blackwell, *The entropy of functions of finite-state Markov chains* (1957): entropy rate represented through an invariant measure on predictive states for a finite-state hidden Markov source. This supports the conceptual Blackwell-measure route only after a valid representation is proved.
- Guangyue Han and Brian Marcus, *Derivatives of Entropy Rate in Special Families of Hidden Markov Chains*, arXiv:cs/0603059 (2006): derivative formulas and stabilization/analyticity phenomena for special HMM families. Its hypotheses are not assumed for the DPP Schur process.
- Alexandra M. Jurgens and James P. Crutchfield, *Shannon Entropy Rate of Hidden Markov Processes*, arXiv:2008.12886 (2020): emphasizes that predictive-state sets are generically infinite even for finite hidden chains; this is consistent with treating the Schur state as continuous rather than declaring a finite HMM.

These sources are methodological references, not proofs of the DPP-specific bridge.

## Failure ledger

1. **Depth-18 whole-interval reuse fails quantitatively under the common PR77 tail.** `T_18` is over `5e-3`, larger than all three scout curvature magnitudes quoted in issue #74.
2. **Naive finite-HMM identification is unjustified.** The exact two-site recurrence has a continuous Schur state; no finite closure was proved.
3. **Entrywise inverse decay is not automatically a contraction certificate.** Converting it to a crude matrix-norm bound loses too much; no uniform `<1` state derivative bound is claimed.
4. **Single Jensen gap remains irrelevant to pointwise curvature.** PR77's strict midpoint gap is retained as a true-rate theorem but does not enter the interval sign proof.

## Next exact gate

A complete result needs one of:

- outward intervals for `h_R''(J)` on cells covering `[1/2,3/2]`, with `R>=21` or a sharper proved tail so that `sup h_R''(J)+T_R<0`; or
- a Riccati invariant-set/contraction/jet certificate giving a sharper total true-rate curvature error and the same strict negative coverage.

Until then the whole-interval claim

```text
h''(t)<0 for every 1/2<=|t|<=3/2
```

is **INCOMPLETE**.
