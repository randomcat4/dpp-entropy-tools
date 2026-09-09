# PR55 issue52 structural reduction — independent second analytic audit

Frozen head: `de802933899b6a02e7c4fb8afc79e0b15564caba`

Overall verdict: `ACCEPTED_SCOPED` for the conditional algebraic reduction from the literal issue52 matrix
`M = d/du(Fmat) + Q`.

The review certifies structural bookkeeping only. It does not certify the all-eight-event derivation of `M`, the global sign of `Rstar` or `M`, global positivity, or an entropy counterexample.

Files read:

- `research/C2/lambda_zero52/inputs/frozen_issue52.md`
- `research/C2/lambda_zero52/structure/STRUCTURE.md`

I did not read any prior structure review or formula review, and I did not run arithmetic, symbolic elimination, scouts, raw `M` derivation, or C2 jobs.

## Verdict table

| Item | Status | Source anchors |
|---|---:|---|
| Domain and positive factors | `ACCEPTED_SCOPED` | `frozen_issue52.md:5-15`, `17-43`; `STRUCTURE.md:15-51` |
| Conditional-polynomial map from original direction variables | `ACCEPTED_SCOPED` | `frozen_issue52.md:21-30`; `STRUCTURE.md:53-95` |
| Four-atom reflection Gram and `S D^-1 S = D` | `ACCEPTED_SCOPED` | `STRUCTURE.md:94-135` |
| Derivative with original `zeta` fixed before pointwise congruence | `ACCEPTED_SCOPED` | `STRUCTURE.md:137-165` |
| Positive Fisher-invisible two-plane and cancelled mixed term | `ACCEPTED_SCOPED` | `STRUCTURE.md:167-205` |
| Coupling rows, `R0`, and `1/4` Schur factor | `ACCEPTED_SCOPED` | `STRUCTURE.md:207-254` |
| Negative-vector back-map from `Rstar` to original six-vector | `ACCEPTED_SCOPED` | `STRUCTURE.md:256-270` |
| Determinant bookkeeping claims | `ACCEPTED_SCOPED`, with a source-addition recommendation | `STRUCTURE.md:84-92`, `242-254`; derivation below |
| All-event derivation of `M=Fmat'+Q` | `INCOMPLETE / out of scope` | explicitly not verified at `STRUCTURE.md:3-13`, `304-310` |
| Global positivity/sign of `Rstar` or `M` | `INCOMPLETE / out of scope` | explicitly not proved at `STRUCTURE.md:291-310` |

## Checks

### 1. Domain and denominator signs

The stated open domain is
`|mu|<1`, `|nu|<1`, `|r|<1`, `0<u<1`, with
`a=(1+r)/2`, `b=(1-r)/2`, `v=(1-mu^2)/4`, `w=(1-nu^2)/4`,
`J=1-u^4`, and `L=1-r^2u^4`
(`frozen_issue52.md:5-19`, `STRUCTURE.md:15-24`). On this open domain, all factors
`a,b,v,w,u,J,L` are positive. Also
`L+rJ=(1+r)(1-r u^4)>0` and
`L-rJ=(1-r)(1+r u^4)>0`, so
`n1,n2,n3` are positive as stated
(`STRUCTURE.md:26-40`). The note correctly treats boundary vanishing factors as excluded and warns that closed-box nonnegativity is not a strict interior proof without excluding residual interior zeros
(`STRUCTURE.md:47-51`).

### 2. Conditional-polynomial map

From the frozen issue input,
`q_ij=(u^2 a e^2, u^2 b f^2, 1, 2u^2abef, -2uae, -2ubf)^T`
(`frozen_issue52.md:21-30`). Using the two Bernoulli identities
`e^2=v-mu e` and `f^2=w-nu f`, the original direction dot product becomes

```text
q_ij dot zeta = m + p e + q f + h e f,
```

