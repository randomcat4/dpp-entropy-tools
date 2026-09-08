# D10-A verdict

STATUS: PROVED

This is an author verdict, not an independent verification. It must not be reported as `CORRECT` until a fresh verifier audits it.

## Result

FT-A is true.

For every finite real symmetric strict DPP kernel

\[
K=\begin{pmatrix}A&X\\X^T&B\end{pmatrix},
\qquad 0<K<I,
\]

the block marginals are DPPs with kernels \(A\) and \(B\), and

\[
H(K)\le H(A)+H(B)=H(A\oplus B).
\]

Equality holds if and only if

\[
X=0.
\]

Equivalently,

\[
H(A)+H(B)-H(K)=I(Y_A;Y_B),
\]

and \(I(Y_A;Y_B)=0\) exactly when the two block configurations are independent; DPP independence across the blocks is equivalent here to vanishing cross block \(X\).

## What is classical and what is DPP-specific

Classical information theory supplies:

- entropy subadditivity;
- the identity \(H(Y_A)+H(Y_B)-H(Y_A,Y_B)=I(Y_A;Y_B)\);
- equality iff the two finite random variables are independent.

A point-process version of the same subadditivity principle for disjoint regions is also explicitly stated in Baccelli--Woo, "On the entropy and mutual information of point processes", IEEE ISIT 2016, Lemma III.2. I checked the IEEE bibliographic page and a public full-text mirror for the title and lemma location during this run. This supports the conservative positioning: FT-A is not an information-theory novelty claim.

DPP-specific input supplies:

- the block marginal kernels are the principal blocks \(A,B\);
- \(X=0\) makes all inclusion probabilities factor and hence makes the exact law a product;
- if \(X_{ij}\neq0\), the singleton cross inclusion probability
  \[
  \Pr(i,j\in Y)=A_{ii}B_{jj}-X_{ij}^2
  \]
  differs from \(\Pr(i\in Y)\Pr(j\in Y)\), so independence fails.

## Strength over NS-3

NS-3 proves a local near-decoupling expansion with negative fourth-order sign:

\[
H(K_\varepsilon)=H(A\oplus B)-c_4(X)\varepsilon^4+O(\varepsilon^6).
\]

FT-A strictly strengthens the sign conclusion for fixed \(A,B\), because it covers every feasible cross block \(X\), not only small perturbations. FT-A does not replace NS-3's explicit \(c_4\) formula; it only gives the global entropy maximum and equality structure.

## Optional quantitative bound

For nonempty blocks,

\[
H(A)+H(B)-H(K)\ge 8\max_{i\in E_A,j\in E_B}X_{ij}^4.
\]

This follows from data processing to the pair of singleton indicators and Pinsker's inequality. It is a safe, non-sharp global lower bound in natural logs.

## R3 consequence

Any R3 positive gap along a general affine chord must come from movement of the marginal block entropies and their interaction with mutual information. It cannot come from a fixed-\(A,B\) cross-block coupling raising the joint entropy above \(H(A)+H(B)\).

Thus FT-A is best labeled as a DPP kernel-space global search-exclusion corollary: it rules out fixed-block cross-coupling as a positive-gap mechanism and supplies the strict equality condition \(X=0\). It is not a full real-domain concavity theorem and not a counterexample.

## Files read

- `AGENTS.md`
- `research/R3/deepening_10h/problem.md`
- `research/R3/deepening_10h/assumptions.md`
- `research/R3/deepening_10h/frozen_theorem_v1.md`
- `research/R3/deepening_10h/hazards.md`
- `research/R3/deepening_10h/lemma_ledger.md`
- `research/R3/next_structures/decoupling_quartic/proof_candidate.md`
- `research/R3/next_structures/decoupling_quartic/verifications/fresh_reduction.md`

External prior-work check:

- Baccelli--Woo, "On the entropy and mutual information of point processes", IEEE ISIT 2016, DOI `10.1109/ISIT.2016.7541388`; IEEE page checked: https://ieeexplore.ieee.org/document/7541388/
- Public full-text mirror checked for the lemma-location cue: https://www.researchgate.net/publication/306117557_On_the_entropy_and_mutual_information_of_point_processes

No computation was needed. No server was used. No `C:\canglan\` path was accessed. No shared files were modified.
