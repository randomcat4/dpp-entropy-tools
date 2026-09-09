# Structure review for issue52 lambda_zero candidate

STATUS: CORRECT_WITH_SCOPE

This is a fresh nonauthor analytic review of the bounded structural candidate in
`research/C2/lambda_zero52/structure/STRUCTURE.md` at local commit
`c20f3ebc422cc4f19d77fc4bd6ab130def4bcd80`.  The frozen literal input is
`research/C2/lambda_zero52/inputs/frozen_issue52.md` at the same commit.

The public PR55 commit named in the assignment,
`5acfaf0c220e271cca92de12fe4e13d4940dd80a`, was not present as a local git
object in this checkout during review, so I did not independently inspect that
object.  The source-level review below is against the frozen local commit and
the repo-relative files named above.  No Python, SymPy, CAS, or numerical
arithmetic was launched for this review.

## Scope

Reviewed:

- the open-domain denominator and sign factors in STRUCTURE.md lines 15-40;
- the conditional polynomial map from the literal four-event input in
  frozen_issue52.md lines 21-30 to STRUCTURE.md lines 53-92;
- the Gram matrix `G`, reflection matrix `S`, and identity `S D^{-1} S=D` in
  STRUCTURE.md lines 94-135;
- the fixed-direction derivative formula
  `y'=U_alpha alpha+U_beta beta+R y` and `Fmat'` bookkeeping in lines 137-165;
- the Fisher-invisible two-plane, mixed cancellation, and positive diagonal
  block in lines 167-205;
- the formulas for `L_alpha`, `L_beta`, `R0`, `Rstar`, and reconstruction of a
  negative six-vector in lines 207-270.

Not reviewed here:

- the derivation from all eight inclusion-exclusion events to the literal input
  `M = d/du Fmat + Q`;
- positivity of `Rstar` on the full open parameter domain;
- novelty, entropy-Hessian consequences, determinant nonvanishing, or an
  entropy counterexample.

## Checks

The domain factors are correct on
`|mu|,|nu|,|r|<1, 0<u<1`.  In particular,
`L+rJ=(1+r)(1-r u^4)` and `L-rJ=(1-r)(1+r u^4)` are strictly positive, so the
displayed signs of `n1,n2,n3,d_alpha,d_beta` follow from positive factors.

The conditional-polynomial reduction is correct from the frozen input.  With
`e=i-(1+mu)/2` and `f=j-(1+nu)/2`, the identities
`e^2=v-mu e` and `f^2=w-nu f` turn
`q_ij dot zeta` from frozen_issue52.md line 25 into
`m+p e+q f+h e f` with exactly the coefficients in STRUCTURE.md lines 78-81.
The inverse map in lines 88-91 is pointwise invertible because `u,a,b>0`.

The matrix `S` is the moment matrix
`E[(2e+mu)(2f+nu) phi phi^T]` for `phi=(1,e,f,ef)`.  Its displayed entries
follow from
`E[e]=0`, `E[e^2]=v`, `E[(2e+mu)e]=2v`, and
`E[(2e+mu)e^2]=-mu v`, with the analogous formulas for `f`.  Since
`2e+mu` and `2f+nu` are signs on the four atoms, multiplication by their product
is an involution in the normalized basis; this gives `S D^{-1} S=D`.  Thus the
Gram representation `zeta^T Fmat zeta = 4 y^T G y` is correct for the literal
four-event conditional Fisher matrix.

The derivative bookkeeping uses fixed original direction coordinates.  Direct
differentiation gives
`m'=2uav alpha+2ubw beta`,
`p'=-2ua mu alpha-2a xi`, `q'=-2ub nu beta-2b omega`, and `h'=4uab eta`.
Substituting the inverse coordinate relations gives exactly
`y'=U_alpha alpha+U_beta beta+R y` in STRUCTURE.md lines 143-146.  Consequently
`d(4y^TGy)/du = 8 y'^T G y + 4 y^T G' y`, with the displayed `d0'` and `d1'`.

