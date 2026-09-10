# PR82 p4/p8 code review

No executable code changes were reviewed. This packet is a mathematical source-review packet consisting of Markdown proof notes, source bindings, and primary-source references.

No inline code comments are attached.

Review-relevant documentation issues:

- `input/I05-DPP-31-pr66-lowreg-20260910/c4_response_p4_repair.md` lines 402--448 contain the old boundary discussion. It is superseded by `c4_response_p4_boundary_correction.md` lines 1--7. This is acceptable inside the packet because the priority rule is explicit, but standalone reuse should either preserve both files together or annotate the stale subsection directly.
- `input/I05-DPP-31-pr66-lowreg-20260910/c4_response_p4_source_audit.md` is an author proof note, not independent review evidence. It is useful as an index to source claims but should not be cited as a SECOND/FIRST validation.
- `input/I05-DPP-31-pr66-lowreg-20260910/c4_response_p8.md` remains a p>8 checkpoint. Its `(6.7)` finite-memory derivative convergence and analytic framing must not be silently imported into the p>4 finite-response repair.

No build/test commands, mathematical enumeration, entropy recomputation, determinant/log arithmetic, or formal checker runs were performed.
