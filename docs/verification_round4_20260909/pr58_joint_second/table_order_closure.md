# Table-order closure for PR58 joint-additive addendum

Verdict: `CORRECT` for the bounded presentation-only patch.

This closure only addresses the actionable presentation note in `review_report.md`: the addendum should state the row/column enumeration for the displayed `8 x 8` interaction table. It does not certify any finite numerical witness, rational/log interval bound, entropy computation, or original corridor computation.

## Patch binding

New author head:

`ce9ade6d57469f0a4a67365604c66eb4cc290fc5`

Parent reviewed in the prior report:

`5ab3cae1c49da8334057596f46a4bd8fc449b98c`

Patch file:

`docs/verification_round4_20260909/pr58_joint_second/table_order_patch.diff`

Patch SHA-256:

`2dbdee1f7d1b0c395849027acf1a503a26580516da05439c85a06f599257bdaf`

## Delta inspected

The patch changes only `research/I05-23-middle-20260909/ADDENDUM_JOINT_ADDITIVE.md` at the prose immediately before the integer interaction table. The original frozen text introduced the table at `input/ADDENDUM_JOINT_ADDITIVE.md` lines 171-182 without naming the enumeration.

The patch replaces that lead-in with a sentence stating that rows and columns both use subset-mask order `0,1,...,7`, where bit `i` records presence of coordinate `i+1` in the corresponding three-coordinate block.

## Check against frozen author code

The patch matches the frozen checker interface:

- `input/code/verify_joint_additive_failure.py` lines 14-15 define `subs(n)` as `range(1<<n)`, so three-coordinate subsets are enumerated by integer masks `0,...,7`.
- Lines 17-20 use bit `i` of a mask to determine whether coordinate index `i` is present in the event matrix. With mathematical coordinate names starting at `1`, this is exactly "bit `i` records coordinate `i+1`."
- Lines 76-79 iterate `sm` and `tm` using `subs(3)`.
- Lines 94-97 index the dual table as `dual[sm][tm]` and use the corresponding atom probability in the Cauchy denominator.

Thus the presentation patch makes the markdown table self-contained with respect to the code's ordering convention. It changes no formulas, no table entries, no source figures, and no proof logic.

## Scope retained

The prior review classifications remain unchanged:

- analytic joint-additive proof units: `CORRECT`;
- static code interface for the finite witness: `CORRECT`;
- concrete `s=9/10` numerical strict witness: `INCOMPLETE`;
- original `[3,15]` / `s=10` computation: `INCOMPLETE`;
- whole dense correlated legal chord, formal proof, and novelty: `INCOMPLETE`.

No new arithmetic, SymPy, interval, entropy, formal, remote, PR76, C1, or other review material was used for this closure. No prior report or author source file was edited.
