INCOMPLETE finite nonzero coordinate-box all-directions Hessian certificate candidate; no frozen author `RESULT.md`/`certificate.json` is available for the intended scope.

## Scope and Bound Version

This review covers the finite-box Hessian certificate candidate under `math/i05-seven-fronts-20260909/runs/C2/verification2/hessian/`. It does not certify the full spectral domain `1/4 I <= A <= 3/4 I`.

Bound current sources:

- `inputs.json`: git blob `c71e1e972db823a2d11d1576e2d0257a90bc2c01`
- `budget.md`: git blob `24e1ced8a7941d96de15562329572ae7e7f35cba`
- `scripts/strict_hessian_certificate.py`: git blob `1d97fc21a6e487747eac7290a79f6c0b93516550`

The input fixes six symmetric coordinates at `inputs.json:4`, the exact `5x3` rational `U` at `inputs.json:5` through `inputs.json:14`, twelve requested centers at `inputs.json:50` through `inputs.json:123`, and the non-claim/finite method framing at `inputs.json:147` through `inputs.json:152`. The candidate budget requires exact interval arithmetic, 32-event Hessian coverage, log enclosures, all-box/all-direction Hessian intervals, and rational sign decisions at `budget.md:31` through `budget.md:37`; it also requires result/certificate outputs at `budget.md:39` through `budget.md:44`.

## Blocking Issue

The candidate is not frozen as an auditable certificate. The author output directories present under `hessian/output/` contain only `run_environment.json`, `center_event_jets.json`, and `attempts.jsonl`; none contains `RESULT.md` or `certificate.json`. The latest author server run I checked, `hessian/output/run_20260909T065952Z_pid168584/`, is no longer running and still contains only those three files. Its `attempts.jsonl` has three accepted attempt summaries, but those lines include only decimal Gershgorin margins and minimum probability summaries, not the exact preconditioner, exact interval matrix, exact Gershgorin rows, or final scoped status needed to verify the certificate.

Because the accepted attempts are not themselves exact certificates, I cannot mark the intended finite-box all-directions claim as accepted. The next author step should freeze either a completed all-requested-centers result or an explicitly partial result with `RESULT.md`, `certificate.json`, source hashes, radius plan hash, run PID/exit/stdout, exact accepted-box data, and exact preconditioner data.

## Code and Math Audit

I did not find a first mathematical flaw in the current script version. The blocking status above is about missing frozen output.

The event polynomial construction appears correct for the six-coordinate symmetric `A`: the script builds `det(A)`, `e2(A)`, `adj(A)`, `D1`, `D2`, singleton/pair/triple probabilities, and the six `|S|>3` zero events at `strict_hessian_certificate.py:239` through `strict_hessian_certificate.py:303`. It also checks the 32 event probabilities sum to 1 as a polynomial at `strict_hessian_certificate.py:300` through `strict_hessian_certificate.py:302`.

The center construction checks every listed rotation is exactly orthogonal before forming `RDR^T`; see `strict_hessian_certificate.py:327` through `strict_hessian_certificate.py:357`. The box-domain guard uses the coordinate-box Frobenius radius `3*rho`, so every accepted box certified by that guard lies inside `0<A<I`; see `strict_hessian_certificate.py:558` through `strict_hessian_certificate.py:576` and the per-attempt use at `strict_hessian_certificate.py:791` through `strict_hessian_certificate.py:805`.

The log enclosure is a rational atanh-series interval with explicit positive tail, range reduction, and monotone interval log extension at `strict_hessian_certificate.py:360` through `strict_hessian_certificate.py:428`. This is acceptable for upper/lower bounding `log p` when `p.lo>0`.

The Hessian formula in `entropy_hessian_iv` uses
`H_ab = -sum p_a p_b/p - sum p_ab log(p)` at `strict_hessian_certificate.py:439` through `strict_hessian_certificate.py:475`. The missing per-event `-p_ab` term is a valid global simplification because all 32 event probabilities are included and their polynomial sum is checked to be exactly 1, so `sum p_ab=0` identically.

The all-directions sign certificate is mathematically sound when the exact certificate fields exist: the script computes an interval enclosure for `-H`, applies a rationalized preconditioner as `S^T(-H)S` at `strict_hessian_certificate.py:521` through `strict_hessian_certificate.py:537`, and checks positive diagonal dominance using rational interval Gershgorin margins at `strict_hessian_certificate.py:540` through `strict_hessian_certificate.py:546`. If those exact margins are all positive, `S^T(-H)S` is positive definite. That also forces the rational `S` to be invertible, since a singular `S` would make `S^T(-H)S` singular.

The current script adds `--radius-plan` at `strict_hessian_certificate.py:687` through `strict_hessian_certificate.py:695` and records it in the run environment at `strict_hessian_certificate.py:719` through `strict_hessian_certificate.py:735`. This changes attempt ordering only; I did not see it alter event construction, interval Hessian construction, or Gershgorin logic.

## Independent Checks Run

I ran the current script in my review directory with `--log-terms 32 --max-attempts 6` as a bounded smoke test. It produced `INCOMPLETE`, accepted `1/12` centers, and wrote a full local certificate for `D_scalar_half` at radius `1/4096`:

```text
STATUS INCOMPLETE
Attempts used: 6/6
Centers accepted: 1/12
Accepted boxes:
- D_scalar_half: radius 1/4096
  min event 245 lower 0.00322596280193742854
  min Gershgorin margin 0.340616330636622333
```

I then parsed that local smoke certificate independently in `hessian_review/check_smoke_certificate.py`. The accepted box has six zero events, strictly positive exact Gershgorin row margins, positive minimum probability, and a nonzero rational determinant for the listed preconditioner `S`. This confirms the certificate format can support the all-directions argument for a single frozen box when the full exact certificate exists.

I also ran the same smoke test on the server inside the assigned `hessian_review` directory. It returned the expected incomplete status because the max-attempt bound was six:

```text
owned_pid=168736
exit_status=2
STATUS INCOMPLETE
OUTPUT_DIR remote_smoke_run/run_20260909T070209Z_pid168736
```

Server environment for that review run: CPython `3.12.3`, Linux `6.8.0-79-generic`, `numpy 2.5.3`, `scipy 1.18.1`, `sympy 1.14.0`, `mpmath 1.3.0`, with all listed thread caps set to `1`.

The main instance's independent center-jet comparison is useful but not sufficient for this review target. The file `verification2/main_output/jet_comparison_server.json` reports `PASS_EXACT_ALL_EVENT_JETS`, `12` centers, `32` events per center, and `10752` exact scalar comparisons. Its own scope says it is an event-derivative implementation check only, not a Hessian sign certificate.

## Verdict

Correctness of the method, conditional on full exact certificate output: no critical flaw found in this bounded audit.

Correctness of the current candidate as a frozen finite-box all-directions certificate: incomplete. The intended author run has no final result file and no exact certificate file, and the available accepted attempt summaries are not enough to check interval matrices, preconditioner invertibility, or exact Gershgorin margins.

Novelty and global significance: not audited.

Formal status: not Lean-checked or kernel-formalized. This is a code/math audit of the interval certificate method plus bounded exact recomputation.
