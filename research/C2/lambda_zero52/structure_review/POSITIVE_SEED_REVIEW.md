# Positive seed review for issue52 lambda_zero

STATUS: CORRECT

This is a fresh nonauthor analytic review of the root-authored seed candidate
`research/C2/lambda_zero52/structure/POSITIVE_SEED.md` at frozen local commit
`1188443de2a147164ba9c951ffbd6da2936a7327`.  The review is only for the
single seed point `mu=nu=r=0`, `u=1/2`, conditional on the previously reviewed
STRUCTURE reduction.  It does not prove global `Rstar` positivity, determinant
nonvanishing, inertia continuation, or the all-event derivation of
`M=d/du Fmat+Q`.

No Python, SymPy, CAS, numerical arithmetic process, or scout was launched.

## Checked formulas

The substitutions in POSITIVE_SEED.md lines 10-17 are correct:
`a=b=1/2`, `v=w=1/4`, `J=15/16`, `L=1`,
`d0=31/30`, `d1=1/30`, `d0'=d1'=64/225`,
`n1=n2=32/15`, `n3=8/15`, and
`d_alpha=d_beta=1/30`.

The coupling rows in lines 19-23 are correct.  In STRUCTURE notation,
`theta=a*nu+b*mu=0`, and
`8u*v*d1=8u*w*d1=1/30`.  The inner factors reduce to
`-m+h/4` for both rows, so

```text
ell_alpha = ell_beta = (1/30)*(-1,0,0,1/4).
```

The displayed `R0` in lines 25-33 is correct.  At the seed point,
`R=diag(0,2,2,4)`, `G=d0*D+d1*S`, and `G'=64/225*(D+S)`.  The sparse `Q`
diagonal additions in `(m,p,q,h)` are `0`, `32/15`, `32/15`, and `16/15`.
Substitution into
`R0=4(R^T G+G R+G')+diag(...)` gives exactly

```text
R0 = (1/225) *
[ 256    0     0    94 ]
[   0 1474    94     0 ]
[   0   94  1474     0 ]
[  94    0     0   721 ].
```

The rank corrections in lines 35-43 are correct.  Since
`d_alpha=d_beta=1/30` and the two coupling rows are equal, the two Schur
corrections sum to

```text
(1/60)*(-1,0,0,1/4)^T*(-1,0,0,1/4).
```

Converting `R0` to denominator `14400` and subtracting this correction gives
the displayed

```text
Rstar = (1/14400) *
[ 16144      0      0   6076 ]
[     0  94336   6016      0 ]
[     0   6016  94336      0 ]
[  6076      0      0  46129 ].
```

The integer row margins in lines 46-51 are correct:

```text
(16144-6076, 94336-6016, 94336-6016, 46129-6076)
= (10068, 88320, 88320, 40053).
```

The positive-definiteness implication in lines 53-59 is valid.  The displayed
matrix is real symmetric, has positive diagonal entries, and is strictly
diagonally dominant by rows; equivalently,
`2|z_i z_j| <= z_i^2+z_j^2` bounds the quadratic form below by the positive row
margins divided by `14400`.  Hence `Rstar` is positive definite at this seed.
Together with the positive eliminated block `diag(1/30,1/30)`, Schur complement
equivalence gives positive definiteness in the `(alpha,beta,m,p,q,h)` variables.
Finally, the forward coordinate map has
`det T=8u^4a^2b^2=1/32` at the seed point, so the invertible pointwise
congruence from STRUCTURE transfers positive definiteness to the original
six-direction matrix `M` at this one strict interior point.

## Scope boundary

This is only a checked positive seed.  It can serve as a base point for a later
exact determinant/nonvanishing computation, but it supplies no global sign
certificate by itself.
