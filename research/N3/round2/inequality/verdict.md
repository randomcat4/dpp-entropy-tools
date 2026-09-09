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

## Second and final unit

`PROVED_HERE`: on the exact hyperplane `Lambda'[D]=0`, each coordinate split
has a stronger event-Fisher lower bound

```text
F(D,D) >= Q_k^lock(D),
```

where

```text
Q_k^lock
 = D_kk^2/(K_kk(1-K_kk))
   + L_0^2/V_0 + L_1^2/V_1
   + (m_0L_0/V_0 - m_1L_1/V_1)^2/(R_0+R_1).
```

This bound uses the fact that `Lambda=ell_1-ell_0`, so `Lambda'[D]=0` forces
the two conditional odds derivatives to be equal.  It retains actual event
Fisher information and is strictly stronger than the old Qk lower bound when
the locked-odds residual is nonzero.

`INCOMPLETE`: I did not prove the hyperplane sufficient condition

```text
Lambda'[D]=0 => B(D,D)>=0.
```

The remaining non-equivalent obligation is to prove a dominance such as

```text
max_k Q_k^lock(D) >= 2 tr(N adj D)
```

or a kernel-dependent convex combination of the three locked lower bounds.
Without that additional sign/alignment argument, this second unit returns to
the same Fisher-versus-cofactor gap and stops.

The main instance's strict Lambda-tangent certificate against the pure
acceleration shortcut `C<=0` is recorded as a route boundary: pure Rayleigh
acceleration sign is not enough; any closure must use full event Fisher.
