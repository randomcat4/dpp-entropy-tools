# PR112 evidence repair and final handoff

Date: 2026-09-10. This is an evidence correction only, not a new research unit. It supersedes all earlier claims in this PR that the wide interval was certified or that its production run and outputs were published.

## 1. Explicit withdrawal, not merely pending review

**WITHDRAWN_UNSUBSTANTIATED:** the claimed theorem `h''(t)<-1/4000` for every `t in [49/40,51/40]`, its negative-interval transfer, and the corresponding quantitative Jensen corollary. This withdrawal does not assert a counterexample or mathematical falsity; it removes the unsupported proof/certificate claim.

I cannot substantiate having actually obtained the claimed production certificate. I have no recoverable production program, original certificate output or execution record to hand over. I therefore withdraw the assertions of a completed successful run rather than characterize this as merely a delayed upload or a certificate awaiting review.

Specifically withdrawn as evidence: the advertised `e02<87/20000`, `e12<611/100000`, `e20<7/10000` global residual bounds and their purported sharper totals; 636 coefficient comparisons; 24 composition checks; the 66.527318643-second/exit-zero production assertion; its stated start/finish times, CPU/memory limits and absence of reruns; the purported certified upper endpoint; and the assertion that the unavailable interval implementation was unaffected by the lifted-label error. A rational combination of unverified residual inputs is not a true-rate certificate.

No missing production script, certificate, independent checker or historical stdout/stderr/environment record has been manufactured during this repair. The old unsupported manuscript remains available in immutable Git history at `2c249eb5ebc11217d7f87b51a0ce8ea51fea21db`. It is withdrawn evidence, not an alternate valid certificate.

## 2. Source reports read

S3's source gate on the exact old head: https://github.com/randomcat4/dpp-entropy-tools/pull/112#issuecomment-5618674720 .

S3's separate narrow analytic verdict: https://github.com/randomcat4/dpp-entropy-tools/pull/112#issuecomment-5618759072 .

The second report says **CORRECT_WITHIN_SCOPE** for `explicit_rate_interval.md` alone: `h''(t)<-1/2000` on `[1-2^-27,1+2^-27]`, using already accepted PR77 inputs. It explicitly does not accept the wide interval, the complete lifted-cone package, or the mixed PR112 head. This repair preserves that file and does not change or extend S3's verdict. Other theoretical units and PR91 dependencies retain their separately recorded review status; no acceptance is inferred from this repair.

## 3. What actually exists, and what does not

The inspected PR112 head has exactly 14 changed files under `research/I05-DPP-27-lifted-cone-20260910/`:

- `RESULT.md`, `check_exact.py`, `entropy_shape.md`, `explicit_rate_interval.md`, `interval_proof.md`, `lifted_cone.md`;
- `dependencies/pr91/{coding_and_fisher.md,curvature_certificate.md,post_handoff_cancellation.md,proof.md}`;
- `input/degree10/{meta.json,u.json,v.json,w.json}`.

Those files were already public. The four degree-10 JSON files are literal trial data, not interval outputs. The original degree-6/8/10 publication and parser/generator remain separately in PR98; no scout is promoted to certificate evidence.

Not present in that frozen tree, and not recovered in this repair: `interval_certificate.py`, `run01/certificate.json`, original production stdout/stderr, original environment/command records, the advertised separate production checker, or `run01/exact_lift.json`. The old README and `sources_and_attempts.md` references also pointed to absent files. The README and this file are NEW repair documents, not recovered historical records.

At the start of this repair, the mounted user-data directory contained only `DPP27_PR91_raw_execution.zip` (55,563 bytes). Its 14 entries are PR91 exact checks, scouts, generator and tightening records; none is a PR112 wide-interval production certificate. The existing connected Drive root was inspected and its relevant DPP27 item is only `DPP27_PR91_full_scout_records_20260910.json` (43,421 bytes). A corrected Drive name search for PR112, interval_certificate and lifted-cone returned no results in the provider search scope. This is a record of the accessible locations inspected, not a claim to have searched inaccessible accounts or every external machine.

An initial Drive filter syntax error was corrected. A direct public-API download from the local container failed at DNS resolution before downloading any source; GitHub connector reads remained available. Neither failure is evidence of a production mathematical run. No permissions were bypassed and no unrelated Drive contents are published.

## 4. Bad exact companion: explicitly retired

The old `check_exact.py` is **RETIRED_KNOWN_FAILING**, not repaired or passing. Its exact original source remains public at:

https://github.com/randomcat4/dpp-entropy-tools/blob/2c249eb5ebc11217d7f87b51a0ce8ea51fea21db/research/I05-DPP-27-lifted-cone-20260910/check_exact.py

Its first homogeneous component used `m/4-c*x/2-a*y/2+ac*(d+2*r-s*m)` with exchanged labels. Direct expansion of `ac*det([[a/2-x,q-z],[q-z,c/2-y]])` requires `1/4-a*x/2-c*y/2+ac*(d+2*r-s)` for mass one. No claim is made that changing this one line validates the remaining moment/witness assertions.

For S3's specified input `t=1/2,n=4,mask=1`, the old recurrence gives `65823/1048576`, whereas the complete signed determinant and independent inclusion/Mobius construction both give `65055/1048576`. The exact discrepancy is `3/4096`. A newly written single-case author diagnostic reproduces this discrepancy and confirms the corrected first component on this case only. The root checker is replaced by a fail-closed retirement notice so it cannot advertise `AUTHOR_EXACT_PASS`.

## 5. New diagnostic evidence, never historical run01

`evidence_repair/diagnose_retired_checker.py` is a NEW source excerpt plus a direct permutation determinant and complete Mobius calculation. `evidence_repair/diagnostic_run.json` records its ACTUAL new command, environment, start/finish, exit status and complete stdout/stderr. It ran only the specified failure case. Exit zero means successful reproduction of a known mismatch, NOT a passing old checker, a repaired general implementation, independent S2 acceptance or a wide-interval certificate.

No PR98 scout was rerun. No production job, new mathematical exploration, server execution or independent review was started. The absent historical files remain absent; there is no placeholder PASS under their old names.

## 6. Handoff and stop

S2 has no reproducible wide-interval production target from this PR, and should not run that claimed certificate based on the withdrawn manuscript. S3 can review this evidence-repair delta without revisiting the unchanged narrow theorem or treating any missing artifact as supplied. The wide interval remains unproved by this submission. New exploration belongs to the designated successor, not this task.

Status after publication: **EVIDENCE_RETRACTION_HANDOFF_COMPLETE / STOPPED** for this author repair. Review acceptance of the repair itself is not claimed. No old compute budget is resumed and no new computation contract is issued.
