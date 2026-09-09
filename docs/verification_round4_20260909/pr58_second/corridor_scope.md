# PR58 Corridor Finite-Certificate Second Scope

Role: bounded independent SECOND follow-up for the original PR58 finite certificate.

The computation-owner packet reviewed here is `corridor_input/`, bound by `corridor_input_binding.json` at public head `e557d93e864582c9f9e7bd4384ed21d6ae2f66e2`. Its executable head is `86617882b7db97f5db39bf613d876a5d5bcf9107`, and its author source head is `1770ed29e8487b8f39aebb4c9466406c7493e580`.

## Inputs Used

Only these materials were used:

1. `corridor_input_binding.json`.
2. The 25 files under `corridor_input/`.
3. `input/RESULT.md`, only for the original (5.1) decimal-display wording.
4. `decimal_display_patch.diff`.
5. Earlier reports in this same directory only as my own preserved scope boundary; their conclusions are not overwritten.

I did not read FIRST material, PR comments, C1 or other reviewer folders, joint-additive files, s9/s10 or PR76 material, private material, or forbidden private-path content. I did not execute Python, SymPy, the independent checker, the author checker, or any new arithmetic computation.

## Accepted Review Scope

This follow-up statically audits whether the independent computation-owner packet contains a complete finite exact certificate for the original PR58 fixed `3+3` fixture:

1. The 64 complete-event construction from the displayed rational matrices in `RESULT.md`.
2. Direct complete-event determinant polynomials and posthoc resolvent extraction of `a,b`.
3. Product-law normalization, global `E a=E b=0`, and all left/right fiber cancellations.
4. All principal and complementary Mobius identities needed to turn positive complete atoms into strict legality.
5. Exact quadratic extrema of `q_s=1-sa+s^2b` on `[3,9]`, `[8,12]`, `[11,14]`, `[14,15]`.
6. Strict positive `q_-` and strict squared compensation margins on all four intervals, covering `[3,15]`.
7. The 27 required exact rational comparisons with the frozen author output: `Amax`, `Bmax`, six corridor quantities on each of four intervals, and `s=10 min q`.
8. The `s=10` rational log enclosure, negative `W(10)=E[b psi(u_10)]`, and full `t^2 I''(t)` curvature lower bound including Fisher and acceleration terms.
9. The decimal-display patch for (5.1), only as a presentation closure.

## Excluded Scope

This follow-up does not certify:

1. Any joint-additive appendix or later PR76/s9/s10 material.
2. Whole-legal-chord concavity.
3. General dense correlated rank-two concavity.
4. Novelty, publication priority, Lean/formal verification, or CI.
5. Any result obtained by executing the checker in this review. This is a static audit of an existing raw computation packet and its JSON outputs.

## Evidence Standard

I did not rely on `MACHINE_PASS` labels by themselves. I inspected the independent implementation's construction and failure conditions, the JSON output fields, the source binding, the recorded exact-comparison list, and the presentation patch. File SHA-256 hashes from `corridor_input_binding.json` were checked against the local files; all 25 matched.
