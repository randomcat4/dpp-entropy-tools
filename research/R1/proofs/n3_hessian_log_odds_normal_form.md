# General `3 x 3` Hessian log-odds normal form

Status: `EXACT_REDUCTION / GLOBAL_RESIDUAL_OPEN`.

This note compresses the general complete-event entropy Hessian to four
log-linear interactions and then rewrites them as six signed conditional pair
odds.  It is a reduction, not a proof of global `3 x 3` concavity.

## Four-dimensional event acceleration

For a strict real-symmetric kernel `K` and direction `V`, write

```text
q_A=det K_A,             p_S=sum_{T subset S^c}(-1)^|T|q_{S union T},
u_S=p'_S,                w_S=p''_S.
```

Only the three pair and one triple inclusion minors have nonzero second
derivatives.  Set

```text
sigma_ij=q''_ij=2(V_ii V_jj-V_ij^2),
tau=q''_123.
```

In event order `empty,1,2,3,12,13,23,123`, Mobius inversion gives

```text
w123=tau,
w12=sigma12-tau,       w13=sigma13-tau,       w23=sigma23-tau,
w1=-sigma12-sigma13+tau,
w2=-sigma12-sigma23+tau,
w3=-sigma13-sigma23+tau,
wempty=sigma12+sigma13+sigma23-tau.                    (1)
```

Thus `w` satisfies total-mass conservation and the three zero one-point
second-derivative constraints.  Conversely those four constraints recover
`sigma12,sigma13,sigma23,tau`; this is the full four-dimensional acceleration
space.

Define

```text
F=sum_S u_S^2/p_S,

theta12=log(pempty p12/(p1p2)),
theta13=log(pempty p13/(p1p3)),
theta23=log(pempty p23/(p2p3)),

theta123=log(p123 p1p2p3/(p12p13p23pempty)).
```

The four theta coefficient vectors are dual to (1).  Hence

```text
D^2H(K)[V,V]
=-F-sigma12 theta12-sigma13 theta13-sigma23 theta23-tau theta123. (2)
```

The global Hessian conjecture is exactly the scalar residual inequality

```text
R=F+sum sigma_ij theta_ij+tau theta123>=0.              (3)
```

This is “minimal” only in the precise linear sense that both the event
acceleration space and log potentials modulo constants and one-body terms
have dimension four.

## What the proved `n=2` theorem removes

For edge `e={i,j}`, aggregate the full atoms to its two-point marginal and
write

```text
rho_e=log(P00 P11/(P10 P01)),
F_e=sum four marginal score squares/probabilities,
R_e=F_e+sigma_e rho_e>=0.
```

The last inequality is the proved `n=2` concavity theorem.  Fisher data
processing gives `F_e<=F`.  Therefore, for nonnegative edge weights with
`sum alpha_e<=1`, the exact identity

```text
R=sum_e alpha_e R_e
 +(F-sum_e alpha_e F_e)
 +sum_e sigma_e(theta_e-alpha_e rho_e)+tau theta123     (4)
```

separates two already nonnegative pieces from a genuine three-body remainder.
For example, `alpha_e=1/3` gives a symmetric explicit sufficient target.  The
remainder in (4) has not been proved nonnegative.

The more rigid strategy of forcing the three pair log terms to cancel and
leaving only one scalar three-body interaction is obstructed.  At the strict
rational point

```text
K_ii=2/5,       K_ij=1/20,       V=I,
```

the forced symmetric weight is about `1.165762`, while

```text
F_123-alpha(F_12+F_13+F_23) about -16.68539.
```

This retires that naive Fisher decomposition only; it is not an entropy
counterexample.

## Six conditional pair odds

Let `L=K(I-K)^(-1)` and normalize its diagonal to obtain

```text
R_L=[[1,x,y],[x,1,z],[y,z,1]],
Delta=det R_L=1+2xyz-x^2-y^2-z^2>0.
```