with exactly the displayed coefficients
(`STRUCTURE.md:53-82`). The inverse map in `STRUCTURE.md:84-92` is correct whenever `u,a,b>0`, which holds throughout the open domain. This is an invertible polynomial/rational coordinate change in the stated variables, and no square roots enter this structural reduction.

### 3. Reflection Gram identity

The denominator parity identity

```text
1/den_ij = d0 + d1*(2e+mu)*(2f+nu)
```

is correct because `2e+mu` and `2f+nu` are the two leaf signs, so their product is `+1` on equal atoms and `-1` on unequal atoms (`STRUCTURE.md:117-122`). In the basis `(1,e,f,ef)`, the ordinary product Gram is
`D=diag(1,v,w,vw)`, while the signed Gram is the displayed matrix `S`
(`STRUCTURE.md:94-115`). Multiplication by the sign product is an involution, so its signed Gram satisfies `S D^{-1} S = D` (`STRUCTURE.md:124-135`). This justifies the two-eigenvalue denominator structure and the claim that the `mu,nu` dependence is a reflection-coordinate change at this level.

### 4. Fixed-direction derivative

The derivative convention is handled correctly. The derivative is taken with the original direction variables
`zeta=(alpha,beta,gamma,eta,xi,omega)` fixed, and only afterward is the pointwise coordinate change used for inertia (`STRUCTURE.md:137-165`). Differentiating the transformed variables while substituting the inverse relations gives

```text
y' = U_alpha alpha + U_beta beta + R y,
R = diag(0,1/u,1/u,2/u),
U_alpha = (2uav, -ua mu, 0, 0)^T,
U_beta  = (2ubw, 0, -ub nu, 0)^T.
```

Then differentiating `4 y^T G y` gives
`8 y'^T G y + 4 y^T G' y`, because `G` is symmetric. The displayed `G'`, `d0'`, and `d1'` follow from differentiating `rho=1/J` and `lambda=1/L` with `mu,nu,r` fixed (`STRUCTURE.md:149-161`). This avoids the common error of differentiating after a moving coordinate congruence.

### 5. Fisher-invisible two-plane

On the two-plane where `m=p=q=h=0`, the conditional Fisher quadratic form and its fixed-direction derivative vanish at the quadratic-form level, since both terms in
`8 y'^T G y + 4 y^T G' y` contain `y` (`STRUCTURE.md:167-179`). The inverse map gives
`eta=0`, `xi=-u mu alpha/2`, `omega=-u nu beta/2`, and
`gamma=-u^2(av alpha+bw beta)` (`STRUCTURE.md:171-177`).

Substituting these into the sparse `Q` from `frozen_issue52.md:34-43` gives the two diagonal terms and the mixed coefficient shown in `STRUCTURE.md:179-187`. The mixed coefficient cancels because

```text
u^2(n2*b+n1*a)
= 4u^3[(b+a)/J + r(b-a)/L]
= 4u^3[1/J - r^2/L]
= 4u^3(1-r^2)/(JL)
= n3.
```

Thus the invisible block is the positive diagonal form with
`d_alpha=n2*a*u^2*v/2>0` and `d_beta=n1*b*u^2*w/2>0`
(`STRUCTURE.md:189-205`). This is a real two-dimensional local certificate, but only for the Fisher-invisible block, as the note says.

### 6. Coupling rows and Schur factor

The unsimplified coupling rows in `STRUCTURE.md:227-233` are the sum of the fixed-direction Fisher derivative couplings and the `Q` couplings after substituting the inverse map. Simplifying them with the displayed `G`, `n1,n2`, and `theta=a*nu+b*mu` gives

```text
L_alpha(y) = 8u*v*d1*(-2b*m + theta*p + 2a*w*h),
L_beta(y)  = 8u*w*d1*(-2a*m + theta*q + 2b*v*h),
```

as stated at `STRUCTURE.md:218-225`. The remaining `y` block

```text
R0 = 4(R^T G + G R + G')
     + diag(0, n2*v/(2u^2a), n1*w/(2u^2b), n3*vw/(2u^4ab))
```

