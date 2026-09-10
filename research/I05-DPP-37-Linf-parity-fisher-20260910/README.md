# I05-DPP-37 — strict L-infinity parity center: measured score cancellation and uniform quartic coefficient

Status: **AUTHOR PROOF / PENDING INDEPENDENT REVIEW.**

Base: current accepted main at creation, after scoped dual-review integration of PR117. This successor does not modify PR117 or PR125 and inherits no review verdict from either.

All finite laws below are the full occupied/vacant DPP configuration laws for the physical affine kernel `K_t=T(c)+tT(g)`. No spectral entropy is substituted for Shannon configuration entropy. Fisher and acceleration are retained through exact complete-event identities.

## 1. Setup

Let real `c,g in L^infinity(T)` satisfy

```text
c(theta+1/2)=c(theta),
g(theta+1/2)=-g(theta),
g != 0,
delta <= c <= 1-delta
```

for some `delta>0`. Choose `tau>0` so that `c+t g` remains in `[delta/2,1-delta/2]` for `|t|<=tau`.

For a finite interval `Lambda`, reorder coordinates into even and odd sites. At `t=0`, every complete-event matrix has the block form

```text
M_x(0)=diag(A_u,C_v),
```

where `u,v` are the occupied/vacant words on the two parity blocks. The perturbation has only cross-parity entries,

```text
G = [[0,B],[B*,0]].
```

Complete-event coercivity gives

```text
||A_u^{-1}||, ||C_v^{-1}|| <= delta^{-1}
```

uniformly in volume and in every complete word.

## 2. Every measured first score vanishes pointwise

For every complete word,

```text
p_x(t)=(-1)^|Z_x| det(M_x(0)+tG).
```

Conjugation by `diag(I_even,-I_odd)` sends `t` to `-t` and leaves the complete-event zero-set diagonal unchanged. Therefore

```text
p_x(t)=p_x(-t)
```

for every finite word, not merely after entropy summation. Hence

```text
p_x'(0)=0
```

for every occupied/vacant atom. The complete classical Fisher information in the physical parameter `t` is therefore exactly zero at the center:

```text
I_t,Lambda(0)=sum_x (p_x'(0))^2/p_x(0)=0.
```

This is the precise occupation-measurement score cancellation. It is stronger than saying only that the entropy is even.

## 3. Exact s=t^2 likelihood ratio

Write `s=t^2`. The block determinant identity gives

```text
p_t(u,v)/p_0(u,v)
 = det(I - s Q_(u,v)),
Q_(u,v)=C_v^{-1} B* A_u^{-1} B.
```

The formula is exact for every complete word. It keeps all occupied and vacant events. Since

```text
||Q_(u,v)|| <= delta^{-2} ||B||^2 <= delta^{-2} ||g||_infinity^2,
```

the `s`-likelihood has an event- and volume-uniform analytic disk around zero. No Fourier absolute summation or spatial localization is used.

At the center the two parity complete laws are independent, so expectation under `P_0` is over the product law of `u` and `v`.

Define the `s`-score at zero

```text
S_(u,v) = partial_s log[p_s/p_0]|_(s=0) = -Tr Q_(u,v).
```

Normalization gives

```text
E_0 det(I-sQ)=1
```

for every sufficiently small `s`. Expanding the determinant through second order,

```text
det(I-sQ)
 =1-s Tr Q + (s^2/2)[(Tr Q)^2-Tr(Q^2)] + O(s^3).
```

Comparing coefficients yields the two exact complete-law identities

```text
E_0 Tr Q =0,
E_0 (Tr Q)^2 = E_0 Tr(Q^2).
```

The left side of the second identity is the full Fisher information in the parameter `s` at the center:

```text
I_s,Lambda(0)=E_0 S^2.
```

Thus

```text
I_s,Lambda(0)=E_0 Tr(Q^2).
```

No Fisher term is dropped: this is an equality obtained from normalization of the exact complete likelihood.

## 4. Uniform extensive bound on the quartic coefficient

Although `Q` is not assumed normal, for each word

