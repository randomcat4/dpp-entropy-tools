# C1 independent finite-kernel verification

Status: COMPLETE for the five frozen review units below. Each acceptance
is limited to its linked report and source version.

This branch contains only C1's nonauthor review, independently written
checks and retained computation records. The public author sources remain
at their own immutable PR commits. C3 is the sole main-branch integrator.
The earlier C1-authored PR30 is outside this review's self-acceptance scope.

| Item | Frozen input | Current independent status |
|---|---|---|
| W1 round one, rank-one cross block | PR32 / 7c6e40bb3ba6dd0537f3c49bba83c718f86462fb | ACCEPTED_SCOPED: Theorem T and its stated closed-boundary extension |
| W1 round two, two actual coordinate columns | PR32 / a8c337826ec87cf09a0cf63ea5dcd4de5de70dc8, R2 directory only | ACCEPTED_SCOPED: real m-by-2 and actual two-column/row support extensions |
| W4 normalized-interaction T1--T3 | PR33 / 0f06eef1dc723058b46596ff9b704d7e97d3522f; unchanged at a0869b44 | ACCEPTED_SCOPED: all six directions on Omega, closure chords and connected-graph strictness |
| C3 radial finite and true-rate theorem | PR29 / 648f1906468e3e548410f98a6b1a53a978f2ea11 | ACCEPTED_SCOPED: radial finite theorem and lines through a constant scalar symbol |
| C3-M1 fixed-object true-rate certificate | Same PR29, separate from radial theorem | ACCEPTED_SCOPED: the fixed three-symbol negative pair gap only |

PR33 later head a0869b44bdce75acb8c2438806b21d3cf013e508 adds only
AUTHOR_CHECKPOINT.md. The GitHub comparison shows no change to the frozen
mathematical payload or scripts. Its listed round-two avenues are plans,
not completed or accepted theorems. A version change is checked for scope
before an existing review can apply to it.

PR32 later head a8c337826ec87cf09a0cf63ea5dcd4de5de70dc8 adds 21 files
under `research/I05-W1-20260909-R2/` only. Its first-round payload is
unchanged. The first completed W1 report records the historical absence of
the R2 manuscript at that review's freeze; a separate completed review now
accepts the supplied R2 manuscript in its stated scope. The R2 verdict
comes from that new review, not from transferring the first-round verdict.

The first accepted unit and its evidence are in
[READY_BATCH_01.md](READY_BATCH_01.md) and
[the W1 review](children/w1/W1_INDEPENDENT_REVIEW.md).
The two separately accepted C3 units are in
[READY_BATCH_02.md](READY_BATCH_02.md), with their full reports and replay
records under `children/c3/`.
The separately reviewed W1 R2 unit is in
[READY_BATCH_03.md](READY_BATCH_03.md). Historical first-round scope and
plan files are preserved; the later versions have explicit `round2` names.
The final W4 unit is in [READY_BATCH_04.md](READY_BATCH_04.md). Its first
timeout and rejected interval implementation are retained separately from
the corrected seven-center certificate. The W1 one-character editorial
fix is bound in [the source-delta note](main/W1_SOURCE_DELTA.md).

The allowed statuses are ACCEPTED_SCOPED, NEEDS_FIX, REFUTED or INCOMPLETE.
Every acceptance must name the exact theorem and quantifiers it covers;
an execution pass is not a proof, an interval certificate applies only to
its displayed object, and finite entropy data cannot replace a true-rate
error argument. Historical source review opinions are not inherited as
independent evidence in this run.

Heavy arithmetic runs only in the authorized isolated C1 server directories,
with one thread per child, no GPU and at most 8 GiB per child initially.
The line-wide ceiling is eight CPU and 32 GiB. Plans freeze certificate
targets and stop conditions before execution. Scripts, inputs, outputs and
runtime/exit records are distributed with each accepted review; no
checksum inventory is requested for this round.

Results were handed off incrementally through separate review PRs after
earlier batches were merged. There is no main merge performed by C1 and
no new open-ended exploration route. Mathematical novelty and all stated
out-of-scope generalizations remain unassessed.
