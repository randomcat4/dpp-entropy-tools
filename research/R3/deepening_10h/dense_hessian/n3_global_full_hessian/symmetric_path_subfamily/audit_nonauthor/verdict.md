# D10-U10d fresh non-author audit verdict

STATUS: CORRECT for the centered symmetric-path theorem and for the stated
scope boundary.  The full two-parameter family remains INCOMPLETE exactly as
the author states.

This audit did not import or execute the author's `sanity.py`.  The supporting
script rebuilds all eight exact atoms from inclusion-probability Möbius
inversion and differentiates those atom polynomials directly.

## Frozen inputs

Hashes recorded in `audit_results.json`:

- `frozen_problem.md`: `339e3427cd9ad430f7509c2f3c4ae8259e764ba6b2981881fe3bec8d9a9405e5`
- `proof_or_blocker.md`: `d655e6065ad362c9c7097994f1f06b470bdd881b966cd62966f497b1b3e39cec`
- `derivation.md`: `8e302f62e3487beeae8903f31d5f1068880049d80a5a9fa1fabeb93ab0a89356`
- `verdict.md`: `9c4cdf508f5d931c12839a520cad30c312a6e05c21ffca5b8362b8d0d09ad175`
- `run_log.md`: `4ce8c5a9ab359161a88d719e25b3fcccdabff61bb694dc92f6ce4c000efea507`
- `sanity.json`: `c98a0b32260ccebf638775cd8cbc9f5d3ba658098934fff258202dafe0988ab2`

## Checks and conclusions

1. Exact atoms and feasibility.

   For
   `K(x,a)=((x,a,0),(a,x,a),(0,a,x))`, the eigenvalues are
   `x, x±sqrt(2)a`.  Thus the strict connected path domain is
   `0<x<1` and `0<sqrt(2)|a|<min(x,1-x)`.  On the centered line this is
   exactly `0<8a^2<1`.  Independent Möbius reconstruction matches the
   claimed atom list `(E,U,W,V,U,Z,V,F)` at non-author rational samples, with
   all atoms positive and total mass one.

2. Reflection and complement/sign symmetries.

   The reflection `1<->3` fixes `K`, so Hessian cross terms between the
   reflection-even and reflection-odd subspaces vanish.  At `x=1/2`,
   `I-K=S K S` with `S=diag(1,-1,1)`, so the affine symmetry
   `X -> S(I-X)S` fixes the base point and sends even coordinates
   `(d,e,h,k)` to `(-d,-e,h,-k)`.  Hence `h` has no cross term with
   `(d,e,k)`.  The independent script finds these cross blocks at
   `10^-147`--`10^-149` numerical residue from exact rational jets plus
   Decimal logs.

3. Centered `3x3 -> 2x2` Schur reduction.

   For the core direction
   `D=((d,0,k),(0,e,0),(k,0,d))`, the atom derivative multiplicities are
   correct:

   - full/empty atoms give `((2-r)d+e+rk)^2/(1-r)`;
   - the two adjacent pairs and their singleton complements give
     `2(rd+e-rk)^2`;
   - the `13` pair and the middle singleton give
     `((2+r)d-e-rk)^2/(1+r)`.

   With `r=8a^2`, `u=r^2`, `L=1-r^2`, `v=2-r^2`,
   `n=log((1+r)/(1-r))`, and `m=-log(1-r^2)`, the core form equals
   `(2/L) C`.  A fresh polynomial checker verifies, after eliminating the
   `e` coordinate, that the Schur block is `L T` and that

   `det T = [m(8-Ln^2)+8uz+16u-vz^2]/v`,

   where `z=rn-m`.  The symbolic residuals for all Schur entries and for the
   determinant identity are exactly zero.

4. Positivity inequalities.

   The proof of `L n^2<4` is valid: write `r=tanh s`,
   `n=2s`, and `L=sech^2 s`; then `L n^2=4s^2/cosh^2 s<4`.

   The proof of `0<z<2u` is also valid:
   `z=(1+r)log(1+r)+(1-r)log(1-r)
     = sum_{j>=1} u^j/[j(2j-1)]`,
   all coefficients are positive, and their sum at `u=1` is `2 log 2<2`.
   Therefore the determinant numerator is strictly positive for every
   `0<r<1`.  This closes strict positivity of the centered core and hence of
   all six real-symmetric directions on the centered line.

5. Compact thickening in `x`.

   The quantifier is sound: for every fixed
   `0<a_min<=a_max<1/(2sqrt(2))`, there exists an `epsilon>0`, depending on
   that compact interval, such that `|x-1/2|<epsilon` and
   `a_min<=|a|<=a_max` remains strictly feasible and has positive full
   Hessian.  The argument is compactness plus continuity over the compact
   centered segment times the unit Frobenius sphere.  It does not give a
   uniform radius as `a_min -> 0` or `a_max` approaches the spectral boundary.

6. General `x`.

   The general even-block derivative formulas and equation (9) were checked
   against exact atoms at independent rational samples.  The author's
   equation (10) is correctly presented as a remaining scalar Schur
   complement, conditional on the already-reviewed U8 weighted-trace-zero
   input for `C0>0`.  No global positivity of `sigma(x,a)` is claimed, and no
   finite check is promoted to a theorem.

## Scope notes

- The centered theorem is a full `Sym(3)` Hessian statement, not merely a
  two-parameter tangent statement.
- The full two-parameter symmetric path family is not proved here.
- Boundary cases `a=0`, `x=0,1`, and the spectral boundary are correctly
  excluded.
- The finite Decimal/Fraction checks are evidence for arithmetic integrity;
  the centered-line conclusion rests on the analytic Schur determinant and
  inequalities above.

No critical gap was found in the centered proof or in the author's stated
INCOMPLETE boundary for the general family.
