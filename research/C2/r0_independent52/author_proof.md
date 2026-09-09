# Independent r=0 author proof

Status: AUTHOR PASS, pending fresh nonauthor FIRST review.  The guarded
author run of `implementation/verify_r0_chain_independent.py` finished
with `RESULT.json` status `PASS` in 9.707 seconds.  The recorded process
was PID 173696, started at 13:32:37 UTC and ended at 13:32:47 UTC, with
the shared absolute deadline at 14:17:37 UTC.  This is an author-produced
candidate proof for issue52 comment 5602242678; it is not a nonauthor FIRST
acceptance.

## Frozen statement

Work only at `r=0`.  For every

```text
|mu| < 1, |nu| < 1, 0 < u < 1,
```

the goal is to prove positive definiteness of the six fixed physical
direction quadratic form `M` from the frozen issue52 Lambda-zero reduction.
The implementation starts from the displayed four-by-four Schur complement
in `inputs/source/structure/STRUCTURE.md`; it does not reconstruct the old
eight-event formula and does not import any old checker or saved matrix.

## Four-dimensional Schur complement

At `r=0`,

```text
a=b=1/2, v=(1-mu^2)/4, w=(1-nu^2)/4, J=1-u^4, L=1,
n1=n2=4u/J, n3=4u^3/J.
```

The verifier builds

```text
D=diag(1,v,w,vw),
G=d0*D+d1*S,
d0=(1/J+1)/2, d1=(1/J-1)/2,
R=diag(0,1/u,1/u,2/u),
G'=d0'*D+d1'*S, d0'=d1'=2u^3/J^2,
```

using the displayed matrix `S` in the frozen source.  It then forms

```text
R0 = 4(R^T G + G R + G')
     + diag(0, n2*v/(2u^2a), n1*w/(2u^2b), n3*vw/(2u^4ab)).
```

The two coupling rows in `(m,p,q,h)` order are

```text
ell_alpha = 8u*v*d1*(-1, (mu+nu)/2, 0, w),
ell_beta  = 8u*w*d1*(-1, 0, (mu+nu)/2, v).
```

With

```text
d_alpha = n2*a*u^2*v/2, d_beta = n1*b*u^2*w/2,
```

the displayed Schur complement is

```text
Rstar = R0
        - (1/(4d_alpha)) ell_alpha^T ell_alpha
        - (1/(4d_beta))  ell_beta^T  ell_beta.
```

The verifier separately checks the reflection identity
`S D^{-1} S = D`, the null-block cancellation
`u^2(n2*b+n1*a)=n3`, and equality of the simplified coupling rows with the
unsimplified rows from the frozen structure note.  It rejects any SymPy
`Float` atom in these mathematical objects.

## Determinant certificate

The guarded run cleared the actual rational denominators of `Rstar`,
computed the determinant of the cleared polynomial matrix with an in-script
Bareiss elimination, and independently recomputed the same determinant by
the 24-term Leibniz expansion of the original four-by-four matrix.  The two
determinants are exactly equal in
[`determinant_independent_equality.json`](outputs/author01/artifacts/determinant_independent_equality.json).

The Bareiss records are exact symbolic division certificates only: their
remainders must be zero in the polynomial ring after denominator clearing.
No proof step assumes that an intermediate Bareiss pivot is nonzero at every
point of the domain.

From the resulting determinant the run extracted an integer polynomial
`P(mu,nu,u)` through

```text
det Rstar = (1-mu^2)^2(1-nu^2)^2 P / (2(1-u^4)^5).
```

The artifact [`P_polynomial.json`](outputs/author01/artifacts/P_polynomial.json)
verifies the identity above exactly, proves that no denominator remains,
and records `P` as a 26-term `ZZ` polynomial of degree box `(4,4,16)`.
The fresh `P` also exactly matches the archived
`coefficient_report["source_factor"]` in
[`archived_P_source_factor_comparison.json`](outputs/author01/artifacts/archived_P_source_factor_comparison.json).

## Positive orthant polynomial

The proof uses the substitution

```text
mu=(X-1)/(X+1), nu=(Y-1)/(Y+1), u=U/(1+U).
```

For `X,Y,U>0`, this is a bijective parametrization of
`|mu|<1, |nu|<1, 0<u<1`, with inverse

```text
X=(1+mu)/(1-mu), Y=(1+nu)/(1-nu), U=u/(1-u).
```

The verifier constructed

```text
Q = (X+1)^4 (Y+1)^4 (U+1)^16
    P((X-1)/(X+1), (Y-1)/(Y+1), U/(U+1)).
```

