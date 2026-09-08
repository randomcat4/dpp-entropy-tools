# P4-03 exact `S_3` reduction for the equicorrelation center

Status: `DERIVED / SIGN NOT CLOSED`

Let

```text
K=(a-c)I_3+c11^T,
lambda=a-c,   mu=a+2c,
```

so strict feasibility is exactly `lambda,mu in (0,1)`.  Permutation symmetry
makes every exact subset of the same size equiprobable.  Boolean Möbius
inversion gives the per-subset probabilities

```text
p0=(1-lambda)^2(1-mu),
p1=(1-lambda)(2lambda+mu-3lambda mu)/3,
p2=lambda(lambda+2mu-3lambda mu)/3,
p3=lambda^2 mu.
```

Thus the entropy on the two-dimensional trivial representation is

```text
h(lambda,mu)=-p0 log p0-3p1 log p1-3p2 log p2-p3 log p3.       (T)
```

Because `(lambda,mu)` is an invertible affine change from `(a,c)`, proving
the Hessian of (T) negative semidefinite is exactly the trivial-sector
obligation.

The six-dimensional real-symmetric direction space splits under simultaneous
row/column permutations into two trivial copies and two equivalent standard
copies.  Hence the full Hessian is determined by the trivial `2x2` block and
one standard `2x2` block.

For the standard block use the unnormalized directions

```text
D=diag(1,-1,0),
O=[[0,0,-1],[0,0,1],[-1,1,0]].
```

Put

```text
R=p1 p2,
M=p1+p2=a(1-a)+c^2,
T=log(p0 p2^3/(p1^3 p3)),
U=log(p0 p2/p1^2).
```

Exact differentiation of all eight complete events gives

```text
H_DD = -(2/R)[a^2 p1+(1-a)^2 p2+R(aT-U)],

H_DO = -(4c/R)[c^2(1-2(a-c))+RT],

H_OO = -(4/R)[2c^2M+R((a+c)T-U)].              (S)
```

The second standard copy has the identical block and the cross-isotypic
entries vanish by `S_3` invariance.  Formula (S) was derived independently
from the signed exact-event determinant expression and checked against the
full numerical Hessian away from cancellation boundaries.

Therefore the frozen six-dimensional theorem is reduced to two explicit
`2x2` sign problems: the Hessian of (T), and negative semidefiniteness of (S).
No implication from the proved `n=2` theorem is used, and the sign of either
block remains open in this file.

## Retained floating failure

A 50,000-point probe (seed `20260908403`) produced a raw positive eigenvalue
`0.01035` only at

```text
lambda = 0.9999999999999886,
mu     = 0.9999999999999882,
c      = -1.11e-16,
min exact-event probability about 1.54e-42.
```

The raw Hessian violated its exact `S_3` block structure at absolute scale
`4.44e-2` while other eigenvalues were about `-8.66e13`, exposing catastrophic
cancellation.  Independent 90- and 140-digit evaluation found the maximum
eigenvalue to be

```text
-0.00027962742674825590131955...
```

and an independent signed-determinant directional formula and finite chord
agreed.  The raw positive value is therefore a rejected floating artifact,
not a counterexample.  The failed raw probe remains counted and recorded.
