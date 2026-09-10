# Independent FIRST review report for PR124 positive analytic units

## Verdict

**ACCEPTED_SCOPED** at exact author head
`344723af6affab240c9f87c395d4e8c1b7b19f6d`.

The equal-strength half-leaf proof and the punctured small-edge face theorem
are supported by the submitted analytic arguments.  The former is an
alternative certificate for the same statement appearing in PR120; the
latter is a genuinely different parameter regime.

## 1. Normalization and complete-law reduction — pass

Writing the edge strengths as `a=A/q` and `b=B/q` gives the four normalized
corner weights

`1+a+b, 1+b, 1+a, 1`.

The extra normalization term in the occupied conditional form is affine in
the leaf parameter, so the normalized and unnormalized second derivatives
have the same sign.  The occupied and vacant restrictions are treated
separately, and their sum is exactly the full complete-law Shannon Hessian.
Thus positivity of both one-sided forms implies strict entropy concavity; no
selected-event or resolvent sign is substituted for the complete law.

## 2. Equal-strength antisymmetric sector — pass

For `a=b>0`, the submitted coordinate change is invertible and splits the
six-dimensional form into symmetric and antisymmetric sectors.  In the
antisymmetric block, the first pivot is positive because

`2 log(1+a)-log(1+2a)=log((1+a)^2/(1+2a))>0`.

The displayed determinant then has only positive factors, so the full
antisymmetric sector is positive definite.

## 3. Equal-strength symmetric sector — pass

The retained three-node chain has positive endpoint residuals.  Their key
inequality is the strict logarithmic-mean bound

`log(r/p)/(r-p) < 1/sqrt(pr)` for `p!=r`,

equivalently `t<sinh(t)`.  Hence the chain matrix is positive definite, and
optimizing its linear coupling produces the exact coefficient
`1/(c^T M^(-1)c)`.

After this optimal absorption, the remaining gap is

`(1-r) N(r) / (32 r^2 D(r))`,

where `D(r)>0` follows from positivity of the retained chain.  With
`x=r^2`, the proof rewrites `N=x^2 F` and obtains

`F'(x)=C(x)L(x)/(2x)`

with `C(x)>0`.  Every nonconstant Taylor coefficient of `L` is bounded below
by

`6(10n^2-5n-3)/(n(n+1)(2n-1)(2n+1))>0`.

Consequently `L>0`, then `F>0`, and finally `N>0`.  This absorbs the negative
shared-cell contribution and proves strict positivity of the symmetric
sector.  Complementation gives the same conclusion for the vacant side.

## 4. Equality-source correspondence — pass with deduplication

PR120 and PR124 assert the same equal-strength theorem.  Their proof
certificates are materially different, so PR124 was checked on its own; but
the result is recorded once, with PR120 as the earlier theorem source and
PR124 as an alternative proof.  No verdict was inherited across heads.

## 5. Small-edge pivot and limiting Schur complement — pass

For a fixed `a>0` and weak edge `b`, the submitted block form has a pivot
`Y`.  At `b=0` it splits into two positive two-by-two blocks.  Their
determinants are

`((a+2)u+4a)/(16a(a+1))` and `9/(256(a+1))`,

with `u=log(1+a)>0`.  Hence the pivot remains positive for sufficiently small
`b`.

At the face the Schur core is `diag(E_A,0)`, where

`E_A=2u(4a^2-(a+1)u^2)/((a+2)u+4a)>0`.

Indeed, putting `x=sqrt(1+a)` gives
`u=2log x<2(x-1/x)=2a/sqrt(1+a)`, which is exactly the required numerator
inequality.

The weak-mode expansions give

`E_ee/b^2 -> y_00>0`, `E_de/b -> 0`.

Therefore

`det(E)/b^2 -> E_A y_00>0`.

The entries have removable logarithmic singularities and extend jointly
real-analytically to the face.  Continuity and compactness then yield a
uniform positive radius when the strong face parameters range over a compact
positive set.  The same argument applies after complementation to the vacant
side.

## 6. Physical parameters and local persistence — pass

On the occupied side, `a=A/q` is fixed and `b=B/q` tends to zero.  On the
vacant side, the complemented diagonal changes with `B`, but its normalized
strong strength remains in a compact positive interval while its weak
strength still tends to zero.  Thus the uniform normalized theorem applies
to both one-sided forms in the original physical parameterization.

At every fixed `B>0` obtained this way, positive definiteness is open under
small leaf-diagonal perturbations.  The proof correctly does not claim a
perturbation radius uniform as `B->0`.

## 7. Residual-only obstruction — pass within stated role

The residual-only limiting gap has a positive denominator.  Its displayed
numerator is negative, for example, at sufficiently large strong coupling
(`a=1000` already suffices using `log(1001)>6`).  This rules out that narrower
residual certificate.  Because the full retained-chain form remains positive,
the sign is not an entropy counterexample and supplies no contrary conclusion
about the complete Hessian.

## Contract ledger

| Unit | Result | Reason |
|---|---|---|
| Normalized reduction | PASS | affine normalization leaves the Hessian sign unchanged |
| Complete entropy identity | PASS | occupied and vacant complete-law forms are both retained |
| Equal antisymmetric block | PASS | positive pivot and determinant |
| Equal symmetric block | PASS | positive chain plus coefficientwise positive residual gap |
| PR120 correspondence | PASS | same theorem statement, distinct proof, deduplicated source claim |
| Small-edge pivot | PASS | positive face blocks and continuity |
| Small-edge Schur core | PASS | one positive limit and one positive quadratic weak mode |
| Compact uniformity | PASS | joint analytic extension plus compactness |
| Physical occupied/vacant passage | PASS | normalized parameters remain in the certified compact regime |
| Local unequal-diagonal persistence | PASS | openness only at fixed positive weak edge |
| Residual obstruction | PASS | method-only conclusion, not entropy falsification |

## Evidence boundary

This FIRST is analytic.  The accompanying symbolic script was inspected only
as provenance for the displayed identities and was not executed or used as a
substitute for their proofs.  No finite PASS was promoted to a theorem.  The
pointwise-resolvent counterexample files are outside this review, and novelty
was not assessed.

