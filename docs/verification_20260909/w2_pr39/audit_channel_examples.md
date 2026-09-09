# PR39 bounded W2 audit

Head-bound input: PR39
`5558a6b22ef8eb080d198d4af6b1a5cfe2fb164f`.

## Status summary

- NC-channel: ACCEPTED_SCOPED.
- Explicit NC examples/constants: ACCEPTED_SCOPED, conditional on the general
  analytic NC lemma from PR39 sections 3-7.
- General analytic NC lemma: OUT_OF_SCOPE for this unit by instruction; no
  redundant certification is made here.

## NC-channel audit

Accepted scope: for fixed strict two-point Hermitian contractions `A,B` with
nonzero off-diagonal entries and any `0<r<1`, there is no pair of local Markov
matrices `T_A,T_B`, depending only on `A,B,r` and not on `C`, such that

```text
(T_A tensor T_B) P_[A C; C* B] = P_[A rC; rC* B]
```

for every sufficiently small complex `2x2` cross-block `C`. The negative result
does not rule out a channel depending on `C`, a nonlocal channel, or a channel
for one fixed scalar family.

The proof in lines 389-427 is sound. At `C=0`, the output block marginals force
`T_A mu_A=mu_A` and `T_B mu_B=mu_B`. For rank-one `C=epsilon v w*`, the exact
law perturbation

```text
P_K(C)=mu_A tensor mu_B - epsilon^2 u_v tensor v_w
```

has no higher `epsilon` terms because the cross-block determinant contribution
is rank one. For a two-point kernel

```text
A = [[a,z],[conj(z),b]], z != 0,
```

the local law is parametrized by `(a,b,d=ab-|z|^2)`, and the perturbation map

```text
delta a = H_11
delta b = H_22
delta d = b H_11 + a H_22 - 2 Re(conj(z) H_12)
```

is onto the full three-dimensional zero-mass direction space. Since Hermitian
matrices are real spans of rank-one `vv*`, the rank-one directions used in the
proof span the actual local distribution tangent space, not a smaller formal
subspace.

Comparing the `epsilon^2` coefficients forces `T_A` and `T_B` to act as scalar
multiples on those zero-mass spaces, with product `alpha beta=r^2`. Together
with the fixed marginals and mass preservation, every joint law with those
marginals would be transformed as

```text
Q + W -> Q + r^2 W.
```

The final obstruction in lines 430-459 is also correct. Taking
`C=epsilon I_2`, the four-point all-occupied probability has the form

```text
p_t = det(A)det(B) + q t^2 + epsilon^4 t^4.
```

The forced affine rule would give `p_0+r^2(p_1-p_0)`, whereas the target at
`t=r` differs by

```text
epsilon^4 r^2(1-r^2) > 0.
```

For the explicit witness

```text
A=B=[[1/2,1/8],[1/8,1/2]], epsilon=1/16, r=1/2,
```

the full four-point kernel has eigenvalues `5/16,7/16,9/16,11/16` at `t=1`,
and remains strict for all `|t|<=1`. The determinant obstruction is exactly

```text
(1/16)^4 * (1/2)^2 * (1-(1/2)^2) = 3/1048576.
```

This proves the stated impossibility even under the weaker assumption of local
mass-preserving linear maps; Markov positivity is not needed for the
contradiction after the fixed-margin and rank-one constraints are imposed.

## Explicit NC examples and constants

These checks assume the general NC analytic lemma and verify only that the
examples satisfy its hypotheses and constants.

### Even first example

For

```text
c(theta)=1/2 + (1/8)cos(4pi theta)
g(theta)=1024^-1 cos(2pi theta),
```

the hypotheses and constants in lines 337-373 are correct:

- `c(theta+1/2)=c(theta)`, `int c=1/2`, and `c` is nonconstant.
- `g(theta+1/2)=-g(theta)` and `ghat(1)=1/2048`, so
  `gamma=|ghat(1)|^2=2^-22`.
- `||c-1/2||_W=1/8`, hence `a=1/4`.
- `||g||_W=1/1024`, hence `b=1/512`.
- `R=(1-a)/(2b)=192`, `rho=5/8`, and
  `M=log(8/3)-5/8 < 3/8`.
- `8 gamma^2 R^6 = 729/32`, while `54M < 81/4 < 729/32`, so the theorem's
  radius satisfies `T_*>=1`.
- The rate correction on `[-1,1]` is
  `(2/3)gamma^2 t^4 = t^4/(3*2^43)`.
- The Jensen gap for the subchord `t=0,1` at midpoint is
  `7/(3*2^47)`.

The stated value range on `[-1,1]` is correct:

```text
383/1024 <= f_t <= 641/1024.
```

The full legal interval is exactly `[-384,384]`. Writing
`y=cos(2pi theta)`,

```text
f_t = 3/8 + y^2/4 + (t/1024)y.
```

The maximum on `[-1,1]` is `5/8+|t|/1024`, forcing `|t|<=384`; for
`|t|<=384`, the minimum is at the vertex and is at least
`3/8-384^2/1024^2=15/64>0`. Thus the proof correctly distinguishes the full
legal interval from the smaller certified concavity interval `[-1,1]`.

The cross-rank claim is correct. On indices `0,...,2m-1`, sorted by parity, the
cross block from `g` has nonzero entries only on the diagonal and one adjacent
diagonal, both `1/2048`; it is triangular with determinant `(1/2048)^m`, hence
rank `m`.

The line is not a reparameterized radial line through a constant symbol: the
second Fourier harmonic of `c` is independent of `t` and cannot be cancelled by
the first harmonic in `g`.

### Non-even variant

For the variant

```text
g(theta) = [cos(2pi theta)+sin(2pi theta)]/2048,
```

the constants in lines 375-377 are correct:

- `g` is real and non-even, and `ghat(1)=(1+i)/4096` up to the convention's
  conjugate sign, so `gamma=|ghat(1)|^2=2^-23`.
- `2||g||_W=sqrt(2)/1024 < 3/2048`, so the proof may use the upper bound
  `b=3/2048`.
- With `a=1/4`, this gives `R=256`, `rho=5/8`, and `M<3/8`.
- `8 gamma^2 R^6 = 32 > 81/4 > 54M`, hence `T_*>=1`.
- The rate correction is `t^4/(3*2^45)` on `[-1,1]`.
- The conservative range
  `1533/4096 <= f_t <= 2563/4096` follows from
  `|cos x + sin x| <= sqrt(2) < 3/2`.

The proof correctly does not claim the full legal interval for this second
example.

## Boundary of this audit

The NC-channel theorem and the two concrete NC applications pass this bounded
audit. The acceptance of the examples is conditional on the sibling-reviewed
general analytic lemma that produces the finite Jensen theorem and entropy-rate
passage; this file checks the examples' membership, constants, certified
radius, legal interval claims, and cross-rank claim only.
