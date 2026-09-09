# W1 compute plan

Date: 2026-09-09.

## Certificate goals

1. Recompute the full event distribution from the inclusion-exclusion definition and from the determinant event formula for representative symbolic or exact rational cases in PR32.
2. Verify the rank-one formula event by event:
   `p_t(S,T)=a_S c_T-t^2 alpha_S gamma_T`.
3. Verify fixed block marginals and the zero-marginal compensation identity
   `sum_{S,T} R(S,T) log(a_S c_T)=0` symbolically where possible and numerically with high precision where logs appear.
4. For the pending `m x 2` statement, derive and test exact rank-two polynomial structure in `s=t^2`, then search only targeted low-dimensional exact examples that address the claim's strict concavity and degeneracy risks. Any finite example is only a diagnostic unless it is a counterexample.
5. For the related "at most two nonzero coordinate columns" statement, verify only the coordinate-basis Schur conditional reduction. Do not replace it by the weaker and basis-dependent condition `rank(B) <= 2`.

## Fixed compute resources

- Heavy or substantive arithmetic runs only in W1's isolated server directory:
  `/root/i05-seven-fronts-20260909/C1/verification/w1`.
- Python path expected there: `/opt/venv/bin/python`.
- Expected package versions: Python 3.12.3, numpy 2.1.2, mpmath 1.3.0, sympy 1.13.3.
- One process at a time, one numerical thread, at most 8 GiB, no GPU.
- Initial single-job wall limit: 600 seconds.

## Required records

For each substantive compute job, preserve:

- relative command,
- PID when available,
- package versions,
- start/end timestamps,
- exit code,
- scripts,
- complete stdout/stderr.

No server address, port, credential, or private connection detail will be written into public artifacts.

## Planned scripts

1. `w1_rank_one_verify.py`: exact event-level rank-one Schur identity checks, fixed-marginal checks, and selected author-example recomputation.
2. `w1_rank_two_probe.py`: exact or high-precision diagnostics for the stated `m x 2` target, focused on strictness, endpoints, coordinate basis dependence, and cases with rank-one versus rank-two `B`.
3. `w1_round2_check.py`: fixed exact checks for the supplied round2 manuscript: conditional Schur factorization, two-coordinate-column conditional directions, the `2 x 2` Hessian formula, determinant-pencil identity on fixed rational inputs, strictness diagnostics at diagonal/off-diagonal crossings, and the harmful `Q` term sign example.

## Stop conditions

- Stop immediately and report if an exact counterexample to a claimed theorem is found.
- Stop second-round manuscript verification as `INCOMPLETE` if no author artifact is present.
- Do not enlarge random scans; finite diagnostics cannot certify universal concavity.
- Do not continue proof search after a critical proof gap is identified unless the gap can be resolved inside this bounded verification unit.
- For round2, do not perform open-ended counterexample search. Use fixed rational examples and symbolic identities that target the manuscript's named proof obligations.
