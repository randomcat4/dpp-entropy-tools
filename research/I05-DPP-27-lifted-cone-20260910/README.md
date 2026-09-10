# PR112: evidence repair and stopping handoff

**The claimed wide certificate on `[49/40,51/40]` is WITHDRAWN_UNSUBSTANTIATED. The old exact companion is RETIRED_KNOWN_FAILING.** This is not a new research line, a replacement interval certificate or an independent review.

Read [RESULT.md](RESULT.md) for the corrected theorem/evidence boundaries, and [sources_and_attempts.md](sources_and_attempts.md) for the complete accessible-artifact inventory, explicit retraction, preserved failure and final handoff.

The production program `interval_certificate.py`, `run01/certificate.json`, original production stdout/stderr, environment/command and claimed independent production checker have not been recovered. They are not included, and no reconstructed historical files or placeholder PASS outputs are supplied. The earlier claims of a successful 66.527318643-second production run, 636 coefficient comparisons, 24 composition checks and rigorous residual bounds are withdrawn. PR98 coefficients are still scouts/trials, not replacement evidence.

S3's separate [narrow analytic verdict](https://github.com/randomcat4/dpp-entropy-tools/pull/112#issuecomment-5618759072) remains limited to `explicit_rate_interval.md`: `h''<-1/2000` on `[1-2^-27,1+2^-27]`. That proof file is unchanged, as are the other theoretical manuscripts and PR91 dependency copies. This repair neither extends nor removes separately recorded mathematical acceptance.

## New diagnostic, not old production

The only new mathematical execution in this repair is a single-case diagnostic for S3's supplied failing input. Source: [evidence_repair/diagnose_retired_checker.py](evidence_repair/diagnose_retired_checker.py). Actual new command, environment and complete stdout/stderr: [evidence_repair/diagnostic_run.json](evidence_repair/diagnostic_run.json).

From this directory, reproduce that diagnostic with:

```sh
python evidence_repair/diagnose_retired_checker.py
```

It compares the old lifted formula, a complete signed determinant, and complete inclusion/Mobius inversion for `t=1/2,n=4,mask=1`. The discrepancy is `3/4096`. Its exit zero means that a KNOWN FAILURE was reproduced; it is not an interval certification or an all-tests pass. The one-line corrected comparison is restricted to that case and does not validate the remaining old checker assertions.

The root `check_exact.py` is intentionally disabled. Its original source and the unsupported interval manuscript remain public at immutable head `2c249eb5ebc11217d7f87b51a0ce8ea51fea21db`, linked in the correction documents. No history was force-rewritten.

## Stop boundary

No new production run, external task, old-budget resumption or independent checker was started. S2 has no reproducible wide-interval target supplied by this PR. S3 can review the correction delta separately. The designated successor owns new exploration. This author's scope ends after publishing and reading back this evidence-retraction handoff.
