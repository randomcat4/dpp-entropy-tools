# S1 round 2

Status: STOPPED_SUBSTANTIVE. Original conjecture: INCOMPLETE. Parent local/server checkpoint 44ca50718b63ce5cb5d688bebe2dd6ef981cccc5. Round-one files and review bindings are preserved.

This unit lifts the even/odd exploratory restriction, uses fixed non-even scalar centres and general cosine/sine affine directions, and retains the Fisher cost. See [frozen contract](frozen_theorem_v1.md), [baseline](baseline_candidate.json), [checkpoint](checkpoint.json), [decision PR #25](https://github.com/randomcat4/dpp-entropy-tools/pull/25), and original [issue #19](https://github.com/randomcat4/dpp-entropy-tools/issues/19).

The fixed non-even B1 chord has a strict negative three-symbol rate enclosure, with outward-rounded summary [-3.034891e-5,-7.346045e-6] nats. The authoritative endpoints are the rational values in the [certificate](rate/artifacts/r2_rate_n4.json); see the [proof](rate/proof_or_certificate.md). All three symbols were evaluated independently using six variational boundary kernels. Past length four already sufficed.

Two distinct phase units plus the main baseline covered 19 non-equivalent centres and 38 full finite Hessians at windows six/eight. All were negative numerically. The second unit uses complex spectral factors outside the first coefficient feasibility ball, with unit-circle roots in four cases. These floating results do not exclude a family. [Execution coverage](coverage.md) separates prechecks, exact certificates and replays.

The [independent finite review](review/review_report.md) accepts the B1 reconstruction and the [finite one-complex-edge concavity proof](main/single_complex_edge.md) within their stated scopes. The [separate rate audit](review/rate_certificate_audit_report.md) accepts the fixed negative gap, recomputes all six residuals and independently rebuilds all 288 exact event probabilities. Both reports come from the same one non-author reviewer; they are not counted as two reviewers. Frozen files retain their historical author-status labels; subsequent acceptance is recorded separately rather than rewriting the audited objects.

See [verdict and reopening condition](verdict.md), [checkpoint](checkpoint.json), [unit ledger](rounds.md), [phase findings](phase/README.md) and [source conditions](prior_art.md). A future positive finite signal still needs the true three-symbol gate (L_-+L_+)/2-U_0>0. No automatic retry or larger search batch is created.
