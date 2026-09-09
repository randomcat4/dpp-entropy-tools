# Rayleigh beta-zero obstruction

## Status

`INCOMPLETE` for the round 2 frozen beta-zero candidate.

`PROVED_HERE` for the Rayleigh-square jet identities and for the exact
beta-zero optimiser reduction.

`EQUIVALENT_BLOCKER` for any attempt that replaces the beta-zero candidate by
the scalar inequality `det(N) alpha<=1` without adding a new DPP-specific
bound.

## Frozen target

For every connected strict real symmetric three-point DPP kernel `0<K<I`,
with

```text
H = F_pair + d G,
d = det(N),
c(D) = tr(N^-1 D),
alpha = c^T H^-1 c,
beta = v_score^T H^-1 c,
v_score(D) = Lambda'[D]/sqrt(Z),
Z = sum_S 1/p_S,
```

the round 2 candidate is

```text
beta(K)=0  =>  d alpha <= 1.                         (B0)
```

Approximate zeros do not count.  The realisability constraints are the real
square constraints for

```text
K = [[x,a,b],[a,y,c],[b,c,z]],
u = a^2, v = b^2, w = c^2, T = 2abc.
```

Equivalently, with inclusion probabilities

```text
q12 = xy-u, q13 = xz-v, q23 = yz-w,
r = xyz - xw - yv - zu + T,
```

the Cayley/Rayleigh relation is

```text
R := T^2 - 4uvw = 0.
```

## Lemma 1: affine real kernels satisfy the full Rayleigh jet

Let `K(t)=K+tD` be an affine real symmetric path, with edge derivatives
`A=a'`, `B=b'`, `C=c'`.  Then

```text
u' = 2aA,      v' = 2bB,      w' = 2cC,
u'' = 2A^2,    v'' = 2B^2,    w'' = 2C^2,
T' = 2(Abc+aBc+abC),
T'' = 4(ABc+ACb+BCa).
```

Consequently the full polynomial relation has the first and second jets

```text
2TT' - 4(u'vw+uv'w+uvw') = 0,                         (R1)
```

and

```text
2(T')^2 + 2TT''
 - 4(u''vw + uv''w + uvw''
      + 2u'v'w + 2u'w'v + 2uv'w') = 0.                 (R2)
```

These identities are polynomial.  They remain valid on zero-edge strata; no
division by `T,u,v,w` is used.

### Proof

The formulas for `u,v,w,T` are obtained by differentiating
`(a+tA)^2`, `(b+tB)^2`, `(c+tC)^2`, and
`2(a+tA)(b+tB)(c+tC)`.  Since
`T(t)^2-4u(t)v(t)w(t)` is identically zero for a real kernel path, its first
and second derivatives give `(R1)` and `(R2)`.

## Lemma 2: beta zero is an exact tangent condition at the H-optimiser

Let

```text
D_H = H^-1 c / alpha.
```

Then `c(D_H)=1`, `H(D_H,D_H)=1/alpha`, and

```text
beta=0  iff  Lambda'[D_H]=0.                         (BZ)
```

At a beta-zero kernel, the full score and the pair-projected score agree on
the optimiser:

```text
F(D_H,D_H) = F_pair(D_H,D_H).
```

Moreover `(B0)` is equivalent to

```text
H(D_H,D_H) >= d.                                    (H-min)
```

Equivalently,

```text
F_pair(D_H,D_H) >= 2 tr(N adj D_H).                 (pair-at-DH)
```

If `(B0)` is false, then `D_H` is already a trace-normalised full-score
counterexample direction with `Lambda'[D_H]=0`.

### Proof

The constrained minimiser of the positive quadratic form `H` under
`c(D)=1` is `D_H=H^-1c/alpha`; hence `c(D_H)=1` and
`H(D_H,D_H)=1/alpha`.  Since

```text
beta = v_score^T H^-1 c = alpha v_score(D_H),
```

