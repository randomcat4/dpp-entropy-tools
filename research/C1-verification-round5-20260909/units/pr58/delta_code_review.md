# PR58 delta static code review

Reviewed file: `source-snapshots/pr58_delta/code/verify_joint_additive_failure.py`.

Overall static-code status: CORRECT.

Scoped verdict: ACCEPTED_SCOPED for source-level implementation shape, with finite conclusions still INCOMPLETE until C2 independently reconstructs the exact witness.

## Findings

No blocking static implementation bug was found. The checker mirrors the addendum's finite witness structure: it imports exact rational arithmetic and SymPy at `source-snapshots/pr58_delta/code/verify_joint_additive_failure.py:1`-`6`, defines the matrix fixture and `s=9/10` at `source-snapshots/pr58_delta/code/verify_joint_additive_failure.py:7`-`12`, builds event determinants and probabilities at `source-snapshots/pr58_delta/code/verify_joint_additive_failure.py:14`-`31`, and checks rank, density, strict marginal blocks, and Schur legality at `source-snapshots/pr58_delta/code/verify_joint_additive_failure.py:33`-`39`.

The code's enumeration path is consistent with the stated mathematics. It derives the marginal atoms at `source-snapshots/pr58_delta/code/verify_joint_additive_failure.py:41`-`44`, constructs certified logarithm intervals by rational atanh enclosure at `source-snapshots/pr58_delta/code/verify_joint_additive_failure.py:46`-`63`, checks the dual table row and column sums at `source-snapshots/pr58_delta/code/verify_joint_additive_failure.py:70`-`72`, and loops over all `64` complete events at `source-snapshots/pr58_delta/code/verify_joint_additive_failure.py:74`-`97`. The loop includes the event probabilities, conditional inverse blocks, `a`, `b`, `q`, `u`, `y`, `Phi`, `psi`, `A2`, `W`, the true curvature sum, and the dual numerator and denominator.

The strict gates are expressed as assertions at `source-snapshots/pr58_delta/code/verify_joint_additive_failure.py:99`-`105`, and the printed summary at `source-snapshots/pr58_delta/code/verify_joint_additive_failure.py:107`-`117` matches the saved output categories in `source-snapshots/pr58_delta/output/verify_joint_additive_failure.txt:1`-`11`.

## Reproducibility notes

The script depends on SymPy but the delta packet does not include a pinned dependency file or interpreter version. It also uses Python `assert` statements as proof gates, so the intended verification run must not disable assertions. These are reproducibility notes rather than discovered source-code failures.

The script prints decimal approximations after exact or interval assertion gates. I found no static indication that a floating-point comparison is being used to prove a strict sign.

## Scope boundary

This review did not execute the script, recompute intervals, run SymPy, or perform any finite diagnostic arithmetic. The saved output is author evidence only. Independent theorem-grade finite evidence must come from the C2 reconstruction described in `delta_review_report.md`.
