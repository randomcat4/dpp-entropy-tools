# Maximal legal-direction scope and symmetric second-order corollary

Status: **AUTHOR COROLLARY / PENDING INDEPENDENT REVIEW.**

## 1. L-infinity is automatic for a two-sided legal direction at a strict center

Let a measurable symbol `c` satisfy

```text
delta <= c(theta) <= 1-delta
```

a.e. Suppose a measurable real direction `g` has a nonempty two-sided physical legal interval: for some `tau>0`,

```text
0 <= c(theta)+tau g(theta) <= 1,
0 <= c(theta)-tau g(theta) <= 1
```

a.e. Subtracting from the center bounds gives, pointwise a.e.,

```text
|tau g(theta)| <= max(c(theta),1-c(theta)) <= 1-delta.
```

Hence

```text
||g||_infinity <= (1-delta)/tau < infinity.
```

Therefore among measurable directions that actually generate a nonempty two-sided affine legal interval around a strict center, boundedness of `g` is not an extra regularity restriction; it follows from legality itself.

Consequently the PR130 quartic theorem applies to every measurable half-period-odd direction that admits such a two-sided physical interval.

## 2. Symmetric second Peano derivative vanishes

The parity conjugacy gives

```text
h(c+t g)=h(c-t g).
```

The quartic theorem gives

```text
0 <= h(c)-h(c+t g) <= C t^4
```

for small real `t`. Therefore

```text
[h(c+t g)+h(c-t g)-2h(c)]/t^2
 = -2[h(c)-h(c+t g)]/t^2
```

converges to zero. Thus

```text
boxed{
lim_(t->0)
 [h(c+t g)+h(c-t g)-2h(c)]/t^2 = 0.
}
```

This is a true entropy-rate value statement and does not assert existence or continuity of an ordinary second derivative away from the center.

## 3. Fourth-order bounds without a fourth derivative claim

For any odd `k` with `g_hat(k)!=0`, the accepted matching floor and the PR130 upper bound give constants `0<c_k<=C<infinity` such that

```text
c_k <= [h(c)-h(c+t g)]/t^4 <= C
```

for all sufficiently small nonzero `t` (after slightly decreasing `c_k` to absorb the `O(t^6)` term in the lower bound).

Thus the deficit has exact quartic scale but the present theorem does not claim that the quotient has a limit, nor that a fourth derivative exists outside `A_0`.

No computation is used.