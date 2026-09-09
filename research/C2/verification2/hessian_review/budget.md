# Hessian scoped review budget

Date: 2026-09-09
Role: fresh non-author verifier for the finite-box all-directions Hessian certificate candidate.

## Frozen read inputs

- `C:/game/gameproject/showa100/math/i05-seven-fronts-20260909/runs/C2/verification2/hessian/inputs.json`
- `C:/game/gameproject/showa100/math/i05-seven-fronts-20260909/runs/C2/verification2/hessian/budget.md`
- `C:/game/gameproject/showa100/math/i05-seven-fronts-20260909/runs/C2/verification2/hessian/scripts/strict_hessian_certificate.py`
- `C:/game/gameproject/showa100/math/i05-seven-fronts-20260909/runs/C2/verification2/hessian/output/**`
- Optional later author method/result files may be read only if needed to identify the exact candidate version under review.

Do not read old acceptance status or prior reviews as evidence for correctness.

## Target

Audit the candidate's finite nonzero coordinate boxes and all real symmetric directions `V`.

The review checks:

- exact interval/rational arithmetic;
- complete `32`-event, six-coordinate Hessian construction;
- logarithm enclosures and error propagation;
- all `A` coordinate boxes and all `V` sign reasoning;
- exact invertibility of any coordinate transform used for boxes or Hessian forms;
- strict positive probabilities and `0<A<I` range on every certified box.

This is not a proof of the full `1/4 I <= A <= 3/4 I` domain.

## Resources

- Local write scope: `C:/game/gameproject/showa100/math/i05-seven-fronts-20260909/runs/C2/verification2/hessian_review/**`
- Remote write scope: assigned `C2/verification2/hessian_review/**`
- Compute: one CPU, no GPU, memory at most 4 GB.
- Thread limits: `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`.
- Maximum extra remote computation time: 10 minutes.

## Stop Conditions

- Stop with `REFUTED` if a checkable box or point satisfies the candidate assumptions but violates the certified Hessian sign claim.
- Stop with `NEEDS_FIX` after the first critical gap in arithmetic, event completeness, box coverage, transform invertibility, positivity, or all-direction sign reasoning.
- Stop with `INCOMPLETE` if the candidate version or required output is unavailable.
- Stop with `ACCEPTED_SCOPED` only if the candidate script and output close the finite-box all-directions goal under the exact stated scope.

## Evidence retention

Record candidate source identity, local/remote run stdout, exit status, environment, owned PID, and any independent audit scripts. Do not publish connection details.
