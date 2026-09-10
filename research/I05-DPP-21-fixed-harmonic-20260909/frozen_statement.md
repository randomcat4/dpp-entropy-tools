# Frozen statement — fixed two-harmonic nonzero-parameter unit

Base: `main@9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.

New statements in this file are **PROVED (AUTHOR PROOF), NOT INDEPENDENTLY REVIEWED**.

The whole curvature target on `1/2<=|t|<=3/2` remains **INCOMPLETE**.

## 1. Fixed symbol and exact legality

For `theta in R/Z`, put

```text
c(theta)=1/2+(1/4)cos(4 pi theta),
g(theta)=(1/8)cos(2 pi theta),
f_t=c+t g.
```

Then for every `|t|<=3/2`,

```text
119/512 <= f_t(theta) <= 15/16                    (1.1)
```

for all `theta`. Consequently

```text
min{f_t(theta),1-f_t(theta)}>=1/16.                 (1.2)
```

Every finite Toeplitz compression is therefore a strict Hermitian positive contraction. This is the genuine affine correlation-kernel path.

## 2. Fixed true-rate Jensen theorem

Let `h(f)` denote the complete-configuration Shannon entropy rate per original lattice coordinate, with natural logarithms. Then

```text
h(f_1)-[h(f_{1/2})+h(f_{3/2})]/2 > 1/10000.         (2.1)
```

The three symbols in (2.1) are fixed and do not depend on the conditioning depth or window size.

### Certificate definition

For `r>=0`, define

```text
h_r(t)=H(X_0|X_1,...,X_r)=H_{r+1}(f_t)-H_r(f_t).     (2.2)
```

Let

```text
rho=49/64,
C0=1033420800/1263214441,
e_r=C0 rho^(2r-6),
E_r=(256/15)e_r^2.                                   (2.3)
```

For every `r>=3` and `t in [1/2,3/2]`,

```text
0<=h_r(t)-h(f_t)<=E_r.                               (2.4)
```

At depth `r=18`, the exact program `code/certify_midpoint_rate_gap.py` proves, with directed logarithm enclosures,

```text
lower(h_18(1))-E_18
 -[upper(h_18(1/2))+upper(h_18(3/2))]/2 > 1/10000.   (2.5)
```

Equations (2.4) and (2.5) imply (2.1).

The event probabilities entering `H_18` are all complete DPP probabilities. After scaling each event matrix by `32`, their numerators are exact integers; the program checks exact normalization and separately cross-checks signed determinants against inclusion-minor Mobius inversion through length six.

## 3. Exact Poisson/correlation curvature identity

Let a strict stationary process be represented by its positive normalized one-sided complete-event `g`-function `G_t` on the binary shift. Put

```text
phi=log G,
psi=d_t phi,
xi=d_t^2 phi,
(LA)(x)=sum_a G(ax)A(ax),
nu L=nu,
Pi A=A-nu(A),
R=(I-L)^(-1)Pi,
v=R phi.                                               (3.1)
```

Then

```text
h'(t)=-nu(psi v),                                      (3.2)

h''(t)=-nu(psi^2)+nu((psi^2-xi)v)
       -2nu(psi R(psi v)).                             (3.3)
```

Equivalently, using `R=sum_{n>=0}L^n Pi`,

```text
h''(t)=-nu(psi^2)-nu((xi+psi^2)v)
       -2 sum_{n>=1}nu((psi o shift^n) psi v).         (3.4)
```

The first term is the complete one-step conditional Fisher information. The remaining terms are the conditional acceleration and the full stationary-measure response; none is assigned an unsupported sign.

For the fixed symbol above, finite range and (1.2) make all terms and the correlation series analytic and exponentially summable on the target compact interval. Formula (3.3), however, is an exact reduction rather than a completed sign proof.

## 4. Curvature certificate interface

Let

```text
d_r(t)=h_r(t)-h_{r+1}(t)
      =I(X_0;X_{r+1}|X_1,...,X_r).                    (4.1)
```

The proof gives explicit constants `A0,A1,A2`, independent of `r,t`, such that

```text
|d_r''(t)|
 <=[A2+4(r+1)A1+(4(r+1)^2+4(r+1))A0] e_r^2.          (4.2)
```

Hence `sum_r d_r''` converges uniformly, and a directed finite calculation of `h_R''` together with the closed geometric-polynomial tail from (4.2) is a valid true-rate curvature certificate. Issue #74 freezes one implementation contract.

## 5. Scope not claimed

This file does not prove `h''(t)<0` on the entire target interval. It does not prove that the fixed amplitude `1/4` lies in PR59's existential tube, and it does not reduce that amplitude. It gives no positive Jensen counterexample. It does not cover legal endpoints or lower-regularity symbols. The midpoint theorem (2.1) is one exact nonzero-parameter true-rate chord result, not a curvature theorem.