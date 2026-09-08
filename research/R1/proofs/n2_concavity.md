# Global concavity for real symmetric `2 x 2` DPP kernels

Status: `PROVED / AWAITING COMMIT-BOUND REVIEW`

This proves `frozen_n2_concavity_v1.md`.  It uses the exact four-event law;
principal minors enter only as inclusion probabilities before Mobius
inversion.

## Exact event coordinates

Write

```text
K = [[a,c],[c,b]],       V = [[u,w],[w,v]],
d = det K = ab-c^2,      q = det V = uv-w^2.
```

For `0<K<I`, the four exact event probabilities are

```text
A = p00 = 1-a-b+d,
B = p10 = a-d,
C = p01 = b-d,
D = p11 = d.
```

They are strictly positive, sum to one, and satisfy

```text
r = BC-AD = c^2 >= 0.
```

Along `K+sV`, put `alpha=d'(0)=bu+av-2cw`.  The first event-probability
derivative and the second derivative are

```text
x   = (-u-v+alpha, u-alpha, v-alpha, alpha),
p'' = 2q(1,-1,-1,1).
```

Consequently

```text
H''(K)[V,V] = -F+2qL,                         (1)
F = x0^2/A+x1^2/B+x2^2/C+x3^2/D,
L = log(BC/(AD)) >= 0.
```

## Fisher and determinant forms for `c!=0`

Use `y=(u,v,alpha)`.  Since `r=c^2>0`, this is an invertible change from
`(u,v,w)`, and

```text
w = (bu+av-alpha)/(2c),
q = uv-(bu+av-alpha)^2/(4r).
```

Thus `F=y^T G y` and `q=y^T Q y`, where

```text
G = [[1/A+1/B, 1/A,       -1/A-1/B],
     [1/A,       1/A+1/C, -1/A-1/C],
     [-1/A-1/B, -1/A-1/C, 1/A+1/B+1/C+1/D]],

Q = [[0,1/2,0],[1/2,0,0],[0,0,0]]
    - (1/(4r)) [b,a,-1]^T [b,a,-1].
```

`G` is positive definite: it is the Fisher quadratic form of the positive
four-event law on its three-dimensional simplex tangent space.  `Q` is an
invertible congruence of `uv-w^2`, so it has inertia `(1 positive, 2
negative)`.

Put

```text
P = ABCD,
E = AD(A+D)+BC(B+C).
```

Direct expansion under `A+B+C+D=1` gives

```text
det(G-sQ) = [16r+4sE-s^3P]/(16rP).            (2)
```

The `s^2` coefficient cancels exactly.  An exact symbolic replay accompanies
the proof.

## Scalar sign bounds

Set `X=AD`, `Y=BC`.  Then `r=Y-X>0`, `P=XY`, and
`L=log(Y/X)>0`.  First,

```text
sqrt(P)L <= r.                                (3)
```

Indeed, for `z=sqrt(Y/X)>1`, (3) is `2z log z<=z^2-1`.  The difference has
derivative `2(z-1-log z)>=0` and vanishes at one.  Hence `PL^2<=r^2`.

Second,

```text
E > 4r^2.                                     (4)
```

To see this, put `p=sqrt(X)`, `q0=sqrt(Y)`, and `t=A+D`.  AM-GM gives

```text
t>=2p,  1-t=B+C>=2q0,  p+q0<=1/2,
E=Xt+Y(1-t) >= 2(p^3+q0^3).
```

Writing `sigma=p+q0` and using `2sigma<=1`,

```text
2(p^3+q0^3)-4(q0^2-p^2)^2
 = 2sigma[(p^2-pq0+q0^2)-2sigma(q0-p)^2]
 >= 2sigma[(p^2-pq0+q0^2)-(q0-p)^2]
 = 2sigma*p*q0 > 0.
```

This proves (4), because `r=q0^2-p^2`.

## Positive definiteness and concavity

For every `0<=s<=2L`, (3) implies

```text
s^3P <= s(2L)^2P <= 4sr^2.
```

Therefore the numerator in (2) satisfies

```text
16r+4sE-s^3P >= 16r+4s(E-r^2) > 0.           (5)
```

The determinant of `G-sQ` never vanishes on `0<=s<=2L`.  At `s=0` the
matrix is the positive-definite `G`; a real symmetric matrix can change
inertia only through a zero eigenvalue.  Hence `G-2LQ` is positive definite.
Equation (1) now gives

```text
H''(K)[V,V] < 0
```

for every nonzero real symmetric `V` when `c!=0`.

If `c=0`, then `r=L=0`, and the undivided formula (1) gives `H''=-F<=0`.
Thus the Hessian is negative semidefinite throughout the convex open domain
of strict real symmetric `2 x 2` contractions.  Every exact event probability
is positive there, so `H` is `C^2`.  Restricting to a feasible line proves

```text
[H(K-tV)+H(K+tV)]/2-H(K) <= 0.
```

This is the frozen theorem.  The argument also gives strict inequality when
`t>0` and `V!=0`: if the off-diagonal entry along the line is not identically
zero, the line second derivative is strict except at at most one point; if it
is identically zero, a nonzero diagonal direction has `F>0` everywhere.

## Scope

This proof is dimension-specific.  It does not establish concavity at an
arbitrary non-block-diagonal kernel of dimension three or higher.

