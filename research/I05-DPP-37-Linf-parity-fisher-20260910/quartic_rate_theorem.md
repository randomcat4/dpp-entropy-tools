# Uniform quartic true entropy-rate bound at every strict L-infinity parity center

Status: **AUTHOR PROOF / PENDING INDEPENDENT REVIEW.**

This file strengthens the initial PR130 checkpoint. It proves the missing volume-uniform remainder bound and therefore has priority over the statement in `README.md` that `O(t^4)` for the true rate was still open.

All laws are full complete occupied/vacant DPP laws. The physical path is `K_t=T(c)+tT(g)`.

## 1. Exact s-family from the parity Schur complement

Use the setup of `README.md`. For a finite interval, reorder even/odd sites. At the center each complete-event matrix is

```text
M_(u,v)(0)=diag(A_u,C_v),
```

and the physical odd perturbation is

```text
G=[[0,B],[B*,0]].
```

Complete-event coercivity gives

```text
||A_u^-1||, ||C_v^-1|| <= delta^-1.
```

For `s=t^2`, the exact complete likelihood ratio is

```text
Z_x(s):=p_s(x)/p_0(x)=det(I-s Q_x),
Q_x=C_v^-1 B* A_u^-1 B.
```

Set

```text
C0 = delta^-2 ||g||_infinity^2.
```

Then uniformly in volume and complete word,

```text
||Q_x|| <= C0.
```

The finite Toeplitz cross block also satisfies

```text
||B||_HS^2 <= |Lambda| ||g||_2^2,
```

hence

```text
||Q_x||_HS^2
 <= delta^-4 ||B||_op^2 ||B||_HS^2
 <= delta^-4 |Lambda| ||g||_infinity^2 ||g||_2^2.
tag{1.1}
```

No entrywise Fourier sum occurs.

## 2. Rebase at the physical parameter s

Fix real `s>=0` so small that

```text
s C0 <= 1/4.
tag{2.1}
```

Define

```text
A_(s,x)=Q_x(I-sQ_x)^-1.
tag{2.2}
```

Then

```text
||A_(s,x)|| <= C0/(1-sC0) <= (4/3) C0,
tag{2.3}
```

and

```text
||A_(s,x)||_HS
 <= (1-sC0)^-1 ||Q_x||_HS
 <= (4/3)||Q_x||_HS.
tag{2.4}
```

The elementary resolvent identity gives

```text
I+s A_s = (I-sQ)^-1,
```

so, exactly for every complete word,

```text
p_0(x)/p_s(x)=det(I+sA_(s,x)).
tag{2.5}
```

This is not an approximation and does not alter the physical DPP path.

## 3. The rebased first trace cancels under the full current law

Differentiate the normalized family `sum_x p_u(x)=1` at `u=s`. From

```text
partial_u log p_u(x)|_(u=s)
 = -Tr[Q_x(I-sQ_x)^-1]
 = -Tr A_(s,x),
```

we obtain the exact score identity

```text
boxed{ E_s Tr A_s =0. }
tag{3.1}
```

Here `E_s` is expectation over every occupied/vacant atom under the actual DPP at `t=sqrt(s)`. Thus the cancellation is not a selected-event or reference-law cancellation.

## 4. Forward KL starts at trace length two after rebasing

By (2.3) and (2.1),

```text
s ||A_s|| <= 1/3 <1.
tag{4.1}
```

Therefore the nonnormal operator trace-log series converges absolutely in operator norm:

```text
log det(I+sA_s)
 = sum_(m>=1) (-1)^(m+1) s^m Tr(A_s^m)/m.
tag{4.2}
```

Since

```text
D(P_s||P_0)
 = - E_s log[p_0/p_s],
```

(2.5), (4.2), and the exact score cancellation (3.1) yield

```text
D(P_s||P_0)
 = sum_(m>=2) (-1)^m s^m E_s Tr(A_s^m)/m.
tag{4.3}
```

The complete Fisher and acceleration are not discarded; (4.3) is an equality for the full complete-law KL. It merely reorganizes their net contribution after rebasing.

## 5. Extensive Schatten bound with no spatial absolute expansion

For every matrix `A`, normal or not, and every integer `m>=2`, Hilbert--Schmidt Cauchy--Schwarz gives

