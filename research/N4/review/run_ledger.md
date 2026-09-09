# N4 review run ledger

All commands below were run from the isolated review checkout.  No system
packages were installed and no candidate implementation scripts were imported.
Server addresses and private handoff paths are intentionally omitted.

## Source state

- Review checkout HEAD: `fa504ec74e16843fafc395880d7ba99b4c1d2129`.
- Branch: `research/N4-review-20260909`.
- Smoke/Pilot script SHA256 before P2 extension:
  `6a9d022e16bee974c16a0304eb84f0145256d765abecf8fc1d2170a01ead5101`.
- P2 script SHA256:
  `21a6ff639625df418015c035cdf0f009061a36fb417d96407b1d4c9ded8a97a9`.
- Source snapshot limitation: the exact file bytes for the pre-P2
  `6a9d022e16bee974c16a0304eb84f0145256d765abecf8fc1d2170a01ead5101`
  script were not preserved as a separate source file before the P2 extension
  was synced.  The current committed script keeps the same smoke and pilot
  review code paths, but it is not byte-identical to the script hash recorded
  inside `smoke_server.json` and `pilot_json_review_denom10000.json`.

## Strict rational smoke fixture

- Command: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 <N4 venv>/bin/python research/N4/review/rational_dpp_review.py --out research/N4/review/smoke_server.json smoke`
- PID recorded by script: `158760`.
- Exit: `0`.
- Denominators: `K <= 100`, `D <= 23`, `t = 1/100`.
- Result: strict open-domain feasibility, all midpoint and endpoint event
  probabilities positive and summing to one, `K4_support=true`,
  `diamond_support=false`.
- Hessian interval: negative, approximately
  `[-0.297638466406211233936573476951852220635205869477,
    -0.297638466406211233936573476951852220635205869477]`.
- Entropy-gap interval: negative, approximately
  `[-0.0000148820941832225797256808146805803163748877449549,
    -0.0000148820941832225797256808146805803163748877449549]`.

## Pilot JSON review

- Source file hashes:
  - `best_curvature.json` SHA256:
    `837f828693b6b8fc87ede1f8c3d0a66c07850e9469057644623a33306a74dc6c`.
  - `best_mechanism.json` SHA256:
    `f214ee30bcc416b5a86a345c165828d319108c96d36697d018cbd2f3f5b44d8c`.
- Fields used: top-level `K`, `D`, and `radius`.
- Attempt with `max_denominator=1000000`: stopped after exceeding the short
  single-thread review window; no certificate claimed.  No JSON report was
  produced, so there is no script-recorded PID or script exit status.  After
  interrupting the terminal session, the process table showed a review-owned
  `python` process `158898` and parent `bash` process `158897`; both were
  explicitly terminated.  A follow-up `ps -p 158898,158897` check returned no
  process rows.  The effective terminal/session status was interrupted and
  then killed, not a completed certificate run.
- Completed command: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 <N4 venv>/bin/python research/N4/review/rational_dpp_review.py --out research/N4/review/pilot_json_review_denom10000.json review-json --max-denominator 10000 --radius-factor 1/2 <best_curvature.json> <best_mechanism.json>`
- PID recorded by script: `159181`.
- Exit: `0`.
- Selection rule: weakest certified negative Hessian midpoint.
- Selected object: `best_curvature.json`.
- `best_curvature.json`: strict feasible, `K4_support=false`,
  `diamond_support=true`; Hessian interval negative near
  `-0.000377580631928322199983011302593729045631440198817`; entropy gap at
  `t=radius/2` negative near
  `-0.00293053338551692820962739763960547551299727282357`.
- `best_mechanism.json`: strict feasible, `K4_support=true`,
  `diamond_support=false`; Hessian interval negative near
  `-1.18755857448375571048937707514859148423447474081`; entropy gap at
  `t=radius/2` negative near
  `-0.00755984536646245939094916868073145769176168235859`.

These are certificates for the rationalized denominator-10000 objects only.
They are not global theorems and do not certify a positive counterexample.

## P2 benchmark

- Command: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 <N4 venv>/bin/python research/N4/review/rational_dpp_review.py --out research/N4/review/p2_benchmark_server.json p2-benchmark --p2-terms 120`
- PID recorded by script: `159490`.
- Exit: `0`.
- Result: `CORRECT`; both benchmark matrices `L_u` and `L_v` are strictly
  negative definite by rational log intervals.

## Active jobs after review runs

No review-owned Python process was left running.  Existing unrelated search
or notebook processes were not stopped.
