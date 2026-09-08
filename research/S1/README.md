# S1: fixed scalar stationary DPP entropy rate

Status: STOPPED_SUBSTANTIVE. Original conjecture: INCOMPLETE. Baseline: `fa504ec74e16843fafc395880d7ba99b4c1d2129`.

This route studies Lyons–Steif Conjecture 9.2 for fixed scalar symbols on the circle. The first unit uses an even real centre and an odd real, multiharmonic perturbation. Finite-window diagnostics and genuine entropy-rate certificates are recorded separately.

The frozen contract is [frozen_theorem_v1.md](frozen_theorem_v1.md). Public coordination: [issue #19](https://github.com/randomcat4/dpp-entropy-tools/issues/19). Work is restricted to `research/S1/`; phase, rate, and review tasks have separate checkouts and branches.

Two fixed rational degree-three pairs have strictly negative true-rate enclosures. The B0 baseline is accepted by two independent non-author reviewers. The phase task's P0 pair uses a variational residual refinement accepted by the non-author rate reviewer. This round has concluded with no unmanaged jobs.

| Pair | True rate-gap enclosure, nats | Evidence |
|---|---|---|
| B0 | [-2.620485e-5,-2.605148e-5] approximately | [Proof](main/rate_certificate_proof.md), [exact interval](main/rational_rate_n8.json), [two review records](verifications/rate_audit.md) |
| P0 | [-5.826509e-6,-4.724191e-6] approximately | [Refinement and application](main/variational_boundary_proof.md), [exact interval](main/phase_rate_n8.json) |

The displayed decimals are summaries; the JSON rational endpoints are the certificate objects. Each interval comes from infinite-past kernel error bounds, exact event determinants and interval logarithms at past length eight. No fitted limit or entropy-rate derivative is used.

The two declared phase units computed 54 finite harmonic Hessians and 30 chord distributions without a positive direction. The single-imaginary-edge and parity restriction lemmas passed independent review within their stated finite scope. These findings do not exclude a full coefficient family or solve Conjecture 9.2.

See [verdict](verdict.md), [checkpoint](checkpoint.json), [work ledger](rounds.md), and [Draft PR #22](https://github.com/randomcat4/dpp-entropy-tools/pull/22). The remaining substantive obligation is a different controlled mixed-edge mechanism or a fixed feasible symbol pair whose certified endpoint lower rate bound exceeds the centre upper bound.
