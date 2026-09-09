# C3-M1 n4 non-author numeric certificate audit

STATUS: CORRECT_SCOPED

This audit covers the single fixed chord `C3-M1` and its `n=4` true entropy-rate negative certificate under the already accepted S1-style conditioning/extreme-past certificate method. It does not certify the full Lyons-Steif conjecture, novelty, or any positive counterexample.

The reviewed source artifacts are the files in the child `rate/` directory with the hashes recorded below. I used the author self-audit JSON as an input artifact only; it is not the basis of this verdict.

## Verdict

No critical gap found for the scoped negative certificate.

The exact rational gate recomputes as

```text
lower =
-21736338200350506195187245238231755852533113
/22835963083295358096932575511191922182123945984
= -0.0009518467918811257

upper =
-299855012916397501897282364769067397783
/356811923176489970264571492362373784095686656
= -0.0000008403727382396920
```

The strict exclusion gate is the upper endpoint

```text
(U_- + U_+)/2 - L_0 < 0,
```

and the recomputed upper fraction is strictly negative. This certifies that this fixed chord is not a positive entropy-rate counterexample.

## Mathematical Assumptions Used

I treated the following as the scoped certificate theorem/interface being audited for this instance:

- finite DPP atom probabilities are computed from exact event determinants;
- the stationary entropy-rate bounds use the S1/Lyons-Steif conditioning and extreme-past method;
- finite-bandwidth all-one/all-zero boundary kernels are certified by the residual identity `A_X-C_infty=R^*T^{-1}R`;
- the operator error is converted into conditional-probability intervals using the stated spectral margin;
- the positive and negative gates use the interval directions stated in the task.

The long-tail residual discussion in `rate_analysis.md` is auxiliary for possible later long-range symbols. The `C3-M1` certificate is degree two and uses finite-bandwidth residual coverage, so it does not depend on the long-tail example or any volume-uniform long-range tail claim.

## Independent Checks Performed

I wrote and ran `c3_m1_numeric_audit.py` in the review directory. It uses exact rational complex arithmetic and permutation determinants for the small `n+1=5` event kernels, deliberately avoiding the author's complex Bareiss routine.

The independent script checked:

- `candidate.json` has `tau=step=1/4`, while the spectral margin is separately `uniform_margin=1/200`;
- the margin proof is exact: each harmonic amplitude is bounded by `153/2500`, total oscillation square by `153/625`, and `153/625 < (99/200)^2`;
- all six boundary cases are present: three `t` values times `{f,1-f}`;
- the saved variational residuals, residual norm bounds, operator-error rationals, and leading corners recompute exactly from the saved dyadic `X`;
- residual rows after the recorded `M+m=66` rows are exactly zero for sampled rows beyond the record, as expected for degree `m=2`;
- all six boundary deltas are below `1/200`, with worst delta about `9.463653280093224e-08`;
- for each of `t=-1/4,0,1/4`, three exact event distributions are positive and exactly normalized, giving `288` independently recomputed atom determinants total;
- the stored conditional-error formula, conditional range, and weighted extreme width checks match/contain the independent rational recomputation;
- the final pair-gap fractions match the rate artifact and the strict negative upper endpoint is the correct exclusion direction.

The script output status was:

```text
{"elapsed_seconds": 1.1681288667023182, "status": "CORRECT_SCOPED"}
SCRIPT_EXIT_CODE=0
```

## Symbol Convention Note

The original child `rate_analysis.md` and `candidate.json` text describe the script input as producing a conjugate-transpose Toeplitz kernel whose law is unchanged. The law-invariance statement is true for an actual whole-kernel conjugation, because principal event determinants are unchanged.

For this specific artifact, however, the actual arrays do something simpler. The true convention is

```text
c_k = (a_k + i b_k)/2,
```

while the scripts use

```text
c_k = (a_k - i b_k)/2.
```

Since `candidate.json` stores `b_script=-b_true` and `db_script=-db_true`, the script's coefficients equal the true coefficients for all three `t` values. The computation therefore uses the same kernel, not merely a conjugate-law-equivalent one. This is a non-critical wording correction; the numerical input/output and verdict are unaffected. The parent later reported that the main copied version has been edited to state this correctly.

## Non-Independent Rerun

For reproducibility only, I also reran the author's three scripts once inside a server-side review snapshot. This is not an independent implementation. The rerun matched the original boundary cases, rate case intervals, classification, and exact gap enclosure. The rerun self-audit returned `CORRECT_SELF_AUDIT`.

Logged rerun output included:

```text
boundary pid 164966, actual_cases=6
rate pid 164968, actual_determinants=288, classification=NEGATIVE_PAIR_GAP
rerun self-audit status=CORRECT_SELF_AUDIT
overall rerun command exit status=0
```

The independent audit script did not print its process PID; its wrapper log records `SCRIPT_EXIT_CODE=0`.

## File Hashes Reviewed

```text
candidate_true_symbol.json
f503d7bfa1e30a5ea30f7fdff2b91474acc158c99cf244c4f8babaaf1307a6a6

candidate.json
969ea3cdf2c0f2970e17ff4eb915eba2b209114ace5085a7d5f907e504d6f3fa

scripts/c3_m1_variational_boundary.py
c1acb8deb382e35f26fd08209c2858d32d8202a3ac33238a12f659326c3bbaed

scripts/c3_m1_rate_certificate.py
946dc35b6311d6bbab7500d1172939b0f1ff6d06a26f728e2089686b4489299e

scripts/c3_m1_audit.py
95c1e32d3bdcbf97be9be74b54780ef2e3a59d0a12876ec558273ff4dc18a27d

artifacts/c3_m1_boundary_M64.json
3c98ce058bd10e0dcebe7e5cd8a6f095e8fc58e2745b802bbb54f7014fe0b616

artifacts/c3_m1_rate_n4.json
e0b09e9265f991b758026fdd4f50dd48a56ac7bb199d92844b2ff0ad7911dc9a

artifacts/c3_m1_audit_result.json
09763f4d71b8aad15a4594acb87b407f7aac2a1cc996d164441256cdc51b4224
```

## New Review Files

```text
c3_m1_numeric_audit.py
c3_m1_numeric_audit.json
c3_m1_numeric_audit.log
c3_m1_author_rerun_summary.json
c3_m1_author_rerun.log
c3_m1_numeric_certificate_review.md
```
