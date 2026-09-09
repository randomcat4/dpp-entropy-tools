# Sources and dependency audit

## Repository baseline

1. [`docs/research_status.md`](../../docs/research_status.md). Current-main status ledger. It records PR53 as the accepted local entropy-rate theorem and separates it from later unreviewed extensions.
2. [`docs/verification_round3_20260909/accepted_pr53.md`](../../docs/verification_round3_20260909/accepted_pr53.md). Accepted quantifiers and coefficient.
3. [`research/I05-DPP-21-20260909/finite_range_local_theorem.md`](../I05-DPP-21-20260909/finite_range_local_theorem.md), [`exponential_wiener_extension.md`](../I05-DPP-21-20260909/exponential_wiener_extension.md), [`proof.md`](../I05-DPP-21-20260909/proof.md), and [`verification.md`](../I05-DPP-21-20260909/verification.md). Full author proof and failure checks behind PR53.
4. [`docs/verification_round3_20260909/archived_pr55.md`](../../docs/verification_round3_20260909/archived_pr55.md). Read to avoid reviving an archived route by relying on a stale issue summary.

The present proof reuses from PR53 only the parity/matching lower bound and its already accepted algebra. The regularity bridge is new and independent of its Hölder–Ruelle–Perron–Frobenius argument.

## Load-bearing primary literature

### One-dimensional finite-first-moment analyticity

- R. L. Dobrushin, **“Analyticity of correlation functions in one-dimensional classical systems with slowly decreasing potentials,”** *Communications in Mathematical Physics* **32** (1973), 269–289. DOI: https://doi.org/10.1007/BF01645609.

  Role: original one-dimensional analyticity theorem beyond finite range/exponential decay. The English translation/related publication states analytic dependence of the specific free energy and correlation functions on the potential.

- M. Cassandro and E. Olivieri, **“Renormalization group and analyticity in one dimension: A proof of Dobrushin's theorem,”** *Communications in Mathematical Physics* **80** (1981), 255–269. DOI: https://doi.org/10.1007/BF01213013.

  Role: many-body formulation. Its abstract explicitly treats one-dimensional many-body potentials with finite first moment and proves analytic dependence of correlation functions on interaction parameters by decimation to a high-temperature effective interaction. This is the external theorem used in `proof.md`, Section 6. The interaction constructed here satisfies the stronger, unnormalized estimate

  \[
  \sum_{A\ni0}\operatorname{diam}(A)\|U_A\|_\infty<\infty,
  \]

  so it is within the usual finite-first-moment conventions whether or not orbit-size normalization is included.

### Chains and two-sided Gibbs specifications

- R. Fernández and G. Maillard, **“Chains with complete connections and one-dimensional Gibbs measures,”** *Electronic Journal of Probability* **9** (2004), 145–176. DOI: https://doi.org/10.1214/EJP.v9-149; arXiv: https://arxiv.org/abs/math/0305025.

  Role: independent bridge check. Theorem 4.12 constructs a two-sided specification from a suitable left-interval specification, and Remark 4.13 includes stationary non-null chains with summable variation. The main proof no longer needs this theorem for equilibrium identification: `equilibrium_bridge.md` gives a direct conditional cross-entropy/variational proof. Fernández–Maillard is retained as a structurally independent consistency check.

### Determinantal negative association and stationary entropy context

- R. Lyons, **“Determinantal probability measures,”** *Publications Mathématiques de l’IHÉS* **98** (2003), 167–212. DOI: https://doi.org/10.1007/s10240-003-0016-0.

  Role: discrete DPP foundations and negative association. The accepted PR53 matching argument invokes this determinantal negative-dependence structure.

- R. Lyons and J. E. Steif, **“Stationary determinantal processes: phase multiplicity, Bernoullicity, entropy, and domination,”** *Duke Mathematical Journal* **120** (2003), 515–575. DOI: https://doi.org/10.1215/S0012-7094-03-12032-3; arXiv: https://arxiv.org/abs/math/0204324.

  Role: stationary Toeplitz DPP and entropy context. It is not used as a spectral formula for the configuration entropy rate.

## Independent localization literature consulted

- S. Jaffard, **“Propriétés des matrices ‘bien localisées’ près de leur diagonale et quelques applications,”** *Annales de l’Institut Henri Poincaré C* **7** (1990), 461–476. DOI: https://doi.org/10.1016/S0294-1449(16)30287-6.

- Q. Sun, **“Wiener's lemma for infinite matrices with polynomial off-diagonal decay,”** *Comptes Rendus Mathématique* **340** (2005), 567–570. DOI: https://doi.org/10.1016/j.crma.2005.03.002.

  Role of both: these provide an independent matrix-localization route showing that polynomial off-diagonal decay is naturally inverse-stable. They are not invoked as black boxes in the theorem: Section 2 gives a finite-section, configuration-uniform band-truncation proof because the event matrices contain arbitrary `0/-1` diagonal patterns and the needed constants must be uniform in the conditioning window.

## Variational facts

The finite-alphabet pressure variational principle and pressure derivative identity are used with the sign convention

\[
P(U)=\sup_\rho\{h(\rho)-\rho(e_U)\},
\qquad
DP(U)[V]=-\nu_U(e_V).
\]

The exact use and sign check are written out in `equilibrium_bridge.md`; no unproved entropy/spectrum identification is inserted.

## Scope of the imported theorem and review obligation

The only substantial imported regularity theorem is Dobrushin–Cassandro–Olivieri analyticity for one-dimensional finite-first-moment many-body interactions. Independent review should check the precise Banach-neighborhood convention used in that theorem against (4.3). The packet deliberately proves a stronger moment sum than normally required to make this audit insensitive to normalization conventions.

No source is claimed to contain the polynomial DPP theorem proved here. Novelty and correctness are separate: the result is new relative to the repository baseline, while its acceptance still requires independent proof review.