also follows from the fixed-direction derivative and the diagonal `Q` contributions in the inverse variables (`STRUCTURE.md:235-240`).

The Schur complement has the stated `1/4` factors. In the quadratic form

```text
d_alpha alpha^2 + alpha L_alpha(y) + y^T R0 y,
```

the actual matrix off-diagonal row is `ell_alpha/2`, because `2 alpha*(ell_alpha/2)y = alpha L_alpha(y)`. Eliminating `alpha` therefore subtracts
`ell_alpha ell_alpha^T/(4d_alpha)`, and likewise for `beta`
(`STRUCTURE.md:242-254`). Since `d_alpha,d_beta>0`, positivity of the full conditional matrix is equivalent to positivity of this `Rstar`.

### 7. Negative-vector back-map

If a vector `y` satisfies `y^T Rstar y<0`, choosing

```text
alpha = -L_alpha(y)/(2d_alpha),
beta  = -L_beta(y)/(2d_beta)
```

minimizes over the two positive diagonal directions and gives the same negative Schur value. The formulas in `STRUCTURE.md:256-266` then map this reduced vector back to an exact original six-vector. Because all denominators in the inverse map are positive on the open domain, this is a valid obstruction back-map for the literal `M` problem.

### 8. Fresh determinant bookkeeping

Let `T` be the coordinate map

```text
(alpha,beta,gamma,eta,xi,omega)
  -> (alpha,beta,m,p,q,h)
```

in the source order of `STRUCTURE.md:67-92`. Its Jacobian is block triangular after the first two identity rows. The remaining four output variables have pivots

```text
gamma -> m              coefficient 1,
xi    -> p              coefficient -2ua,
omega -> q              coefficient -2ub,
eta   -> h              coefficient 2u^2ab.
```

The nonzero permutation has positive sign, so

```text
det T = 1*(-2ua)*(-2ub)*(2u^2ab)
      = 8u^4a^2b^2.
```

This proves the first proposed determinant identity.

For the second identity, let `M_red` be the matrix of the same quadratic form in the reduced coordinates `(alpha,beta,m,p,q,h)`. Because reduced coordinates equal `T zeta`,

```text
M_red = T^{-T} M T^{-1},
det M = (det T)^2 det M_red.
```

By the Schur decomposition in `STRUCTURE.md:242-254`,

```text
det M_red = d_alpha d_beta det Rstar.
```

Using `d_alpha=n2*a*u^2*v/2` and `d_beta=n1*b*u^2*w/2`
(`STRUCTURE.md:195-200`) gives

```text
det M
= (8u^4a^2b^2)^2
   * (n2*a*u^2*v/2)
   * (n1*b*u^2*w/2)
   * det Rstar
= 16 n1 n2 u^12 a^5 b^5 v w det Rstar.
```

All prefactors are strictly positive in the open domain, so the determinant sign is exactly the sign of `det Rstar` for this conditional reduction. Boundary factors may vanish only at excluded boundaries, so this identity should not be used to infer boundary behavior without a separate limit analysis.

## Specific correction / addition

The structural note should add the determinant bookkeeping above, including the orientation of the coordinate map `T` and the relation
`M_red = T^{-T} M T^{-1}`. Without that orientation, the determinant formula is easy to invert accidentally. With it stated, both proposed identities are correct.

No other correction is needed for the scoped structural algebra.

## Limitations

The reduction is conditional on the literal issue52 formula `M=d/du(Fmat)+Q` from `frozen_issue52.md:43`. As the note itself states, it does not verify the all-eight-event derivation of that formula (`STRUCTURE.md:3-13`, `304-310`). It also does not prove positive definiteness of `Rstar`, determinant nonvanishing, inertia continuation, a rational negative direction, an entropy Hessian sign, or a Jensen counterexample (`STRUCTURE.md:291-310`). The global `Rstar/M` sign remains open.
