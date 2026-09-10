# Terminal invalidation: mathematical implementation mismatch

Status: `STOPPED_MATHEMATICAL_IMPLEMENTATION_MISMATCH`.

The raw attempt-3 program output reported
`RIGOROUS_TRIAL_SCHEME_OBSTRUCTION`, but that status is invalid and must not be
used as mathematical evidence.

The PR91 residual is

```text
r1(Q,t) = partial_t(B+Lu)(Q,t) - c1 - v(Q) + (Lv)(Q,t).
```

For its state Hessian at a fixed parameter, the required normalized Taylor
coefficients are therefore

```text
[partial_t(B+Lu)]_(state alpha, t order 0)
  - v_(state alpha)
  + (Lv)_(state alpha, t order 0).
```

The frozen executable instead formed

```text
r1_proxy = (B+Lu) - (v-Lv)
```

and extracted its coefficient of parameter order one.  This computes

```text
partial_t(B+Lu) + partial_t(Lv)
```

and omits the fixed-parameter state Hessian of `-v+Lv`.  Consequently the
reported `e12` point lower bounds and both derived obstruction margins are not
certified.  The error is mathematical, not a final-serialization or launcher
failure.

Per the public issue74 contract, execution stopped at the first mathematical
mismatch.  No repair or rerun is authorized under the existing clock.  The raw
output and logs are retained only as invalidated provenance.  They prove no
curvature sign, no whole-interval result, and no inability of the frozen PR98
trial to satisfy the PR91 gate.

All owned processes are absent after the stop: launcher PID `61900` and Python
PID `26792`.  Any continuation requires a new explicit issue authorization
naming this retained checkpoint and a fresh bounded budget.