```text
|Tr(Q^2)| <= ||Q||_HS^2.
```

Using `Q=C_v^{-1} B* A_u^{-1} B`,

```text
||Q||_HS
 <= delta^{-2} ||B||_op ||B||_HS.
```

Hence

```text
I_s,Lambda(0)
 <= delta^{-4} ||B||_op^2 ||B||_HS^2.
```

For the finite Toeplitz cross block, `||B||_op<=||g||_infinity`, while

```text
||B||_HS^2 <= |Lambda| ||g||_2^2
```

(up to the harmless parity-block compression, which only lowers the Hilbert--Schmidt norm). Therefore

```text
boxed{
 I_s,Lambda(0)/|Lambda|
 <= delta^{-4} ||g||_infinity^2 ||g||_2^2.
}
```

Since `D(P_s||P_0)` has zero value and zero first derivative at `s=0`, its second derivative there is exactly `I_s,Lambda(0)`. Equivalently, for every finite volume,

```text
D(P_t||P_0)
 = (t^4/2) I_s,Lambda(0) + o_Lambda(t^4),
```

and the quartic coefficient per original coordinate satisfies the volume-uniform bound

```text
boxed{
 limsup_(t->0) [D(P_t||P_0)/(|Lambda| t^4)]
 <= (1/2) delta^{-4} ||g||_infinity^2 ||g||_2^2.
}
```

The remainder is not claimed uniform in volume.

## 5. Consequence for the possible true entropy-rate order

The fixed parity marginals imply for every finite interval

```text
D(P_(Lambda,t)||P_(Lambda,0))
 = H_Lambda(c)-H_Lambda(c+t g).
```

Thus every finite-window entropy deficit has no quadratic term in `t`, and its quartic coefficient per coordinate is uniformly bounded as above.

This does **not** by itself prove

```text
h(c)-h(c+t g)=O(t^4)
```

for arbitrary strict `L^infinity` symbols, because the `o_Lambda(t^4)` remainder has not been made uniform before the thermodynamic limit. In particular, pointwise score cancellation is not silently interchanged with `Lambda -> infinity`.

The new obstruction is therefore precise:

> If the true entropy-rate deficit has a nonzero quadratic coefficient for some strict `L^infinity` parity path, that coefficient cannot arise from divergence of the finite-volume quartic coefficients. It must arise from non-uniformity of higher-order terms / shrinking parameter control as the volume grows.

Conversely, any proof of an event/volume-uniform bound on the `s`-relative-entropy curvature on a fixed disk would immediately upgrade the result to a true `O(t^4)` entropy-rate bound without any `A_0` assumption.

## 6. Relation to the occupation measurement and quasi-free relative entropy

PR125 uses the occupation measurement only through data processing from the gauge-invariant quasi-free state and obtains an `O(t^2)` upper bound for the true configuration KL density. The present result identifies exactly why that upper bound is not second-order sharp at the parity center: the measured first score vanishes atom by atom, so the complete classical Fisher in `t` is zero even though the underlying quantum tangent is generally nonzero.

The quasi-free reference `arXiv:0709.1061` is used only as background for the density-operator / one-particle correspondence and relative-entropy formulas. No theorem there is promoted to the missing uniform measured fourth-order response.

## 7. Scope and review request

Proved here as an author theorem, pending independent review:

1. pointwise complete-event first-score cancellation at every strict `L^infinity` parity center;
2. exact Schur determinant likelihood in `s=t^2` with an event/volume-uniform operator disk;
3. exact normalization identity `E(Tr Q)^2=E Tr(Q^2)`;
4. an extensive, volume-uniform bound on the finite-volume quartic KL coefficient using only `||g||_infinity` and `||g||_2`;
5. the resulting precise regularity obstruction for any hypothetical nonzero quadratic entropy-rate loss.

Not proved: a uniform `O(t^4)` entropy-rate bound, `C^2/C^4` outside `A_0`, neighborhood concavity outside `A_0`, or existence of a strict `L^infinity` example with nonzero quadratic entropy-rate coefficient. No computation is used.