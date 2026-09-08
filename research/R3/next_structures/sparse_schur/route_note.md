# NS-1 sparse Schur route note

Status: DEEP for the path-sparse L-ensemble subroute.  Status remains HOLD
inside this note for generic sparse marginal `K`, generic trees, and
arrowheads with arbitrary weights.  No real concavity counterexample is claimed.

## Read context and boundary

Read before acting:

```text
repo/AGENTS.md
research/R3/problem.md
research/R3/verdict.md
research/R3/reduction/*
research/R3/structure/*
research/R3/next_structures/*
```

The current R3 verdict says the old grouped count reduction is already
verified and that future work should change to a non-repeated-row sparse
Schur/low-treewidth structure.  This route therefore must not be another
block-exchangeable orbit count.

No `C:\canglan\` path was read or searched.  No remote computation was used.

## Candidate NS-1A: path-sparse L-ensemble

Let `L` be a real symmetric tridiagonal positive definite matrix:

```text
L =
[ d_1  e_1              ]
[ e_1  d_2  e_2         ]
[      e_2  d_3  ...    ]
[           ...   ... e ]
[                 e d_n ]
```

with heterogeneous rational entries.  Define the marginal DPP kernel

```text
K = L(I+L)^(-1).
```

Then `K` is real symmetric and satisfies `0<K<I`, because every eigenvalue
`mu>0` of `L` maps to `mu/(1+mu)` for `K`.  The kernel `K` is generally dense;
the sparse structure is in the exact-event `L` representation, not in repeated
rows of `K`.

This is genuinely outside the old block-exchangeable family: a heterogeneous
path has no nontrivial group permutation symmetry, and its exact event weights
depend on the locations and lengths of selected intervals, not only on group
counts.

## Exact event formula

For strict kernels, the previous reduction established

```text
p_K(S) = det(I-K) det L_S = det(L_S) / det(I+L).
```

For path-sparse `L`, the induced principal submatrix `L_S` is block diagonal
after permuting coordinates: its blocks are the maximal contiguous selected
runs

```text
[a_1,b_1], ..., [a_m,b_m].
```

Therefore

```text
det L_S = prod_j kappa(a_j,b_j),
```

where `kappa(a,b)` is the determinant of the tridiagonal interval
`L_{a..b,a..b}`.  These interval determinants obey the Schur/continuant
recurrence

```text
kappa(a,a) = d_a,
kappa(a,b) = d_b kappa(a,b-1) - e_{b-1}^2 kappa(a,b-2)
             for b>a,
```

with `kappa(a,a-1)=1`.  If `L>0`, every interval principal minor is positive.

## Entropy dynamic program

Let

```text
Z_m = sum det L_S
T_m = sum det L_S log(det L_S),
```

where the sums are over subsets of the first `m` path vertices.  Use
`Z_0=1`, `T_0=0`.  For `m>=1`, either vertex `m` is absent, or the last
selected run is `[a,m]` and vertex `a-1` is absent when `a>1`.  Thus

```text
Z_m = Z_{m-1}
      + sum_{a=1}^m Z_{a-2} kappa(a,m),

T_m = T_{m-1}
      + sum_{a=1}^m kappa(a,m) T_{a-2}
      + sum_{a=1}^m Z_{a-2} kappa(a,m) log kappa(a,m),
