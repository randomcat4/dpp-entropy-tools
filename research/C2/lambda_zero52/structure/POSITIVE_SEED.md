# Exact positive seed for the issue52 matrix

STATUS: AUTHOR CANDIDATE, pending nonauthor review.

This is a hand-derived seed calculation from the frozen `STRUCTURE.md`
reduction. No Python, CAS, or arithmetic process was launched. It supplies only
one strictly positive seed, not determinant nonvanishing on the parameter
domain.

Set `mu=nu=r=0` and `u=1/2`. Then

```text
a=b=1/2, v=w=1/4, J=15/16, L=1,
d0=31/30, d1=1/30, d0'=d1'=64/225,
n1=n2=32/15, n3=8/15,
d_alpha=d_beta=1/30.
```

In the `(m,p,q,h)` order of STRUCTURE.md, the two coupling rows agree:

```text
ell_alpha = ell_beta = (1/30)*(-1,0,0,1/4).
```

The uneliminated four-dimensional block is

```text
R0 = (1/225) *
[ 256    0     0    94 ]
[   0 1474    94     0 ]
[   0   94  1474     0 ]
[  94    0     0   721 ].
```

The two Schur corrections sum to
`(1/60)*(-1,0,0,1/4)^T*(-1,0,0,1/4)`. Consequently

```text
Rstar = (1/14400) *
[ 16144      0      0   6076 ]
[     0  94336   6016      0 ]
[     0   6016  94336      0 ]
[  6076      0      0  46129 ].
```

Each diagonal entry exceeds the sum of absolute off-diagonal entries in its
row. Before division by 14400, the four strict margins are

```text
(10068, 88320, 88320, 40053).
```

For a real symmetric matrix, the elementary inequality
`2|z_i z_j| <= z_i^2+z_j^2` bounds its quadratic form below by the sum of these
positive row margins times `z_i^2/14400`. Hence `Rstar` is positive definite.
The eliminated block is `diag(1/30,1/30)`, and the forward coordinate map has
`det T=1/32`, so the reviewed congruence and Schur identity imply that the
original six-direction `M` is positive definite at this one strict interior
point.

The full four-parameter domain is connected, but this seed alone does not
justify inertia continuation. A separate exact certificate that `det M` never
vanishes on that domain remains necessary.
