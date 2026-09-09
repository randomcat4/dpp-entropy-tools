# PR43 task D directed flow certificate

Status: `CANDIDATE_EXACT_SELF_CHECKED`

This directory contains an exact rational feasible directed stationary-flow certificate for task D of `CODEX_VERIFICATION_TASKS_v2.md`, using frozen source commit `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78`.

## Frozen input and convention

The fixed matrices are

```text
C = [[1/2,  1/12, 1/15],
     [1/12, 2/5,  1/20],
     [1/15, 1/20, 3/5 ]]

V = [[1, 0],
     [0, 1],
     [1, 1]]
```

The state order is exactly `000,001,010,011,100,101,110,111`.

Bit convention: the state string is `b3b2b1`; the rightmost bit is matrix coordinate 1, the middle bit is coordinate 2, and the leftmost bit is coordinate 3. Thus `001` means coordinate 1 is occupied.

The variables are directed stationary flows `r_xy = mu(x) q_xy` for every ordered pair `x != y`. No reversibility constraint `r_xy = r_yx` is imposed.

The rational system is built as `A r = b`, `r >= 0`, with rows ordered as:

1. `balance:<state>` for all 8 states, encoding outgoing flow minus incoming flow equals zero.
2. `adjoint:<feature>:<state>` for `feature in G11,G12,G22,detG`, encoding
   `sum_{x != y} r_xy (f(x)-f(y)) = mu(y) lambda_f f(y)`,
   with eigenvalues `-1,-1,-1,-2`.

## Machine-readable artifacts

- `instance.json`: exact reconstructed `mu`, `G`, `detG`, variable order, equation order, `A`, and `b`.
- `flow_certificate.json`: exact rational directed flow. It contains all 56 variables and a compact `nonzero_flow` block with 33 positive entries.
- `verify_pr43_flow.py`: portable exact verifier using only the Python standard library.
- `discover_pr43_flow.py`: discovery script using SciPy only to find a numerical LP basis, then SymPy rational arithmetic to emit the exact certificate.
- `verify_local_summary.json`: local exact verifier summary.
- `verify_final_summary.json`: server exact verifier summary.

## Verification result

Exact verification passes:

```json
{
  "outcome": "FEASIBLE_FLOW",
  "ok": true,
  "nonzero_flow_count": 33,
  "negative_count": 0,
  "bad_equation_count": 0,
  "max_abs_residual": "0",
  "mu_sum": "1",
  "variable_count": 56,
  "equation_count": 40
}
```

The exact verifier reconstructs `mu` by inclusion determinants/Mobius inversion and verifies the certificate by rational arithmetic. This proves task D is feasible for the fixed PR43 input under the directed nonreversible adjoint-flow convention.

## Run metadata

Discovery on the C2 server used Python 3.12.3, SymPy 1.14.0, SciPy 1.18.1, and NumPy 2.5.3, with BLAS/OpenMP-style thread variables set to 1. The first LP attempt found a feasible point, and exact rational recovery produced the current certificate.

The final exact verifier-only server job used PID `171148`, exited with code `0`, and finished at `2026-09-09T10:18:42Z`. Private run logs and the recovered PID marker are stored in the assigned private directory `runs/C2/verification3/pr43_flow`.

A duplicate discovery rerun was attempted only to recapture launch metadata and aborted under the strict virtual-memory wrapper before producing a new object. Its private stderr/exit files are retained. The accepted candidate is the earlier emitted exact flow, checked by the final verifier job and again locally with the portable verifier.

## Scope

No task E or F computation was performed. No search enlargement was performed. Because I authored both this certificate and its self-check, this is not an independent acceptance; it is ready for fresh nonauthor review.
