# C3 PR29 compute plan

No computation is needed for the analytic radial theorem beyond line-by-line proof audit.

For the fixed C3-M1 rate certificate, I will run exactly one independent replay/reconstruction pass in the isolated server directory `/root/i05-seven-fronts-20260909/C1/verification/c3`:

1. Copy only the public PR29 `rate/` inputs and scripts needed for C3-M1 into the private compute directory.
2. Record Python and package versions, current time, exact input hashes, process id, command lines, exit status, and elapsed time.
3. Set one-thread environment variables: `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `BLIS_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`.
4. Run the supplied certificate commands with the frozen parameters only:
   - `python scripts/c3_m1_variational_boundary.py --candidate candidate.json --output artifacts/c3_m1_boundary_M64.replay.json --M 64 --bits 160`
   - `python scripts/c3_m1_rate_certificate.py --candidate candidate.json --boundary artifacts/c3_m1_boundary_M64.replay.json --output artifacts/c3_m1_rate_n4.replay.json --n 4`
   - `python scripts/c3_m1_audit.py --candidate candidate.json --true-symbol candidate_true_symbol.json --boundary artifacts/c3_m1_boundary_M64.replay.json --rate artifacts/c3_m1_rate_n4.replay.json --output artifacts/c3_m1_audit_result.replay.json`
5. Run one small reviewer-written exact summary checker against the replay outputs. Its purpose is limited to independently confirm the fixed input set, case counts, determinant counts, boundary margins, gap sign, and equality/containment of stable non-timestamp fields against the public artifacts.
6. Retrieve the replay logs, metadata, reviewer checker, and resulting JSON files into `verification_20260909/children/c3/compute_replay/`.

Resource limits and stop conditions:

- One CPU thread; no GPU.
- Target memory under 8 GiB.
- First job timeout: 600 seconds.
- Stop immediately if an input hash differs unexpectedly, a supplied script exits nonzero, a replay changes a substantive artifact field, a conditional interval is empty or directionally wrong, or the certified upper pair-gap is not strictly negative.
- Do not increase `n`, `M`, precision, or perform random scanning in this review pass.
