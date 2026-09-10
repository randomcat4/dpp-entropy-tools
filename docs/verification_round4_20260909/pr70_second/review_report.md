# PR70 independent SECOND mathematical review

Frozen head reviewed: `f7be60759fd4d65184803b6585965dc7e5ccd624`.

Input binding reviewed: `input_binding.json`, SHA-256 `5d9bdeae61659ea837ff82298ddbdd3dfd6d77d922b14baea3ea9f65ecec621d7b`.

I reviewed only the eight author files in `input/` plus `input_binding.json`. The review is static and source-level. I did not run the author checker, Python/SymPy arithmetic, determinant or logarithm rebuilds, entropy jobs, resource tests, or any new computation.

## Overall verdict

PR70 is CORRECT for the analytic identities, reductions, positive pivots, quadratic-perspective theorem, fixed-shape large-`q` tail theorem, and thinning bridge listed below.

PR70 remains OPEN for the general one-sided sign `G1'' >= 0` and for the full missing-edge Shannon determinant/sign target. The author does not close those targets, and I found no hidden proof of them in the supplied files.

The fixed rational post-checkpoint obstruction and Jensen signs are not accepted in this review. Their formulas and reproduction specification are inspectable, but their signs and decimal enclosures are reserved for a separate independent raw arithmetic owner by the review instruction.

## Unit findings

### 1. Eight events, domain, and all six physical directions

Verdict: CORRECT.

Source pins: `proof.md` lines 7-60; `verify_bridges.py` lines 8-52.

The eight atom formulas in mask order are the standard inclusion-exclusion transform from inclusion minors. At the arrow center `K12=0`, the leaf marginal is the independent Bernoulli product and the conditional third-bit table is

`t_ij = q + A(1-i) + B(1-j)`.

The domain `0<x,y<1, A,B,q,qbar>0` exactly encodes strict positivity of the leaf block, the arrow Schur complement of `K`, and the arrow Schur complement of `I-K`. Since `A,B>0`, diagonal sign conjugation covers both signs of `b,c` and preserves the six-dimensional physical direction space.

The coordinate map from physical symmetric directions to `(d,e,m,f,g,h)` is invertible. Substituting the inverse displayed in `proof.md` lines 44-49 into the conditional derivative formula at lines 51-54 recovers `T_ij=m+f(i-x)+g(j-y)+h(i-x)(j-y)` in every leaf cell. The marginal acceleration formula `Pij''=2 det(D12block)(-1)^(i+j)` is also correct and keeps the missing-edge direction.

Minimal repair: none.

### 2. Perspective acceleration formula, cofactor formula, and simultaneous scaling

Verdict: CORRECT.

Source pins: `proof.md` lines 62-115; `verify_bridges.py` lines 53-69.

The scalar identity

`[P phi(r/P)]'' = P phi''(t) T^2 + r'' phi'(t) + P''[phi(t)-t phi'(t)]`

is a direct differentiation formula. It correctly retains the acceleration of both `r` and `P`.

For `phi(t)=t log t`, the `+1` term has coefficient `sum r_i''=0`, and the `P''` contribution cancels because the table `t_ij` has zero mixed double difference. Pairing selected-mass second derivatives with log weights gives the displayed cofactor form

`G1'' = F1 - 2 tr(N1 adj D)`.

The sign of `N1` is justified from `K>0`, `V1>0`, and positive diagonal `k0,ell0`. The scaling law under `S=diag(1,1,sqrt(lambda))` is also correct, provided the direction is transformed simultaneously as `D -> S D S`; the added `lambda log(lambda) K33` term is affine along a `K+tD` line.

Minimal repair: none.

### 3. `L_s,C_s,R_s,Y_s` pivots and corrected `N0` face

Verdict: CORRECT.

Source pins: `proof.md` lines 117-198; `verification.md` lines 27-30; `post_checkpoint.md` lines 147-151; `verify_bridges.py` lines 70-84.

The block decomposition in `proof.md` is consistent with the cofactor form after the six-coordinate substitution. Lemma 1 is valid: `J_s` is the double integral of the strictly convex positive function `phi_s''`; the trapezoid bounds imply `J_s^2 < AB ell_s k_s/(4vw)`, and hence both `L_s` are positive definite.

Lemma 2 also checks. For side 1, `N1>0` was already established. For side 0, the corrected decomposition

`N0 = diag(k_side0_face1, ell_side0_face1, 0) + V0(I-K)`

uses face 1, not face 0. This is the right face because `k_face0 - V0 = k_face1`, and similarly for `ell`. Since `I-K>0`, `V0>0`, and the face-1 diagonal entries are positive, `N0>0`. The congruence from `(f,g,h)` to `(D23,D13,-D12)` proves the lower `R_s` block is positive definite, and the complete Fisher `F_s` is positive definite because the four bilinear evaluations determine the four score coordinates.

