# Assumptions and conventions

- `E={1,...,n}`, with `1 <= r <= n-1` and `s=n-r`.
- `P` is a fixed rank-`r` real orthogonal projection and `Q=I-P`.
- `U` and `V` are fixed real orthonormal frames for `ran(P)` and `ran(Q)`.
- `B` is a fixed real `r x s` matrix and
  `D=U B V^T + V B^T U^T`.
- `tau >= 0` is fixed and `tau ||B||_op < 1` unless an endpoint boundary is
  explicitly discussed.
- `epsilon` tends to zero through `(0,1/2)`.
- Logs are natural; `0 log 0=0` by continuity.
- All asymptotic constants may depend on the fixed finite data
  `(n,r,P,B,tau)`, but not on `epsilon`.

At each fixed `epsilon`, the path `M_epsilon+tD` is affine with fixed center
and direction.  Across the outer family,

```text
M_epsilon=(1-epsilon)P+epsilon Q,
t_epsilon=tau sqrt(epsilon(1-epsilon)),
K_epsilon,+/-=M_epsilon +/- t_epsilon D.
```

Thus the center and sampled half-length vary with `epsilon`; `D` itself does
not.
