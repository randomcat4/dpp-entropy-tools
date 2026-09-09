# Compute plan

## Local policy

- Do not run heavy recomputation on Windows.
- Do not install system dependencies.
- Keep all generated scripts, exact inputs, outputs, process records, and failures under this review directory or the assigned server directory.

## Server policy

- Assigned server directory: `[isolated owned execution directory]`.
- Runtime: `/opt/venv/bin/python` 3.12.3 with SymPy 1.13.3, NumPy 2.1.2, mpmath 1.3.0.
- Environment: one numerical thread, at most 8 GiB intended working set, no GPU, each fixed check under 600 seconds.
- Before starting work, inspect only this assigned process/directory state to avoid duplicate jobs.

## Exact checks

1. Rebuild complete-event probabilities from
   `p_K(S)=(-1)^{n-|S|} det(K-E_{S^c})`.
2. For symbolic generic `3 x 3` symmetric `K` and a structured rank-two indefinite `D` with null vector `n`, verify the eight-atom four-cycle coefficient formula by comparing inclusion moments and direct event coefficients.
3. For the rational fixture, exactly verify:
   - `rank(B)=2`, left/right null vectors, all entries nonzero;
   - `M0=B^T B` and characteristic polynomial `x(x^2-246x+162)`;
   - `0<A<I` and `0<C<I`;
   - `M_empty=-5M0/3`, `M_full=5M0/2`, and the six middle `M_S` are indefinite rank two;
   - the stated legal radius formula.
4. For `t=1/100` and `t=1/50`, exactly verify all 64 event probabilities are positive and compute high-precision entropy curvature only as a diagnostic.
5. Independently verify the rank-two exterior likelihood ratio and KL compression by direct summation over all finite fibers for the fixture.

## Stopping conditions

- If an exact algebraic identity fails, stop and report the smallest failing claim with saved input/output.
- If a server check is expected to exceed 60 minutes, do not start it; instead save the exact algorithm, input, error bound, and stopping condition for a compute-lane handoff.
- No random enlargement or new theorem search is part of this task.
