# Actual boundary obstruction and common-leaf-diagonal compensation

## 1. Exact object inherited from accepted PR81

Consider the strict connected half-leaf missing-edge kernel

```text
K=[[1/2,0,b],[0,1/2,c],[b,c,z]],
b^2=A/4, c^2=B/4,
z=q+(A+B)/2,
A,B,q,qbar>0, qbar=1-A-B-q.
```

For `g(t)=log(t/(1-t))`, `f(t)=g'(t)=1/[t(1-t)]`, set

```text
t11=q, t10=q+B, t01=q+A, t00=q+A+B,

a_minus=g(t01)-g(t11), a_plus=g(t00)-g(t10),
b_minus=g(t10)-g(t11), b_plus=g(t00)-g(t01),

J=integral_0^A integral_0^B f(q+s+t) dt ds.
```

Let `(d,e,T00,T10,T01,T11)` be the accepted invertible six-coordinate representation of a physical symmetric direction and put

```text
Delta=T00-T10-T01+T11.
```

For an actual edge `[u,u+s]`, write

```text
h=g(u+s)-g(u), m=h/s,
kappa(u,s)=[f(u)f(u+s)-m^2]
           /[8(f(u)+f(u+s)-2m)].                    (1)
```

The accepted PR81 one-edge completion is

```text
E_s(h;X,Y,delta)
 >= s h [delta-(X+Y)/(4s)]^2
    +kappa(u,s)(X-Y)^2.                              (2)
```

Every quantity in (1)-(2) is tied to the same physical edge. The complete paired quadratic is the sum of its four actual edge terms, the marginal block

```text
4d^2+4e^2+2Jde,
```

and the exact shared-cell term

```text
-J Delta^2/(32AB).                                   (3)
```

This is the full complete-event `-H''`; no conditional side, rare event, Fisher term, acceleration, marginal term, or physical direction is removed.

## 2. The accepted parallel-edge criterion is not universal

PR81 defines

```text
alpha_minus=kappa(q,A),       alpha_plus=kappa(q+B,A),
beta_minus =kappa(q,B),       beta_plus =kappa(q+A,B),
K_A=alpha_minus*alpha_plus/(alpha_minus+alpha_plus),
K_B=beta_minus *beta_plus /(beta_minus +beta_plus).
```

Its strict sufficient condition is

```text
K_A+K_B>J/(32AB).                                    (4)
```

### Theorem 2.1: actual asymptotic failure

Fix `a in (0,1)` and `rho>0`. Put

```text
A=a, B=epsilon, q=rho*epsilon.                       (5)
```

For every sufficiently small positive `epsilon`, (5) is a strict legal half-leaf arrow, but

```text
K_A+K_B<J/(32AB).                                    (6)
```

In fact, the left side of (4) has a finite limit and the right side tends to positive infinity.

### Proof

Let `L=log(1/epsilon)` and

```text
c_a=log[a/(1-a)].
```

Uniformly for `u` in a fixed compact subset of `(0,infinity)`,

```text
g(a+epsilon*u)-g(epsilon*u)
 =L+c_a-log u+o(1).                                  (7)
```

The two horizontal optimal coefficients therefore satisfy

```text
kappa(rho*epsilon,a)       -> f(a)/8,
kappa((rho+1)*epsilon,a)   -> f(a)/8.                (8)
```

To see (8), divide the numerator and denominator of (1) by `f(rho*epsilon)`: the lower-end Fisher weight tends to infinity, the upper-end weight tends to `f(a)`, and `epsilon log(1/epsilon)^2` and `epsilon log(1/epsilon)` tend to zero.

For a shrinking edge at a fixed interior point, Taylor expansion of (1) gives

```text
kappa(a+rho*epsilon,epsilon) -> kappa_0(a),
kappa_0(a)=1/[32a(1-a)(1-3a(1-a))].                 (9)
```

For the lower shrinking edge,

```text
kappa(rho*epsilon,epsilon)=c(rho)/epsilon+o(1/epsilon),
```

with `c(rho)>0`. Positivity follows either from the strict logarithmic-mean determinant in (1), or directly from

```text
c(rho)=
 [1/(rho(rho+1))-log((rho+1)/rho)^2]
 /[8(1/rho+1/(rho+1)-2log((rho+1)/rho))].            (10)
```

