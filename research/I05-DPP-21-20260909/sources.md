# Primary sources and scope actually used

The bibliography is separated from mathematical acceptance. A cited paper is not evidence that the new bridges in `proof.md` have been independently reviewed.

## Stationary determinantal processes

1. Russell Lyons and Jeffrey E. Steif, **Stationary Determinantal Processes: Phase Multiplicity, Bernoullicity, Entropy, and Domination**, Duke Math. J. 120 (2003), arXiv:math/0204324.

   Used as background for the scalar stationary DPP, entropy-rate/prediction viewpoint, and regenerative examples associated with reciprocal trigonometric polynomials. It does not state the affine-symbol entropy concavity needed here.

2. Russell Lyons, **Determinantal Probability Measures**, Publ. Math. IHES 98 (2003), arXiv:math/0204325.

   Main already uses Theorem 8.1 for negative association in PR39. The new inverse and beam-splitter reductions do not invoke negative association.

3. András Mészáros, **Limiting entropy of determinantal processes**, Ann. Probab. 48 (2020), arXiv:1905.11459.

   Used only to compare random-order conditional-entropy/local-convergence methods. Its limiting-entropy theorem does not give the parameter-curvature sign and does not justify dropping prediction accelerations.

## Gauge-invariant quasifree states and maps

4. Ben Dierckx, Mark Fannes, and Małgorzata Pogorzelska, **Fermionic Quasi-free States and Maps in Information Theory**, J. Math. Phys. 49 (2008), arXiv:0709.1061.

   Used for the standard gauge-invariant quasifree-state representation, covariance transformation under fermionic linear optics, and the distinction between von-Neumann entropy `Tr b(K)` and occupation-basis measurement entropy. The finite formulas used in `proof.md` are also written out there directly.

5. Xingjian Lyu and Kaifeng Bu, **Fermionic Gaussian Testing and Non-Gaussian Measures via Convolution**, arXiv:2409.08180 (2024), especially the balanced fermionic convolution construction and Appendix C.

   The paper proves a von-Neumann entropy inequality for the reduced output of a balanced fermionic beam splitter by unitary invariance and quantum subadditivity. This is equation (5.7) in `proof.md`. It does **not** prove the occupation-measurement inequality `(BS-occ)` in equation (5.6), which is the extra statement required for DPP Shannon entropy. The paper is therefore a bridge source, not a solution of the present problem.

6. N. J. B. Aza, **Entropy Power Inequality in Fermionic Quantum Computation**, arXiv:2008.05532 (2020).

   Consulted as a cross-domain entropy-power route. Its entropy is quantum/von-Neumann entropy of CAR states; it does not control the spatial occupation-basis Shannon entropy.

## Matrix inverse decay

The explicit estimate in Lemma 4.2 is proved from the finite Neumann series identity

```text
M^{-1}=M sum_{k>=0}(I-M^2)^k
```

and bandwidth support. No external inverse-decay theorem is required for the stated constants.

## Source boundary

No source above is cited for whole-legal-interval concavity. No numerical experiment is promoted to a rate theorem. Main-reviewed PR29/34/39 remain the only accepted repository inputs used as mathematical theorems.
