# D10-A hazards

STATUS: PROVED

Author hazard log. This is not an independent `CORRECT` verification.

## Event semantics

- The proof never uses \(\det K_S\) as an exact event probability. It uses principal minors only for inclusion probabilities.
- Exact entropy \(H(K)\) is the entropy of the full finite subset law. For strict kernels, exact atoms are positive via the \(L\)-ensemble formula, but the proof of subadditivity itself is purely information-theoretic.

## Equality condition

- Entropy subadditivity gives equality if and only if the block random variables \(Y_A\) and \(Y_B\) are independent.
- Independence of blocks is stronger than zero covariance, but FT-A only needs the easy direction: block independence implies every singleton event across the two blocks is independent.
- For singleton cross events,
  \[
  \Pr(i,j\in Y)=A_{ii}B_{jj}-X_{ij}^2.
  \]
  Therefore any nonzero \(X_{ij}\) breaks independence immediately.

## Empty and small blocks

- If one block is empty, \(X\) is an empty zero matrix and the statement is tautological.
- If a block has size one, the singleton argument is still valid; no rank or genericity assumption is needed.

## Sign symmetry

Replacing \(X\) by \(-X\) is diagonal sign conjugacy of \(K\). All principal minors, exact probabilities, and entropies are unchanged. The proof's obstruction to independence is \(X_{ij}^2\), so no orientation/sign choice is hidden.

## Boundary

- FT-A assumes strict \(0<K<I\), as frozen.
- The information-theoretic inequality itself survives at the boundary, but equality and atom-positivity statements need support-aware conventions. This proof does not claim that extension.

## R3 scope

- FT-A proves a global maximum over the fixed \(A,B\) fiber:
  \[
  H([[A,X],[X^T,B]])\le H(A\oplus B).
  \]
- It does not prove concavity of \(H\) on the full real DPP domain. A general affine \(K\)-chord changes the diagonal block kernels \(A_t,B_t\), and then the marginal entropy terms can also curve.
- It is therefore a useful exclusion/necessary-condition tool: any positive R3 gap cannot be explained by increasing entropy at fixed block marginals; it must involve the balance between block marginal entropy deficits and mutual-information terms.
- It should not be presented as information-theoretic novelty. Entropy subadditivity for finite random variables is classical, and Baccelli--Woo's IEEE ISIT 2016 point-process paper explicitly lists subadditivity for disjoint point-process regions.

## Relation to NS-3

- NS-3's local fourth-order formula is strictly weaker in sign scope but sharper locally.
- FT-A proves the sign globally on the fixed-block feasible section.
- FT-A does not recover the explicit \(c_4\) coefficient or a high-order expansion. For near-decoupling numerical diagnosis, NS-3 remains the sharper tool.

## Quantitative lower-bound caution

The Pinsker/data-processing lower bound
\[
H(A)+H(B)-H(K)\ge 8\max_{i,j}X_{ij}^4
\]
uses natural logarithms and is safe but crude. It should not be used as a sharp certificate, and it does not replace exact entropy/gap interval arithmetic for a claimed positive R3 counterexample.