Consequently

```text
K_A -> f(a)/16,
K_B -> kappa_0(a).                                   (11)
```

On the other hand, using (7) in

```text
J=integral_(rho*epsilon)^((rho+1)*epsilon)
      [g(a+t)-g(t)] dt,
```

gives

```text
J/epsilon
 =L+c_a-I(rho)+o(1),
I(rho)=integral_rho^(rho+1) log u du.                (12)
```

Thus `J/(32a epsilon)` diverges like `L/(32a)`, while (11) stays finite. This proves (6). The counterfamily is fully realizable; no four-scalar relaxation is involved.

The mismatch scale is therefore simultaneous: merely taking one coupling small with `q` bounded away from zero does not create this logarithmic loss. It occurs when the disappearing edge and a rare selected corner have comparable scale `B=epsilon`, `q=rho epsilon`.

## 3. Retaining the common leaf-diagonal direction

The criterion (4) minimizes the four endpoint residuals but discards the fact that the same `d` appears in both horizontal completed squares. Keep that common variable.

Put

```text
H_A=a_plus*a_minus/[16A(a_plus+a_minus)].            (13)
```

For

```text
u=T00-T01, v=T10-T11,
```

the two horizontal completed squares obey, for every common `d`,

```text
A a_plus [d-(T00+T10)/(4A)]^2
+A a_minus[d-(T01+T11)/(4A)]^2
 >= H_A (u+v)^2.                                     (14)
```

This is the exact minimum over one common `d`, not two independent minima. Retain also the two vertical endpoint residuals

```text
beta_plus u^2+beta_minus v^2.
```

Since `Delta=u-v`, minimizing the positive quadratic

```text
H_A(u+v)^2+beta_plus u^2+beta_minus v^2
```
under fixed `Delta` yields

```text
C_A Delta^2,
C_A=[H_A(beta_plus+beta_minus)+beta_plus beta_minus]
    /[4H_A+beta_plus+beta_minus].                    (15)
```

The formula follows by a two-by-two inverse or direct completion; its denominator is positive.

### Theorem 3.1: common-diagonal sufficient condition

Every strict connected half-leaf arrow has

```text
-H''(K;D)>0
```

for every nonzero real symmetric physical direction whenever

```text
C_A>J/(32AB).                                        (16)
```

There is a symmetric condition `C_B>J/(32AB)` obtained by retaining the common vertical direction `e` and the two horizontal endpoint residuals. Either condition is sufficient.

### Proof

Apply (2) to all four actual edges. Keep the two horizontal completed squares and the two vertical `kappa` residuals; the other two completed squares and residuals are nonnegative. The marginal block satisfies

```text
4d^2+4e^2+2Jde >= (4-J)(d^2+e^2)>0                 (17)
```

away from `(d,e)=(0,0)`, because every binary rectangle has `0<J<2log2<2<4`. Equations (14)-(15), together with the cell term (3), give

```text
-H''(K;D)
 >= nonnegative retained terms
    +(C_A-J/(32AB)) Delta^2.                         (18)
```

Under (16), the quadratic in `(u,v)` before its fixed-Delta minimization is positive definite after subtracting the cell term. If equality held in (18), (17) would give `d=e=0`, and that two-variable quadratic would give `u=v=0`. The remaining completed edge squares then force the two corner sums on each opposite edge to vanish, hence all four `Tij` vanish. The accepted coordinate map is invertible, so the physical direction is zero. This proves strictness.

Condition (16) is not a relabeling of (4): it uses one completed-square family and the perpendicular endpoint residual family, joined through their shared corner variables.

## 4. A punctured boundary wedge where the old test fails but entropy remains concave

### Theorem 4.1

Fix `a in (0,1)` and `rho>0`. Along (5), for all sufficiently small `epsilon>0`,

```text
K_A+K_B<J/(32AB)<C_A.                                (19)
```

Therefore the accepted parallel-edge sufficient method fails, while the actual complete-event Shannon Hessian is strictly negative in every nonzero physical direction.

More uniformly: for every compact `I subset (0,1)` and compact `R subset (0,infinity)`, there is `epsilon_(I,R)>0` such that (19) holds for every `a in I`, `rho in R`, and `0<epsilon<epsilon_(I,R)` satisfying legality.

