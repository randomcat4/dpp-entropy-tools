#!/usr/bin/env python3
"""RETIRED_KNOWN_FAILING: this entry point is deliberately disabled.

The original PR112 companion fails at t=1/2, n=4, mask=1:
old recurrence 65823/1048576 != complete-event mass 65055/1048576.
Its occupied-sign labels are exchanged in the first homogeneous component.
This retirement does not claim that its other assertions have been repaired.

Original source is preserved, without rewriting Git history, at:
https://github.com/randomcat4/dpp-entropy-tools/blob/2c249eb5ebc11217d7f87b51a0ce8ea51fea21db/research/I05-DPP-27-lifted-cone-20260910/check_exact.py

See sources_and_attempts.md for evidence withdrawal and handoff.
The NEW evidence_repair/diagnose_retired_checker.py is only a single-case
failure diagnostic. It is not a replacement full checker or interval proof.
"""

raise SystemExit(
    "RETIRED_KNOWN_FAILING: no AUTHOR_EXACT_PASS is available from this file. "
    "See sources_and_attempts.md. The wide interval certificate is withdrawn."
)
