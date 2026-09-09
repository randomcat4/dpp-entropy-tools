# Sources, route comparison, and remaining obligations

Correctness and novelty are separate. The full Lambda-zero result in proof.md is a new author proof in this packet, not an independently reviewed conclusion or a priority claim. Main's earlier accepted and archived scopes are preserved.

## Primary sources and the exact bridges used

[Q] Ronan Quarez, *Piecewise Certificates of Positivity for matrix polynomials*, arXiv:1001.1277v1 (2010), https://arxiv.org/abs/1001.1277 ; full text https://arxiv.org/pdf/1001.1277 .

Theorem 4.1 uses positive definiteness in the homogeneous sphere/projective convention of section 2; its finite cover uses compactness. Theorem 5.4 additionally specifies a closed semialgebraic set defined by homogeneous polynomials. Theorem 5.6 concerns a single-variable local problem. None automatically supplies strictness on our open four-parameter domain with degenerate boundary factors. We do not use this existence result to assume the positivity we are trying to establish. Its domain-piece perspective motivates the explicit chart proof here.

[L] Russell Lyons, *Determinantal Probability: Basic Properties and Conjectures*, Proceedings of the International Congress of Mathematicians 2014, IV, 137–161, arXiv:1406.2707, https://arxiv.org/abs/1406.2707 . This is a primary source for the determinantal inclusion law and its complete-event interpretation; it is not cited as a theorem proving the entropy curvature obtained here. The bridge is inclusion-exclusion (proof.md (4)) followed by the exact finite entropy differentiation (6) and cofactor grouping (7).

The algebraic sign bridge is entirely explicit:

    M > 0  <=>  Rstar > 0,
    det Rstar = positive_prefactor * P,
    Q = positive_denominator_multiplier * P(chart),
    every coefficient of Q >= 0 and Q(0)=432>0.

The determinant step is combined with a positive seed only AFTER global nonvanishing has been proved. No literature theorem about generic existence or asymptotic approximation is substituted for these identities.

## Two structurally different routes considered before selection

### A. Product-Bernoulli Gram geometry and direct weighted Schur estimates

The accepted identity S Delta^(-1) S=Delta makes the four conditional-score denominators two reflection eigenvalues. Differentiating in fixed physical direction coordinates and then completing the two invisible-direction squares produces

    Rstar=R0-ell_alpha ell_alpha^T/(4d_alpha)
             -ell_beta ell_beta^T/(4d_beta).

This is a potential direct analytic weighted decomposition: one would prove that the positive Gram/derivative block pays for both rank-one losses simultaneously. It cannot be justified by separately proving two rank-one direction inequalities, or by treating the two subtractions as independent uses of the same Fisher budget. It also cannot simply replace the reflection by a norm-one bound near all boundary faces: denominators J and L have different scales.

The usable part of this route is retained in the exact compact matrix (16). A separate bias-concavity shortcut is false. For the determinant residual P defined in the source, at mu=nu=0, r=-1/2, t=1/4,

    d^2P/dmu^2 = 3548043/131072 > 0.

This follows by extracting twice the mu^2 coefficient from the literal polynomial. Thus separate concavity in both leaf biases cannot be used to reduce the entire sign question to their endpoints. This is only an obstruction to that sufficient argument; P itself is positive by the successful certificate.

### B. Symmetry fundamental domain and an explicit positive chart — selected

Actual leaf exchange gives (mu,nu,r) -> (nu,mu,-r) without changing entropy or Hessian inertia. Substituting t=u^4 into the exact Schur matrix, not into a differentiated moving direction, reduces the determinant degree. On the fundamental domain r>=0, the positive-orthant chart uses r=R/(1+R), rather than forcing a single chart across both signs of r.

The resulting Q has 1731 positive integer coefficients and constant 432. The binomial transform formula in proof.md (21) supplies a finite exact certificate, so no compactness or generic degree-existence theorem is required. The lower bound is allowed to vanish as the original open boundary is approached. This simultaneously controls all mu,nu and all edge ratios; it is not an enlargement of the old 1/4 weak-coupling constant or an extrapolation from half filling.

## Earlier failures that remain relevant

The following are accepted method limitations in PR51 and main's route ledger; none is a DPP entropy counterexample.

The conditional resolvent Phi=sum Pij^2/pij1 can have strictly negative second derivative at a legal arrow kernel while the actual entropy Hessian and Jensen gap have the concave sign. Hence a universal pointwise resolvent-convexity proof cannot be imported.

The rescaled half-filled family with a direction depending on the family parameter has an s^4 curvature coefficient -1/18. That excludes a coefficientwise PSD power-series route in those moving coordinates, but does not refute fixed-direction M. The present certificate concerns a scalar determinant after exact Schur elimination, not those coefficient matrices.

Adding facewise two-point conditional-entropy proofs can double count Fisher and omit the exact residual acceleration terms

    2 Jrect d e - v w Jrect h^2/(2AB).

Both remain present in the general Lambda-nonzero problem. The previously disproved uniform positive safety margin on sparse beta-zero families is not restored here: our certificate's displayed quantitative bound vanishes at appropriate limiting faces.

Finally, the old full-r transform's mixed coefficient signs were not a sign determination of its polynomial. The successful symmetry chart demonstrates precisely why failure of a particular coefficient certificate must be kept separate from failure of the underlying inequality.

## What is still open after this proof

At a general strict arrow center with Lambda != 0, the accepted full Schur matrix is

    Sfull = Fc+R-Cblock^T [Lblock+diag(1/v,1/w)]^(-1) Cblock.

Its global positive semidefiniteness remains the target, with all variables and weights as in PR51 continuation. The stronger conditional-entropy version replacing the bracket by Lblock remains separate. The present Lambda-zero theorem does not remove these nonzero three-way-log terms by continuity outside a quantified neighborhood, nor does it settle arbitrary full real three-point kernels.

The two proof files and exact verifier constitute the author Lambda-zero result. The code is public on the new branch; no private Drive file is needed. Ordinary progress, independent-review requests, and computation handoff are recorded in issue52 and the successor PR, not cross-thread messages.
