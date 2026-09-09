# pr57 SECOND Frozen Scope

STATUS: CORRECT

## accepted_scope

- Frozen case only: `r=0`, `|mu|<1`, `|nu|<1`, `0<u<1`.
- Starting point: the already accepted displayed four-by-four Schur complement `Rstar` from the copied frozen STRUCTURE source, with `a=b=1/2`, `L=1`, `J=1-u^4`, `n1=n2=4u/J`, and `n3=4u^3/J`.
- Reviewed proof chain: displayed formula -> in-script symbolic `Rstar` -> exact determinant -> extracted `P` via
  `det Rstar=(1-mu^2)^2(1-nu^2)^2 P/[2(1-u^4)^5]` -> positive-orthant polynomial `Q` under
  `mu=(X-1)/(X+1)`, `nu=(Y-1)/(Y+1)`, `u=U/(1+U)` -> `P>0` -> `det Rstar` nonzero -> seed positive definiteness -> constant inertia on the connected open domain -> `Rstar>0`.
- Reviewed lift: the already accepted six fixed physical direction reduction, using the positive eliminated `(alpha,beta)` block and the Schur complement criterion, then the displayed invertible coordinate map back to the six fixed physical directions.
- Accepted conclusion in this scope: for every `|mu|<1`, `|nu|<1`, `0<u<1` at `r=0`, the six fixed physical direction matrix `M` is positive definite.

## excluded_scope

- No claim for general `r`, including any `|r|<1` full-domain result.
- No Lambda-nonzero result.
- No entropy Hessian or Jensen counterexample claim; a negative `M`, if one existed elsewhere, would not by itself be an entropy counterexample.
- No rederivation of the all-eight-event formula `M=d/du(Fmat)+Q`; that is outside this SECOND review and remains covered only by the accepted prior reduction assumptions.
- No use of determinant positivity alone as a positive-definiteness proof; positive definiteness is accepted only through positive seed plus global nonvanishing plus connected-domain inertia.
- No assumption that Bareiss intermediate pivots are nonzero on the parameter domain; they are treated only as exact polynomial division certificates after denominator clearing.
- No use of archived `P` or `Q` as construction input; archived objects are accepted only as later comparison targets in the author implementation.
- No novelty, literature, Lean, or formal-mechanized certification.
- No reading of `review_first` material, PR57 comments, upstream successor packages, `C:\canglan\`, private author files, or Drive material.

## source lines anchoring the scope

- `frozen_contract.md` lines 7-11 freeze `r=0`, the open domain, the displayed four-by-four Schur formula, and the six fixed physical directions.
- `frozen_contract.md` lines 13-24 require independent analytic construction, exact determinant/P/Q identities, all coefficients, positive denominators, positive seed, nonvanishing, connectedness, inertia, and Schur lift.
- `author_proof.md` lines 13-23 restate the frozen theorem and the restriction to the displayed STRUCTURE formula.
- `author_proof.md` lines 179-210 give the lift back to the six fixed physical directions.
