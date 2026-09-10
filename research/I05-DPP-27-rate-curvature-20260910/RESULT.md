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

### EXPLICIT UPPER BUDGET (author arithmetic claims; independent finite checks pending)

Under the PR77 conditional-mutual-information derivative and remainder bounds (equations (8.14)--(8.16)), define the explicit rational upper budget

```text
B_R = sum_{r>=R} [A2 + 4(r+1)A1 + (4(r+1)^2+4(r+1))A0]
                    * C0^2 * rho^(4r-12).
sum_{r>=R} |d_r''(t)| <= B_R.
```

Here `A0,A1,A2,C0,rho` are the PR77 constants displayed in `tail_budget.py`. The script sums this explicit majorant; it does not compute the actual absolute curvature tail. This budget discussion concerns the positive interval `t in [1/2,3/2]`. Extending a completed sign certificate to the negative interval additionally uses the physical gauge evenness of the true entropy rate.

The following are retained author decimal displays for `B_R`, with their exact rational comparisons pending independent arithmetic review:

```text
B_18 = 0.005512904463282267...,
B_20 = 0.0007184877398699024...,
B_21 = 0.00025895742050788696...,
B_22 = 0.00009323703026192439...,
B_23 = 0.000033536439712203354...,
B_24 = 0.0000120512043381899....
```

The author program `tail_budget.py` asserts the following comparisons of the explicit upper budget

```text
B_20 > 1/2500,
B_21 < 1/2500,
B_21 > 1/5000,
B_22 < 1/10000.
```

Conditional on verifying those rational comparisons, a finite conditional-curvature upper bound of `-4e-4` on a parameter cell would not be certified negative at the true-rate level by adding this coarse `B_20`; `B_21<4e-4` would suffice for that error comparison. Likewise `B_22<1e-4` would suffice with a finite upper bound of `-1e-4`. A lower bound on `B_R` is not a lower bound on the actual tail: it only shows that this particular upper estimate is too coarse for the stated margin. No minimum necessary depth and no finite or true curvature sign follow from the budget alone.

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

**Prediction-potential / Poisson + finite conditional tail.** Advantage: the PR77 source supplies an explicit true-rate bridge without assuming a hidden finite-state representation. Its independent constants and finite certificates remain pending. The retained author budget displays suggest depths 21--22 could match the example margins above; a proved cell certificate must combine its actual finite upper bound with a validated upper error budget. The budget alone does not rule out smaller depths with stronger finite margins or sharper error bounds.

The methods are complementary rather than interchangeable. A Riccati computation may sharpen the same true-rate error, but a finite value of its stationary-cell curvature without invariant-measure/jet error remains insufficient.

## Primary sources checked

- David Blackwell, *The entropy of functions of finite-state Markov chains* (1957): entropy rate represented through an invariant measure on predictive states for a finite-state hidden Markov source. This supports the conceptual Blackwell-measure route only after a valid representation is proved.
- Guangyue Han and Brian Marcus, *Derivatives of Entropy Rate in Special Families of Hidden Markov Chains*, arXiv:cs/0603059 (2006): derivative formulas and stabilization/analyticity phenomena for special HMM families. Its hypotheses are not assumed for the DPP Schur process.
- Alexandra M. Jurgens and James P. Crutchfield, *Shannon Entropy Rate of Hidden Markov Processes*, arXiv:2008.12886 (2020): emphasizes that predictive-state sets are generically infinite even for finite hidden chains; this is consistent with treating the Schur state as continuous rather than declaring a finite HMM.

These sources are methodological references, not proofs of the DPP-specific bridge.

## Failure ledger

1. **The author common upper budget does not certify whole-interval reuse of the point results.** The displayed `B_18` is over `5e-3`; this concerns the size of an upper estimate, not a proved lower bound for the actual tail. Its exact comparison remains independently pending.
2. **Naive finite-HMM identification is unjustified.** The exact two-site recurrence has a continuous Schur state; no finite closure was proved.
3. **Entrywise inverse decay is not automatically a contraction certificate.** Converting it to a crude matrix-norm bound loses too much; no uniform `<1` state derivative bound is claimed.
4. **A single Jensen gap does not imply pointwise curvature.** PR77's strict midpoint claim still awaits independent finite certification and does not enter the interval sign proof.

## Next exact gate

A complete result needs one of:

- outward intervals for `h_R''(J)` on cells covering `[1/2,3/2]`, together with a validated upper budget `B_R` (or a sharper proved error) satisfying `sup h_R''(J)+B_R<0` on every cell; the depth is determined by this combined margin, with no unconditional `R>=21` requirement; or
- a Riccati invariant-set/contraction/jet certificate giving a sharper total true-rate curvature error and the same strict negative coverage.

Until then the whole-interval claim

```text
h''(t)<0 for every 1/2<=|t|<=3/2
```

is **INCOMPLETE**.
