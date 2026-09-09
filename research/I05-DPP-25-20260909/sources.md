# Sources and dependency audit

## Repository baseline

1. [`docs/research_status.md`](../../docs/research_status.md). Current-main status ledger; it records PR53 as the accepted local entropy-rate theorem and separates it from later unreviewed extensions.
2. [`docs/verification_round3_20260909/accepted_pr53.md`](../../docs/verification_round3_20260909/accepted_pr53.md). Accepted quantifiers and coefficient.
3. [`research/I05-DPP-21-20260909/finite_range_local_theorem.md`](../I05-DPP-21-20260909/finite_range_local_theorem.md), [`exponential_wiener_extension.md`](../I05-DPP-21-20260909/exponential_wiener_extension.md), [`proof.md`](../I05-DPP-21-20260909/proof.md), and [`verification.md`](../I05-DPP-21-20260909/verification.md). Full author proof and failure checks behind PR53.
4. [`docs/verification_round3_20260909/archived_pr55.md`](../../docs/verification_round3_20260909/archived_pr55.md). Read to avoid reviving an archived route from a stale issue summary.

The present proof imports from PR53 only the parity/matching lower bound and its accepted coefficient algebra. Its regularity bridge is independent of the Hölder–Ruelle–Perron–Frobenius argument.

## Load-bearing primary literature

### General one-dimensional finite-first-moment analyticity

- R. L. Dobrushin, **“Analyticity of correlation functions in one-dimensional classical systems with slowly decreasing potentials,”** *Communications in Mathematical Physics* **32** (1973), 269–289. DOI: https://doi.org/10.1007/BF01645609.

- R. L. Dobrushin, **“Analyticity of the correlation functions for one-dimensional classical systems with power law decay of the potential,”** *Mathematics of the USSR-Sbornik* **23** (1974), 13–44. DOI: https://doi.org/10.1070/SM1974v023n01ABEH001712.

  **Load-bearing role.** These are the original/general-system analyticity results used in `proof.md`, Section 6. The English publication explicitly treats one-dimensional lattice and continuous classical systems with power-law-decaying potentials and states that the specific free energy and correlation functions depend analytically on the potential. The present interaction is finite-alphabet and satisfies the stronger unnormalized estimate

  \[
  \sum_{A\ni0}\operatorname{diam}(A)\|U_A\|_\infty<\infty.
  \]

  Hence it lies within the usual finite-first-moment class even when a source divides each translation orbit by `|A|`. The proof uses Dobrushin in the standard analytic-family corollary: a holomorphic finite-first-moment interaction curve has holomorphic pressure and local expectations near a real point.

- M. Cassandro and E. Olivieri, **“Renormalization group and analyticity in one dimension: A proof of Dobrushin's theorem,”** *Communications in Mathematical Physics* **80** (1981), 255–269. DOI: https://doi.org/10.1007/BF01213013.

  **Independent mechanism check, not sole scope justification.** Its abstract treats one-dimensional many-body potentials with finite first moment and analytic dependence on interaction parameters, using decimation to reach a high-temperature effective interaction. The article's concrete lattice-gas coordinates are not used here to encode arbitrary binary block functions: a naïve monomial expansion can have an exponentially large coefficient norm. General block-function scope is therefore assigned to Dobrushin's general classical-system theorem, while Cassandro–Olivieri corroborates the finite-first-moment/complex-parameter mechanism.

- Y. Aoun, D. Ioffe, S. Ott, and Y. Velenik, **“Non-analyticity of the correlation length in systems with exponentially decaying interactions,”** *Communications in Mathematical Physics* **386** (2021), 433–467. DOI: https://doi.org/10.1007/s00220-021-04038-6.

  **Modern scope check.** Its introduction distinguishes correlation-length analyticity from standard thermodynamic analyticity and records that the general one-dimensional pressure/correlation result for interactions with finite first moment was settled by Dobrushin. This paper is corroborative; it is not substituted for the original theorem.

### Chains and two-sided Gibbs specifications

- R. Fernández and G. Maillard, **“Chains with complete connections and one-dimensional Gibbs measures,”** *Electronic Journal of Probability* **9** (2004), 145–176. DOI: https://doi.org/10.1214/EJP.v9-149; arXiv: https://arxiv.org/abs/math/0305025.

  **Independent bridge check.** Theorem 4.12 constructs a two-sided specification from a suitable left-interval specification, and Remark 4.13 covers stationary non-null chains with summable variation. The main proof does not rely on any hereditary-uniqueness hypothesis from this route: `equilibrium_bridge.md` gives a direct conditional cross-entropy/variational identification.

### Determinantal negative association and stationary entropy context

- R. Lyons, **“Determinantal probability measures,”** *Publications Mathématiques de l’IHÉS* **98** (2003), 167–212. DOI: https://doi.org/10.1007/s10240-003-0016-0.

  **Role.** Discrete DPP foundations and negative association. The accepted PR53 matching argument uses this determinantal negative-dependence structure.

- R. Lyons and J. E. Steif, **“Stationary determinantal processes: phase multiplicity, Bernoullicity, entropy, and domination,”** *Duke Mathematical Journal* **120** (2003), 515–575. DOI: https://doi.org/10.1215/S0012-7094-03-12032-3; arXiv: https://arxiv.org/abs/math/0204324.

  **Role.** Stationary Toeplitz DPP and entropy context. It is not used as a spectral formula for the configuration entropy rate.

## Independent localization literature consulted

- S. Jaffard, **“Propriétés des matrices ‘bien localisées’ près de leur diagonale et quelques applications,”** *Annales de l’Institut Henri Poincaré C* **7** (1990), 461–476. DOI: https://doi.org/10.1016/S0294-1449(16)30287-6.

- Q. Sun, **“Wiener's lemma for infinite matrices with polynomial off-diagonal decay,”** *Comptes Rendus Mathématique* **340** (2005), 567–570. DOI: https://doi.org/10.1016/j.crma.2005.03.002.

  **Role.** These give a structurally independent reason to expect inverse stability under polynomial off-diagonal decay. They are not invoked as black boxes: `proof.md`, Section 2, proves a finite-section and configuration-uniform bound because the matrices contain arbitrary complete-event `0/-1` diagonal patterns and a common parameter disk is essential.

## Variational facts and sign convention

The finite-alphabet pressure variational principle is used with

\[
P(U)=\sup_\rho\{h(\rho)-\rho(e_U)\},
\qquad
DP(U)[V]=-\nu_U(e_V).
\]

`equilibrium_bridge.md` derives the DPP equilibrium identity from conditional cross entropy and checks the relative-entropy sign. No unproved configuration-entropy/spectral-entropy identification is inserted.

## Scope of the imported theorem and review obligation

The only substantial imported regularity result is Dobrushin's general one-dimensional finite-first-moment analyticity theorem. Cassandro–Olivieri and Aoun–Ioffe–Ott–Velenik are independent scope/mechanism checks. Independent review should audit the exact Banach-neighborhood convention against (4.3), although the packet deliberately proves a stronger moment sum than normally required.

No cited source is claimed to contain the polynomial DPP theorem proved here. Novelty and correctness are separate: the result is new relative to the repository baseline, while acceptance still requires independent proof review.
