# C1 first reviews: PR53 and PR54

Status: original FIRST reviews, PR54 repair closure, Theorem FR FIRST,
and the separate exponential-Wiener EW FIRST are complete.
C3's FR second is active; EW is ready for C3's independent second.
This successor packet does not amend merged PR49.

The [Theorem EW first report](units/pr53_ew/review_report.md) returns
CORRECT / ACCEPTED_SCOPED at `73cdbd09ad9aa975354a116a01f1e0f4955a8c27`
for all seven changed/added files frozen in frozen_theorem_v4.md. It accepts
true local quartic strict entropy-rate concavity for arbitrary-mean strict
half-period centers in the exponentially weighted Wiener algebra, without
a small-Wiener-norm assumption. The infinite-range weighted inverse,
remote-condition estimate and inherited RPF/rate/KL steps pass. The exact
Schur block identity and weaker Hölder convergence merit non-blocking
exposition clarification. The companion checker/output were inspected,
not run; they certify only finite example constants.

The [Theorem FR first report](units/pr53_fr/review_report.md) independently
accepts the separately added 473-line source at abdd660a:
CORRECT / ACCEPTED_SCOPED for local finite-range quartic strict entropy-rate
concavity. Its verdict is separate from the original five-file packet.
The fixed weaker Hölder exponent, direct RPF citation and Section 7 heading
have non-blocking exposition recommendations. No global interval is certified.

- [PR53 report](units/pr53/review_report.md): ACCEPTED_SCOPED for all four
  bridge/locality/operator claims at `e0688fbb713e55f93acf791b83437ddf2cc06b7f`.
- [PR54 report](units/pr54/review_report.md): the main local-curvature,
  matching and rate-deficit results are ACCEPTED_SCOPED at
  `203f7044815faac9a2de7bc8dbc5bfe249026b1f`. Its original Section 5
  NEEDS_FIX findings are now CLOSED / ACCEPTED_SCOPED by the
  [bounded repair review](units/pr54/section5_delta_review.md) at
  `a1e7f7208262565bb3db0509ff0cccffab757e98`. The original report is
  preserved; the closure checks only the three requested repairs.

Neither report proves whole-chord or whole-interval entropy-rate concavity.
There is no C1 second review. C3 owns subsequent independent reviews and
the separate first and second audits of all four PR54 appendix units.
Other author changes after the frozen commits are not covered by these
original-unit verdicts.

Read [STATUS.md](STATUS.md), [the frozen contract](frozen_theorem_v1.md),
[the claim ledger](lemma_ledger.md), and [the version ledger](rounds.md).
Each unit includes its independently frozen scope and immutable source binding.
The `source-snapshots/` aliases in exported reports refer to the public source
commits linked in the frozen contract, not to extra files in this review PR.

No new computation was needed or run. The author fixture/diagnostic outputs
were inspected with their source, without treating stored output as a new
execution or generic theorem certificate. Formal coverage is L0 environment
only; no new Lean theorem was checked. Novelty and priority are unassessed.
