# Fixed-ratio double-boundary extension

Status: **PROVED (author proof; PENDING_REVIEW)**. This is a post-checkpoint continuation of `proof.md`. It extends the `B=q` boundary family there to every fixed positive ratio `B/q`; it does not assert a universal half-leaf theorem. No computation or issue73 allocation is used.

## 1. Actual fixed-ratio rectangles

Fix

```text
0<A<1, rho>0,
q=epsilon, B=rho epsilon,
0<epsilon<(1-A)/(1+rho).
```

All notation is that of `proof.md`. Thus the four corners are

```text
t11=epsilon,
t10=(1+rho)epsilon,
t01=A+epsilon,
t00=A+(1+rho)epsilon,
```

and all four edge integrals, Fisher endpoints, `J`, and edge coefficients come from these same four physical corners.

Put

```text
L=log(1/epsilon), ellrho=log(1+rho).
```

As `epsilon -> 0+`, direct expansion of `g=logit` gives

```text
a_minus=L+g(A)+o(1),
a_plus =L+g(A)-ellrho+o(1),
b_minus=ellrho+o(1),
b_plus =rho epsilon f(A)+o(epsilon).                 (1)
```

The rectangle integral satisfies

```text
J/(rho epsilon)
 =L+g(A)+1-[(1+rho)/rho]ellrho+o(1).                 (2)
```

Indeed the interior endpoint displacement contributes `rho epsilon g(A)+o(epsilon)`, while

```text
psi(epsilon)-psi((1+rho)epsilon)
 =rho epsilon L+rho epsilon
  -(1+rho)epsilon ellrho+o(epsilon).
```

## 2. The old parallel criterion fails for every fixed ratio

The two horizontal optimal edge coefficients both tend to `f(A)/8`, hence

```text
K_A -> f(A)/16.                                      (3)
```

The lower shrinking vertical edge obeys

```text
epsilon kappa(epsilon,rho epsilon)
 -> c_rho
 =[1/(1+rho)-(ellrho/rho)^2]
   /[8(1+1/(1+rho)-2ellrho/rho)] >0,                (4)
```

where positivity also follows from the strict positivity of the actual one-edge endpoint matrix. The upper shrinking edge has the finite limit

```text
kappa(A+epsilon,rho epsilon)->kappa0(A),
kappa0(A)=1/[32A(1-A)(1-3A(1-A))].                  (5)
```

Thus the lower vertical coefficient diverges, but its old series/parallel combination with the finite upper edge tends only to `kappa0(A)`. From (2)--(5),

```text
K_A+K_B-J/(32AB)
 =-L/(32A)+O(1) -> -infinity.                        (6)
```

Therefore the accepted PR81 bare parallel sufficient criterion fails on every actual fixed-ratio double-boundary scale, not only on the special ray `B=q`.

## 3. Common-square recovery for every fixed ratio

For the strengthened coefficients from `proof.md`,

```text
c_u->f(A),
c_v=[L+g(A)]/(2A)-ellrho/(4A)+o(1),
K_A_hat->f(A)/16.                                    (7)
```

Let the diverging lower vertical coefficient be `M`, let the upper coefficient tend to `R=kappa0(A)`, and put `c=c_v`. The exact identity

```text
(M+R)/4-(M-R)^2/[4(M+R)+c]
 =R+c/16-(8R+c)^2/[16(4(M+R)+c)]                    (8)
```

shows, since `M` has order `1/epsilon` while `c=O(L)`, that

```text
K_B_hat=kappa0(A)+c_v/16+o(1).                       (9)
```

Combining (2), (7), and (9) gives

```text
K_A_hat+K_B_hat-J/(32AB) -> C(A,rho),                (10)

C(A,rho)=f(A)/16+kappa0(A)
 +{(1+2/rho)log(1+rho)-2}/(64A).                    (11)
```

The last summand is strictly positive. Indeed

```text
log(1+rho)>2rho/(rho+2), rho>0,                      (12)
```

because the difference vanishes at zero and its derivative is

```text
rho^2/[(1+rho)(rho+2)^2]>0.
```

Hence `C(A,rho)>0` for every `0<A<1` and every `rho>0`.

### Theorem 3.1

For every fixed pair `(A,rho)` in `(0,1) x (0,infinity)`, there exists
`epsilon_(A,rho)>0` such that every actual strict half-leaf kernel above with

```text
0<epsilon<epsilon_(A,rho)
```

has strictly negative complete-event Shannon Hessian in all six nonzero real symmetric physical directions by the common-square criterion, while the old parallel criterion fails for all sufficiently small `epsilon`.

This is an analytic continuum result with actual four-corner realizability. It is not a finite sample, a relaxed-scalar argument, or an entropy counterexample.

## 4. Uniformity on compact ratio ranges

The rescaled expressions used above are continuous jointly in `(epsilon,rho)` after adjoining `epsilon=0`, provided `rho` remains in a compact subinterval of `(0,infinity)`. Since `C(A,rho)` is continuous and strictly positive, the convergence in (10) is uniform for

```text
rho_min <= rho <= rho_max,
0<rho_min<rho_max<infinity.
```

Consequently, for each fixed `A,rho_min,rho_max`, one may choose a single positive `epsilon_*` such that the strengthened criterion holds for all ratios in that compact range and all `0<epsilon<epsilon_*`. The old criterion simultaneously fails there after possibly decreasing `epsilon_*`.

No threshold uniform as `A` approaches `0` or `1`, or as `rho` approaches `0` or infinity, is claimed.

## 5. Symmetry images and scope

Leaf exchange gives the analogous result with `A` and `B` interchanged. Full complementation exchanges `q` and `qbar` while preserving the complete Shannon Hessian. Thus the same recovery applies in every fixed-ratio double-boundary sector obtained by:

- shrinking `q` together with either edge parameter;
- shrinking `qbar` together with either edge parameter;
- exchanging the two leaves.

The universal common-square inequality, arbitrary ratio sequences approaching `0` or infinity, the compact interior, unequal leaf diagonals, and general missing-edge concavity remain open.

Final classification: the old bare parallel criterion is **DISPROVED** on every fixed-ratio double-boundary scale; the common-square full-Hessian recovery is **PROVED by the author / PENDING_REVIEW** on a sufficiently small actual continuum for every fixed `A,rho`.
