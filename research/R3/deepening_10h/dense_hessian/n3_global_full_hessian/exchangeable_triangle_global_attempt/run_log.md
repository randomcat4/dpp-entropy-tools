# D10-U10h author run log

Date: 2026-09-08. Working directory is this exchangeable_triangle_global_attempt
unit. Only this newly owned directory was changed. No shared-index edits,
commits, server jobs, child agents, GPU use, or dependency installation.

Replay command, standard Python 3.11+:

```text
python sanity.py
```

The first run exited 0 with 86/86 exact/high-precision cases and all symbolic
identities passing. After adding the explicit prime-log witness and the
diagonal coordinate-normalization explanation to the proof, the same script
was cleanly rerun to refresh its proof hash; exit 0, unchanged numerical
results. There were no failed executions, rejected inputs, random proposals,
or unrecorded restarts. All finite points are fixed explicitly in the script.

The calculation uses only Fraction, Decimal (150 digits), and other Python
standard-library modules. It does not import U10f or another author's
implementation. Exact inclusion Möbius values are independently reconstructed
at every finite point; the Fisher and log-coefficient claims are also checked
as polynomial identities with denominators cleared.

Frozen hashes:

| File | SHA256 |
| --- | --- |
| frozen_problem.md | fe527abc03d4014a743cf3b8327eb31c7ebaae6087b16583e81f17542d56bec7 |
| proof_or_blocker.md | 5f527d94e08b831c111d17d94fff2f50f73415b626f58900dc84904aaa7e852c |
| sanity.py | 240e43c71cc248b57d4289cd4d8f4812aa9289860e8bf3de41f09b0f05760b94 |
| sanity.json | 68bc5f503e36b634a45f7c0888762d442c478eb8de5bb6ce3aae82a8ab997cec |

Read-only U10f proof and non-author audit hashes are additionally recorded
in sanity.json. The new boundary strips remain proof candidates pending
fresh independent review. The entire triangle domain remains INCOMPLETE.
