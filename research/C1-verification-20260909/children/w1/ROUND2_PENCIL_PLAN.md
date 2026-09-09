# Round2 determinant-pencil supplement plan

Date: 2026-09-09.

## Target

Independently verify the general symbolic identity in proof equation (3.9), not just a fixed rational instance:

```text
det(G - lambda Q)
= (16 r + 4 lambda E - lambda^3 P) / (16 r P).
```

Use symbolic variables `A0,A1,A2`, set `A3=1-A0-A1-A2`, then express:

- `a=A1+A3`
- `b=A2+A3`
- `r=A1*A2-A0*A3`
- `P=A0*A1*A2*A3`
- `E=A0*A3*(A0+A3)+A1*A2*(A1+A2)`

Build `G` and `Q` exactly as in the manuscript and check that the fully simplified difference is zero.

## Resource Bound

- Same W1 isolated compute directory.
- One process, one thread, no GPU.
- Wall limit at most 600 seconds.
- Preserve PID, command, package versions, exit code, stdout/stderr, and script.

## Stop Condition

Stop after this one symbolic identity check. Do not rerun prior fixed examples or start a new scan.
