# Primary sources and scope actually used

The bibliography is separated from mathematical acceptance. A cited paper is not evidence that the new bridges in `proof.md`, `finite_range_local_theorem.md`, or `exponential_wiener_extension.md` have been independently reviewed.

## Stationary determinantal processes

1. Russell Lyons and Jeffrey E. Steif, **Stationary Determinantal Processes: Phase Multiplicity, Bernoullicity, Entropy, and Domination**, Duke Math. J. 120 (2003), 515–575, arXiv:math/0204324.

   Used as background for the scalar stationary DPP, the entropy-rate/prediction viewpoint, and regenerative examples associated with reciprocal trigonometric polynomials. It does not state the affine-symbol entropy concavity proved in the new scoped theorem.

2. Russell Lyons, **Determinantal Probability Measures**, Publ. Math. IHES 98 (2003), 167–212, arXiv:math/0204325.

   Theorem 8.1 supplies negative association. In `finite_range_local_theorem.md`, it is applied only to nonnegative decreasing functions of disjoint matched edges; the induction and the subsequent KL tilt are written out there.

3. András Mészáros, **Limiting entropy of determinantal processes**, Ann. Probab. 48 (2020), arXiv:1905.11459.

   Used only to compare random-order conditional-entropy/local-convergence methods. Its limiting-entropy theorem does not give the parameter-curvature sign and does not justify dropping prediction accelerations.

4. Shilei Fan, Lingmin Liao, and Yanqi Qiu, **Stationary determinantal processes: psi-mixing property and L^q-dimensions**, arXiv:1911.04718 (2019).

   This paper proves, in particular, psi-mixing under a strict pointwise margin and an `H^{1/2}` Fourier condition, with a Fourier-tail bound. It is comparison evidence that strict finite-range symbols are strongly mixing. The proofs here do not infer analyticity or curvature merely from psi-mixing; they derive a configuration-uniform complete-event conditional limit directly.

5. Tomoyuki Shirai and Yoichiro Takahashi, **Random point fields associated with certain Fredholm determinants II: Fermion shifts and their ergodic and Gibbs properties**, Ann. Probab. 31 (2003), 1533–1564.

   Consulted for the Gibbs/ergodic viewpoint. No unquoted Gibbs theorem is used to replace the explicit event-matrix argument in the new proof.

## g-measures and transfer operators

6. Peter Walters, **Ruelle's Operator Theorem and g-Measures**, Trans. Amer. Math. Soc. 214 (1975), 375–387, DOI 10.1090/S0002-9947-1975-0412389-8.

   Used for the Ruelle-Perron-Frobenius/g-measure theorem on a mixing finite shift: a strictly positive Hölder normalized `g`-function has a unique `g`-measure and the normalized transfer operator has a simple leading eigendatum. The proof maps the DPP one-sided complete-event conditionals to this hypothesis.

7. Leandro Cioletti and Eduardo A. Silva, **Spectral Properties of the Ruelle Operator on the Walters Class over Compact Spaces**, Nonlinearity 29 (2016), 2253–2278, arXiv:1511.01579.

   Theorem 2.1 supplies the simple maximal eigenvalue and spectral gap for Hölder potentials with exponent in `(0,1)`; Lemma 2.4, Proposition 2.6 and Corollary 2.7 give the operator/dual analyticity framework. With the uniform prior on `{0,1}` and potential `log(2G_s)`, its integral operator equals the normalized sum operator used here. The proof uses this Hölder result, not a gap for the general Walters class. A contour Riesz projection around the simple isolated eigenvalue directly gives the holomorphic normalized eigenmeasure.

The entropy and relative-entropy rate formulas are not imported as a black box. They follow from the finite right-to-left chain rules plus the exponentially summable, configuration-uniform conditional error proved in the branch.

## Gauge-invariant quasifree states and maps

8. Ben Dierckx, Mark Fannes, and Malgorzata Pogorzelska, **Fermionic Quasi-free States and Maps in Information Theory**, J. Math. Phys. 49 (2008), arXiv:0709.1061.

   Used for the standard gauge-invariant quasifree-state representation, covariance transformation under fermionic linear optics, and the distinction between von-Neumann entropy `Tr b(K)` and occupation-basis measurement entropy. The finite formulas used in `proof.md` are also written out there directly.

9. Xingjian Lyu and Kaifeng Bu, **Fermionic Gaussian Testing and Non-Gaussian Measures via Convolution**, arXiv:2409.08180 (2024), especially the balanced fermionic convolution construction and Appendix C.

   The paper proves a von-Neumann entropy inequality for the reduced output of a balanced fermionic beam splitter by unitary invariance and quantum subadditivity. This is equation (5.7) in `proof.md`. It does **not** prove the occupation-measurement inequality `(BS-occ)` in equation (5.6), which is the extra statement required for DPP Shannon entropy. The paper is therefore a bridge source, not a solution of the present problem.

10. N. J. B. Aza, **Entropy Power Inequality in Fermionic Quantum Computation**, arXiv:2008.05532 (2020).

   Consulted as a cross-domain entropy-power route. Its entropy is quantum/von-Neumann entropy of CAR states; it does not control the spatial occupation-basis Shannon entropy.

## Matrix inverse decay

The explicit estimate in Lemma 4.2 of the finite-range proof is proved from the finite Neumann series identity

```text
M^{-1}=M sum_{r>=0}(I-M^2)^r
```

and bandwidth support. No external inverse-decay theorem is required for the stated constants. The exponentially weighted extension obtains a uniform inverse algebra by band truncation followed by another Neumann series.

## Source boundary

No source above is cited for whole-legal-interval concavity. The new scoped theorems are author proofs assembled from the stated standard transfer theorem and the complete derivations in the branch; they have not been independently reviewed. No numerical experiment is promoted to a rate theorem. Main-reviewed PR29/34/39 remain the only accepted repository inputs used as mathematical theorems.