Minimal repair: none.

### 4. Parallel-sum compensation and marginal Fisher

Verdict: CORRECT.

Source pins: `proof.md` lines 200-229.

The identity

`S_cond = S1 + S0 + Z^T P Z`

is the standard completion-of-squares identity for minimizing the sum of two positive quadratic forms over the same leaf-diagonal variable. No commutativity is needed. The positive `Z^T P Z` term is exactly the compensation lost by minimizing the two sides independently.

The leaf marginal contribution to full Shannon negative Hessian is correctly `M=diag(1/v,1/w)`. At the missing-edge center, the acceleration contribution from `K12` cancels because the leaf product log table has zero mixed double difference. Thus formula (15) correctly adds the positive retained marginal Fisher term.

Minimal repair: none.

### 5. Two-dimensional Schur target, inertia/determinant equivalence, and back-map

Verdict: CORRECT as an equivalence and reduction; no determinant sign is proved.

Source pins: `proof.md` lines 231-259; `post_checkpoint.md` lines 136-145.

Since `Y_s` and `Y` are positive definite, eliminating all four conditional-score coordinates gives the exact two-dimensional Schur targets

`E_s`, `E_cond`, and `E_H`.

The inertia argument is valid. For positive definite `N`, the cofactor quadratic form has five positive directions and one negative direction in the six-dimensional symmetric-matrix space. Adding the relevant Fisher keeps at least five positive directions. With a positive four-dimensional pivot already removed, each `2 x 2` Schur target has at least one positive eigenvalue. Therefore nonnegativity is equivalent to nonnegative determinant for these pointwise targets.

If `E_H` has a negative two-vector `delta`, the minimizing lift `U=-Y^{-1}C^T delta`, followed by the inverse coordinate map in `proof.md` lines 44-49, gives the corresponding physical direction. This is a correct falsification reduction.

Minimal repair: to close the global theorem, an independent proof or disproof of `det E_H >= 0` on the stated domain is still required.

### 6. Fisher inverse formulas

Verdict: CORRECT.

Source pins: `proof.md` lines 261-292; `verify_bridges.py` lines 95-107.

The four rows `a_ij` are an orthogonal product-Bernoulli basis with

`E^T P E = Dv` and `E Dv^{-1} E^T = P^{-1}`.

This gives the complete inverse identity

`[E^T diag(P_ij w_ij) E]^{-1} = Dv^{-1} E^T diag(P_ij/w_ij) E Dv^{-1}`

for positive weights. The specializations to `F1^{-1}`, `F0^{-1}`, and `(F0+F1)^{-1}` are correct. In particular, `(F0+F1)^{-1}` uses the weight `t(1-t)`, not the sum of the separate inverses.

Minimal repair: none.

### 7. Complement and leaf-exchange symmetries

Verdict: CORRECT.

Source pins: `post_checkpoint.md` lines 111-134.

Complementing all three bits sends

`(x,y,A,B,q,qbar,D)` to `(1-x,1-y,A,B,qbar,q,-D)`.

In the relabeled leaf coordinates, `delta'=-delta` and `U'=diag(-1,1,1,-1)U`. The block transformations in (P9) follow from equality of the full conditional entropy quadratic form. Leaf exchange similarly conjugates the `2 x 2` target by the coordinate swap matrix.

The fundamental domain

`0<x,y<1, A>=B>0, 0<q<=qbar, A+B+q+qbar=1`

keeps the equality surfaces `A=B` and `q=qbar`, and every strict connected missing-edge center is represented by complement and optional leaf exchange.

Minimal repair: none.

### 8. Strict quadratic-perspective sum of squares

Verdict: CORRECT.

Source pins: `proof.md` lines 294-319; `verify_bridges.py` lines 85-94.

Applying the perspective formula to `phi(t)=t^2` gives the retained acceleration identity

`J2'' = 2 E[T^2] - 4A det(D13block) - 4B det(D23block) - 4AB det(D12block)`.

The final `-4AB` term is exactly the contribution from `-sum Pij'' t_ij^2` and is not optional. Substitution of the six-coordinate inverse gives the displayed strict sum of squares. All coefficients are positive for `0<x,y<1` and `A,B,q>0`, and vanishing forces all six physical coordinates to vanish.

Minimal repair: none.

### 9. Fixed-shape large-`q` tail

Verdict: CORRECT with the stated legality limitation.

Source pins: `tail_bound.md` lines 1-93; `proof.md` lines 315-319.

For fixed `x,y,A,B` and fixed physical directions, the limiting quadratic form `Qinf=J2''/2` is uniformly positive in Frobenius norm at that fixed shape. The two scalar blocks and two `2 x 2` blocks give the constant `kappa` in (T1).

