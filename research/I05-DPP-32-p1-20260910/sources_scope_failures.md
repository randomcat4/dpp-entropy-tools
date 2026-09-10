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

The theorem's condition `r>d(1-1/p_alg)` becomes `r>0`. The direct sum is
invertible on `l^2` with a uniform inverse norm. This is the only imported
matrix inverse theorem. Its norm control, not mere inverse-closedness, is
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

The proof uses only the displayed coupling objects and derives summability of
the defective renewal mass. It does not cite BFG as a ready-made first- or
second-response theorem.

## 2. Independent route checks that are not load-bearing

### Fernandez--Maillard 2003/2004

R. Fernandez and G. Maillard, *Chains with complete connections: General
theory, uniqueness, loss of memory and mixing properties*, arXiv
`math/0305026v2`.

The paper gives singleton/LIS consistency, uniqueness criteria, and loss of
memory in a one-sided Dobrushin sensitivity regime. Its Theorem 5.3 controls
loss of memory through a sensitivity matrix; the paper explicitly notes that
its power-law variation formulation loses one power whereas BFG obtains the
same power. It does not state the parameter derivatives of the invariant law
needed here. More importantly, its one-sided Dobrushin route contains a small
sensitivity condition that is not proved for an arbitrary strict-margin DPP
center. It is a structurally different cross-check, not a substitute citation.

### Tanaka 2022

H. Tanaka, *General asymptotic perturbation theory in transfer operators*,
arXiv `2205.12561`.

Tanaka's higher-order conclusions require the specified reduced inverse and
operator-scale hypotheses. The present proof verifies the two needed
inversions explicitly on

```text
V_1 -> V_0 -> C
```

instead of claiming that summable variation supplies the hypotheses of a
general perturbation theorem.

### Dobrushin 1974

The old PR66 pressure import remains rejected. Dobrushin's class A1 has an
exponential support-cardinality weight; A2 requires a controlled null-state
interaction. Neither follows from the old interval first-moment estimate. No
part of either new theorem uses that import.

## 3. Comparison with the frozen PR82 mechanism

The frozen PR82 proof used two reductions:

1. its band-truncation inverse argument obtained an `S_q` inverse only under
   `2q+1<p`;
2. it reduced the two legs to the pointwise estimate `O(j^{-q})`, hence used
   only the tail `O(n^{1-2q})`.

Together with two Poisson losses this led to `p>4`.

The new proof changes both points.

First, one norm-controlled inversion is applied to the direct sum of **all**
complete-event matrices. This gives a common `l^1_p` diagonal envelope and
spends no Fourier exponent.

Second, the product of the two leg envelopes is kept before taking a
pointwise bound:

\[
\sum_j(1+j)^{2p}e(j)^2<\infty.
\]

Thus the conditional derivative variations have a finite first moment when
`p>=1`, which closes two response orders on moment spaces. When `p>=1/2`, they
have summable variations, which closes one response order and identifies the
centered Fisher coefficient.

These are mathematical changes, not a renamed use of the PR82 interface.

## 4. Endpoint accounting

### Local concavity endpoint

At `p=1`, the influence envelope has a finite second moment. This is exactly
what is needed for

```text
conditional derivatives in V_1,
first Poisson inverse in V_0,
second Poisson inverse in C.
```

The local corrected-concavity theorem therefore includes `p=1`.

### Centered Fisher endpoint

At `p=1/2`, the influence envelope has a finite first moment. Consequently the
conditional score lies in `V_0`, one Poisson inverse is bounded into `C`, and
normalization collapses the center Poisson term. This proves

\[
h(c+t g)=h(c)-\frac12\mathcal I_s(0)t^4+o(t^4)
\]

and the full conditional Fisher representation at the endpoint `p=1/2`.
It does not give nearby curvature.

## 5. Exact remaining gaps

For `1/2<=p<1`, the second moment of the general two-leg influence envelope is
not implied by `A_p`. The author proof therefore establishes the centered
quartic coefficient but not the continuity of the second `s` response needed
for local concavity.

For `0<p<1/2`, the general envelope need not even have the first moment used by
the one-response Fisher proof. This is a limitation of the present estimates,
not a DPP entropy counterexample.

Accordingly:

- `p>=1`: local corrected concavity **PROVED by the author packet**;
- `p>=1/2`: centered quartic/Fisher expansion **PROVED by the author packet**;
- `1/2<=p<1`: local corrected concavity **INCOMPLETE**;
- `0<p<1/2`: even the present general Fisher-response bridge is
  **INCOMPLETE**;
- no sharpness or entropy counterexample is claimed.

A future local-concavity improvement below `p=1` must either prove an
entropy-specific cancellation that removes the second Poisson inversion,
establish a stronger common inverse/leg moment than follows from `A_p`, or
derive a direct Jensen inequality for the true configuration entropy rate. An
abstract `g`-chain counterexample would not disprove the DPP theorem.

## 6. Evidence classes

- Author proofs: the localization, moment-response and centered-Fisher files.
- Previously accepted import: the regularity-free PR53 matching inequality.
- External source theorem: Fang--Shin norm-controlled inversion; BFG coupling
  identities.
- Numerical or machine evidence: none used.
- Independent FIRST/SECOND for these new theorems: not yet present.
- Novelty/priority: not assessed.
