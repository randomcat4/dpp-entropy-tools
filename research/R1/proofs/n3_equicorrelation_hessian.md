# Three-dimensional equicorrelation Hessian and family concavity

## Statement

Let

```text
P_triv=J/3,                  P_std=I-J/3,
K(lambda,mu)=lambda P_std+mu P_triv,
0<lambda,mu<1.
```

Thus `K` is a strict real-symmetric `3 x 3` equicorrelation kernel.  Let
`H(K)` be the Shannon entropy of the complete DPP event distribution obtained
from the inclusion probabilities by Boolean Mobius inversion.

1. The Hessian `D^2 H(K)` is negative semidefinite on the full six-dimensional
   space of real-symmetric directions.  It is negative definite when
   `lambda!=mu`.
2. The restriction `h(lambda,mu)=H(K(lambda,mu))` is globally strictly concave
   on `(0,1)^2`.  In particular, distinct strict equicorrelation kernels have
   strictly negative nontrivial midpoint gap.

The first result is local in arbitrary directions.  It does not prove the
finite-midpoint statement for a chord that starts at an equicorrelation center
and leaves the equicorrelation family.

## Event probabilities and symmetry split

Write

```text
a=(2lambda+mu)/3,              c=(mu-lambda)/3.
```

The complete-event probabilities are constant on subset-size orbits:

```text
p0=(1-lambda)^2(1-mu),
p1=(1-lambda)(2lambda+mu-3lambda mu)/3,   each singleton,
p2=lambda(lambda+2mu-3lambda mu)/3,       each pair,
p3=lambda^2 mu.
```

The `S_3` action splits the real-symmetric direction space as two trivial
copies and two standard copies.  Symmetry makes the trivial-standard Hessian
entries zero and reduces the six-dimensional Hessian to a trivial `2 x 2`
block and two identical standard `2 x 2` blocks.  The exact derivative-table
replay for this reduction is in
`certificate/phase4/scripts/symbolic_s3_identities.py`.

## Standard block

By complete-event complementation, it is enough to treat
`0<mu<=lambda<1`.  Define

```text
R=p1 p2,                       M=p1+p2,
d=a+c=(lambda+2mu)/3,
P=a^2 p1+(1-a)^2 p2,
b=c^2(1-2lambda),

T=log[rho((rho+2)/(2rho+1))^3],
W=log[(2rho+1)^2/(3rho(rho+2))],
rho=[lambda/(1-lambda)]/[mu/(1-mu)]>=1.
```

Here `T,W>=0`.  In the standard basis

```text
D=diag(1,-1,0),
O=[[0,0,-1],[0,0,1],[-1,1,0]],
```

the block is

```text
H_DD=-(2/R)A,             H_DO=-(4c/R)B,
H_OO=-(4/R)C,

A=P+R(aT+W),
B=b+RT,
C=2c^2M+R(dT+W).
```

Thus `A>0`, `C>=0`, and

```text
det B_standard=(8/R^2)Psi,
Psi=AC-2c^2B^2.                                      (1)
```

For fixed `lambda,mu,T`,

```text
partial_W Psi=R(A+C)>0,
```

so `Psi(T,W)>=Psi(T,0)`.  Exact expansion gives

```text
Psi(T,0)=2c^2 q0+R q1 T+R^2 lambda mu T^2,            (2)

q0=PM-c^4(1-2lambda)^2,
q1=Pd+2ac^2M-4c^4(1-2lambda).
```

Put

```text
A0=2lambda+mu-3lambda mu,
B0=lambda+2mu-3lambda mu.
```

Then

```text
q0=lambda(1-lambda)A0B0/9>0.                         (3)
```

For `sigma=mu/lambda`, exact collection gives

```text
q1=lambda^3 F(lambda,sigma)/9,

F=(2sigma+1)^2
  +lambda(sigma^3-14sigma^2-5sigma)
  +lambda^2(-2sigma^3+13sigma^2-2sigma).
```

The derivative of `F` in `lambda` is affine and has endpoint values

```text
F_lambda(0,sigma)=sigma(sigma^2-14sigma-5)<0,
F_lambda(1,sigma)=-3sigma(sigma-3)(sigma-1)<=0.
```

Hence `F` is nonincreasing, while

```text
F(1,sigma)=(1-sigma)^3>=0.
```

Since `lambda<1`, this gives `F>0` and `q1>0`; at `sigma=1` the strict case is
explicitly `F=9(1-lambda)^2`.  Every term in (2) is therefore nonnegative.
The standard block is negative semidefinite, and is negative definite when
`lambda!=mu`.  Complementation covers the other half-domain.

## Trivial block

Let

```text
r0=p0,             r1=3p1,
r2=3p2,            r3=p3.
```

This is the count law of `N=B_lambda+B_lambda+B_mu`, and

```text
H(K)=H(N)+(r1+r2)log 3.                               (4)
```

