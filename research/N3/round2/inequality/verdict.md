# Verdict and failure ledger

## Status

`INCOMPLETE`.

This unit does not prove the frozen beta-zero candidate

```text
beta(K)=0 => det(N) alpha(K)<=1.
```

It also does not find a strict beta-zero counterexample.

## New proved material

`PROVED_HERE`: for every affine real symmetric three-point path `K+tD`, the
real square variables

```text
u=a^2, v=b^2, w=c^2, T=2abc
```

satisfy the full polynomial Rayleigh jet

```text
R=T^2-4uvw=0,   R'=0,   R''=0
```

with the explicit first and second derivative formulas recorded in
[`rayleigh_beta_zero_obstruction.md`](rayleigh_beta_zero_obstruction.md).
The proof never divides by `T,u,v,w`, so zero-edge strata are not mishandled.

`PROVED_HERE`: beta zero is exactly the statement that the `H`-minimising
trace direction

```text
D_H=H^-1 c/alpha
```

is tangent to the triple score:

```text
Lambda'[D_H]=0.
```

At beta zero, `(B0)` is equivalent to

```text
H(D_H,D_H)>=det(N),
```

or to the pair-score inequality at that one special direction

```text
F_pair(D_H,D_H) >= 2 tr(N adj D_H).
```

## Failed route

The attempted idea was to use the real Rayleigh square relation and its
affine jets to force beta away from zero, or to force the beta-zero direction
to satisfy a useful sign condition.

This fails at the level of available constraints.  When all three edges are
nonzero, the first-order Rayleigh equation cuts out exactly the ordinary
six-dimensional affine real tangent space.  The condition `Lambda'[D]=0` is
then only one homogeneous linear equation on that space.  Therefore the
Rayleigh tangent equations alone leave a large family of exact
Lambda-tangent affine directions.  The second-order Rayleigh equation is
automatic for affine real paths and supplies no sign by itself.

## Minimal remaining obligation

Any proof of `(B0)` must use the fact that the Lambda-tangent direction is not
arbitrary.  It is the unique `H`-stationary trace direction satisfying

```text
H(D_H,E)=c(E)/alpha  for all symmetric E,
Lambda'[D_H]=0.
```

The missing step is a DPP-specific sign or alignment consequence of this full
stationarity system together with `R=R'=R''=0`.

## EQUIVALENT_BLOCKER

The implication

```text
beta=0 => det(N) alpha<=1
```

itself is the frozen candidate.  Replacing the missing sign/alignment
argument by this inequality is an `EQUIVALENT_BLOCKER`.

The round 1 Sherman-Morrison `SM-close` condition remains an
`EQUIVALENT_BLOCKER` for the full theorem, and the current beta-zero slice is
the exact beta-zero subcase of that issue.
