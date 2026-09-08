# Command log

All commands were run from the local Windows checkout
`C:\game\gameproject\showa100\math\i05-successors-20260909\N3\children\inequality\repo`
unless noted otherwise.  BLAS/OpenMP thread variables were set to `1` for
the Python sanity checks.

## Baseline and required reads

- `Get-Content -LiteralPath 'C:\Users\UIO\.agents\skills\math-theorem\SKILL.md' -Raw`
  - exit status: 0
  - PID: not captured in this preliminary read
- `Get-Content` for `references/prompt-library.md` and
  `references/openai-workflow.md`
  - exit status: 0
  - PID: not captured in this preliminary read
- Git branch/head/status and AGENTS lookup
  - branch: `research/N3-inequality-20260909`
  - head: `fa504ec74e16843fafc395880d7ba99b4c1d2129`
  - status: clean at that point
  - exit status: 0
  - PID: not captured in this preliminary read
- Required project reads:
  - `AGENTS.md`: read successfully
  - `COMMON_HANDOFF.md`: read successfully with private connection lines
    redacted from displayed output
  - `N3_HANDOFF.md`: requested path was absent
  - main frozen theorem:
    `C:\game\gameproject\showa100\math\i05-successors-20260909\N3\repo\research\N3\frozen_theorem_v1.md`
    read successfully
  - exit status: 0 for the read command, with a path-not-found diagnostic for
    the missing `N3_HANDOFF.md`
  - PID: not captured in this preliminary read
- `rg --files` under the N3 round directory to locate handoff-like files
  - found no `N3_HANDOFF.md`
  - exit status: 0
  - PID: not captured in this preliminary read
- `Get-Content` for `BASELINE.json`, `docs/dispatch_20260909.md`, and root
  `README.md`
  - baseline: `fa504ec74e16843fafc395880d7ba99b4c1d2129`
  - exit status: 0
  - PID: not captured in this preliminary read

## Local checks

- Checked whether `research\N3\inequality` already existed.
  - result: missing
  - exit status: 0
  - PID: not captured
- Attempted to run the sanity check with the default `python` command.
  - result: Windows app alias reported Python was not found
  - exit status: 1
  - PID: not captured
- Loaded Codex workspace dependencies.
  - Python:
    `C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`
  - bundle version: `26.905.11957`
- Ran the 50-case Fisher lower-bound sanity check with bundled Python.
  - PID: `63712`
  - Python: `3.12.14`
  - NumPy: `2.3.5`
  - seed: `20260909`
  - cases: `50`
  - result: `min_F_minus_Qk = 3.505181e-01`
  - exit status: 0
- Created `research\N3\inequality`.
  - PID: `65136`
  - exit status: 0
- Rechecked the reported full-direction `max Q_k` failure with bundled
  Python and an approximate decimal direction.
  - PID: `57400`
  - Python: `3.12.14`
  - NumPy: `2.3.5`
  - result: `maxQ_minus_cofactor = -0.5552967965780338`,
    while `B = 8.574421097913286`
  - exit status: 0
- Ran `git status --short; git diff --check; git diff -- research/N3/inequality`.
  - PID: `66864`
  - result: only untracked `research/N3/` was present; `git diff --check`
    reported no issue on tracked files
  - exit status: 0
- Ran `git status --porcelain=v1 --untracked-files=all`.
  - PID: `11504`
  - result: four untracked files under `research/N3/inequality`
  - exit status: 0
- Rechecked the simplified rational full-direction `max Q_k` failure reported
  by the main instance:
  `K=(1/100)[[30,29,15],[29,33,10],[15,10,16]]`,
  `D=diag(1,1,1/3)`.
  - PID: `44196`
  - Python: `3.12.14`
  - NumPy: `2.3.5`
  - result: `maxQ_minus_cofactor = -1.9116985259272132`,
    while `B = 30.995287360637487`
  - exit status: 0
- Ran `git add -N research/N3/inequality; git diff --check; git diff --stat;
  git diff -- research/N3/inequality`.
  - PID: `57692`
  - result: `git diff --check` passed; Git printed normal Windows line-ending
    warnings for the new Markdown files
  - exit status: 0
- Ran `git diff --check; git status --porcelain=v1 --untracked-files=all;
  git add research/N3/inequality; git commit -m "Add N3 slice Fisher
  inequality note"`.
  - PID: `53932`
  - result: `git diff --check` passed, files staged, commit failed because
    this isolated checkout had no Git author identity configured
  - exit status: 1
- Ran `git config user.name 'Codex'; git config user.email 'codex@local'`.
  - PID: `66044`
  - result: repo-local author identity set to `Codex <codex@local>`
  - exit status: 0
- Ran `git add research/N3/inequality; git diff --cached --check; git commit
  -m "Add N3 slice Fisher inequality note"; git rev-parse HEAD; git status
  --short`.
  - PID: `42108`
  - result: commit `cafbcaec27e881468f39013079684bbcb2aaa258`; worktree
    clean after commit
  - exit status: 0
- Ran a one-point Sherman-Morrison matrix sanity check for
  `K=(1/100)[[30,29,15],[29,33,10],[15,10,16]]` using bundled Python.
  - PID: `37076`
  - Python: `3.12.14`
  - NumPy: `2.3.5`
  - result: `detN=2.4429101938261777`,
    `alpha=0.20425865117804817`, `beta=0.038934504578526256`,
    `gamma=0.9842540583580244`, `s=0.2034946887003654`;
    `c(D_A)=1.0000000000000002`, `A(D_A)=1/s=4.914133171664467`;
    normalised suppression ratio `0.5058597255353982`
  - exit status: 0
- Ran `Get-Content` on this command log tail and checked `git status --short`
  after a failed patch attempt.
  - PID: `55776`
  - result: worktree was clean; no partial failed-patch modification remained
  - exit status: 0
- Ran `git diff --check; git diff --stat; git diff -- research/N3/inequality;
  git status --short` after adding the optimiser lemma.
  - PID: `67060`
  - result: `git diff --check` passed; Git printed normal Windows line-ending
    warnings; status showed three modified tracked files and one untracked
    optimiser lemma
  - exit status: 0

## Notes

No GPU was used.  No system dependencies were installed.  No global Git,
SSH, proxy, or environment settings were modified.  The only Git
configuration change was repo-local author identity in this isolated
checkout.  No command accessed `C:\canglan\`.