Let `F` be the Fisher matrix of `(r0,r1,r2,r3)`, and let
`Nmat=-nabla^2 h`.  Define

```text
A=log[(2rho+1)^2/(3rho(rho+2))],
B=log[(rho+2)^2/(3(2rho+1))],
T=B-A.
```

On `rho>=1`, direct differentiation of (4) gives

```text
Nmat_ll=Fll-2(A+mu T),
Nmat_lm=Flm-2(A+lambda T),
Nmat_mm=Fmm.                                           (5)
```

Both diagonal entries of `nabla^2 h` are strictly negative in the interior.
It remains to prove `Phi=det Nmat>=0`.

At fixed `rho`, substitute

```text
mu=lambda/[rho(1-lambda)+lambda].
```

Exact rational simplification of (5) yields

```text
Phi=-2P(lambda)/[lambda rho(lambda-1)(rho+2)(2rho+1)]. (6)
```

The denominator is negative, so `Phi` has the sign of `P`.  Write

```text
P(lambda)=sum_{i=0}^4 binom(4,i)b_i lambda^i(1-lambda)^(4-i).
```

Set

```text
S=2rho^2+5rho+2,
C0=12rho^3+10rho^2+7rho-2,
D0=(rho-1)^2(rho^2+rho+1),
E=rho(-2rho^3+7rho^2+10rho+12).
```

The five Bernstein coefficients obey the exact identities

```text
b0=rho[3A rho^2+6A rho+2(rho-1)^2],

4b1=rho(4rho^2+7rho-2)B
    +rho S A(3-2A)+2(rho^2-1)^2,

6b2=(C0-4rho S A)B+EA+4D0,

4b3=2(rho^2-1)^2+3rho S B-2rho S B^2
    +rho(-2rho^2+7rho+4)A,

b4=rho[(6rho+3)B+2(rho-1)^2].                        (7)
```

The following elementary bounds suffice:

```text
0<=A<=B,                    A<log(4/3)<1/3,            (8)
rho S B^2<=(rho^2-1)^2.                                 (9)
```

For (9), apply

```text
log y<=(y-1)/sqrt(y),       y>=1,
```

to `y=exp(B)=(rho+2)^2/[3(2rho+1)]`.  After squaring, the needed rational
comparison is equivalent to

```text
3(2rho+1)(rho+2)^2(rho+1)^2-rho S(rho-1)^2
=4rho^5+38rho^4+102rho^3+110rho^2+58rho+12>0.
```

Now `b0,b4>=0` immediately.  Equation (8) makes every term in `b1`
nonnegative.  For `b2`,

```text
C0-4rho S A
>=(28rho^3+10rho^2+13rho-6)/3>0.
```

If `E>=0` the remaining terms are nonnegative.  If `E<0`, then

```text
EA+4D0>E/3+4D0,
E+12D0=10rho^4-5rho^3+10rho^2+12>0.
```

For `b3`, (9) handles the quadratic part, while `B>=A` gives

```text
3rho S B+rho(-2rho^2+7rho+4)A
>=rho(4rho^2+22rho+10)A>=0.
```

Thus every `b_i>=0`; for `rho>1` they are strictly positive.  Consequently
`Phi>=0`, strictly off `rho=1`.  Complementation covers `rho<1`.  The trivial
block is negative semidefinite everywhere and negative definite off
`lambda=mu`.

The dependency-free exact replay
`certificate/phase4/scripts/equicorrelation_trivial_symbolic.py` reconstructs
(5)--(7) with rational-function arithmetic over `fractions.Fraction`; it uses
no floating-point sign test or external algebra package.

Combining the trivial block with the two standard copies proves statement 1.

## Strict concavity inside the equicorrelation family

The parameter square is convex and `(lambda,mu)->K(lambda,mu)` is affine.  The
trivial block just proved is the Hessian of the restricted entropy `h`.  It is
negative definite away from `lambda=mu`.  On that diagonal,

```text
nabla^2 h(r,r)
=-1/[3r(1-r)] [[4,2],[2,1]],                          (10)
```

whose only zero direction is `(1,-2)`.

A nonconstant affine chord not contained in the diagonal meets it at most
once, so its second derivative is strictly negative except possibly at one
point.  A chord contained in the diagonal has direction `(u,u)`, and (10)
gives curvature `-3u^2/[r(1-r)]<0`.  Integrating the second derivative with
the positive midpoint kernel proves strict midpoint loss for every nonconstant
chord and establishes statement 2.

## Verification boundary

Two independent nonauthor contexts checked the standard and trivial block
proofs, including the algebra, complement reduction, inequality directions,
strictness, and two-by-two inertia conclusions; both returned `CORRECT`.  Two
independent contexts also returned `CORRECT` for the finite-chord corollary.
The verification reports record the reviewed SHA-256 values.

This result does not settle a general connected `3 x 3` kernel, and does not
settle the frozen arbitrary-direction finite-midpoint claim at an
equicorrelation midpoint.