```

with `Z_{-1}=Z_0=1` and `T_{-1}=T_0=0` under the convention that fixing
vertex `0` absent contributes weight one.  The implementation uses zero-based
prefix lengths, but the recurrence is the same.

At the end,

```text
Z_n = det(I+L),
H(K) = log Z_n - T_n/Z_n.
```

The proof is by unique decomposition of a subset into maximal selected runs
and additivity of `log` over the product of run determinants.

Complexity:

```text
interval determinants: O(n^2) arithmetic
entropy DP:            O(n^2) arithmetic
memory:                O(n^2), or O(n) with streamed interval rows
```

This replaces `2^n` event enumeration by `n(n+1)/2` interval states.  For the
`n=12` smoke test, that is `78` interval determinants instead of `4096` event
atoms.

## Positive-contraction certificate

For rational tridiagonal `L`, use exact leading continuants:

```text
D_1 = d_1,
D_m = d_m D_{m-1} - e_{m-1}^2 D_{m-2}.
```

By Sylvester's criterion for the given coordinate order, `D_m>0` for all
`m=1..n` certifies `L>0`.  Then `K=L(I+L)^(-1)` is automatically a strict real
positive contraction.  This avoids a dense `K` eigenvalue computation.

For a final numerical sign certificate, Decimal logs in the prototype must be
replaced by outward-rounded log intervals.  The algebraic probability weights
are exact rationals in the validation cases.

## Minimal `n<=8` Mobius comparison design

For a validation case with `n<=8`:

1. Choose rational tridiagonal `L` and certify `L>0` by continuants.
2. Build the dense rational marginal kernel `K=L(I+L)^(-1)`.
3. Compute exact atom probabilities from the marginal kernel by direct Mobius
   inversion:

```text
p_K(S)=sum_{T subset S^c} (-1)^|T| det K_{S union T}.
```

4. Independently compute `det(L_S)/det(I+L)` by path run factorization.
5. Require exact rational equality for every event, exact normalization, and
   a high-precision entropy comparison.

The prototype executes this for heterogeneous `n=6` and `n=8` paths.

## Generic sparse-K and tree blockers

Sparse marginal `K` path: the exact event determinant

```text
p_K(S)=(-1)^|S^c| det(K-I_{S^c})
```

keeps the off-diagonal path couplings through selected and unselected vertices.
The continuant recurrence depends on a binary diagonal sequence, but the pair
of previous continuants takes generically distinct rational values for
exponentially many prefixes.  I do not have a finite-state exact entropy DP for
generic sparse `K`.  Status: HOLD.

Generic tree-sparse `L`: `det L_S` still factors over selected connected
components, but the number of possible rooted connected component shapes can
be exponential.  A bounded-treewidth Schur message must remember an effective
boundary Schur complement, not only the boundary occupancy.  I did not prove a
polynomial exact entropy DP for arbitrary heterogeneous trees in one work
unit.  Status: HOLD.

Arrowhead `L`: if leaves are arbitrary, then for selected leaves `T`,

```text
det L_{T union center}
  = (d_0 - sum_{i in T} b_i^2/d_i) prod_{i in T} d_i.
```

Entropy then contains a subset-sum logarithm.  It admits pseudo-polynomial or
count compression only under extra arithmetic collisions or repeated leaf
types, which would partially return to the old count philosophy.  Status:
HOLD for arbitrary weights.

## Chord limitation

The path recursion computes `H(K)` for any `K=L(I+L)^(-1)` with path-sparse
positive `L`.  However DPP entropy concavity is about affine chords in
marginal-kernel space:

```text
K_t=(1-t)K_0+tK_1.
```

If `K_0` and `K_1` come from path-sparse `L_0,L_1`, the midpoint `K_t` usually
does not have path-sparse `L_t=K_t(I-K_t)^(-1)`.  Therefore this route is not
yet a complete `n>=11` chord-gap evaluator.

Possible next steps:

* search for explicit triples `K_0,K_1,K_t` whose three `L` kernels are all
  path sparse;
* combine path endpoints with a certified T2 or other midpoint bound;
* prove a separate recursion for the sparse marginal `K` event matrix.

Until one of these closes, this route is a DEEP entropy-evaluator candidate,
not a counterexample route.

## Denominator of attempts

Candidate branches considered in this work unit:

```text
1. path-sparse L: accepted as DEEP entropy recursion and prototyped.
2. generic sparse marginal K path: HOLD, state explosion blocker.
3. generic tree-sparse L: HOLD, boundary Schur-message blocker.
4. arbitrary arrowhead L: HOLD, subset-sum logarithm blocker.
```

No random search was run.  No finite experiment is used as a general theorem.
