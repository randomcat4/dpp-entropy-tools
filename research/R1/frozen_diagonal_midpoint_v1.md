# Frozen auxiliary theorem D1 v1

Let `n>=1`, let `D=diag(d_1,...,d_n)` with `0<d_i<1`, let `V` be a
nonzero real symmetric matrix, and let `t>0`. Assume

```text
K_- = D-tV,  K_+ = D+tV,  0<K_-,K_+<I.
```

For full-event finite DPP Shannon entropy, with

```text
P_K(X=S) = sum_{A superset S} (-1)^(|A|-|S|) det K_A,
```

the claim is

```text
(H(K_-)+H(K_+))/2 - H(D) < 0.
```

The proof must cover directions with a nonzero diagonal entry and purely
off-diagonal nonzero directions. It must state the equality conditions and may
use principal minors only for valid DPP inclusion events.

This result excludes only chords centered at diagonal kernels. It does not
claim global real-symmetric concavity.