On the plane `m=p=q=h=0`, the inverse relations give
`eta=0`, `xi=-u mu alpha/2`, `omega=-u nu beta/2`, and
`gamma=-u^2(av alpha+bw beta)`.  Since the quadratic derivative of `Fmat` has a
factor of `y` in every term, it vanishes there.  Substituting these relations
into the literal sparse `Q` from frozen_issue52.md lines 34-41 gives the
candidate block
`(n2*a*u^2*v/2) alpha^2 + (n1*b*u^2*w/2) beta^2
 + 2vw*(u^2(n2*b+n1*a)-n3) alpha beta`.  The mixed term cancels because
`u^2(n2*b+n1*a)=n3`, after expanding
`a=(1+r)/2`, `b=(1-r)/2`, `n1=4u(1/J-r/L)`, and `n2=4u(1/J+r/L)`.

The unsimplified coupling rows in STRUCTURE.md lines 231-232 are correct:
the `Fmat'` contribution is `8 U_alpha^T G y` and `8 U_beta^T G y`, while the
only `Q` contributions linear in `alpha` or `beta` are
`-2n2 v m+n2 mu v p` and `-2n1 w m+n1 nu w q`.  Simplifying with
`n2=8u(a d0+b d1)`, `n1=8u(b d0+a d1)`, and the rows of `G` gives exactly
`L_alpha=8u v d1(-2b m+theta p+2a w h)` and
`L_beta=8u w d1(-2a m+theta q+2b v h)`, with
`theta=a nu+b mu`.

The four-variable block `R0` has the right symmetric quadratic-form
convention.  The `8(Ry)^T G y` term is represented by
`4(R^T G+G R)`, the derivative denominator contributes `4G'`, and the sparse
`Q` contributes only the displayed diagonal terms in the `(m,p,q,h)` variables.
Because the two eliminated diagonal coefficients are strictly positive, the
Schur complement is
`R0-(1/(4d_alpha))ell_alpha ell_alpha^T
    -(1/(4d_beta))ell_beta ell_beta^T`;
the factor `1/4` is correct because `alpha L_alpha(y)` corresponds to a
matrix off-diagonal row `ell_alpha/2`.  A negative vector for `Rstar` therefore
reconstructs a negative six-vector by the formulas in STRUCTURE.md lines
260-265.

## Remaining obligations

This review certifies only the algebraic structure conditional on the literal
input `M=d/du Fmat+Q`.  A complete result still needs independent coverage of
the all-event derivation of that literal `M` and a separate sign certificate or
obstruction for `Rstar` over the full open parameter domain.

## Addendum: root-proposed determinant bookkeeping

ADDENDUM STATUS: CORRECT

This addendum checks only the determinant bookkeeping proposed by root after the
main review.  It is not part of the frozen candidate note and does not certify
global positivity of `Rstar`.

For the forward coordinate map
`zeta=(alpha,beta,gamma,eta,xi,omega) -> (alpha,beta,m,p,q,h)`, the first two
coordinates are unchanged.  After those are removed, the lower block from
`(gamma,eta,xi,omega)` to `(m,p,q,h)` has nonzero diagonal/permuted entries
`1`, `2u^2ab`, `-2ua`, and `-2ub`, with even permutation sign.  Hence

```text
det T = 8*u^4*a^2*b^2.
```

If `M_zeta` denotes the original fixed-direction matrix and `M_x` denotes the
matrix of the same quadratic form in the new variables
`x=(alpha,beta,m,p,q,h)`, then `M_zeta = T^T M_x T`.  Therefore

```text
det M_zeta = det(T)^2 det(M_x).
```

The block form in the main review has leading diagonal block
`diag(d_alpha,d_beta)`, so the Schur determinant identity gives
`det(M_x)=d_alpha*d_beta*det(Rstar)`.  Thus

```text
det M_zeta =
64*u^8*a^4*b^4*d_alpha*d_beta*det(Rstar).
```

Using `d_alpha=n2*a*u^2*v/2` and `d_beta=n1*b*u^2*w/2`, this becomes

```text
det M_zeta =
16*n1*n2*u^12*a^5*b^5*v*w*det(Rstar).
```

The formula is therefore correct as determinant bookkeeping for the pointwise
congruence.  It does not by itself prove `det(Rstar)` is nonzero or positive.