### Proof

The first inequality is Theorem 2.1. For the second, (7) gives

```text
a_minus=L+c_a-log rho+o(1),
a_plus =L+c_a-log(rho+1)+o(1).                       (20)
```

Hence (13) has expansion

```text
H_A=L/(32a)
 +[c_a-(log rho+log(rho+1))/2]/(32a)+o(1).           (21)
```

By (9)-(10), `beta_plus->kappa_0(a)` and `beta_minus->infinity`. Formula (15) then gives

```text
C_A=H_A+kappa_0(a)+o(1).                             (22)
```

Combining (12), (21), and (22),

```text
C_A-J/(32AB)
 -> kappa_0(a)+D(rho)/(32a),                         (23)

D(rho)=I(rho)-[log rho+log(rho+1)]/2.
```

The function `log u` is strictly concave, so its integral over the unit interval `[rho,rho+1]` is strictly larger than the trapezoid formed by its endpoint values. Thus `D(rho)>0`, and (23) is strictly positive. All expansions are uniform when `a` and `rho` stay in the stated compact sets, proving the uniform version.

Complementation gives the analogous wedge with `qbar=rho epsilon`; leaf exchange gives the wedges with `A=epsilon` and the other coupling fixed in a compact interior set. The exact singular boundary is not included: at `epsilon=0` some complete atoms vanish and the ordinary interior Hessian formula is no longer the asserted object.

## 5. Exact rational witness and complete-event certificate

Take

```text
A=1/9, B=q=1/10000, qbar=39991/45000,
K=[[1/2,0,1/6],
   [0,1/2,1/200],
   [1/6,1/200,10027/180000]].                       (24)
```

All entries are rational and `A,B,q,qbar>0`. The eight complete events are exactly

```text
p_ij1=tij/4, p_ij0=(1-tij)/4,
```

so they are strictly positive. The Schur complements of `K` and `I-K` are `q` and `qbar`, respectively.

The checker in `code/verify_halfleaf_boundary.py` does not import the PR81 author checker. It independently:

1. constructs every inclusion-minor polynomial on the true line `K+tD`;
2. performs Möbius inversion for all eight complete events;
3. reconstructs `p,p',p''`, full Fisher, and log acceleration;
4. proves exact coefficient equality with the six-coordinate shared-corner quadratic;
5. encloses each logarithm by a fixed 24-term rational atanh series with the displayed tail;
6. evaluates the old and new actual criteria; and
7. proves positive definiteness of the full six-by-six `-H''` matrix by six outward rational Sylvester intervals.

Its retained output gives

```text
K_A+K_B-J/(32AB)
 in [-0.84076354091282164122362505309489821790034,
     -0.84076354091282164122001995334825658460059],

C_A-J/(32AB)
 in [ 0.37431639269638852651851279887776355488888,
      0.37431639269638852652217984470940295671446].
```

The six leading principal minors are enclosed strictly inside

```text
(5.5079,5.5080),
(22.0321,22.0322),
(97.2440,97.2441),
(1.63728e5,1.63729e5),
(7.48331e5,7.48332e5),
(2.11073e9,2.11074e9).
```

Thus (24) is a strict actual obstruction to universal (4), but its full complete-event entropy curvature has the concave sign in every nonzero physical direction. It is not an entropy counterexample.

## 6. Exact scope

Proved here at author level:

- universal strict parallel-edge coverage is false on actual DPP rectangles;
- the common-diagonal criterion (16) and its symmetric counterpart;
- the compact-uniform punctured boundary wedge (19), including actual nonzero-Lambda centers;
- the fixed rational method obstruction and complete-event positive Hessian certificate.

Not proved:

- (16) or its symmetric version for every half-leaf rectangle;
- full concavity for all half-leaf arrows away from the stated wedge and accepted PR81 families;
- any unequal-leaf theorem;
- a genuine positive-Jensen entropy counterexample;
- novelty or formal verification.

Final classification: **DISPROVED** for universal validity of the old sufficient criterion; **PROVED (author), PENDING_REVIEW** for Theorems 3.1 and 4.1; **INCOMPLETE** for general half-leaf and general missing-edge concavity.
