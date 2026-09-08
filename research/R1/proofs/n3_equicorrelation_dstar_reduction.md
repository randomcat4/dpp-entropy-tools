# The four-case Fisher target on the equicorrelation family

Status: `EXACT_FAMILY_REDUCTION / TWO_MATRIX_FAMILIES_OPEN`.

This note specializes the sufficient condition `F>=D_*` from the general
`3 x 3` log-odds normal form to compound-symmetric kernels.  It proves the
condition for every direction with `tau<=0`, and for every pure trivial or
pure standard direction.  For mixed directions it reduces the remaining
question to two explicit parameterized `6 x 6` matrix inequalities.  It does
not prove either matrix inequality on the full parameter domain.

## Scalar allocation formula

Let the standard and trivial eigenvalues be `lambda` and `mu`, respectively,
and write

```text
K_ii=a=(2lambda+mu)/3,       K_ij=c=(mu-lambda)/3.
```

Complementation sends `(K,V)` to `(I-K,-V)`.  It preserves `F` and `sigma_e`,
sends `tau` to `S-tau` where `S=sum_e sigma_e`, swaps the absent and present
conditional costs, and maps `beta_e` to `sigma_e-beta_e`.  Hence it preserves
`D_*`, and it is enough to take `0<mu<=lambda<1`.

For this ordering, all absent-conditioned costs equal `A`, all
present-conditioned costs equal `B`, and the already proved one-odds formulas
give

```text
0<=A<B or A=B=0,       A<log(4/3)<1/3,
delta=B-A>=0.
```

For a direction, put

```text
P=sum_e max(sigma_e,0),
N=sum_e min(sigma_e,0),       S=P+N.
```

Specializing the one-dimensional LP dual in the general normal form yields

```text
D_*=max{A(S-tau), AP, AP+delta tau, B tau}.             (1)
```

Equivalently, allocating `sum beta_e=tau` in increasing slope order gives

```text
D_*=A(S-tau),          tau<N,
     AP,               N<=tau<=0,
     AP+delta tau,     0<=tau<=P,
     B tau,            tau>P.                           (2)
```

These identities are exact for arbitrary directions; `P` makes them
piecewise quadratic rather than a single invariant quadratic form.

## Direction and Fisher formulas

Use opposite-edge coordinates

```text
V_ii=h_i,       (r1,r2,r3)=(V_23,V_13,V_12),
U=sum h_i,      Q=sum r_i.
```

Direct differentiation gives

```text
sigma_(opposite i)=2(h_j h_k-r_i^2),
S=2 sum_(i<j) h_i h_j-2 sum_i r_i^2,
tau=a S+4c[sum_(i<j)r_i r_j-sum_i h_i r_i].             (3)
```

The four per-orbit complete-event probabilities are

```text
p0=(1-lambda)^2(1-mu),
p1=(1-lambda)(2lambda+mu-3lambda mu)/3,
p2=lambda(lambda+2mu-3lambda mu)/3,
p3=lambda^2 mu.
```

With

```text
t123=lambda[(a+c)U-2cQ],
t0=(2a-1)U-2cQ-t123,
t_i=(1-a)h_i-aU+2c(Q-r_i)+t123,
t_(opposite i)=a(U-h_i)-2c r_i-t123,
```

the full Fisher quadratic form is

```text
F=t0^2/p0+sum_i t_i^2/p1+sum_i t_(opposite i)^2/p2
  +t123^2/p3.                                           (4)
```

These are complete-event probabilities and their first jets, not inclusion
minors used as event atoms.

## All `tau<=0` directions

For an edge inclusion minor `q_e=det K_e`, concavity of `log det` gives

```text
sigma_e=q_e'' <= (q_e')^2/q_e <= F.                     (5)
```

The last inequality is Fisher data processing after aggregating all complete
atoms containing that edge.  Hence `P<=3F`, and `AP<=F` because `A<1/3`.

Likewise `S-tau=p_empty''`, since the empty-event probability is
`det(I-K)`.  The same log-determinant and Fisher argument gives
`A(S-tau)<=F` when `S-tau>=0`; if it is negative the inequality is immediate.
For `tau<=0`, the last two terms in (1) cannot exceed `AP` or zero.  Therefore

```text
D_*=max{A(S-tau),AP}<=F.                                (6)
```

## Pure isotypic directions

Write

```text
h=m 1+h_perp,       r=n 1+r_perp,
sum h_perp=sum r_perp=0.
```

On the full four-dimensional standard subspace `m=n=0`, not merely on one
representative plane,

```text
S_std=-||h_perp||^2-2||r_perp||^2,
tau_std=-a||h_perp||^2-2(a+c)||r_perp||^2
        -4c<h_perp,r_perp>.
```

After rescaling the second coordinate by `sqrt(2)`, the quadratic form
`-tau_std` has matrix

```text
[[a,sqrt(2)c],[sqrt(2)c,a+c]],
```

whose eigenvalues are `lambda,mu`.  Thus every nonzero pure standard
direction has `S_std<tau_std<0` and is covered by (6).

For a pure trivial direction set its standard and trivial eigenvalue
velocities to

```text
alpha=m-n,       beta=m+2n.
```

Then

```text
S=2alpha^2+4alpha beta,
tau=2mu alpha^2+4lambda alpha beta,
sigma_e=S/3.
```

If `tau<=0`, use (6).  If `tau>0`, division by `alpha^2` shows
`beta/alpha>-mu/(2lambda)>=-1/2`, whence `0<tau<S=P`.  Formula (2) gives

```text
D_*=AS+delta tau=-Lambda.
```

The already proved trivial-sector Hessian inequality is exactly
`F>=-Lambda`, so every pure trivial direction also satisfies `F>=D_*`.

## The two remaining matrix families

Both `F` and `tau` are invariant quadratic forms, so their trivial-standard
cross terms vanish.  In particular

```text
F=F_triv+F_std,       tau=tau_triv+tau_std,
F_std>=0,             tau_std<=0.
```

The branch `B tau` is already controlled.  It is automatic for `tau<=0`; if
`tau>0`, then `tau_triv>0` and the pure-trivial result gives

```text
F>=F_triv>=A S_triv+delta tau_triv
             >=B tau_triv>=B tau.                       (7)
```

It remains only to compare `F` with `AP+delta tau`.  Since

```text
P=max_(J subset {12,13,23}) sum_(e in J) sigma_e,
```

this is equivalent to eight quadratic inequalities

```text
M_J(V):=F-A sum_(e in J)sigma_e-delta tau>=0.            (8)
```

The empty set follows from (7) and the `tau<=0` case.  The full set is the
already proved compound-symmetric entropy Hessian residual.  Permutation
symmetry identifies all subsets having the same cardinality.  Therefore only
the two cases

```text
M_{23}>=0,       M_{23,13}>=0                            (9)
```

remain, as parameterized `6 x 6` quadratic matrices for
`0<mu<=lambda<1`.  Equations (3)--(4) give every entry explicitly, rational in
`lambda,mu` apart from `A` and `delta`.  Proving both matrices positive
semidefinite would establish `F>=D_*` throughout the equicorrelation family;
a negative direction would retire only this sufficient route, not the
already proved entropy theorem.
