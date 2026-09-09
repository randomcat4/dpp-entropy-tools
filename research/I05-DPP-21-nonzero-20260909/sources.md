# Sources and exact roles

Correctness, repository acceptance, and novelty are separate. A citation below does not independently review the new theorem in `proof.md`.

## Accepted repository inputs

1. `docs/verification_round3_20260909/accepted_pr53.md` and the final merged files under `research/I05-DPP-21-20260909/`.

   Used for the strict exponentially weighted Fourier event-inverse localization, one-sided complete-event conditional construction, Ruelle entropy-rate formula, and the exact fact that the half-period entropy deficit has no term of order `t^2` at the parity-decoupled point. The accepted theorem itself is local in `t`; this continuation does not claim it already covers nonzero centers.

2. `docs/verification_20260909/w2/radial_quartic_audit.md`.

   Used exactly for the constant-centered whole-legal-interval statement

   ```text
   t -> h(mu+t g)+(4/3)|g_hat(k)|^4t^4
   ```

   concave whenever `g` is real and mean zero. The new compact-tube theorem transports this already reviewed strict curvature margin in the transverse center direction. It does not reprove the product-refresh theorem.

3. `docs/verification_20260909/w2_pr39/audit_channel_examples.md` and the PR53 accepted bridge record.

   Used only as a boundary: a universal local classical block-refresh channel is unavailable for correlated fixed blocks. This is consistent with the beam-splitter obstruction proved here, but neither obstacle is an entropy counterexample.

## Stationary determinantal processes

4. Russell Lyons and Jeffrey E. Steif, **Stationary Determinantal Processes: Phase Multiplicity, Bernoullicity, Entropy, and Domination**, Duke Mathematical Journal 120 (2003), 515–575; arXiv:math/0204324.

   Background for scalar stationary Toeplitz DPPs and entropy rates. The paper studies their ergodic and entropy properties; it does not state the transverse compact-tube theorem or the RPF Hessian formula proved here.

5. Russell Lyons, **Determinantal Probability Measures**, Publications Mathématiques de l'IHÉS 98 (2003), 167–212; arXiv:math/0204325.

   Source of determinantal negative association used in the accepted radial and PR53 matching arguments. No new use of negative association is needed for the compactness step in this continuation.

## Ruelle operators, g-measures, and analytic perturbation

6. Peter Walters, **Ruelle's Operator Theorem and g-Measures**, Transactions of the American Mathematical Society 214 (1975), 375–387, DOI 10.1090/S0002-9947-1975-0412389-8.

   Source for the positive normalized Hölder `g`-function/Ruelle-operator identification on a finite full shift. The DPP conditional is not assumed to be Hölder from this theorem; that property is proved from complete-event inverses before Walters is applied.

7. Leandro Cioletti and Eduardo A. Silva, **Spectral Properties of the Ruelle Operator on the Walters Class over Compact Spaces**, Nonlinearity 29 (2016), 2253–2280; arXiv:1511.01579.

   Source for analytic dependence of Ruelle operators on Hölder/Walters potentials and the spectral-gap framework. The linear-response and Hessian identities in Section 6 of `proof.md` are nevertheless derived directly from `nu L=nu`, the centered resolvent, and a Riesz projection; no sign is imported from this paper.

The volume-uniform entropy and relative-entropy rate formulas are not taken as black boxes from either source. They come from the right-to-left finite chain rules plus the exponentially summable complete-event conditional error, as in accepted PR53 and Lemma 2.2 here.

## Fermionic quasifree states and beam splitters

8. Ben Dierckx, Mark Fannes, and Małgorzata Pogorzelska, **Fermionic Quasi-free States and Maps in Information Theory**, Journal of Mathematical Physics 49 (2008); arXiv:0709.1061.

   Source for the covariance description of gauge-invariant quasifree states, their entropy formulas, and covariance transformation under quasifree maps. The occupation-basis diagonal is separately identified with the complete DPP distribution in the accepted PR53 bridge.

9. Xingjian Lyu and Kaifeng Bu, **Fermionic Gaussian Testing and Non-Gaussian Measures via Convolution**, arXiv:2409.08180 (2024).

   Source for the balanced fermionic convolution/beam-splitter viewpoint. Its quantum entropy statements concern von-Neumann entropy. They do not imply the occupation-measurement Shannon inequality `E_occ>=0`; Section 8 of `proof.md` isolates this distinction and proves that output occupation mutual information is only quartic at a midpoint.

## Search outcome and novelty boundary

The primary literature search located the standard stationary-DPP, Ruelle/g-measure, analytic-transfer-operator, and fermionic-convolution bridges above. It did not locate the precise theorem that a constant-centered whole-line quartic curvature margin is open, in the exponentially weighted symbol topology, to transverse half-period-even center perturbations uniformly over a prescribed compact parameter interval. This finite search is not a novelty certification or priority claim.