and `alpha>0`, beta vanishes exactly when `v_score(D_H)=0`, equivalently
`Lambda'[D_H]=0`.

When beta is zero, `v_score(D_H)^2=0`, so `F=F_pair+v_score^2` gives
`F(D_H,D_H)=F_pair(D_H,D_H)`.  The inequality `d alpha<=1` is exactly
`1/alpha>=d`, i.e. `(H-min)`.

Finally, for three by three matrices,

```text
2 tr(N adj D) = d(c(D)^2 - G(D,D)).
```

At `c(D_H)=1`, the inequality
`F_pair(D_H,D_H) >= 2 tr(N adj D_H)` is therefore equivalent to
`F_pair(D_H,D_H)+dG(D_H,D_H)>=d`, i.e. `H(D_H,D_H)>=d`.

## Lemma 3: Rayleigh tangency alone cannot exclude beta zero

At a point with all three edges nonzero, the map from affine edge derivatives
`(A,B,C)` to `(u',v',w',T')` has rank three and its image is exactly the
first-order tangent space to `R=T^2-4uvw=0` in the edge variables.

Indeed, `u'=2aA`, `v'=2bB`, `w'=2cC` determine `A,B,C`; substituting them
into the formula for `T'` gives `(R1)`, and every solution of `(R1)` arises
this way.  Therefore the full affine tangent space in
`(x,y,z,u,v,w,T)` has dimension six, as does the original symmetric direction
space.

The equation `Lambda'[D]=0` is one additional homogeneous linear condition on
this tangent space.  Unless this linear functional is identically zero, its
kernel has codimension one.  Thus the Rayleigh first-order square constraint
allows many exact `Lambda'`-tangent affine directions.  The second-order
constraint `(R2)` is also automatic for every affine real direction and does
not add a sign condition on `Lambda'[D]`.

Consequently, a proof of `(B0)` cannot come merely from saying that real
kernels satisfy `T^2=4uvw` and its jets.  It must use the additional fact that
the special direction in `(BZ)` is not arbitrary: it is the `H`-minimising
trace direction satisfying the stationarity system

```text
H(D_H,E) = c(E)/alpha        for every symmetric direction E,
Lambda'[D_H] = 0.
```

This is the exact remaining obligation.

## Explicit score form retained

The triple score is not replaced by `Lambda=0`.  Along any affine real path,

```text
Lambda'[D] = sum_S sigma_S p'_S[D]/p_S,
sigma_S = (-1)^(3-|S|),
```

where the eight configuration probabilities are

```text
p111 = r,
p110 = q12-r,
p101 = q13-r,
p011 = q23-r,
p100 = x-q12-q13+r,
p010 = y-q12-q23+r,
p001 = z-q13-q23+r,
p000 = 1-x-y-z+q12+q13+q23-r.
```

Here `q12=xy-u`, `q13=xz-v`, `q23=yz-w`, and
`r=xyz-xw-yv-zu+T`.  These formulas keep the full Rayleigh square
polynomial.  They do not divide by `T,u,v,w` and are valid on zero-edge
strata as long as the DPP is strict, so all event probabilities in the
denominators are positive.

The main instance's current weak-edge observation that beta appears to stay
strictly positive near diagonal kernels is compatible with this obstruction:
it would be a local `H`-stationarity/alignment fact, not a consequence of the
Rayleigh tangent equations alone.

## Verdict

This unit does not prove `(B0)` and does not produce a beta-zero
counterexample.  It proves a smaller exact reduction:

```text
beta=0 violation
  <=> an H-stationary, trace-normalised, Lambda'-tangent affine direction
      D_H with H(D_H,D_H)<det(N).
```

The precise blocker is the absence of a DPP-specific sign or alignment
consequence from

```text
R=R'=R''=0,
H(D_H,E)=c(E)/alpha,
Lambda'[D_H]=0.
```

Replacing that missing consequence by `det(N) alpha<=1` is an
`EQUIVALENT_BLOCKER`, because it is exactly the frozen beta-zero target.
