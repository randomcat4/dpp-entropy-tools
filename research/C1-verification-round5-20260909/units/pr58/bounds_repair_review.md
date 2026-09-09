# PR58 additive bounds repair review

Overall verdict: `CORRECT / ACCEPTED_SCOPED` for the repaired additive finite-witness text at head `89aa874c24dd5a3ea98f8474826392560b1d0397`.

The previous PR76 findings are preserved: the original run still stopped at the first false literal bound, and there is still no new all-literals machine PASS. The latest author text now repairs the false (3.5) decimal, withdraws the unsupported author-W decimal in (3.6), and explicitly states that the corrected claims are deductions from retained PR76 rational enclosures rather than a rerun.

Unless a longer alias is written explicitly, source paths below are under `source-snapshots/pr58_bounds_repair/`.

## Source binding

Verdict: `CORRECT / ACCEPTED_SCOPED`.

The binding records parent `ce9ade6d57469f0a4a67365604c66eb4cc290fc5`, scope limited to one-file revised literal bounds/evidence interpretation, commit `89aa874c24dd5a3ea98f8474826392560b1d0397`, one changed file, blob `09ab0a14f2a096e732730561c194fd730a14a8ef`, four additions, four deletions, and hash verification at `SOURCE_BINDING.json:2-14`. I verified this bound file has 15 lines. The binding states that matrices, formulas, code, and output are unchanged, with no rerun and no new machine pass at `SOURCE_BINDING.json:3`.

## Repaired (3.5) bound

Verdict: `CORRECT / ACCEPTED_SCOPED`; the former `NEEDS_FIX` item is closed.

The repaired text now says the retained independent PR76 enclosures support the revised bounds at `ADDENDUM_JOINT_ADDITIVE.md:199`, keeps (3.4) unchanged at `ADDENDUM_JOINT_ADDITIVE.md:201-203`, and replaces the false upper bound in (3.5) with

`R_add < 4(P+A_2)^2/A_2 < 166.441251953051541`

at `ADDENDUM_JOINT_ADDITIVE.md:205-209`.

This is directly supported by the already reviewed PR76 raw evidence: the retained outward interval for `T` is `[166.441251953051540106785812, 166.441251953051540106785813]`, and the repaired decimal is a coarser strict upper bound above that stored upper endpoint. The new paragraph cites the same interval at `ADDENDUM_JOINT_ADDITIVE.md:231`, matching `source-snapshots/pr76_additive/outputs/run01/08_comparisons_N80.json:32-57` and `source-snapshots/pr76_additive/outputs/run01/final.json:3-34`.

## Repaired (3.6) W statement

Verdict: `CORRECT / ACCEPTED_SCOPED` for the qualitative sign; the former unsupported author-W decimal is no longer asserted.

The repaired text changes (3.6) to the qualitative statement `W(9/10)<0` at `ADDENDUM_JOINT_ADDITIVE.md:213-217`. The final paragraph explains the PR76 label correction: run01's field labelled `W` denotes `V=E_mu[y psi]=s^2 W`, gives the retained negative `V` interval, notes `s^2>0`, and says this supports only the qualitative author-W sign while withdrawing the former author-W decimal at `ADDENDUM_JOINT_ADDITIVE.md:231`.

This matches the prior PR76 source/evidence finding. The retained PR76 evidence supports run-labelled `V<0`; together with the stated positive scaling relation, that supports `W<0` qualitatively. It does not certify the former decimal `W(9/10)<-2.253552138695407`, and the repaired source no longer asks it to.

## Qualitative witness and curvature statement

Verdict: `CORRECT / ACCEPTED_SCOPED`.

The repaired text keeps the conclusion that the joint-additive compensation criterion fails strictly at this legal point at `ADDENDUM_JOINT_ADDITIVE.md:211`. This remains supported because the retained PR76 evidence has `L>T` after the (3.5) decimal repair.

The repaired text keeps (3.7), `t^2I''(t)>4.653598245398841>0`, at `ADDENDUM_JOINT_ADDITIVE.md:219-223`, and then states `H''(t)<0` at `ADDENDUM_JOINT_ADDITIVE.md:225`. The final paragraph gives the retained direct complete-curvature interval `[4.653598245398841812928176,4.653598245398841812928177]` at `ADDENDUM_JOINT_ADDITIVE.md:231`, matching the already reviewed PR76 interval evidence. Positive `t^2 I''` hence negative entropy curvature remains accepted scoped.

The final paragraph also preserves the first-mismatch history, original code/output status, and post-launch request correction, and explicitly denies a rerun or new all-literals machine PASS at `ADDENDUM_JOINT_ADDITIVE.md:231`. That wording matches the evidence packet and avoids overstating the repair.

## Latest finite-readiness status

At head `89aa874c24dd5a3ea98f8474826392560b1d0397`, the PR58 joint-additive finite witness is `ACCEPTED_SCOPED` as source/evidence for:

- the fixed rational legal point and additive-table convention closed in prior reports;
- the dual lower bound and qualitative `L>T` failure/non-necessity of the joint-additive sufficient criterion;
- the qualitative `W<0` sign after W/V separation;
- positive `t^2 I''` and hence negative entropy curvature `H''` at the point.

Remaining limits:

- There is no new PR76 all-literals PASS; the historical first mismatch remains part of the record.
- The original PR76 code/output were not changed or rerun.
- The former author-W decimal is withdrawn rather than certified.
- This is a finite fixed-witness closure, not a whole-chord result, formal proof, novelty certification, or broad theorem beyond the already scoped analytic results.