The Fisher error estimate follows from

`|q/(q+c_ij)-1| <= s/q`

and the stated fourth-moment bound for the conditional score. The cofactor error estimate follows from the integral formulas for `k0`, `ell0`, and `V1`, the operator-norm bound on `qN1-Ninf`, and the nuclear-norm bound for `adj D`. Combining these estimates gives

`q G1'' >= (kappa-Cstar/q)||D||_F^2`,

and therefore the strict tail for `q>=2Cstar/kappa`.

This theorem is fixed-shape and auxiliary-domain. It may give no legal coverage on a finite legal filament when `qstar` is larger than the available interval; the author states that limitation.

Minimal repair: none for the stated theorem. It does not repair the intermediate-`q` or full Shannon target.

### 10. Thinning equivalence and conditional/full distinction

Verdict: CORRECT.

Source pins: `thinning_bridge.md` lines 5-112.

The implication from one-sided global `G1''>=0` to global conditional concavity follows by complementing all bits. Conversely, if conditional concavity held globally, thinning the third coordinate gives

`-H_cond''(K_lambda;D_lambda) = lambda G1''(K;D) + O(lambda^2)`.

Dividing by `lambda` and sending `lambda` down to zero proves the one-sided global claim. The endpoint is used only as a limit, so no boundary Hessian is assumed.

The explicit third-order remainder bound is correct. Formula (R6) follows from the same perspective derivative, with `sum a_i=0`, and the three scalar series bounds on `0<=lambda t_i<=1/2` give (R4)-(R5). The conditional construction in Section 3 correctly shows that a hypothetical negative side would refute universal conditional concavity while sufficiently thinned corresponding full-entropy directions would remain positive because the leaf marginal Fisher survives.

Minimal repair: none. The result is conditional and logical; it provides no actual negative `G1''` point.

### 11. Fixed rational post-checkpoint obstruction and Jensen signs

Verdict: CRITICAL_GAPS for independent acceptance of the numerical signs; CORRECT for the displayed algebraic specification that can be statically checked.

Source pins: `post_checkpoint.md` lines 5-109; `verification.md` lines 8-9 and 21; `README.md` lines 11 and 33-46.

The quotient derivative formula (P3) is correct, and the vertical-translation identity (P4) is mathematically sound: selected third-bit masses are affine in `K33` with derivative `Pij`, while `Pij` is independent of `K33`, so the second `K33` derivative of conditional negative entropy is the paired resolvent sum.

However, the assignment explicitly marks the fixed rational `K,D,tau` signs and decimals as author-only pending separate raw machine evidence. Therefore I do not accept the claimed negative sign of `Phi_pair''`, the claimed positive signs of `G0''`, `G1''`, conditional/full curvatures, the legality minor signs, or the negative Jensen interval. These may be true, but they are outside this review's acceptance authority.

Minimal repair: an independent arithmetic owner must reconstruct the eight event jets from (P1), verify the exact rational resolvent sums and Sylvester minors, and independently enclose the logarithmic entropy/Jensen quantities with outward rational interval bounds.

### 12. Finite input request and open determinant target

Verdict: CORRECT as a request/specification; no finite result accepted.

Source pins: `inputs.json` lines 1-10; `README.md` lines 21-25 and 54-56; `verification.md` lines 41-45; `proof.md` lines 331-332.

The 273 fixed issue73 inputs are plainly marked as requested C2 inputs, not an executed filament run. No sign conclusion follows from them.

The remaining analytic target is exactly the full paired determinant in (P12), with both sides, parallel-sum compensation, and marginal Fisher retained. The author also leaves the stronger one-sided determinant/sign question open.

Minimal repair: complete the independent bounded computation/proof contract for the finite inputs if the finite route is desired; separately prove or disprove `det E_H >= 0` on the full reduced domain for the general theorem.

## Accepted scope to C3

C3 may accept, at source-review level, the analytic identities and reductions listed in Units 1-10 above. These include the full eight-event and six-direction setup, the perspective/cofactor/scale identities, positive pivots including corrected `N0` face 1, parallel-sum and marginal-Fisher compensation, the `2 x 2` Schur/determinant target and back-map, complete Fisher inverse identities, complement/leaf-exchange fundamental domain, strict quadratic-perspective SOS, fixed-shape large-`q` tail with legal-coverage caveat, and thinning equivalence with the conditional/full distinction.

## Exclusions to C3

C3 should not accept from this review:

1. Any fixed rational sign or decimal enclosure in `post_checkpoint.md`.
2. Any executed or certified result for the 273 issue73 inputs.
3. Any proof of global `G1'' >= 0`.
4. Any proof of the full missing-edge Shannon sign or `det E_H >= 0`.
5. Any entropy counterexample.
6. Any novelty, publication priority, CI, or formal proof-assistant result.

