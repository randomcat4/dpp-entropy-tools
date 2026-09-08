# Frozen-v1 cross-category re-encoding probes

These are representation probes for frozen v1, not proofs or proof strategies.
They are ordered by faithfulness and then by the number of native tools not
known to have been applied to this exact coefficient problem.  The local
toolbox exclusions in `local_toolbox.md` apply.

## 1. Fermionic Fock-space measurement leakage

1. **Target category.** Finite fermionic Fock space and number-conserving
   Gaussian states.
2. **Encoding map.** `K` is the one-particle correlation matrix; an exact
   coordinate subset `S` is a Fock occupation-basis outcome; a rank-`r`
   projection is the pure Slater vector `wedge^r ran(P)`; `D` is a
   particle-hole tangent.
3. **Faithfulness.** EQUIVALENT for the full exact-event distribution and its
   Shannon measurement entropy.
4. **Native name.** Leading occupation-measurement entropy defect of a
   particle-hole-perturbed Slater state with balanced thermal leakage.
5. **Native machinery.** Wick/quasi-free state calculus (APPLIED: YES);
   second quantization (UNKNOWN); Slater tangent decomposition (YES);
   pinching/measurement entropy (UNKNOWN); fermionic Gaussian fidelity
   expansions (NO); particle-hole normal forms (UNKNOWN).
6. **Hypotheses for the two leading items.** Slater tangent decomposition
   assumes a fixed finite occupied subspace and an off-diagonal one-particle
   tangent, both satisfied; Gaussian fidelity expansions generally compare
   quantum states before a fixed measurement, while the needed signed
   coefficient may be lost under measurement, the likely failure.

## 2. Grassmannian tangent geometry

1. **Target category.** Riemannian/extrinsic geometry of the real Grassmannian.
2. **Encoding map.** `P` is a point of `Gr(r,n)`; `B` is a tangent vector in
   `Hom(ran(P),ker(P))`; `psi_S` are Plucker coordinates; `Z` is tangent energy
   on the vanishing coordinate hyperplanes.
3. **Faithfulness.** EQUIVALENT for the `Z` term; ONE-WAY from the full entropy
   statement to the normal spectral-defect bookkeeping.
4. **Native name.** Coordinate-hyperplane leakage of a Grassmannian tangent
   compared with total tangent norm.
5. **Native machinery.** Plucker embedding (APPLIED: YES); canonical angles
   (UNKNOWN); second fundamental form (NO); Schubert stratification (NO);
   tangent-cone geometry (NO); moment-map convexity (NO).
6. **Hypotheses for the two leading items.** The second fundamental form needs
   a smooth fixed-rank Grassmannian point, satisfied; Schubert-stratum
   transversality may fail because arbitrary `P` and `B` can lie in singular
   intersections of several coordinate strata.

## 3. Singular perturbation of a finite probability simplex

1. **Target category.** Polyhomogeneous asymptotics on a stratified simplex.
2. **Encoding map.** The `2^n` exact masses form a probability vector; the
   projection law lies on a face; each event is assigned its leading valuation
   in `x=sqrt(epsilon)`; entropy is a boundary-singular functional.
3. **Faithfulness.** EQUIVALENT once the event valuations and coefficients are
   supplied by the DPP map.
4. **Native name.** Boundary expansion of Shannon entropy along an analytic
   two-sided probability curve crossing nested simplex faces.
5. **Native machinery.** Mellin asymptotics (APPLIED: NO); resolution of
   singularities (NO); Newton polyhedra (NO); stratified Morse theory (NO);
   epi-convergence (NO); analytic-curve selection (UNKNOWN).
6. **Hypotheses for the two leading items.** Mellin methods require controlled
   positive leading coefficients and finitely many valuations, satisfied after
   event partition; resolution machinery is applicable to analytic
   nonnegative germs but is excessive and does not itself supply the DPP
   coefficients, the likely failure.

## 4. Valuated matroids and tropical Plucker support

1. **Target category.** Matroid/valuated-matroid geometry.
2. **Encoding map.** Nonzero `psi_S` define the bases of the representable
   matroid of `U`; vanishing bases acquiring `phi_S` are first-order support
   extensions; probability orders define valuations.
3. **Faithfulness.** EQUIVALENT for the zero/nonzero Plucker support and its
   first tangent layer; ONE-WAY for metric coefficient sums.
4. **Native name.** First-order creation of nonbases under a representable
   matroid deformation with squared Plucker weights.
5. **Native machinery.** Basis exchange (APPLIED: UNKNOWN); Dressian/tropical
   Grassmannian (NO); initial matroids (NO); matroid strata (NO); Lorentzian
   polynomials (UNKNOWN); Hodge theory for matroids (NO).