The L-ensemble event formula gives

```text
theta12=log(1-x^2),       theta13=log(1-y^2),
theta23=log(1-z^2),
theta123=log[Delta/((1-x^2)(1-y^2)(1-z^2))].           (5)
```

For each pair `e`, let `ell_e^0` and `ell_e^1` be its conditional log odds
when the third point is absent or present.  All six are nonpositive.  For
example,

```text
ell12^0=log(1-x^2),
ell12^1=log[Delta/((1-y^2)(1-z^2))]
       =log[1-(x-yz)^2/((1-y^2)(1-z^2))]<=0.
```

The three differences coincide:

```text
ell_e^1-ell_e^0=theta123.                              (6)
```

Consequently, for arbitrary `beta_e` satisfying `sum beta_e=tau`,

```text
Lambda=sum sigma_e theta_e+tau theta123
      =sum_e[(sigma_e-beta_e)ell_e^0+beta_e ell_e^1].  (7)
```

This is a two-free-parameter gauge of the same log functional.  Put
`a_e^k=-ell_e^k>=0` and define

```text
D(beta)=sum_e[(sigma_e-beta_e)_+ a_e^0+(beta_e)_+ a_e^1],
D_*=inf_{sum beta=tau}D(beta).                          (8)
```

Then `Lambda>=-D_*`, so the pointwise scalar inequality

```text
F>=D_*                                                   (9)
```

is sufficient for concavity.  The infimum in (8) is only a two-dimensional
convex piecewise-linear problem.  A narrow exact sign cone has `D_*=0`: it is
enough that

```text
sigma_e<=0 for all e,       sum_e sigma_e<=tau<=0.      (10)
```

The allocation problem admits a sharper exact collapse.  The identity

```text
a x_+=max_{0<=s<=a} sx
```

and ordinary linear-program duality give

```text
D_*=max [r tau+sum_e s_e sigma_e],
r in [-min_e a_e^0,min_e a_e^1],
s_e in [max(0,-r),min(a_e^0,a_e^1-r)].                (11)
```

There is no gap, including when some conditional odds vanish: the relevant
dual interval then simply collapses.  Moreover, (6) implies that

```text
delta:=a_e^1-a_e^0=-theta123
```

is independent of the edge.  Put

```text
m=min_e a_e^0,
P=sum_e max(sigma_e,0),
N=sum_e min(sigma_e,0),
C=sum_e max(sigma_e,0)a_e^0.
```

Here `N<=0` is the signed negative part.  Optimizing `s_e` in (11) leaves the
one-dimensional concave piecewise-linear function

```text
G(r)=C+r tau+P min(0,delta-r)+N max(0,-r),
-m<=r<=m+delta.                                        (12)
```

Its only interior breakpoints are `0` and `delta`, both of which lie in the
displayed interval.  Consequently

```text
D_*=max{G(-m),G(0),G(delta),G(m+delta)},               (13)

G(-m)=C-m tau+mN,
G(0)=C+P min(0,delta),
G(delta)=C+delta tau+N max(0,-delta),
G(m+delta)=C+(m+delta)tau-mP.
```

Duplicate points are removed in degenerate cases.  Thus (9) is exactly four
explicit signed quadratic-form comparisons, rather than a residual
two-dimensional optimization.

No proof of (9) for all strict kernels and directions is known here.  Equations
(2)--(13) expose the remaining general `3 x 3` obstacle without reviving the
retired mutual-information route.

## Verification

Dependency-free rational scripts checked the Mobius event jets, the four
coefficient vectors, edge aggregation, L-ensemble ratios, conditional-odds
relations, and the beta representation.  Each exited `0`.  Independent
nonauthor reviews returned `CORRECT` for both exact reductions and confirmed
that general `3 x 3` concavity remains open.  The additional dual collapse
(11)--(13) is an exact linear-program calculation; it introduces no finite
search or new global concavity claim.
