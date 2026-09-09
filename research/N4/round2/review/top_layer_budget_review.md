# Non-Author Review: Top-Layer Budget Bound

Status: CORRECT_BOUND_ONLY.

Reviewed source: main-authored `research/N4/round2/top_layer_budget.md` at
commit `629d1fb1030d7d070ae719a0807f974f6a85ec98`, blob
`915f894c28309b340e3112a56ffc5589c5ea8b60`.

Related frozen scope: `research/N4/round2/frozen_theorem_v2.md` at the same
commit, blob `6277e4fe5a9527f7714efacbd6e2a8e22de4b3d4`.

## Verdict

No critical gaps found for the auxiliary bound as stated. For a fixed
`n x r` isometry and maximum-cardinality events `|S|=r`,

```text
p_S = q_S det(A),     q_S = det(U_S)^2,     sum_S q_S = 1
```

by Cauchy-Binet. If `c=H(q)`, the extra entropy from splitting the merged
top event is `c det(A)`.

For `A(s)=A+sV` and `X=A^{-1/2} V A^{-1/2}`,

```text
d'  = d tr X
d'' = d((tr X)^2 - tr(X^2)).
```

The eigenvalue Cauchy-Schwarz inequality gives
`tr(X^2) >= (tr X)^2/r`, hence

```text
c d'' <= ((r-1)/r)c (d')^2/d.
```

The top-event Fisher cost is exactly

```text
sum_S (q_S d')^2/(q_S d) = (d')^2/d,
```

with zero `q_S` terms contributing continuously as zero. Thus no Fisher term is
discarded.

For the four-point rank-three case, `c<=log 4`, so `(2/3)c<1`; the sufficient
top-layer budget cannot fail there. The independently checked five-point frame
has `H(q)>3/2`, so `(2/3)H(q)>1`, giving a concrete reason for the bounded n5
follow-up. This is only a failure of that sufficient budget bound; it is not a
counterexample and does not settle face concavity because the remaining
coarse logarithmic acceleration terms are still unsigned.
