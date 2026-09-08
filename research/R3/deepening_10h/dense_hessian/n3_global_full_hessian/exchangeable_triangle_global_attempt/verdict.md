# D10-U10h verdict

GLOBAL STATUS: INCOMPLETE.
NEW RESULTS: ANALYTIC CANDIDATES PENDING INDEPENDENT REVIEW.
FINITE COMPUTATION: SCOUT / AUTHOR SANITY.

No strict triangle counterexample was found or certified. No global theorem
or author-side CORRECT label is claimed.

## New candidate results

[proof_or_blocker.md](proof_or_blocker.md) proves the following candidates.

1. The two-dimensional exact Fisher matrix is
   diag(u,2v)-kappa(u,-v)(u,-v)^T, where kappa is an explicit rational
   conditional variance from the model Bernoulli(alpha)+Binomial(2,beta).
   The entropy acceleration uses only two conditional-odds logarithms.
2. For every compact transverse interval [r,1-r], the four spectral edges
   have uniformly positive inner strips. This is a FULL Sym(3) result via
   the reviewed U10f four-dimensional-block theorem, not just invariant
   tangent concavity. The normalized determinant limits are

   ```text
   alpha -> 0: alpha Delta_T -> beta^2 L(beta);
   alpha -> 1: (1-alpha)Delta_T -> (1-beta)^2 L(beta);
   beta -> 0: beta Delta_T -> 2/(1-alpha);
   beta -> 1: (1-beta)Delta_T -> 2/alpha;
   L(beta)=2/[beta(1-beta)]-2log(4/3)>0.
   ```

   The widths are existential and depend on r; corners are not included.
   The proof controls uniform remainders, not finite point spacing.
3. Swapping alpha and beta is not an entropy symmetry, certified by an
   exact nonzero prime-log expression at rational inputs. Complete
   complementation is a valid symmetry and supplies the two opposite edges.
4. The entrywise shortcut C_alpha_beta>=0 fails along an entire strict
   beta->0 approach, although the full Hessian is positive there. Its
   logarithmically negative mixed term is controlled by a positive pole
   in C_beta_beta, not by an entrywise sign rule.

## What remains

The exact unsolved gate is proof (5), a rational expression and two log
ratios, over all 0<alpha,beta<1 off the diagonal. The new edge strips plus
the already-reviewed punctured diagonal neighborhood do not yet cover
joint corner limits or certify the separated compact middle. No finite
net is promoted to a compact-region proof.

## Evidence denominator and review priorities

[sanity.py](sanity.py) and [sanity.json](sanity.json) provide:

- 3 exact polynomial identities for the rational rank-one Fisher formula;
- 8 exact polynomial log-coefficient identities and 4 zero pure-alpha
  acceleration identities;
- an exact prime-factorization proof that the swap witness has unequal
  entropy;
- 86/86 Fraction/150-digit sanity points: 6 ordinary, 60 boundary, 20
  signed diagonal approaches, all strictly feasible and checked against
  Möbius event probabilities; no failed case or positive-curvature candidate.

These finite values are only SCOUT. In particular 60 boundary samples do
not certify the four strips: the analytic uniform limits do that work.

Fresh review should prioritize the sign and factor two in the latent-score
covariance, n_beta versus n_alpha in the mixed/diagonal acceleration,
the coefficient 2(1-alpha)log beta, and uniformity away from all corners.
All new statements remain pending independent non-author review.
