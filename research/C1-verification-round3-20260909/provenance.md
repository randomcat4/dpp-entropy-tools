# Provenance and independence

Three fresh GPT-5.5/xhigh non-author contexts own PR41, PR43 E–H, and PR43
D/I–N respectively. They may not spawn descendants. Their reports and checks
will be published in separate unit directories. A fourth fresh context was
started for PR41's second review only after its first report completed,
within the same three-child concurrency ceiling.

C1 prepares the source map, tests statement/proof consistency, checks external
dependencies and integrates reports. It does not self-approve substantive
author changes and does not merge main. C3 is the sole integration owner.

Source snapshots are fetched by immutable GitHub commit and retained outside
the review worktree. The original PR43 snapshot and the later overlay remain
separate. Public source links identify the exact commits. Local operational
paths and infrastructure details are not needed to reproduce the mathematics.

C1 child checks are bounded fixed jobs, one numerical thread and up to 8 GiB
per child, initially 600 seconds. The line limit is eight CPU / 32 GiB, no GPU.
Scripts, frozen plans, exact inputs, outputs, versions, process identifiers,
exit codes and failed attempts are retained. C2 separately owns the full
computation lane under issue #45; its evidence will be cited only after reading.

Public report copies replace operational absolute paths with repository/source
references and omit infrastructure-only details. The mathematical text,
limitations, failure records and verdicts are preserved.
