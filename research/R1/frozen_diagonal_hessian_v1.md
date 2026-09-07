# Frozen auxiliary theorem D2 v1

Let `n>=1`, let `D=diag(d_1,...,d_n)` with `0<d_i<1`, and let `V` be any
real symmetric matrix. For the full-event finite DPP Shannon entropy

```text
H(K) = -sum_S p_K(S) log p_K(S),
p_K(S) = sum_{A superset S} (-1)^(|A|-|S|) det K_A,
```

the claim is

```text
D^2 H(D)[V,V] = -sum_i V_ii^2/(d_i(1-d_i)) <= 0.
```

In particular, every purely off-diagonal real-symmetric direction has zero
second-order curvature at a diagonal strict-interior kernel. This local zero
does not assert that its finite chord gap vanishes.

The proof must use full event probabilities, cover all bilinear mixed terms,
and justify smoothness from strict interiority.
