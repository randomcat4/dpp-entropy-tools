ACCEPTED_SCOPED single-box `R12_boundary_mid`, radius `1/2048`, all real symmetric directions in that finite coordinate box only; no 12-center, global spectral-domain, novelty, or Lean/formal-verification claim.

## Scope checked

This supplement is a directed non-author follow-up to `hessian_review/REVIEW.md`, which remains unchanged. I checked only the final bounded target stated in `hessian_scope.md:5-18`: the rational center

```text
A0 = [[41/100, -3/25, 0],
      [-3/25, 17/50, 0],
      [0, 0, 3/4]]
```

with coordinate order `(A11,A22,A33,A12,A13,A23)` and radius `rho=1/2048`. The accepted conclusion is only: for every real symmetric `A` in this six-coordinate box and every nonzero real symmetric direction `V`, the complete configuration Shannon entropy Hessian along the actual affine path `A+tV` is strictly negative. The box is certified inside `0<A<I` by the stated spectral envelope `[509/2048,1539/2048]`, and is explicitly not claimed to lie wholly inside `1/4 I <= A <= 3/4 I` (`hessian_scope.md:16-18`).

## Bound sources and version comparison

The reviewed final source/input identity is:

- `hessian/scripts/strict_hessian_certificate.py`, git blob `e0603c77dc5a2844d0c94a36238f27856882c873`.
- `hessian/inputs.json`, git blob `c71e1e972db823a2d11d1576e2d0257a90bc2c01`.
- Prior version used in my incomplete review: `hessian_review/server_author_snapshot/strict_hessian_certificate.py`, git blob `1d97fc21a6e487747eac7290a79f6c0b93516550`.

The current script differs from `1d97fc21` only in review-relevant control and persistence surfaces, not in the Hessian formula or interval sign test. The unchanged core paths are event polynomial construction at `hessian/scripts/strict_hessian_certificate.py:239-250`, complete interval entropy Hessian assembly at `:439-475`, exact preconditioning multiplication at `:521-537`, and Gershgorin positivity at `:540-546`. The new/changed surfaces are exact optional row serialization at `:631-649`, atomic JSON writing at `:667-669`, `--only-center` filtering and run metadata at `:709-758`, accepted-box checkpoint persistence at `:882-885`, final certificate aggregation at `:908-927`, and CLI flags at `:961-980`. The earlier checkpoint `NameError` is fixed because the checkpoint filename now uses the live `attempts` counter at `:882`.

## Certificate evidence

The author’s official final result is `hessian/RESULT.md:1-12` and its output list is `hessian/RESULT.md:14-20`. The method statement says the accepted server unit is exactly `R12_boundary_mid`, coordinate radius `1/2048`, all real symmetric directions, with no full-domain claim (`hessian/certificate_method.md:5-24`). It also states the sign method: interval `-H(A)`, rationalized square preconditioner `S`, and strict Gershgorin inequalities in all six rows (`hessian/certificate_method.md:64-90`). Persistence and normal final exit are stated at `hessian/certificate_method.md:92-96`.

I inspected the mirrored official final certificate at `hessian/server_output/run_20260909T071241Z_pid169650/certificate.json` and the fetched copy at `hessian_review/author_final_run/certificate.json`. Both report:

- status `ACCEPTED_SCOPED`;
- attempts `1`, centers accepted/requested `1/1`, log terms `96`;
- center `R12_boundary_mid`, radius `1/2048`, coordinates `[41/100,17/50,3/4,-3/25,0,0]`;
- 32 event probability records: 26 positive-support events and six identically zero events `1234,1235,1245,1345,2345,12345`;
- minimum positive event `245`, lower bound `110463061471749/45802848256000000`;
- six Gershgorin rows with `strict_positive_margin_checked_by_fraction=true`; decimal margins `[0.658345462512669788, 0.595696616700131298, 0.484286632217133806, 0.499897654279470915, 0.122914091193169067, 0.319492630422189061]`;
- a `6 x 6` rational preconditioner with nonzero determinant, approximately `0.0280175633849638096`.

The official invocation mirror records exit code `0` and stdout `STATUS ACCEPTED_SCOPED`, `OUTPUT_DIR output/run_20260909T071241Z_pid169650`. I did not include connection details in this report.

Because the official certificate was generated without exact fraction rows in the JSON display, I ran one bounded non-author server replay with the same final script blob `e0603c77dc5a2844d0c94a36238f27856882c873`, same input blob `c71e1e972db823a2d11d1576e2d0257a90bc2c01`, same center/radius plan, `--only-center R12_boundary_mid`, `--max-attempts 1`, and `--write-exact-gershgorin`. This was not a search over centers or radii. The replay is stored under `hessian_review/remote_single_exact_output/`; it used PID `169870`, exit code `0`, stdout `STATUS ACCEPTED_SCOPED`, `OUTPUT_DIR output/run_20260909T071634Z_pid169870`, and elapsed `91.673` seconds.

The replay certificate at `hessian_review/remote_single_exact_output/output/run_20260909T071634Z_pid169870/certificate.json` matches the official run on status, center, radius, attempts, log terms, support counts, minimum probability event/lower bound, all six Gershgorin margin decimals, and the rational preconditioner determinant. Its Gershgorin rows additionally contain exact rational string fields `diagonal_lower`, `offdiagonal_abs_sum`, and `margin`; parsing those fraction strings with unbounded integer precision gives all six `margin > 0` and all six diagonal lower bounds positive. The smallest margin decimal is again `0.122914091193169067`.

The independent center-jet cross-check at `main_output/jet_comparison_server.json` reports `PASS_EXACT_ALL_EVENT_JETS`, 12 centers, 32 events per center, and 10752 exact scalar comparisons. I treat that only as an implementation cross-check for center jets, not as the box sign certificate.

## Verdict

For the single finite box `R12_boundary_mid` with radius `1/2048`, I find no remaining correctness gap in the certificate pipeline checked here. The exact interval Hessian, rational preconditioner, complete 32-event probability ledger, positivity of the 26 nonzero events, six constant-zero events, exact Gershgorin sign comparison, and normal server completion are all present for this one scoped target.

This review does not audit novelty, does not certify the other eleven centers, does not prove the full spectral band `1/4 I <= A <= 3/4 I`, and is not a Lean or other formal proof kernel verification.
