# Primary sources and exact roles

A bibliography entry is not an independent review of the new proof. The fixed midpoint theorem, Poisson reduction, and curvature-tail lemma in this branch are author results until separately audited.

## Stationary determinantal processes

1. Russell Lyons and Jeffrey E. Steif, **Stationary Determinantal Processes: Phase Multiplicity, Bernoullicity, Entropy, and Domination**, Duke Math. J. 120 (2003), 515–575; arXiv:math/0204324.

   Used for the stationary scalar DPP framework and entropy-rate background. It does not state the fixed-path Jensen certificate or the curvature theorem sought here.

2. Russell Lyons, **Determinantal Probability Measures**, Publ. Math. IHES 98 (2003), 167–212; arXiv:math/0204325.

   Background for complete finite DPPs and negative association. The new midpoint certificate does not need to delete or project events; it enumerates every complete event directly.

3. András Mészáros, **Limiting entropy of determinantal processes**, Ann. Probab. 48 (2020); arXiv:1905.11459.

   Comparison source for entropy limits and local conditional approaches. The true-rate error in this branch is proved directly from complete-event conditional influence; no finite-window trend is inferred from this paper.

## Ruelle operators, normalized g-functions, and linear response

4. Peter Walters, **Ruelle's Operator Theorem and g-Measures**, Trans. Amer. Math. Soc. 214 (1975), 375–387.

   Primary source for normalized positive `g`-functions and the transfer-operator description of their invariant measures.

5. David Ruelle, **Differentiation of SRB States**, Comm. Math. Phys. 187 (1997), 227–241.

   Primary linear-response reference. The present one-sided finite-alphabet formula is derived explicitly from `nu L=nu` and the centered Poisson resolvent; no sign is imported from Ruelle's theorem.

6. Paolo Giulietti, Benoit Kloeckner, Artur O. Lopes, and Diego Marcon, **The Calculus of Thermodynamical Formalism**, J. Eur. Math. Soc. 20 (2018), 2357–2412; arXiv:1508.01297.

   Primary modern source for differentiability/analyticity of Gibbs data, Poisson equations, and correlation-response formulas. Equations (7.3), (7.9), and (7.11) in `proof.md` are nevertheless rederived with the normalization conventions used here.

7. Leandro Cioletti and Eduardo A. Silva, **Spectral Properties of the Ruelle Operator on the Walters Class over Compact Spaces**, Nonlinearity 29 (2016), 2253–2280; arXiv:1511.01579.

   Used only for the spectral-gap/Riesz-projection background already present in the accepted PR53 machinery. The fixed finite-memory tail in this branch is also derived directly, so a negative finite-state result is not promoted without its error bound.

## Mixing comparison

8. Shilei Fan, Lingmin Liao, and Yanqi Qiu, **Stationary determinantal processes: psi-mixing property and L^q-dimensions**, arXiv:1911.04718.

   Comparison evidence for mixing of strict regular stationary DPPs. Psi-mixing alone is not used as a curvature theorem and does not replace the configuration-uniform event-inverse estimates.

## Fermionic operator comparison

9. Ben Dierckx, Mark Fannes, and Malgorzata Pogorzelska, **Fermionic Quasi-free States and Maps in Information Theory**, J. Math. Phys. 49 (2008); arXiv:0709.1061.

   Source for the gauge-invariant quasifree-state covariance transformation and the fact that the occupation diagonal is the complete DPP law.

10. Xingjian Lyu and Kaifeng Bu, **Fermionic Gaussian Testing and Non-Gaussian Measures via Convolution**, arXiv:2409.08180.

    Source for the balanced fermionic convolution comparison. Its entropy inequality is von Neumann/spectral. It does not establish the classical occupation-Shannon gain in `proof.md` Section 9.

## Repository inputs used within accepted scope

- `docs/verification_round3_20260909/accepted_pr53.md`: accepted local exponentially weighted Fourier entropy-rate result and its complete-event/RPF infrastructure.
- `docs/verification_20260909/w2/radial_quartic_audit.md`: accepted constant-centered whole-legal-line quartic strengthening.

PR59 is read as an unreviewed author manuscript only. The Poisson formula needed here is independently rederived, and no new theorem inherits PR59's status.

## Computational source boundary

The fixed entropy certificate uses only exact integer arithmetic plus the correctly rounded `decimal`/libmpdec logarithm contract with an explicit outward enlargement. No external numerical table, floating Hessian, or sampled rate is a premise. Broader novelty and publication priority are not assessed.