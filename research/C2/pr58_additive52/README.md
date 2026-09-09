# PR58 joint-additive fixed witness: literal-bound discrepancy

The independent run stopped at the first exact discrepancy: the strict upper
bound on T in equation(3.5) is false at its printed decimal endpoint. The
qualitative separation survives the raw interval checks, but the original
literal certificate does not receive MACHINE_PASS.

[Status](STATUS.md), [machine notes](machine_notes.md), and the
[run ledger](execution/RUN_LEDGER.json) describe the result and provenance.
The [first mismatch](outputs/run01/final.json),
[complete scalar intervals](outputs/run01/07_scalar_enclosures_N80.json),
[ordered comparisons](outputs/run01/08_comparisons_N80.json), and
[all64events](outputs/run01/04_events.json) retain exact numerator/denominator
strings and outward decimals. Inputs and independent source were frozen before
launch; no author checker was read, imported or executed.

A [post-launch correction](execution/CONTRACT_CORRECTION.md) fixes C3's request:
run01's W means V=E_mu[y psi]=s^2 W_author. The failed T upper bound does not
depend on this naming error. The author W decimal comparison is unverified;
the request-caused scale mismatch is not an author discrepancy.

Run01 ended with exit20 at16:22:48UTC, before its unchanged16:31:24UTC deadline.
All arithmetic stopped, with no repair, retry, overlap or expansion. C1/C3 own
the source repair and subsequent review decision. This finite machine packet
is not an entropy-concavity counterexample or a whole-chord result.

The [original frozen request](inputs/REQUEST.md),
[post-launch request correction](inputs/REQUEST_CORRECTION.md), and
[source binding](inputs/SOURCE_BINDING.json) preserve the contract history.