# Proof candidate: block-diagonal midpoint and pure cross-block direction

Status before commit-bound review: **PROVED BY AUTHOR, REVIEW PENDING**.

Let `Y_a=Y cap B_a` denote the random subset in block `B_a`.

For either endpoint and every exact block event `S subseteq B_a`, Mobius
inversion inside that block gives

```text
P_K(Y_a=S)
 = sum_{A: S subseteq A subseteq B_a}
     (-1)^(|A|-|S|) det(K_A).
```

Every matrix in this sum is unchanged from `K_0`, because
`V[B_a,B_a]=0`. Hence both endpoints have exactly the same block marginal
laws, and therefore the same block marginal entropies, as `K_0`. This uses
complete event probabilities; no principal minor is identified with an exact
event probability.

At `K_0`, inclusion probabilities factor over blocks because every relevant
principal submatrix is block diagonal:

```text
det((K_0)_(A_1 union ... union A_m))
 = product_a det((K_0)_(A_a)).
```

Finite subset laws are determined from their inclusion tables by Mobius
inversion, so the block random vectors are independent under `K_0`. Thus

```text
H(K_0)=sum_a H(Y_a under K_0).
```

For `sigma` in `{-1,+1}`, entropy subadditivity and the preserved block
marginals give

```text
H(K_0+sigma*tV)
 <= sum_a H(Y_a under K_0+sigma*tV)
  = H(K_0).
```

The inequality is strict. Since `V` is nonzero and all its within-block
restrictions vanish, some `V_ij` is nonzero for `i` and `j` in different
blocks. At either endpoint,

```text
P(i,j in Y)
 = det([[K_ii, sigma*t*V_ij], [sigma*t*V_ij, K_jj]])
 = K_ii*K_jj-t^2*V_ij^2
 < K_ii*K_jj
 = P(i in Y)P(j in Y).
```

Therefore the two containing block variables cannot be independent. The
equality condition in entropy subadditivity yields a strict inequality for
each endpoint, and averaging proves the frozen statement.

The assumptions `t>0` and `V!=0` exclude equality loopholes. Endpoint
feasibility is assumed, not inferred. The argument does not apply to a
non-block-diagonal center or a direction with changing within-block entries.

Exact-rational sanity checks (not used as proof) gave:

| case | block split | cross-pair defect | midpoint gap |
| --- | --- | ---: | ---: |
| n=3 | 2+1 | `-1/2500` | `-2.87086658091e-6` |
| n=4 | 2+2 | `-1/6400` | `-1.01772529604e-6` |

In both cases all complete probabilities summed exactly to one and both block
marginals were exactly preserved.
