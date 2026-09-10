# Primary-source map, route comparison, and failure ledger

Status: **AUTHOR SOURCE AUDIT / PENDING INDEPENDENT REVIEW**.

## 1. Load-bearing primary sources

### Fang--Shin 2020: norm-controlled BGS inversion

Q. Fang and C. E. Shin, *Norm-Controlled Inversion of Banach algebras of
infinite matrices*, C. R. Math. 358 (2020), 407--414, DOI
`10.5802/crmath.54`.

Exact use:

- definition of `C^{p_alg,r}(Lambda)`: printed p. 408, equations (2)--(3);
- Banach-algebra and Schur embeddings: printed pp. 409--410, Proposition 1;
- norm-controlled inversion: printed pp. 410--411, Theorem 2.

Parameter map:

```text
Lambda = Z x N subset R^2
p_alg = 1
q_alg = 2
r = Fourier weight exponent > 0.
```

The theorem's condition `r>d(1-1/p_alg)` becomes `r>0`.  The direct sum is
invertible on `l^2` with a uniform inverse norm.  This is the only imported
matrix inverse theorem.  Its norm control, not mere inverse-closedness, is
necessary for the simultaneous family estimate.

### Bressaud--Fernandez--Galves 1999: explicit coupling

X. Bressaud, R. Fernandez and A. Galves, *Decay of correlations for non
Holderian dynamics. A coupling approach*, Electronic Journal of Probability 4
(1999); author PDF at the Toulouse link supplied in the task and arXiv
`math/9806132`.

Exact use:

- ratio condition and maximal coupling: printed pp. 5--8;
- matched-suffix comparison for an arbitrary continuous observable before
  specialization to `V_phi`: equations (5.4)--(5.5), printed pp. 8--9;
- first-return/renewal formula: equations (5.7)--(5.11), printed pp. 8--9.

The new proof needs only summability of the renewal mass, which it derives from
the defective first-return law.  It does not cite BFG as a ready-made
second-response theorem.

## 2. Independent route checks that are not load-bearing

### Fernandez--Maillard 2003/2004

R. Fernandez and G. Maillard, *Chains with complete connections: General
theory, uniqueness, loss of memory and mixing properties*, arXiv
`math/0305026v2`.

The paper gives singleton/LIS consistency, uniqueness criteria, and loss of
memory in a one-sided Dobrushin sensitivity regime.  Its Theorem 5.3 controls
loss of memory through a sensitivity matrix; the paper explicitly notes that
its power-law variation formulation loses one power whereas BFG obtains the
same power.  It does not state the two parameter derivatives of the invariant
law needed here.  More importantly, its one-sided Dobrushin route contains a
small sensitivity condition that is not proved for an arbitrary strict-margin
DPP center.  It is therefore a structurally different cross-check, not a
substitute citation.

### Tanaka 2022

H. Tanaka, *General asymptotic perturbation theory in transfer operators*,
arXiv `2205.12561`.

Tanaka's higher-order conclusions require the specified reduced inverse and
operator-scale hypotheses.  The PR82 polynomial proof only had a one-power
loss, so it correctly did not invoke the same-space version as a black box.
The present endpoint proof instead verifies the two required inversions
explicitly on

```text
V_1 -> V_0 -> C.
```

### Dobrushin 1974

The old PR66 pressure import remains rejected.  Dobrushin's class A1 has an
exponential support-cardinality weight; A2 requires a controlled null-state
interaction.  Neither follows from the old interval first-moment estimate.
No part of the new theorem uses that import.

## 3. Comparison with the frozen PR82 mechanism

The frozen PR82 proof used two reductions:

1. its band-truncation inverse argument obtained an `S_q` inverse only under
   `2q+1<p`;
2. it reduced the two legs to the pointwise estimate `O(j^{-q})`, hence used
   the tail `O(n^{1-2q})`.

Together with two Poisson losses this led to `p>4`.

The new proof changes both points.

First, one norm-controlled inversion is applied to the direct sum of **all**
complete-event matrices.  This gives a common `l^1_p` diagonal envelope and
spends no Fourier exponent.

Second, the product of the two leg envelopes is kept before taking a
pointwise bound:

\[
\sum_j(1+j)^{2p}e(j)^2<\infty.
\]

Thus the conditional derivative variations have a finite first moment when
`p>=1`.  The response is then proved on moment spaces rather than replacing
that information by the borderline class `B_2`.

These are mathematical changes, not a renamed use of the PR82 interface.

## 4. Endpoint and exact remaining gap

At `p=1`, the influence envelope has a finite second moment.  This is exactly
what is needed for

```text
conditional derivatives in V_1,
first Poisson inverse in V_0,
second Poisson inverse in C.
```

The proof therefore includes the endpoint `p=1`.

For `0<p<1`, the general `A_p` assumptions supplied here give only a finite
`2p` moment of the two-leg influence envelope.  They do not imply the finite
second moment used by the two-response lemma.  The centered identity
`D'(0)=0` and the exact quartic coefficient can reduce the work needed to
identify the derivative at the center, but a center expansion alone does not
control the curvature sign at every nearby nonzero parameter.  No convexity
of the DPP relative entropy as a function of `s=t^2` has been proved.

Accordingly:

- `p>=1`: **PROVED by the author proof in this packet**;
- `0<p<1`: **INCOMPLETE**;
- failure of the present second-moment argument is not a DPP entropy
  counterexample and is not claimed to be sharp.

A future improvement below `p=1` must either prove an entropy-specific
cancellation that removes the second Poisson inversion, establish a stronger
common inverse/leg moment than follows from `A_p`, or derive a direct Jensen
inequality for the true configuration entropy rate.  An abstract `g`-chain
counterexample would not disprove the DPP theorem.

## 5. Evidence classes

- Author proof: the two mathematical files in this directory.
- Previously accepted import: the regularity-free PR53 matching inequality.
- External source theorem: Fang--Shin norm-controlled inversion; BFG coupling
  identities.
- Numerical or machine evidence: none used.
- Independent FIRST/SECOND for this new theorem: not yet present.
- Novelty/priority: not assessed.