6. **Hypotheses for the two leading items.** Tropical-Grassmannian machinery
   needs a non-Archimedean or one-parameter Plucker valuation, supplied by the
   analytic path; Hodge-theoretic inequalities control coefficients on fixed
   supports but generally discard the Euclidean tangent norm needed for `Z`,
   the likely failure.

## 5. Spectrahedral Schur-complement geometry

1. **Target category.** Convex algebraic geometry of matrix intervals.
2. **Encoding map.** Positive contractions form the spectrahedron
   `{K:K>=0,I-K>=0}`; `P` is a zero-dimensional transverse face point;
   `epsilon` is normal slack and `sqrt(epsilon)B` is the maximal off-face scale.
3. **Faithfulness.** EQUIVALENT for feasibility; ONE-WAY for entropy.
4. **Native name.** Exact tangent-paraboloid section of the positive-contraction
   spectrahedron at a projection face.
5. **Native machinery.** Schur complements (APPLIED: YES); facial reduction
   (UNKNOWN); tangent/second-order tangent cones (NO); semidefinite error bounds
   (NO); matrix-pencil normal forms (NO); spectrahedral curvature (NO).
6. **Hypotheses for the two leading items.** Second-order tangent cones require
   a fixed face and a specified first/second-order path, both satisfied;
   semidefinite error bounds quantify distance to feasibility but do not encode
   exact-event entropy, the likely failure.

## 6. Stable and multiaffine generating polynomials

1. **Target category.** Real stable/Lorentzian multiaffine polynomials.
2. **Encoding map.** The DPP probability generating polynomial is
   `det(I-K+K diag(z))`; exact masses are its coefficients; the path perturbs a
   determinantal stable polynomial toward a projection-support boundary.
3. **Faithfulness.** EQUIVALENT for the probability law; ONE-WAY for the
   coefficientwise entropy asymptotic.
4. **Native name.** Coefficient-entropy boundary defect for a determinantal
   stable polynomial under a transverse spectrahedral perturbation.
5. **Native machinery.** Strong Rayleigh theory (APPLIED: YES); polarization
   (UNKNOWN); Gurvits capacity (NO); Lorentzian Hessian inequalities (NO);
   complete log-concavity (UNKNOWN); hyperbolic barriers (NO).
6. **Hypotheses for the two leading items.** Capacity methods require positive
   coefficient support or a controlled face restriction, potentially available;
   Lorentzian inequalities control coefficient ratios but not directly the sum
   `-p log p` across coefficients born at different scales, the likely failure.

## 7. Classical information geometry with latent spectral modes

1. **Target category.** Information geometry of latent-variable models.
2. **Encoding map.** Formula (spectral subset `J`, then projection-DPP outcome
   `S`) is a latent channel `J -> S`; near a projection, single particle/hole
   flips are rare latent states; `H(S)` is observed entropy.
3. **Faithfulness.** EQUIVALENT for every fixed kernel after choosing a spectral
   frame; invariant formulation under multiplicities uses spectral subspaces.
4. **Native name.** Observed-entropy singularity of a finite rare-component
   latent mixture with a rotating emission channel.
5. **Native machinery.** Chain rule and data processing (APPLIED: UNKNOWN);
   missing-information principle (NO); mixture singularities (NO); Fisher
   information blow-up (UNKNOWN); information projections (NO); stratified
   statistical models (NO).
6. **Hypotheses for the two leading items.** Rare-mixture singularity formulas
   require identifiable leading component weights, supplied by the spectral
   flip classes; ordinary Fisher expansions assume interior positive masses and
   fail precisely at Plucker zeros.

## 8. Analytic perturbation of invariant subspaces

1. **Target category.** Kato-style finite-dimensional spectral perturbation.
2. **Encoding map.** The high/low spectral clusters of `K(x)` are analytic
   invariant subspaces; eigenvalue defects are order `x^2`; their exterior
   powers produce the coordinate amplitudes.
3. **Faithfulness.** EQUIVALENT locally under the frozen strict gap condition.
4. **Native name.** Coupled second-order eigenvalue leakage and first-order
   spectral-projector rotation across a fixed gap.
5. **Native machinery.** Riesz projectors (APPLIED: UNKNOWN); reduced resolvent
   expansions (NO); Davis-Kahan bounds (UNKNOWN); Rellich analytic frames
   (UNKNOWN); exterior-power perturbation (YES); block diagonalization (YES).
6. **Hypotheses for the two leading items.** Riesz-projector expansions require
   an isolated cluster, satisfied by the limiting 0/1 gap; Davis-Kahan gives
   norm bounds but normally loses the exact second-order trace and zero-event
   coefficients, the likely failure.

## Selection

The two highest-faithfulness bridge representations retained for the first
proof unit are fermionic/Slater leakage and Grassmannian tangent geometry.  The
simplex-valuation encoding is retained independently for the entropy remainder.