```text
|Tr(A^m)|
 = |Tr(A^(m-1) A)|
 <= ||A^(m-1)||_HS ||A||_HS
 <= ||A||_op^(m-2) ||A||_HS^2.
tag{5.1}
```

Combining (1.1), (2.3), and (2.4),

```text
|E_s Tr(A_s^m)|
 <= ((4/3)C0)^(m-2)
    (16/9) delta^-4 |Lambda|
    ||g||_infinity^2 ||g||_2^2.
tag{5.2}
```

Insert this into (4.3). Since `s(4/3)C0<=1/3`,

```text
D(P_s||P_0)/|Lambda|
 <= (16/9) delta^-4 ||g||_infinity^2 ||g||_2^2
    s^2 sum_(m>=2) [((4/3)sC0)^(m-2)/m].
```

Using `1/m<=1/2` for `m>=2`,

```text
sum_(m>=2) r^(m-2)/m <= 1/[2(1-r)] <= 3/4
```

when `r<=1/3`. Therefore

```text
boxed{
 D(P_s||P_0)/|Lambda|
 <= (4/3) delta^-4
    ||g||_infinity^2 ||g||_2^2 s^2.
}
tag{5.3}
```

Equivalently, for

```text
|t|^2 delta^-2 ||g||_infinity^2 <= 1/4,
```

```text
boxed{
 [H_Lambda(c)-H_Lambda(c+t g)]/|Lambda|
 <= (4/3) delta^-4
    ||g||_infinity^2 ||g||_2^2 t^4.
}
tag{5.4}
```

The equality between KL and entropy deficit uses the fixed parity marginals and their independence at the center, exactly as in the accepted parity identity. All complete configurations are retained.

## 6. Thermodynamic limit

For each fixed legal `t`, stationary Shannon entropy rates exist and

```text
h(c)-h(c+t g)
 = lim_(n->infinity) D(P_(n,t)||P_(n,0))/n.
```

The right side of (5.4) is independent of volume. Passing to the limit therefore gives

```text
boxed{
0 <= h(c)-h(c+t g)
 <= (4/3) delta^-4
    ||g||_infinity^2 ||g||_2^2 t^4
}
tag{6.1}
```

through the displayed nonempty symmetric physical interval.

No derivative is passed through the thermodynamic limit. This is a direct value bound at each fixed `t`.

## 7. Exact small-t order

For every nonzero `g in L^infinity`, at least one odd Fourier coefficient `g_hat(k)` is nonzero. The already accepted regularity-free parity matching bound gives

```text
h(c)-h(c+t g)
 >= (1/2) d_Ber(mu^2-|g_hat(k)|^2t^2 || mu^2)
 = |g_hat(k)|^4 t^4/[4 mu^2(1-mu^2)] + O(t^6).
tag{7.1}
```

Together with (6.1), this proves the genuine order statement

```text
boxed{
 h(c)-h(c+t g)=Theta(t^4)
}
tag{7.2}
```

as `t->0` for every strict bounded half-period-even center and every nonzero bounded half-period-odd direction.

In particular a nonzero quadratic entropy-deficit coefficient is impossible in this class, despite the fact that no `C^2` or `C^4` entropy-rate response theorem is asserted outside `A_0`.

## 8. Measurement interpretation

At finite volume the occupation measurement kills the physical first tangent atom by atom: `p_x'(0)=0`. PR125's quantum relative-entropy upper bound remains only `O(t^2)` because the underlying quasi-free quantum state has a generally nonzero first tangent. The present proof quantifies the measurement loss without replacing classical entropy by quantum entropy: it works entirely with the exact measured complete likelihood after the Schur reduction.

The quasi-free paper arXiv:0709.1061 is background for the state/one-particle information-theory correspondence only. No quantum relative-entropy equality is used in (2.5)--(7.2).

## 9. Scope

Author proof, pending independent review:

- true complete-configuration entropy deficit is `O(t^4)` for every strict `L^infinity` parity center/direction;
- combined with the accepted matching floor, its exact small-parameter order is `Theta(t^4)` for every nonzero direction;
- no spatial absolute Fourier summation and no HMM representation are required.

Still open: `C^2/C^4` response outside `A_0`, local curvature/concavity on a punctured neighborhood from value bounds alone, whole-legal-interval concavity, general real kernels, and novelty.