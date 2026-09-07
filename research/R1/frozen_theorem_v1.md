# Frozen theorem v1

Proof and search instances must not modify, strengthen, weaken, or reinterpret
these definitions.

Let n be an integer with 3 <= n <= 10. Let K be a real symmetric matrix with
0 < K < I. The DPP on [n] with marginal kernel K has exact event probabilities

```text
p_K(S) = sum_{T superset S} (-1)^(|T|-|S|) det K[T]
       = (-1)^|S^c| det(K - I[S^c]).
```

Let

```text
H(K) = - sum_{S subset [n]} p_K(S) log p_K(S).
```

R1 searches for a strict real chord counterexample:

```text
exists n in {3,...,10}, exists rational real symmetric K0,V and rational t:
    t > 0,
    0 < K0 < I,
    0 < K0 - tV < I,
    0 < K0 + tV < I,
    (H(K0-tV)+H(K0+tV))/2 - H(K0) > 0.
```

All three kernels must be strictly interior. The gap certificate must use the
full event probabilities above. A positive value for
`H(K0) - (H(K0-tV)+H(K0+tV))/2` is evidence for concavity, not a
counterexample.

Permitted finite evidence:

- Floating point Hessian eigenvalues or chord gaps may only nominate
  candidates.
- A counterexample is accepted only after a rational or interval certificate
  proves both strict feasibility and strict positive midpoint gap.
- A no-hit result applies only to the exact recorded finite search range.