It did this in two independent ways: direct homogeneous substitution and
coefficient-wise binomial expansion.  The difference is the zero polynomial
in [`Q_polynomial_full_box.json`](outputs/author01/artifacts/Q_polynomial_full_box.json).
The run checked the entire `5 x 5 x 17` degree box, including omitted zero
coefficients, and compared the completed box against the archived
coefficient table only after the fresh `Q` had been built.

The completed box has 425 entries: 389 positive nonzero coefficients and
36 zero coefficients.  The minimum positive coefficient is 192 and the
maximum coefficient is 99220032.  All archived coefficients match exactly
in [`archived_coefficient_comparison.json`](outputs/author01/artifacts/archived_coefficient_comparison.json).
Therefore `Q(X,Y,U)>0` for every `X,Y,U>0`.

All factors used to clear denominators in this substitution are positive on
the positive orthant, so `Q>0` implies `P>0` on the original open domain.
The determinant identity then implies `det Rstar` never vanishes on the
open r=0 domain, since `(1-mu^2)^2`, `(1-nu^2)^2`, `2`, and `(1-u^4)^5`
are strictly positive there.

## Seed and inertia continuation

The run computed the seed from the rebuilt `Rstar`, not from the old seed
table.  At

```text
mu=0, nu=0, u=1/2,
```

it scaled the exact rational `Rstar` by 14400 and verified strict diagonal
dominance.  The row margins before division by 14400 are

```text
10068, 88320, 88320, 40053.
```

These positive margins, recorded in
[`positive_seed_certificate.json`](outputs/author01/artifacts/positive_seed_certificate.json),
show that `Rstar` is positive definite at one strict interior point.

The domain

```text
(-1,1) x (-1,1) x (0,1)
```

is connected.  The entries of the real symmetric matrix `Rstar` are
continuous wherever the listed denominator factors are positive.  Since
`det Rstar` is nonzero everywhere in the connected domain, no eigenvalue can
cross zero along any path in the domain.  The positive seed therefore fixes
the inertia of `Rstar` as four positive eigenvalues throughout the domain.

## Lift back to the six fixed directions

The frozen structure note gives a positive eliminated block

```text
d_alpha alpha^2 + d_beta beta^2,
```

where

```text
d_alpha = n2*a*u^2*v/2 > 0,
d_beta  = n1*b*u^2*w/2 > 0.
```

The full reduced quadratic form in `(alpha,beta,m,p,q,h)` has this positive
two-dimensional block, the two coupling rows, and four-dimensional block
`R0`.  By the exact Schur complement criterion, positivity of `Rstar`
implies positivity of the reduced six-dimensional form.

Finally, the displayed change of variables between the original fixed
physical direction coordinates

```text
zeta=(alpha,beta,gamma,eta,xi,omega)
```

and `(alpha,beta,m,p,q,h)` is invertible for `u,a,b>0`.  At `r=0`,
`a=b=1/2`, so the congruence preserves positive definiteness.  Therefore,
the author artifacts establish the candidate conclusion that the original
six fixed physical direction matrix `M` is positive definite for all
`|mu|<1, |nu|<1, 0<u<1` at `r=0`.

## Artifacts

- [`RESULT.json`](outputs/author01/RESULT.json): AUTHOR PASS.
- [`determinant_independent_equality.json`](outputs/author01/artifacts/determinant_independent_equality.json): two determinant methods match exactly.
- [`P_polynomial.json`](outputs/author01/artifacts/P_polynomial.json): 26-term `ZZ` polynomial, degree `(4,4,16)`.
- [`archived_P_source_factor_comparison.json`](outputs/author01/artifacts/archived_P_source_factor_comparison.json): fresh `P` matches archived `source_factor`.
- [`Q_polynomial_full_box.json`](outputs/author01/artifacts/Q_polynomial_full_box.json): direct and combinatorial transforms match; full 425-entry box checked.
- [`archived_coefficient_comparison.json`](outputs/author01/artifacts/archived_coefficient_comparison.json): all archived `Q` coefficients match, including omitted zeros.
- [`positive_seed_certificate.json`](outputs/author01/artifacts/positive_seed_certificate.json): scale 14400, margins `(10068,88320,88320,40053)`.
- [`domain_inertia_certificate.json`](outputs/author01/artifacts/domain_inertia_certificate.json): domain, nonvanishing, inertia, and Schur-lift chain recorded.

This remains an author proof.  Fresh nonauthor FIRST review is still the
next acceptance gate.
