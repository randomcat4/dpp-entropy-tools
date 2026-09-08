# Single-edge matrix reduction on the equicorrelation family

Status: `EXACT_SINGLE_SCALAR_RESIDUAL / GLOBAL_SIGN_OPEN`.

This note treats only the remaining single-edge matrix from
`n3_equicorrelation_dstar_reduction.md`.  It reduces that `6 x 6` matrix to
one explicit scalar inequality and proves two analytic sufficient regions.
The scalar's sign on the full parameter domain is not proved.

Let `0<mu<=lambda<1`, and set

```text
a=(2lambda+mu)/3,       c=(mu-lambda)/3,       d=a+c,
A=-ell_e^0,             B=-ell_e^1,            delta=B-A.
```

Thus `A,delta>=0` and `A<1/3`.  For diagonal direction coordinates `h_i`
and opposite-edge coordinates `(r1,r2,r3)=(V23,V13,V12)`, the target is

```text
M(V)=F(V)-delta tau(V)-A sigma23(V)>=0.                 (1)
```

This is stronger than the entropy Hessian inequality.  A failure would
retire only the sufficient route `F>=D_*`.

## Trivial and standard blocks before the edge update

For a unit vector `e` orthogonal to `(1,1,1)`, the standard sector
`h=x e,r=y e` has Fisher and determinant-acceleration matrices

```text
Fs11=(1-a)^2/p1+a^2/p2,
Fs12=2c[a/p2-(1-a)/p1],
Fs22=4c^2(1/p1+1/p2),
Ts=[[-a,-2c],[-2c,-2d]].
```

For normalized trivial coordinates `h=x 1/sqrt(3),r=y 1/sqrt(3)`, define

```text
v3=(lambda d,-2lambda c),
v0=(2a-1-lambda d,-2c+2lambda c),
b1=(1-4a+3lambda d,(4-6lambda)c),
b2=(2a-3lambda d,(6lambda-2)c).
```

With the per-atom probabilities `p0,p1,p2,p3` from the preceding family
reduction,

```text
Ft=3 v0^T v0/p0+b1^T b1/p1+b2^T b2/p2+3 v3^T v3/p3,
Tt=[[2a,-2c],[-2c,4c-2a]].
```

Put

```text
T=Ft-delta Tt=[[t11,t12],[t12,t22]],
S=Fs-delta Ts=[[s11,s12],[s12,s22]],
dt=det T,       ds=det S.                               (2)
```

For `mu<lambda`, both `T` and `S` are positive definite.  Indeed, `F` is
positive definite because zero complete-event first jet forces first the
diagonal and then, since `c!=0`, every off-diagonal entry of `V` to vanish.
The form `-Ts` is positive definite with eigenvalues `lambda,mu` after the
standard rescaling, proving the assertion for `S`.  For a pure trivial
direction, the already reviewed equicorrelation Hessian theorem gives
`F>=A Sigma+delta tau`.  If `tau>0`, its eigenvalue-velocity formulas imply
`Sigma>tau>0`; if `tau<=0`, positive definiteness of `F` suffices.  Hence
`F-delta tau>0`, proving the assertion for `T` without assuming (1).

## Stabilizer decomposition

The transposition `(23)` preserves (1).  Its odd subspace is

```text
h=(0,u,-u),       r=(0,v,-v).
```

Since `sigma23=-2u^2`, its block is

```text
O=2[S+A diag(1,0)],       det O=4(ds+A s22)>0.           (3)
```

Thus the odd block is automatically positive definite.  Parameterize the
even subspace by

```text
h=m(1,1,1)+u(2,-1,-1),
r=n(1,1,1)+v(2,-1,-1).
```

In coordinate order `(m,n,u,v)`, set

```text
R0=diag(3T,6S),
alpha=(1,0,-1,0)^T,       beta=(0,1,0,2)^T.
```

Because `sigma23=2[(m-u)^2-(n+2v)^2]`, the even block is

```text
E=R0+2A beta beta^T-2A alpha alpha^T
 =[[3t11-2A,3t12,2A,0],
   [3t12,3t22+2A,0,4A],
   [2A,0,6s11-2A,6s12],
   [0,4A,6s12,6s22+8A]].                                (4)
```

## One necessary-and-sufficient scalar

The matrix `C0=R0+2A beta beta^T` is positive definite.  The rank-one
downdate criterion and Sherman--Morrison identity show that `E>=0` is
equivalent to

```text
Psi=(1-2AU)(1+2AV)+4A^2W^2>=0,                          (5)
U=t22/(3dt)+s22/(6ds),
V=t11/(3dt)+2s11/(3ds),
W=-t12/(3dt)+s12/(3ds).
```

The factor `1+2AV` is strictly positive, so this is not a determinant-only
test.  Clearing the positive denominators, define

```text
L=(2t11-2t22)ds+(4s11-s22)dt,
J=2ds+2dt+4t22 s11+t11 s22+4t12 s12,
Phi=9dt ds+3A L-2A^2 J.                                (6)
```

Then

```text
Psi=Phi/(9dt ds),       det E=36 Phi,
M_{23}>=0 iff Phi(lambda,mu)>=0                         (7)
```

for `0<mu<lambda<1`.  Also `J>0`: it is the positive Gram determinant of
the independent vectors `alpha,beta` in the `R0^{-1}` metric, after clearing
denominators.

## Two covered parameter regions

Log-determinant concavity and Fisher aggregation for the edge inclusion event
and the full event give

```text
sigma23<=F,       tau<=F.
```

Therefore `M>=(1-B)F`, and the whole region `B<=1` is covered.  The sharper
event/complement Cauchy bound is

```text
(q')^2/q<=(1-q)F,
q=det K23=lambda(lambda+2mu)/3,
p3=lambda^2 mu.
```

It yields the additional sufficient region

```text
A(1-q)+delta(1-p3)<=1.                                 (8)
```

On the product line `mu=lambda`, `A=delta=c=0` and (1) reduces directly to
`F>=0`; the inverse formulas above are not used there.  Outside (8), the sign
of the exact scalar (6) remains open.  The double-edge matrix and general
connected `3 x 3` concavity also remain open.

The dependency-free formal script in `certificate/phase4/scripts` checks all
36 congruence entries, the odd determinant, `det E=36 Phi`, and the Gram
identity.  It performs zero parameter evaluations and does not certify the
open sign of `Phi`.
