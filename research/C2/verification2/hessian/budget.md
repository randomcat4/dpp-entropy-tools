# C2 Hessian verification budget

Status: frozen before computation.

Scope:
- Worker: C2 bounded strict-computation line.
- Local writable area: `C:/game/gameproject/showa100/math/i05-seven-fronts-20260909/runs/C2/verification2/hessian/`.
- Server writable area: `/root/i05-seven-fronts-20260909/C2/verification2/hessian/`.
- Forbidden: `C:/canglan/`, old review files as substitutes for verification, source-proof edits, random spectral sweeps, recursive subagents.

Resource limits:
- At most 2 CPU cores for this worker.
- At most 8 GB RAM for this worker.
- No GPU.
- Environment thread caps: `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`.
- Server wall budget: at most 20 minutes for the strict Hessian computation attempts.
- Certificate attempts: at most 128 total box attempts across all centers.

Inputs:
- Exact `U` and all centers are frozen in `inputs.json`.
- Coordinate order for symmetric `A` and direction `V` is `[a11,a22,a33,a12,a13,a23]`.
- A coordinate box of radius `rho` around a center means every listed coordinate lies in `[center_coordinate-rho, center_coordinate+rho]`.
- A box may cross the target spectral band `1/4 I <= A <= 3/4 I`; in that case the certificate only claims the whole box is inside `0 < A < I` and separately records its certified intersection with the target band.

Attempt policy:
- For each center, try the frozen rational radius schedule from largest to smallest.
- Stop after the first accepted strict box for that center.
- If a point Hessian has a strictly positive direction, save the exact center, a rationalized feasible direction, and a small feasible chord witness, then mark the run `REFUTED`.
- If a center cannot be certified before the attempt budget is exhausted, save the failed radii, minimal event lower-bound intervals, and the sharpest interval eigenvalue/Gershgorin obstruction observed.

Certificate method:
- Floating point may only choose candidate radii, pivots, preconditioners, and display summaries.
- Final sign decisions must use exact rational interval arithmetic.
- Logarithms must be enclosed by a rational atanh-series interval with explicit remainder.
- The Hessian interval must include every `A` in the coordinate box and every real symmetric direction `V`.
- Negative curvature certificates use interval preconditioning followed by strict rational Gershgorin, or an equivalent rational interval LDL check.
- Positive curvature certificates, if found, must give a real feasible chord in `0 < A < I`.

Required outputs:
- `certificate_method.md`
- `inputs.json`
- independent script(s)
- raw output directory with versions, PIDs, exit codes, and logs
- `RESULT.md` whose first line is one of `ACCEPTED_SCOPED`, `NEEDS_FIX`, `REFUTED`, or `INCOMPLETE`

Non-claim:
- A successful finite-box certificate is not a proof over the entire matrix spectral domain.
