# U10e boundary_full_atom verdict

STATUS: INCOMPLETE.

The full-atom boundary `c=1-s`, `s->0` was sharpened substantially, but not
proved globally safe.

## What is now clear

- For fixed `0<x<1/2`, only the full atom vanishes:
  `F=x^3 s`.
- Its Fisher contribution is a positive rank-one blow-up:
  `(x/s) w_s w_s^T`.
- Therefore the only possible danger is in the moving tangent directions
  that nearly cancel `jF`, not in the full atom itself.
- A stable Sherman--Morrison Schur formula was derived and used to avoid
  catastrophic `1/s` cancellation.
- Polynomial rates `s=x^p` with sampled `p` send `sigma` to `+infinity`
  (`x sigma -> 1` in the profile).
- The sharp nonuniform scale is `s=exp(-beta/x)`.  On this scale sigma is
  `O(1)` and positive in the frozen high-precision table; the smallest
  sampled near-limit value was approximately `26.58` at `beta≈0.58`.

## What remains open

The missing proof is a closed limiting inequality for the exponential scale:

```text
phi(beta)>0 for every beta>0,
```

plus a uniform remainder bound connecting finite `x` to that limit.  Without
that, this boundary work is a refined SCOUT/BLOCKER, not a theorem.

No negative or趋零 mechanism was found.
