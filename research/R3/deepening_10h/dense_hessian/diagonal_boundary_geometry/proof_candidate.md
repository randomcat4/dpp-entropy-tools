# D10-U6/S10 proof candidate: diagonal kernels are angularly generic boundary points

## 1. Statement

Fix `n>=2`.  The set `N_n` of strict kernels whose full observation-coordinate
entropy Hessian is negative definite is open in `Omega_n`.

Every strict diagonal kernel `X=diag(x)` belongs to the relative boundary of
`N_n` in `Omega_n`.  More precisely, on the unit sphere

```text
S_0={A in Sym(n): diag A=0, ||A||_F=1},
```

the set

```text
G={A in S_0: A_ij != 0 for every i<j}
```

is open, dense, and has full spherical measure.  For every `A in G` there is
`epsilon_0(X,A)>0` such that

```text
X+epsilon A in N_n whenever 0<|epsilon|<epsilon_0(X,A).
```

There is also a uniform positive-measure version.  Fix a compact diagonal box
`x_i in [a,b] subset (0,1)` and choose

```text
0 < eta < 1/sqrt(n(n-1)).
```

Let

```text
G_eta={A in S_0: min_{i<j}|A_ij| >= eta}.
```

Then `G_eta` is nonempty, compact, and has positive spherical measure, and
there is one `epsilon_0(a,b,n,eta)>0` such that for every box diagonal X,
every `A in G_eta`, and every `0<|epsilon|<epsilon_0`, one has
`X+epsilon A in N_n`.

Consequently every sufficiently small ball about every box diagonal X meets
`N_n` in a nonempty open set of positive ambient Lebesgue measure.  None of
these statements asserts that `N_n` is dense in all of `Omega_n`.

## 2. Openness of `N_n`

On the strict domain every exact event probability is positive and analytic in
the entries of K.  Hence the entropy Hessian matrix in any fixed linear basis
of `Sym(n)` is continuous.  The cone of negative-definite matrices is open, so
its inverse image `N_n` is open.

## 3. Generic directions

Each condition `A_ij=0` cuts `S_0` by a coordinate great subsphere.  The finite
union of these subspheres is closed, has empty interior, and has spherical
measure zero.  Its complement G is therefore open, dense, and full measure.

The verified U3/S9 theorem applies to every `A in G` and gives the stated
punctured radial interval in `N_n`.

At X itself the U2 Hessian formula has every zero-diagonal direction in its
kernel, so X is not in `N_n`.  Yet each neighborhood of X contains
`X+epsilon A in N_n` for any fixed `A in G` and sufficiently small nonzero
epsilon.  Thus X is in the closure of `N_n` and in its complement, hence in
the relative boundary of `N_n` inside `Omega_n`.

## 4. Uniform conical sector and positive measure

In the Frobenius convention a zero-diagonal symmetric matrix with all edge
magnitudes `1/sqrt(n(n-1))` has norm one.  Thus the strict inequality imposed
on eta makes `G_eta` nonempty; taking a sufficiently small open perturbation of
that equal-magnitude point inside `S_0` shows it has positive spherical
measure.  It is closed in the compact sphere and therefore compact.

The compact-uniform clause of U3/S9 applies jointly to the compact diagonal
box and `G_eta`, yielding one positive radial threshold.  For a fixed X, the
map `(r,A) -> X+rA` sends an open angular sub-sector with
`0<r<epsilon_0` into `N_n`.  Since `N_n` itself is open in `Sym(n)`, this
intersection contains an ambient open set and therefore has positive ambient
Lebesgue measure.  Choosing r below any prescribed ball radius proves the
local assertion.

The conclusion is deliberately local at the diagonal stratum.  It neither
classifies sparse angular directions nor controls kernels far from that
stratum.
